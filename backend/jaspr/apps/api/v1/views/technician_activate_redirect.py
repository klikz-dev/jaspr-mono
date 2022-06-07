import logging

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_variables
from rest_framework import serializers
from rest_framework.request import Request

from jaspr.apps.kiosk.authentication import (
    JasprExtraSecurityTokenAuthentication,
)

from ....common.functions import resolve_frontend_url
from .base import JasprBaseView

logger = logging.getLogger(__name__)


class TechnicianActivateRedirectView(JasprBaseView):
    """
    View that checks the `uid` and `token` and redirects according to the following
    logic:
    1. If the `User` doesn't exist, the `User` doesn't have a `Technician`, the uid
    or token are invalid, or checking the token doesn't work or is expired, redirect
    to the frontend invalid link/error page (this could be the login or reset
    password page with a special url param or hash to indicate coming from an invalid
    link).
    2. If the `User` exists, the `User` has a `Technician`, the token is valid, and
    tools to go is not set up, redirect to the technician activation page.
    """

    authentication_classes = ()
    permission_classes = ()
    token_authentication_class = JasprExtraSecurityTokenAuthentication
    invalid_redirect_link = f"{resolve_frontend_url()}/technician/activate/?activate-technician-link=invalid"

    @method_decorator(sensitive_variables("token", "url"))
    @method_decorator(never_cache)
    def get(self, request: Request, **kwargs) -> HttpResponseRedirect:
        # NOTE: Decided to do this to make `self.token_authentication_class` work with
        # the `uid` and `token` that are provided by `**kwargs` this time instead of
        # already in the `response.data` from say a `POST`.
        request.data["uid"] = kwargs["uid"]
        request.data["token"] = kwargs["token"]
        try:
            user = self.token_authentication_class().authenticate(request)[0]
        except serializers.ValidationError:
            return redirect(self.invalid_redirect_link)
        if user.is_technician and hasattr(user, "technician"):
            uid = kwargs["uid"]
            token = kwargs["token"]
            return redirect(
                f"{resolve_frontend_url(technician=user.technician)}/technician/activate/#uid={uid}&token={token}"
            )
        return redirect(self.invalid_redirect_link)
