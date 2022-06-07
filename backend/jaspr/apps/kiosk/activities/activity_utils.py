import os
from datetime import datetime
from enum import Enum
from typing import List, Optional, TYPE_CHECKING

from django.apps import apps
from django.db import models, transaction
from django.db.models import Prefetch
from django.utils import timezone
from django.utils.functional import cached_property
from django.conf import settings

from jaspr.apps.kiosk.activities.errors import ActivityValidationError
from .question_json import camelcase_to_underscore, extract_answer_keys_from_json
from ..models import AssignmentLocks

if TYPE_CHECKING:
    from ..models import AssignedActivity


class ActivityType(Enum):
    StabilityPlan = 1
    SuicideAssessment = 2
    ComfortAndSkills = 3
    Intro = 4
    Outro = 5
    LethalMeans = 6

    def is_explicit(self):
        return int(self.value) <= 3

    def is_implicit(self):
        return int(self.value) > 3

    def __str__(self):
        return ACTIVITY_STR[self]

ACTIVITY_STR = {
    ActivityType.Outro: "outro",
    ActivityType.Intro: "intro",
    ActivityType.LethalMeans: "lethal_means",
    ActivityType.ComfortAndSkills: "comfort_and_skills",
    ActivityType.SuicideAssessment: "suicide_assessment",
    ActivityType.StabilityPlan: "stability_plan"
}


class ActivityStatus(Enum):
    NOT_ASSIGNED = "not-assigned"
    ASSIGNED = 'assigned'
    NOT_STARTED = "not-started"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    UPDATED = "updated"

    def __str__(self):
        return ACTIVITY_STATUS_STR[self]


ACTIVITY_STATUS_STR = {
    ActivityStatus.NOT_ASSIGNED: "not-assigned",
    ActivityStatus.ASSIGNED: "assigned",
    ActivityStatus.NOT_STARTED: "not-started",
    ActivityStatus.IN_PROGRESS: "in-progress",
    ActivityStatus.COMPLETED: "completed",
    ActivityStatus.UPDATED: "updated",
}


