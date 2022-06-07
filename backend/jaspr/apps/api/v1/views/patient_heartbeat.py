import logging

from rest_framework import status
from rest_framework.response import Response

from ..permissions import (
    HasRecentHeartbeat,
)

from .base import JasprBaseView

from ..permissions import (
    IsAuthenticated,
    IsPatient,
)

logger = logging.getLogger(__name__)


class PatientHeartbeatView(JasprBaseView):
    """ Accepts Heartbeat POST from frontend """

    permission_classes = (IsAuthenticated, IsPatient, HasRecentHeartbeat)

    def post(self, request, **kwargs):
        # `HasRecentHeartbeat` will update `last_heartbeat` if valid.
        return Response(status=status.HTTP_204_NO_CONTENT)
