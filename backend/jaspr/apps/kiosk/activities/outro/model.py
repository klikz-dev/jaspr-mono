
import pathlib
import json
from typing import List

from django.template.loader import render_to_string
from jaspr.apps.kiosk.activities.activity_utils import IActivity, ActivityType
from ..question_json import extract_answer_keys

PATH_ROOT = pathlib.Path(__file__).parent / "questions"
STANDARD_QUESTIONS_FILE = (PATH_ROOT / "standard.json.tpl").resolve()


class OutroActivity(IActivity):
    """
    Interface for all activity classes.
    These methods must be implemented.
    """

    class Meta:
        abstract = True

    def type(self) -> ActivityType:
        return ActivityType.Outro

    def user_selected_activity(self) -> bool:
        return False

    def get_answer_keys(self) -> List[str]:
        template_vars = self.get_template_vars()
        return extract_answer_keys(STANDARD_QUESTIONS_FILE, template_vars=template_vars)

    def get_questions(self) -> List:
        question_json = render_to_string(STANDARD_QUESTIONS_FILE, self.get_template_vars())
        return json.loads(str(question_json))

    @staticmethod
    def get_static_questions() -> List:
        """Fetch a generic question list on the model object and when a model instance is unavailable"""
        question_json = render_to_string(STANDARD_QUESTIONS_FILE, OutroActivity.get_default_template_vars())
        return json.loads(str(question_json))

