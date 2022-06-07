import before_after
from django.utils import timezone
from rest_framework import status

from jaspr.apps.kiosk.constants import ActionNames
from jaspr.apps.kiosk.models import Action
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import (
    JasprApiTestCase,
    JasprApiTransactionTestCase,
)
from jaspr.apps.kiosk.activities.activity_utils import ActivityType


class TestPatientActionAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(patient=self.patient)

        super().setUp(
            resource_pattern="patient/action",
            version_prefix="v1",
            factory_name="create_action",
            encounter=self.encounter
        )

        self.action_group_map["create"]["allowed_groups"] = ["Patient"]


class TestPatientActionAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/action"

        self.system, self.clinic, self.department = self.create_full_healthcare_system()

        self.patient = self.create_patient(department=self.department)
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        self.set_patient_creds(self.patient, encounter=self.encounter)

    def test_valid_action_without_section_uid(self):
        """Can an authenticated patient post a valid action without a section uid?"""
        initial_time = timezone.now()
        response = self.client.post(
            self.uri,
            data={"action": ActionNames.EXPLORE, "client_timestamp": initial_time},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data)

        action = Action.objects.select_related("patient").get(
            action=ActionNames.EXPLORE
        )
        self.assertEqual(action.patient, self.patient)
        # Since we're using `self.set_creds`, which does a regular login, we won't be
        # in the ER.
        self.assertEqual(action.in_er, False)
        self.assertEqual(action.screen, "")
        self.assertEqual(action.extra, "")
        self.assertEqual(action.section_uid, "")
        self.assertGreater(action.timestamp, initial_time)
        self.assertEqual(action.client_timestamp, initial_time)

    def test_valid_action_with_section_uid(self):
        """Can an authenticated patient post a valid action with a section uid?"""
        initial_time = timezone.now()
        response = self.client.post(
            self.uri,
            data={
                "action": ActionNames.SUBMIT,
                "section_uid": [*self.encounter.sections_dictionary][-1],
                "client_timestamp": initial_time,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data)

        action = Action.objects.select_related("patient").get(action=ActionNames.SUBMIT)
        self.assertEqual(action.patient, self.patient)
        self.assertEqual(action.in_er, False)
        self.assertEqual(action.screen, "")
        self.assertEqual(action.extra, "")
        self.assertEqual(
            action.section_uid, [*self.encounter.sections_dictionary][-1]
        )
        self.assertGreater(action.timestamp, initial_time)
        self.assertEqual(action.client_timestamp, initial_time)

    def test_valid_action_with_camel_cased_section_uid(self):
        """Can an authenticated patient post a valid action with a camel cased section uid?"""
        initial_time = timezone.now()
        response = self.client.post(
            self.uri,
            data={
                "action": ActionNames.SUBMIT,
                "section_uid": "reasonsLiveDie",
                "client_timestamp": initial_time,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertIsNone(response.data)

        action = Action.objects.select_related("patient").get(action=ActionNames.SUBMIT)
        self.assertEqual(action.patient, self.patient)
        self.assertEqual(action.in_er, False)
        self.assertEqual(action.screen, "")
        self.assertEqual(action.extra, "")
        self.assertEqual(action.section_uid, "reasons_live_die")
        self.assertGreater(action.timestamp, initial_time)
        self.assertEqual(action.client_timestamp, initial_time)

    def test_valid_action_with_section_uid_trailing_number(self):
        """Can an authenticated patient post a valid action with camel cased section uid with a trailing number?"""
        initial_time = timezone.now()
        response = self.client.post(
            self.uri,
            data={
                "action": ActionNames.SUBMIT,
                "section_uid": "viewCard1",
                "client_timestamp": initial_time,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertIsNone(response.data)

        action = Action.objects.select_related("patient").get(action=ActionNames.SUBMIT)
        self.assertEqual(action.patient, self.patient)
        self.assertEqual(action.in_er, False)
        self.assertEqual(action.screen, "")
        self.assertEqual(action.extra, "")
        self.assertEqual(action.section_uid, "view_card1")
        self.assertGreater(action.timestamp, initial_time)
        self.assertEqual(action.client_timestamp, initial_time)

    def test_section_uid_validation_when_not_provided(self):
        """
        Does an action that needs a section uid that doesn't have a section uid get
        correctly invalidated?
        """
        initial_time = timezone.now()
        response = self.client.post(
            self.uri,
            data={"action": ActionNames.ARRIVE, "client_timestamp": initial_time},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            f"A section uid is required with action {ActionNames.ARRIVE}.",
            response.data["non_field_errors"][0],
        )

    def test_valid_action_that_requires_extra(self):
        """Can an authenticated patient post a valid action that requires extra?"""
        initial_time = timezone.now()
        response = self.client.post(
            self.uri,
            data={
                "action": ActionNames.WATCH,
                # NOTE: This is a made up "screen" and "extra" value and is not
                # necessarily something the frontend would send exactly (I.E. there is
                # a puppies video but that might not be the exact name). Currently same
                # for the other tests too at the time of writing.
                "screen": "Walkthrough",
                "extra": "puppies",
                "client_timestamp": initial_time,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data)

        action = Action.objects.select_related("patient").get(action=ActionNames.WATCH)
        self.assertEqual(action.patient, self.patient)
        self.assertEqual(action.in_er, False)
        self.assertEqual(action.screen, "Walkthrough")
        self.assertEqual(action.extra, "puppies")
        self.assertEqual(action.section_uid, "")
        self.assertGreater(action.timestamp, initial_time)
        self.assertEqual(action.client_timestamp, initial_time)

    def test_jah_action_invalid_when_extra_required_but_not_set(self):
        """
        Does an action that requires extra get correctly invalidated if extra is not
        provided?
        """
        initial_time = timezone.now()
        response = self.client.post(
            self.uri,
            data={
                "action": ActionNames.WATCH,
                "client_timestamp": initial_time,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            f"The `extra` field is required for action Watch.",
            response.data["non_field_errors"][0],
        )

    def test_jah_action_invalid_when_patient_in_er(self):
        """
        Does an action that requires JAH get correctly invalidated if the
        authenticated patient is in the ER?
        """
        self.set_patient_creds(self.patient, in_er=True)
        initial_time = timezone.now()
        response = self.client.post(
            self.uri,
            data={
                "action": ActionNames.JAH_ARRIVE_SS_SUPPORTIVE_PEOPLE,
                "client_timestamp": initial_time,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            f"Must not be in the ER (JAH required) for action JAHArriveSSSupportivePeople.",
            response.data["non_field_errors"][0],
        )

    def test_jah_action_section_uid_onboard(self):
        """Can an authenticated patient post a valid jah onboarding section id?"""
        initial_time = timezone.now()
        response = self.client.post(
            self.uri,
            data={
                "action": ActionNames.ARRIVE,
                "section_uid": "jahOnboardDisclaimer",
                "client_timestamp": initial_time,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertIsNone(response.data)

        action = Action.objects.select_related("patient").get(action=ActionNames.ARRIVE)
        self.assertEqual(action.patient, self.patient)
        self.assertEqual(action.in_er, False)
        self.assertEqual(action.screen, "")
        self.assertEqual(action.extra, "")
        self.assertEqual(action.section_uid, "jah_onboard_disclaimer")
        self.assertGreater(action.timestamp, initial_time)
        self.assertEqual(action.client_timestamp, initial_time)


class TestArriveActionPatientInterviewProgressSectionUpdating(
    JasprApiTransactionTestCase
):

    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/action"

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        self.patient.refresh_from_db()
        self.set_patient_creds(self.patient, encounter=self.encounter)



class TestArriveActionAssessmentCurrentSectionUidUpdating(JasprApiTransactionTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient()
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])

        self.answers_uri = f"/v1/patient/answers"
        self.create_action_uri = "/v1/patient/action"
        self.set_patient_creds(
            self.patient, in_er=True, from_native=False, encounter=self.encounter
        )

    def test_assessment_patch_happens_before_arrive(self):

        Action.objects.create(
            action=ActionNames.ARRIVE,
            section_uid="rate_stress_text",
            patient=self.encounter.patient,
            encounter=self.encounter,
            in_er=True,
        )

        self.encounter.save_answers({"most_stress": "Skunks"})
        # Check that some assumptions hold at this point. If questions/sections change
        # around we may need to update these tests.
        self.assertEqual(self.encounter.get_current_section_uid(), "rateStressText")

        def run_before_arrive(*a, **k):
            response = self.client.patch(
                self.answers_uri,
                data={"shame_yes_no": True, "shame_yes_no_describe": "Squirrels"},
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data["answers"]["shame_yes_no"])
            self.assertEqual(response.data["answers"]["shame_yes_no_describe"], "Squirrels")
            self.assertEqual(response.data["metadata"]["current_section_uid"], "shameDescribe")

        with before_after.before(
            "jaspr.apps.kiosk.models.Action.save", run_before_arrive
        ):
            response = self.client.post(
                self.create_action_uri,
                data={"action": ActionNames.ARRIVE, "section_uid": "ssfaFinish"},
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.encounter.save()

        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)

        suicide_assessment.refresh_from_db()
        answers = self.encounter.get_answers()

        self.assertTrue(answers["answers"]["shame_yes_no"])
        self.assertEqual(answers["answers"]["shame_yes_no_describe"], "Squirrels")

        ## TODO FIX BEFORE RELEASE
        # self.assertEqual(self.encounter.current_section_uid, "ssfaFinish")
        # # Should be four records:
        # # 1. Creation
        # # 2. Assign SRAT and CSP
        # # 3. Initial modification at the top of the tests.
        # # 4. PATCH
        # # 5. rate_psych_section_viewed Update <-- Would love to get rid of this extra history
        # # 6. Action being created and updating `current_section_uid`.
        # # TODO JACOB Update description ^
        # self.assertEqual(suicide_assessment.history.count(), 3)
        # self.assertEqual(suicide_assessment.history.count(), 11)

    ## TODO FIX BEFORE RELEASE
    # def test_assessment_patch_happens_after_arrive(self):
    #     self.encounter.save_answers({"most_stress": "Skunks"})
    #     # Check that some assumptions hold at this point. If questions/sections change
    #     # around we may need to update these tests.
    #     suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
    #     self.assertEqual(self.encounter.current_section_uid, "rate_stress_text")
    #
    #     def run_after_arrive(*a, **k):
    #         response = self.client.patch(
    #             self.answers_uri,
    #             data={"shame_yes_no": True, "shame_yes_no_describe": "Squirrels"},
    #         )
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertTrue(response.data["answers"]["shame_yes_no"])
    #         self.assertEqual(response.data["answers"]["shame_yes_no_describe"], "Squirrels")
    #         self.assertEqual(response.data["metadata"]["current_section_uid"], "ssfaFinish")
    #
    #     with before_after.after(
    #         "jaspr.apps.kiosk.models.Action.save", run_after_arrive
    #     ):
    #         response = self.client.post(
    #             self.create_action_uri,
    #             data={"action": ActionNames.ARRIVE, "section_uid": "ssfaFinish"},
    #         )
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    #
    #     answers = self.encounter.get_answers()
    #     self.assertTrue(answers["answers"]["shame_yes_no"])
    #     self.assertEqual(answers["answers"]["shame_yes_no_describe"], "Squirrels")
    #     self.assertEqual(self.encounter.current_section_uid, "ssfa_finish")
    #     # Should be five records:
    #     # 1. Creation
    #     # 2. Assign SRAT and CSP
    #     # 3. Initial modification at the top of the tests.
    #     # 4. Action being created and updating `current_section_uid`.
    #     # 5. PATCH
    #     # 6. rate_psych_section_viewed Update <-- Would love to get rid of this extra history
    #
    #     ## TODO Review 4 new queries
    #     self.assertEqual(self.encounter.history.count(), 10)
    #
    #     # Should be three records:
    #     # 1. Creation
    #     # 2. Extra save called in save method to calculate scores.
    #     # 4. PATCH
    #
    #     self.assertEqual(suicide_assessment.history.count(), 3)


'''
class TestUpdateRatePsychSectionViewed(JasprApiTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/action"
        self.patient = self.create_patient()
        self.assessment = self.create_assessment(patient=self.patient)
        self.set_patient_creds(self.patient)

    def test_update_rate_psych_section_viewed_first(self):
        """When an ARRIVAL is registered for rate_psych, is rate_psych_section_viewed set?"""

        now = timezone.now()

        with freeze_time(now):

            response = self.client.post(
                self.uri,
                data={
                    "action": ActionNames.ARRIVE,
                    "client_timestamp": now.isoformat(),
                    "section_uid": "rate_psych",
                },
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertIsNone(response.data)

        action = Action.objects.select_related("patient").get(action=ActionNames.ARRIVE)
        self.assertEqual(
            now, action.patient.current_assessment.rate_psych_section_viewed
        )
'''
