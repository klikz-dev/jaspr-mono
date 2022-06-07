import os
from typing import List

from jaspr.apps.kiosk.activities.activity_utils import get_file_versions
from jaspr.apps.kiosk.models import Encounter, AssignedActivity
from jaspr.apps.kiosk.models.lethal_means import LethalMeans

VERSIONS = get_file_versions(os.path.join(os.path.dirname(__file__), "questions"))

def create(encounter: Encounter) -> AssignedActivity:
    lm = LethalMeans()
    lm.save()
    aa = AssignedActivity(
        encounter=encounter,
        lethal_means=lm
    )
    aa.save()
    return aa


def get_versions() -> List[str]:
    return VERSIONS
