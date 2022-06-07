"""Test operations on Assessment"""
import re
from csv import DictReader
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from freezegun import freeze_time

from jaspr.apps.kiosk.constants import ActionNames
from jaspr.apps.test_infrastructure.testcases import JasprTestCase
from jaspr.apps.kiosk.activities.activity_utils import ActivityType


class TestKioskAssessment(JasprTestCase):

    def setUp(self):
        super().setUp()

        self.system, self.clinic, self.department = self.create_full_healthcare_system()
        self.system.name = "Clinic One"
        self.clinic.name = "Location One"

        self.patient = self.create_patient(ssid="Test Patient 1")

        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )

        self.encounter.add_activities([ActivityType.SuicideAssessment, ActivityType.StabilityPlan])

    def test_assessment_properties_some_answered(self):
        """
        Does `current_section_uid`
        return the right values if some (certain) questions are answered?
        """

        self.encounter.save_answers({
            "rate_psych": 3,
            "most_painful": "This is the most painful.",
            "rate_stress": 2,
        })
        self.encounter.refresh_from_db()

        self.assertEqual(self.encounter.current_section_uid, "rate_stress")

    ## TODO JACOB Do we still need to track unordered fields differently
    # def test_current_question_all_answered_returns_last_ordered_question(self):
    #     """
    #     Does `current_question` return the last ordered question if all ordered questions are
    #     answered? And is `current_section_uid` correct in that case too, along with
    #     `assessment_finished`?
    #     """
    #     srat = self.patient_session.srat
    #     self.assertIsNotNone(self.patient_session.current_question)
    #
    #     for field in assessment.ordered_question_fields:
    #         # `PositiveSmallIntegerField` and other similar fields
    #         # inherit from `IntegerField`.
    #         if isinstance(field, (models.IntegerField)):
    #             setattr(assessment, field.name, 1)
    #         elif isinstance(
    #             field,
    #             (
    #                 models.CharField,
    #                 models.TextField,
    #                 EncryptedCharField,
    #                 EncryptedTextField,
    #             ),
    #         ):
    #             setattr(assessment, field.name, "a")
    #         elif isinstance(field, models.BooleanField):
    #             setattr(assessment, field.name, False)
    #         elif isinstance(field, EncryptedDateTimeField):
    #             setattr(assessment, field.name, timezone.now())
    #         elif isinstance(field, ArrayField):
    #             setattr(assessment, field.name, [])
    #
    #     # need to save assessment to set current_section_uid
    #     assessment.save()
    #
    #     self.assertEqual(assessment.current_question, "overall_er_care")
    #     self.assertEqual(assessment.current_section_uid, "overall_er_care")
    #     self.assertEqual(assessment.assessment_finished, True)

    def test_current_section_uid_uses_latest_actions_section_uid_if_farther(self):
        """
        When the `Patient` has an `Action` record of `ARRIVE` on a later section
        UID, does this modify the current section UID?  We have to compare to both question
        and  Arrival order.  It's not latest chronologically  -- it's latest by section order.
        """

        # this is an early section at a later datetime.
        self.create_action(
            patient=self.patient,
            encounter=self.encounter,
            action=ActionNames.ARRIVE,
            section_uid="surviving_makes_sense",
        )

        # this is an earlier question
        self.encounter.save_answers({"shame_yes_no": True})
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        # we'll be looking for the following section below.
        self.create_action(
            patient=self.patient,
            encounter=self.encounter,
            action=ActionNames.ARRIVE,
            section_uid="skip_lethal_means",
        )

        self.encounter.refresh_from_db()

        self.assertEqual(self.encounter.current_section_uid, "surviving_makes_sense")

    def test_current_section_uid_ignores_bad_section_uid(self):
        """
        When the `Patient` has an `Action` record of `ARRIVE` on a legacy section
        UID that no longer exists, does this modify the current section UID?
        """

        # this is an earlier question
        self.encounter.save_answers({"shame_yes_no": True})
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        # we'll be looking for the following section below.
        self.create_action(
            patient=self.patient,
            encounter=self.encounter,
            action=ActionNames.ARRIVE,
            section_uid="surviving_makes_sense",
        )

        # this one we're hoping to ignore.
        self.create_action(
            patient=self.patient,
            encounter=self.encounter,
            action=ActionNames.ARRIVE,
            section_uid="bad_section_from_somewhere",
        )

        # this is an early section at a later datetime.
        self.create_action(
            patient=self.patient,
            encounter=self.encounter,
            action=ActionNames.ARRIVE,
            section_uid="skip_lethal_means",
        )

        # this one we're hoping to ignore also.
        self.create_action(
            patient=self.patient,
            encounter=self.encounter,
            action=ActionNames.ARRIVE,
            section_uid="something_not_present_probably_because_of_a_migration",
        )

        self.encounter.refresh_from_db()

        self.assertEqual(self.encounter.current_section_uid, "surviving_makes_sense")

    def test_current_section_uid_uses_original_section_uid_if_latest_actions_not_farther(
        self,
    ):
        """
        When the `Patient` has an `Action` record of `ARRIVE` on an earlier
        section UID, does this not modify the current section UID?
        """

        # this is an earlier question
        self.encounter.save_answers({"shame_yes_no": True})
        self.create_action(
            patient=self.patient,
            encounter=self.encounter,
            action=ActionNames.ARRIVE,
            section_uid="one_thing",
        )
        self.assertEqual(self.encounter.current_section_uid, "shame_describe")

    def test_current_section_uid_uses_original_section_uid_no_action_present(self):
        """
        When the `Patient` has no `Action` record of `ARRIVE`, does this not
        modify the current section UID?
        """

        self.encounter.save_answers({"shame_yes_no": True})
        self.encounter.refresh_from_db()
        self.assertEqual(self.encounter.current_section_uid, "shame_describe")

    def test_current_section_uid_uses_original_section_uid_if_latest_actions_section_uid_not_in_list(
        self,
    ):
        """
        When the `Patient` has an `Action` record of `ARRIVE` on a section UID
        that is not present in `SECTION_UIDS_ORDERED_LIST`, does this not modify the
        current section UID?
        """

        self.encounter.save_answers({"shame_yes_no": True})

        self.create_action(
            patient=self.patient,
            encounter=self.encounter,
            action=ActionNames.ARRIVE,
            section_uid="something_not_present_probably_because_of_a_migration",
        )
        self.encounter.refresh_from_db()
        self.assertEqual(self.encounter.current_section_uid, "shame_describe")

    def test_updating_distress_and_frustration_updates_check_in_time(self):
        """
        For `i` in [0, 1, 2]:
            Does `f'check_in_time{i}'` change from `None` to the current time once
            `f'distress{i}'` and `f'frustration{i}'` are not `None`?

        NOTE: At the time of writing this is implemented in `Patient Session`'s
        `save(...)` method.
        """
        self.encounter.save_answers({
            "distress0": 5,
            "frustration1": 5
        })

        # Check that none of the check in times were updated because for all check ins
        # we don't have both distress and frustration updated.
        answers = self.encounter.get_answers()
        self.assertFalse("check_in_time0" in answers["answers"])
        self.assertFalse("check_in_time1" in answers["answers"])

        first_time_freeze = timezone.now() - timedelta(minutes=3, seconds=3)
        with freeze_time(first_time_freeze):
            self.encounter.save_answers({
                "distress0": 5,
                "frustration0": 3,
                "frustration1": 5,
            })

        updated_answers = self.encounter.get_answers()
        updated_answers.update({
            "frustration1": 2,
            "distress1": 4,
        })
        second_time_freeze = first_time_freeze + timedelta(minutes=2, seconds=2)
        with freeze_time(second_time_freeze):
            self.encounter.save_answers(updated_answers)

        self.encounter.refresh_from_db()
        answers = self.encounter.get_answers()
        self.assertEqual(answers["answers"]["distress0"], 5)
        self.assertEqual(answers["answers"]["frustration0"], 3)
        self.assertEqual(datetime.fromisoformat(answers["answers"]["check_in_time0"]), first_time_freeze)

        self.assertEqual(answers["answers"]["distress1"], 4)
        self.assertEqual(answers["answers"]["frustration1"], 2)
        self.assertEqual(datetime.fromisoformat(answers["answers"]["check_in_time1"]), second_time_freeze)

    def test_check_and_reduce_top_with_top_field_empty_or_null(self):
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        for top_field_name in ["coping_top", "ws_top"]:
            with self.subTest(top_field_name=top_field_name):
                # Check setting empty.
                suicide_assessment.answers = {top_field_name: []}
                suicide_assessment.save()
                self.assertEqual(suicide_assessment.answers.get(top_field_name), [])

                # Check setting null.
                suicide_assessment.answers = {top_field_name: None}
                suicide_assessment.save()
                self.assertEqual(suicide_assessment.answers.get(top_field_name), None)

    def test_check_and_reduce_top_for_coping_top_others_empty_or_null(self):
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)

        stability_plan.coping_body = []
        stability_plan.coping_distract = None
        stability_plan.coping_help_others = None
        stability_plan.coping_courage = []
        stability_plan.coping_senses = None
        stability_plan.supportive_people = []
        stability_plan.coping_top = ["Super Skillz"]

        stability_plan.save()

        self.assertEqual(stability_plan.coping_top, [])

    def test_check_and_reduce_top_for_coping_top_some_removed(self):
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)

        stability_plan.coping_body = ["Bench Presses", "Wookie Walks"]
        stability_plan.coping_distract = None
        stability_plan.coping_help_others = []
        stability_plan.coping_courage = ["Super Skill"]
        stability_plan.coping_senses = ["creative listening"]
        stability_plan.supportive_people = [
            {"name": "The Name", "phone": "(777) 777-7777"}
        ]
        stability_plan.coping_top = [
            "Bench Presses",
            "Wookie Walks",
            "Creative Listening",
            "Super Skillz",
            # Expects parenthesis around number, so this should be removed.
            "The Name (777) 777-7777",
        ]

        stability_plan.save()

        self.assertEqual(
            stability_plan.coping_top, ["Bench Presses", "Wookie Walks"]
        )

    def test_check_and_reduce_top_for_coping_top_none_removed(self):
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)

        stability_plan.coping_body = ["first"]
        stability_plan.coping_distract = ["second"]
        stability_plan.coping_help_others = ["third"]
        stability_plan.coping_courage = ["fourth"]
        stability_plan.coping_senses = ["fifth", "and moar"]
        stability_plan.supportive_people = [
            {"name": "a", "phone": "(555) 555-5555"},
            {"name": "b", "phone": "(777) 777-7777"},
        ]
        stability_plan.coping_top = [
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "b ((777) 777-7777)",
        ]

        stability_plan.save()

        self.assertEqual(
            stability_plan.coping_top,
            ["first", "second", "third", "fourth", "fifth", "b ((777) 777-7777)"],
        )

    def test_check_and_reduce_top_for_ws_top_others_empty_or_null(self):
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)

        stability_plan.ws_stressors = []
        stability_plan.ws_thoughts = None
        stability_plan.ws_feelings = []
        stability_plan.ws_actions = None
        stability_plan.ws_top = []

        stability_plan.save()

        self.assertEqual(stability_plan.ws_top, [])

    def test_check_and_reduce_top_for_ws_top_some_removed(self):
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)

        stability_plan.ws_stressors = ["Bench Presses", "Road Runner Rumbles"]
        stability_plan.ws_thoughts = ["Super Skillz"]
        stability_plan.ws_feelings = None
        stability_plan.ws_actions = ["creative listening"]
        stability_plan.ws_top = [
            "creative listening",
            "Road Runner Rumbles",
            "Super Skill",
        ]

        stability_plan.save()

        self.assertEqual(
            stability_plan.ws_top, ["creative listening", "Road Runner Rumbles"]
        )

    def test_check_and_reduce_top_for_ws_top_none_removed(self):
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)

        stability_plan.ws_stressors = ["first"]
        stability_plan.ws_thoughts = ["second", "with", "some", "more"]
        stability_plan.ws_feelings = ["third"]
        stability_plan.ws_actions = ["fourth", "and more"]
        stability_plan.ws_top = ["first", "second", "third", "fourth"]

        stability_plan.save()

        self.assertEqual(
            stability_plan.ws_top, ["first", "second", "third", "fourth"]
        )

    supportive_people_validation_test_params = [
        ("", "Supportive people should either be `None` or a `list`."),
        ("Max", "Supportive people should either be `None` or a `list`."),
        (
            {"name": "Max", "phone": "(777) 777-7777"},
            "Supportive people should either be `None` or a `list`.",
        ),
        (
            [
                {"name": "David", "phone": "(777) 777-7777"},
                "Steve",
                {"name": "David", "phone": "(777) 777-7777"},
            ],
            "Supportive people index 1: Item should be a `dict`.",
        ),
        (
            [{"name": ["David"]}],
            "Supportive people index 0: The `name` should be a `str`.",
        ),
        (
            [{"name": "David", "phone": ["(777) 777-7777"]}],
            "Supportive people index 0: The `phone` should be a `str`.",
        ),
        (
            [{"name": "David", "phone": "7" * 22}],
            "Supportive people index 0: The `phone` can be at most 21 characters.",
        ),
    ]

    def test_validate_and_sanitize_supportive_people_validation(self):
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        for index, (value, error_message) in enumerate(
            self.supportive_people_validation_test_params
        ):
            with self.subTest(test_case=index), self.assertRaisesMessage(
                ValidationError, error_message
            ):
                stability_plan.supportive_people = value
                stability_plan.save()

    supportive_people_sanitization_test_params = [
        (None, None),
        ([], []),
        (
            [{"name": "", "phone": "777-777-7777"}],
            [{"name": "", "phone": "777-777-7777"}],
        ),
        (
            [{"name": None, "phone": "777-777-7777"}],
            [{"name": "", "phone": "777-777-7777"}],
        ),
        ([{"phone": "777-777-7777"}], [{"name": "", "phone": "777-777-7777"}]),
        ([{"name": "Fred", "phone": ""}], [{"name": "Fred", "phone": ""}]),
        ([{"name": "Steve", "phone": None}], [{"name": "Steve", "phone": ""}]),
        ([{"name": "Jubilee"}], [{"name": "Jubilee", "phone": ""}]),
        (
            [{"name": "Jubilee"}, {"phone": "777-777-7777"}],
            [{"name": "Jubilee", "phone": ""}, {"name": "", "phone": "777-777-7777"}],
        ),
        (
            [{"name": "Jubilee", "x": ["y"]}, {"phone": "777-777-7777", "a": "b"}],
            [{"name": "Jubilee", "phone": ""}, {"name": "", "phone": "777-777-7777"}],
        ),
        (
            [{"name": "Hippopawtamoose", "phone": "(777) 777-7777 x 7777"}],
            [{"name": "Hippopawtamoose", "phone": "(777) 777-7777 x 7777"}],
        ),
        (
            [
                {"name": "Hippopawtamoose", "phone": "(777) 777-7777 x 7777"},
                {"name": "", "phone": ""},
                {},
            ],
            [{"name": "Hippopawtamoose", "phone": "(777) 777-7777 x 7777"}],
        ),
    ]

    def test_validate_and_sanitize_supportive_people_sanitization(self):
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        for index, (value, sanitized_value) in enumerate(
            self.supportive_people_sanitization_test_params
        ):
            with self.subTest(test_case=index):
                stability_plan.supportive_people = value
                stability_plan.save()
                self.assertEqual(stability_plan.supportive_people, sanitized_value)

    def test_lethal_means_questions_returns_correct_section_uids(self):
        """ When a lethal means question is answered, the section uid is correct """

        self.encounter.save_answers({"rate_psych": 2})
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)


        self.create_action(
            patient=self.patient,
            encounter=self.encounter,
            action=ActionNames.ARRIVE,
            section_uid="reason_dont_want_to_talk_all",
        )


        self.assertEqual(
            self.encounter.current_section_uid, "reason_dont_want_to_talk_all"
        )

        suicide_assessment.answers = {"not_sure_talk_dec": "Skip for now"}
        suicide_assessment.save()

        self.assertEqual(
            self.encounter.current_section_uid, "reason_dont_want_to_talk_all"
        )

        self.create_action(
            patient=self.patient,
            encounter=self.encounter,
            action=ActionNames.ARRIVE,
            section_uid="reason_dont_want_to_talk_all_skip",
        )
        # not saving, to test save method on Action's relationship to patient_session.

        self.encounter.refresh_from_db()

        self.assertEqual(
            self.encounter.current_section_uid,
            "reason_dont_want_to_talk_all_skip",
        )

        self.create_action(
            patient=self.patient,
            encounter=self.encounter,
            action=ActionNames.MENU_SS,
        )
        self.encounter.save()

        self.assertEqual(
            self.encounter.current_section_uid,
            "reason_dont_want_to_talk_all_skip",
        )


