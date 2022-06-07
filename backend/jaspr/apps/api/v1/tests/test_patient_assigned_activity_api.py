from rest_framework import status
from jaspr.apps.kiosk.activities.activity_utils import ActivityType
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase

class TestPatientAssignedActivityAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.system, self.clinic, self.department = self.create_full_healthcare_system()
        self.patient = self.create_patient(department=self.department)
        self.encounter = self.create_patient_encounter(patient=self.patient, department=self.department)

        self.uri = f"/v1/patient/interview-activity"
        self.set_patient_creds(self.patient, in_er=True, encounter=self.encounter)


    def test_patient_lock_activity(self):

        self.encounter.add_activities([ActivityType.SuicideAssessment])
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        response = self.client.patch(self.uri + f"/{suicide_assessment.assignedactivity.pk}", {
            "locked": True
        })

        suicide_assessment.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["locked"])
        self.assertTrue(suicide_assessment.assignedactivity.locked)

    def test_patient_cannot_unlock_activity(self):
        self.encounter.add_activities([ActivityType.SuicideAssessment])
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        suicide_assessment.lock()
        response = self.client.patch(self.uri + f"/{suicide_assessment.assignedactivity.pk}", {
            "locked": False
        })

        suicide_assessment.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["locked"])
        self.assertTrue(suicide_assessment.assignedactivity.locked)
