from typing import List, Tuple

from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_rq.jobs import Job

from jaspr.apps.accounts.models import User
from jaspr.apps.common.jobs.messaging import email_user_from_templates
from jaspr.apps.kiosk.tokens import JasprExtraSecurityTokenGenerator

from ..common.functions import resolve_frontend_url
from .models import Technician
from .tokens import (
    JasprExtraSecurityTokenGenerator,
    JasprPasswordResetTokenGenerator,
    JasprToolsToGoSetupTokenGenerator,
)


def send_technician_activation_email(
    technician: Technician,
    template_base: str = "kiosk/technician_activation",
    *,
    save_technician: bool = True,
) -> Tuple[Job, List[str]]:
    """
    Send the activation email to the technician, returning the associated `Job` that
    is sending the email, and a list of fields that were set on `technician` (for
    cases like in the `Technician` admin where calling code may need to know which
    fields were set so it can do an efficient bulk update).
    """
    assert (
        technician.user.pk is not None
    ), "`Technician`'s `User` must have a `pk` present."
    b64_uid = urlsafe_base64_encode(force_bytes(technician.user.pk))
    token = JasprExtraSecurityTokenGenerator().make_token(technician.user)
    activate_technician_url = (
        f"{settings.BACKEND_URL_BASE}/v1/technician/activate/{b64_uid}/{token}"
    )
    # NOTE: Technically this is actually more like "activation email last queued for
    # delivery at". Could improve this to run synchronously, but it's kind of nice
    # because it's fast to email multiple `Technician`s all at once since we're using
    # background processing.
    technician.activation_email_last_sent_at = timezone.now()
    update_fields: List[str] = ["activation_email_last_sent_at"]
    if save_technician:
        technician.save(update_fields=update_fields)
    return (
        email_user_from_templates(
            technician.user.pk,
            template_base,
            context={"activate_technician_url": activate_technician_url},
        ),
        update_fields,
    )


def send_technician_activation_confirmation_email(
    technician: Technician,
    template_base: str = "kiosk/technician_activation_confirmation",
) -> Job:
    assert (
        technician.user.pk is not None
    ), "`Technician`'s `User` must have a `pk` present."
    frontend_tech_login_url = resolve_frontend_url(technician=technician)
    return email_user_from_templates(
        technician.user.pk,
        template_base,
        context={"frontend_tech_login_url": frontend_tech_login_url},
    )


def send_technician_set_password_confirmation_email(
    technician: Technician,
    template_base: str = "kiosk/technician_set_password_confirmation",
) -> Job:
    assert (
        technician.user.pk is not None
    ), "`Technician`'s `User` must have a `pk` present."
    return email_user_from_templates(
        technician.user.pk,
        template_base,
    )


def send_tools_to_go_setup_email(
    user: User, template_base: str = "kiosk/tools_to_go_setup"
) -> Job:
    b64_uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = JasprToolsToGoSetupTokenGenerator().make_token(user)
    jaspr_setup_url = (
        f"{settings.BACKEND_URL_BASE}/v1/patient/at-home-setup/{b64_uid}/{token}"
    )
    return email_user_from_templates(
        user.pk,
        template_base,
        context={"jaspr_setup_url": jaspr_setup_url},
    )


def send_reset_password_email(
    user: User, template_base: str = "kiosk/reset_password"
) -> Job:
    b64_uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = JasprPasswordResetTokenGenerator().make_token(user)
    jaspr_reset_password_url = (
        f"{settings.BACKEND_URL_BASE}/v1/reset-password/{b64_uid}/{token}"
    )
    return email_user_from_templates(
        user.pk,
        template_base,
        context={"jaspr_reset_password_url": jaspr_reset_password_url},
    )


def send_tools_to_go_confirmation_email(user: User) -> Job:
    jaspr_login_url = resolve_frontend_url()
    return email_user_from_templates(
        user.pk,
        "kiosk/tools_to_go_confirmation",
        context={"jaspr_login_url": jaspr_login_url},
    )
