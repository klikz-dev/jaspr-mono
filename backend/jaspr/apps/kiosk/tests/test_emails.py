from datetime import timedelta

from django.conf import settings
from django.core import mail
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.html import escape
from django.utils.http import urlsafe_base64_encode
from django_rq.jobs import Job
from freezegun import freeze_time

from jaspr.apps.common.functions import resolve_frontend_url
from jaspr.apps.kiosk.emails import (
    send_reset_password_email,
    send_technician_activation_confirmation_email,
    send_technician_activation_email,
    send_tools_to_go_confirmation_email,
    send_tools_to_go_setup_email,
)
from jaspr.apps.kiosk.models import Patient
from jaspr.apps.kiosk.tokens import (
    JasprExtraSecurityTokenGenerator,
    JasprPasswordResetTokenGenerator,
    JasprToolsToGoSetupTokenGenerator,
)
from jaspr.apps.message_logs.models import EmailLog
from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class TestJasprToolsToGoSetupEmail(JasprTestCase):
    def setUp(self):
        self.patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_NOT_STARTED
        )
        self.now = timezone.now()

    def test_email_delivery_and_content(self):
        with freeze_time(self.now):
            send_tools_to_go_setup_email(self.patient.user)

        self.assertEqual(len(mail.outbox), 1)
        email_log = EmailLog.objects.get(date=self.now)
        self.assertEqual(email_log.user, self.patient.user)
        self.assertEqual(email_log.user_email, self.patient.user.email)
        self.assertEqual(email_log.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email_log.subject, "Welcome to Jaspr at Home")
        self.assertIn("We hope having access to things you saved", email_log.text_body)
        self.assertIn("We hope having access to things you saved", email_log.html_body)
        self.assertEqual(email_log.email_response, "1")

    def test_first_resend_delivery_and_content(self):
        with freeze_time(self.now + timedelta(days=3)):
            send_tools_to_go_setup_email(
                self.patient.user,
                template_base="kiosk/tools_to_go_setup_first_resend",
            )

        self.assertEqual(len(mail.outbox), 1)
        email_log = EmailLog.objects.get(date=self.now + timedelta(days=3))
        self.assertEqual(email_log.user, self.patient.user)
        self.assertEqual(email_log.user_email, self.patient.user.email)
        self.assertEqual(email_log.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email_log.subject, "Welcome to Jaspr at Home")
        self.assertIn("We wanted to let you know we are thinking", email_log.text_body)
        self.assertIn("We wanted to let you know we are thinking", email_log.html_body)
        self.assertEqual(email_log.email_response, "1")

    def test_second_resend_delivery_and_content(self):
        with freeze_time(self.now + timedelta(days=7)):
            send_tools_to_go_setup_email(
                self.patient.user,
                template_base="kiosk/tools_to_go_setup_second_resend",
            )

        self.assertEqual(len(mail.outbox), 1)
        email_log = EmailLog.objects.get(date=self.now + timedelta(days=7))
        self.assertEqual(email_log.user, self.patient.user)
        self.assertEqual(email_log.user_email, self.patient.user.email)
        self.assertEqual(email_log.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email_log.subject, "Welcome to Jaspr at Home")
        self.assertIn(
            "We are just hoping to touch base and let you", email_log.text_body
        )
        self.assertIn(
            "We are just hoping to touch base and let you", email_log.html_body
        )
        self.assertEqual(email_log.email_response, "1")


class TestResetPasswordEmail(JasprTestCase):
    def setUp(self):
        self.patient = self.create_tools_to_go_patient()
        self.now = timezone.now()
        self.b64_uid = urlsafe_base64_encode(force_bytes(self.patient.user_id))

    def test_email_delivery_and_content(self):
        with freeze_time(self.now):
            token = JasprPasswordResetTokenGenerator().make_token(self.patient.user)
            jaspr_reset_password_url = (
                f"{settings.BACKEND_URL_BASE}/v1/reset-password/{self.b64_uid}/{token}"
            )
            jaspr_reset_password_url_escaped = escape(jaspr_reset_password_url)
            send_reset_password_email(self.patient.user)

        self.assertEqual(len(mail.outbox), 1)
        email_log = EmailLog.objects.get(date=self.now)
        self.assertEqual(email_log.user, self.patient.user)
        self.assertEqual(email_log.user_email, self.patient.user.email)
        self.assertEqual(email_log.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email_log.subject, "Jaspr at Home password reset")
        self.assertIn(jaspr_reset_password_url, email_log.text_body)
        self.assertIn(jaspr_reset_password_url_escaped, email_log.html_body)
        self.assertEqual(email_log.email_response, "1")


