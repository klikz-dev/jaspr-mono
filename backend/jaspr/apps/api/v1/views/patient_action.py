import logging

from djangorestframework_camel_case.util import underscoreize
from rest_framework import status
from rest_framework.response import Response

from jaspr.apps.epic.models import NotesLog
from jaspr.apps.kiosk.jobs import queue_action_creation
from jaspr.apps.kiosk.narrative_note import NarrativeNote

from ..permissions import IsAuthenticated, IsPatient
from ..serializers import ActionSerializer
from .base import JasprBaseView

logger = logging.getLogger(__name__)


class PatientActionView(JasprBaseView):
    permission_classes = (IsAuthenticated, IsPatient)

    def post(self, request):
        data = {**request.data}
        if "section_uid" in data:
            # Convert the sent section uid from camel case to snake case.
            data["section_uid"] = [
                *underscoreize(
                    {data["section_uid"]: ""}, no_underscore_before_number=True
                )
            ][0]
        serializer = ActionSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        queue_action_creation(validated_data)

        # Handle arrival triggers
        # Send SSI Note if arrive at SSI end question
        if validated_data.get("section_uid", None) == "talk_it_through":
            encounter = request.auth.jaspr_session.encounter
            note = NarrativeNote(encounter)
            try:
                note.save_narrative_note(trigger="SSI Finish")
            except Exception as e:
                if NotesLog.error_messages["duplicate"] not in e.messages:
                    raise e
        # Send CSP note if arrive at CSP end question
        elif validated_data.get("section_uid", None) == "thanks_plan_to_cope":
            encounter = request.auth.jaspr_session.encounter
            note = NarrativeNote(encounter)
            try:
                note.save_stability_plan_note(trigger="CSP Finish")
            except Exception as e:
                if NotesLog.error_messages["duplicate"] not in e.messages:
                    raise e

        # Don't return any data right now because the frontend doesn't currently
        # use/need the returned data.
        return Response(status=status.HTTP_201_CREATED)
