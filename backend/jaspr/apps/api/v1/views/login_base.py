import logging
from typing import Tuple

from rest_framework import serializers

from jaspr.apps.accounts.models import User
from jaspr.apps.kiosk.models import JasprSession, JasprSessionError, JasprUserTypeString

from ..serializers import JasprSessionCreateSerializer
from .base import JasprBaseView

logger = logging.getLogger(__name__)


class LoginBaseView(JasprBaseView):
    authentication_classes = ()
    permission_classes = ()

    def create_jaspr_session(
        self,
        user: User,
        user_type: JasprUserTypeString,
        in_er: bool,
        from_native: bool = None,
        long_lived: bool = None,
    ) -> Tuple[JasprSession, str]:
        context = {
            "request": self.request,
            "user": user,
            "user_type": user_type,
            "in_er": in_er,
            "log_user_login_attempt": False,
            "save": True,
        }
        if from_native is not None:
            context["from_native"] = from_native
        if long_lived is not None:
            context["long_lived"] = long_lived
        serializer = JasprSessionCreateSerializer(
            data=self.request.data, context=context
        )
        try:
            serializer.is_valid(raise_exception=True)
            return serializer.save()
        except JasprSessionError as e:
            raise serializers.ValidationError(e.error_message) from e
