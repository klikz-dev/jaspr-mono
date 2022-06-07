import logging
from typing import Sequence
from django.utils import timezone

from jaspr.apps.kiosk.models import ActivateRecord
from jaspr.apps.clinics.models import Clinic, Department, HealthcareSystem
from jaspr.apps.epic.models import EpicDepartmentSettings

from ..serializers import (
    ReadOnlyAuthTokenSerializer,
)

from rest_framework import status
from rest_framework.response import Response
from jaspr.apps.api.v1.serializers import PatientTabletPinSerializer
from jaspr.apps.kiosk.authentication import login_patient

from ..permissions import (
    SatisfiesClinicIPWhitelisting,
)

from .base import JasprBaseView

logger = logging.getLogger(__name__)

class SatisfiesClinicIPWhitelistingFromPatientPin(
    SatisfiesClinicIPWhitelisting
):
    def get_clinics(self, request, view) -> Sequence[Clinic]:
        department_code = request.data.get("department_code")
        system_code = request.data.get("system_code")
        if department_code:
            logger.info(f"Getting Department for Pin Authentication with department code {department_code}")
        if system_code:
            logger.info(f"Getting System for Pin Authentication with system code {system_code}")

        if not department_code and not system_code:
            return []

        if department_code:
            try:
                department = Department.objects.get(tablet_department_code=request.data.get("department_code"))
            except (EpicDepartmentSettings.DoesNotExist, Department.DoesNotExist):
                logger.warning(f"Unable to find department with department code {department_code}")
                return []
            return [department.clinic]
        elif system_code:
            try:
                system = HealthcareSystem.objects.get(tablet_system_code=request.data.get("system_code"))
            except (EpicDepartmentSettings.DoesNotExist, HealthcareSystem.DoesNotExist):
                logger.warning(f"Unable to find system with system code {system_code}")
                return []
            return Clinic.objects.filter(system=system).all()
        return []


class PatientTabletPinView(JasprBaseView):
    permission_classes = (
        SatisfiesClinicIPWhitelistingFromPatientPin,
    )

    def post(self, request, **kwargs):
        patient_tablet_pin_serializer = PatientTabletPinSerializer(
            data=request.data, context={"request": request, "view": self}
        )

        try:
            patient_tablet_pin_serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.warning(f"Pin authentication failed with error {str(e)}")
            raise

        encounter = patient_tablet_pin_serializer.data.get("encounter")
        technician = patient_tablet_pin_serializer.data.get("technician")
        technician_operated = patient_tablet_pin_serializer.data.get("technician_operated", False)
        patient = encounter.patient

        if not encounter.start_time:
            encounter.start_time = timezone.now()
            encounter.save()

        if technician_operated and not encounter.technician_operated:
            encounter.technician_operated = technician_operated
            encounter.save()

        jaspr_session, token_string = login_patient(
            patient=patient,
            request=request,
            encounter=encounter,
            log_user_login_attempt=True,
            in_er=True,
            from_native=False,
            long_lived=False,
            technician_operated=technician_operated,
            save=True,
        )
        # Record a successful activation for the Patient by the Technician.
        ActivateRecord.objects.create(
            technician=technician, patient=patient, new=False
        )

        logger.info(f"Pin authentication successful")
        return Response(
            ReadOnlyAuthTokenSerializer(
                jaspr_session.auth_token, context={"token_string": token_string}
            ).data,
            status=status.HTTP_200_OK,
        )