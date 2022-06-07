import pytz
import logging
import traceback
from collections import namedtuple
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime
import requests
from django.apps import apps
from django.db.models import Prefetch
from django.conf import settings
from django.utils import timezone

from jaspr.apps.epic.models import NotesLog
from jaspr.apps.kiosk.activities.activity_utils import ActivityType, ActivityStatus

logger = logging.getLogger(__name__)

# Workaround to deal with weak DH keys used at Allina
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'


class NarrativeNote:

    # Note: NO_ENTRY symbols were previously emdash unicode characters.  However, Epic was garbling
    # those characters so they have been replaced with regular dashes.
    NO_ENTRY_SYMBOL = "(Not Answered)"
    QUOTED_NO_ENTRY_SYMBOL = "(Not Answered)"
    YES = "YES"
    NO = "NO"

    CORE_SUICIDE_ITEMS = (
        (1, "rate_psych", "psychological pain", "most_painful"),
        (2, "rate_stress", "stress", "most_stress"),
        (3, "rate_agitation", "agitation", "causes_agitation"),
        (4, "rate_hopeless", "hopelessness", "most_hopeless"),
        (5, "rate_self_hate", "self-hate", "most_hate"),
    )

    def __init__(self, encounter, admin=False) -> None:
        Encounter = apps.get_model('kiosk', 'Encounter')
        AssignedActivity = apps.get_model('kiosk', 'AssignedActivity')
        self.encounter = Encounter.objects.select_related('patient', 'department').prefetch_related(Prefetch(
            "assignedactivity_set",
            queryset=AssignedActivity.objects.order_by("-created").select_related(
                'stability_plan', 'suicide_assessment', 'comfort_and_skills', 'intro', 'outro', 'lethal_means'
            )
        )).get(pk=encounter.pk)

        self.answers = encounter.get_answers()
        self.admin = True

    def display(self, prop: str, no_entry: Optional[str] = NO_ENTRY_SYMBOL) -> str:
        answers_and_meta = self.encounter.get_answers()
        answers = answers_and_meta["answers"]
        answers.update(answers_and_meta["metadata"])
        value = answers.get(prop)
        if value or value == 0:
            return answers.get(prop)
        return no_entry

    def quote_no_entry(self, prop: str) -> str:
        return self.display(prop, no_entry=self.QUOTED_NO_ENTRY_SYMBOL)

    def yesnoify(
        self, prop: str, yes: str = YES, no: str = NO, no_entry=QUOTED_NO_ENTRY_SYMBOL
    ) -> str:
        """ Yes-No-Ify:  Convert boolean to yes/no """
        return (
            no_entry
            if self.answers.get("answers", {}).get(prop) is None
            else yes
            if self.answers.get("answers", {}).get(prop)
            else no
        )

    def ssi_assessment_started(self) -> bool:
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        return suicide_assessment is not None and suicide_assessment.status != ActivityStatus.NOT_STARTED

    def separate_with_commas(
        self, prop: str, no_entry: str = QUOTED_NO_ENTRY_SYMBOL, top_key: str = None, answers: dict = None
    ) -> str:
        value: List = answers if answers is not None else self.answers.get("answers", {}).get(prop)
        if value:
            if top_key:
                top = self.answers.get("answers", {}).get(top_key, []) or []

                # Highlight item if it is a users custom item
                # Custom items in the top list should have asterisks and not quotations

                question_action = self.encounter.get_question_action(prop)
                if question_action:
                    choices = question_action.get('choices', [])
                    if choices:
                        # Custom items should be in quotes
                        value = [f"\"{item}\"" if item not in choices else item for item in value]

                # Highlight item if the user placed the item in their top item list
                # Note top may be in answers as None, so the result will be None and not []
                value = [f"*{item}*" if item in top else item for item in value]

        return ", ".join(value) if value else no_entry

    def separate_with_newlines(
            self, prop: str, indent=False, no_entry: str = QUOTED_NO_ENTRY_SYMBOL, top_key: str = None
    ) -> str:
        tab: str = "\t"
        value: List = self.answers.get("answers", {}).get(prop)
        if value:
            if top_key:
                top = self.answers.get("answers", {}).get(top_key, []) or []

                # Highlight item if it is a users custom item
                # Custom items in the top list should have asterisks and not quotations
                question_action = self.encounter.get_question_action(prop)
                if question_action:
                    choices = question_action.get('choices', [])
                    if choices:
                        value = [f"\"{item}\"" if item not in choices else item for item in value]

                # Highlight item if the user placed the item in their top item list
                # Note top may be in answers as None, so the result will be None and not []
                value = [f"*{item}*" if item in top else item for item in value]

        return "+ " + f"\n{tab if indent else ''}+ ".join(value) if value else ""

    def separate_with_numberlines(self, prop: str, no_entry: str = QUOTED_NO_ENTRY_SYMBOL) -> str:
        value: List = self.answers.get("answers", {}).get(prop)
        output = ""
        i = 1
        if value:
            item_count = len(value) - 1
            for index, item in enumerate(value):
                output += f"{i}. {item}"
                if index != item_count:
                    output += "\n"
                i += 1
        return output if output else no_entry

    def core_suicide_items_data(
        self,
    ) -> List[Tuple[Optional[str], Optional[int], Optional[str]]]:
        """Return a list of 3-tuples containing (attr, rating, description) ordered by rank_feelings.

        Ex of 3-tuple: ("self-hate", 4, "most_hate")
        """

        ItemData = namedtuple("ItemData", ("item_id", "attr", "rating", "description"))
        id_data = [
            ItemData(
                item_id,
                label,
                self.answers.get("answers", {}).get(attr),
                self.answers.get("answers", {}).get(desc_attr)
                if desc_attr is not None
                else self.QUOTED_NO_ENTRY_SYMBOL,
            )
            for item_id, attr, label, desc_attr in self.CORE_SUICIDE_ITEMS
        ]
        if self.answers.get("answers", {}).get("rank_feelings"):
            ranking = [
                int(rank) for rank in self.answers.get("answers", {}).get("rank_feelings").split(",")
            ]
            id_data.sort(
                key=lambda item: 99
                if item.rating is None
                else ranking.index(item.item_id)
            )

        # remove item_id to keep data simple
        data = [(attr, rating, description) for _, attr, rating, description in id_data]

        return data

    def elevated_core_suicide_items(self) -> Union[List[Tuple], None]:
        """ return for example: [("self-hate", 4, "most_hate"),]"""

        elevated_items = [
            (
                label,
                rating,
                description if description is not None else self.QUOTED_NO_ENTRY_SYMBOL,
            )
            for label, rating, description in self.core_suicide_items_data()
            if rating and rating >= 4
        ]

        # When no elevated items, check to see if anything was entered at all.
        if len(elevated_items) == 0:
            non_elevated_items = [
                (
                    label,
                    rating,
                    description
                    if description is not None
                    else self.QUOTED_NO_ENTRY_SYMBOL,
                )
                for label, rating, description in self.core_suicide_items_data()
                if rating and rating <= 3
            ]

            # We find some items that are ranked low, so return an empty list.
            if len(non_elevated_items):
                return []

            # There were none that were ranked at all, so return None
            return None

        return elevated_items

    def core_suicide_items_text(self) -> str:

        if self.elevated_core_suicide_items() is None:
            return self.QUOTED_NO_ENTRY_SYMBOL

        elevated_items = self.elevated_core_suicide_items()
        labels = [item[0] for item in elevated_items]
        if len(labels) == len(self.CORE_SUICIDE_ITEMS):
            text = "elevated"
        elif len(labels) > 1:
            text = (
                "mixed with "
                + ", ".join(labels[:-1])
                + " and "
                + labels[-1]
                + " elevated"
            )
        elif len(elevated_items) == 1:
            text = "mixed with " + labels[0] + " elevated"
        else:
            text = "not elevated"
        return text

    def core_suicide_items_as_table(self) -> Union[List[str], str]:
        """ Return a ranked core suicide items formatted as a table. """

        rows = [
            "Rank | Item               | Rating (1-5) | Description",
        ]
        for rank, row in enumerate(self.core_suicide_items_data(), start=1):

            label, rating, description = row
            if rating is None:
                rating = self.QUOTED_NO_ENTRY_SYMBOL

            if description is None:
                description = self.QUOTED_NO_ENTRY_SYMBOL

            # watch-out for tricky substitution of QUOTED_NO_ENTRY_SYMBOL -- breaks justification.
            row = f" {rank}   | {label.title().ljust(19)}| {str(rating).ljust(13 if rating != self.QUOTED_NO_ENTRY_SYMBOL else 15)}| {description}"
            rows.append(row)
        return rows

    def merge_array_answers(self, answer_keys = []):
        answers = self.answers.get("answers", {})
        merged_answers = []
        for answer_key in answer_keys:
            a = answers.get(answer_key, [])
            if a:
                merged_answers = merged_answers + a
        return merged_answers


    def get_context(self) -> Dict[str, Any]:
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        preferences = self.encounter.department.get_preferences()
        answers = self.answers.get("answers", {})
        try:
            local_timezone = preferences.timezone
        except AttributeError:
            local_timezone = "America/New_York"
            logger.exception("No Global preferences are set")
        tz = pytz.timezone(local_timezone)
        timezone_abbrev = datetime.now().astimezone(tz).tzname()

        started = self.encounter.start_time.astimezone(tz) if self.encounter.start_time else self.NO_ENTRY_SYMBOL
        activities_last_modified = self.encounter.activities_last_modified.astimezone(
            tz) if self.encounter.activities_last_modified else None
        csp_modified = stability_plan.modified.astimezone(tz) if stability_plan else self.NO_ENTRY_SYMBOL

        check_in_time0 = self.answers.get("answers", {}).get("check_in_time0")
        check_in_time0 = datetime.strptime(check_in_time0, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(
            tz) if check_in_time0 else self.NO_ENTRY_SYMBOL

        check_in_time1 = self.answers.get("answers", {}).get("check_in_time0")
        check_in_time1 = datetime.strptime(check_in_time1, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(
            tz) if check_in_time1 else self.NO_ENTRY_SYMBOL

        rate_psych_section_viewed = suicide_assessment.rate_psych_section_viewed.astimezone(
            tz) if suicide_assessment and suicide_assessment.rate_psych_section_viewed else None

        all_strategies = self.merge_array_answers(answer_keys=["strategies_general",
                                                           "strategies_firearm",
                                                           "strategies_medicine",
                                                           "strategies_places",
                                                           "strategies_other",
                                                           "strategies_custom", ])

        context = {
            "tab": "\t",
            "newline": "\n",
            "has_stability_plan": self.encounter.has_activity(ActivityType.StabilityPlan),
            "has_suicide_assessment": self.encounter.has_activity(ActivityType.SuicideAssessment),
            "patient_first_name": self.encounter.patient.first_name,
            "patient_last_name": self.encounter.patient.last_name,
            "date_of_birth": self.encounter.patient.date_of_birth,
            "mrn": self.encounter.patient.mrn,
            "ssid": self.encounter.patient.ssid,
            "timezone": local_timezone,
            "timezone_abbrev": timezone_abbrev,
            "csp_modified": csp_modified,
            "activities_last_modified": activities_last_modified if activities_last_modified else self.NO_ENTRY_SYMBOL,
            "first_accessed": started,
            "no_entry_symbol": self.NO_ENTRY_SYMBOL,
            "quoted_no_entry_symbol": self.QUOTED_NO_ENTRY_SYMBOL,
            "rate_psych_section_viewed": rate_psych_section_viewed,
            "crisis_desc": self.display("crisis_desc"),
            "scoring_risk": self.quote_no_entry("scoring_risk"),
            "scoring_suicide_index_score": self.display(
                "scoring_suicide_index_score", no_entry=None
            ),
            "scoring_suicide_index_score_typology": self.display(
                "scoring_suicide_index_score_typology", no_entry=None
            ),
            "suicide_risk": self.display("suicide_risk", no_entry=None),
            "suicidal_yes_no": self.yesnoify("suicidal_yes_no"),
            "suicidal_yes_no_describe": self.display("suicidal_yes_no_describe", no_entry=""),
            "suicidal_freq": self.quote_no_entry("suicidal_freq"),
            "suicidal_freq_units": self.quote_no_entry("suicidal_freq_units"),
            "length_suicidal_thought": self.quote_no_entry("length_suicidal_thought"),
            "worse_yes_no": self.yesnoify("worse_yes_no", "are", "are not"),
            "nssi_yes_no": self.yesnoify("nssi_yes_no", "did", "did not"),
            "firearms_yes_no": self.yesnoify("firearms_yes_no"),
            "firearms_yes_no_describe": self.display("firearms_yes_no_describe", no_entry=""),
            "means_yes_no": self.yesnoify("means_yes_no"),
            "means_yes_no_describe": self.display("means_yes_no_describe", no_entry=""),
            "means_support_yes_no": self.display("means_support_yes_no"),
            "means_support_who": self.quote_no_entry("means_support_who"),
            "plan_yes_no": self.yesnoify("plan_yes_no"),
            "plan_yes_no_describe": self.display("plan_yes_no_describe", no_entry=""),
            "steps_yes_no": self.yesnoify("steps_yes_no", "have", "have not", None),
            "steps_yes_no_describe": self.display("steps_yes_no_describe", no_entry=""),
            "practiced_yes_no": self.yesnoify(
                "practiced_yes_no", "have", "have not", None
            ),
            "practiced_yes_no_describe": self.display("practiced_yes_no_describe", no_entry=""),
            "intent_yes_no":self.answers.get("answers", {}).get("intent_yes_no"),
            "times_tried": (
                "0 times"
                if self.answers.get("answers", {}).get("times_tried") == "no attempts"
                else "once"
                if self.answers.get("answers", {}).get("times_tried") == "once"
                else "2 + times"
                if self.answers.get("answers", {}).get("times_tried") == "many"
                else self.QUOTED_NO_ENTRY_SYMBOL
            ),
            "current_yes_no": self.yesnoify("current_yes_no", "are", "are not"),
            "current_yes_no_describe": self.display("current_yes_no_describe", no_entry=""),
            "intent_yes_no": self.yesnoify("intent_yes_no", "have", "have not"),
            "intent_yes_no_describe": self.display("intent_yes_no_describe", no_entry=""),
            "times_tried_describe": self.display("times_tried_describe", no_entry=""),
            "abuse_yes_no": self.yesnoify("abuse_yes_no"),
            "abuse_yes_no_describe": self.display("abuse_yes_no_describe", no_entry=""),
            "sleep_yes_no": self.yesnoify("sleep_yes_no"),
            "sleep_yes_no_describe": self.display("sleep_yes_no_describe", no_entry=""),
            "has_reasons_live": bool(self.answers.get("answers", {}).get("reasons_live")),
            "reasons_live": self.separate_with_commas("reasons_live", no_entry=None),
            "reasons_die": self.separate_with_commas("reasons_die", no_entry=None),
            "core_suicide_items_text": self.core_suicide_items_text(),
            "most_painful": self.quote_no_entry("most_painful"),
            "rate_psych": self.quote_no_entry("rate_psych"),
            "most_stress": self.quote_no_entry("most_stress"),
            "rate_stress": self.quote_no_entry("rate_stress"),
            "causes_agitation": self.quote_no_entry("causes_agitation"),
            "most_hopeless": self.quote_no_entry("most_hopeless"),
            "rate_hopeless": self.quote_no_entry("rate_hopeless"),
            "most_hate": self.quote_no_entry("most_hate"),
            "rate_self_hate": self.quote_no_entry("rate_self_hate"),
            "core_suicide_items_table": self.core_suicide_items_as_table(),
            "core_suicide_items_data": self.core_suicide_items_data(),
            "hospitalized_yes_no": self.yesnoify("hospitalized_yes_no"),
            "hospitalized_yes_no_describe": self.display(
                "hospitalized_yes_no_describe", no_entry=""
            ),
            "impulsive_yes_no": self.yesnoify("impulsive_yes_no"),
            "impulsive_yes_no_describe": self.display("impulsive_yes_no_describe", no_entry=""),
            "losses_yes_no": self.yesnoify("losses_yes_no"),
            "losses_yes_no_describe": self.display("losses_yes_no_describe", no_entry=""),
            "relationship_yes_no": self.yesnoify("relationship_yes_no"),
            "relationship_yes_no_describe": self.display(
                "relationship_yes_no_describe", no_entry=""
            ),
            "burden_on_others_yes_no": self.yesnoify("burden_on_others_yes_no"),
            "burden_on_others_yes_no_describe": self.display(
                "burden_on_others_yes_no_describe", no_entry=""
            ),
            "health_yes_no": self.yesnoify("health_yes_no"),
            "health_yes_no_describe": self.display("health_yes_no_describe", no_entry=""),
            "legal_yes_no": self.yesnoify("legal_yes_no"),
            "legal_yes_no_describe": self.display("legal_yes_no_describe", no_entry=""),
            "shame_yes_no": self.yesnoify("shame_yes_no"),
            "shame_yes_no_describe": self.display("shame_yes_no_describe", no_entry=""),
            "skip_reason": self.display("skip_reason", no_entry=None),
            "means_willing": self.quote_no_entry("means_willing"),
            "any_means": any(
                (
                    self.answers.get("answers", {}).get("means_willing"),
                    all_strategies,
                )
            ),
            "all_strategies": self.separate_with_commas(all_strategies, answers=all_strategies),
            "strategies_general": self.separate_with_commas("strategies_general"),
            "strategies_general_newline": self.separate_with_newlines("strategies_general", indent=True),
            "strategies_firearm": self.separate_with_commas("strategies_firearm"),
            "strategies_firearm_newline": self.separate_with_newlines("strategies_firearm", indent=True),
            "strategies_medicine": self.separate_with_commas("strategies_medicine"),
            "strategies_medicine_newline": self.separate_with_newlines("strategies_medicine", indent=True),
            "strategies_places": self.separate_with_commas("strategies_places"),
            "strategies_places_newline": self.separate_with_newlines("strategies_places", indent=True),
            "strategies_other": self.separate_with_commas("strategies_other"),
            "strategies_other_newline": self.separate_with_newlines("strategies_other", indent=True),
            "strategies_custom": self.separate_with_commas("strategies_custom"),
            "strategies_custom_newline": self.separate_with_newlines("strategies_custom", indent=True),
            "supportive_people": self.answers.get("answers", {}).get("supportive_people"),
            "ranked_reasons_live": self.separate_with_commas(
                "reasons_live", no_entry=self.NO_ENTRY_SYMBOL
            ),
            "ranked_reasons_live_numbered": self.separate_with_numberlines("reasons_live", no_entry=self.NO_ENTRY_SYMBOL),
            "one_thing": self.display("one_thing"),
            "ws_stressors": self.separate_with_newlines("ws_stressors", top_key="ws_top"),
            "ws_thoughts": self.separate_with_newlines("ws_thoughts", top_key="ws_top"),
            "ws_feelings": self.separate_with_newlines("ws_feelings", top_key="ws_top"),
            "ws_actions": self.separate_with_newlines("ws_actions", top_key="ws_top"),
            "ws_stressors_oneline": self.separate_with_commas("ws_stressors", top_key="ws_top"),
            "ws_thoughts_oneline": self.separate_with_commas("ws_thoughts", top_key="ws_top"),
            "ws_feelings_oneline": self.separate_with_commas("ws_feelings", top_key="ws_top"),
            "ws_actions_oneline": self.separate_with_commas("ws_actions", top_key="ws_top"),
            "coping_body": self.separate_with_commas("coping_body"),
            "coping_body_newline": self.separate_with_newlines("coping_body", top_key="coping_top"),
            "coping_distract": self.separate_with_commas("coping_distract"),
            "coping_distract_newline": self.separate_with_newlines("coping_distract", top_key="coping_top"),
            "coping_help_others": self.separate_with_commas("coping_help_others"),
            "coping_help_others_newline": self.separate_with_newlines("coping_help_others", top_key="coping_top"),
            "coping_courage": self.separate_with_commas("coping_courage"),
            "coping_courage_newline": self.separate_with_newlines("coping_courage", top_key="coping_top"),
            "coping_senses": self.separate_with_commas("coping_senses"),
            "coping_senses_newline": self.separate_with_newlines("coping_senses", top_key="coping_top"),
            "stability_confidence": self.quote_no_entry("stability_confidence"),
            "readiness": self.quote_no_entry("readiness"),
            "READINESS_VERY_READY": "Very Ready", ## TODO CONSTANT
            "readiness_yes_reasons": self.separate_with_commas("readiness_yes_reasons"),
            "readiness_yes_changed": self.quote_no_entry("readiness_yes_changed"),
            "readiness_no": self.display("readiness_no"),
            "check_in_time0": check_in_time0,
            "check_in_time1": check_in_time1,
            "distress0": self.display("distress0"),
            "distress1": self.display("distress1"),
            "frustration0": self.display("frustration0"),
            "frustration1": self.display("frustration1"),
            "tools_to_go_status": "has"
            if (
                self.encounter.patient.tools_to_go_status
                != self.encounter.patient.TOOLS_TO_GO_NOT_STARTED
            )
            else "has not",
        }
        return context

    @staticmethod
    def sanitize(note) -> str:
        sanitized_note = (
            note
                .strip()
                # switch out html special characters
                # for reasonable substitutes to keep security good but remain readable.
                .replace("||—||", '"-"')
                .replace("&#x27;", "'")
                .replace("&#39;", "'")
                .replace("&quot;", "\"")
                .replace("&lt;", "‹")
                .replace("&gt;", "›")
                .replace("&amp;", "and")
        )
        return sanitized_note

    def render_stability_plan_note(self) -> str:
        try:
            context = self.get_context()
        except Exception as e:
            logger.exception(
                f"Failed to render Patient Stability Plan Note template for Encounter: {self.encounter.pk}"
            )
            if settings.DEBUG and self.admin:
                return f"{e.__repr__()}\n\n{traceback.format_exc()}"
            return "There has been an error while creating the Patient Stability Plan note. Please contact JasprHealth for assistance."
        else:
            preferences = self.encounter.department.get_preferences()
            template = preferences.stability_plan_template
            if not template:
                NoteTemplate = apps.get_model('kiosk.NoteTemplate')
                template = NoteTemplate.objects.get(name="Default Stability Plan")
            note = self.sanitize(template.render(context=context))

            return note

    @property
    def narrative_note_ready(self) -> bool:
        if self.encounter.has_activity(ActivityType.StabilityPlan) or self.encounter.has_activity(ActivityType.SuicideAssessment):
            return True
        return False

    def render_narrative_note(self) -> str:
        if (
            self.narrative_note_ready
        ):

            try:
                context = self.get_context()
            except Exception as e:
                logger.exception(
                    f"Failed to render Narrative Note template for Encounter: {self.encounter.pk}"
                )
                if settings.DEBUG and self.admin:
                    return f"{e.__repr__()}\n\n{traceback.format_exc()}"
                return "There has been an error while creating note. Please contact JasprHealth for assistance."

            else:
                preferences = self.encounter.department.get_preferences()
                template = preferences.narrative_note_template
                if not template:
                    NoteTemplate = apps.get_model('kiosk.NoteTemplate')
                    template = NoteTemplate.objects.get(name="Default Narrative Note")

                note = self.sanitize(template.render(context=context))

                return note

        else:
            return "Patient has not begun Suicide Status Interview, no note available."

    def save_narrative_note(self, sender=None, trigger=None) -> NotesLog:
        note = self.render_narrative_note()

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        # The Narrative Note also includes information from the CSP so can be rendered even when a CSA is not assigned
        if suicide_assessment:
            suicide_assessment.note_generated = timezone.now()
            # We do not want to trigger an update to the modified datetime field
            suicide_assessment.save(update_fields=["note_generated"])

        note_log = NotesLog.objects.create(
            encounter=self.encounter,
            note=note,
            sent_by=sender,
            trigger=trigger,
            note_type="narrative_note",
        )

        note_log.send_to_ehr()

        return note_log

    def save_stability_plan_note(self, sender=None, trigger=None) -> NotesLog:
        note = self.render_stability_plan_note()

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.note_generated = timezone.now()
        # We do not want to trigger an update to the modified datetime field
        stability_plan.save(update_fields=["note_generated"])

        note_log = NotesLog.objects.create(
            encounter=self.encounter,
            note=note,
            sent_by=sender,
            trigger=trigger,
            note_type="stability_plan",
        )

        note_log.send_to_ehr()

        return note_log
