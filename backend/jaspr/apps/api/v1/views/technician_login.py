import logging

from django.db import transaction

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions, status

from ..serializers import (
    TechnicianUserLoginSerializer,
    ReadOnlyAuthTokenSerializer
)

from .login_base import LoginBaseView

logger = logging.getLogger(__name__)


class TechnicianLoginView(LoginBaseView):
    """Expects a POST of email, password and organization_code
    Returns token if successful.
    Unsuccessful requests return validation errors as a 400 BAD REQUEST

    /v1/technician/login
    """

    def post(self, request: Request):
        login_serializer = TechnicianUserLoginSerializer(
            data=request.data, context={"request": request, "view": self}
        )
        login_serializer.is_valid(raise_exception=True)
        user = login_serializer.validated_data["user"]

        # Technician should log in using the web app and enter from the proper
        # subdomain.
        if (
                user.is_technician
                and (technician := getattr(user, "technician", None))
                and login_serializer.validated_data.get("organization_code")
                == technician.system.organization_code
        ):
            # We want to create/log the failed login attempt that could happen above, so we
            # don't start the transaction until now.
            with transaction.atomic():
                jaspr_session, token_string = self.create_jaspr_session(
                    user, "Technician", True, long_lived=False, from_native=False
                )
        else:
            raise exceptions.PermissionDenied

        return Response(
            ReadOnlyAuthTokenSerializer(
                jaspr_session.auth_token, context={"token_string": token_string}
            ).data,
            status=status.HTTP_200_OK,
        )