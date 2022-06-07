
from jaspr.apps.kiosk.activities.activity_utils import IActivity
from jaspr.apps.kiosk.models import AssignedActivity, ComfortAndSkills

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jaspr.apps.kiosk.models import Encounter


def create(encounter: "Encounter") -> IActivity:
    # check encounter for existing C&S activity
    # if it exists, return it
    # otherwise create a new one and return that
    try:
        return encounter.assignedactivity_set.exclude(comfort_and_skills=None).get()
    except AssignedActivity.DoesNotExist:
        pass

    cs = ComfortAndSkills()
    cs.save()
    aa = AssignedActivity(
        encounter=encounter,
        comfort_and_skills=cs
    )
    aa.save()
    return aa

