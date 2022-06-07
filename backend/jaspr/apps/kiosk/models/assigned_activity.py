import logging
from datetime import datetime

from django.db import models
from django.utils.functional import cached_property
from model_utils import Choices

from jaspr.apps.common.models import JasprAbstractBaseModel
from jaspr.apps.kiosk.activities.activity_utils import IActivity, ActivityType, ActivityStatus
from typing import List, Optional

logger = logging.getLogger(__name__)


class AssignedActivity(JasprAbstractBaseModel, IActivity):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    start_time = models.DateTimeField("Start Time", blank=True, null=True)

    ACTIVITY_STATUS_CHOICES = Choices(
        ActivityStatus.NOT_STARTED.value,
        ActivityStatus.IN_PROGRESS.value,
        ActivityStatus.UPDATED.value,
        ActivityStatus.COMPLETED.value
    )
    activity_status = models.CharField(
        "Activity Status",
        default=ActivityStatus.NOT_STARTED.value,
        choices=ACTIVITY_STATUS_CHOICES,
        max_length=50
    )
    activity_status_updated = models.DateTimeField("Activity Status Updated", blank=True, null=True)
    encounter = models.ForeignKey(
        'kiosk.encounter',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    stability_plan = models.OneToOneField(
        'kiosk.crisisstabilityplan',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    suicide_assessment = models.OneToOneField(
        'kiosk.srat',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    comfort_and_skills = models.OneToOneField(
        'kiosk.comfortandskills',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    intro = models.OneToOneField(
        'kiosk.customonboardingquestions',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    outro = models.OneToOneField(
        'kiosk.outro',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    lethal_means = models.OneToOneField(
        'kiosk.lethalmeans',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def get_active_module(self) -> IActivity:
        if not self.pk:
            return None
        if self.suicide_assessment is not None:
            return self.suicide_assessment
        if self.stability_plan is not None:
            return self.stability_plan
        if self.comfort_and_skills is not None:
            return self.comfort_and_skills
        if self.intro is not None:
            return self.intro
        if self.outro is not None:
            return self.outro
        if self.lethal_means is not None:
            return self.lethal_means
        raise Exception("No active module set on AssignActivity. This is an invalid state.")

    @cached_property
    def type(self) -> ActivityType:
        if not self.pk:
            return None
        if self.suicide_assessment is not None:
            return ActivityType.SuicideAssessment
        if self.stability_plan is not None:
            return ActivityType.StabilityPlan
        if self.comfort_and_skills is not None:
            return ActivityType.ComfortAndSkills
        if self.intro is not None:
            return ActivityType.Intro
        if self.outro is not None:
            return ActivityType.Outro
        if self.lethal_means is not None:
            return ActivityType.LethalMeans
        raise Exception("No active module set on AssignActivity. This is an invalid state.")

    def get_progress_bar_label(self) -> Optional[str]:
        return self.get_active_module().get_progress_bar_label()

    def get_answers(self) -> dict:
        return self.get_active_module().get_answers()

    def save_answers(self, answers: dict, takeaway_kit: bool = False) -> None:
        return self.get_active_module().save_answers(answers, takeaway_kit=takeaway_kit)

    def lock(self) -> None:
        return self.get_active_module().lock()

    def unlock(self) -> None:
        return self.get_active_module().unlock()

    def get_questions(self) -> List:
        return self.get_active_module().get_questions()

    def get_status(self) -> ActivityStatus:
        return self.get_active_module().get_status()

    def get_status_updated(self) -> Optional[datetime]:
        return self.get_active_module().get_status_updated()

    def update_status(self) -> ActivityStatus:
        return self.get_active_module().update_status()

    def get_metadata(self) -> dict:
        return self.get_active_module().get_metadata()

    def get_assigned_activity(self):
        """ This interface is used for both AssignedActivities and Activities"""
        return self

    def get_activity(self):
        """ This interface is used for both AssignedActivities and Activities"""
        return self.get_active_module()

    @cached_property
    def current_assignment_lock(self):
        # assignment locks must be ordered by -modified, which is the default model ordering
        assignment_lock = self.assignmentlocks_set.first()
        return assignment_lock

    @property
    def locked(self):
        if self.current_assignment_lock:
            return self.current_assignment_lock.locked
        return False

    @property
    def is_assignment_lock_acknowledged(self):
        return self.current_assignment_lock.acknowledged

    class Meta:
        verbose_name_plural = "Assigned Activities"


