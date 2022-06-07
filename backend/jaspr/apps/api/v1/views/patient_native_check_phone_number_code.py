import logging
from typing import Any, Dict

from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_variables
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import serializers

from jaspr.apps.kiosk.models import Patient

from ..serializers import NativeCheckPhoneNumberFieldCheckSerializer
from jaspr.apps.kiosk.authentication import (
    JasprResetPasswordUidAndTokenAuthentication,
    JasprToolsToGoUidAndTokenAuthentication,
)
from jaspr.apps.common.phonenumbers.verify import VerificationCodeInvalid
from jaspr.apps.common.decorators import drf_sensitive_post_parameters
from .patient_check_phone_number_code import PatientCheckPhoneNumberCodeView
from .base import NativeEmailAndMobilePhonePatientMatchingMixin

logger = logging.getLogger(__name__)


class PatientNativeCheckPhoneNumberCodeView(
    PatientCheckPhoneNumberCodeView, NativeEmailAndMobilePhonePatientMatchingMixin
):
    """
    Native version of `PatientCheckPhoneNumberCodeView` which differs in that it:
    1. Does not require authentication or permissions (NOTE/TODO: Make sure this is
    rate-limited to some extent at least in the future on some level. Also,
    NOTE/TODO: If there's a way we can restrict this to native in the future that
    might be nice but is not essential).
    2. (Instead of 1. above) Requires `email` and `mobile_phone` to be provided and
    checks them similar to how they are checked in `PatientNativeVerifyPhoneNumberView`.
    3. Additionally provides `uid` and `token` (corresonding to `uid` and `token` in
    `JasprToolsToGoUidAndTokenAuthentication`) in the response if the check was
    successful so that in the `PatientSetPasswordView` can be successfully
    authenticated with in the next request.

    !Important: This endpoint should have consistent responses that never leak any
    !information about whether the `email` and `mobile_phone` point to a `Patient`
    !in the database.

    ^ To satisfy the above requirement, `data_check_serializer` is set to
    `NativeCheckPhoneNumberFieldCheckSerializer` so that the `code` is checked
    for formatting validity before `check_patient` is called. Tests will make sure
    the error messages are the _exact same_ in all the error paths corresponding to
    an invalid token.
    """

    authentication_classes = ()
    permission_classes = ()

    data_check_serializer = NativeCheckPhoneNumberFieldCheckSerializer

    def get_response_data(self, patient: Patient) -> Dict[str, Any]:
        b64_uid = urlsafe_base64_encode(force_bytes(patient.user.pk))
        # The `already_set_up` value determines what flow the `Patient` should take
        # after this point? If they've already set up JAH (tools to go is what it used
        # to be called) then we'll use the token for the reset password flow, otherwise
        # we'll make a token for the setup flow.
        already_set_up = (
                patient.tools_to_go_status == Patient.TOOLS_TO_GO_SETUP_FINISHED
        )
        if already_set_up:
            token = JasprResetPasswordUidAndTokenAuthentication.token_generator().make_token(
                patient.user
            )
        else:
            token = (
                JasprToolsToGoUidAndTokenAuthentication.token_generator().make_token(
                    patient.user
                )
            )
        return {
            "already_set_up": already_set_up,
            "uid": b64_uid,
            "token": token,
            **super().get_response_data(patient),
        }

    @method_decorator(drf_sensitive_post_parameters())
    @method_decorator(sensitive_variables("token", "set_password_token", "code"))
    @method_decorator(never_cache)
    def post(self, request):
        # Because of "code" being in `request.POST` in addition to "email" and
        # "mobile_phone", we have `data_check_serializer =
        # NativeCheckPhoneNumberFieldCheckSerializer` above to make sure "code" is
        # validated here right away in order to make sure that we have consistent error
        # messages that don't leak or reveal any information about whether or not the
        # `Patient` exists from the response data.
        email, mobile_phone = self.check_email_and_phone_and_maybe_extra_data(request)
        patient = self.check_patient(email, mobile_phone)
        if patient is None:
            # In order to hide potentially sensitive data or revealing information
            # about what happened, if we can't find the `Patient`, we just go with the
            # default error message about an invalid code.
            raise serializers.ValidationError(VerificationCodeInvalid.error_message)
        return self.check_and_update_and_respond(patient)