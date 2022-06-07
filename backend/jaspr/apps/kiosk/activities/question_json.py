import json
import random
import re
from enum import Enum
from typing import List, Dict, Optional
from djangorestframework_camel_case.util import camelize, underscoreize
from django.template.loader import render_to_string


class ActionType(Enum):
    # IGNORE THESE
    SECURITY_IMAGE = "security-image"
    SECURITY_QUESTION = "security-question"
    PROGRESS_BAR = "progress-bar"
    SECTION_CHANGE = "section-change"
    VIDEO = "video"
    COMFORT_SKILLS = "comfort-skills"
    SHARED_STORIES = "shared-stories"
    STABILITY_CARD = "stability-card"
    RANK_TOP = "rank-top"
    LIST_RANK = "list-rank"
    SORT_EDIT = "sort-edit"
    RANK = "rank"

    # GENERIC Actions (Used in multiple places)
    SCALE_BUTTONS = "scalebuttons"
    BUTTONS = "buttons"
    CHOICE = "choice"
    SLIDER = "slider"
    TEXT = "text"
    COPING_STRATEGY = "coping-strategy"
    LIST = "list"
    TAB_CHOICE = "tab-choice"

    # ONE OFF Actions (Used once)
    MEANS_CUSTOM = "means-custom"
    ASSESSMENT_LOCK = "assessment-lock"
    GIVE_CONSENT = "give-consent"
    SUPPORTIVE_PEOPLE = "supportive-people"
    COUNTER = "counter"


LOREM_IPSUM_LONG = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec est ut sem pharetra euismod."
LOREM_IPSUM_SHORT = "Lorem ipsum dolor"


def gak(action):
    """ Get Answer Key"""
    return camelcase_to_underscore(action["answerKey"])


def scalebutton_gen(action):
    def __inner__():
        return {
            gak(action): random.randint(action["min"], action["max"])
        }
    return __inner__


def buttons_gen(action):
    def __inner__():
        if "answerKey" not in action:
            return {}
        count = len(action["buttons"])
        index = random.randint(0, count-1)
        return {
            gak(action): action["buttons"][index]["label"]
        }
    return __inner__


def noop_gen(action):
    def __inner__():
        return {}
    return __inner__


def choice_gen(action):
    count = len(action["options"])
    multiple = False
    if "multiple" in action and action["multiple"]:
        multiple = True

    def __inner__():
        index = random.randint(0, count-1)
        value = action["options"][index]["value"]
        if multiple:
            # convert to an array
            value = [value,]
        result = {
            gak(action): value
        }
        return result
    return __inner__


def tab_choice_gen(action):
    def __inner__():
        result = {}
        for group in action["groups"]:
            count = len(group["options"])
            index = random.randint(0, count-1)
            result[gak(group)] = group["options"][index]["value"]
        return result
    return __inner__


def means_custom_gen(action):
    def __inner__():
        result = {
            "strategies_custom": [
                "Go skiing",
                "Go sailing",
                "Go for a walk with my dog"
            ]
        }
        return result
    return __inner__


def text_gen(action):
    def __inner__():
        result = { gak(action): LOREM_IPSUM_LONG }
        return result
    return __inner__


def coping_strat_gen(action):
    def __inner__():
        count = len(action["choices"])
        index = random.randint(0, count-1)
        result = {
            gak(action): [action["choices"][index],]
        }
        return result
    return __inner__


def supportive_people_gen(action):
    def __inner__():
        return {
            "supportive_people": [
                { "name": "Todd Cullen", "phone": "123-456-7890"},
                {"name": "Jacob Lesser", "phone": "223-456-7890"},
            ]
        }
    return __inner__


def list_gen(action):
    def __inner__():
        return {
            gak(action): [
                LOREM_IPSUM_SHORT + " 1",
                LOREM_IPSUM_SHORT + " 2"
            ]
        }
    return __inner__


def counter_gen(action):
    def __inner__():
        return {
            "suicidal_freq": 1,
            "suicidal_freq_units": "month",
        }
    return __inner__


def tab_choice_gen(action):
    def __inner__():
        result = {}
        for group in action["groups"]:
            count = len(group["options"])
            index = random.randint(0, count - 1)
            result[gak(group)] = [group["options"][index]["label"],]
        return result
    return __inner__


def rank_gen(action):
    def __inner__():
        result = []
        for option in action["options"]:
            result.append(option["answerKey"])
        return {
            gak(action): result
        }
    return __inner__


ACTION_TYPE_TO_ANSWER_GENERATOR = {
    ActionType.SCALE_BUTTONS: scalebutton_gen,
    ActionType.BUTTONS: buttons_gen,
    ActionType.SECURITY_IMAGE: noop_gen,
    ActionType.SECURITY_QUESTION: noop_gen,
    ActionType.PROGRESS_BAR: noop_gen,
    ActionType.SECTION_CHANGE: noop_gen,
    ActionType.CHOICE: choice_gen,
    ActionType.MEANS_CUSTOM: means_custom_gen,
    ActionType.ASSESSMENT_LOCK: noop_gen,
    ActionType.GIVE_CONSENT: choice_gen, # Check this choice
    ActionType.SLIDER: scalebutton_gen, # Check this choice
    ActionType.VIDEO: noop_gen,
    ActionType.TEXT: text_gen,
    ActionType.COMFORT_SKILLS: noop_gen,
    ActionType.SHARED_STORIES: noop_gen,
    ActionType.STABILITY_CARD: noop_gen,
    ActionType.COPING_STRATEGY: coping_strat_gen,
    ActionType.SUPPORTIVE_PEOPLE: supportive_people_gen,
    ActionType.RANK_TOP: noop_gen,
    ActionType.LIST: list_gen,
    ActionType.LIST_RANK: noop_gen,
    ActionType.SORT_EDIT: noop_gen,
    ActionType.RANK: rank_gen,
    ActionType.COUNTER: counter_gen,
    ActionType.TAB_CHOICE: tab_choice_gen,
}


