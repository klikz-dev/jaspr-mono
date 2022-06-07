import logging

from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_variables
from django.utils.decorators import method_decorator

from rest_framework.response import Response

from .base import JasprBaseView
from ..serializers import (
    PatientChangePasswordSerializer,
)
from ..permissions import (
    HasToolsToGoSetupFinished,
    IsAuthenticated,
    IsPatient,
)
from jaspr.apps.common.decorators import drf_sensitive_post_parameters

logger = logging.getLogger(__name__)


class PatientChangePasswordView(JasprBaseView):
    """
    Currently, view/endpoint for making a `POST` requests to change `password`.
    Requires an authenticated, tools to go "Setup Finished" `Patient` and the
    `current_password` provided that will be checked before setting the new
    `password` supplied.
    """

    permission_classes = (IsAuthenticated, IsPatient, HasToolsToGoSetupFinished)

    @method_decorator(drf_sensitive_post_parameters())
    @method_decorator(sensitive_variables("current_password", "password"))
    @method_decorator(never_cache)
    def post(self, request):
        serializer = PatientChangePasswordSerializer(
            self.request.user.patient,
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)