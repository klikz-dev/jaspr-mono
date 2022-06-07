import logging
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response

from jaspr.apps.kiosk.constants import ActionNames
from jaspr.apps.kiosk.jobs import (
    queue_action_creation,
)
from ..permissions import (
    HasRecentHeartbeat,
)

from .base import JasprBaseView

from ..permissions import (
    IsAuthenticated,
    IsInER,
    IsPatient,
    SatisfiesClinicIPWhitelistingFromPatient,
)

logger = logging.getLogger(__name__)


class PatientSessionLockView(JasprBaseView):
    """Accepts Heartbeat POST of {} from frontend.
    Returns 204 No Content.
    Locks Session, requiring a validate-session call to unlock.
    """

    permission_classes = (
        IsAuthenticated,
        IsPatient,
        IsInER,
        SatisfiesClinicIPWhitelistingFromPatient,
        HasRecentHeartbeat,
    )

    def post(self, request, **kwargs):
        encounter = self.request.auth.jaspr_session.encounter
        encounter.account_locked_at = timezone.now()
        encounter.session_lock = True
        encounter.save()
        patient = self.request.user.patient
        queue_action_creation(
            {
                "action": ActionNames.LOCKOUT,
                "patient": patient,
                "encounter": encounter,
                "in_er": request.auth.jaspr_session.in_er,
            }
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
