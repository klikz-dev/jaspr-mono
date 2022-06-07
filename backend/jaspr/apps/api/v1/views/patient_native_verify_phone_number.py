import logging

from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status

from .base import JasprBaseView, NativeEmailAndMobilePhonePatientMatchingMixin
from ..serializers import (
    VerifyPhoneNumberSerializer,
    NativeVerifyPhoneNumberFieldCheckSerializer,
)
from jaspr.apps.common.phonenumbers.verify import (
    VerificationException,
)
from jaspr.apps.common.decorators import drf_sensitive_post_parameters

logger = logging.getLogger(__name__)


class PatientNativeVerifyPhoneNumberView(
    JasprBaseView, NativeEmailAndMobilePhonePatientMatchingMixin
):
    """
    Endpoint for submitting `email` and `mobile_phone` and getting a verification
    code sent to the `mobile_phone` if the `email` and `mobile_phone` matches a
    patient in the database and the `Patient`'s `tools_to_go_status` is one of "Email
    Sent" or "Phone Number Verified".

    !Important: This endpoint should _always_ return a 200, and never leak any
    !information about whether or not the text message was actually sent or not.

    NOTE: This is the Native JAH version of `PatientVerifyPhoneNumberView` since, on native,
    it's not desired to have to check for an email or follow an email link. See
    EBPI-825 for frontend info and EBPI-837 for backend info.
    """

    authentication_classes = ()
    permission_classes = ()

    data_check_serializer = NativeVerifyPhoneNumberFieldCheckSerializer

    @method_decorator(drf_sensitive_post_parameters())
    @method_decorator(never_cache)
    def post(self, request):
        email, mobile_phone = self.check_email_and_phone_and_maybe_extra_data(request)
        patient = self.check_patient(email, mobile_phone)
        if patient is None:
            return Response(status=status.HTTP_200_OK)
        try:
            VerifyPhoneNumberSerializer.send_verification(patient.user)
        except VerificationException:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)