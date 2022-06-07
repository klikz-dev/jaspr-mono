"""
`verify.py` deals with verifying phone numbers. Currently we are using Twilio Verify
for this (https://www.twilio.com/verify).
"""
import logging
from typing import Callable, Dict, Literal, NoReturn, Optional, Tuple, Union

from django.conf import settings
from django_twilio.client import twilio_client
from twilio.base.exceptions import TwilioRestException
from twilio.rest.verify.v2.service.verification import VerificationInstance
from twilio.rest.verify.v2.service.verification_check import VerificationCheckInstance

logger = logging.getLogger(__name__)


VERIFY_SERVICE_CONTEXT = twilio_client.verify.services(settings.TWILIO_VERIFY_SID)


class VerificationException(Exception):
    error_message: str


class VerificationCodeInvalid(VerificationException):
    error_message = "Invalid verification code."

    def __init__(self) -> None:
        super().__init__(self.error_message)


class VerificationCodeNotFound(VerificationException):
    error_message = (
        "Verification codes are only valid for 10 minutes and are not "
        "valid once already approved or more than five attempts have been made within "
        "10 minutes. If you're seeing this message, try resending another code."
    )

    def __init__(self) -> None:
        super().__init__(self.error_message)


class VerificationTwilioException(VerificationException):
    SEND = "send"
    CHECK = "check"
    GENERIC = "generic"
    # https://www.twilio.com/docs/api/errors#6-anchor
    TWILIO_CODE_MAP: Dict[int, Union[str, Tuple[str, Callable]]] = {
        60202: (
            "Too many attempts to check the verification code for your phone "
            "number have occurred in the last 10 minutes. Wait for a bit and then "
            "request a new code and try again. If this message keeps showing up, "
            "please contact support."
        ),
        60203: (
            "A verification code for your phone number has been requested too many "
            "times in the last 10 minutes. Wait for a bit and then try again. If this "
            "message keeps showing up, please contact support."
        ),
        60205: (
            "The phone number we have on file for you is a landline phone number and "
            "it cannot receive text messages. Please contact support to get your phone "
            "number changed to a non-landline one."
        ),
        60207: ("twilio_code", lambda service: 60202 if service == "check" else 60203),
        60212: ("twilio_code", lambda service: 60202 if service == "check" else 60203),
    }
    STATUS_CODE_MAP: Dict[int, str] = {
        404: ("exception_class", lambda service: VerificationCodeNotFound),
        429: ("twilio_code", lambda service: 60202 if service == "check" else 60203),
        500: GENERIC,
        503: GENERIC,
    }
    GENERIC_ERROR_MESSAGE = (
        "We ran into an issue communicating with your phone. Try again after "
        "a few seconds. If this message keeps showing up, please contact support."
    )

    def __init__(self, error_message: str) -> None:
        self.error_message = error_message

    @classmethod
    def raise_from_twilio_rest_exception(
        cls,
        exception: TwilioRestException,
        service: Literal[SEND, CHECK],
        user_id: Optional[str] = None,
    ) -> NoReturn:
        exception_class = cls
        exception_class_args = "default"
        handled_specifically = True
        if (code := exception.code) is not None and code in cls.TWILIO_CODE_MAP:
            error = cls.TWILIO_CODE_MAP[code]
        elif (status := exception.status) is not None and status in cls.STATUS_CODE_MAP:
            error = cls.STATUS_CODE_MAP[status]
        else:
            error = cls.GENERIC_ERROR_MESSAGE
            handled_specifically = False
        if isinstance(error, tuple):
            alias, decider = error
            if alias == "twilio_code":
                twilio_code = decider(service)
                error_message = cls.TWILIO_CODE_MAP[twilio_code]
            else:
                exception_class = decider(service)
                exception_class_args = ()
        elif error == cls.GENERIC:
            error_message = cls.GENERIC_ERROR_MESSAGE
        else:
            error_message = error
        logger.info(
            (
                "(user_id=%s, twilio_error_code=%s, status_code=%s, "
                "handled_specifically=%s, twilio_msg=%s) Raising %s from %s (%s)."
            ),
            str(user_id),
            str(exception.code),
            str(exception.status),
            str(handled_specifically),
            exception.msg,
            str(exception_class.__name__),
            str(exception.__class__.__name__),
            str(exception),
        )
        if exception_class_args == "default":
            raise exception_class(error_message) from exception
        raise exception_class(*exception_class_args) from exception


def send_phonenumber_verification(
    phone_number: str, user_id: Optional[str] = None
) -> VerificationInstance:
    try:
        return VERIFY_SERVICE_CONTEXT.verifications.create(
            to=phone_number, channel="sms"
        )
    except TwilioRestException as e:
        VerificationTwilioException.raise_from_twilio_rest_exception(
            e, VerificationTwilioException.SEND, user_id=user_id
        )


def check_phonenumber_verification(
    phone_number: str, code: str, user_id: Optional[str] = None,
) -> VerificationCheckInstance:
    try:
        verification_check = VERIFY_SERVICE_CONTEXT.verification_checks.create(
            to=phone_number, code=code
        )
    except TwilioRestException as e:
        VerificationTwilioException.raise_from_twilio_rest_exception(
            e, VerificationTwilioException.CHECK, user_id=user_id
        )
    if verification_check.status == "pending":
        raise VerificationCodeInvalid
    elif verification_check.status == "denied":
        raise VerificationCodeNotFound
    # At this point we return the `VerificationCheckInstance` and the calling code can
    # assume the verification is valid.
    return verification_check
