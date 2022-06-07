import logging

from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response

from jaspr.apps.api.v1.serializers import TechnicianEpicNoteToEhrSerializer
from jaspr.apps.api.v1.views.login_base import LoginBaseView
from jaspr.apps.kiosk.models import Encounter
from jaspr.apps.kiosk.narrative_note import NarrativeNote

logger = logging.getLogger(__name__)


class TechnicianEpicNoteToEhrView(LoginBaseView):
    """Expects a POST of assessment_id"""

    def post(self, request: Request):
        technician_epic_note_to_ehr_serializer = TechnicianEpicNoteToEhrSerializer(
            data=request.data, context={"request": request, "view": self}
        )

        technician_epic_note_to_ehr_serializer.is_valid(raise_exception=True)

        # TODO JACOB Get encounter from context?
        encounter_id = technician_epic_note_to_ehr_serializer.data[
            "encounter_id"
        ]

        encounter = Encounter.objects.get(pk=encounter_id)

        narrative_note = NarrativeNote(encounter)

        narrative_note.save_to_epic()

        return Response({}, status=status.HTTP_200_OK)
