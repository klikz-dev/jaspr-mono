from datetime import timedelta
from typing import List, Dict
from freezegun import freeze_time
from django.utils import timezone

from jaspr.apps.kiosk.activities.activity_utils import ActivityType, ActivityStatus, IActivity
from jaspr.apps.kiosk.activities.question_json import generate_answers_from_questions, \
    generate_answers_from_question_list
from jaspr.apps.kiosk.constants import ActionNames
from jaspr.apps.kiosk.models import Encounter, Action, AssignmentLocks
from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class EncounterTestCase(JasprTestCase):
    fixtures = [
        "jaspr/apps/bootstrap/fixtures/jaspr_content.json",
    ]

    def setUp(self):
        super().setUp()
        self.department = self.create_department()
        self.patient = self.create_patient()
        self.encounter: Encounter = self.create_patient_encounter(patient=self.patient, department=self.department)

    def create_arrive_action(self, section_uid):
        specific_time = timezone.now()
        client_time = specific_time - timedelta(milliseconds=555)
        Action.objects.create(
            **{
                "patient": self.patient,
                "encounter": self.encounter,
                "in_er": True,
                "action": ActionNames.ARRIVE,
                # NOTE: `screen` and `extra` below are made up for this test. They may
                # or may not be actual/legit values that the frontend would send.
                "screen": "cui",
                "section_uid": section_uid,
                "timestamp": specific_time,
                "client_timestamp": client_time,
            }
        )

    def test_activity_statuses(self):
        activities = [
            ActivityType.SuicideAssessment,
            ActivityType.StabilityPlan,
            ActivityType.ComfortAndSkills
        ]
        self.encounter.add_activities(activities)
        self.assertEqual(self.encounter.assignedactivity_set.count(), 6)
        statuses = self.encounter.get_statuses()
        self.assertEqual(len(statuses), 6)
        self.assertEqual(statuses[0]["type"], str(ActivityType.Intro))
        self.assertEqual(statuses[0]["status"], str(ActivityStatus.NOT_STARTED))
        self.assertEqual(statuses[1]["type"], str(ActivityType.SuicideAssessment))
        self.assertEqual(statuses[1]["status"], str(ActivityStatus.NOT_STARTED))
        self.assertEqual(statuses[2]["type"], str(ActivityType.LethalMeans))
        self.assertEqual(statuses[2]["status"], str(ActivityStatus.NOT_STARTED))
        self.assertEqual(statuses[3]["type"], str(ActivityType.StabilityPlan))
        self.assertEqual(statuses[3]["status"], str(ActivityStatus.NOT_STARTED))
        self.assertEqual(statuses[4]["type"], str(ActivityType.ComfortAndSkills))
        self.assertEqual(statuses[4]["status"], str(ActivityStatus.ASSIGNED))
        self.assertEqual(statuses[5]["type"], str(ActivityType.Outro))
        self.assertEqual(statuses[5]["status"], str(ActivityStatus.NOT_STARTED))

    def test_activity_order_all(self):
        activities = [ActivityType.SuicideAssessment, ActivityType.StabilityPlan]
        self.encounter.add_activities(activities)
        self.assertEqual(self.encounter.assignedactivity_set.count(), 5)
        assigned_activities = self.encounter.filter_activities()
        self.assertEqual(assigned_activities[0].type, ActivityType.Intro)
        self.assertEqual(assigned_activities[1].type, ActivityType.SuicideAssessment)
        self.assertEqual(assigned_activities[2].type, ActivityType.LethalMeans)
        self.assertEqual(assigned_activities[3].type, ActivityType.StabilityPlan)
        self.assertEqual(assigned_activities[4].type, ActivityType.Outro)

    def test_activity_order_csp_first(self):
        self.encounter.add_activities([ActivityType.StabilityPlan])
        self.assertEqual(self.encounter.assignedactivity_set.count(), 4)
        assigned_activities = self.encounter.filter_activities()
        self.assertEqual(assigned_activities[0].type, ActivityType.Intro)
        self.assertEqual(assigned_activities[1].type, ActivityType.LethalMeans)
        self.assertEqual(assigned_activities[2].type, ActivityType.StabilityPlan)
        self.assertEqual(assigned_activities[3].type, ActivityType.Outro)

        self.encounter.add_activities([ActivityType.SuicideAssessment])
        self.encounter.refresh_from_db()
        self.assertEqual(self.encounter.assignedactivity_set.count(), 6)

        assigned_activities = self.encounter.filter_activities(active_only=True)
        self.assertEqual(assigned_activities[0].type, ActivityType.Intro)
        self.assertEqual(assigned_activities[1].type, ActivityType.LethalMeans)
        self.assertEqual(assigned_activities[2].type, ActivityType.StabilityPlan)
        self.assertEqual(assigned_activities[3].type, ActivityType.SuicideAssessment)
        self.assertEqual(assigned_activities[4].type, ActivityType.Outro)

    def test_explicit_activity(self):
        activities = [ActivityType.StabilityPlan, ActivityType.SuicideAssessment]
        self.encounter.add_activities(activities)
        explicit_activities = self.encounter.get_explicit_activities()
        self.assertEqual(len(explicit_activities), 2)
        # Note that if a CSP and CSA are assigned at the same time,
        # they get ordered with the CSA coming first and then the CSP
        self.assertEqual(explicit_activities[0].type, ActivityType.SuicideAssessment)
        self.assertEqual(explicit_activities[1].type, ActivityType.StabilityPlan)

    def test_explicit_activities_ordering(self):
        self.encounter.add_activities([ActivityType.StabilityPlan])
        self.encounter.add_activities([ActivityType.SuicideAssessment])
        explicit_activities = self.encounter.get_explicit_activities()
        self.assertEqual(len(explicit_activities), 2)
        # Note that activities assigned at different times retain their ordering
        self.assertEqual(explicit_activities[0].type, ActivityType.StabilityPlan)
        self.assertEqual(explicit_activities[1].type, ActivityType.SuicideAssessment)

    def test_activity_answers(self):
        expected = {
            "time_here": "Just got here",
            "distress0": 5,
            "frustration0": 5
        }
        activities = [ActivityType.StabilityPlan]
        self.encounter.add_activities(activities)

        self.create_arrive_action("set_security_image")

        self.encounter.refresh_from_db()

        self.encounter.save_answers(expected)

        # make sure the answers match
        result = self.encounter.get_answers()
        answers = result["answers"]
        self.assertEqual(expected["time_here"], answers["time_here"])
        self.assertEqual(expected["distress0"], answers["distress0"])
        self.assertEqual(expected["frustration0"], answers["frustration0"])

        # status
        statuses = self.encounter.get_statuses()
        self.assertEqual(statuses[0]["type"], str(ActivityType.Intro))
        self.assertEqual(statuses[0]["status"], str(ActivityStatus.IN_PROGRESS))
        self.assertEqual(statuses[1]["type"], str(ActivityType.LethalMeans))
        self.assertEqual(statuses[1]["status"], str(ActivityStatus.NOT_STARTED))

    def test_assigned_ssi_encounter(self):
        encounter = self.create_patient_encounter(department=self.department)
        encounter.add_activities([ActivityType.SuicideAssessment])
        suicide_assessment = encounter.get_activity(ActivityType.SuicideAssessment)
        lethal_means = encounter.get_activity(ActivityType.LethalMeans)

        self.assertEqual(suicide_assessment.get_status(), ActivityStatus.NOT_STARTED)
        self.assertEqual(lethal_means.get_status(), ActivityStatus.NOT_STARTED)

    def test_all_assigned_encounter(self):
        encounter = self.create_patient_encounter(department=self.department)
        encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        stability_plan = encounter.get_activity(ActivityType.StabilityPlan)
        suicide_assessment = encounter.get_activity(ActivityType.SuicideAssessment)
        lethal_means = encounter.get_activity(ActivityType.LethalMeans)

        self.assertEqual(suicide_assessment.get_status(), ActivityStatus.NOT_STARTED)
        self.assertEqual(lethal_means.get_status(), ActivityStatus.NOT_STARTED)
        self.assertEqual(stability_plan.get_status(), ActivityStatus.NOT_STARTED)

    def test_start_ssi_encounter(self):
        encounter = self.create_patient_encounter(department=self.department)
        encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])

        encounter.save_answers({
            "rate_psych": 4,
        })
        encounter.refresh_from_db()
        suicide_assessment = encounter.get_activity(ActivityType.SuicideAssessment)
        lethal_means = encounter.get_activity(ActivityType.LethalMeans)
        stability_plan = encounter.get_activity(ActivityType.StabilityPlan)

        self.assertEqual(suicide_assessment.get_status(), ActivityStatus.IN_PROGRESS)
        self.assertEqual(lethal_means.get_status(), ActivityStatus.NOT_STARTED)
        self.assertEqual(stability_plan.get_status(), ActivityStatus.NOT_STARTED)

    def test_start_lmc_encounter(self):
        encounter = self.create_patient_encounter(department=self.department)
        encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        stability_plan = encounter.get_activity(ActivityType.StabilityPlan)
        suicide_assessment = encounter.get_activity(ActivityType.SuicideAssessment)
        lethal_means = encounter.get_activity(ActivityType.LethalMeans)
        encounter.save_answers({
            "means_yes_no": True,
        })
        action = Action(
            patient=encounter.patient,
            encounter=encounter,
            in_er=True,
            action="Arrive",
            section_uid="means_describe_review",
            client_timestamp="2021-10-05"
        )
        action.save()

        suicide_assessment.refresh_from_db()
        lethal_means.refresh_from_db()
        stability_plan.refresh_from_db()
        self.assertEqual(suicide_assessment.get_status(), ActivityStatus.COMPLETED)
        self.assertEqual(lethal_means.get_status(), ActivityStatus.IN_PROGRESS)
        self.assertEqual(stability_plan.get_status(), ActivityStatus.NOT_STARTED)

    def test_start_csp_encounter(self):
        encounter = self.create_patient_encounter(department=self.department)
        encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])

        encounter.save_answers({
            "willing_to_talk": True,
        })
        action = Action(
            patient=encounter.patient,
            encounter=encounter,
            in_er=True,
            action="Arrive",
            section_uid="talk_it_through",
            client_timestamp="2021-10-05"
        )
        action.save()
        stability_plan = encounter.get_activity(ActivityType.StabilityPlan)
        suicide_assessment = encounter.get_activity(ActivityType.SuicideAssessment)
        lethal_means = encounter.get_activity(ActivityType.LethalMeans)

        self.assertEqual(suicide_assessment.get_status(), ActivityStatus.COMPLETED)
        self.assertEqual(lethal_means.get_status(), ActivityStatus.COMPLETED)
        self.assertEqual(stability_plan.get_status(), ActivityStatus.IN_PROGRESS)

    def test_completed_encounter(self):
        """
        wh
        :return:
        """

        encounter = self.create_patient_encounter(department=self.department)
        encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])

        encounter.save_answers({
            "willing_to_talk": True,
        })
        stability_plan = encounter.get_activity(ActivityType.StabilityPlan)
        suicide_assessment = encounter.get_activity(ActivityType.SuicideAssessment)
        lethal_means = encounter.get_activity(ActivityType.LethalMeans)
        action = Action(
            patient=encounter.patient,
            encounter=encounter,
            in_er=True,
            action="Arrive",
            section_uid="collect_email",
            client_timestamp="2021-10-05"
        )
        action.save()

        self.assertEqual(suicide_assessment.get_status(), ActivityStatus.COMPLETED)
        self.assertEqual(lethal_means.get_status(), ActivityStatus.COMPLETED)
        self.assertEqual(stability_plan.get_status(), ActivityStatus.IN_PROGRESS)

    def test_assessment_locked_encounter(self):
        """
        Check to see if a locked assessment causes CSP to switch to completed.
       :return:
        """

        encounter = self.create_patient_encounter(department=self.department)
        encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        encounter.save_answers({
            "willing_to_talk": True,
        })
        stability_plan = encounter.get_activity(ActivityType.StabilityPlan)
        suicide_assessment = encounter.get_activity(ActivityType.SuicideAssessment)
        lethal_means = encounter.get_activity(ActivityType.LethalMeans)
        action = Action(
            patient=encounter.patient,
            encounter=encounter,
            in_er=True,
            action="Arrive",
            section_uid="collect_email",
            client_timestamp="2021-10-05"
        )
        action.save()
        AssignmentLocks.objects.create(
            activity=stability_plan.get_assigned_activity(),
            locked=True
        )
        AssignmentLocks.objects.create(
            activity=suicide_assessment.get_assigned_activity(),
            locked=True
        )
        self.assertEqual(suicide_assessment.get_status(), ActivityStatus.COMPLETED)
        self.assertEqual(lethal_means.get_status(), ActivityStatus.COMPLETED)
        self.assertEqual(stability_plan.get_status(), ActivityStatus.COMPLETED)

    def test_csa_flow(self):
        activities = [
            ActivityType.SuicideAssessment,
        ]
        self.encounter.add_activities(activities)
        csa = self.encounter.get_activity(ActivityType.SuicideAssessment)
        questions = csa.get_questions()
        answer_keys = csa.get_answer_keys()
        answers = generate_answers_from_question_list(questions)
        self.encounter.save_answers(answers)
        csa.refresh_from_db()
        saved_answers = csa.get_answers()
        for key in answer_keys:
            self.assertEqual(answers[key], saved_answers[key], key)

    def test_full_answer_flow(self):
        activities = [
            ActivityType.StabilityPlan,
            ActivityType.SuicideAssessment,
            ActivityType.ComfortAndSkills
        ]
        self.encounter.add_activities(activities)
        #questions = self.encounter.get_questions()
        activities = self.encounter.filter_activities(active_only=True)
        answers = generate_answers_from_questions(activities)
        self.encounter.save_answers(answers)
        saved_answers = self.encounter.get_answers()
        for key in answers.keys():
            self.assertTrue(key in saved_answers["answers"])
            self.assertEqual(answers[key], saved_answers["answers"][key])

    def test_csp_is_not_started_when_lmc_completed(self):
        activities = [
            ActivityType.StabilityPlan,
        ]
        self.encounter.add_activities(activities)
        lmc_activity = self.encounter.get_activity(ActivityType.LethalMeans)
        answers = generate_answers_from_question_list(lmc_activity.get_questions())
        # print(answers)
        #self.encounter.save_answers(answers)
        answers = {'skip_lethal_means': "Yes, I'll think with you",
                   'skip_reason': 'I feel too depressed or overwhelmed', 'too_private_dec': "Yes, I'll think with you",
                   'overreact_specific': 'Keep me in hospital against my will',
                   'overreact_take_away_dec': "Yes, I'll think with you",
                   'overreact_keep_me_dec': "Yes, I'll think with you",
                   'reason_not_sure_talk': "I'm undecided if I want to kill myself",
                   'not_sure_talk_dec': 'Skip for now', 'too_shameful_dec': 'Skip for now',
                   'do_not_need_dec': "Yes, I'll think with you", 'cannot_rid_means_dec': "Yes, I'll think with you",
                   'stable_dec': 'Skip for now', 'keep_means_dec': 'Skip for now',
                   'keep_in_hospital_dec': "Yes, I'll think with you", 'feel_depressed_dec': 'Skip for now',
                   #'means_yes_no': True,
                   #'means_yes_no_describe': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec est ut sem pharetra euismod.',
                   'strategies_general': ['Dispose of method'], 'strategies_firearm': ['Locking device'],
                   # 'strategies_medicine': ['Locked up at home'], 'strategies_places': ['Avoid location'],
                   # 'strategies_other': ['Have list of emergency response and lifelines available'],
                   # 'strategies_custom': ['Go skiing', 'Go sailing', 'Go for a walk with my dog'],
                   #'means_support_yes_no': False,
                   # 'means_support_who': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec est ut sem pharetra euismod.',
                   # 'means_willing': 'Not willing'
                   #
                   }
        self.encounter.save_answers(answers)
        activities = self.encounter.filter_activities()

        statuses = self.encounter.get_statuses()
        self.assertEqual(len(statuses), 4)
        # Intro
        intro = statuses[0]
        self.assertEqual(intro["type"], str(ActivityType.Intro))
        self.assertEqual(intro["status"], str(ActivityStatus.COMPLETED))
        # LMC
        lmc = statuses[1]
        self.assertEqual(lmc["type"], str(ActivityType.LethalMeans))
        self.assertEqual(lmc["status"], str(ActivityStatus.IN_PROGRESS))

        # CSP
        csp = statuses[2]
        self.assertEqual(csp["type"], str(ActivityType.StabilityPlan))
        self.assertEqual(csp["status"], str(ActivityStatus.NOT_STARTED))
        # Outro
        outro = statuses[3]
        self.assertEqual(outro["type"], str(ActivityType.Outro))
        self.assertEqual(outro["status"], str(ActivityStatus.NOT_STARTED))

    def test_activity_modified_dates(self):
        activities = [
            ActivityType.StabilityPlan,
            ActivityType.SuicideAssessment
        ]

        # No activities assigned
        self.assertIsNone(self.encounter.activities_last_modified)
        self.encounter.add_activities(activities)

        # Activities assigned but not started
        self.assertIsNone(self.encounter.activities_last_modified)

        time1 = timezone.now()
        with freeze_time(time1):
            # Save CSP Answer
            self.encounter.save_answers({"coping_help_others": ["Do something kind"]})
            self.assertEqual(self.encounter.activities_last_modified, time1)
            stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
            self.assertEqual(time1, stability_plan.modified)

        time2 = timezone.now()
        with freeze_time(time2):
            # Save CSA Answer
            self.encounter.save_answers({'rate_psych': 0})
            self.assertEqual(self.encounter.activities_last_modified, time2)
            suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
            self.assertEqual(time2, suicide_assessment.modified)

        self.assertEqual(time2, suicide_assessment.modified)
