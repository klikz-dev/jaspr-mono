import json
import pathlib
from typing import List

from jaspr.apps.kiosk.activities.activity_utils import IActivity, ActivityType
from ..question_json import extract_answer_keys

PATH_ROOT = pathlib.Path(__file__).parent / "questions"
STANDARD_QUESTIONS_FILE = (PATH_ROOT / "0.0.json.tpl").resolve()

SCORING_CURRENT_ATTEMPT = "Current Attempt"
SCORING_NO_CURRENT_ATTEMPT = "No Current Attempt"

SCORING_SUICIDE_PLAN_AND_INTENT = "Suicide Plan and Intent"
SCORING_SUICIDE_PLAN_OR_INTENT = "Suicide Plan or Intent"
SCORING_SUICIDE_NO_PLAN_OR_INTENT = "No Suicide Plan or Intent"

SCORING_RISK_LOW = "Low"
SCORING_RISK_MODERATE = "Moderate"
SCORING_RISK_HIGH = "High"

SCORING_SUICIDE_INDEX_SCORE_WISH_TO_LIVE = "Wish to Live"
SCORING_SUICIDE_INDEX_SCORE_AMBIVALENT = "Ambivalent"
SCORING_SUICIDE_INDEX_SCORE_WISH_TO_DIE = "Wish to Die"


