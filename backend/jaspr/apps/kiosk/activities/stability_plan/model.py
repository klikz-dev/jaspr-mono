import json
import pathlib
from typing import List

from django.db import transaction

from jaspr.apps.kiosk.activities.activity_utils import IActivity, ActivityType
from django.utils import timezone
from django.template.loader import render_to_string

from jaspr.apps.kiosk.activities.errors import ActivityValidationError
from jaspr.apps.kiosk.helpers import update_coping_fields

PATH_ROOT = pathlib.Path(__file__).parent / "questions"
STANDARD_QUESTIONS_FILE = (PATH_ROOT / "0.0.json.tpl").resolve()
FIELDS = [
    "reasons_live",
    "strategies_general",
    "strategies_firearm",
    "strategies_medicine",
    "strategies_places",
    "strategies_other",
    "strategies_custom",
    "means_support_yes_no",
    "means_support_who",
    "coping_body",
    "coping_distract",
    "coping_help_others",
    "coping_courage",
    "coping_senses",
    "supportive_people",
    "coping_top",
    "ws_stressors",
    "ws_thoughts",
    "ws_feelings",
    "ws_actions",
    "ws_top",
]


class StabilityPlanActivity(IActivity):
    """
    Comfort and Skills activity interface.
    """

    class Meta:
        abstract = True

    def type(self) -> ActivityType:
        return ActivityType.StabilityPlan

    def get_progress_bar_label(self) -> str:
        return "Plan to Cope"

    def get_answers(self) -> dict:
        """
        Filter the answers by the answer keys in the question set.
        """
        result = self.answers
        if result is None:
            result = {}
        for field in FIELDS:
            value = getattr(self, field)
            result[field] = value
        return result

    @transaction.atomic
    def save_answers(self, answers: dict, takeaway_kit: bool = False) -> None:
        update = False
        # Get instance copy before new answers are saved, so we can compare differences later
        # This also ensures we have the latest answers
        old_instance = type(self).objects.select_for_update().get(pk=self.pk)
        for field in self._meta.fields:
            setattr(old_instance, field.name, getattr(self, field.name))

        # instance = (
        #     type(self).objects.select_for_update().get(pk=self.pk)
        # )
        if old_instance.answers is None:
            self.answers = {}
        if answers is None:
            answers = {}
        answer_keys = self.get_answer_keys()
        for k in answers.keys():
            if k == "supportive_people":
                # validate supportive people
                # TODO: Move validation to framework
                if not isinstance(answers[k], list):
                    self.raise_validation_error(ActivityValidationError.LIST_REQUIRED)
                self.validate_supportive_people(answers[k])

            if k in FIELDS:
                if getattr(self, k) != answers[k]:
                    setattr(self, k, answers[k])
                    update = True
            elif k in answer_keys:
                # Key must be in the answer keys for CSP's questions
                if k not in self.answers or self.answers[k] != answers[k]:
                    self.answers[k] = answers[k]
                    update = True
        self.update_status(update=update, takeaway_kit=takeaway_kit)
        self.save()

        update_coping_fields(old_instance, self)

    def validate_supportive_people(self, people) -> None:
        for person in people:
            if not (person.get("name") or person.get("phone")):
                self.raise_validation_error(ActivityValidationError.NOT_ALL_BLANK, "supportive_people")
        return None

    def get_questions(self) -> list:
        question_json = render_to_string(STANDARD_QUESTIONS_FILE, self.get_template_vars())
        return json.loads(str(question_json))

    @staticmethod
    def get_static_questions() -> List:
        """Fetch a generic question list on the model object and when a model instance is unavailable"""
        question_json = render_to_string(STANDARD_QUESTIONS_FILE, StabilityPlanActivity.get_default_template_vars())
        return json.loads(str(question_json))

