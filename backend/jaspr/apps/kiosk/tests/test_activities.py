from jaspr.apps.test_infrastructure.testcases import JasprTestCase
from jaspr.apps.kiosk.activities.activity_utils import ActivityType, ActivityStatus

class TestActivities(JasprTestCase):

    def setUp(self):
        super().setUp()

        self.system, self.clinic, self.department = self.create_full_healthcare_system()
        self.system.name = "Clinic One"
        self.clinic.name = "Location One"

        self.patient = self.create_patient(ssid="Test Patient 1")

        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )

    def test_activity_locking(self):
        self.encounter.add_activities([ActivityType.SuicideAssessment, ActivityType.StabilityPlan])
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        suicide_assessment.lock()
        self.assertTrue(suicide_assessment.locked)
        self.assertFalse(stability_plan.locked)
        suicide_assessment.unlock()
        self.assertFalse(suicide_assessment.locked)
        self.assertFalse(stability_plan.locked)

    def test_lock_section_sets_next_section_uid(self):
        self.encounter.add_activities([ActivityType.SuicideAssessment, ActivityType.StabilityPlan])
        self.assertIsNone(self.encounter.current_section_uid)
        self.encounter.save_answers({"rate_psych": 2})
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        self.assertEqual(self.encounter.current_section_uid, "rate_psych")
        suicide_assessment.lock()
        self.assertTrue(suicide_assessment.locked)
        self.assertEqual(self.encounter.current_section_uid, "make_home_start")

    def test_assigning_new_activity_keeps_patient_on_current_activity(self):
        self.encounter.add_activities([ActivityType.StabilityPlan])
        self.encounter.save_answers({"crisis_desc": "answer"})
        self.assertEqual(self.encounter.current_section_uid, "crisis_desc")
        self.encounter.add_activities([ActivityType.SuicideAssessment])
        self.assertEqual(self.encounter.current_section_uid, "crisis_desc")

    def test_assigning_new_activity_updates_current_section_uid_if_outro(self):
        """If the patient is in the middle of the outro when a new activity is assigned, set them to the first
        unanswered activity, otherwise they'll skip over it back to the outro because the outro will be moved to
        the end"""
        self.encounter.add_activities([ActivityType.StabilityPlan])
        self.encounter.save_answers({"distress1": 1})
        self.assertEqual(self.encounter.current_section_uid, "rate_distress1")
        self.encounter.add_activities([ActivityType.SuicideAssessment])
        self.assertEqual(self.encounter.current_section_uid, "start")

    def test_assigning_csa_before_assigned_csp_started(self):
        self.encounter.add_activities([ActivityType.StabilityPlan])
        self.encounter.save_answers({"distress0": 0})
        self.encounter.current_section_uid = "surviving_makes_sense"
        self.encounter.save()
        self.encounter.add_activities([ActivityType.SuicideAssessment])
        self.assertEqual(self.encounter.current_section_uid, "surviving_makes_sense")

    def test_assigning_csa_after_locking_csp(self):
        self.encounter.add_activities([ActivityType.StabilityPlan])
        self.encounter.save_answers({"distress0": 0})
        self.encounter.current_section_uid = "surviving_makes_sense"
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.lock()
        self.encounter.add_activities([ActivityType.SuicideAssessment])
        self.assertEqual(self.encounter.current_section_uid, "start")

    def test_saving_csp_as_takeaway_updates_status(self):
        """Saving the takeaway kit should update the CSP status to in-progress"""
        self.encounter.add_activities([ActivityType.SuicideAssessment, ActivityType.StabilityPlan])
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        self.assertEqual(stability_plan.assignedactivity.activity_status, str(ActivityStatus.NOT_STARTED))
        self.encounter.save_answers({"reasons_live": "My Dog"}, takeaway_kit=True)
        suicide_assessment.assignedactivity.refresh_from_db()
        stability_plan.assignedactivity.refresh_from_db()
        self.assertEqual(suicide_assessment.assignedactivity.activity_status, str(ActivityStatus.NOT_STARTED))
        self.assertEqual(stability_plan.assignedactivity.activity_status, str(ActivityStatus.IN_PROGRESS))
        self.assertIsNone(self.encounter.current_section_uid)

    def test_saving_takeaway_kit_does_not_impact_current_section_uid(self):
        """Saving the takeaway kit should not change the users place in the CUI"""
        self.assertIsNone(self.encounter.current_section_uid)
        self.encounter.add_activities([ActivityType.SuicideAssessment, ActivityType.StabilityPlan])
        self.encounter.save_answers({"rate_psych": 5})
        self.assertEqual(self.encounter.current_section_uid, "rate_psych")
        self.encounter.save_answers({"reasons_live": "My Dog"}, takeaway_kit=True)
        self.assertEqual(self.encounter.current_section_uid, "rate_psych")




