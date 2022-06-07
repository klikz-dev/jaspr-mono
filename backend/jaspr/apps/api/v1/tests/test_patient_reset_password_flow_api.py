from unittest.mock import NonCallableMagicMock

from django.utils import timezone
from django.utils.html import escape
from freezegun import freeze_time
from rest_framework import status
from twilio.rest.verify.v2.service.verification_check import VerificationCheckInstance

from jaspr.apps.api.v1.serializers import (
    CheckPhoneNumberVerificationSerializer,
    VerifyPhoneNumberSerializer,
)
from jaspr.apps.common.functions import resolve_frontend_url
from jaspr.apps.common.phonenumbers.verify import (
    VerificationCodeInvalid,
    VerificationCodeNotFound,
    VerificationTwilioException,
)
from jaspr.apps.common.tests.mixins import UidAndTokenTestMixin
from jaspr.apps.kiosk.models import Patient
from jaspr.apps.kiosk.tokens import (
    JasprPasswordResetTokenGenerator,
    JasprSetPasswordTokenGenerator,
    JasprToolsToGoSetupTokenGenerator,
)
from jaspr.apps.message_logs.models import EmailLog
from jaspr.apps.test_infrastructure.mixins.common_mixins import (
    TwilioClientTestCaseMixin,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase

from .helpers import assert_auth_token_string_valid, patient_before_login_setup_kwargs


class TestPatientResetPasswordAPI(UidAndTokenTestMixin, JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.url = "/v1/reset-password"

    def test_invalid_email(self):
        response = self.client.post(self.url, data={"email": "!"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_user_does_not_have_patient(self):
        user = self.create_user()
        response = self.client.post(self.url, data={"email": user.email})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EmailLog.objects.count(), 0)

    def test_patient_has_tools_to_go_not_started(self):
        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_NOT_STARTED
        )
        response = self.client.post(self.url, data={"email": patient.user.email})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EmailLog.objects.count(), 0)

    def test_patient_has_not_finished_setting_up_tools_to_go(self):
        self.token_generator = JasprToolsToGoSetupTokenGenerator
        patient = self.create_patient(tools_to_go_status=Patient.TOOLS_TO_GO_EMAIL_SENT)
        email = patient.user.email
        email_case_swapped = email[0].swapcase() + email[1:-1] + email[-1].swapcase()
        now = timezone.now()
        with freeze_time(now):
            response = self.client.post(self.url, data={"email": email_case_swapped})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        email_log = EmailLog.objects.get(user=patient.user, user_email=email, date=now)
        self.assertEqual(email_log.subject, "Welcome to Jaspr at Home")
        self.assertIn("We hope having access to things you saved", email_log.text_body)
        self.assertIn("We hope having access to things you saved", email_log.html_body)
        # Make sure the email got sent to the email on record, not the one that was
        # submitted and case insensitive compared against.
        self.assertFalse(
            EmailLog.objects.filter(user_email=email_case_swapped).exists()
        )

    def test_patient_has_finished_setting_up_tools_to_go(self):
        self.token_generator = JasprPasswordResetTokenGenerator
        patient = self.create_tools_to_go_patient()
        email = patient.user.email
        email_case_swapped = email[0].swapcase() + email[1:-1] + email[-1].swapcase()
        now = timezone.now()
        with freeze_time(now):
            response = self.client.post(self.url, data={"email": email_case_swapped})
            uidb64, token = self.uidb64_and_token(patient.user)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        email_log = EmailLog.objects.get(user=patient.user, user_email=email, date=now)
        self.assertEqual(email_log.subject, "Jaspr at Home password reset")
        self.assertIn(uidb64, email_log.text_body)
        self.assertIn(escape(uidb64), email_log.html_body)
        self.assertIn(token, email_log.text_body)
        self.assertIn(escape(token), email_log.html_body)
        self.assertIn("/reset-password/", email_log.text_body)
        self.assertIn("/reset-password/", email_log.html_body)
        # Make sure the email got sent to the email on record, not the one that was
        # submitted and case insensitive compared against.
        self.assertFalse(
            EmailLog.objects.filter(user_email=email_case_swapped).exists()
        )


class TestPatientResetPasswordRedirectAPI(UidAndTokenTestMixin, JasprApiTestCase):
    token_generator = JasprPasswordResetTokenGenerator

    def setUp(self):
        super().setUp()

        self.url = "/v1/reset-password/{uid}/{token}"

    def test_invalid_token_redirect(self):
        """
        If an invalid token is provided, is there a redirect to the appropriate
        frontend URL?
        """
        patient = self.create_patient()
        uid = self.uidb64_for(patient.user)
        token = self.invalid_token_for(patient.user)
        url = self.url.format(uid=uid, token=token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url,
            f"{resolve_frontend_url()}/forgot-password?reset-password-link=invalid",
        )

    def test_valid_token_user_not_patient_or_technician_redirect(self):
        """
        If an valid token is provided but the `User` is not a `Patient` or `Technician`, is
        there a redirect to the appropriate frontend URL?
        """
        user = self.create_user()
        uid, token = self.uidb64_and_token(user)
        url = self.url.format(uid=uid, token=token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url,
            f"{resolve_frontend_url()}/forgot-password?reset-password-link=invalid",
        )

    def test_valid_token_user_is_patient_redirect(self):
        """
        If an valid token is provided and the `User` has a `Patient` is there a
        redirect to the appropriate frontend URL?
        """
        patient = self.create_patient()
        uid, token = self.uidb64_and_token(patient.user)
        url = self.url.format(uid=uid, token=token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url,
            f"{resolve_frontend_url()}/reset-password/confirm/#uid={uid}&token={token}&userType=Patient",
        )


class TestPatientResetPasswordVerifyPhoneNumberAPI(
    UidAndTokenTestMixin, TwilioClientTestCaseMixin, JasprApiTestCase
):
    token_generator = JasprPasswordResetTokenGenerator

    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/reset-password/verify-phone-number"

    def test_verify_phone_number_successful(self):
        """
        Can an authenticated (and tools to go setup finished) patient `POST` a
        phone number that matches and get a code sent to the phone?
        """
        mobile_phone = "+15005550006"
        patient = self.create_tools_to_go_patient(user__mobile_phone=mobile_phone)
        with self.patched_twilio_verifications_create() as mock_verifications_create:
            response = self.post_with_creds(
                # NOTE: This also indirectly tests that we can compare `user.mobile_phone`
                # against the same phone number nationally (we do have the default
                # 'US' `PHONENUMBER_DEFAULT_REGION` set) that is formatted differently
                # and still have this work.
                self.uri,
                patient.user,
                {"mobile_phone": "(500) 555-0006"},
            )
            # Check that we have record of the verification being
            # created/called with Twilio.
            mock_verifications_create.assert_called_once_with(
                to=mobile_phone, channel="sms"
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["sent"])

    def test_verify_phone_number_mismatch(self):
        """
        Is an error message returned properly when the phone number submitted doesn't
        match the `User`'s phone number?
        """
        mobile_phone = "+15005550006"
        patient = self.create_tools_to_go_patient(user__mobile_phone=mobile_phone)
        with self.patched_twilio_verifications_create() as mock_verifications_create:
            response = self.post_with_creds(
                self.uri, patient.user, {"mobile_phone": "(500) 555-0005"}
            )
            mock_verifications_create.assert_not_called()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            VerifyPhoneNumberSerializer.default_error_messages["mobile_phone_mismatch"],
        )

    def test_verify_phone_number_throws_verification_exception(self):
        """
        If a `VerificationException` is thrown when sending the verification code, is
        it caught and an error message returned back?
        """
        mobile_phone = "+15005550006"
        patient = self.create_tools_to_go_patient(user__mobile_phone=mobile_phone)
        with self.patched_twilio_verifications_create() as mock_verifications_create:
            mock_verifications_create.side_effect = self.twilio_rest_exception_instance
            response = self.post_with_creds(
                self.uri, patient.user, {"mobile_phone": "(500) 555-0006"}
            )

        # NOTE: This might not exactly be the best/most logically correct status code,
        # but we're doing this for now because it allows us to easily throw the error
        # in the serializer and handle it that way vs. throwing it with a different
        # status code and having the frontend have to handle a different status code, etc.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            VerificationTwilioException.GENERIC_ERROR_MESSAGE,
        )

    def test_tools_to_go_status_other_than_setup_finished_forbidden(self):
        """
        If the Patient's tools to go status is something other than "Setup
        Finished", is `POST`ing to this endpoint forbidden?
        """
        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED
        )
        mobile_phone = "+15005550006"
        response = self.post_with_creds(
            self.uri, patient.user, {"mobile_phone": mobile_phone}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPatientResetPasswordCheckPhoneNumberCodeAPI(
    UidAndTokenTestMixin, TwilioClientTestCaseMixin, JasprApiTestCase
):
    token_generator = JasprPasswordResetTokenGenerator
    set_password_token_generator = JasprSetPasswordTokenGenerator

    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/reset-password/check-phone-number-code"

    def test_check_phone_number_verification_successful(self):
        """
        Can an authenticated (and tools to go setup finished) patient `POST` a
        code and finish the phone number verification flow?
        """
        mobile_phone = "+15005550006"
        patient = self.create_tools_to_go_patient(
            **patient_before_login_setup_kwargs(), user__mobile_phone=mobile_phone
        )
        code = "777777"

        post_data = {"code": code}
        with self.patched_twilio_verification_checks_create() as mock_verification_checks_create:
            time_before = timezone.now()
            response = self.post_with_creds(
                self.uri,
                patient.user,
                post_data,
            )
            # Check that we have record of the verification check being
            # created/called with Twilio.
            mock_verification_checks_create.assert_called_once_with(
                to=mobile_phone, code=code
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(
            patient.tools_to_go_status,
            Patient.TOOLS_TO_GO_SETUP_FINISHED,
        )
        self.assertEqual(len(response.data), 1)
        self.assertTrue(
            self.set_password_token_generator().check_token(
                patient.user, response.data["set_password_token"]
            )
        )

    def test_check_phone_number_verification_code_invalid(self):
        """
        If a code is `POST`ed that is invalid, is the correct error message returned?
        """

        def patched_verification_checks_create_code_invalid(
            *args, **kwargs
        ) -> NonCallableMagicMock:
            mock = NonCallableMagicMock(spec_set=VerificationCheckInstance)
            mock.sid = "verification-check-sid-code-invalid"
            mock.status = "pending"
            return mock

        mobile_phone = "+15005550006"
        patient = self.create_tools_to_go_patient(user__mobile_phone=mobile_phone)
        code = "777777"
        with self.patched_twilio_verification_checks_create() as mock_verification_checks_create:
            mock_verification_checks_create.side_effect = (
                patched_verification_checks_create_code_invalid
            )
            response = self.post_with_creds(self.uri, patient.user, {"code": code})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            VerificationCodeInvalid.error_message,
        )

    def test_check_phone_number_verification_code_denied(self):
        """
        If a code is `POST`ed that is denied, is the correct error message returned?
        """

        def patched_verification_checks_create_code_denied(
            *args, **kwargs
        ) -> NonCallableMagicMock:
            mock = NonCallableMagicMock(spec_set=VerificationCheckInstance)
            mock.sid = "verification-check-sid-code-denied"
            mock.status = "denied"
            return mock

        mobile_phone = "+15005550006"
        patient = self.create_tools_to_go_patient(user__mobile_phone=mobile_phone)
        code = "777777"
        with self.patched_twilio_verification_checks_create() as mock_verification_checks_create:
            mock_verification_checks_create.side_effect = (
                patched_verification_checks_create_code_denied
            )
            response = self.post_with_creds(self.uri, patient.user, {"code": code})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            VerificationCodeNotFound.error_message,
        )

    def test_check_phone_number_verification_throws_verification_exception(self):
        """
        If a `VerificationException` is thrown when checking the verification code, is
        it caught and an error message returned back?
        """
        mobile_phone = "+15005550006"
        patient = self.create_tools_to_go_patient(user__mobile_phone=mobile_phone)
        code = "777777"
        with self.patched_twilio_verification_checks_create() as mock_verification_checks_create:
            mock_verification_checks_create.side_effect = (
                self.twilio_rest_exception_instance
            )
            response = self.post_with_creds(self.uri, patient.user, {"code": code})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0],
            VerificationTwilioException.GENERIC_ERROR_MESSAGE,
        )

    def test_tools_to_go_status_other_than_setup_finished_forbidden(self):
        """
        If the Patient's tools to go status is something other than "Setup
        Finished", is `POST`ing to this endpoint forbidden?
        """
        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED
        )
        code = "7777777"
        response = self.post_with_creds(self.uri, patient.user, {"code": code})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPatientResetPasswordSetPasswordAPI(UidAndTokenTestMixin, JasprApiTestCase):
    token_generator = JasprPasswordResetTokenGenerator

    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/reset-password/set-password"

    def test_can_set_password(self):
        """
        Can an authenticated (and tools to go setup finished) patient set his/her
        password if a valid `set_password_token` (along with authentication `uid` and
        `token`) is provided?
        """
        patient = self.create_tools_to_go_patient(
            user__password_complex=False,
            user__password_changed=None,
        )
        time_before_patch = timezone.now()
        new_password = "TheGoose87623##"
        set_password_token = self.valid_token_for(
            patient.user, token_generator=JasprSetPasswordTokenGenerator
        )
        response = self.post_with_creds(
            self.uri,
            patient.user,
            data={"password": new_password, "set_password_token": set_password_token},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)
        patient.user.refresh_from_db()
        self.assertTrue(patient.user.check_password(new_password))
        self.assertGreater(patient.user.password_changed, time_before_patch)
        self.assertTrue(patient.user.password_complex)

    def test_password_not_complex(self):
        """
        Check that password complexity checking is not done for validation, but that
        the `password_complex` field is set accordingly. The above test (at the time
        of writing) tests for a complex password while this test tests for a
        non-complex password and still makes sure everything else works except for
        setting the field.
        """
        patient = self.create_tools_to_go_patient(
            user__password_complex=False,
            user__password_changed=None,
        )
        time_before_patch = timezone.now()
        new_password = "a"
        set_password_token = self.valid_token_for(
            patient.user, token_generator=JasprSetPasswordTokenGenerator
        )
        response = self.post_with_creds(
            self.uri,
            patient.user,
            data={"password": new_password, "set_password_token": set_password_token},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)
        patient.user.refresh_from_db()
        self.assertTrue(patient.user.check_password(new_password))
        self.assertGreater(patient.user.password_changed, time_before_patch)
        self.assertFalse(patient.user.password_complex)

    def test_token_invalid(self):
        """
        If the provided `set_password_token` is invalid, is a 403 response returned?
        """
        patient = self.create_tools_to_go_patient(
            user__password_complex=False,
            user__password_changed=None,
        )
        new_password = "TheGoose87623##"
        set_password_token = self.invalid_token_for(
            patient.user, token_generator=JasprSetPasswordTokenGenerator
        )
        response = self.post_with_creds(
            self.uri,
            patient.user,
            data={"password": new_password, "set_password_token": set_password_token},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_requires_tools_to_go_setup_finished(self):
        """
        This is partially a test to make sure that `HasToolsToGoSetupFinished` is
        working properly. You shouldn't be able to change your Jaspr account info
        until you're at the "Setup Finished" tools to go status.
        """
        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED
        )
        new_password = "TheGoose87623##"
        set_password_token = self.valid_token_for(
            patient.user, token_generator=JasprSetPasswordTokenGenerator
        )
        response = self.post_with_creds(
            self.uri,
            patient.user,
            data={"password": new_password, "set_password_token": set_password_token},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
