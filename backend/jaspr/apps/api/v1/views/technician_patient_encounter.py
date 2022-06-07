import logging

from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from jaspr.apps.kiosk.models import Encounter, Patient, Technician
from jaspr.apps.api.v1.serializers import ReadOnlyTechnicianPatientSerializer

from ..permissions import (
    IsAuthenticated,
    IsInER,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
)
from .base import JasprBaseView

logger = logging.getLogger(__name__)

def technician_has_access_to_encounter(technician: Technician, encounter: Encounter) -> bool:
    count = technician.departmenttechnician_set \
        .filter(status="active", department=encounter.department).count()
    if count > 0:
        return True
    return False


class TechnicianPatientEncounterView(JasprBaseView):
    """
    Allow technicians to create new patient sessions and define the patient path
    """

    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SatisfiesClinicIPWhitelistingFromTechnician,
    )

    def post(self, request: Request) -> Response:
        patient_id = request.data.get("patient")
        patient = Patient.objects.get(pk=patient_id)
        current_encounter = patient.current_encounter

        if not technician_has_access_to_encounter(request.user.technician, current_encounter):
            return Response("Access Denied", status=status.HTTP_403_FORBIDDEN)

        Encounter.objects.create(patient=current_encounter.patient, department=current_encounter.department)

        patient_serializer = ReadOnlyTechnicianPatientSerializer(
            instance=current_encounter.patient,
            context = self.get_serializer_context()
        )

        return Response(status=status.HTTP_201_CREATED, data=patient_serializer.data)

