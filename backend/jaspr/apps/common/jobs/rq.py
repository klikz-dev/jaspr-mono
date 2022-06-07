"""
rq.py: Helpful functions for manually enqueueing/scheduling jobs
(especially if they're not decorated with the @job decorator)
"""
import logging
from datetime import datetime, timedelta
from typing import Any, Callable

import django_rq
import pytz
from django.conf import settings
from django.utils import timezone
from django_rq.jobs import Job
from django_rq.queues import Queue

logger = logging.getLogger(__name__)


def default_result_ttl() -> int:
    RQ = getattr(settings, "RQ", {})
    # If the default isn't set, we'll use five minutes.
    return RQ.get("DEFAULT_RESULT_TTL") or 300


def default_failure_ttl() -> int:
    RQ = getattr(settings, "RQ", {})
    # If the default isn't set, we'll use seven days.
    return RQ.get("DEFAULT_FAILURE_TTL") or (60 * 60 * 24 * 7)


def enqueue(fn: Callable[..., Any], *args, queue_name="default", **kwargs) -> Job:
    kwargs.setdefault("result_ttl", default_result_ttl())
    kwargs.setdefault("failure_ttl", default_failure_ttl())
    return django_rq.get_queue(name=queue_name).enqueue(fn, *args, **kwargs)


def enqueue_at(
    time: datetime,
    fn: Callable[..., Any],
    *args,
    scheduler_name: str = "default",
    **kwargs,
) -> Job:
    scheduler = django_rq.get_scheduler(name=scheduler_name)
    kwargs.setdefault("job_result_ttl", default_result_ttl())
    return scheduler.enqueue_at(time, fn, *args, **kwargs)


def enqueue_in(
    delta: timedelta,
    fn: Callable[..., Any],
    *args,
    scheduler_name: str = "default",
    **kwargs,
) -> Job:
    scheduler = django_rq.get_scheduler(name=scheduler_name)
    kwargs.setdefault("job_result_ttl", default_result_ttl())
    return scheduler.enqueue_in(delta, fn, *args, **kwargs)


@django_rq.job  # Don't have to use it as a job, but here in case we want/need it.
def cleanup_failed_jobs(
    high_delta: timedelta = timedelta(days=1),
    default_delta: timedelta = timedelta(days=1),
    low_delta: timedelta = timedelta(days=1),
    log_regular: Callable[[str], Any] = logger.info,
    log_success: Callable[[str], Any] = logger.info,
) -> int:
    """
    Delete jobs from the failed job registry for each queue that are older than
    `{queue_name}_delta` (specified by the keyword arguments). Return the number of
    jobs successfully deleted.
    """
    time_now = timezone.now()
    deltas_string = f"high = {high_delta}, default = {default_delta}, low = {low_delta}"
    log_regular(
        f"Preparing to delete failed jobs at {time_now} with specified deltas: {deltas_string}."
    )
    deleted_jobs_count = 0
    for name in ("high", "default", "low"):
        delta = locals()[f"{name}_delta"]
        queue = django_rq.get_queue(name)
        failed_registry = queue.failed_job_registry
        for job in Job.fetch_many(
            failed_registry.get_job_ids(), connection=failed_registry.connection
        ):
            if job is None:
                continue
            # If for whatever reason any of these are `None`, use earlier time values
            # as the `end_time` here.
            end_time = job.ended_at or job.started_at or job.enqueued_at
            if time_now - timezone.make_aware(end_time, timezone=pytz.UTC) > delta:
                failed_registry.remove(job, delete_job=True)
                deleted_jobs_count += 1
    log_success(f"{deleted_jobs_count} failed jobs deleted.")
    return deleted_jobs_count


def cleanup_all_rq_data() -> None:
    """
    Delete jobs, results, and whatever else from all queues.

    NOTE/TODO: Some of the code below is probably redundant. Could be cleaned up when
    doing a deeper dive on `django_rq` and/or wanting to optimize test teardown
    speed. All that being said though, at least at the moment, it's not essential
    that this be fast/optimal. I wanted to write the code quick as it wasn't a
    priority at the time.
    """
    queues = [
        django_rq.get_queue(queue_name) for queue_name in ("high", "default", "low")
    ]
    for queue in queues:
        queue.empty()

        for registry in (
            queue.scheduled_job_registry,
            queue.started_job_registry,
            queue.deferred_job_registry,
            queue.finished_job_registry,
            queue.failed_job_registry,
        ):
            for job_id in registry.get_job_ids():
                registry.remove(job_id, delete_job=True)

        scheduler = django_rq.get_scheduler(queue=queue)
        for job in scheduler.get_jobs():
            # Doing it a whole bunch of ways just to make sure. Probably only need to
            # do it one of these ways.
            scheduler.cancel(job)
            job.cancel()
            job.delete()

        while True:
            job = Queue.dequeue_any([queue], None, connection=queue.connection)
            if not job:
                break
            job.delete()
