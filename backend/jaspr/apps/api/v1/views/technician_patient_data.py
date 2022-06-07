import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from ..permissions import (
    IsAuthenticated,
    IsInER,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
    SharesClinic
)
from ..serializers import (
    ActivateExistingPatientSerializer,
    AssignedActivitySerializer,
)
from ..viewsets import (
    ActivityViewSet,
    JasprMediaViewSet,
    PatientVideoViewSet,
)
from jaspr.apps.kiosk.activities.activity_utils import ActivityType
from .base import JasprBaseView

logger = logging.getLogger(__name__)


class TechnicianPatientDataView(JasprBaseView):
    """
    Expects a GET with `department` (primary key) provided as the first argument
    to the URL, and `pk` provided as the second argument.

    NOTE: Some different names (like skills vs. activities) are used in this view.
    The reason for this is to as closely match how the frontend has it set up (early
    January 2020 at the time of writing) and named with the actions and reducers
    there.
    """

    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SatisfiesClinicIPWhitelistingFromTechnician,
        SharesClinic
    )

    def get_skills(self, patient):
        queryset = ActivityViewSet.queryset_for_patient_user(
            ActivityViewSet.queryset.all(), patient.user_id
        )
        serializer = ActivityViewSet.serializer_class(queryset, many=True)
        return serializer.data

    def get_stories_videos(self):
        # NOTE: This is one where the same logic is handled in the filter backend. We
        # want to be careful to keep this in sync if the frontend's request URL/data
        # changes, or if the backend implementation changes. Currently, the frontend
        # requests `.../video?tag=PLE`.
        queryset = JasprMediaViewSet.queryset.filter(tags__name__iexact="PLE")
        serializer = JasprMediaViewSet.serializer_class(queryset, many=True)
        return serializer.data

    def get_patient_videos(self, patient):
        queryset = PatientVideoViewSet.queryset.filter(patient=patient)
        serializer = PatientVideoViewSet.serializer_class(queryset, many=True)
        return serializer.data

    def get_answers(self, patient):
        encounter = patient.current_encounter
        if not encounter:
            return {}
        return encounter.get_answers()

    def get_crisis_stability_plan(self, patient):
        encounter = patient.current_encounter
        if encounter:
            stability_plan = encounter.get_activity(ActivityType.StabilityPlan)
            if stability_plan:
                return stability_plan.get_serializer()(stability_plan).data
        return {}

    def get_questions(self, patient):
        encounter = patient.current_encounter

        if not encounter:
            return {}
        return AssignedActivitySerializer(encounter.filter_activities(active_only=True), many=True).data

    def get(self, request: Request, department: int, patient: int) -> Response:
        validation_serializer = ActivateExistingPatientSerializer(
            data={"department": department, "patient": patient},
            context={"request": request},
        )
        validation_serializer.is_valid(raise_exception=True)
        patient = validation_serializer.validated_data["patient"]
        data = {
            "skills": self.get_skills(patient),
            "stories_videos": self.get_stories_videos(),
            "patient_videos": self.get_patient_videos(patient),
            "answers": self.get_answers(patient),
            "crisis_stability_plan": self.get_crisis_stability_plan(patient),
            "questions": self.get_questions(patient)
        }
        return Response(data=data, status=status.HTTP_200_OK)
