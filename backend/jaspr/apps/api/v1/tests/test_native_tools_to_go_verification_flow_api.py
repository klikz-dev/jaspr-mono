import enum
import logging
import random
from typing import ClassVar, List
from unittest.mock import NonCallableMagicMock

from django.utils import timezone
from django.utils.functional import cached_property
from freezegun import freeze_time
from jaspr.apps.api.v1.serializers import (
    CheckPhoneNumberVerificationSerializer,
    ReadOnlyAuthTokenSerializer,
    ReadOnlyJasprSessionSerializer,
)
from jaspr.apps.common.phonenumbers.verify import (
    VerificationCodeInvalid,
    VerificationCodeNotFound,
    VerificationTwilioException,
)
from jaspr.apps.common.tests.mixins import UidAndTokenTestMixin
from jaspr.apps.kiosk.authentication import JasprTokenAuthentication
from jaspr.apps.kiosk.models import JasprSession, Patient
from jaspr.apps.kiosk.tokens import (
    JasprPasswordResetTokenGenerator,
    JasprSetPasswordTokenGenerator,
    JasprToolsToGoSetupTokenGenerator,
)
from jaspr.apps.test_infrastructure.mixins.common_mixins import (
    TwilioClientTestCaseMixin,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status
from rest_framework.response import Response
from twilio.base.exceptions import TwilioRestException
from twilio.rest.verify.v2.service.verification_check import VerificationCheckInstance

from .helpers import assert_auth_token_string_valid, assert_patient_logged_in


class ToolsToGoNativeTestingBase(TwilioClientTestCaseMixin, JasprApiTestCase):
    uri: ClassVar[str]
    random_tools_to_go_statuses_choices: ClassVar[List[str]]

    def create_patient(self, *args, **kwargs) -> Patient:
        kwargs.setdefault("user__email", self.valid_email)
        kwargs.setdefault("user__mobile_phone", self.valid_mobile_phone)
        kwargs.setdefault(
            "tools_to_go_status",
            random.choice(self.random_tools_to_go_statuses_choices),
        )
        self.patient = super().create_patient(*args, **kwargs)
        return self.patient

    @cached_property
    def valid_email(self) -> str:
        return "valid_email_example@example.jasprhealth.com"

    @cached_property
    def valid_different_email(self) -> str:
        return "valid_different_email_example@example.jasprhealth.com"

    @cached_property
    def valid_mobile_phone(self) -> str:
        return "+15005550006"

    @cached_property
    def valid_different_mobile_phone(self) -> str:
        return "+14155552671"

    @cached_property
    def valid_equivalent_mobile_phone_different_format(self) -> str:
        # This assumes we do have the default 'US' `PHONENUMBER_DEFAULT_REGION` set).
        return "(500) 555-0006"


class TestNativeVerifyPhoneNumberAPI(ToolsToGoNativeTestingBase):
    """
    For all cases (except the current first test of a badly formatted email or mobile
    phone), 200 responses should be expected.

    Shortcuts in these tests:
    - 200 responses and data are checked in `self.make_request` by default because
    the `check_response` defaults to `True`.
    - `self.patient` is set in the latest call to `self.create_patient` by default,
    which is used for the default values for `email` and `mobile_phone` in
    `self.make_request`, and also the default value for `mobile_phone` in
    `self.assert_verification_sms_sent`.
    """

    uri = "/v1/patient/native-verify-phone-number"
    random_tools_to_go_statuses_choices = [
        Patient.TOOLS_TO_GO_EMAIL_SENT,
        Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
    ]

    def make_request(
        self,
        email: str = None,
        mobile_phone: str = None,
        *,
        check_response: bool = True,
        throw_twilio_exception: bool = False,
    ) -> Response:
        if email is None:
            email = self.patient.user.email
        if mobile_phone is None:
            mobile_phone = self.patient.user.mobile_phone.as_e164
        with self.patched_twilio_verifications_create() as mock_verifications_create:
            if throw_twilio_exception:
                mock_verifications_create.side_effect = (
                    self.twilio_rest_exception_instance
                )
            self.mock_verifications_create = mock_verifications_create
            data = {"email": email, "mobile_phone": mobile_phone}
            response = self.client.post(self.uri, data=data)
        if check_response:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIsNone(response.data)
        return response

    def assert_verification_sms_attempted(self, mobile_phone: str = None) -> None:
        if mobile_phone is None:
            mobile_phone = self.patient.user.mobile_phone.as_e164
        # Check that we have record of the verification being created/called with
        # Twilio.
        self.mock_verifications_create.assert_called_once_with(
            to=mobile_phone, channel="sms"
        )

    def assert_verification_sms_not_attempted(self) -> None:
        self.mock_verifications_create.assert_not_called()

    def test_badly_formatted_email_or_mobile_phone(self):
        email = "badly_formatted_email@"
        mobile_phone = "(111) 222-333"
        response = self.make_request(email, mobile_phone, check_response=False)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("mobile_phone", response.data)

    def test_patient_present_but_tools_to_go_status_not_started(self):
        self.create_patient(tools_to_go_status=Patient.TOOLS_TO_GO_NOT_STARTED)
        self.make_request()

        self.assert_verification_sms_not_attempted()

    def test_patient_missing_from_database_email_mismatch(self):
        self.create_patient()
        self.make_request(email=self.valid_different_email)

        self.assert_verification_sms_not_attempted()

    def test_patient_present_but_mobile_phone_mismatch(self):
        self.create_patient()
        self.make_request(mobile_phone=self.valid_different_mobile_phone)

        self.assert_verification_sms_not_attempted()

    def test_twilio_exception_when_sending_verification_code(self):
        patient = self.create_patient()
        self.make_request(throw_twilio_exception=True)

        self.assert_verification_sms_attempted()
        # Quickest and easiest way for now to check that the exception was thrown.
        self.assertIsInstance(
            self.mock_verifications_create.side_effect, TwilioRestException
        )

    def test_verification_successfully_sent_with_mobile_phone_same_format(self):
        patient = self.create_patient()
        self.make_request()

        self.assert_verification_sms_attempted()

    def test_verification_successfully_sent_with_mobile_phone_format_difference(self):
        patient = self.create_patient()
        self.make_request(
            mobile_phone=self.valid_equivalent_mobile_phone_different_format
        )

        self.assert_verification_sms_attempted()

    def test_verification_successfully_sent_with_tools_to_go_setup_finished(self,):
        """
        This was a change made in EBPI-881. It makes the endpoint we're testing
        corresponding with self.uri` work for both the initial JAH native setup flow,
        and the JAH native reset password flow.
        """
        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_SETUP_FINISHED
        )
        self.make_request()

        self.assert_verification_sms_attempted()


