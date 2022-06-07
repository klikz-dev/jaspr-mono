"""Test operations on Patient"""
from copy import deepcopy

from jaspr.apps.jah.models import CrisisStabilityPlan, JAHAccount
from jaspr.apps.test_infrastructure.testcases import JasprTestCase
from jaspr.apps.kiosk.activities.activity_utils import ActivityType



class TestPatient(JasprTestCase):
    def setUp(self):
        super().setUp()

        self.department = self.create_department()

        self.patient = self.create_patient(department=self.department)
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.encounter.add_activities([ActivityType.StabilityPlan])

    def create_jah_account_and_copy_csp(self):
        jah_account = JAHAccount.objects.create(
            patient=self.encounter.patient
        )
        jah_csp = CrisisStabilityPlan.objects.create(jah_account=jah_account)

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        stability_plan.reasons_live = ["reason 1"]
        stability_plan.strategies_general = ["strategy 1"]
        stability_plan.means_support_yes_no = True
        stability_plan.coping_body = ["coping body 1"]
        stability_plan.ws_actions = ["action 1"]

        jah_csp_data = jah_csp.get_serializer()(stability_plan).data
        jah_csp_serializer = jah_csp.get_serializer()(jah_csp, data=jah_csp_data)
        jah_csp_serializer.is_valid(raise_exception=True)
        jah_csp_serializer.save()

        self.assertEqual(stability_plan.reasons_live, jah_csp.reasons_live)
        self.assertEqual(
            stability_plan.strategies_general, jah_csp.strategies_general
        )
        self.assertEqual(
            stability_plan.means_support_yes_no, jah_csp.means_support_yes_no
        )
        self.assertEqual(stability_plan.coping_body, jah_csp.coping_body)
        self.assertEqual(stability_plan.ws_actions, jah_csp.ws_actions)
