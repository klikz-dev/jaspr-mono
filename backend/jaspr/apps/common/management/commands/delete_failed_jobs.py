from datetime import timedelta

from jaspr.apps.common.jobs.rq import cleanup_failed_jobs
from jaspr.apps.common.management.base import JasprBaseCommand


class Command(JasprBaseCommand):
    """
    Delete jobs from the 'FailedJobRegistry' that have an expiry earlier than the
    specified or default number of hours.
    """

    # Use the docstring defined above as `help` for the management command.
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument(
            "--high",
            type=int,
            default=24,
            help="Failed jobs in the 'high' queue older than this number of hours should be deleted.",
        )
        parser.add_argument(
            "--default",
            type=int,
            default=24,
            help="Failed jobs in the 'default' queue older than this number of hours should be deleted.",
        )
        parser.add_argument(
            "--low",
            type=int,
            default=24,
            help="Failed jobs in the 'low' queue older than this number of hours should be deleted.",
        )

    def handle(self, *app_labels, **options):
        cleanup_failed_jobs(
            high_delta=timedelta(hours=options["high"]),
            default_delta=timedelta(hours=options["default"]),
            low_delta=timedelta(hours=options["low"]),
            log_regular=self.stdout.write,
            log_success=lambda s: self.stdout.write(self.style.SUCCESS(s)),
        )
