import sys
import unittest
from datetime import datetime, timedelta
from typing import Optional
from unittest.mock import MagicMock, call, patch

import django_rq
import pytz
from django.core import mail
from django.template.exceptions import TemplateDoesNotExist
from django_rq import get_worker
from freezegun import freeze_time

from jaspr.apps.common.jobs.messaging import message_user_from_template, text_user
from jaspr.apps.message_logs.models import EmailLog, SMSLog
from jaspr.apps.test_infrastructure.mixins.common_mixins import (
    TwilioClientTestCaseMixin,
)
from jaspr.apps.test_infrastructure.testcases import JasprRedisTestCase


# NOTE: Not using some arguments here; just copying the exact
# signature of `render_to_string`.
def patched_render_to_string(template_name, context=None, request=None, using=None):
    if context is None:
        context = {}
    context_string = ", ".join(f"{key}: {value}" for key, value in context.items())
    return f"{template_name} + {context_string}"


def patched_render_to_string_no_title(
    template_name, context=None, request=None, using=None
):
    if template_name.endswith("_sms_title.txt"):
        raise TemplateDoesNotExist("No SMS Title", backend=MagicMock())
    return patched_render_to_string(
        template_name, context=context, request=request, using=using
    )


def patched_noop(*args, **kwargs):
    pass


