import logging
import random
from datetime import datetime, timedelta
from itertools import product
from unittest.mock import NonCallableMagicMock

import django_rq
from django.conf import settings
from django.core import mail
from django.utils import timezone
from freezegun import freeze_time
from jaspr.apps.api.v1.serializers import (
    CheckPhoneNumberVerificationSerializer,
    VerifyPhoneNumberSerializer,
)
from jaspr.apps.api.v1.serializers import logger as jaspr_v1_serializers_logger
from jaspr.apps.common.functions import resolve_frontend_url
from jaspr.apps.common.phonenumbers.verify import (
    VerificationCodeInvalid,
    VerificationCodeNotFound,
    VerificationTwilioException,
)
from jaspr.apps.common.tests.mixins import UidAndTokenTestMixin
from jaspr.apps.kiosk.authentication import JasprToolsToGoUidAndTokenAuthentication
from jaspr.apps.kiosk.jobs import check_and_resend_tools_to_go_setup_email
from jaspr.apps.kiosk.models import JasprSession, Patient, PatientCopingStrategy as KioskPatientCopingStrategy
from jaspr.apps.jah.models import PatientCopingStrategy as JAHPatientCopingStrategy
from jaspr.apps.kiosk.tokens import JasprSetPasswordTokenGenerator
from jaspr.apps.message_logs.models import EmailLog
from jaspr.apps.test_infrastructure.helpers import enter_transaction_then_roll_back
from jaspr.apps.test_infrastructure.mixins.common_mixins import (
    TwilioClientTestCaseMixin,
)
from jaspr.apps.test_infrastructure.mixins.redis_mixins import RedisTestCaseMixin
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import (
    JasprApiRedisTestCase,
    JasprApiTestCase,
)
from rest_framework import status
from twilio.rest.verify.v2.service.verification_check import VerificationCheckInstance
from jaspr.apps.kiosk.activities.activity_utils import ActivityType

from .helpers import assert_patient_logged_in


class TestPatientToolsToGoVerificationSetupAPIPermissions(
    RedisTestCaseMixin, JasprTestResourcePermissions
):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(resource_pattern="patient/at-home-setup", version_prefix="v1")
        self.action_group_map["create"]["allowed_groups"] = ["Patient"]
        self.groups["Patient"]["set_creds_kwargs"] = {"in_er": True, "encounter": True}