class TestJasprToolsToGoConfirmationEmail(JasprTestCase):
    def test_email_delivery_and_content(self):
        # NOTE: `tools_to_go_status` is arbitrary at this point, but
        # we're using `TOOLS_TO_GO_SETUP_FINISHED` since it would emulate
        # the stauts ` Patient` would have when this email is actually sent.
        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_SETUP_FINISHED
        )
        now = timezone.now()
        with freeze_time(now):
            send_tools_to_go_confirmation_email(patient.user)

        self.assertEqual(len(mail.outbox), 1)
        email_log = EmailLog.objects.get(date=now)
        self.assertEqual(email_log.user, patient.user)
        self.assertEqual(email_log.user_email, patient.user.email)
        self.assertEqual(email_log.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(
            email_log.subject,
            "Congratulations for setting up your Jaspr at Home account",
        )
        self.assertIn(
            "We are so glad you're here and that you've signed up for",
            email_log.text_body,
        )
        self.assertIn(
            "We are so glad you're here and that you've signed up for",
            email_log.html_body,
        )
        self.assertEqual(email_log.email_response, "1")


class TestSendTechnicianActivationEmail(JasprTestCase):
    def setUp(self):
        some_datetime_past = timezone.now() - timedelta(days=18)
        self.technician = self.create_technician(
            activation_email_last_sent_at=some_datetime_past
        )
        self.now = timezone.now()
        self.b64_uid = urlsafe_base64_encode(force_bytes(self.technician.user_id))

    def test_email_delivery_and_content(self):
        with freeze_time(self.now):
            result = send_technician_activation_email(self.technician)
            token = JasprExtraSecurityTokenGenerator().make_token(self.technician.user)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], Job)
        assert result[1] == ["activation_email_last_sent_at"]
        self.assertEqual(len(mail.outbox), 1)
        email_log = EmailLog.objects.get(date=self.now)
        self.assertEqual(email_log.user, self.technician.user)
        self.assertEqual(email_log.user_email, self.technician.user.email)
        self.assertEqual(email_log.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(
            email_log.subject,
            "Jaspr Tech Account Activation",
        )
        expected_activation_url = (
            f"{settings.BACKEND_URL_BASE}/v1/technician/activate/{self.b64_uid}/{token}"
        )
        self.assertIn(expected_activation_url, email_log.text_body)
        self.assertIn(
            "Click or copy paste the link below into your browser to activate your Jaspr Tech account.",
            email_log.text_body,
        )
        self.assertIn(expected_activation_url, email_log.html_body)
        self.assertIn(
            "Click the button below to activate your Jaspr Tech account.",
            email_log.html_body,
        )
        self.assertEqual(email_log.email_response, "1")
        self.technician.refresh_from_db()
        self.assertEqual(self.technician.activation_email_last_sent_at, self.now)


class TestSendTechnicianActivationConfirmationEmail(JasprTestCase):
    def setUp(self):
        recently = timezone.now() - timedelta(minutes=30)
        self.technician = self.create_technician(activation_email_last_sent_at=recently)
        self.now = timezone.now()

    def test_email_delivery_and_content(self):
        with freeze_time(self.now):
            send_technician_activation_confirmation_email(self.technician)
        self.assertEqual(len(mail.outbox), 1)
        email_log = EmailLog.objects.get(date=self.now)
        self.assertEqual(email_log.user, self.technician.user)
        self.assertEqual(email_log.user_email, self.technician.user.email)
        self.assertEqual(email_log.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(
            email_log.subject,
            "Congrats on activating your Jaspr Tech account",
        )
        expected_frontend_tech_login_url = resolve_frontend_url(
            technician=self.technician
        )
        self.assertIn(expected_frontend_tech_login_url, email_log.text_body)
        self.assertIn(
            "Congrats on activating your Jaspr Tech account.",
            email_log.text_body,
        )
        self.assertNotIn("href=", email_log.text_body)
        self.assertIn(expected_frontend_tech_login_url, email_log.html_body)
        self.assertIn(
            "Congrats on activating your Jaspr Tech account.",
            email_log.html_body,
        )
        self.assertIn("href=", email_log.html_body)
        self.assertEqual(email_log.email_response, "1")
