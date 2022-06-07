import logging

from rest_framework import status
from rest_framework.response import Response

from .base import JasprBaseView

from jaspr.apps.jah.models import PrivacyPolicyAcceptance

from ..permissions import (
    IsAuthenticated,
    IsPatient,
)

logger = logging.getLogger(__name__)


class PatientPrivacyPolicyAcceptanceView(JasprBaseView):
    """Accepts POST of {} from frontend.
    Returns 204 No Content.
    Adds a new acceptance record of the privacy policy.  When the policy
    changes, we need to update the default value for version in the model.
    We can then force all users that don't have a record for a specific version
    to accept the new policy.  Note: The created date on the model is synonymous
    with the time the policy was accepted by the user
    """

    permission_classes = (
        IsAuthenticated,
        IsPatient,
    )

    def post(self, request, **kwargs):
        user = self.request.user
        jah_account = user.patient.jahaccount
        PrivacyPolicyAcceptance.objects.create(jah_account=jah_account)

        return Response(status=status.HTTP_204_NO_CONTENT)