class TestPatientToolsToGoVerificationRedirectAPI(
    UidAndTokenTestMixin, JasprApiTestCase
):
    token_generator = JasprToolsToGoUidAndTokenAuthentication.token_generator

    def setUp(self):
        super().setUp()

        self.url = "/v1/patient/at-home-setup/{uid}/{token}"

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
            response.url, f"{resolve_frontend_url()}/?at-home-setup-link=invalid",
        )

    def test_valid_token_user_not_patient_redirect(self):
        """
        If an valid token is provided but the `User` is not a `Patient`, is
        there a redirect to the appropriate frontend URL?
        """
        user = self.create_user()
        uid, token = self.uidb64_and_token(user)
        url = self.url.format(uid=uid, token=token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url, f"{resolve_frontend_url()}/?at-home-setup-link=invalid",
        )

    def test_valid_token_tools_to_go_setup_not_finished_redirect(self):
        """
        If an valid token is provided and the `Patient` hasn't finished setting
        up tools to go, is there a redirect to the appropriate frontend URL?
        """
        patient = self.create_patient()
        uid, token = self.uidb64_and_token(patient.user)
        url = self.url.format(uid=uid, token=token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url,
            f"{resolve_frontend_url()}/activate-tools-to-go/#uid={uid}&token={token}",
        )

    def test_valid_token_tools_to_go_setup_finished_redirect(self):
        """
        If an valid token is provided and the `Patient` has finished setting up
        tools to go, is there a redirect to the appropriate frontend URL?
        """
        patient = self.create_tools_to_go_patient()
        uid, token = self.uidb64_and_token(patient.user)
        url = self.url.format(uid=uid, token=token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(
            response.url, f"{resolve_frontend_url()}?at-home-setup-link=already-set-up",
        )


class TestPatientToolsToGoVerificationSetupAPI(JasprApiRedisTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/at-home-setup"

    def _test_future_resend_jobs(
        self, request_time: datetime, patient: Patient
    ) -> None:
        """
        Assertion helper method to check if the jobs were queued to check and resend
        the tools to go setup email in the future. This method also time travels to
        the future and runs the jobs, making sure that works properly.
        """
        scheduler = django_rq.get_scheduler()
        first_job_time = request_time + timedelta(days=3)
        second_job_time = request_time + timedelta(days=7)
        jobs_with_times = list(scheduler.get_jobs(with_times=True))
        self.assertEqual(len(jobs_with_times), 2)
        (job1, scheduled_time1), (job2, scheduled_time2) = jobs_with_times
        self.assertEqual(job1.func, check_and_resend_tools_to_go_setup_email)
        self.assertEqual(job1.created_at, request_time.replace(tzinfo=None))
        self.assertEqual(
            scheduled_time1, first_job_time.replace(tzinfo=None, microsecond=0)
        )
        self.assertEqual(job1.args[0], patient.pk)
        self.assertEqual(job1.args[1], 1)
        self.assertEqual(job2.func, check_and_resend_tools_to_go_setup_email)
        self.assertEqual(job2.created_at, request_time.replace(tzinfo=None))
        self.assertEqual(
            scheduled_time2,
            (request_time + timedelta(days=7)).replace(tzinfo=None, microsecond=0),
        )
        self.assertEqual(job2.args[0], patient.pk)
        self.assertEqual(job2.args[1], 2)
        with freeze_time(first_job_time):
            jobs_to_queue = list(scheduler.get_jobs_to_queue())
            self.assertEqual(len(jobs_to_queue), 1)
            self.assertEqual(jobs_to_queue[0], job1)
            django_rq.get_queue().enqueue_job(job1)
        scheduler.cancel(job1)
        with freeze_time(second_job_time):
            jobs_to_queue = list(scheduler.get_jobs_to_queue())
            self.assertEqual(len(jobs_to_queue), 1)
            self.assertEqual(jobs_to_queue[0], job2)
            django_rq.get_queue().enqueue_job(job2)
        # Check that there are now three emails sent
        # (the initial one and two re-sent ones).
        self.assertEqual(EmailLog.objects.filter(user_id=patient.user_id).count(), 3)

    def test_tools_to_go_verification_setup_successful(self):
        """
        Can an authenticated (and tools to go setup not started) patient `POST`
        an email and a phone number and start the verification flow?
        """
        patient = self.create_patient()
        encounter = self.create_patient_encounter(patient=patient)
        self.set_patient_creds(patient, in_er=True, encounter=encounter)

        email = "vroooooooom@jasprhealth.com"
        mobile_phone = "+15005550006"
        now = timezone.now()
        with freeze_time(now), self.rq_jobs_async(True):
            response = self.client.post(
                self.uri, data={"email": email, "mobile_phone": mobile_phone}
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], email)
        self.assertEqual(response.data["mobile_phone"], mobile_phone)
        self.assertEqual(
            response.data["tools_to_go_status"], Patient.TOOLS_TO_GO_EMAIL_SENT
        )
        patient.user.refresh_from_db()
        self.assertEqual(patient.user.email, email)
        self.assertEqual(patient.user.mobile_phone, mobile_phone)
        patient.refresh_from_db()
        self.assertEqual(patient.tools_to_go_status, Patient.TOOLS_TO_GO_EMAIL_SENT)
        # Check that we have record of an email being sent.
        EmailLog.objects.get(user=patient.user, user_email=email)
        # Check that the future resend jobs have been queued and work properly.
        self._test_future_resend_jobs(now, patient)

    def test_tools_to_go_verification_setup_email_already_exists(self):
        """
        Can an authenticated (and tools to go setup not started) patient `POST`
        an email that belongs to another user in the system (alongside `POST`ing a
        valid phone number) and get a successful response, but not have the email
        sent?

        NOTE: This is currently how we handle hiding emails/sensitive information. We
        don't tell end users if the email exists in the system or not. If they `POST`
        a valid `email` and `phone_number` (valid in terms of validation) we give
        them a successful response.
        """
        email = "vroooooooom@jasprhealth.com"
        mobile_phone = "+15005550006"
        existing_patient = self.create_patient(user__email=email)
        patient = self.create_patient()
        encounter = self.create_patient_encounter(patient=patient)
        initial_email = patient.user.email
        self.set_patient_creds(patient, in_er=True, encounter=encounter)
        now = timezone.now()
        with freeze_time(now), self.rq_jobs_async(True), self.assertLogs(
            'jaspr.apps.api.v1.serializers.serializers', logging.WARNING
        ) as l:
            response = self.client.post(
                self.uri, data={"email": email, "mobile_phone": mobile_phone}
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], email)
        self.assertEqual(response.data["mobile_phone"], mobile_phone)
        self.assertEqual(
            response.data["tools_to_go_status"], Patient.TOOLS_TO_GO_EMAIL_SENT
        )
        patient.user.refresh_from_db()
        self.assertEqual(patient.user.email, initial_email)
        self.assertEqual(patient.user.mobile_phone, mobile_phone)
        patient.refresh_from_db()
        self.assertEqual(patient.tools_to_go_status, Patient.TOOLS_TO_GO_EMAIL_SENT)
        # Check that no emails were sent to either user.
        self.assertEqual(
            EmailLog.objects.filter(
                user__in=[existing_patient.user, patient.user], user_email=email,
            ).count(),
            0,
        )
        # Check that the existing email warning was logged.
        self.assertIn(
            f"For Jaspr at Home setup for Patient pk {patient.pk}, email "
            f"{email} was given but was already present in the database.",
            l.output[0],
        )

    def test_tools_to_go_status_other_than_not_started_forbidden(self):
        """
        If the Patient's tools to go status is something other than "Not
        Started", is `POST`ing to this endpoint forbidden?
        """
        patient = self.create_patient(tools_to_go_status=Patient.TOOLS_TO_GO_EMAIL_SENT)
        encounter = self.create_patient_encounter(patient=patient)
        self.set_patient_creds(patient, in_er=True)
        email = "vroooooooom@jasprhealth.com"
        mobile_phone = "+15005550006"
        with self.rq_jobs_async(True):
            response = self.client.post(
                self.uri, data={"email": email, "mobile_phone": mobile_phone}
            )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPatientVerifyPhoneNumberAPI(
    UidAndTokenTestMixin, TwilioClientTestCaseMixin, JasprApiTestCase
):
    token_generator = JasprToolsToGoUidAndTokenAuthentication.token_generator

    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/verify-phone-number"

    def test_verify_phone_number_successful(self):
        """
        Can an authenticated (and tools to go email sent) patient `POST` a
        phone number that matches and get a code sent to the phone?
        """
        mobile_phone = "+15005550006"
        patient = self.create_patient(
            user__mobile_phone=mobile_phone,
            tools_to_go_status=Patient.TOOLS_TO_GO_EMAIL_SENT,
        )
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
        patient = self.create_patient(
            user__mobile_phone=mobile_phone,
            tools_to_go_status=Patient.TOOLS_TO_GO_EMAIL_SENT,
        )
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
        patient = self.create_patient(
            user__mobile_phone=mobile_phone,
            tools_to_go_status=Patient.TOOLS_TO_GO_EMAIL_SENT,
        )
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

    def test_tools_to_go_status_other_than_permitted_forbidden(self):
        """
        If the Patient's tools to go status is something other than "Email
        Sent" or "Phone Number Verified", is `POST`ing to this endpoint forbidden?
        """
        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_SETUP_FINISHED
        )
        mobile_phone = "+15005550006"
        response = self.post_with_creds(
            self.uri, patient.user, {"mobile_phone": mobile_phone}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPatientCheckPhoneNumberCodeAPI(
    UidAndTokenTestMixin, TwilioClientTestCaseMixin, JasprApiTestCase
):
    token_generator = JasprToolsToGoUidAndTokenAuthentication.token_generator
    set_password_token_generator = JasprSetPasswordTokenGenerator

    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/check-phone-number-code"

    def test_check_phone_number_verification_successful(self):
        """
        Can an authenticated (and tools to go email sent) patient `POST` a code
        and finish the phone number verification flow?
        """
        mobile_phone = "+15005550006"
        patient = self.create_patient(
            user__mobile_phone=mobile_phone,
            tools_to_go_status=Patient.TOOLS_TO_GO_EMAIL_SENT,
        )
        code = "777777"

        post_data = {"code": code}
        with self.patched_twilio_verification_checks_create() as mock_verification_checks_create:
            response = self.post_with_creds(self.uri, patient.user, post_data)
            # Check that we have record of the verification check being
            # created/called with Twilio.
            mock_verification_checks_create.assert_called_once_with(
                to=mobile_phone, code=code
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(
            patient.tools_to_go_status, Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
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
        patient = self.create_patient(
            user__mobile_phone=mobile_phone,
            tools_to_go_status=Patient.TOOLS_TO_GO_EMAIL_SENT,
        )
        code = "777777"
        with self.patched_twilio_verification_checks_create() as mock_verification_checks_create:
            mock_verification_checks_create.side_effect = (
                patched_verification_checks_create_code_invalid
            )
            response = self.post_with_creds(self.uri, patient.user, {"code": code})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"][0], VerificationCodeInvalid.error_message,
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
        patient = self.create_patient(
            user__mobile_phone=mobile_phone,
            tools_to_go_status=Patient.TOOLS_TO_GO_EMAIL_SENT,
        )
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
        patient = self.create_patient(
            user__mobile_phone=mobile_phone,
            tools_to_go_status=Patient.TOOLS_TO_GO_EMAIL_SENT,
        )
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

    def test_tools_to_go_status_other_than_not_started_or_finished_forbidden(self):
        """
        If the Patient's tools to go status is something other than "Email
        Sent" or "Phone Number Verified", is `POST`ing to this endpoint forbidden?
        """
        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_NOT_STARTED
        )
        code = "7777777"
        response = self.post_with_creds(self.uri, patient.user, {"code": code})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPatientSetPasswordAPI(UidAndTokenTestMixin, JasprApiTestCase):
    token_generator = JasprToolsToGoUidAndTokenAuthentication.token_generator

    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/set-password"

    def _test_confirmation_email_sent(
        self, request_time: datetime, patient: Patient
    ) -> None:
        """
        If a `Patient` has his/her password changed and status changed from
        "Phone Number Verified" to "Setup Finished" then a confirmation email should
        be sent. This checks for the presence of that email.
        """
        self.assertEqual(len(mail.outbox), 1)
        email_log = EmailLog.objects.get(user_id=patient.user_id, date=request_time)
        self.assertEqual(
            email_log.subject,
            "Congratulations for setting up your Jaspr at Home account",
        )

    def test_can_set_password(self):
        """
        Can an authenticated (and tools to go setup finished) patient set his/her
        password if a valid `set_password_token` (along with authentication `uid` and
        `token`) is provided?
        """
        patient = self.create_tools_to_go_patient(
            user__password_complex=False, user__password_changed=None,
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
            user__password_complex=False, user__password_changed=None,
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
            user__password_complex=False, user__password_changed=None,
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

    def test_can_change_password_and_have_tools_to_go_status_change(self):
        """
        Can an authenticated (and tools to go setup at "Phone Number Verified")
        patient change his/her password and have status change from "Phone Number
        Verified" to "Setup Finished"?
        """

        department = self.create_department()

        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
            user__password_complex=False,
            user__password_changed=None,
        )
        encounter = self.create_patient_encounter(patient=patient, department=department)
        encounter.add_activities([ActivityType.StabilityPlan])

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
                },
            )

        # Still check everything even though we also checked it in another test. The
        # reason is that we want to make sure we're still saving both the patient
        # and the user in the serializer after updating relevant data. The code takes
        # two separate paths so we'll keep these tests here also.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data)
        patient.user.refresh_from_db()
        patient.refresh_from_db()
        self.assertEqual(patient.tools_to_go_status, Patient.TOOLS_TO_GO_SETUP_FINISHED)
        self.assertTrue(patient.user.check_password(new_password))
        self.assertEqual(patient.user.password_changed, now)
        self.assertTrue(patient.user.password_complex)
        self._test_confirmation_email_sent(now, patient)

    def test_jah_account_creation(self):
        """
        Does a patients JAH account get created when setting their JAH password for the first time?
        """
        department = self.create_department()

        patient = self.create_patient(
            tools_to_go_status=Patient.TOOLS_TO_GO_PHONE_NUMBER_VERIFIED,
            user__password_complex=False,
            user__password_changed=None,
        )
        encounter = self.create_patient_encounter(patient=patient, department=department)
        encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])

        distract_category = self.create_coping_strategy_category(
            name="Do things to distract yourself.", slug="distract"
        )

        distract_coping_strategy = self.create_kiosk_patient_coping_strategy(
            encounter=encounter,
            category=distract_category,
            title="distract coping strategy",
            status="active",
        )

        stability_plan = encounter.get_activity(ActivityType.StabilityPlan)
        encounter.save_answers({"coping_distract": [
            distract_coping_strategy.title,
        ]})
        new_password = "TheGoose87623##"
        set_password_token = self.valid_token_for(
            patient.user, token_generator=JasprSetPasswordTokenGenerator
        )

        response = self.post_with_creds(
            self.uri,
            patient.user,
            data={
                "password": new_password,
                "set_password_token": set_password_token,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        patient.user.refresh_from_db()
        patient.refresh_from_db()
        self.assertEqual(patient.tools_to_go_status, Patient.TOOLS_TO_GO_SETUP_FINISHED)
        jah_coping_strategies = JAHPatientCopingStrategy.objects.all()
        ## TODO FIX BEFORE RELEASE
        self.assertEqual(jah_coping_strategies.count(), 1)
        self.assertEqual(distract_coping_strategy.title, jah_coping_strategies.first().title)


    def test_requires_tools_to_go_phonenumber_verified(self):
        """
        This is partially a test to make sure that
        `HasToolsToGoAtLeastPhoneNumberVerified` is working properly. You shouldn't
        be able to change your Jaspr account info until you're at the "Phone Number
        Verified" tools to go status.
        """
        patient = self.create_patient(tools_to_go_status=Patient.TOOLS_TO_GO_EMAIL_SENT)
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

    def test_user_type_other_than_patient_forbidden(self):
        """
        Since the authentication/permissions here are different/unusual compared to
        other types of authentication/permissions, it was difficult to use the
        standard permissions testing framework here. Hence we add one test to make
        sure that a `Technician`, even if authenticated successfully with a valid
        `set_password_token`, hits a `403` forbidden response code.
        """
        technician = self.create_technician(
            user__password_complex=False, user__password_changed=None,
        )
        self.set_technician_creds(technician)
        new_password = "TheGoose87623##"
        set_password_token = self.valid_token_for(
            technician.user, token_generator=JasprSetPasswordTokenGenerator
        )
        response = self.post_with_creds(
            self.uri,
            technician.user,
            data={"password": new_password, "set_password_token": set_password_token},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
