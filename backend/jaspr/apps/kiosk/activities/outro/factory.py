from jaspr.apps.kiosk.activities.activity_utils import IActivity
from jaspr.apps.kiosk.models import Encounter, AssignedActivity
from jaspr.apps.kiosk.models import Outro


def create(encounter: Encounter) -> IActivity:
    outro = Outro()
    outro.save()
    aa = AssignedActivity(
        encounter=encounter,
        outro=outro
    )
    aa.save()
    return aa