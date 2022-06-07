import logging

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_variables

from rest_framework import serializers
from rest_framework.request import Request

from jaspr.apps.kiosk.authentication import JasprToolsToGoUidAndTokenAuthentication
from jaspr.apps.kiosk.models import Patient

from ....common.functions import resolve_frontend_url
from .base import JasprBaseView

logger = logging.getLogger(__name__)


class PatientToolsToGoVerificationRedirectView(JasprBaseView):
    """
    View that checks the `uid` and `token` and redirects according to the following
    logic:
    1. If the `User` doesn't exist, the `User` doesn't have a `Patient`, the uid
    or token are invalid, or checking the token doesn't work or is expired, redirect
    to the frontend invalid link/error page (this could be the login or reset
    password page with a special url param or hash to indicate coming from an invalid
    link).
    2. If the `User` exists, the `User` has a `Patient`, the token is valid, and
    tools to go is not set up, redirect to the next page/step of the at home setup.
    3. If the `User` exists, the `User` has a `Patient`, the token is valid, and
    tools to go is set up, redirect to the frontend login page (potentially
    indicating that we came from a valid setup link so a dialog could display, etc.).
    """

    authentication_classes = ()
    permission_classes = ()
    token_authentication_class = JasprToolsToGoUidAndTokenAuthentication
    invalid_redirect_link = f"{resolve_frontend_url()}/?at-home-setup-link=invalid"
    already_set_up_redirect_link = (
        f"{resolve_frontend_url()}?at-home-setup-link=already-set-up"
    )

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
        if user.is_patient and hasattr(user, "patient"):
            patient = user.patient
            if patient.tools_to_go_status != Patient.TOOLS_TO_GO_SETUP_FINISHED:
                uid = kwargs["uid"]
                token = kwargs["token"]
                return redirect(
                    f"{resolve_frontend_url()}/activate-tools-to-go/#uid={uid}&token={token}"
                )
            # NOTE: This is very unlikely to happen. It would require a `Patient`
            # to get a valid tools to go setup email link in their inbox, and then have
            # them click this when already having "Setup Finished" as their tools to go
            # status. It's very unlikely because at the time of writing, the reset
            # password endpoint will send a different email based on the tools to go
            # status, so shouldn't send a valid verification setup email to a
            # `Patient` that has already set up tools to go. Hence, the link will
            # either be invalid (or expired, which would hit code above) or valid with
            # the `Patient` not having set up tools to go. That being said, this
            # has already been coded and tested so leaving here in case we change the
            # logic in the future or something fluke happens.
            return redirect(self.already_set_up_redirect_link)
        return redirect(self.invalid_redirect_link)