class TestScoring(JasprTestCase):
    sheet_path = (
        settings.ROOT_DIR
        / "jaspr"
        / "apps"
        / "kiosk"
        / "tests"
        / "risk_stratification_test_examples.csv"
    )
    number_header = "test patient #"
    header_to_field = {
        "wish_live": "wish_live",
        "wish_die": "wish_die",
        "suicidal_yes_no": "suicidal_yes_no",
        "intent_yes_no": "intent_yes_no",
        "plan_yes_no": "plan_yes_no",
        "suicide_risk": "suicide_risk",
        "hospitalized_yes_no": "hospitalized_yes_no",
        "abuse_yes_no": "abuse_yes_no",
        "rate_agitation": "rate_agitation",
        "frustration0": "frustration0",
        "current_yes_no": "current_yes_no",
        "Score (0-6)": "scoring_score",
        "Current Attempt": "scoring_current_attempt",
        "Suicide Plan and Intent": "scoring_suicide_plan_and_intent",
        "Risk (low/mod/high)": "scoring_risk",
        "suicide_index_score": "scoring_suicide_index_score",
        "suicide_index_score_typology": "scoring_suicide_index_score_typology",
    }
    number_regex = re.compile(r"^-?[0-9]+$")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.system, cls.clinic, cls.department = cls.create_full_healthcare_system()

        cls.system.name = "Clinic One"
        cls.clinic.name = "Location One"
        cls.department.name = "Department One"
        cls.department.save()

        cls.sheet_data = {}
        with open(cls.sheet_path) as csv_file:
            reader = DictReader(csv_file)
            for row in reader:
                number = int(row.pop(cls.number_header))
                cls.sheet_data[number] = row

        assert (
            len(cls.sheet_data) >= 10
        ), "Pre-condition sanity check that there are >= 10 rows."

    @classmethod
    def check_and_transform_value(cls, value: str):
        v = value.strip()
        if v == "yes":
            return True
        if v == "no":
            return False
        if v == "-":
            return None
        if not v:
            return None
        if cls.number_regex.match(v):
            return int(v)
        return v

    # def test_rows_from_examples_sheet(self):
    #    patient_session = self.create_patient_encounter(department=self.department).get_current_session()
    #    assessment = Assessment.objects.filter(patient_session=patient_session).get()
    #    for number, row in self.sheet_data.items():
    #        with enter_transaction_then_roll_back(), self.subTest(
    #            sheet_test_patient_number=number
    #        ):
    #            seen_scoring_field = False
    #            for header_name, sheet_value in row.items():
    #                transformed_sheet_value = self.check_and_transform_value(
    #                    sheet_value
    #                )
    #                field_name = self.header_to_field[header_name.strip()]
    #                if field_name in Assessment.scoring_field_names:
    #                    if not seen_scoring_field:
    #                        seen_scoring_field = True
    #                        assessment.save()
    #                    field_value = getattr(assessment, field_name)
    #                    with self.subTest(
    #                        sheet_test_patient_number=number, field_name=field_name
    #                    ):
    #                        self.assertEqual(
    #                            field_value,
    #                            transformed_sheet_value,
    #                            f"Test Patient Number {number}: Field `{field_name}` saw "
    #                            f"{field_value} != {transformed_sheet_value}",
    #                        )
    #                else:
    #                    # The non-scoring fields should all come in the sheet before
    #                    # the scoring fields.
    #                    self.assertFalse(seen_scoring_field, "Pre-condition")
    #                    setattr(assessment, field_name, transformed_sheet_value)
