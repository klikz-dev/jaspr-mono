import logging
from typing import Any, Dict, Tuple

from django.db import transaction
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_variables
from django.utils.decorators import method_decorator

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers, status

from .base import JasprBaseView
from jaspr.apps.kiosk.models import (
    JasprSession,
    JasprSessionError,
    Technician
)
from ..serializers import (
    JasprSessionCreateSerializer,
    TechnicianSetPasswordSerializer,
    ReadOnlyAuthTokenSerializer
)
from ..permissions import (
    HasValidJasprSetPasswordToken,
    IsAuthenticated,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
)
from jaspr.apps.kiosk.authentication import (
    JasprExtraSecurityTokenAuthentication,
)
from jaspr.apps.common.decorators import drf_sensitive_post_parameters

logger = logging.getLogger(__name__)


class TechnicianActivateSetPasswordView(JasprBaseView):
    authentication_classes = (JasprExtraSecurityTokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        SatisfiesClinicIPWhitelistingFromTechnician,
        HasValidJasprSetPasswordToken,
    )

    def get_jaspr_session_context(self, technician: Technician) -> Dict[str, Any]:
        return {
            "request": self.request,
            "user": technician.user,
            "user_type": "Technician",
            "in_er": True,
            # Currently, Technicians only activate on the web.
            "from_native": False,
            "long_lived": False,
            "log_user_login_attempt": True,
            "save": True,
        }

    def create_jaspr_session(self, technician: Technician) -> Tuple[JasprSession, str]:
        serializer = JasprSessionCreateSerializer(
            data=self.request.data, context=self.get_jaspr_session_context(technician)
        )
        # NOTE: At the time of writing we really shouldn't hit this exception, but
        # wrapping it anyway to avoid throwing any 500s and giving a hopefully helpful
        # error message if anything did arise.
        try:
            serializer.is_valid(raise_exception=True)
            return serializer.save()
        except JasprSessionError as e:
            raise serializers.ValidationError(e.error_message) from e

    def get_token_response_data(
            self, jaspr_session: JasprSession, token_string: str
    ) -> Dict[str, Any]:
        return ReadOnlyAuthTokenSerializer(
            jaspr_session.auth_token, context={"token_string": token_string}
        ).data

    @method_decorator(drf_sensitive_post_parameters())
    @method_decorator(sensitive_variables("token", "set_password_token", "password"))
    @method_decorator(never_cache)
    def post(self, request: Request):
        serializer = TechnicianSetPasswordSerializer(
            self.request.user.technician,
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            technician = serializer.save()
            jaspr_session, token_string = self.create_jaspr_session(technician)
            return Response(
                data=self.get_token_response_data(jaspr_session, token_string),
                status=status.HTTP_200_OK,
            )