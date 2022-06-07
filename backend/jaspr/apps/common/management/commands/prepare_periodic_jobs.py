import re
from itertools import chain
from typing import Counter, Dict, Literal, Optional, Set, Type

import django_rq
from django.core.management.base import CommandParser
from django.utils.encoding import smart_str
from jaspr.apps.common.functions import sort_dict
from jaspr.apps.common.jobs.rq import cleanup_all_rq_data
from jaspr.apps.common.management.base import JasprBaseCommand
from scheduler.models import (
    FIXED_JOB_ID_MAPPING,
    RQ_SCHEDULER_INTERVAL,
    BaseJob,
    CronJob,
    RepeatableJob,
)


class Command(JasprBaseCommand):
    """
    Prepare jobs that will be executed in the background by `rqworker`. The
    `rqscheduler` process will periodically poll scheduled jobs and put them into the
    specified queue when it's their time to run and an `rqworker` process can/will
    pick the job up and run it.
    """

    # Use the docstring defined above as `help` for the management command.
    help = __doc__

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-d",
            "--delete_if_no_match",
            action="store_true",
            help=(
                "If redis scheduled job references are found to other `CronJob`s or "
                "`RepeatableJob`s with primary keys that aren't found in the existing "
                "`QuerySet`s, should those scheduled jobs be deleted?"
            ),
        )

    def handle(self, *app_labels, **options) -> None:
        delete_if_no_match = options["delete_if_no_match"]
        counts = Counter()
        pk_strings: Dict[Type[BaseJob], Set[str]] = {
            CronJob: set(),
            RepeatableJob: set(),
        }

        for job_instance in chain(
            CronJob.objects.all().iterator(), RepeatableJob.objects.all().iterator()
        ):
            assert job_instance.pk is not None and isinstance(job_instance.pk, int)
            pk_strings[job_instance.__class__].add(str(job_instance.pk))
            verbose_name = smart_str(job_instance._meta.verbose_name)
            underscore_name = verbose_name.replace(" ", "_").casefold()
            job_name = job_instance.name
            if job_instance.enabled:
                counts[f"{underscore_name}_enabled"] += 1
                # NOTE: Currently `save()` calls `unschedule()` under the hood. If that
                # ever changed, we'd want to manually call `unschedule()` ourselves
                # since, from fixtures, certain fields may have changed and we'd want
                # the most fresh version to get scheduled properly (with the old
                # version unscheduled).
                job_instance.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{job_name} ({verbose_name}) (pk={job_instance.pk}): "
                        "Scheduled (Saved) (Was Enabled)"
                    )
                )
            else:
                counts[f"{underscore_name}_not_enabled"] += 1
                # NOTE: `unschedule()` will set `job_id` to `None`, so we make sure to
                # set the fixed id before to make sure it gets unscheduled if it was
                # there already.
                job_instance.job_id = job_instance.get_fixed_id()
                job_instance.unschedule()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{job_name} ({verbose_name}) (pk={job_instance.pk}): "
                        "Unscheduled (Was Not Enabled)"
                    )
                )
        self.stdout.write(
            self.style.SUCCESS(
                "\nAll done with initial scheduling and unscheduling! Result: "
                f"{dict(sort_dict(counts))}.\n\n"
            )
        )

        shared_start_str = "django-rq-scheduler:"
        # NOTE: If anything in `FIXED_JOB_ID_MAPPING` changes, this assertion should
        # break and tests should break. It's critical to have what we expect here.
        assert FIXED_JOB_ID_MAPPING[CronJob] == "django-rq-scheduler:cron-job:{pk}"
        cron_id_regex = re.compile(r"^django-rq-scheduler:cron-job:([0-9]+)$")
        assert (
            FIXED_JOB_ID_MAPPING[RepeatableJob]
            == "django-rq-scheduler:repeatable-job:{pk}"
        )
        repeatable_id_regex = re.compile(
            r"^django-rq-scheduler:repeatable-job:([0-9]+)$"
        )

        # NOTE/TODO: Due to changes made in our fork of `django_rq_scheduler` (starting with
        # https://github.com/MicahLyle/django-rq-scheduler/commit/2fa10a5aecdbcbbc2ac0754cf3bf6cadb2fdbbdf),
        # and the implementation here, we should be relatively safe regarding potential
        # mismatches in `job_id`s when dumping and loading fixtures (I.E. overwriting
        # an old job id that was sitting in Redis and then getting duplicate scheduled
        # jobs sitting there). There is room for improvement, and if anything comes up
        # this can definitely be modified.
        job_counts = Counter()
        cron_pk_strings = pk_strings[CronJob]
        repeatable_pk_strings = pk_strings[RepeatableJob]
        num_searched: int = 0
        # We can just use the "default" queue because we're not enqueueing any tasks,
        # just canceling (which shouldn't matter regarding high/default/low).
        scheduler = django_rq.get_scheduler("default", interval=RQ_SCHEDULER_INTERVAL)
        for job in scheduler.get_jobs():
            num_searched += 1
            job_id = str(job.id)
            match_and_not_found: bool = False
            match_type: Optional[Literal["cron", "repeatable"]] = None
            if job_id.startswith(shared_start_str):
                if cron_match := cron_id_regex.match(job_id):
                    match_type = "cron"
                    pk_string = cron_match.group(1)
                    if pk_string in cron_pk_strings:
                        job_counts["cron_match_and_found"] += 1
                    else:
                        job_counts["cron_match_and_not_found"] += 1
                        match_and_not_found = True
                elif repeatable_match := repeatable_id_regex.match(job_id):
                    match_type = "repeatable"
                    pk_string = repeatable_match.group(1)
                    if pk_string in repeatable_pk_strings:
                        job_counts["repeatable_match_and_found"] += 1
                    else:
                        job_counts["repeatable_match_and_not_found"] += 1
                        match_and_not_found = True
                else:
                    job_counts["start_but_no_full_match"] += 1
                    job_counts["not_processed"] += 1
                    continue
            else:
                job_counts["not_processed"] += 1
                continue
            if match_and_not_found:
                if delete_if_no_match:
                    scheduler.cancel(job)
                    self.stdout.write(
                        self.style.NOTICE(f"Canceled {match_type} job {job_id}.")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"{match_type.title()} Job {job_id} found but not canceled."
                        )
                    )
            else:
                self.stdout.write(f"Found {match_type} {job_id}.")
        self.stdout.write(
            self.style.SUCCESS(
                "\nAll done with rqscheduler job sweep! Result: "
                f"{dict(sort_dict(job_counts))}."
            )
        )