def camelcase_to_underscore(value: str) -> str:
    return [
        *underscoreize(
            {value: ""},
            no_underscore_before_number=True,
        )
    ][0]


def underscore_to_camel(value: str) -> str:
    return [*camelize({value: ""})][0]


def extract_answer_keys(filepath, template_vars=None) -> List[str]:
    questions = None
    if template_vars:
        question_json = render_to_string(filepath, template_vars)
        questions = json.loads(question_json)
    else:
        with open(filepath, "rb") as f:
            questions = json.load(f)

    return extract_answer_keys_from_json(questions)


# A question's answer_key describes the dictionary key to which a particular questions answer is saved.
# Questions can have one or more answer_key's associated with them.  An action can have a list of groups, with
# each group having it's own answerkey.  An action can also have an answer_key directly.  In one special instance,
# the answer_key may be two answer_keys separated by a pipe (|), e.g. suicidalFreq|suicidalFreqUnit.
def extract_answer_keys_from_json(questions):
    answer_keys = []
    for question in questions:
        for action in question["actions"]:
            if "answerKey" in action:
                aks = action["answerKey"].split("|")
                for answer_key in aks:
                    key = camelcase_to_underscore(answer_key)
                    answer_keys.append(key)

            if "groups" in action:
                for group in action["groups"]:
                    if "answerKey" in group:
                        key = camelcase_to_underscore(group["answerKey"])
                        answer_keys.append(key)
    return answer_keys


def generate_answers_from_questions(activities=None, activity=None):
    if activity is not None:
        activities = [activity]
    if activities is None:
        raise Exception("You must provide either an activity or a list of activities")

    result = {}
    for activity in activities:
        answers = generate_answers_from_question_list(activity.get_questions())
        result.update(answers)
    return result


def generate_answers_from_question_list(questions):
    result = {}
    for question in questions:
        for action in question["actions"]:
            at = ActionType(action["type"])
            generator = ACTION_TYPE_TO_ANSWER_GENERATOR[at]
            value = generator(action)()
            result.update(value)
    return result

def create_section_dictionary(questions):
    dictionary = {}
    for question in questions:
        if 'uid' in question:
            question_uid = camelcase_to_underscore(question["uid"])
            dictionary[question_uid] = {"questions": []}

            if "actions" in question:
                for action in question["actions"]:
                    if "answerKey" in action:
                        aks = action["answerKey"].split("|")
                        for answer_key in aks:
                            answer_key = camelcase_to_underscore(answer_key)
                            dictionary[question_uid]["questions"].append(answer_key)

                    if "groups" in action:
                        for group in action["groups"]:
                            answer_key = camelcase_to_underscore(group["answerKey"])
                            dictionary[question_uid]["questions"].append(answer_key)
    return dictionary


NUMBER_ANSWER_KEY_REGEX = re.compile(r"[0-9]+$")


def section_uid_to_answer_key(sections_dictionary: dict, answer_key: str) -> Optional[str]:
    """
    At the time of writing, `answer_key` is assumed to be the current question for
    the `Assessment`, and we take the first section uid in the list (if it shows
    up multiple times) as the section uid to use.

    This could be improved later by passing in more contextual information around the
    current question so that we could always correctly have the exact section uid
    with the question key in cases where there are multiple section uids a question
    key is contained in.
    """

    answer_key_to_section_ids: Dict[str, List[str]] = {}
    for uid, sub_dictionary in sections_dictionary.items():
        for keys in sub_dictionary["questions"]:
            for key in keys.split("|"):
                if key in answer_key_to_section_ids:
                    answer_key_to_section_ids[key].append(uid)
                else:
                    answer_key_to_section_ids[key] = [uid]

    if answer_key in answer_key_to_section_ids:
        return answer_key_to_section_ids[answer_key][0]

    match = re.search(NUMBER_ANSWER_KEY_REGEX, answer_key)
    if match:
        new_answer_key = re.sub(NUMBER_ANSWER_KEY_REGEX, "", answer_key)
        if new_answer_key in answer_key_to_section_ids:
            return answer_key_to_section_ids[new_answer_key][0]
    return None


def get_question_action(questions: list, answer_key: str) -> Optional[dict]:
    for question in questions:
        if "actions" in question:
            for action in question["actions"]:
                if "answerKey" in action:
                    if action["answerKey"] == underscore_to_camel(answer_key):
                        return action

                if "groups" in action:
                    groups = action["groups"]
                    for group in groups:
                        if "answerKey" in group:
                            if group["answerKey"] == underscore_to_camel(answer_key):
                                return action
    return None