class TestNativeCheckPhoneNumberCodeAPI(
    UidAndTokenTestMixin, ToolsToGoNativeTestingBase
):
    """
    For all cases except the success path (correctly formatted `POST` data, valid
    code, and no Twilio exceptions), 400 responses should be expected. Additionally,
    the error message for an invalid code format should be consistent regardless.

    Shortcuts in these tests:
    - `self.patient` is set in the latest call to `self.create_patient` by default,
    which is used for the default values for `email` and `mobile_phone` in
    `self.make_request`, and also the default value for `mobile_phone` in
    `self.assert_verification_check_attempted`.
    - `self.code_used` is set in the latest call to `self.make_request` and is the
    default value for `code` in `self.assert_verification_check_attempted`
    - `self.valid_code` is used as the default for `code` in `self.make_request`.
    """

    token_generator = JasprToolsToGoSetupTokenGenerator
    uri = "/v1/patient/native-check-phone-number-code"
    random_tools_to_go_statuses_choices = (
        TestNativeVerifyPhoneNumberAPI.random_tools_to_go_statuses_choices
    )

    class TwilioCheck(enum.Enum):
        CODE_INVALID = enum.auto()
        CODE_DENIED = enum.auto()
        EXCEPTION_THROWN = enum.auto()

    def make_request(
        self,
        email: str = None,
        mobile_phone: str = None,
        code: str = None,
        *,
        twilio_check: TwilioCheck = None,
    ) -> Response:
        if email is None:
            email = self.patient.user.email
        if mobile_phone is None:
            mobile_phone = self.patient.user.mobile_phone.as_e164
        if code is None:
            code = self.valid_code
        self.code_used = code
        with self.patched_twilio_verification_checks_create() as mock_verification_checks_create:
            if twilio_check is self.TwilioCheck.CODE_INVALID:

                def patched_verification_checks_create_code_invalid(
                    *args, **kwargs
                ) -> NonCallableMagicMock:
                    mock = NonCallableMagicMock(spec_set=VerificationCheckInstance)
                    mock.sid = "verification-check-sid-code-invalid"
                    mock.status = "pending"
                    return mock

                mock_verification_checks_create.side_effect = (
                    patched_verification_checks_create_code_invalid
                )
            elif twilio_check is self.TwilioCheck.CODE_DENIED:

                def patched_verification_checks_create_code_denied(
                    *args, **kwargs
                ) -> NonCallableMagicMock:
                    mock = NonCallableMagicMock(spec_set=VerificationCheckInstance)
                    mock.sid = "verification-check-sid-code-denied"
                    mock.status = "denied"
                    return mock

                mock_verification_checks_create.side_effect = (
                    patched_verification_checks_create_code_denied
                )
            elif twilio_check is self.TwilioCheck.EXCEPTION_THROWN:
                mock_verification_checks_create.side_effect = (
                    self.twilio_rest_exception_instance
                )
            self.mock_verification_checks_create = mock_verification_checks_create
            data = {"email": email, "mobile_phone": mobile_phone, "code": code}
            return self.client.post(self.uri, data=data)

    @cached_property
    def valid_code(self) -> str:
        return "123456"

    def assert_verification_check_attempted(
        self, mobile_phone: str = None, code: str = None
    ) -> None:
        if mobile_phone is None:
            mobile_phone = self.patient.user.mobile_phone.as_e164
        if code is None:
            code = self.code_used
        # Check that we have record of the verification being created/called with
        # Twilio.
        self.mock_verification_checks_create.assert_called_once_with(
            to=mobile_phone, code=code
        )

    def assert_verification_check_not_attempted(self) -> None:
        self.mock_verification_checks_create.assert_not_called()

    def assert_response_exactly_invalid_code_and_nothing_else(
        self, response: Response
    ) -> None:
        """This assertion is very important so it's named with `_exactly_...`."""
        expected_data_exactly = {
            "non_field_errors": [VerificationCodeInvalid.error_message]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data_exactly)

    def assert_response_denied_code(self, response: Response) -> None:
        expected_data = {"non_field_errors": [VerificationCodeNotFound.error_message]}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def assert_response_twilio_exception(self, response: Response) -> None:
        expected_data = {
            "non_field_errors": [VerificationTwilioException.GENERIC_ERROR_MESSAGE]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)

    def assert_response_success(
        self, response: Response, already_set_up: bool = False,
    ) -> None:
        self.patient.refresh_from_db()
        self.assertEqual(
            self.patient.tools_to_go_status,
            Patient.TOOLS_TO_GO_SETUP_FINISHED
            if already_set_up
            else Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
        )

        self.assert_verification_check_attempted()

        token_string = response.data["token"]
        if already_set_up:
            valid_token = self.valid_token_for(
                self.patient.user, token_generator=JasprPasswordResetTokenGenerator
            )
        else:
            valid_token = self.valid_token_for(self.patient.user)
        expected_data = {
            "already_set_up": already_set_up,
            "uid": self.uidb64_for(self.patient.user),
            "token": valid_token,
            "set_password_token": self.valid_token_for(
                self.patient.user, token_generator=JasprSetPasswordTokenGenerator
            ),
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_badly_formatted_email_or_mobile_phone(self):
        email = "badly_formatted_email@"
        mobile_phone = "(111) 222-333"
        response = self.make_request(email, mobile_phone, self.valid_code)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("mobile_phone", response.data)
        self.assertNotIn("code", response.data)
        self.assert_verification_check_not_attempted()

    def test_badly_formatted_code_with_patient_not_present(self):
        code = "&25!"
        response = self.make_request(self.valid_email, self.valid_mobile_phone, code)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("email", response.data)
        self.assertNotIn("mobile_phone", response.data)
        self.assertIn("code", response.data)
        self.assert_verification_check_not_attempted()

    def test_badly_formatted_code_with_patient_present(self):
        """
        Make sure that even if a `Patient` is present and is a valid candidate for
        checking the `code` with Twilio that an invalid `code` raises an error right
        away, still providing a consistent error message (the same error message as
        the test above).
        """
        code = "&25!"
        no_patient_response = self.make_request(
            self.valid_email, self.valid_mobile_phone, code
        )
        patient = self.create_patient()
        self.assertEqual(
            no_patient_response.status_code,
            status.HTTP_400_BAD_REQUEST,
            "Pre-Condition",
        )
        self.assertIn("code", no_patient_response.data, "Pre-Condition")
        self.assertEqual(patient.user.email, self.valid_email, "Pre-Condition")
        self.assertEqual(
            patient.user.mobile_phone, self.valid_mobile_phone, "Pre-Condition"
        )
        patient_response = self.make_request(code=code)

        self.assertEqual(patient_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("code", patient_response.data, "Pre-Condition")
        self.assertEqual(no_patient_response.data, patient_response.data)
        self.assert_verification_check_not_attempted()

    def test_patient_present_but_tools_to_go_status_not_started(self):
        self.create_patient(tools_to_go_status=Patient.TOOLS_TO_GO_NOT_STARTED)
        response = self.make_request()

        self.assert_response_exactly_invalid_code_and_nothing_else(response)
        self.assert_verification_check_not_attempted()

    def test_patient_missing_from_database_email_mismatch(self):
        self.create_patient()
        response = self.make_request(email=self.valid_different_email)

        self.assert_response_exactly_invalid_code_and_nothing_else(response)
        self.assert_verification_check_not_attempted()

    def test_patient_present_but_mobile_phone_mismatch(self):
        self.create_patient()
        response = self.make_request(mobile_phone=self.valid_different_mobile_phone)

        self.assert_response_exactly_invalid_code_and_nothing_else(response)
        self.assert_verification_check_not_attempted()

    def test_invalid_code(self):
        self.create_patient()
        response = self.make_request(twilio_check=self.TwilioCheck.CODE_INVALID)

        self.assert_response_exactly_invalid_code_and_nothing_else(response)
        self.assert_verification_check_attempted()

    def test_denied_code(self):
        self.create_patient()
        response = self.make_request(twilio_check=self.TwilioCheck.CODE_DENIED)

        self.assert_response_denied_code(response)
        self.assert_verification_check_attempted()

    def test_twilio_exception_when_checking_verification_code(self):
        patient = self.create_patient()
        response = self.make_request(twilio_check=self.TwilioCheck.EXCEPTION_THROWN)

        self.assert_response_twilio_exception(response)
        self.assert_verification_check_attempted()

    def test_verification_successfully_checked_with_mobile_phone_same_format(self):
        patient = self.create_patient()
        now = timezone.now()
        # NOTE: We `freeze_time` in order to make sure we get the exact same `token`
        # and `set_password_token`.
        with freeze_time(now):
            response = self.make_request()

            self.assert_response_success(response)

    def test_verification_successfully_checked_with_mobile_phone_format_difference(
        self,
    ):
        patient = self.create_patient()
        now = timezone.now()
        with freeze_time(now):
            response = self.make_request(
                mobile_phone=self.valid_equivalent_mobile_phone_different_format
            )

            self.assert_response_success(response)

    def test_verification_successfully_checked_with_tools_to_go_setup_finished(self):
        """
        This was a change made in EBPI-881 (implement after EBPI-848). It makes the
        endpoint we're testing corresponding with self.uri` work for both the initial
        JAH native setup flow and the JAH native reset password flow.
        """
        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_SETUP_FINISHED
        )
        now = timezone.now()
        with freeze_time(now):
            response = self.make_request()

            self.assert_response_success(response, already_set_up=True)


class TestPatientSetPasswordAPIWithNativeFlow(UidAndTokenTestMixin, JasprApiTestCase):
    """
    `TestPatientSetPasswordAPI` handles the rest of the test cases in
    `test_tools_to_go_verification_flow_api`.
    """

    token_generator = JasprToolsToGoSetupTokenGenerator

    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/set-password"

    def test_can_change_password_and_get_auth_token_back(self):
        """
        Can an authenticated patient change his/her password and specify `auth_token`
        in the `POST` body to be logged in and get the auth token/session data back?
        """
        patient = self.create_patient(
            tools_to_go_status=random.choice(
                [
                    Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
                    Patient.TOOLS_TO_GO_SETUP_FINISHED,
                ]
            ),
            user__password_complex=False,
            user__password_changed=None,
        )
        department = self.create_department()
        self.create_patient_department_sharing(patient=patient, department=department)
        new_password = "TheGoose87623##"
        set_password_token = self.valid_token_for(
            patient.user, token_generator=JasprSetPasswordTokenGenerator
        )
        now = timezone.now()
        with freeze_time(now):
            response = self.post_with_creds(
                self.uri,
                patient.user,
                data={
                    "password": new_password,
                    "set_password_token": set_password_token,
                    "auth_token": True,
                },
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("password", response.data)
        patient.user.refresh_from_db()
        patient.refresh_from_db()
        self.assertEqual(patient.tools_to_go_status, Patient.TOOLS_TO_GO_SETUP_FINISHED)
        self.assertTrue(patient.user.check_password(new_password))
        self.assertEqual(patient.user.password_changed, now)
        self.assertTrue(patient.user.password_complex)

        assert_auth_token_string_valid(self, response.data["token"], patient)
        jaspr_session = JasprSession.objects.get(auth_token__user=patient.user)
        self.assertIs(jaspr_session.in_er, False)
        self.assertIs(jaspr_session.from_native, True)
        self.assertIs(jaspr_session.long_lived, True)
        patient.refresh_from_db()
        assert_patient_logged_in(
            self, patient, False, now, from_native=True, long_lived=True,
        )


class TestPatientResetPasswordSetPasswordAPIWithNativeFlow(
    UidAndTokenTestMixin, JasprApiTestCase
):
    """
    `TestPatientResetPasswordSetPasswordAPI` handles the rest of the test cases in
    `test_reset_password_flow_api`.
    """

    token_generator = JasprPasswordResetTokenGenerator

    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/reset-password/set-password"

    def test_can_change_password_and_get_auth_token_back(self):
        """
        Can an authenticated patient change his/her password and specify `auth_token`
        in the `POST` body to be logged in and get the auth token/session data back?
        """
        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_SETUP_FINISHED,
            user__password_complex=False,
            user__password_changed=None,
        )
        department = self.create_department()
        self.create_patient_department_sharing(patient=patient, department=department)
        new_password = "TheGoose87623##"
        set_password_token = self.valid_token_for(
            patient.user, token_generator=JasprSetPasswordTokenGenerator
        )
        now = timezone.now()
        with freeze_time(now):
            response = self.post_with_creds(
                self.uri,
                patient.user,
                data={
                    "password": new_password,
                    "set_password_token": set_password_token,
                    "auth_token": True,
                },
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("password", response.data)
        patient.user.refresh_from_db()
        patient.refresh_from_db()
        self.assertEqual(patient.tools_to_go_status, Patient.TOOLS_TO_GO_SETUP_FINISHED)
        self.assertTrue(patient.user.check_password(new_password))
        self.assertEqual(patient.user.password_changed, now)
        self.assertTrue(patient.user.password_complex)

        assert_auth_token_string_valid(self, response.data["token"], patient)
        jaspr_session = JasprSession.objects.get(auth_token__user=patient.user)
        self.assertIs(jaspr_session.in_er, False)
        self.assertIs(jaspr_session.from_native, True)
        self.assertIs(jaspr_session.long_lived, True)
        patient.refresh_from_db()
        assert_patient_logged_in(
            self, patient, False, now, from_native=True, long_lived=True,
        )
