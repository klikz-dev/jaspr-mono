from rest_framework import status
from jaspr.apps.kiosk.activities.activity_utils import ActivityType
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase

class TestTechnicianAssignedActivityAPIRetrieve(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.technician = self.create_technician()
        self.department_technician = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            ).get(department__name="unassigned")
        )
        self.department = self.department_technician.department
        self.clinic = self.department.clinic
        self.patient = self.create_patient()
        self.create_patient_department_sharing(
            department=self.department,
            patient=self.patient
        )
        self.encounter = self.create_patient_encounter(
            department=self.department,
            patient=self.patient
        )

        self.uri = f"/v1/technician/encounter/{self.encounter.pk}/activities"
        self.set_technician_creds(self.technician)

    def test_gets_activities_in_correct_order(self):
        """ Does the tech get actvities in the right order?"""
        self.encounter.add_activities([
            ActivityType.SuicideAssessment,
            ActivityType.StabilityPlan,
            ActivityType.ComfortAndSkills
        ])
        response = self.client.get(self.uri)
        activities = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(activities), 3)
        self.assertEqual(activities[0]["type"], str(ActivityType.SuicideAssessment))
        self.assertEqual(activities[1]["type"], str(ActivityType.StabilityPlan))
        self.assertEqual(activities[2]["type"], str(ActivityType.ComfortAndSkills))

    def test_gets_activities_with_multiple_csps(self):
        """ Does the tech get actvities in the right order?"""
        self.encounter.add_activities([
            ActivityType.StabilityPlan,
        ])
        self.encounter.add_activities([
            ActivityType.SuicideAssessment,
            ActivityType.StabilityPlan,
            ActivityType.ComfortAndSkills
        ])
        response = self.client.get(self.uri)
        activities = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(activities), 4)
        self.assertEqual(activities[0]["type"], str(ActivityType.StabilityPlan))
        self.assertEqual(activities[1]["type"], str(ActivityType.SuicideAssessment))
        self.assertEqual(activities[2]["type"], str(ActivityType.StabilityPlan))
        self.assertEqual(activities[3]["type"], str(ActivityType.ComfortAndSkills))

    def test_gets_activities_with_comfort_skills_first(self):
        """ Does the tech get actvities in the right order?"""
        self.encounter.add_activities([
            ActivityType.ComfortAndSkills
        ])
        self.encounter.add_activities([
            ActivityType.SuicideAssessment,
            ActivityType.StabilityPlan
        ])
        response = self.client.get(self.uri)
        activities = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(activities), 3)
        self.assertEqual(activities[0]["type"], str(ActivityType.ComfortAndSkills))
        self.assertEqual(activities[1]["type"], str(ActivityType.SuicideAssessment))
        self.assertEqual(activities[2]["type"], str(ActivityType.StabilityPlan))

    def test_only_one_comfort_and_skills(self):
        """ Does the tech get actvities in the right order?"""
        self.encounter.add_activities([
            ActivityType.ComfortAndSkills
        ])
        self.encounter.add_activities([
            ActivityType.ComfortAndSkills
        ])
        response = self.client.get(self.uri)
        activities = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]["type"], str(ActivityType.ComfortAndSkills))

    def test_adding_csp_copies_csa_answers_forward(self):
        self.encounter.add_activities([ActivityType.SuicideAssessment])
        reasons_to_live = ["reason1", "reason2"]
        self.encounter.save_answers({"reasons_live": reasons_to_live})
        answers = self.encounter.get_answers().get('answers').get("reasons_live")
        self.assertEqual(answers, reasons_to_live)

        self.encounter.add_activities([ActivityType.StabilityPlan])
        answers = self.encounter.get_answers().get('answers').get("reasons_live")
        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
        self.assertEqual(answers, reasons_to_live)
        self.assertEqual(stability_plan.reasons_live, reasons_to_live)

    def test_assigning_activity(self):
        response = self.client.post(self.uri, {
            "csp": True
        })

        stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)

        self.assertEqual(response.data[0]['id'], stability_plan.assignedactivity.pk)
        self.assertEqual(response.data[0]['status'], stability_plan.assignedactivity.activity_status)
        self.assertEqual(response.data[0]['locked'], stability_plan.assignedactivity.locked)
        self.assertEqual(response.data[0]['type'], str(ActivityType.StabilityPlan))
        self.assertEqual(response.data[0]['order'], 0)


    def test_lock_activity(self):
        self.encounter.add_activities([ActivityType.SuicideAssessment])
        suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
        response = self.client.patch(self.uri + f"/{suicide_assessment.assignedactivity.pk}", {
            "locked": True
        })

        suicide_assessment.refresh_from_db()
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["locked"])
        self.assertTrue(suicide_assessment.assignedactivity.locked)
