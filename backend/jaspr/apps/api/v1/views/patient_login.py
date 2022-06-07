import logging

from django.db import transaction
from rest_framework.response import Response
from rest_framework import exceptions, status

from ..serializers import (
    ReadOnlyAuthTokenSerializer,
    PatientUserLoginSerializer,
)
from .login_base import LoginBaseView

logger = logging.getLogger(__name__)


class PatientLoginView(LoginBaseView):
    """Expects a POST of email, and password.
    Returns token if successful.
    Unsuccessful requests return validation errors as a 400 BAD REQUEST

    /v1/patient/login
    """

    def post(self, request):
        login_serializer = PatientUserLoginSerializer(
            data=request.data, context={"request": request, "view": self}
        )
        login_serializer.is_valid(raise_exception=True)
        user = login_serializer.validated_data["user"]

        if user.is_patient and hasattr(user, "patient"):
            # We want to create/log the failed login attempt that could happen above,
            # so we don't start the transaction until now.
            with transaction.atomic():
                jaspr_session, token_string = self.create_jaspr_session(
                    user,
                    "Patient",
                    False,
                    # `Patient`s currently can only log in using the native app from
                    # this endpoint.
                    from_native=True,
                    long_lived=login_serializer.validated_data["long_lived"],
                )

        else:
            raise exceptions.PermissionDenied

        return Response(
            ReadOnlyAuthTokenSerializer(
                jaspr_session.auth_token, context={"token_string": token_string}
            ).data,
            status=status.HTTP_200_OK,
        )