import json
import pathlib
from typing import Optional, List
from django.template.loader import render_to_string

from jaspr.apps.kiosk.activities.activity_utils import IActivity, ActivityType
from ..question_json import extract_answer_keys

PATH_ROOT = pathlib.Path(__file__).parent / "questions"
STANDARD_QUESTIONS_FILE = (PATH_ROOT / "standard.json.tpl").resolve()
CS_ONLY_QUESTIONS_FILE = (PATH_ROOT / "path3.json.tpl").resolve()


class IntroActivity(IActivity):
    """
    Interface for all activity classes.
    These methods must be implemented.
    """

    class Meta:
        abstract = True

    def type(self) -> ActivityType:
        return ActivityType.Intro

    def user_selected_activity(self) -> bool:
        return False

    def get_progress_bar_label(self) -> Optional[str]:
        return None

    def get_answer_keys(self) -> List[str]:
        template_vars = self.get_template_vars()
        if self.is_only_cs():
            return extract_answer_keys(CS_ONLY_QUESTIONS_FILE, template_vars=template_vars)
        return extract_answer_keys(STANDARD_QUESTIONS_FILE, template_vars=template_vars)

    def get_questions(self) -> List:
        if self.is_only_cs():
            result = render_to_string(CS_ONLY_QUESTIONS_FILE, self.get_template_vars())
            return json.loads(str(result))
        else:
            result = render_to_string(STANDARD_QUESTIONS_FILE, self.get_template_vars())
            return json.loads(str(result))

    @staticmethod
    def get_static_questions():
        """This function makes it possible to fetch a generic question
        list on the model object and doesn't require an instance"""
        question_json = render_to_string(STANDARD_QUESTIONS_FILE, {"means_yes_no_answered": False})
        return json.loads(str(question_json))


