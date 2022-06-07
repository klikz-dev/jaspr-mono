import importlib
import re
import unittest
from contextlib import contextmanager
from typing import Any, Callable, Union

import django_rq
from django.conf import settings
from django.test.testcases import SerializeMixin

from jaspr.apps.common.jobs.rq import (
    cleanup_all_rq_data,
    default_failure_ttl,
    default_result_ttl,
)


class RedisTestCaseMixin(SerializeMixin):
    """
    This mixin should be used if any part of job/redis dependent
    code executes asynchronously, or if rq-scheduler is used
    at all in any part of a test class.

    Provides a method used with `tearDown` by default, called
    `clear_scheduler_and_worker_queues`, that removes any
    existing queued jobs or scheduled jobs that haven't
    been executed or pulled off the scheduler (essentially it
    just wipes the slate for django-rq and rq-scheduler).
    If you don't want it to be used in tearDown, set
    `redis_handle_teardown_manually` to `True`.

    NOTE: Make sure to inherit this correctly so that `tearDown`
    is called (I.E. put this Mixin left of something like TestCase).
    """

    # NOTE: Trying this out to allow parallel tests to not fail. Could also
    # consider acquiring a redis lock for up to 15-30 seconds (and making sure it's
    # removed on tear down, using something that handles even exceptions, etc. (and/or
    # a `try ... finally block`)) (Updated NOTE: This is working solid at the time of
    # writing).
    lockfile = __file__

    handle_redis_teardown_automatically = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # NOTE: With local environments, if a test fails because someone is in the
        # process of writing/debugging it, it's possible Redis teardown may not occur.
        # To avoid those spurious and non-code related errors, we do an extra flush of
        # the queues at the start of each `RedisTestCaseMixin` when testing locally.
        # Shouldn't be needed in CI environments since it will be a fresh Redis
        # everytime anyway.
        if settings.ENVIRONMENT == "local":
            cls.clear_scheduler_and_worker_queues()

    def tearDown(self):
        if self.handle_redis_teardown_automatically:
            self.clear_scheduler_and_worker_queues()
        super().tearDown()

    @staticmethod
    def clear_scheduler_and_worker_queues():
        cleanup_all_rq_data()

    # NOTE: This is a context manager meant to be used like this:
    # `with self.rq_jobs_async(True):`
    # (Perform some code while jobs have to be run by workers)
    # NOTE: WARNING: This code is not currently working, falling back to a different strategy for now.
    # NOTE: Might be helpful to file a ticket in the django-rq GitHub and/or search the issue history
    # to find out how to make this work (and make testing work) with FakeRedis, and work correctly
    # in general.
    # Ticket filed: https://github.com/rq/django-rq/issues/317
    @contextmanager
    def rq_jobs_async(self, yes_or_no: bool):
        """
        If `yes_or_no` is `True`, jobs execute asynchronously and need to be run by workers.
        If `yes_or_no` is `False`, jobs execute synchronously and don't need to be run by workers.
        """
        QUEUES = django_rq.settings.QUEUES
        originals = {}
        # https://github.com/rq/django-rq#synchronous-mode
        for name, queue_config in settings.RQ_QUEUES.items():
            # NOTE: We change both the settings and `queue`. Realistically,
            # you only need to change `queue` since the settings are only
            # used in the beginning to set `_is_async` on the queue.
            # However, keeping the settings here in case that ever changes in the
            # future and/or other code accesses the settings for whatever reason.
            originals[name] = queue_config["ASYNC"]
            queue_config["ASYNC"] = yes_or_no
            QUEUES[name]["ASYNC"] = yes_or_no
            queue = django_rq.get_queue(name)
            queue._is_async = yes_or_no
        try:
            yield
        finally:
            # Restore the `RQ_QUEUES` 'ASYNC' values to their originals,
            # the 'QUEUES' 'ASYNC' values to their originals, and
            # the `_is_async` property of each `queue` to its original.
            for name, queue_config in settings.RQ_QUEUES.items():
                queue_config["ASYNC"] = originals[name]
                QUEUES[name]["ASYNC"] = originals[name]
                queue = django_rq.get_queue(name)
                queue._is_async = originals[name]

    # NOTE: Only handles top level functions and classes right now.
    @contextmanager
    def patch_delay_of(
        self, to_patch: Union[str, Callable[..., Any]], run_async: bool = True
    ):
        if isinstance(to_patch, str):
            module_name = re.sub(r"\.[^\.]*$", "", to_patch)
            module_attribute_name = re.search(r"\.([^\.]*)$", to_patch).group(1)
            module = importlib.import_module(module_name)
            original_function = getattr(module, module_attribute_name).delay
            to_patch = f"{to_patch}.delay"
        else:
            to_patch = f"{to_patch.__module__}.{to_patch.__qualname__}.delay"
            original_function = to_patch

        def patched_delay(*args, **kwargs):
            # NOTE: Does not pass any other arguments, so you only get defaults right now.
            # If this is not desired, might have to test some other way.
            queue = django_rq.get_queue(is_async=run_async)
            kwargs.setdefault("result_ttl", default_result_ttl())
            kwargs.setdefault("failure_ttl", default_failure_ttl())
            queue.enqueue(original_function, *args, **kwargs)

        with unittest.mock.patch(to_patch, patched_delay):
            yield
