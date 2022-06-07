import logging

import random
import string
from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response
from jaspr.apps.kiosk.models import Encounter
from jaspr.apps.api.v1.serializers import TechnicianTabletPinSerializer

from ..permissions import (
    IsAuthenticated,
    IsInER,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
    SharesClinic
)

from .base import JasprBaseView

logger = logging.getLogger(__name__)


class PatientForEncounterSharesClinic(SharesClinic):
    """
    Override `SharesClinic` to set the `patient` from this `ViewSet`
    (since it's not `obj` which is the default).
    """

    def get_patient(self, request, view, obj):
        try:
            return request.auth.jaspr_session.encounter.patient
        except AttributeError:
            try:
                return Encounter.objects.get(pk=request.data.get("encounter")).patient
            except Encounter.DoesNotExist:
                return None

    def has_permission(self, request, view):
        return self.has_object_permission(request, view, None)


class TechnicianTabletPinView(JasprBaseView):
    TIMEOUT = 30 * 60  # 30 Minutes
    CODE_LENGTH = 6

    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SatisfiesClinicIPWhitelistingFromTechnician,
        PatientForEncounterSharesClinic
    )

    @staticmethod
    def generate_code():
        chars = string.ascii_uppercase
        code = "".join(random.SystemRandom().choice(chars) for _ in range(TechnicianTabletPinView.CODE_LENGTH))
        return code


    def post(self, request, **kwargs):
        technician_tablet_pin_serializer = TechnicianTabletPinSerializer(
            data=request.data, context={"request": request, "view": self}
        )
        technician_tablet_pin_serializer.is_valid(raise_exception=True)
        encounter = technician_tablet_pin_serializer.data.get("encounter")
        technician_operated = technician_tablet_pin_serializer.data.get("technician_operated")
        department = encounter.department
        system = encounter.department.clinic.system

        iteration_count = 0
        while True:
            pin = self.generate_code()
            if department.tablet_department_code:
                cache_key = f"pin-code-department-{department.pk}-{pin}"
            elif system.tablet_system_code:
                cache_key = f"pin-code-system-{system.pk}-{pin}"
            else:
                logger.exception(
                    f"This department or system is not configured for PIN entry. dept: {department.pk} system: {system.pk}")
                return Response({"non_field_errors": ["Department not configured for PIN entry"]})

            val_already_exists = cache.get(cache_key)

            if not val_already_exists:
                break

            if iteration_count > 10:
                logger.exception(f"There are to many 6-digit pin collisions for department {department.pk}")
                return Response({"non_field_errors": ["The system is busy, try again later"]})

            iteration_count += 1

        cache.set(cache_key, {
            "encounter": encounter.pk,
            "technician_operated": technician_operated,
            "technician": request.user.technician.pk
        }, self.TIMEOUT)

        return Response({"pin": pin}, status=status.HTTP_201_CREATED)
