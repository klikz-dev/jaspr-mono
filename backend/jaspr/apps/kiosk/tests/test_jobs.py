from jaspr.apps.kiosk.jobs import check_and_resend_tools_to_go_setup_email
from jaspr.apps.kiosk.models import Patient
from jaspr.apps.message_logs.models import EmailLog
from jaspr.apps.test_infrastructure.testcases import JasprRedisTestCase


class TestCheckAndResendToolsToGoSetupEmail(JasprRedisTestCase):
    def setUp(self):
        super().setUp()

        self.patient = self.create_patient()

    def test_email_re_sent_if_specified_tools_to_go_statuses(self):
        """
        Does the email get resent if the `Patient`'s `tools_to_go_status`
        is one of the available ones to resend the email with?
        """
        email_log_counter = 1
        for status in (
            Patient.TOOLS_TO_GO_NOT_STARTED,
            Patient.TOOLS_TO_GO_EMAIL_SENT,
        ):
            with self.subTest(status=status):
                if self.patient.tools_to_go_status != status:
                    self.patient.tools_to_go_status = status
                    self.patient.save()
                check_and_resend_tools_to_go_setup_email.delay(
                    self.patient.pk, email_log_counter
                )
                self.assertEqual(
                    EmailLog.objects.filter(user_id=self.patient.user_id).count(),
                    email_log_counter,
                )
                email_log_counter += 1

    def test_email_not_re_sent_if_not_specified_tools_to_go_statuses(self):
        """
        Does the email not get resent if the `Patient`'s `tools_to_go_status`
        is not one of the available ones to resend the email with?
        """
        self.patient.tools_to_go_status = Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED
        self.patient.save()
        check_and_resend_tools_to_go_setup_email.delay(self.patient.pk, 1)
        self.assertEqual(
            EmailLog.objects.filter(user_id=self.patient.user_id).count(), 0
        )