class MessagingTest(JasprRedisTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_user(preferred_message_type="email")
        # Could also use a class decorator to make
        # available as an argument to all the `test_` methods.
        # However, we perform repetitive setup on top of the mock,
        # so I think it's better to do it here.
        # See: https://docs.python.org/3/library/unittest.mock-examples.html#applying-the-same-patch-to-every-test-method
        mock_render_to_string_patcher = patch(
            "jaspr.apps.common.jobs.messaging.render_to_string", autospec=True
        )
        # Safer than putting in `tearDown` in case there's an exception later in `setUp`.
        self.addCleanup(mock_render_to_string_patcher.stop)
        self.mock_render_to_string = mock_render_to_string_patcher.start()
        self.mock_render_to_string.side_effect = patched_render_to_string


class EmailMessagingTest(MessagingTest):
    def test_template_rendering(self):
        base = "directory/base_filename"
        context = {"sugar": "rush"}
        message_user_from_template(self.user, base, context=context)
        subject_call = call(f"{base}_email_subject.txt", context=context)
        txt_call = call(f"{base}_email.txt", context=context)
        html_call = call(f"{base}_email.html", context=context)
        expected_calls = [subject_call, txt_call, html_call]
        self.assertEqual(self.mock_render_to_string.call_args_list, expected_calls)

    def test_email_sent(self):
        message_user_from_template(self.user, "d/bf", {"yip": "ee"})
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("d/bf_email_subject.txt + yip: ee", mail.outbox[0].subject)
        self.assertIn("d/bf_email.txt + yip: ee", mail.outbox[0].body)
        self.assertIn("d/bf_email.html + yip: ee", mail.outbox[0].alternatives[0][0])

    def test_email_log_created(self):
        frozen_time = datetime(2018, 1, 16, 12, 12, 12, 0, tzinfo=pytz.UTC)
        with freeze_time(frozen_time):
            # 'd/bf' is shorthand for 'directory/base_filename',
            # in case you were wondering what that stands for.
            message_user_from_template(self.user, "d/bf")
        email_log = EmailLog.objects.latest()
        self.assertEqual(email_log.user, self.user)
        self.assertEqual(email_log.user_email, self.user.email)
        self.assertEqual(email_log.date, frozen_time)
        # The subject gets stripped and put into one line, so no space after the '+'.
        self.assertEqual(email_log.subject, "d/bf_email_subject.txt +")
        self.assertEqual(email_log.text_body, "d/bf_email.txt + ")
        self.assertEqual(email_log.html_body, "d/bf_email.html + MEDIA_URL: /media/")
        # In this case, we assume one email is always sent.
        self.assertEqual(email_log.email_response, "1")

    # @unittest.skip(
    #     "Assuming Redis is working properly. Might wait until a better test configuration "
    #     "or for FakeRedis to be used/implemented in tests before unskipping this. Last time "
    #     "running the test it passed though."
    #     "One other note: `patch_delay_of` doesn't carry over `@job` args and kwargs, so it just "
    #     "uses the defaults. That's fine for this test, but there isn't a better solution yet. "
    #     "See https://github.com/rq/django-rq/issues/317 for more information."
    # )
    @unittest.skipIf(
        sys.platform == "win32",
        "'win32' platform does not support `os.fork` required by `rqworker`.",
    )
    def test_email_log_created_from_job(self):
        frozen_time = datetime(2018, 1, 16, 12, 12, 12, 0, tzinfo=pytz.UTC)
        with freeze_time(frozen_time):
            with self.patch_delay_of("jaspr.apps.common.jobs.messaging.email_user"):
                message_user_from_template(self.user, "d/bf")
            get_worker().work(burst=True)
        email_log = EmailLog.objects.latest()
        self.assertEqual(email_log.user, self.user)
        self.assertEqual(email_log.user_email, self.user.email)
        self.assertEqual(email_log.date, frozen_time)
        self.assertEqual(email_log.subject, "d/bf_email_subject.txt +")
        self.assertEqual(email_log.text_body, "d/bf_email.txt + ")
        self.assertEqual(email_log.html_body, "d/bf_email.html + MEDIA_URL: /media/")
        self.assertEqual(email_log.email_response, "1")


class SMSMessagingTest(TwilioClientTestCaseMixin, MessagingTest):
    def setUp(self):
        super().setUp()
        self.user.mobile_phone = "+14155552671"
        self.user.preferred_message_type = "sms"
        self.user.save()

    def test_template_rendering_title_template(self):
        base = "directory/base_filename"
        context = {"sugar": "rush"}
        with patch("jaspr.apps.common.jobs.messaging.text_user.delay", patched_noop):
            message_user_from_template(self.user, base, context=context)
        title_call = call(f"{base}_sms_title.txt", context=context)
        body_call = call(f"{base}_sms.txt", context=context)
        expected_calls = [title_call, body_call]
        self.assertEqual(self.mock_render_to_string.call_args_list, expected_calls)

    def test_template_rendering_no_title_template(self):
        self.mock_render_to_string.side_effect = patched_render_to_string_no_title
        base = "directory/base_filename"
        context = {"sugar": "rush"}
        with patch("jaspr.apps.common.jobs.messaging.text_user.delay", patched_noop):
            message_user_from_template(self.user, base, context=context)
        title_call = call(f"{base}_sms_title.txt", context=context)
        subject_call = call(f"{base}_email_subject.txt", context=context)
        body_call = call(f"{base}_sms.txt", context=context)
        expected_calls = [title_call, subject_call, body_call]
        self.assertEqual(self.mock_render_to_string.call_args_list, expected_calls)

    def test_full_sms_path_from_template(self):
        frozen_time = datetime(2018, 1, 16, 12, 12, 12, 0, tzinfo=pytz.UTC)
        with freeze_time(frozen_time), self.patched_twilio_client_messages_create():
            message_user_from_template(self.user, "d/bf", {"yip": "ee"})
        sms_log = SMSLog.objects.latest()
        self.assertEqual(sms_log.recipient, self.user)
        self.assertEqual(sms_log.mobile_phone, self.user.mobile_phone)
        self.assertEqual(sms_log.title, "d/bf_sms_title.txt + yip: ee")
        self.assertEqual(sms_log.body, "d/bf_sms.txt + yip: ee")
        self.assertEqual(sms_log.message_id, "message-sid-success")
        self.assertEqual(sms_log.status, "sent")
        self.assertEqual(sms_log.sent, frozen_time)
        self.assertEqual(sms_log.times_retried, 0)
        self._test_single_future_job_presence(False, "text_user")

    def test_attribute_error_if_no_phone(self):
        self.user.mobile_phone = ""
        self.user.save()
        with self.assertRaises(AttributeError):
            text_user(self.user.id, "Test Title", "Test Body")

    def test_successful_delivery(self):
        frozen_time = datetime(2018, 1, 16, 12, 12, 12, 0, tzinfo=pytz.UTC)
        with freeze_time(frozen_time), self.patched_twilio_client_messages_create():
            text_user(self.user.id, "Test Title", "Test Body")
        sms_log = SMSLog.objects.latest()
        self.assertEqual(sms_log.recipient, self.user)
        self.assertEqual(sms_log.mobile_phone, self.user.mobile_phone)
        self.assertEqual(sms_log.title, "Test Title")
        self.assertEqual(sms_log.body, "Test Body")
        self.assertEqual(sms_log.message_id, "message-sid-success")
        self.assertEqual(sms_log.status, "sent")
        self.assertEqual(sms_log.sent, frozen_time)
        self.assertEqual(sms_log.times_retried, 0)
        self._test_single_future_job_presence(False, "text_user")

    def _test_twilio_rest_exception(self, status="retry", times_retried=0):
        sms_log = SMSLog.objects.latest()
        self.assertEqual(sms_log.recipient, self.user)
        self.assertEqual(sms_log.mobile_phone, self.user.mobile_phone)
        self.assertEqual(sms_log.title, "Test Title")
        self.assertEqual(sms_log.body, "Test Body")
        self.assertEqual(sms_log.message_id, "")
        self.assertEqual(sms_log.status, status)
        self.assertEqual(sms_log.sent, None)
        self.assertEqual(sms_log.times_retried, times_retried)

    def test_twilio_rest_exception(self):
        with patch(
            "jaspr.apps.common.jobs.messaging.retry_text_user.delay", patched_noop
        ), self.patched_twilio_client_messages_create() as mock_create:
            mock_create.side_effect = self.twilio_rest_exception_instance
            text_user(self.user.id, "Test Title", "Test Body")
        self._test_twilio_rest_exception()

    def _test_single_future_job_presence(
        self,
        expected_present: bool,
        function_name: str,
        expected_time: Optional[datetime] = None,
    ):
        scheduler = django_rq.get_scheduler()
        text_user_filter = (
            lambda job_and_time: job_and_time[0].func.__name__ == function_name
        )
        job_list = list(filter(text_user_filter, scheduler.get_jobs(with_times=True)))
        if expected_present:
            self.assertEqual(len(job_list), 1)
            job, scheduled_time = job_list[0]
            # The scheduled execution times returned by `get_job(with_times=True)` are naive.
            self.assertEqual(scheduled_time, expected_time.replace(tzinfo=None))
            # For convenience, return the job and its scheduled time.
            return job, scheduled_time
        else:
            self.assertEqual(len(job_list), 0)
            return None

    def test_initial_retries_and_scheduled(self):
        frozen_time = datetime(2018, 1, 16, 12, 12, 12, 0, tzinfo=pytz.UTC)
        with freeze_time(
            frozen_time
        ), self.patched_twilio_client_messages_create() as mock_create:
            mock_create.side_effect = self.twilio_rest_exception_instance
            text_user(self.user.id, "Test Title", "Test Body")
            # Initial try, plus three retries
            self.assertEqual(mock_create.call_count, 4)
        self._test_twilio_rest_exception(times_retried=3)
        self._test_single_future_job_presence(
            True, "text_user", frozen_time.replace(tzinfo=None) + timedelta(hours=6)
        )

    def test_last_scheduled_retry_and_after(self):
        sms_log = SMSLog.objects.create(
            recipient=self.user,
            mobile_phone=self.user.mobile_phone,
            title="Test Title",
            body="Test Body",
            status="retry",
            sent=None,
            times_retried=4,
        )
        frozen_time = datetime(2018, 1, 16, 12, 12, 12, 0, tzinfo=pytz.UTC)
        with freeze_time(
            frozen_time
        ), self.patched_twilio_client_messages_create() as mock_create:
            mock_create.side_effect = self.twilio_rest_exception_instance
            text_user(
                self.user.id, "Test Title", "Test Body", existing_sms_log_id=sms_log.id
            )
            # Get the single job back, and then run it (`enqueue_job` calls `run_job` under the hood).
            self._test_twilio_rest_exception(times_retried=5)
            job, _ = self._test_single_future_job_presence(
                True, "text_user", frozen_time.replace(tzinfo=None) + timedelta(hours=6)
            )
            django_rq.get_scheduler().cancel(job)
            django_rq.get_queue().enqueue_job(job)
            self._test_twilio_rest_exception(status="failed", times_retried=6)
            self._test_single_future_job_presence(False, "text_user")


class EmailAndSMSMessagingTest(TwilioClientTestCaseMixin, MessagingTest):
    def setUp(self):
        super().setUp()
        self.user.mobile_phone = "+14155552671"
        self.user.preferred_message_type = "email and sms"
        self.user.save()

    def test_successful_delivery_for_both(self):
        with self.patched_twilio_client_messages_create():
            message_user_from_template(self.user, "d/bf", {"yip": "ee"})
        self.assertTrue(
            EmailLog.objects.filter(
                subject="d/bf_email_subject.txt + yip: ee",
                text_body="d/bf_email.txt + yip: ee",
                html_body="d/bf_email.html + yip: ee, MEDIA_URL: /media/",
            ).exists()
        )
        self.assertTrue(
            SMSLog.objects.filter(
                title="d/bf_sms_title.txt + yip: ee",
                body="d/bf_sms.txt + yip: ee",
                message_id="message-sid-success",
            ).exists()
        )
