import logging
from typing import Any, Dict

from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_variables
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from jaspr.apps.common.decorators import drf_sensitive_post_parameters
from jaspr.apps.kiosk.authentication import (
    JasprExtraSecurityTokenAuthentication,
)
from jaspr.apps.kiosk.models import (
    Technician,
)
from jaspr.apps.kiosk.tokens import JasprSetPasswordTokenGenerator

from ..permissions import (
    IsAuthenticated,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
)
from ..serializers import (
    ActivateTechnicianSerializer,
)
from .base import JasprBaseView

logger = logging.getLogger(__name__)


class TechnicianActivateView(JasprBaseView):
    authentication_classes = (JasprExtraSecurityTokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        SatisfiesClinicIPWhitelistingFromTechnician,
    )

    set_password_token_generator = JasprSetPasswordTokenGenerator

    def get_response_data(self, technician: Technician) -> Dict[str, Any]:
        set_password_token = self.set_password_token_generator().make_token(
            technician.user
        )
        return {
            "set_password_token": set_password_token,
        }

    @method_decorator(drf_sensitive_post_parameters())
    @method_decorator(
        sensitive_variables("token", "set_password_token", "activation_code")
    )
    @method_decorator(never_cache)
    def post(self, request: Request):
        serializer = ActivateTechnicianSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            technician = serializer.save()
            return Response(
                data=self.get_response_data(technician),
                status=status.HTTP_200_OK,
            )