import logging
import secrets
import jwt
import time

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_variables
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from jaspr.apps.api.v1.views.base import JasprBaseView
from jaspr.apps.epic.models import EpicSettings
from jaspr.settings.mixins.environment_and_versioning_mixin import ENVIRONMENT

from ....common.functions import resolve_frontend_url

logger = logging.getLogger("EPIC")


class TechnicianEpicOauthRedirectView(JasprBaseView):
    """
    View that receives iss and launch parameters initiated by an EPIC Oauth signin :
    """

    authentication_classes = ()
    permission_classes = ()

    @method_decorator(sensitive_variables("launch"))
    @method_decorator(never_cache)
    def get(self, request: Request) -> HttpResponseRedirect:
        iss = request.GET.get("iss")
        launch = request.GET.get("launch")

        logger.info("Epic OAuth session initiated with iss %s and launch %s", iss, launch)

        if iss is None:
            return Response(
                {
                    "iss": [
                        "iss metadata url is required"
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if ENVIRONMENT == "production":
            redirect_uri = "https://epic.jasprhealth.com/epic/redirect"
        elif ENVIRONMENT == "integration":
            redirect_uri = "https://epic.jaspr-integration.com/epic/redirect"
        elif ENVIRONMENT == "local":
            redirect_uri = "http://localhost:3000/epic/redirect"
        else:
            redirect_uri = f"{resolve_frontend_url()}/epic/redirect"
            logger.warning("Epic OAuth attempting to redirect to unsupported URI %s", redirect_uri)

        logger.info(f"Returning ${redirect_uri} as the OAuth Redirect URL")

        oauth_session_id = secrets.token_urlsafe(32)
        cache.set(
            f"oauth-session-{oauth_session_id}",
            iss,
            timeout=60 * 5
        )

        # This is a global Jaspr private key we use to sign and verify
        # jwt tokens used as secrets during OAuth handshakes
        private_key = settings.JASPR_PRIVATE_KEY
        epoch_time = int(time.time())

        encoded_jwt = jwt.encode(
            {
                "sub": oauth_session_id,
                "exp": epoch_time + (60 * 4),
                "nbf": epoch_time - 60,
                "iat": epoch_time,
            },
            private_key,
            algorithm="RS384",
        )

        logger.info("OAuth Session saved to Redis with {session_key: %s, iss: %s}",
                    oauth_session_id,
                    iss
        )

        epic_authorize_url = EpicSettings.get_authorize_url(iss)

        if not epic_authorize_url:
            logger.exception(f"Unable to get token and authorization urls from EPIC instance metadata for {iss}")
            return Response(
                {
                    "non_field_errors": [
                        "Unable to get token and authorization urls from EPIC instance metadata"
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        redirect_route = f"{epic_authorize_url}?response_type=code&client_id={settings.EPIC_CLIENT_ID}&redirect_uri={redirect_uri}&scope=launch&launch={launch}&state={encoded_jwt}&aud={iss}"

        logger.info("Epic OAuth Redirect with url length %s to %s", len(redirect_route), redirect_route)

        return HttpResponseRedirect(redirect_route)
