import logging
from typing import Any, Dict

from django.db import transaction
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_variables
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework import status

from .base import JasprBaseView
from jaspr.apps.kiosk.models import (
    Patient
)
from ..serializers import (
    CheckPhoneNumberVerificationSerializer,
)
from ..permissions import (
    HasToolsToGoStartedButNotFinished,
    IsAuthenticated,
    IsPatient,
)
from jaspr.apps.kiosk.authentication import (
    JasprToolsToGoUidAndTokenAuthentication,
)
from jaspr.apps.common.decorators import drf_sensitive_post_parameters
from jaspr.apps.kiosk.tokens import JasprSetPasswordTokenGenerator

logger = logging.getLogger(__name__)


class PatientCheckPhoneNumberCodeView(JasprBaseView):
    """
    Endpoint for submitting a `code` and checking to see if that `code` matches the
    most recent, non-expired code texted to that `User`'s `mobile_phone`. If this
    succeeds, the `Patient` that made the request is transitioned to having
    `tools_to_go_status` set to `tools_to_go_status.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED`.
    Additionally, the `Patient` is logged in and the token is returned.
    """

    authentication_classes = (JasprToolsToGoUidAndTokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        IsPatient,
        HasToolsToGoStartedButNotFinished,
    )

    set_password_token_generator = JasprSetPasswordTokenGenerator

    def get_response_data(self, patient: Patient) -> Dict[str, Any]:
        set_password_token = self.set_password_token_generator().make_token(
            patient.user
        )
        return {
            "set_password_token": set_password_token,
        }

    def check_and_update_and_respond(self, patient: Patient) -> Response:
        serializer = CheckPhoneNumberVerificationSerializer(
            data=self.request.data,
            context={**self.get_serializer_context(), "user": patient.user},
        )
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            # Only update the `tools_to_go_status` if it was previously "Email Sent".
            if patient.tools_to_go_status == Patient.TOOLS_TO_GO_EMAIL_SENT:
                patient.tools_to_go_status = Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED
                patient.save()
        return Response(self.get_response_data(patient), status=status.HTTP_200_OK)

    @method_decorator(drf_sensitive_post_parameters())
    @method_decorator(sensitive_variables("token", "set_password_token", "code"))
    @method_decorator(never_cache)
    def post(self, request):
        return self.check_and_update_and_respond(request.user.patient)