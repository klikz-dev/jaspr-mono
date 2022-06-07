import logging

from rest_framework import status
from rest_framework.response import Response

from jaspr.apps.kiosk.models import AssignedActivity, AssignmentLocks
from jaspr.apps.api.v1.serializers import AssignedActivitySerializer

from ..permissions import (
    HasRecentHeartbeat,
    IsAuthenticated,
    IsInER,
    IsPatient,
    SatisfiesClinicIPWhitelistingFromPatient,
)

from .base import JasprBaseView

logger = logging.getLogger(__name__)


class PatientAssignedActivityView(JasprBaseView):
    permission_classes = (
        HasRecentHeartbeat,
        IsAuthenticated,
        IsPatient,
        IsInER,
        SatisfiesClinicIPWhitelistingFromPatient,
    )

    @staticmethod
    def patch(request, activity_id: int):
        try:
            assigned_activity = AssignedActivity.objects.select_related('encounter',
                                                                        'encounter__patient').get(pk=activity_id)
        except AssignedActivity.DoesNotExist:
            return Response("Access Denied", status=status.HTTP_403_FORBIDDEN)

        if assigned_activity.encounter.patient_id != request.user.patient.id:
            return Response("Access Denied", status=status.HTTP_403_FORBIDDEN)
        locked = request.data.get('locked', False)

        if locked:
            assigned_activity.lock()

        return Response(AssignedActivitySerializer(assigned_activity).data, status=status.HTTP_200_OK)