class SuicideAssessmentActivity(IActivity):
    """
    Comfort and Skills activity interface.
    """

    class Meta:
        abstract = True

    def type(self) -> ActivityType:
        return ActivityType.SuicideAssessment

    def get_progress_bar_label(self) -> str:
        return "Guided Interview"

    def get_questions(self) -> List:
        with open(STANDARD_QUESTIONS_FILE, "rb") as f:
            result = json.load(f)
        return result

    @staticmethod
    def get_static_questions() -> List:
        """Fetch a generic question list on the model object and when a model instance is unavailable"""
        with open(STANDARD_QUESTIONS_FILE, "rb") as f:
            result = json.load(f)
        return result

    def update_status(self, update=False) -> bool:
        self.update_scores()
        return super().update_status(update=update)

    def update_scores(self):
        answers = self.answers or {}
        required_fields_set = (
                answers.get("suicidal_yes_no") is not None
                and answers.get("intent_yes_no") is not None
                and answers.get("plan_yes_no") is not None
                and answers.get("suicide_risk") is not None
                and answers.get("hospitalized_yes_no") is not None
                and answers.get("abuse_yes_no") is not None
                and (
                        answers.get("rate_agitation") is not None
                        or answers.get("frustration0") is not None
                )
        )

        # Cannot assign the score unless the required fields are set.
        if required_fields_set:
            self.scoring_score = 0
            if answers.get("suicidal_yes_no") and answers.get("intent_yes_no"):
                self.scoring_score += 1
            if answers.get("plan_yes_no"):
                self.scoring_score += 1
            if answers.get("suicide_risk") is not None and answers.get("suicide_risk") >= 3:
                self.scoring_score += 1
            if answers.get("hospitalized_yes_no"):
                self.scoring_score += 1
            if answers.get("abuse_yes_no"):
                self.scoring_score += 1
            if (
                    answers.get("rate_agitation") is not None
                    and answers.get("rate_agitation") >= 4
            ) or (
                    answers.get("rate_agitation") is None
                    and answers.get("frustration0") is not None
                    and answers.get("frustration0") >= 7
            ):
                self.scoring_score += 1
        else:
            self.scoring_score = None

        if (
                answers.get("plan_yes_no")
                and answers.get("suicide_risk") is not None
                and answers.get("suicide_risk") >= 3
        ):
            plan_and_intent = 3
        elif (
                answers.get("plan_yes_no")
                and answers.get("suicide_risk") is not None
                and answers.get("suicide_risk") < 3
        ) or (
                answers.get("plan_yes_no") is False
                and answers.get("suicide_risk") is not None
                and answers.get("suicide_risk") >= 3
        ):
            plan_and_intent = 2
        elif (
                answers.get("plan_yes_no") is False
                and answers.get("suicide_risk") is not None
                and answers.get("suicide_risk") < 3
        ):
            plan_and_intent = 1
        else:
            plan_and_intent = None

        # Cannot assign the risk unless the required fields are set.
        if not required_fields_set:
            self.scoring_risk = None
        elif (
                self.scoring_score == 5
                or self.scoring_score == 6
                or answers.get("current_yes_no")
                or plan_and_intent == 3
        ):
            self.scoring_risk = SCORING_RISK_HIGH
        elif self.scoring_score == 3 or self.scoring_score == 4 or plan_and_intent == 2:
            self.scoring_risk = SCORING_RISK_MODERATE
        elif self.scoring_score == 1 or self.scoring_score == 2 or plan_and_intent == 1:
            self.scoring_risk = SCORING_RISK_LOW
        # NOTE: It's actually impossible to hit this `else` branch here under the
        # current logic in this function. However, leaving this here in case logic
        # changes as it feels a little safer and more clear to define the above `elif`
        # instead of doing an `else`.
        else:  # pragma: no cover
            self.scoring_risk = None

        if answers.get("wish_live") is None:
            wish_to_live = None
        elif answers.get("wish_live") < 3:
            wish_to_live = 1
        elif 3 <= answers.get("wish_live") < 6:
            wish_to_live = 2
        else:
            wish_to_live = 3

        if answers.get("wish_die") is None:
            wish_to_die = None
        elif answers.get("wish_die") < 3:
            wish_to_die = 1
        elif 3 <= answers.get("wish_die") < 6:
            wish_to_die = 2
        else:
            wish_to_die = 3

        if wish_to_live is None or wish_to_die is None:
            self.scoring_suicide_index_score = None
        else:
            self.scoring_suicide_index_score = wish_to_live - wish_to_die

        if self.scoring_suicide_index_score is None:
            self.scoring_suicide_index_score_typology = None
        elif self.scoring_suicide_index_score > 0:
            self.scoring_suicide_index_score_typology = (
                SCORING_SUICIDE_INDEX_SCORE_WISH_TO_LIVE
            )
        elif self.scoring_suicide_index_score == 0:
            self.scoring_suicide_index_score_typology = (
                SCORING_SUICIDE_INDEX_SCORE_AMBIVALENT
            )
        else:
            self.scoring_suicide_index_score_typology = (
                SCORING_SUICIDE_INDEX_SCORE_WISH_TO_DIE
            )

        if answers.get("current_yes_no"):
            self.scoring_current_attempt = SCORING_CURRENT_ATTEMPT
        elif answers.get("current_yes_no") is False:
            self.scoring_current_attempt = SCORING_NO_CURRENT_ATTEMPT
        else:
            self.scoring_current_attempt = None

        if plan_and_intent is None:
            self.scoring_suicide_plan_and_intent = None
        elif plan_and_intent == 3:
            self.scoring_suicide_plan_and_intent = SCORING_SUICIDE_PLAN_AND_INTENT
        elif plan_and_intent == 2:
            self.scoring_suicide_plan_and_intent = SCORING_SUICIDE_PLAN_OR_INTENT
        elif plan_and_intent == 1:
            self.scoring_suicide_plan_and_intent = SCORING_SUICIDE_NO_PLAN_OR_INTENT

        # Save should be called from the calling function to prevent duplicate save requests

    def get_metadata(self):
        return {
            "scoring_score": self.scoring_score,
            "scoring_current_attempt" : self.scoring_current_attempt,
            "scoring_suicide_plan_and_intent" : self.scoring_suicide_plan_and_intent,
            "scoring_risk" : self.scoring_risk,
            "scoring_suicide_index_score" : self.scoring_suicide_index_score,
            "scoring_suicide_index_score_typology" : self.scoring_suicide_index_score_typology,
        }


