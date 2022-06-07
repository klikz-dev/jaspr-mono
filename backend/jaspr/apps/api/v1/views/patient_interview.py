import logging
from .base import JasprBaseView
from rest_framework import status
from rest_framework.response import Response

from ..permissions import (
    HasRecentHeartbeat,
    IsAuthenticated,
    IsInER,
    IsPatient,
    SatisfiesClinicIPWhitelistingFromPatient,
)
from jaspr.apps.api.v1.serializers import AssignedActivitySerializer

logger = logging.getLogger(__name__)


class PatientInterviewView(JasprBaseView):
    permission_classes = (
        IsAuthenticated,
        IsPatient,
        IsInER,
        SatisfiesClinicIPWhitelistingFromPatient,
        HasRecentHeartbeat,
    )

    @staticmethod
    def get(request):
        encounter = request.auth.jaspr_session.encounter
        questions = AssignedActivitySerializer(encounter.filter_activities(active_only=True), many=True)
        return Response(questions.data, status=status.HTTP_200_OK)





