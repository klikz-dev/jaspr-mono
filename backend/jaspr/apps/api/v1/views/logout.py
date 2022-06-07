import logging

from django.db import transaction

from rest_framework.response import Response
from rest_framework import permissions, status

from rest_condition import And, Or

from .base import JasprBaseView
from ..permissions import (
    IsPatient,
    IsTechnician,
)
from jaspr.apps.kiosk.authentication import (
    logout_kiosk_user,
)

logger = logging.getLogger(__name__)


class LogoutView(JasprBaseView):
    """
    Expects a POST with no data or a single value corresponding to the key
    `manually_initiated`.
    """

    permission_classes = [And(permissions.IsAuthenticated, Or(IsPatient, IsTechnician))]

    def post(self, request):
        with transaction.atomic():
            logout_kiosk_user(
                request.auth, manually_initiated=request.data.get("manually_initiated")
            )
        return Response(status=status.HTTP_200_OK)