import os
from typing import List

from jaspr.apps.kiosk.activities.activity_utils import IActivity
from jaspr.apps.kiosk.models import Encounter, AssignedActivity, CrisisStabilityPlan


def create(encounter: Encounter) -> IActivity:
    csp = CrisisStabilityPlan()
    csp.save()
    aa = AssignedActivity(
        encounter=encounter,
        stability_plan=csp
    )
    aa.save()
    return aa


def get_versions() -> List[str]:
    files = os.listdir("./questions")
    versions = []
    for filename in files:
        if filename.index(".json.tmpl") > -1:
            version = filename.strip(".json.tmpl")
            versions.append(version)
    return versions
