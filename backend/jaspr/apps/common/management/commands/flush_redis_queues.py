from jaspr.apps.common.jobs.rq import cleanup_all_rq_data
from jaspr.apps.common.management.base import JasprBaseCommand


class Command(JasprBaseCommand):
    """
    Flush redis queues, including regular queues and scheduler queues. Also flush the
    failed job registry.
    """

    # Use the docstring defined above as `help` for the management command.
    help = __doc__

    def handle(self, *app_labels, **options):
        cleanup_all_rq_data()
