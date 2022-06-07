import logging

from rest_framework import status
from rest_framework.response import Response

from ..permissions import (
    HasRecentHeartbeat,
    IsAuthenticated,
    IsInER,
    IsPatient,
    SatisfiesClinicIPWhitelistingFromPatient,
)
from ..serializers import (
    MePatientSerializer,
    ToolsToGoVerificationSetupSerializer,
)

from .base import JasprBaseView

logger = logging.getLogger(__name__)


class PatientToolsToGoVerificationSetupView(JasprBaseView):
    """
    Endpoint for submitting `email` and `mobile_phone` and
    starting the tools to go verification flow process. Expects
    that the `Patient` has `tools_to_go_status` set
    to `Patient.TOOLS_TO_GO_NOT_STARTED`, and enforces that
    at the permissions level.
    """

    permission_classes = (
        IsAuthenticated,
        IsPatient,
        IsInER,
        SatisfiesClinicIPWhitelistingFromPatient,
        HasRecentHeartbeat,
    )

    def post(self, request):
        serializer = ToolsToGoVerificationSetupSerializer(
            self.request.user.patient,
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        updated_patient = serializer.save()
        # Regardless of what happens in the serializer (whether the email already
        # existed or not in the system), send back to the frontend the email that was
        # initially submitted (for security/privacy reasons). See the tests and the
        # comments in the serializer for more information.
        data = {
            **MePatientSerializer(
                updated_patient, context=self.get_serializer_context()
            ).data,
            "email": serializer.validated_data["email"],
        }
        # NOTE: Choosing to use `HTTP_201_CREATED` in order to indicate that we created
        # something (in this sense we sent an email, and created an `EmailLog`). Not
        # sure honestly if `HTTP_200_OK` would be better or make more sense here vs.
        # `HTTP_201_CREATED`.
        return Response(data, status=status.HTTP_201_CREATED)
