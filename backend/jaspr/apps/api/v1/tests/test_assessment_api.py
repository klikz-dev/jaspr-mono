import os
import threading
import time
from datetime import timedelta

import before_after
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from freezegun import freeze_time
from rest_framework import status

from jaspr.apps.kiosk.models import (
    CopingStrategyCategory,
    PatientCopingStrategy,
    PatientMeasurements,
)
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import (
    JasprApiTestCase,
    JasprApiTransactionTestCase,
)
from jaspr.apps.kiosk.activities.activity_utils import ActivityType

from jaspr.apps.kiosk.activities.suicide_assessment.model import SuicideAssessmentActivity, SCORING_CURRENT_ATTEMPT, \
    SCORING_NO_CURRENT_ATTEMPT, SCORING_RISK_LOW, SCORING_RISK_MODERATE, SCORING_RISK_HIGH, \
    SCORING_SUICIDE_NO_PLAN_OR_INTENT, SCORING_SUICIDE_PLAN_OR_INTENT, SCORING_SUICIDE_PLAN_AND_INTENT, \
    SCORING_SUICIDE_INDEX_SCORE_WISH_TO_LIVE, SCORING_SUICIDE_INDEX_SCORE_AMBIVALENT, \
    SCORING_SUICIDE_INDEX_SCORE_WISH_TO_DIE


class TestPatientAnswersAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="patient/answers",
            version_prefix="v1",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Patient"]
        self.action_group_map["create"]["allowed_groups"] = ["Patient"]

        del self.action_group_map["partial_update"]
        del self.action_group_map["retrieve"]
        del self.action_group_map["update"]


class TestPatientAssessmentAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        self.uri = f"/v1/patient/answers"
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)

    def test_retrieve_assessment(self):
        """Does a get return the assessment and all fields?"""
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["metadata"]["current_section_uid"], None)

    def test_update_assessment(self):
        """Can the user add answers to assessment?"""
        data = {
            "time_here": "Just got here",
            "distress0": 4,
            "frustration0": 3,
            "rate_psych": 2,
        }
        now = timezone.now()
        response = self.client.patch(self.uri, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["answers"]["time_here"], "Just got here")
        self.assertEqual(response.data["answers"]["distress0"], 4)
        self.assertEqual(response.data["answers"]["frustration0"], 3)
        self.assertEqual(response.data["answers"]["rate_psych"], 2)
        # Implicitly under the hood is checking/making sure that `check_in_time0` has
        # been set because `distress0` and `frustration0` have been filled out. The two
        # assertions below assumes that behavior, which is required.
        self.assertGreaterEqual(parse_datetime(response.data["answers"]["check_in_time0"]), now)

        # No action has been saved to current_section_uid but we did set the question uid to the first question
        # in the first assigned activity
        self.assertEqual("ratePsych", response.data["metadata"]["current_section_uid"])

    def test_check_in_times_are_only_updated_by_backend(self):
        """
        Are the check in times only updated and handled by the backend
        (I.E. they shouldn't be exposed on the serializer)?
        """
        now = timezone.now()
        data0 = {"check_in_time0": now - timedelta(minutes=3, seconds=1)}
        response0 = self.client.patch(self.uri, data=data0)
        data1 = {"check_in_time1": now - timedelta(minutes=2, seconds=1)}
        response1 = self.client.patch(self.uri, data=data1)

        self.assertEqual(response0.status_code, 200)
        self.assertFalse("check_in_time0" in response0.data["answers"])
        self.assertEqual(response1.status_code, 200)
        self.assertFalse("check_in_time1" in response1.data["answers"])

        freeze_at = now - timedelta(minutes=1, seconds=1)
        data00 = {
            "distress0": 5,
            "frustration0": 4,
            "check_in_time0": freeze_at - timedelta(minutes=3, seconds=1),
        }
        data11 = {
            "distress1": 3,
            "frustration1": 3,
            "check_in_time1": freeze_at - timedelta(minutes=2, seconds=1),
        }

        with freeze_time(freeze_at):
            response00 = self.client.patch(self.uri, data=data00)
            response11 = self.client.patch(self.uri, data=data11)

        self.assertEqual(response00.status_code, 200)
        self.assertEqual(response00.data["answers"]["distress0"], 5)
        self.assertEqual(response00.data["answers"]["frustration0"], 4)
        self.assertEqual(parse_datetime(response00.data["answers"]["check_in_time0"]), freeze_at)
        self.assertEqual(response11.status_code, 200)
        self.assertEqual(response11.data["answers"]["distress1"], 3)
        self.assertEqual(response11.data["answers"]["frustration1"], 3)
        self.assertEqual(parse_datetime(response11.data["answers"]["check_in_time1"]), freeze_at)

    def test_measurement_records_created(self):
        """When a distressX or frustrationX attribute is set the first time, does an equivalent measurement record
        get created?"""

        # Measurement is not created until both distress and frustration are submitted
        data = {
            "distress0": 4,
        }
        response = self.client.patch(self.uri, data=data)
        patient_measurements = PatientMeasurements.objects.filter(
            encounter=self.encounter,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(patient_measurements), 0)

        data = {
            "distress0": 4,
            "frustration0": 3,
        }
        response = self.client.patch(self.uri, data=data)
        patient_measurements = PatientMeasurements.objects.filter(
            encounter=self.encounter,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(patient_measurements), 1)

        # Patient measurements for now are only created when the check_in time is set
        data = {
            "distress0": 4,
            "frustration0": 3,
        }
        response = self.client.patch(self.uri, data=data)

        patient_measurements = PatientMeasurements.objects.filter(
            encounter=self.encounter,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(patient_measurements), 1)

        # Additional measurements for later check-ins get recorded
        data = {
            "distress1": 4,
            "frustration1": 3,
        }
        response = self.client.patch(self.uri, data=data)

        patient_measurements = PatientMeasurements.objects.filter(
            encounter=self.encounter,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(patient_measurements), 2)

    def test_cannot_update_assessment_if_not_in_er(self):
        """Is the assessment only changeable if the Patient is in the ER?"""
        self.set_patient_creds(self.patient, encounter=self.encounter)
        data = {"time_here": "Just got here"}
        response = self.client.patch(self.uri, data=data)
        self.assertEqual(response.status_code, 403)

    # TODO JACOB Reenable after we have validation rules
    # def test_suicidal_freq_units_not_allowed_empty_string_or_null(self):
    #    """
    #    Is the user not allowed to create/update an assessment if
    #    `suicidal_freq_units` is specified as the empty string?
    #    """
    #    first_response = self.client.patch(self.uri, data={"suicidal_freq_units": ""})
    #    self.assertEqual(first_response.status_code, 400)
    #    self.assertIn("suicidal_freq_units", first_response.data)

    def test_valid_supportive_people(self):
        valid_supportive_people = [
            {"name": "Buggz Bunny", "phone": "14155552671"},
            {"name": "Daffy Duck", "phone": "415-555-2671"},
        ]
        response = self.client.patch(
            self.uri, data={"supportive_people": valid_supportive_people}
        )
        self.assertEqual(response.status_code, 200)
        expected_response_data = [
            {"name": "Buggz Bunny", "phone": "14155552671"},
            {"name": "Daffy Duck", "phone": "415-555-2671"},
        ]
        self.assertEqual(response.data["answers"]["supportive_people"], expected_response_data)

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.refresh_from_db()
        self.assertEqual(
            stability_plan.supportive_people,
            expected_response_data,
        )

    def test_weirdly_valid_supportive_people(self):
        # Dropped a number off of the phone number in two different ways
        # to test and see if the serializer(s) catch (and raise) the error.
        weirdly_valid_supportive_people = [
            {"name": "Buggz Bunny", "phone": ""},  # Should be valid.
            {"name": "", "phone": "415-555-2671"},  # Should be valid as well.
        ]
        response = self.client.patch(
            self.uri, data={"supportive_people": weirdly_valid_supportive_people}
        )
        self.assertEqual(response.status_code, 200, response.data)

        self.assertEqual(
            response.data["answers"]["supportive_people"], weirdly_valid_supportive_people
        )

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.refresh_from_db()

        self.assertEqual(
            stability_plan.supportive_people,
            weirdly_valid_supportive_people,
        )

    def test_invalid_supportive_people_all_blank(self):
        invalid_supportive_people = [{"name": "", "phone": ""}]
        response = self.client.patch(
            self.uri, data={"supportive_people": invalid_supportive_people}
        )
        self.assertEqual(response.status_code, 400, response.data)
        self.assertEqual(
            response.data["supportive_people"],
            ["Must provide at least one of name or phone number."],
        )

    def test_invalid_supportive_people_wrong_data_type(self):
        invalid_supportive_people = ({"name": "", "phone": ""},)
        response = self.client.patch(
            self.uri, data={"supportive_people": invalid_supportive_people}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("supportive_people", response.data)

    def test_valid_custom_strategies(self):
        valid_custom_strategies = ["I love squirrels.", "Puppies are the best!"]
        response = self.client.patch(
            self.uri, data={"strategies_custom": valid_custom_strategies}
        )
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data["answers"]["strategies_custom"], valid_custom_strategies)
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        self.assertEqual(
            stability_plan.strategies_custom, valid_custom_strategies
        )

    ## TODO FIX BEFORE GO LIVE
    # def test_invalid_custom_strategies_empty_item(self):
    #     invalid_custom_strategies = ["I love squirrels.", "", "Puppies are the best!"]
    #     response = self.client.patch(
    #         self.uri, data={"strategies_custom": invalid_custom_strategies}
    #     )
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("strategies_custom", response.data["answers"])

    ## TODO FIX BEFORE RELEASE
    # def test_invalid_custom_strategies_wrong_data_type(self):
    #     invalid_custom_strategies = "I am a string, not a list."
    #     response = self.client.patch(
    #         self.uri, data={"strategies_custom": invalid_custom_strategies}
    #     )
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn("strategies_custom", response.data["answers"])

    def test_custom_coping_body_entries_create_custom_coping_strategies(self):
        """ Do PatientCopingStrategy records get made when custom coping strategies are entered?"""

        physical_category = self.create_coping_strategy_category(
            name="Do things with your body", slug="physical"
        )
        known_coping_skill = self.create_coping_strategy(
            title="known skill, pre-existing", category=physical_category
        )
        response = self.client.patch(
            self.uri,
            data={
                "coping_body": [known_coping_skill.title, "New physical coping skill"]
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.refresh_from_db()
        custom_coping_strategies = PatientCopingStrategy.objects.filter(
            encounter=self.encounter, category=physical_category
        )
        self.assertEqual(custom_coping_strategies.count(), 1)
        new_strategy = custom_coping_strategies.first()
        self.assertEqual(
            stability_plan.coping_body,
            [known_coping_skill.title, new_strategy.title],
        )

    def test_custom_coping_body_entries_get_marked_archived_if_unused(self):
        """ Do unused PatientCopingStrategy records get marked archived when coping strategies are updated?"""

        physical_category = self.create_coping_strategy_category(
            name="Do things with your body", slug="physical"
        )

        existing_patient_coping_strategy = self.create_kiosk_patient_coping_strategy(
            encounter=self.encounter,
            category=physical_category,
            title="pre-existing custom strategy",
        )
        known_coping_skill = self.create_coping_strategy(
            title="known skill, pre-existing", category=physical_category
        )

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.coping_body = [
            known_coping_skill.title,
            existing_patient_coping_strategy.title,
        ]
        stability_plan.save()

        # now PATCH without custom coping strategy.
        response = self.client.patch(
            self.uri,
            data={"coping_body": [known_coping_skill.title]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        existing_patient_coping_strategy.refresh_from_db()
        custom_coping_strategies = PatientCopingStrategy.objects.filter(
            encounter=self.encounter, category=physical_category, status="archived"
        )
        self.assertEqual(custom_coping_strategies.count(), 1)
        archived_patient_strategy = custom_coping_strategies.first()
        self.assertEqual(existing_patient_coping_strategy, archived_patient_strategy)

        stability_plan.refresh_from_db()
        self.assertEqual(
            stability_plan.coping_body,
            [known_coping_skill.title],
        )

    def test_custom_coping_body_entries_get_ignored_if_already_present(self):
        """ Do pre-existing PatientCopingStrategy records get ignored when other coping strategies are updated??"""

        physical_category = self.create_coping_strategy_category(
            name="Do things with your body", slug="physical"
        )

        existing_patient_coping_strategy = self.create_kiosk_patient_coping_strategy(
            encounter=self.encounter,
            category=physical_category,
            title="pre-existing custom strategy",
        )
        known_coping_skill = self.create_coping_strategy(
            title="known skill, pre-existing", category=physical_category
        )
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.coping_body = [
            known_coping_skill.title,
            existing_patient_coping_strategy.title,
        ]
        stability_plan.save()

        # now PATCH without custom coping strategy.
        response = self.client.patch(
            self.uri,
            data={"coping_body": [existing_patient_coping_strategy.title]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        existing_patient_coping_strategy.refresh_from_db()
        custom_coping_strategies = PatientCopingStrategy.objects.filter(
            encounter=self.encounter, category=physical_category, status="active"
        )
        self.assertEqual(custom_coping_strategies.count(), 1)
        self.assertEqual(
            existing_patient_coping_strategy, custom_coping_strategies.first()
        )

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.refresh_from_db()
        self.assertEqual(
            stability_plan.coping_body,
            [existing_patient_coping_strategy.title],
        )

    def test_coping_top_does_not_mark_patient_coping_strategies_archived_inapproriately(
        self,
    ):
        """ when ranked, are Patient Coping Strategies left active?"""

        physical_category = self.create_coping_strategy_category(
            name="Do things with your body", slug="physical"
        )

        existing_patient_coping_strategy = self.create_kiosk_patient_coping_strategy(
            encounter=self.encounter,
            category=physical_category,
            title="pre-existing custom strategy",
        )

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.coping_body = [
            existing_patient_coping_strategy.title,
        ]
        stability_plan.save()

        # now PATCH coping_body.
        response = self.client.patch(
            self.uri,
            data={"coping_top": [existing_patient_coping_strategy.title]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        existing_patient_coping_strategy.refresh_from_db()
        self.assertEqual(existing_patient_coping_strategy.status, "active")

    def test_coping_body_accepts_empty_list(self):
        """ Does system delete when an empty list is patched?"""

        physical_category = self.create_coping_strategy_category(
            name="Do things with your body", slug="physical"
        )

        known_coping_skill = self.create_coping_strategy(
            title="known skill, pre-existing", category=physical_category
        )

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.coping_body = [
            known_coping_skill.title,
        ]
        stability_plan.save()

        # now PATCH coping_body with empty list.
        response = self.client.patch(
            self.uri,
            data={"coping_body": []},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        stability_plan.refresh_from_db()
        self.assertEqual(stability_plan.coping_body, [])

    def test_patient_coping_strategies_can_be_archived_and_reactivated(self):
        """ Can a patient coping strategy be removed and then recreated/re-used?"""
        physical_category = self.create_coping_strategy_category(
            name="Do things with your body", slug="physical"
        )

        archived_patient_coping_strategy = self.create_kiosk_patient_coping_strategy(
            encounter=self.encounter,
            category=physical_category,
            title="archived custom strategy",
            status="archived",
        )

        # now PATCH coping_body
        response = self.client.patch(
            self.uri,
            data={"coping_body": [archived_patient_coping_strategy.title]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        archived_patient_coping_strategy.refresh_from_db()
        stability_plan.refresh_from_db()
        self.assertEqual(
            stability_plan.coping_body,
            [archived_patient_coping_strategy.title],
        )
        self.assertEqual(archived_patient_coping_strategy.status, "active")

    def test_patient_coping_strategies_can_be_archived_without_setting_others_to_archived(
        self,
    ):
        """ Can a patient coping strategy be archived without archiving others?"""
        physical_category = self.create_coping_strategy_category(
            name="Do things with your body", slug="physical"
        )

        active_patient_coping_strategy = self.create_kiosk_patient_coping_strategy(
            encounter=self.encounter,
            category=physical_category,
            title="active custom strategy",
            status="active",
        )

        changing_patient_coping_strategy = self.create_kiosk_patient_coping_strategy(
            encounter=self.encounter,
            category=physical_category,
            title="soon to be archived custom strategy",
            status="active",
        )

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.coping_body = [
            active_patient_coping_strategy.title,
            changing_patient_coping_strategy.title,
        ]
        stability_plan.save()

        # now PATCH coping_body
        response = self.client.patch(
            self.uri,
            data={"coping_body": [active_patient_coping_strategy.title]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        active_patient_coping_strategy.refresh_from_db()
        changing_patient_coping_strategy.refresh_from_db()
        stability_plan.refresh_from_db()
        self.assertEqual(
            stability_plan.coping_body,
            [active_patient_coping_strategy.title],
        )
        self.assertEqual(active_patient_coping_strategy.status, "active")
        self.assertEqual(changing_patient_coping_strategy.status, "archived")

    def test_new_patient_coping_strategy_with_different_category_can_be_created_without_archiving_first(
        self,
    ):
        """ Can two patient coping strategies with different categories be created without archiving first?"""
        physical_category = self.create_coping_strategy_category(
            name="Do things with your body", slug="physical"
        )

        physical_coping_strategy = self.create_kiosk_patient_coping_strategy(
            encounter=self.encounter,
            category=physical_category,
            title="physical coping strategy",
            status="active",
        )

        distract_category = self.create_coping_strategy_category(
            name="Do things to distract yourself.", slug="distract"
        )

        distract_coping_strategy = self.create_kiosk_patient_coping_strategy(
            encounter=self.encounter,
            category=distract_category,
            title="distract coping strategy",
            status="active",
        )

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.coping_body = [
            physical_coping_strategy.title,
        ]
        stability_plan.save()

        # now PATCH coping_body
        response = self.client.patch(
            self.uri,
            data={"coping_distract": [distract_coping_strategy.title]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        stability_plan.refresh_from_db()
        self.assertEqual(
            stability_plan.coping_body,
            [
                physical_coping_strategy.title,
            ],
        )
        self.assertEqual(
            stability_plan.coping_distract,
            [
                distract_coping_strategy.title,
            ],
        )
        physical_coping_strategy.refresh_from_db()
        self.assertEqual(physical_coping_strategy.status, "active")

        distract_coping_strategy.refresh_from_db()
        self.assertEqual(distract_coping_strategy.status, "active")

    def test_scoring_included_and_read_only(self):
        """Is the scoring included in the response and read-only?"""

        self.encounter.save_answers({
            "wish_live": 4,
            "wish_die": 1,
        })

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        self.assertIs(suicide_assessment.scoring_score, None, "Pre-condition")
        self.assertIs(
            suicide_assessment.scoring_current_attempt, None, "Pre-condition"
        )
        self.assertIs(
            suicide_assessment.scoring_suicide_plan_and_intent, None, "Pre-condition"
        )
        self.assertIs(suicide_assessment.scoring_risk, None, "Pre-condition")

        self.assertEqual(
            suicide_assessment.scoring_suicide_index_score,
            1,
            (
                "Pre-condition, populating at least one aspect of the scoring. Can "
                "update this if it goes out of date.",
            ),
        )
        self.assertEqual(
            suicide_assessment.scoring_suicide_index_score_typology,
            SCORING_SUICIDE_INDEX_SCORE_WISH_TO_LIVE,
            "Pre-condition",
        )
        patch_response = self.client.patch(
            self.uri,
            data={
                "scoring_score": 3,
                "scoring_current_attempt": SCORING_NO_CURRENT_ATTEMPT,
                "scoring_suicide_plan_and_intent": SCORING_SUICIDE_PLAN_OR_INTENT,
                "scoring_risk": SCORING_RISK_MODERATE,
                "scoring_suicide_index_score": 0,
                "scoring_suicide_index_score_typology": SCORING_SUICIDE_INDEX_SCORE_AMBIVALENT,
            },
        )

        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.encounter.refresh_from_db()

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        self.assertIs(suicide_assessment.scoring_score, None)
        self.assertIs(suicide_assessment.scoring_current_attempt, None)
        self.assertIs(suicide_assessment.scoring_suicide_plan_and_intent, None)
        self.assertIs(suicide_assessment.scoring_risk, None)
        self.assertEqual(suicide_assessment.scoring_suicide_index_score, 1)
        self.assertEqual(
            suicide_assessment.scoring_suicide_index_score_typology,
            SCORING_SUICIDE_INDEX_SCORE_WISH_TO_LIVE,
        )

        get_response = self.client.get(self.uri)
        self.assertIs(get_response.data["metadata"]["scoring_score"], None)
        self.assertIs(get_response.data["metadata"]["scoring_current_attempt"], None)
        self.assertIs(get_response.data["metadata"]["scoring_suicide_plan_and_intent"], None)
        self.assertIs(get_response.data["metadata"]["scoring_risk"], None)
        self.assertEqual(get_response.data["metadata"]["scoring_suicide_index_score"], 1)
        self.assertEqual(
            get_response.data["metadata"]["scoring_suicide_index_score_typology"],
            SCORING_SUICIDE_INDEX_SCORE_WISH_TO_LIVE,
        )


class TestAssessmentAPIConcurrencyHandling(JasprApiTransactionTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        self.uri = f"/v1/patient/answers"
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)

    def test_concurrent_updates_assessment(self):
        """
        Simulates close to a race condition (just using a single worker/thread/etc.),
        but not exactly because `before_after` uses a single thread, so this doesn't
        actually test the `select_for_update` race condition, but it does test what
        would happen if two threads were really close to patching at the same time,
        making sure the assessment is refreshed before updating (and we can hand/eye
        verify we used `select_for_update`).
        """
        data1 = {"rate_psych": 4}
        data2 = {"rate_stress": 3}

        def run_before(*a, **k):
            response = self.client.patch(self.uri, data=data2)
            self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        with before_after.before(
            "jaspr.apps.kiosk.activities.manager.ActivityManagerMixin.save_answers",
            run_before,
        ):
            response = self.client.patch(self.uri, data=data1)
            self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        answers = self.encounter.get_answers()

        self.assertEqual(answers["answers"]["rate_psych"], 4)
        self.assertEqual(answers["answers"]["rate_stress"], 3)
