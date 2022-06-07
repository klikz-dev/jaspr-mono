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
    Patient
)
from ..serializers import (
    JasprSessionCreateSerializer,
    ReadOnlyAuthTokenSerializer,
    PatientSetPasswordSerializer,
)
from ..permissions import (
    HasToolsToGoAtLeastPhoneNumberVerified,
    HasValidJasprSetPasswordToken,
    IsAuthenticated,
    IsPatient,
)
from jaspr.apps.kiosk.authentication import (
    JasprToolsToGoUidAndTokenAuthentication,
)
from jaspr.apps.common.decorators import drf_sensitive_post_parameters

logger = logging.getLogger(__name__)


class PatientSetPasswordView(JasprBaseView):
    """
    Currently, view/endpoint for making a `POST` request to set `password`. Requires
    an authenticated `Patient` along with a valid `token` that passes the token
    generator's `check_token` method. The reason for the `token` is it only allows
    the `password` to be set this way once, and then the `token` would be invalid
    after that (because the hash would change with a new password). If they set the
    password to their same existing password currently then the hash wouldn't change,
    but that's very unlikely given they are here in the first place probably because
    they forgot their password and are setting a new one. Even if that did happen,
    tokens expire after a certain time too and they wouldn't have a way of getting
    that token again unless they got the email sent to them again.
    """

    authentication_classes = (JasprToolsToGoUidAndTokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        IsPatient,
        HasToolsToGoAtLeastPhoneNumberVerified,
        HasValidJasprSetPasswordToken,
    )

    def get_jaspr_session_context(self, patient: Patient) -> Dict[str, Any]:
        return {
            "request": self.request,
            "user": patient.user,
            "user_type": "Patient",
            # If the `Patient` gets logged in this way he/she is not in the ER.
            "in_er": False,
            # Currently, only native is having the session created in with this endpoint.
            "from_native": True,
            # Currently, native only wants long lived from this endpoint.
            "long_lived": True,
            "log_user_login_attempt": True,
            "save": True,
        }

    def create_jaspr_session(self, patient: Patient) -> Tuple[JasprSession, str]:
        serializer = JasprSessionCreateSerializer(
            data=self.request.data, context=self.get_jaspr_session_context(patient)
        )
        # NOTE: At the time of writing all possible combinations of `from_native` and
        # `long_lived` here should be legal since `user_type` is always 'Patient'.
        # However, requirements may change, so wrapping this in the try/except block so
        # that errors are more gracefully caught if we do update requirements and don't
        # update this immediately or forget to change this.
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
        serializer = PatientSetPasswordSerializer(
            self.request.user.patient,
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        create_session = self.request.data.get("auth_token") in (
            "true",
            "True",
            True,
            1,
        )
        with transaction.atomic():
            patient = serializer.save()
            if create_session:
                jaspr_session, token_string = self.create_jaspr_session(patient)
                return Response(
                    data=self.get_token_response_data(jaspr_session, token_string),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(status=status.HTTP_200_OK)