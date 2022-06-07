from datetime import datetime, timedelta
from typing import Literal, Optional, Type, Union

from django.test import SimpleTestCase
from django.utils import timezone
from knox.models import AuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from jaspr.apps.accounts.models import LoggedOutAuthToken, LogUserLoginAttempts
from jaspr.apps.kiosk.authentication import JasprTokenAuthentication
from jaspr.apps.kiosk.constants import ActionNames
from jaspr.apps.kiosk.models import Action, Encounter, Patient, Technician


def patient_before_login_setup_kwargs() -> dict:
    """
    Return a dictionary that can be used as `**kwargs`` for running
    `{some_test_case}.create_patient` in tests right before checking if the
    `Patient` has logged in. All the fields from the keys below should be reset
    after logging in.
    """
    return {}


def assert_patient_logged_in(
    test_case_instance: SimpleTestCase,
    patient: Patient,
    in_er: bool,
    time_before: datetime,
    from_native: bool = None,
    long_lived: bool = None,
    auth_token_count: int = 1,
    encounter: Encounter = None,
) -> None:
    """
    Asserts that if a `Patient` logs in, all the different records that should be
    created are created, and the `Patient` fields that should be reset are reset.

    * NOTE: If possible, it's important to set up the `Patient` with the respective
    * fields below set to values that are not what they are going to be asserted below
    * initially. That way we can be sure all the login functionality was run. You can use
    * the function `patient_before_login_setup_kwargs` above to get `**kwargs` to
    * call `test_case_instance.create_patient` with.
    """
    if from_native is None:
        from_native = not in_er
    if long_lived is None:
        long_lived = not in_er
    test_case_instance.assertEqual(
        AuthToken.objects.filter(
            user_id=patient.user_id,
            created__gte=time_before,
            jaspr_session__in_er=in_er,
            jaspr_session__from_native=from_native,
            jaspr_session__long_lived=long_lived,
        ).count(),
        auth_token_count,
    )
    LogUserLoginAttempts.objects.get(
        user_id=patient.user_id,
        was_successful=True,
        locked_out=False,
        date_time__gte=time_before,
    )

    if encounter:
        test_case_instance.assertGreaterEqual(encounter.last_heartbeat, time_before)
        test_case_instance.assertFalse(encounter.session_lock)
        test_case_instance.assertEqual(encounter.session_validation_attempts, 0)

    Action.objects.get(
        patient=patient,
        in_er=in_er,
        action=ActionNames.SESSION_START,
        created__gte=time_before,
    )


def assert_technician_logged_in(
    test_case_instance: SimpleTestCase,
    technician: Technician,
    time_before: datetime,
    from_native: bool = False,
    long_lived: bool = False,
    auth_token_count: int = 1,
) -> None:
    """
    Asserts that if a `Technician` logs in, all the different records that should be
    created are created.
    """
    test_case_instance.assertEqual(
        AuthToken.objects.filter(
            user_id=technician.user_id,
            created__gte=time_before,
            # `Technician`s can only be in the ER right now.
            jaspr_session__in_er=True,
            jaspr_session__from_native=from_native,
            jaspr_session__long_lived=long_lived,
        ).count(),
        auth_token_count,
    )
    LogUserLoginAttempts.objects.get(
        user_id=technician.user_id,
        was_successful=True,
        locked_out=False,
        date_time__gte=time_before,
    )


def assert_kiosk_instance_logged_out(
    test_case_instance: SimpleTestCase,
    kiosk_instance: Union[Patient, Technician],
    in_er: bool,
    time_before: datetime,
    manually_initiated: Optional[bool] = None,
    from_native: bool = None,
    long_lived: bool = None,
    auth_token_count: int = 0,
) -> None:
    """
    Asserts that if a `Patient` or `Technician` logs out, all the different
    records that should be created are created, and any fields that should be set or
    reset are set or reset, etc.
    """
    is_patient = isinstance(kiosk_instance, Patient)
    if from_native is None:
        from_native = not in_er if is_patient else False
    if long_lived is None:
        long_lived = not in_er if is_patient else False
    LoggedOutAuthToken.objects.get(
        user_id=kiosk_instance.user_id, logged_out_at__gte=time_before
    )
    test_case_instance.assertEqual(
        AuthToken.objects.filter(
            user_id=kiosk_instance.user_id,
            created__gte=time_before,
            jaspr_session__in_er=in_er,
            jaspr_session__from_native=from_native,
            jaspr_session__long_lived=long_lived,
        ).count(),
        auth_token_count,
    )
    if is_patient:
        if manually_initiated:
            action_name = ActionNames.LOG_OUT_BY_USER
        else:
            action_name = ActionNames.LOG_OUT_TIMEOUT
        Action.objects.get(
            patient=kiosk_instance,
            action=action_name,
            created__gte=time_before,
            in_er=in_er,
        )


def assert_kiosk_instance_not_logged_out(
    test_case_instance: SimpleTestCase,
    kiosk_instance: Union[Patient, Technician],
    time_before: datetime,
    logged_out_auth_token_count: int = 0,
) -> None:
    """
    Asserts that a `Patient` or `Technician` instance has not logged out on or
    after `time_before`.
    """
    test_case_instance.assertEqual(
        LoggedOutAuthToken.objects.filter(
            user_id=kiosk_instance.user_id, logged_out_at__gte=time_before
        ).count(),
        logged_out_auth_token_count,
    )


def assert_auth_token_string_valid(
    test_case_instance: SimpleTestCase,
    token_string: str,
    kiosk_instance: Union[Patient, Technician],
):
    """
    Check that the token string successfully authenticates for `kiosk_instance`.
    """
    authentication = JasprTokenAuthentication()
    (authenticated_user, authenticated_token) = authentication.authenticate_credentials(
        token_string.encode()
    )
    if isinstance(kiosk_instance, Patient):
        test_case_instance.assertEqual(authenticated_user.patient, kiosk_instance)
        test_case_instance.assertEqual(authenticated_token.user.patient, kiosk_instance)
        test_case_instance.assertEqual(
            authenticated_token.jaspr_session.user_type, "Patient"
        )
    else:
        test_case_instance.assertEqual(authenticated_user.technician, kiosk_instance)
        test_case_instance.assertEqual(
            authenticated_token.user.technician, kiosk_instance
        )
        test_case_instance.assertEqual(
            authenticated_token.jaspr_session.user_type, "Technician"
        )


def assert_validation_error_thrown(
    self: SimpleTestCase,
    response: Response,
    data_key: str,
    serializer_error_key: Union[str, Literal[...]],
    serializer_class: Optional[Type[Serializer]] = None,
) -> None:
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    data = response.data
    if serializer_error_key is ...:  # Just check that there was some error thrown.
        self.assertGreaterEqual(len(data[data_key]), 1)
    else:  # We have a specific key to check for one of our custom error messages.
        serializer = (serializer_class or self.serializer_class)()
        self.assertEqual(
            data[data_key][0],
            serializer.error_messages[serializer_error_key],
        )
