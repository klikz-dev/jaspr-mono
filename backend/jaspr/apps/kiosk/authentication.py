from typing import Literal, Tuple

from django.utils import timezone
from ipware import get_client_ip
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.settings import knox_settings
from rest_framework import exceptions
from rest_framework.request import Request

from jaspr.apps.accounts.authentication import log_login_attempt
from jaspr.apps.accounts.models import LoggedOutAuthToken
from jaspr.apps.common.authentication import UidAndTokenAuthentication
from jaspr.apps.kiosk.constants import ActionNames
from jaspr.apps.kiosk.jobs import queue_action_creation
from jaspr.apps.kiosk.models import (
    Encounter,
    JasprSession,
    JasprSessionError,
    Patient,
    Technician,
)

from .tokens import (
    JasprExtraSecurityTokenGenerator,
    JasprPasswordResetTokenGenerator,
    JasprToolsToGoSetupTokenGenerator,
)


class JasprTokenAuthentication(TokenAuthentication):
    def renew_token(self, auth_token: AuthToken) -> None:
        jaspr_session = auth_token.jaspr_session
        session_parameters = {
            "user_type": jaspr_session.user_type,
            "in_er": jaspr_session.in_er,
            "from_native": jaspr_session.from_native,
            "long_lived": jaspr_session.long_lived,
            "technician_operated": jaspr_session.technician_operated
        }
        try:
            JasprSession.validate_create_parameters(
                user=auth_token.user, **session_parameters
            )
        # NOTE: If we encounter a `JasprSessionError`, it's possible (although very
        # unlikely) that these parameters aren't valid together anymore (could be a
        # long-lived token that gets used almost a month later at the time of writing,
        # and maybe business requirements or specifications changed). In that case,
        # delete the token, and then they'll get redirected and have to log in/get a
        # new token.
        except JasprSessionError:
            auth_token.delete()
            raise exceptions.AuthenticationFailed(
                ("Token parameters invalid for refresh. Please get a new token.")
            )
        else:
            # The code below is copy pasted from knox at the time of writing except for
            # the line `new_expiry = ...` (which was modified to fit our use case).
            current_expiry = auth_token.expiry
            new_expiry = timezone.now() + JasprSession.expiration_timedelta_for(
                **session_parameters
            )
            auth_token.expiry = new_expiry
            delta = (new_expiry - current_expiry).total_seconds()
            # Throttle refreshing of token to avoid db writes.
            if delta > JasprSession.expiration_min_refresh_interval_for(
                **session_parameters
            ):
                auth_token.save(update_fields=("expiry",))


class JasprTokenAuthenticationNoRenew(TokenAuthentication):
    def renew_token(self, auth_token) -> None:
        return None

class JasprExtraSecurityTokenAuthentication(UidAndTokenAuthentication):
    token_generator = JasprExtraSecurityTokenGenerator


class JasprToolsToGoUidAndTokenAuthentication(UidAndTokenAuthentication):
    token_generator = JasprToolsToGoSetupTokenGenerator


class JasprResetPasswordUidAndTokenAuthentication(UidAndTokenAuthentication):
    token_generator = JasprPasswordResetTokenGenerator


def login_patient(
    patient: Patient,
    *,
    request: Request,
    encounter: Encounter = None,
    log_user_login_attempt: bool,
    in_er: bool,
    from_native: bool,
    long_lived: bool,
    technician_operated: bool = False,
    save: bool = True,
) -> Tuple[JasprSession, str]:
    """
    Log in the `patient`, returning the `JasprSession` and `AuthToken` token
    string. If `save` is `True`, the `patient` will be saved at the end.

    ! IMPORTANT: This function should be wrapped in `transaction.atomic()`
    ! from somewhere higher up in the call stack.
    """
    jaspr_session, token_string = JasprSession.create(
        user=patient.user,
        encounter=encounter,
        user_type="Patient",
        in_er=in_er,
        from_native=from_native,
        long_lived=long_lived,
        technician_operated=technician_operated,
    )
    # NOTE: We have an if statement here because at the time of writing,
    # `LoginSerializer` does this already.
    if log_user_login_attempt:
        log_login_attempt(patient.user_id, get_client_ip(request)[0], True, False)

    # Make sure account is unlocked
    if in_er and encounter:
        encounter.reset_lockout()

    if save:
        patient.save()
    # Queue the "SessionStart" action for creation.
    queue_action_creation(
        {
            "action": ActionNames.SESSION_START,
            "patient": patient,
            "in_er": jaspr_session.in_er,
        }
    )
    return jaspr_session, token_string


def login_technician(
    technician: Technician,
    *,
    request: Request,
    log_user_login_attempt: bool,
    in_er: bool,
    from_native: bool,
    long_lived: bool,
    save: bool = True,
    encounter=None,
) -> Tuple[JasprSession, str]:
    """
    Log in the `technician`, returning the `JasprSession` and `AuthToken` token
    string. If `save` is `True`, the `technician` will be saved at the end.

    ! IMPORTANT: This function should be wrapped in `transaction.atomic()`
    ! from somewhere higher up in the call stack.
    """
    jaspr_session, token_string = JasprSession.create(
        user=technician.user,
        user_type="Technician",
        in_er=in_er,
        from_native=from_native,
        long_lived=long_lived,
    )
    # NOTE: We have an if statement here because at the time of writing,
    # `LoginSerializer` does this already.
    if log_user_login_attempt:
        log_login_attempt(technician.user_id, get_client_ip(request)[0], True, False)
    if save:
        technician.save()
    return jaspr_session, token_string


ManuallyInitiatedType = Literal["True", "true", "False", "false", True, False, None]


def logout_kiosk_user(
    auth_token: AuthToken, manually_initiated: ManuallyInitiatedType = None
) -> None:
    """
    If it is known ahead of time whether the `User` is a `Patient` or
    `Technician`, can specify `provided_user_type` to `Patient` or `Technician` to
    avoid database queries here.
    """
    # Grab the `digest`, `token_key`, `salt`, and `user` before deleting the token. At
    # least one of these at the time of writing has `primary_key=True` on the field, so
    # it should be accessed before deleting. Also, grab `user_type` and `in_er` from
    # `auth_token.jaspr_session` before deleting the `auth_token` since the
    # `JasprSession` will also be deleted once the `AuthToken` is deleted because of
    # `models.CASCADE`. Since we always have a `jaspr_session` present from
    # `select_related` at the time of writing it would technically still work to access
    # it after `auth_token.delete()` but I think it's safer to just get it before
    # deleting `auth_token`.
    digest = auth_token.digest
    token_key = auth_token.token_key
    user = auth_token.user
    user_type = auth_token.jaspr_session.user_type
    in_er = auth_token.jaspr_session.in_er

    auth_token.delete()
    LoggedOutAuthToken.objects.create(
        user=user,
        digest=digest,
        token_key=token_key,
        logged_out_at=timezone.now(),
    )

    # If the `User` is a `Patient` (checking the session for the `user_type` first
    # and then making sure the `user` still has a `patient`), queue the relevant
    # logout action.
    if user_type == "Patient" and hasattr(user, "patient"):
        action = (
            ActionNames.LOG_OUT_BY_USER
            if manually_initiated in (True, "true", "True")
            else ActionNames.LOG_OUT_TIMEOUT
        )
        queue_action_creation(
            {"action": action, "patient": user.patient, "in_er": in_er}
        )
