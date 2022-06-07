import logging

from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_variables
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework import status

from .base import JasprBaseView
from ..serializers import (
    VerifyPhoneNumberSerializer,
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

logger = logging.getLogger(__name__)


class PatientVerifyPhoneNumberView(JasprBaseView):
    """
    Endpoint for submitting `mobile_phone` and getting a verification code sent to the
    `mobile_phone` if the `mobile_phone` submitted matches the one stored on the
    `User` model's `mobile_phone`.
    """

    authentication_classes = (JasprToolsToGoUidAndTokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        IsPatient,
        HasToolsToGoStartedButNotFinished,
    )

    @method_decorator(drf_sensitive_post_parameters())
    @method_decorator(sensitive_variables("token"))
    @method_decorator(never_cache)
    def post(self, request):
        serializer = VerifyPhoneNumberSerializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        # NOTE: Choosing to use `HTTP_201_CREATED` in order to indicate that we
        # created something (in this sense we created a Twilio Verification on
        # Twilio's servers).
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)