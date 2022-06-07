from jaspr.apps.common.management.base import JasprBaseCommand
from jaspr.apps.kiosk.jobs import review_note_sending


class Command(JasprBaseCommand):
    """
    Run this command to check for notes that have not been sent to the EHR for any SRAT or CSP but should have
    """

    help = __doc__

    def handle(self, *args, **options) -> None:
        review_note_sending()
