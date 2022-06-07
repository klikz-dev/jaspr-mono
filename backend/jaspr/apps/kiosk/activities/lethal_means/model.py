import json
from pathlib import Path
from typing import List
from django.template.loader import render_to_string
from jaspr.apps.kiosk.activities.activity_utils import IActivity, ActivityType

PATH_ROOT = Path(__file__).parent / "questions"
FILENAME = "0.0.json.tpl"
QUESTION_FILE = (PATH_ROOT / FILENAME).resolve()


class LethalMeansActivity(IActivity):
    """
    Interface for all activity classes.
    These methods must be implemented.
    """

    class Meta:
        abstract = True

    def type(self) -> ActivityType:
        return ActivityType.LethalMeans

    def user_selected_activity(self) -> bool:
        return False

    def get_progress_bar_label(self) -> str:
        return "Make Home Safer"

    def get_template_vars(self) -> dict:
        if not self.answers:
            return {"means_yes_no_answered": False}
        return {"means_yes_no_answered": "means_yes_no" in self.answers}

    def get_questions(self) -> List:
        question_json = render_to_string(QUESTION_FILE, self.get_template_vars())
        return json.loads(str(question_json))

    @staticmethod
    def get_static_questions():
        """Fetch a generic question list on the model object and when a model instance is unavailable"""
        question_json = render_to_string(QUESTION_FILE, {"means_yes_no_answered": False})
        return json.loads(str(question_json))

