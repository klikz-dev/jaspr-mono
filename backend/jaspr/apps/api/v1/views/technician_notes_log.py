import logging

from django.db.models import Subquery

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from jaspr.apps.kiosk.narrative_note import NarrativeNote
from jaspr.apps.kiosk.models import Technician, Patient, PatientDepartmentSharing, Encounter
from jaspr.apps.epic.models import NotesLog
from jaspr.apps.api.v1.serializers import NotesLogSerializer
from ..permissions import (
    IsAuthenticated,
    IsInER,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
)

from .base import JasprBaseView

logger = logging.getLogger(__name__)


def technician_has_access_to_patient(technician: Technician, patient: Patient) -> bool:
    department_ids = PatientDepartmentSharing.objects.filter(status="active", patient=patient).values_list("department")
    count = technician.departmenttechnician_set.filter(
        status="active",
        department__in=Subquery(department_ids)
    ).count()
    if count > 0:
        return True
    return False

def technician_has_access_to_encounter(technician: Technician, encounter: Encounter) -> bool:
    count = technician.departmenttechnician_set \
        .filter(status="active", department=encounter.department).count()
    if count > 0:
        return True
    return False


def fail(msg, st=status.HTTP_400_BAD_REQUEST):
    return Response(msg, status=st)


class TechnicianNotesLogView(JasprBaseView):
    """
    Triggers the manual creation of a narrative note and stability plan note.  In EHR integrated environments, each
    note is sent to the EHR in addition to a NoteLog being created in the database.  In Non-Integrated environments
    just the NoteLog record is created in the database.  The expectation in non-integrated environments is that the
    technician will manually copy and paste the notes from the frontend into their own record keeping system.
    """

    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SatisfiesClinicIPWhitelistingFromTechnician,
    )

    def post(self, request: Request):
        if "encounter" not in request.data:
            return fail("Request must provide valid encounter")

        if "narrative_note" not in request.data and "stability_plan_note" not in request.data:
            return fail("Must specify at least one note to save")

        try:
            encounter = Encounter.objects.get(pk=request.data["encounter"])
        except Exception as e:
            return fail("Invalid Encounter.")

        tech = request.user.technician

        if not technician_has_access_to_encounter(tech, encounter):
            return fail("Access Denied", st=status.HTTP_403_FORBIDDEN)

        note = NarrativeNote(encounter)

        try:
            note.save_narrative_note(sender=tech, trigger="/technician/notes-log")
        except Exception as e:
            if NotesLog.error_messages["duplicate"] not in e.messages:
                logger.exception("Unable to save narrative note to epic", exc_info=e)
                return Response(
                    {"nonFieldErrors": ["Unable to save narrative note to epic"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            note.save_stability_plan_note(sender=tech, trigger="/technician/notes-log")
        except Exception as e:
            if hasattr(e, 'messages') and NotesLog.error_messages["duplicate"] not in e.messages:
                logger.exception("Unable to save stability plan note to epic", exc_info=e)
                return Response(
                    {"nonFieldErrors": ["Unable to save stability plan note to epic"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"status": "ok"},
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        patient_id = request.GET.get("patient")
        # TODO Throws 500 if query does not return result
        patient = Patient.objects.get(pk=patient_id)
        technician = request.user.technician

        if not technician_has_access_to_patient(technician, patient):
            return fail("Access Denied", st=status.HTTP_403_FORBIDDEN)

        # Get the most recent of each type of note for each of the past encounters.  Only 1 note per type
        # should be shown per encounter, and the current encounter should not be included.
        # Limit to shared departments between the technician and patient to prevent leaking data to unauthorized
        # technicians
        department_ids = technician.departmenttechnician_set.filter(
            status="active",
        ).values_list("department_id")
        notes = NotesLog.objects.filter(
            encounter__patient__id=patient_id,
            encounter__department_id__in=Subquery(department_ids),
        ).exclude(encounter=patient.current_encounter).order_by('encounter__id', 'note_type', '-created').distinct('encounter__id', 'note_type')

        notes_serializer = NotesLogSerializer(notes, many=True)

        return Response(notes_serializer.data, status=status.HTTP_200_OK)
