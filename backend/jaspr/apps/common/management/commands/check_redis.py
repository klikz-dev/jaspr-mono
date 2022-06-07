from datetime import timedelta
from typing import Any

import django_rq
from django.core import management
from jaspr.apps.common.management.base import JasprBaseCommand


@django_rq.job
def basic_job(basic_arg: Any, basic_kwarg: str = "Test Default Kwarg"):
    print(f"printing `basic_arg`: {basic_arg}")
    print(f"printing `basic_kwarg`: {basic_kwarg}")
    return (basic_arg, basic_kwarg)


class Command(JasprBaseCommand):
    """
    Check that redis integration (rqworker and rqscheduler)
    is working as intended.
    """

    # Use the docstring defined above as `help` for the management command.
    help = __doc__

    def enqueue_non_scheduled_jobs(self, high_queue, default_queue, low_queue):
        high_queue.enqueue(basic_job, "Test")
        high_queue.enqueue(basic_job, "Test", "Test Non Default Kwarg")
        high_queue.enqueue(basic_job, "Test", basic_kwarg="Test Non Default Kwarg")
        default_queue.enqueue(basic_job, "Test")
        default_queue.enqueue(basic_job, "Test", "Test Non Default Kwarg")
        default_queue.enqueue(basic_job, "Test", basic_kwarg="Test Non Default Kwarg")
        basic_job.delay("Test With `@job`")
        low_queue.enqueue(basic_job, "Test")
        low_queue.enqueue(basic_job, "Test", "Test Non Default Kwarg")
        low_queue.enqueue(basic_job, "Test", basic_kwarg="Test Non Default Kwarg")
        self.stdout.write("10 regular jobs just enqueued (3 high, 4 default, 3 low)")

    def enqueue_scheduled_jobs(self, high_queue, default_queue, low_queue):
        high_scheduler = django_rq.get_scheduler("high")
        default_scheduler = django_rq.get_scheduler("default")
        low_scheduler = django_rq.get_scheduler("low")
        high_scheduler.enqueue_in(timedelta(seconds=20), basic_job, "Test")
        high_scheduler.enqueue_in(
            timedelta(seconds=20), basic_job, "Test", "Test Non Default Kwarg"
        )
        high_scheduler.enqueue_in(
            timedelta(seconds=20),
            basic_job,
            "Test",
            basic_kwarg="Test Non Default Kwarg",
        )
        default_scheduler.enqueue_in(timedelta(seconds=20), basic_job, "Test")
        default_scheduler.enqueue_in(
            timedelta(seconds=20), basic_job, "Test", "Test Non Default Kwarg"
        )
        default_scheduler.enqueue_in(
            timedelta(seconds=20),
            basic_job,
            "Test",
            basic_kwarg="Test Non Default Kwarg",
        )
        low_scheduler.enqueue_in(timedelta(seconds=20), basic_job, "Test")
        low_scheduler.enqueue_in(
            timedelta(seconds=20), basic_job, "Test", "Test Non Default Kwarg"
        )
        low_scheduler.enqueue_in(
            timedelta(seconds=20),
            basic_job,
            "Test",
            basic_kwarg="Test Non Default Kwarg",
        )
        self.stdout.write(
            "9 scheduled jobs just enqueued for 20 seconds from now (3 high, 3 default, 3 low)"
        )

    def handle(self, *app_labels, **options):
        self.stdout.write("Calling `rqstats` before running to get pre-stats.")
        management.call_command("rqstats")
        high_queue = django_rq.get_queue("high")
        default_queue = django_rq.get_queue("default")
        low_queue = django_rq.get_queue("low")
        self.enqueue_non_scheduled_jobs(high_queue, default_queue, low_queue)
        self.enqueue_scheduled_jobs(high_queue, default_queue, low_queue)
        self.stdout.write(
            """
            Within the next 2-3 minutes, you should see 19 total completed jobs
            (6 high, 7 default, 6 low). Use `./manage.py rqstats` to check.
            If there are a ton of queued jobs right now it's possible it could take
            longer than 2-3 minutes.
            """
        )
