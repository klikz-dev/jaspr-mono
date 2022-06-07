from jaspr.apps.kiosk.activities.activity_utils import IActivity
from jaspr.apps.kiosk.models import CustomOnboardingQuestions, Encounter, AssignedActivity


def create(encounter: Encounter) -> IActivity:
    coq = CustomOnboardingQuestions()
    coq.save()
    aa = AssignedActivity(
        encounter=encounter,
        intro=coq
    )
    aa.save()
    return aa