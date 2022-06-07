import logging
from typing import ClassVar, List, Optional, Tuple, Type

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import serializers

from jaspr.apps.common.mixins import AssureNonFieldErrorsMixin
from jaspr.apps.kiosk.models import Patient
from jaspr.apps.kiosk.authentication import JasprTokenAuthentication, JasprTokenAuthenticationNoRenew

logger = logging.getLogger(__name__)


class JasprBaseView(AssureNonFieldErrorsMixin, APIView):
    authentication_classes = ()
    def get_authenticators(self):
        if self.request.headers.get("Heartbeat") == "ignore":
            return [JasprTokenAuthenticationNoRenew()]
        elif self.authentication_classes:
            return [auth() for auth in self.authentication_classes]
        return [JasprTokenAuthentication()]

    def get_serializer_context(self):
        return {"request": self.request, "view": self, "format": self.format_kwarg}


class NativeEmailAndMobilePhonePatientMatchingMixin:
    data_check_serializer: ClassVar[Type[serializers.Serializer]]
    tools_to_go_status_whitelist: ClassVar[List[str]] = [
        Patient.TOOLS_TO_GO_EMAIL_SENT,
        Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
        Patient.TOOLS_TO_GO_SETUP_FINISHED,
    ]

    def check_email_and_phone_and_maybe_extra_data(
            self: JasprBaseView, request: Request
    ) -> Tuple[str, str]:
        serializer = self.data_check_serializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return data["email"], data["mobile_phone"]

    @classmethod
    def check_patient(cls, email: str, mobile_phone: str) -> Optional[Patient]:
        try:
            patient = Patient.objects.select_related("user").get(
                user__email__iexact=email,
                tools_to_go_status__in=cls.tools_to_go_status_whitelist,
            )
        except Patient.DoesNotExist:
            return None
        # NOTE: Have to compare `mobile_phone` in python instead of in the database
        # because the database `mobile_phone` field is currently encrypted.
        if patient.user.mobile_phone != mobile_phone:
            return None
        return patient
