import logging
from datetime import timedelta
from typing import Mapping, Optional, Tuple, Union

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils import timezone
from django_rq import job
from django_twilio.client import twilio_client
from rq.job import Job
from twilio.base.exceptions import TwilioRestException

from jaspr.apps.accounts.models import User
from jaspr.apps.message_logs.models import EmailLog, SMSLog

from .rq import enqueue_in

logger = logging.getLogger(__name__)


def message_user_from_template(
    user: Union[User, int],
    base: str,
    context: Optional[Mapping] = None,
    from_email: Optional[str] = None,
) -> Union[Job, Tuple[Job, Job]]:
    if isinstance(user, int):
        user = User.objects.get(id=user)
    if user.preferred_message_type == "email":
        return email_user_from_templates(user.id, base, context, from_email=from_email)
    elif user.preferred_message_type == "sms":
        return text_user_from_templates(user.id, base, context)
    elif user.preferred_message_type == "email and sms":
        sms_job = text_user_from_templates(user.id, base, context)
        email_job = email_user_from_templates(
            user.id, base, context, from_email=from_email
        )
        return email_job, sms_job


def find_sms_title(base: str, context: Mapping) -> str:
    title_path = f"{base}_sms_title.txt"
    try:
        title = render_to_string(title_path, context=context)
    except TemplateDoesNotExist as first_e:
        logger.info(
            f"Couldn't find title at {title_path}, falling back to email subject."
        )
        email_subject_path = f"{base}_email_subject.txt"
        try:
            title = render_to_string(email_subject_path, context=context)
        except TemplateDoesNotExist as second_e:
            raise TemplateDoesNotExist(
                "Couldn't find a title for the SMS log to use.",
                tried=first_e.tried + second_e.tried,
                # They both use the same backend, so just pick the second one here.
                backend=second_e.backend,
                chain=first_e.chain + second_e.chain,
            )
    return "".join(title.splitlines()).strip()


def text_user_from_templates(
    user_id: int, base: str, context: Optional[Mapping] = None
) -> Job:
    if context is None:
        context = {}
    title = find_sms_title(base, context)
    body = render_to_string(f"{base}_sms.txt", context=context).strip()
    return text_user.delay(user_id, title, body)


def email_user_from_templates(
    user_id: int,
    base: str,
    context: Optional[Mapping] = None,
    from_email: Optional[str] = None,
) -> Job:
    if context is None:
        context = {}
    subject = "".join(
        render_to_string(f"{base}_email_subject.txt", context=context).splitlines()
    ).strip()
    txt = render_to_string(f"{base}_email.txt", context=context)
    try:
        context["MEDIA_URL"] = settings.MEDIA_URL
        html = render_to_string(f"{base}_email.html", context=context)
    except TemplateDoesNotExist:
        html = None
    return email_user.delay(user_id, subject, txt, html=html, from_email=from_email)


@job
def email_engineering(
    subject: str,
    txt: str,
) -> Job:
    """
    Sends a message to the engineering team
    """
    try:
        send_mail(
            subject,
            txt,
            settings.DEFAULT_FROM_EMAIL,
            ["dev@ebpi.org"],
            # If it fails silently, then `email_response` should be '0'
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Error sending email in background job. Error: {str(e)}")


@job
def email_support(
    subject: str,
    txt: str,
) -> Job:
    """
    Sends a message to the customer support team
    """

    try:
        send_mail(
            subject,
            txt,
            settings.DEFAULT_FROM_EMAIL,
            ["support@jasprhealth.com"],
            # If it fails silently, then `email_response` should be '0'
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Error sending email in background job. Error: {str(e)}")


@job
def email_user(
    user_id: int,
    subject: str,
    txt: str,
    html: Optional[str] = None,
    from_email: Optional[str] = None,
) -> int:
    """
    Returns the id of the EmailLog created.
    """
    user = User.objects.get(id=user_id)
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    response = None
    try:
        response = send_mail(
            subject,
            txt,
            from_email,
            [user.email],
            html_message=html,
            # If it fails silently, then `email_response` should be '0'
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Error sending email in background job. Error: {str(e)}")

    return EmailLog.objects.create(
        user=user,
        user_email=user.email,
        from_email=from_email,
        date=timezone.now(),
        subject=subject,
        text_body=txt,
        html_body=html or "",
        # '1' or '0'
        email_response=response,
    ).id


@job
def text_user(
    user_id: int, title: str, body: str, existing_sms_log_id: Optional[int] = None
) -> int:
    """
    Returns a dictionary (`{id: str, status: str}`) of the SMS Log if
    certain exceptions weren't raised earlier.
    """
    user = User.objects.get(id=user_id)
    phone_number = user.mobile_phone
    if not phone_number:
        raise AttributeError(f"User {user} does not have a mobile phone number set.")
    if existing_sms_log_id:
        sms_log = SMSLog.objects.get(id=existing_sms_log_id)
    else:
        sms_log = SMSLog.objects.create(
            recipient=user, mobile_phone=phone_number.as_e164, title=title, body=body
        )
    message_sid = ""
    try:
        message = twilio_client.messages.create(
            to=phone_number.as_e164, from_=settings.TWILIO_PHONE_NUMBER, body=body
        )
    except TwilioRestException:
        logger.exception(f"Exception when sending text message, SMS Log: {sms_log}")
    else:
        message_sid = message.sid
    if existing_sms_log_id:
        # If an existing SMS Log ID was passed in, we know this is a retry, so we increment
        # `times_retried`. Any job that runs after this, like `retry_text_user`,
        # can use this number to determine what to do.
        sms_log.times_retried = F("times_retried") + 1
    if message_sid:
        sms_log.status = "sent"
    else:
        sms_log.status = "retry"
    sms_log.message_id = message_sid
    sms_log.save()
    if sms_log.status == "retry":
        # NOTE: It's important that if this implementation ever changes, that this happens
        # after `save()` is called. Could also abstract this sort of functionality into
        # a decorator.
        retry_text_user.delay(sms_log.id)
    return sms_log.id, sms_log.status


@job
def retry_text_user(sms_log_id: int) -> Mapping[str, Union[int, str]]:
    """
    Returns a dictionary (`{id: str, status: str}`) of the SMS Log after
    queueing a retry for sending the SMS.
    """
    sms_log = SMSLog.objects.get(id=sms_log_id)
    if sms_log.status == "sent":
        return {"id": sms_log.id, "status": sms_log.status}
    if sms_log.times_retried <= 2:
        text_user.delay(
            sms_log.recipient_id,
            sms_log.title,
            sms_log.body,
            existing_sms_log_id=sms_log.id,
        )
    elif sms_log.times_retried <= 5:
        enqueue_in(
            timedelta(hours=6),
            text_user,
            sms_log.recipient_id,
            sms_log.title,
            sms_log.body,
            existing_sms_log_id=sms_log.id,
        )
    else:
        sms_log.status = "failed"
        sms_log.save()
    return sms_log.id, sms_log.status
