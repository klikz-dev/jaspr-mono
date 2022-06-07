from jaspr.apps.kiosk.activities.activity_utils import IActivity, ActivityType, ActivityStatus


class ComfortAndSkillsActivity(IActivity):
    class Meta:
        abstract = True

    """
    Comfort and Skills activity interface.
    Most of the implementation comes from the base class.
    """

    def type(self) -> ActivityType:
        return ActivityType.ComfortAndSkills

    def get_status(self) -> ActivityStatus:
        return ActivityStatus.ASSIGNED

    def get_status_updated(self) -> None:
        return None

    def update_status(self, update=False) -> bool:
        return True

    def save_answers(self, answers: dict, takeaway_kit: bool = False) -> None:
        return None

    @property
    def answers(self):
        return {}