class IActivity(models.Model):
    """
    Interface for all activity classes.
    These methods must be implemented.
    """

    class Meta:
        abstract = True
        ordering = ["-created"]

    def type(self) -> ActivityType:
        raise NotImplementedError

    def user_selected_activity(self) -> bool:
        return True

    def get_progress_bar_label(self) -> Optional[str]:
        return None

    def can_be_deleted(self) -> bool:
        """
        This is a stub method for a future function.
        Don't need to actually implement it yet.
        """
        return False

    def delete(self) -> bool:
        """
        This is a stub method for a future function.
        Don't need to actually implement it yet.
        """
        return False

    def get_answers(self) -> dict:
        if self.answers is not None:
            return self.answers
        return {}

    def save_answers(self, answers: dict, takeaway_kit: bool = False) -> None:
        """
        This is assumed to always be a partial update.
        Answers from this dictionary update the values already found in
        the database.
        """
        result = self.get_answers()
        update = False
        answer_keys = self.get_answer_keys()
        for key in answer_keys:
            if key in answers and (key not in result or result[key] != answers[key]):
                result[key] = answers[key]
                update = True

        self.answers = result
        self.update_status(update=update)
        self.save()

    def lock(self) -> None:
        AssignmentLocks.objects.create(
            activity=self.get_assigned_activity(),
            locked=True
        )
        try:
            # Remove cached property so it can be refreshed
            del self.get_assigned_activity().current_assignment_lock
        except AttributeError:
            # Property has not been cached
            pass

        self.encounter.update_section_uid(self.encounter.get_next_section_uid())

    def unlock(self) -> None:
        a = AssignmentLocks.objects.create(
            activity=self.get_assigned_activity(),
            locked=False
        )
        try:
            # Remove cached property so it can be refreshed
            del self.get_assigned_activity().current_assignment_lock
        except AttributeError:
            # Property has not been cached
            pass

    @property
    def locked(self) -> bool:
        return self.get_assigned_activity().locked

    def get_questions(self) -> List:
        """
        The concrete implementation will need to return
        the correct list of questions based on the context of
        the encounter's activity stream.
        I expect most of the question lists for this will be static JSON
        and depending on the situation a different static JSON file will be
        returned here. The one major exception will be exit questions which live in
        the database.
        """
        return []

    @staticmethod
    def get_static_questions() -> List:
        """Fetch a generic question list on the model object and when a model instance is unavailable"""
        return []

    def get_answer_keys(self) -> List[str]:
        """
        Based on the current instance, extract the answerkeys required.
        """
        return extract_answer_keys_from_json(self.get_questions())

    def get_status(self) -> ActivityStatus:
        """
        This is the status of the current activity.
        """
        assigned_activity = self.get_assigned_activity()
        status = ActivityStatus(assigned_activity.activity_status)

        if assigned_activity.locked:
            # if the activity is locked, then the status should be COMPLETED
            status = ActivityStatus.COMPLETED
        return status

    def get_status_updated(self) -> Optional[datetime]:
        """
        This is the timestamp of when the status for the current activity was updated.
        """
        assigned_activity = self.get_assigned_activity()
        status_updated = assigned_activity.activity_status_updated
        if assigned_activity.locked:
            # if the activity is locked, then the status updated should be the creation timestamp of the lock object
            status_updated = assigned_activity.current_assignment_lock.created
        return status_updated

    def update_status(self, update=False, takeaway_kit=False) -> bool:
        """
        This updates the status of an activity.
        Return value indicates whether the status changed or not.
        """
        aa = self.get_assigned_activity()
        original_status = aa.activity_status
        status = original_status
        if not status:
            status = str(ActivityStatus.NOT_STARTED)
        encounter = self.encounter
        current_section_uid = encounter.current_section_uid
        current_index = encounter.get_safe_index(current_section_uid)
        questions = self.get_questions()
        start_uid = camelcase_to_underscore(questions[0]["uid"])
        start_index = encounter.get_safe_index(start_uid)
        end_uid = camelcase_to_underscore(questions[-1]["uid"])
        end_index = encounter.get_safe_index(end_uid)

        if status == str(ActivityStatus.NOT_STARTED) and takeaway_kit:
            status = str(ActivityStatus.IN_PROGRESS)
        if start_index <= current_index < end_index:
            status = str(ActivityStatus.IN_PROGRESS)
        elif current_index > end_index:
            if original_status == ActivityStatus.COMPLETED and update:
                status = str(ActivityStatus.UPDATED)
            else:
                status = str(ActivityStatus.COMPLETED)

        if status != original_status:
            aa.activity_status = status
            aa.activity_status_updated = timezone.now()
            if update and aa.start_time is None:
                aa.start_time = timezone.now()
            aa.save()
            return True
        return False

    def get_assigned_activity(self) -> 'AssignedActivity':
        """ This interface is used for both AssignedActivities and Activities"""
        return self.assignedactivity

    def get_activity(self):
        """ This interface is used for both AssignedActivities and Activities"""
        return self

    @property
    def encounter(self):
        return self.assignedactivity.encounter

    def get_metadata(self):
        return None

    def is_only_cs(self):
        """
        Is comfort and skills the only activity being used?
        """
        for activity in self.encounter.assignedactivity_set.all():
            activity_type = activity.type
            if activity_type != ActivityType.ComfortAndSkills and activity_type != ActivityType.Intro:
                return False
        return True

    def get_template_vars(self):
        """
        Thse are the variables used to convert a Django template to a JSON document.
        """
        Patient = apps.get_model('kiosk', 'Patient')
        department = self.encounter.department
        preferences = department.get_preferences()
        csa_assigned = self.encounter.has_activity(ActivityType.SuicideAssessment)
        csp_assigned = self.encounter.has_activity(ActivityType.StabilityPlan)
        jah_consent = self.encounter.patient.tools_to_go_status != Patient.TOOLS_TO_GO_NOT_STARTED
        has_security_steps = self.encounter.has_security_steps
        answers = self.encounter.get_answers().get("answers")
        stability_plan_label = preferences.stability_plan_label if preferences else "Stability Plan"

        return {
            "media_root_url": settings.MEDIA_URL,
            "csa_assigned": csa_assigned,
            "csp_assigned": csp_assigned,
            "jah_consented": jah_consent,
            "has_security_steps": has_security_steps,
            "reasons_live_answered": bool(answers.get('reasons_live')),
            "stability_plan_label": stability_plan_label,
        }

    @staticmethod
    def get_default_template_vars():
        """Returns default template vars on the model when a model instance is unavailable"""
        return {
            "media_root_url": settings.MEDIA_URL,
            "csa_assigned": True,
            "csp_assigned": True,
            "jah_consented": True,
            "has_security_steps": True,
            "reasons_live_answered": True,
        }

    def raise_validation_error(self, validation_type: str, field : str):
        raise ActivityValidationError(validation_type, field)


def default_version_extractor(filename) -> str:
    return filename.replace(".json.tpl", "")


def get_file_versions(directory, version_extractor=default_version_extractor) -> List[str]:
    """
    This function goes through all the question JSON documents
    in a folder and extracts the unique versions from it.
    """
    files = os.listdir(directory)
    versions = []
    for filename in files:
        try:
            filename.index(".json.tpl")
            version = version_extractor(filename)
            versions.append(version)
        except ValueError:
            pass
    return versions
