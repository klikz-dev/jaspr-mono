import logging

from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_variables
from django.utils.decorators import method_decorator
from django.db import transaction

from rest_framework.decorators import  permission_classes
from rest_framework.response import Response

from .base import JasprBaseView
from ..serializers import (
    SecurityQuestionSerializer,
)
from jaspr.apps.kiosk.models import Encounter
from ..permissions import (
    IsAuthenticated,
    IsPatient,
    IsInER,
    SatisfiesClinicIPWhitelistingFromPatient,
    HasRecentHeartbeat,
)
from jaspr.apps.common.decorators import drf_sensitive_post_parameters

logger = logging.getLogger(__name__)


class PatientSecurityQuestion(JasprBaseView):
    """
    view/endpoint for making a `POST` request to change security question and answer on current patient encounter.
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            permissions = (IsAuthenticated, IsPatient, IsInER, SatisfiesClinicIPWhitelistingFromPatient)
            return [permission() for permission in permissions]

        permissions = (IsAuthenticated, IsPatient, IsInER, SatisfiesClinicIPWhitelistingFromPatient, HasRecentHeartbeat)
        return [permission() for permission in permissions]


    def get(self, request):
        serializer = SecurityQuestionSerializer(
            instance=request.auth.jaspr_session.encounter,
        )
        return Response(serializer.data)

    @method_decorator(drf_sensitive_post_parameters())
    @method_decorator(sensitive_variables("answer"))
    @method_decorator(never_cache)
    def post(self, request):
        with transaction.atomic():
            encounter = (
                Encounter.objects.filter(pk=request.auth.jaspr_session.encounter.pk)
                    .select_for_update()
                    .get()
            )
            serializer = SecurityQuestionSerializer(
                instance=encounter,
                data=request.data,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)