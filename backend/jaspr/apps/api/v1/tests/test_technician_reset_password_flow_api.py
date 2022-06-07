from datetime import timedelta

from django.core import mail
from django.utils import timezone
from django.utils.html import escape
from freezegun import freeze_time
from rest_framework import status

from jaspr.apps.common.functions import resolve_frontend_url
from jaspr.apps.common.tests.mixins import UidAndTokenTestMixin
from jaspr.apps.kiosk.models import Patient
from jaspr.apps.kiosk.tokens import (
    JasprExtraSecurityTokenGenerator,
    JasprPasswordResetTokenGenerator,
)
from jaspr.apps.message_logs.models import EmailLog
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestTechnicianResetPasswordAPI(UidAndTokenTestMixin, JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.url = "/v1/reset-password"
        self.token_generator = JasprPasswordResetTokenGenerator

    def test_user_is_not_patient_or_technician(self):
        user = self.create_user()
        response = self.client.post(self.url, data={"email": user.email})

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EmailLog.objects.count(), 0)

    def test_technician_receives_reset_password_email_if_activated(self):
        """
        Does a technician receive the reset password email after requesting a
        password reset if he/she is already activated?
        """
        technician = self.create_technician(activated=True)
        now = timezone.now()
        with freeze_time(now):
            response = self.client.post(self.url, data={"email": technician.user.email})
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            email_log = EmailLog.objects.get(
                user=technician.user, user_email=technician.user.email, date=now
            )
            uidb64, token = self.uidb64_and_token(technician.user)

        self.assertEqual(EmailLog.objects.count(), 1)
        self.assertEqual(email_log.subject, "Jaspr at Home password reset")
        self.assertIn(uidb64, email_log.text_body)
        self.assertIn(escape(uidb64), email_log.html_body)
        self.assertIn(token, email_log.text_body)
        self.assertIn(escape(token), email_log.html_body)
        self.assertIn("/reset-password/", email_log.text_body)
        self.assertIn("/reset-password/", email_log.html_body)

    def test_technician_receives_activation_email_if_not_activated(self):
        """
        Does a technician receive the activation email after requesting a password
        reset if he/she is not activated?
        """
        technician = self.create_technician(activated=False)
        now = timezone.now()
        with freeze_time(now):
            response = self.client.post(self.url, data={"email": technician.user.email})
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            email_log = EmailLog.objects.get(
                user=technician.user, user_email=technician.user.email, date=now
            )
            uidb64, token = self.uidb64_and_token(
                technician.user, token_generator=JasprExtraSecurityTokenGenerator
            )

        self.assertEqual(EmailLog.objects.count(), 1)
        self.assertEqual(email_log.subject, "Jaspr Tech Account Activation")
        self.assertIn(uidb64, email_log.text_body)
        self.assertIn(escape(uidb64), email_log.html_body)
        self.assertIn(token, email_log.text_body)
        self.assertIn(escape(token), email_log.html_body)
        self.assertIn("/technician/activate/", email_log.text_body)
        self.assertIn("/technician/activate/", email_log.html_body)

    def test_technician_is_sent_email_to_address_on_file_not_address_submitted(self):
        """ Does email get sent only to email on file, not submitted email to prevent hackery?"""
        technician = self.create_technician()
        email = technician.user.email
        email_case_swapped = email[0].swapcase() + email[1:-1] + email[-1].swapcase()
        response = self.client.post(self.url, data={"email": email_case_swapped})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            EmailLog.objects.filter(user_email=email_case_swapped).exists()
        )


