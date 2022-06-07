import logging
import hmac
from hashlib import md5
from time import time

import jwt
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.utils.http import urlencode
from django.conf import settings

from .base import JasprBaseView
from ..permissions import (
    IsAuthenticated,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
    IsInER
)

logger = logging.getLogger(__name__)


class FreshdeskSSOView(JasprBaseView):
    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SatisfiesClinicIPWhitelistingFromTechnician,
    )

    def get(self, request):
        state = request.GET.get('state', None)
        nonce = request.GET.get('nonce', None)
        if nonce is None or state is None or request.user is None:
            raise Http404()

        user = request.user
        technician = user.technician
        email = user.email
        payload = {
            "sub": f"tech-{technician.pk}",
            "email": email,
            "iat": time(),
            "nonce": nonce,
            "given_name": technician.first_name,
            "family_name": technician.last_name,
        }

        encoded = jwt.encode(payload, settings.JASPR_PRIVATE_KEY, algorithm="RS256")

        params = urlencode({
            'state': state,
            'id_token': encoded
        })
        redirect_url = f"{settings.FRESHDESK_SSO_REDIRECT_URL}?{params}"

        return JsonResponse({
            "redirect_url": redirect_url,
        })
