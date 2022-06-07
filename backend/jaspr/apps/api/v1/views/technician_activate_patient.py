import logging

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from jaspr.apps.kiosk.authentication import login_patient, logout_kiosk_user
from jaspr.apps.kiosk.models import ActivateRecord

from ..permissions import (
    IsAuthenticated,
    IsInER,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
)
from ..serializers import (
    ActivateExistingPatientSerializer,
    ReadOnlyAuthTokenSerializer,
)
from .base import JasprBaseView

logger = logging.getLogger(__name__)


class TechnicianActivatePatientView(JasprBaseView):
    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SatisfiesClinicIPWhitelistingFromTechnician,
        # The SharesClinic permission is handled by the serializer
    )

    def post(self, request):
        # This route is only for activating patients in a Non-EHR setting.  In an EHR setting, patients are activated
        # through the /patient/tablet-pin route
        serializer = ActivateExistingPatientSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        technician = request.user.technician
        from_native = request.auth.jaspr_session.from_native
        with transaction.atomic():
            patient = serializer.save()
            logout_kiosk_user(request.auth)
            # Log in the Patient (if we log in here, then we are marking `in_er`
            # `True` since we're in the emergency room if activated by a Technician).

            encounter = patient.current_encounter

            if not encounter.start_time:
                encounter.start_time = timezone.now()
                encounter.save()

            # TODO Set start time on all linked activities if they have not yet been started and update status fields

            jaspr_session, token_string = login_patient(
                patient=patient,
                request=request,
                encounter=encounter,
                log_user_login_attempt=True,
                in_er=True,
                from_native=from_native,
                long_lived=False,
                save=True,
            )
            # Record a successful activation for the Patient by the Technician.
            ActivateRecord.objects.create(
                technician=technician,
                patient=patient,
                new=False,
                encounter=encounter
            )
        return Response(
            ReadOnlyAuthTokenSerializer(
                jaspr_session.auth_token, context={"token_string": token_string}
            ).data,
            status=status.HTTP_200_OK,
        )
