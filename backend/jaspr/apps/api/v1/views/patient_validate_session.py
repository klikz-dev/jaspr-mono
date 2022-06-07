import logging

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from jaspr.apps.kiosk.models import Encounter

from ..permissions import (
    IsAuthenticated,
    IsInER,
    IsPatient,
    SatisfiesClinicIPWhitelistingFromPatient,
)
from ..serializers import ValidateSessionSerializer
from .base import JasprBaseView

logger = logging.getLogger(__name__)


class PatientValidateSessionView(JasprBaseView):
    permission_classes = (
        IsAuthenticated,
        IsPatient,
        IsInER,
        SatisfiesClinicIPWhitelistingFromPatient,
    )

    @staticmethod
    def validation_failure(max_exceeded=False) -> Response:
        msg = "Incorrect picture or answer. Please try again."
        if max_exceeded:
            msg = "Your account has been locked due to 5 failed attempts."
        return Response({"non_field_errors": [msg]}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, **kwargs):
        with transaction.atomic():
            encounter = (
                Encounter.objects.filter(pk=request.auth.jaspr_session.encounter.pk)
                .select_for_update()
                .get()
            )

            if encounter.session_validation_attempts >= 5:
                return self.validation_failure(max_exceeded=True)
            encounter.session_validation_attempts += 1

            serializer = ValidateSessionSerializer(data=request.data)
            if not serializer.is_valid():
                encounter.save()
                return self.validation_failure()

            expected_answer = getattr(encounter, "encrypted_answer", None)
            if (
                expected_answer is None
                or serializer.validated_data["security_question_answer"]
                != expected_answer
                or serializer.validated_data["image"] != encounter.privacy_screen_image
            ):
                encounter.save()
                return self.validation_failure()
            else:
                encounter.session_validation_attempts = 0
                encounter.last_heartbeat = timezone.now()
                encounter.account_locked_at = None
                encounter.session_lock = False
                encounter.save()
                return Response({}, status=status.HTTP_200_OK)
