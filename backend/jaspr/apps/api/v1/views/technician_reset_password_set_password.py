import logging
from typing import Any, Dict, Tuple

from django.db import transaction
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_variables
from django.utils.decorators import method_decorator

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
    ReadOnlyAuthTokenSerializer,
    TechnicianSetPasswordSerializer
)
from ..permissions import (
    IsAuthenticated,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
)
from jaspr.apps.kiosk.authentication import (
    JasprResetPasswordUidAndTokenAuthentication,
)
from jaspr.apps.common.decorators import drf_sensitive_post_parameters

logger = logging.getLogger(__name__)


class TechnicianResetPasswordSetPasswordView(JasprBaseView):
    """
    Currently, view/endpoint for making a `POST` request to set `password` for a `Technician`.
    Requires an authenticated `Technician` along with a valid `token` that passes the token
    generator's `check_token` method. The reason for the `token` is it only allows
    the `password` to be set this way once, and then the `token` would be invalid
    after that (because the hash would change with a new password). If they set the
    password to their same existing password currently then the hash wouldn't change,
    but that's very unlikely given they are here in the first place probably because
    they forgot their password and are setting a new one. Even if that did happen,
    tokens expire after a certain time too and they wouldn't have a way of getting
    that token again unless they got the email sent to them again.

    POST
        /v1/technician/reset-password/set-password

            {
                "uid": "<JasprResetPasswordUID>",
                "token": "<JasprResetPasswordToken>",
                "password": "super-secret-passwlrd"
            }
    """

    authentication_classes = (JasprResetPasswordUidAndTokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        SatisfiesClinicIPWhitelistingFromTechnician,
    )

    def get_jaspr_session_context(self, technician: Technician) -> Dict[str, Any]:
        return {
            "request": self.request,
            "user": technician.user,
            "user_type": "Technician",
            "in_er": True,
            # Currently, Technicians are only entering via web-app.
            "from_native": False,
            # Currently, Technicians are only given short-lived tokens.
            "long_lived": False,
            "log_user_login_attempt": True,
            "save": True,
        }

    def create_jaspr_session(self, technician: Technician) -> Tuple[JasprSession, str]:
        serializer = JasprSessionCreateSerializer(
            data=self.request.data, context=self.get_jaspr_session_context(technician)
        )
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
    def post(self, request):
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
