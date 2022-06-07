from jaspr.apps.common.management.base import JasprBaseCommand
from jaspr.apps.kiosk.jobs import check_for_unsent_notes


class Command(JasprBaseCommand):
    """
    Run this command to send notes to the EHR for any SRAT or CSP that has an outdated note that hasn't
    been sent in the last 10 minutes
    """

    help = __doc__

    def handle(self, *args, **options) -> None:
        check_for_unsent_notes()
