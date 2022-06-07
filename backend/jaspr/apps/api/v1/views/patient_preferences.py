import logging
from rest_framework.response import Response
from .base import JasprBaseView

from ..permissions import (
    HasRecentHeartbeat,
    IsAuthenticated,
    IsInER,
    IsPatient,
    SatisfiesClinicIPWhitelistingFromPatient,
)
from ..serializers import (
    PatientPreferencesSerializer
)

logger = logging.getLogger(__name__)


class PatientPreferencesView(JasprBaseView):
    serializer_class = PatientPreferencesSerializer

    permission_classes = (
        HasRecentHeartbeat,
        IsAuthenticated,
        IsPatient,
        IsInER,
        SatisfiesClinicIPWhitelistingFromPatient,
    )

    @staticmethod
    def get(request):
        encounter = request.auth.jaspr_session.encounter
        preferences = encounter.department.get_preferences()
        serializer = PatientPreferencesSerializer(preferences)
        return Response(serializer.data)
