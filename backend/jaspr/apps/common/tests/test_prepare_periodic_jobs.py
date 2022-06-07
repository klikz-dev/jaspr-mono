from datetime import datetime, timedelta
from io import StringIO
from typing import Counter, Tuple, Type, Union

import django_rq
from django.core.management import call_command
from django.utils import timezone
from django.utils.functional import cached_property
from jaspr.apps.common.functions import sort_dict
from jaspr.apps.test_infrastructure.testcases import JasprRedisTestCase
from rq_scheduler import Scheduler
from scheduler.models import (
    BaseJob,
    CronJob,
    JobArg,
    JobKwarg,
    RepeatableJob,
    ScheduledJob,
)


def callable_for_test(
    key: str, arg: int, *, kwarg1: Union[int, str, bool], kwarg2: str = "default-value"
) -> Tuple[str, str]:
    """
    NOTE: At the time of writing, not currently doing anything or making assertions
    on this callable, but could do something with it in the future.

    RQ scheduled jobs do require a callable with args and kwargs though and this is
    the expected callable to use for these tests. More tests could be written against
    it in the future too.
    """
    value = f"{arg}, kwarg1={kwarg1}, kwarg2={kwarg2}"
    return key, value


class TestPreparePeriodicJobs(JasprRedisTestCase):
    def call_command_and_get_output(self, delete_if_no_match: bool) -> str:
        output = StringIO()
        call_command(
            "prepare_periodic_jobs",
            delete_if_no_match=delete_if_no_match,
            stdout=output,
        )
        return output.getvalue()

    @cached_property
    def callable_str(self) -> str:
        qualname = callable_for_test.__qualname__
        full_path_str = (
            "jaspr.apps.common.tests.test_prepare_periodic_jobs.callable_for_test"
        )
        self.assertTrue(full_path_str.endswith(qualname), "In case this ever changes.")
        return full_path_str

    @cached_property
    def low_scheduler(self) -> Scheduler:
        return django_rq.get_scheduler("low")

    @cached_property
    def default_scheduler(self) -> Scheduler:
        return django_rq.get_scheduler()

    @cached_property
    def high_scheduler(self) -> Scheduler:
        return django_rq.get_scheduler("high")

    @cached_property
    def relaxed_now(self) -> datetime:
        return timezone.now()

    @staticmethod
    def get_arg_type_and_value(
        value: Union[int, str, bool]
    ) -> Tuple[str, Union[int, str, bool]]:
        if isinstance(value, bool):
            return "bool_val", value
        elif isinstance(value, int):
            return "int_val", value
        else:
            return "str_val", value

    def create_job(
        self, job_type: Type[Union[CronJob, RepeatableJob, ScheduledJob]], **kwargs
    ) -> Union[CronJob, RepeatableJob, ScheduledJob]:
        callable_args = kwargs.pop("args", kwargs.pop("callable_args", ()))
        callable_kwargs = kwargs.pop("kwargs", kwargs.pop("callable_kwargs", {}))
        kwargs.setdefault("callable", self.callable_str)
        kwargs.setdefault("queue", "default")
        job = job_type.objects.create(**kwargs)
        self.add_args_and_kwargs_to_job(job, *callable_args, **callable_kwargs)
        # NOTE: Currently, any save on `JobArg` or `JobKwarg` automatically saves the
        # `content_object` so we don't need an extra `save()` on the `job` right now.
        return job

    def create_cron_job(self, **kwargs) -> CronJob:
        kwargs.setdefault("cron_string", "0 1 * * *")
        return self.create_job(CronJob, **kwargs)

    def create_repeatable_job(self, **kwargs) -> RepeatableJob:
        kwargs.setdefault("scheduled_time", self.relaxed_now + timedelta(hours=2))
        kwargs.setdefault("interval_unit", "hours")
        kwargs.setdefault("interval", 2)
        return self.create_job(RepeatableJob, **kwargs)

    def create_scheduled_job(self, **kwargs) -> ScheduledJob:
        kwargs.setdefault("scheduled_time", self.relaxed_now + timedelta(hours=1))
        return self.create_job(ScheduledJob, **kwargs)

    def add_args_and_kwargs_to_job(self, job: BaseJob, *args, **kwargs) -> None:
        for arg in args:
            arg_type, val = self.get_arg_type_and_value(arg)
            JobArg.objects.create(
                content_object=job, arg_type=arg_type, **{arg_type: val}
            )
        for key, value in kwargs.items():
            arg_type, val = self.get_arg_type_and_value(value)
            JobKwarg.objects.create(
                content_object=job, key=key, arg_type=arg_type, **{arg_type: val}
            )

    def setup_cron_jobs_landscape(self):
        """
        - 3 enabled (with 2 that are not in Redis)
        - 2 disabled (with 1 that's still in Redis)
        - 3 deleted (with 2 that are still in Redis)
        """
        self.enabled_cron_job1 = self.create_cron_job(
            name="Cron Enabled 1",
            # NOTE: "tppj" is shorthand for "test prepare periodic jobs".
            args=("tppj:cron-enabled-1", 1),
            kwargs={"kwarg1": 0},
        )
        self.enabled_cron_job2 = self.create_cron_job(
            name="Cron Enabled 2",
            args=("tppj:cron-enabled-2", 2),
            kwargs={"kwarg1": False, "kwarg2": "ce2"},
        )
        self.enabled_cron_job3 = self.create_cron_job(
            name="Cron Enabled 3",
            args=("tppj:cron-enabled-3", 3),
            kwargs={"kwarg1": "c3", "kwarg2": "ce3"},
        )
        # Unscheduling does not save/persist to the database currently so we're fine
        # doing this.
        [
            job_instance.unschedule()
            for job_instance in self.enabled_cron_job2.__class__.objects.filter(
                pk__in=[self.enabled_cron_job2.pk, self.enabled_cron_job3.pk]
            )
        ]

        self.disabled_cron_job1 = self.create_cron_job(
            name="Cron Disabled 1",
            args=("tppj:cron-disabled-1", 4),
            kwargs={"kwarg1": 1},
        )
        self.disabled_cron_job1.__class__.objects.filter(
            pk=self.disabled_cron_job1.pk
        ).update(enabled=False, job_id=None)
        self.disabled_cron_job2 = self.create_cron_job(
            name="Cron Disabled 2",
            args=("tppj:cron-disabled-2", 5),
            kwargs={"kwarg1": 55555, "kwarg2": "cd2"},
            enabled=False,
        )

        self.deleted_cron_job1 = self.create_cron_job(
            name="Cron Deleted 1",
            args=("tppj:cron-deleted-2", 6),
            kwargs={"kwarg1": True, "kwarg2": "cdl1"},
        )
        self.deleted_cron_job2 = self.create_cron_job(
            name="Cron Deleted 2",
            args=("tppj:cron-deleted-2", 7),
            kwargs={"kwarg1": "duck", "kwarg2": "cdl2"},
        )
        self.deleted_cron_job2.delete()
        self.deleted_cron_job3 = self.create_cron_job(
            name="Cron Deleted 3",
            args=("tppj:cron-deleted-3", 8),
            kwargs={"kwarg1": False, "kwarg2": "cdl3"},
        )
        self.deleted_cron_job1.__class__.objects.filter(
            pk__in=[self.deleted_cron_job1.pk, self.deleted_cron_job3.pk]
        ).delete()

    def setup_repeatable_jobs_landscape(self):
        """
        - 2 enabled (with 1 that's not in Redis)
        - 3 disabled (with 2 that are still in Redis)
        - 2 deleted (with 1 that's still in Redis)
        """
        self.enabled_repeatable_job1 = self.create_repeatable_job(
            name="Repeatable Enabled 1",
            args=("tppj:repeatable-enabled-1", 11),
            kwargs={"kwarg1": 1},
        )
        self.enabled_repeatable_job2 = self.create_repeatable_job(
            name="Repeatable Enabled 2",
            args=("tppj:repeatable-enabled-2", 12),
            kwargs={"kwarg1": False, "kwarg2": "re2"},
        )
        self.enabled_repeatable_job2.__class__.objects.filter(
            pk=self.enabled_repeatable_job2.pk
        ).get().unschedule()

        self.disabled_repeatable_job1 = self.create_repeatable_job(
            name="Repeatable Disabled 1",
            args=("tppj:repeatable-disabled-1", 13),
            kwargs={"kwarg1": 1},
        )
        self.disabled_repeatable_job1.enabled = False
        self.disabled_repeatable_job1.save()
        self.disabled_repeatable_job2 = self.create_repeatable_job(
            name="Repeatable Disabled 2",
            args=("tppj:repeatable-disabled-2", 14),
            kwargs={"kwarg1": True, "kwarg2": "rd2"},
        )
        self.disabled_repeatable_job3 = self.create_repeatable_job(
            name="Repeatable Disabled 3",
            args=("tppj:repeatable-disabled-3", 15),
            kwargs={"kwarg1": "r3", "kwarg2": "rd3"},
        )
        self.disabled_repeatable_job3.__class__.objects.filter(
            pk__in=[self.disabled_repeatable_job2.pk, self.disabled_repeatable_job3.pk]
        ).update(enabled=False)
        self.disabled_repeatable_job3.__class__.objects.filter(
            pk=self.disabled_repeatable_job3.pk
        ).update(job_id=None)

        self.deleted_repeatable_job1 = self.create_repeatable_job(
            name="Repeatable Deleted 1",
            args=("tppj:repeatable-deleted-1", 16),
            kwargs={"kwarg1": False, "kwarg2": "rdl1"},
        )
        self.deleted_repeatable_job1.delete()
        self.deleted_repeatable_job2 = self.create_repeatable_job(
            name="Repeatable Deleted 2",
            args=("tppj:repeatable-deleted-2", 17),
            kwargs={"kwarg1": "bunny", "kwarg2": "rdl2"},
        )
        self.deleted_repeatable_job2.__class__.objects.filter(
            pk=self.deleted_repeatable_job2.pk
        ).delete()

    def setup_scheduled_jobs_landscape(self):
        """
        - 1 enabled ~6 hours into the future
        - 1 disabled from ~1 hour in the past
        """
        self.enabled_scheduled_job = self.create_scheduled_job(
            name="Scheduled Enabled 1",
            args=("tppj:scheduled-enabled-1", 22),
            kwargs={"kwarg1": 1},
            scheduled_time=self.relaxed_now + timedelta(hours=6),
        )
        self.disabled_scheduled_job = self.create_scheduled_job(
            name="Scheduled Disabled 1",
            args=("tppj:scheduled-disabled-1", 21),
            kwargs={"kwarg1": "s2", "kwarg2": "s2-override"},
            scheduled_time=self.relaxed_now - timedelta(hours=1),
        )

    def setup_other_landscape(self):
        """
        - 2 scheduled jobs in Redis with matching prefixes but not exactly matching
        the cron/scheduled regexes.
        - 1 other scheduled job without a matching prefix.
        """
        self.low_scheduler.enqueue_in(
            timedelta(hours=1),
            callable_for_test,
            kwarg1="soon",
            job_id="django-rq-scheduler:soon",
        )
        self.default_scheduler.enqueue_in(
            timedelta(days=1),
            callable_for_test,
            kwarg1="later",
            kwarg2="non-default",
            job_id="django-rq-scheduler:later",
        )
        self.high_scheduler.enqueue_at(
            self.relaxed_now + timedelta(minutes=40),
            callable_for_test,
            kwarg1="very-soon",
            job_id="very-soon:not-matching",
        )

    def setup_jobs_landscape(self):
        self.setup_cron_jobs_landscape()
        self.setup_repeatable_jobs_landscape()
        self.setup_scheduled_jobs_landscape()
        self.setup_other_landscape()

    def assert_cron_jobs_consistent(self, output: str, deleted: bool):
        self.assertTrue(self.enabled_cron_job1.is_scheduled())
        self.assertTrue(self.enabled_cron_job2.is_scheduled())
        self.assertTrue(self.enabled_cron_job3.is_scheduled())
        self.assertFalse(self.disabled_cron_job1.is_scheduled())
        self.assertFalse(self.disabled_cron_job2.is_scheduled())
        if deleted:
            self.assertFalse(self.deleted_cron_job1.is_scheduled())
            self.assertFalse(self.deleted_cron_job2.is_scheduled())
            self.assertFalse(self.deleted_cron_job3.is_scheduled())
        else:
            self.assertTrue(self.deleted_cron_job1.is_scheduled())
            self.assertFalse(self.deleted_cron_job2.is_scheduled())
            self.assertTrue(self.deleted_cron_job3.is_scheduled())

    def assert_repeatable_jobs_consistent(self, output: str, deleted: bool):
        self.assertTrue(self.enabled_repeatable_job1.is_scheduled())
        self.assertTrue(self.enabled_repeatable_job2.is_scheduled())
        self.assertFalse(self.disabled_repeatable_job1.is_scheduled())
        self.assertFalse(self.disabled_repeatable_job2.is_scheduled())
        self.assertFalse(self.disabled_repeatable_job3.is_scheduled())
        if deleted:
            self.assertFalse(self.deleted_repeatable_job1.is_scheduled())
            self.assertFalse(self.deleted_repeatable_job2.is_scheduled())
        else:
            self.assertFalse(self.deleted_repeatable_job1.is_scheduled())
            self.assertTrue(self.deleted_repeatable_job2.is_scheduled())

    def assert_scheduled_jobs_consistent(self):
        self.enabled_scheduled_job.refresh_from_db()
        self.assertTrue(self.enabled_scheduled_job.is_scheduled)
        self.disabled_scheduled_job.refresh_from_db()
        self.assertTrue(self.disabled_scheduled_job.is_scheduled)

    def test_no_models_or_jobs(self):
        non_delete_output = self.call_command_and_get_output(False)
        self.assertIn(
            f"All done with initial scheduling and unscheduling! Result: {dict()}",
            non_delete_output,
        )
        self.assertIn(
            f"All done with rqscheduler job sweep! Result: {dict()}", non_delete_output,
        )

        delete_output = self.call_command_and_get_output(True)
        self.assertIn(
            f"All done with initial scheduling and unscheduling! Result: {dict()}",
            delete_output,
        )
        self.assertIn(
            f"All done with rqscheduler job sweep! Result: {dict()}", delete_output,
        )

    def test_landscape_with_delete_if_no_match_false(self):
        self.setup_jobs_landscape()
        output = self.call_command_and_get_output(delete_if_no_match=False)

        expected_instance_counts = Counter(
            cron_job_enabled=3,
            cron_job_not_enabled=2,
            repeatable_job_enabled=2,
            repeatable_job_not_enabled=3,
        )
        expected_job_counts = Counter(
            cron_match_and_found=3,
            cron_match_and_not_found=2,
            repeatable_match_and_found=2,
            repeatable_match_and_not_found=1,
            start_but_no_full_match=2,
            not_processed=4,
        )
        self.assertIn(
            f"All done with initial scheduling and unscheduling! Result: {sort_dict(expected_instance_counts)}",
            output,
        )
        self.assertIn(
            f"All done with rqscheduler job sweep! Result: {sort_dict(expected_job_counts)}",
            output,
        )
        self.assert_cron_jobs_consistent(output, False)
        self.assert_repeatable_jobs_consistent(output, False)
        self.assert_scheduled_jobs_consistent()

    def test_landscape_with_delete_if_no_match_true(self):
        self.setup_jobs_landscape()
        output = self.call_command_and_get_output(delete_if_no_match=True)

        expected_instance_counts = Counter(
            cron_job_enabled=3,
            cron_job_not_enabled=2,
            repeatable_job_enabled=2,
            repeatable_job_not_enabled=3,
        )
        expected_job_counts = Counter(
            cron_match_and_found=3,
            cron_match_and_not_found=2,
            repeatable_match_and_found=2,
            repeatable_match_and_not_found=1,
            start_but_no_full_match=2,
            not_processed=4,
        )
        self.assertIn(
            f"All done with initial scheduling and unscheduling! Result: {sort_dict(expected_instance_counts)}",
            output,
        )
        self.assertIn(
            f"All done with rqscheduler job sweep! Result: {sort_dict(expected_job_counts)}",
            output,
        )
        self.assert_cron_jobs_consistent(output, True)
        self.assert_repeatable_jobs_consistent(output, True)
        self.assert_scheduled_jobs_consistent()
