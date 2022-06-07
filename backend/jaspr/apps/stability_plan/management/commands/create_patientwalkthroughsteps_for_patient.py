from django.core.management.base import CommandParser
from jaspr.apps.common.management.base import JasprBaseCommand
from jaspr.apps.kiosk.models import Patient
from jaspr.apps.stability_plan.walkthrough_manager import WalkthroughManager


class Command(JasprBaseCommand):
    """
    Run this command to update or create PatientWalkthroughSteps for a patient.
    """

    help = __doc__

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-p", "--patient_pk", help="the patient pk",
        )

    def handle(self, *args, **options) -> None:
        pk = options.pop("patient_pk")
        if pk:
            patient = Patient.objects.get(pk=pk)
            manager = WalkthroughManager(patient)
            manager.handle()