class TestTechnicianResetPasswordRedirectAPI(UidAndTokenTestMixin, JasprApiTestCase):
    token_generator = JasprPasswordResetTokenGenerator

    def setUp(self):
        super().setUp()

        self.url = "/v1/reset-password/{uid}/{token}"

    def test_invalid_token_redirect(self):
        """ If an invalid token is provided, is there a redirect to the appropriate frontend URL? """
        technician = self.create_technician()
        uid = self.uidb64_for(technician.user)
        token = self.invalid_token_for(technician.user)
        url = self.url.format(uid=uid, token=token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url,
            f"{resolve_frontend_url()}/forgot-password?reset-password-link=invalid",
        )

    def test_valid_token_user_is_technician_redirect(self):
        """ When technician user provides valid token,is there a redirect to the appropriate frontend URL? """
        technician = self.create_technician()
        uid, token = self.uidb64_and_token(technician.user)
        url = self.url.format(uid=uid, token=token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url,
            f"{resolve_frontend_url(technician=technician)}/reset-password/confirm/#uid={uid}&token={token}&userType=Technician",
        )


class TestTechnicianResetPasswordSetPasswordAPI(UidAndTokenTestMixin, JasprApiTestCase):
    token_generator = JasprPasswordResetTokenGenerator

    def setUp(self):
        super().setUp()
        self.uri = "/v1/technician/reset-password/set-password"

    def test_can_set_password(self):
        """
        Can an authenticated technician set password with valid `uid` and `token`?
        """
        technician = self.create_technician()
        time_before_patch = timezone.now()
        new_password = "TheGoose87623##"

        freeze_at = time_before_patch + timedelta(microseconds=1)
        with freeze_time(time_before_patch + timedelta(microseconds=1)):
            response = self.post_with_creds(
                self.uri,
                technician.user,
                data={"password": new_password},
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("expiry" in response.data)
        self.assertTrue("token" in response.data)
        self.assertTrue("session" in response.data)
        self.assertEqual("Technician", response.data["session"]["user_type"])
        technician.user.refresh_from_db()
        self.assertTrue(technician.user.check_password(new_password))
        self.assertGreater(technician.user.password_changed, time_before_patch)
        self.assertTrue(technician.user.password_complex)

        self.assertEqual(len(mail.outbox), 1)
        email_log = EmailLog.objects.get(user_id=technician.user_id, date=freeze_at)
        self.assertEqual(
            email_log.subject,
            "Jaspr at Home password reset",
        )

    def test_password_not_complex(self):
        """
        Does the endpoint enforce password requirements for the `Technician`?
        """
        technician = self.create_technician()
        new_password = "TheGoose##"
        response = self.post_with_creds(
            self.uri,
            technician.user,
            data={"password": new_password},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data["password"],
            [
                (
                    "Passwords must be at least 8 characters and have at least one "
                    "uppercase character, one lowercase character, and one number."
                )
            ],
        )

    def test_token_invalid(self):
        """
        If the provided `token` is invalid, is a 400 response returned with a nice
        error message?
        """
        technician = self.create_technician()
        new_password = "TheGoose87623##"
        response = self.post_with_creds(
            self.uri,
            technician.user,
            data={"password": new_password},
            # Use a different token generator than the correct one
            # (`JasprPasswordResetTokenGenerator`) to simulate an invalid token.
            token_generator=JasprExtraSecurityTokenGenerator,
        )

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )
        self.assertEqual(
            response.data["non_field_errors"],
            [
                (
                    "The link is invalid. Please get a new link sent to you or contact "
                    "support. Be aware that links currently expire after 15 days."
                )
            ],
        )

    def test_user_type_other_than_technician_forbidden(self):
        """
        Since the authentication/permissions here are different/unusual compared to
        other types of authentication/permissions, it was difficult to use the
        standard permissions testing framework here. Hence we add one test to make
        sure that a `Patient`, even if authenticated successfully with a valid
        `token`, hits a `403` forbidden response code.
        """
        patient = self.create_patient(
            user__password_complex=False,
            user__password_changed=None,
            tools_to_go_status=Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
        )
        self.set_patient_creds(patient)
        new_password = "TheGoose87623##"
        response = self.post_with_creds(
            self.uri,
            patient.user,
            data={"password": new_password},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
