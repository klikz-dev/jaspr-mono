import logging
from rest_framework import status
from rest_framework.response import Response

from jaspr.apps.epic.models import NotesLog
from jaspr.apps.kiosk.models import AssignedActivity
from jaspr.apps.kiosk.activities.errors import ActivityValidationError
from jaspr.apps.kiosk.activities.question_json import camelcase_to_underscore
from jaspr.apps.kiosk.narrative_note import NarrativeNote

from ..permissions import (
    HasRecentHeartbeat,
    HasAccessAssessmentObj,
    IsAuthenticated,
    IsInER,
    IsPatient,
    SatisfiesClinicIPWhitelistingFromPatient,
)
from .base import JasprBaseView

logger = logging.getLogger(__name__)

class PatientInterviewAnswersView(JasprBaseView):
    """Expects a PATCH/PUT of assessment answers

    /v1/patient/answers
    """

    permission_classes = (
        IsAuthenticated,
        IsPatient,
        HasAccessAssessmentObj,
        IsInER,
        SatisfiesClinicIPWhitelistingFromPatient,
        HasRecentHeartbeat
    )

    def patch(self, request):
        activity = request.GET.get('activity')
        encounter = request.auth.jaspr_session.encounter

        answers = {}
        for key in request.data:
            cased_key = camelcase_to_underscore(key)
            answers[cased_key] = request.data[key]

        if activity:
            assigned_activity = AssignedActivity.objects.get(pk=activity)
            locked = assigned_activity.locked

            if locked:
                return Response({"nonFieldErrors": ["activity is locked"]}, status=status.HTTP_400_BAD_REQUEST)

        is_takeaway = request.query_params.get('takeaway', False)

        try:
            encounter.save_answers(answers, takeaway_kit=is_takeaway)
        except ActivityValidationError as e:
            data = {e.field: [e.message]}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        answers = encounter.get_answers()

        if is_takeaway:
            note = NarrativeNote(encounter)
            try:
                note.save_stability_plan_note(trigger="Takeaway Edit")
            except Exception as e:
                if NotesLog.error_messages["duplicate"] not in e.messages:
                    raise e
            try:
                note.save_narrative_note(trigger="Takeaway Edit")
            except Exception as e:
                if NotesLog.error_messages["duplicate"] not in e.messages:
                    raise e

        return Response(
            answers,
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        encounter = request.auth.jaspr_session.encounter
        answers = encounter.get_answers()
        return Response(
            answers,
            status=status.HTTP_200_OK,
        )
