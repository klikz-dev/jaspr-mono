import jwt
import logging
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from typing import Any,  Dict
from django.conf import settings
from django.core.cache import cache
from rest_framework import serializers
from jaspr.apps.epic.models import EpicSettings
from .base import JasprBaseSerializer

logger = logging.getLogger("EPIC")

class TechnicianEpicOauthLoginSerializer(JasprBaseSerializer):
    redirect_uri = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    token_url = serializers.SerializerMethodField()
    iss = serializers.SerializerMethodField()

    default_error_messages = {
        "missing_state": "Validation state is not set on the user session",
        "expired_state": "Validation failed because the session has expired",
        "invalid_token": "Validation state is not valid",
    }

    def get_iss(self, obj):
        return obj["iss"]

    def get_token_url(self, obj):
        try:
            iss = obj["iss"]
            return EpicSettings.get_token_url(iss)
        except Exception as e:
            return None

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data = super().validate(attrs)

        encoded_jwt = data["state"]

        try:
            jwt_payload = jwt.decode(
                encoded_jwt,
                key=settings.JASPR_PUBLIC_KEY,
                algorithms=['RS384',]
            )
        except ExpiredSignatureError as e:
            logger.exception(f"Decoding JWT failed due to expired signature", exc_info=e)
            self.fail("expired_state")
        except InvalidSignatureError as e:
            logger.exception(f"Decoding JWT failed due to invalid signature", exc_info=e)
            self.fail("invalid_token")
        except Exception as e:
            logger.exception(f"Decoding JWT failed", exc_info=e)
            self.fail("invalid_token")

        cache_key = f"oauth-session-{jwt_payload.get('sub')}"
        iss = cache.get(cache_key)
        cache.delete(cache_key)

        if not iss:
            self.fail("missing_state")

        data["iss"] = iss

        return data

    class Meta:
        fields = (
            "redirect_uri",
            "code",
            "state",
            "token_url"
        )