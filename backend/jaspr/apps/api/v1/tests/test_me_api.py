from django.utils.dateparse import parse_datetime
from rest_framework import status

from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from jaspr.apps.kiosk.activities.activity_utils import ActivityType


class TestMeAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403,  404, 405 """

    def setUp(self):
        super().setUp(resource_pattern="me", version_prefix="v1")

        self.action_group_map["list"]["allowed_groups"] = ["Technician", "Patient"]
        self.action_group_map["retrieve"]["allowed_groups"] = [
            "Technician",
            "Patient",
        ]
        self.action_group_map["partial_update"]["allowed_groups"] = [
            "Technician",
            "Patient",
        ]
        self.detail_uri = self.base_uri


class TestMeAPI(JasprApiTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.system, cls.clinic, cls.department = cls.create_full_healthcare_system(
            name="System 1",
            department_kwargs={
                "name": "Dept One"
            }
        )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.uri = "/v1/me"

    def test_get_me_technician(self):
        """Can an authenticated technician user get data on self?"""
        technician = self.create_technician(
            system=self.system, department=self.department
        )
        self.set_technician_creds(technician)
        response = self.client.get(self.uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], technician.user.pk)
        self.assertEqual(response.data["user_type"], "technician")
        self.assertEqual(
            response.data["analytics_token"], str(technician.analytics_token)
        )
        self.assertEqual(response.data["location"]["system"]["name"], technician.user.system.name)
        self.assertEqual(response.data["role"], technician.role)

    def test_get_me_patient(self):
        """Can an authenticated patient user get data on self?"""
        patient = self.create_patient(department=self.department)
        encounter = self.create_patient_encounter(
            patient=patient, department=self.department
        )
        encounter.add_activities([ActivityType.SuicideAssessment, ActivityType.StabilityPlan])
        self.set_patient_creds(patient, encounter=encounter)
        response = self.client.get(self.uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], patient.user.pk)
        self.assertEqual(response.data["user_type"], "patient")
        self.assertEqual(response.data["guide"], patient.guide)
        self.assertEqual(
            response.data["tools_to_go_status"], patient.tools_to_go_status
        )
        self.assertEqual(response.data["tour_complete"], patient.tour_complete)
        self.assertEqual(response.data["onboarded"], patient.onboarded)
        self.assertEqual(response.data["email"], "") # Internal email addresses are returned as an empty string
        self.assertEqual(response.data["mobile_phone"], patient.user.mobile_phone)
        self.assertEqual(
            response.data["tools_to_go_status"], patient.tools_to_go_status
        )
        # TODO: Remove once the frontend does not need anymore. Check after 01/01/2021.
        self.assertEqual(response.data["in_er"], False)
        self.assertEqual(
            response.data["current_walkthrough_step"], patient.current_walkthrough_step
        )
        self.assertEqual(
            parse_datetime(response.data["current_walkthrough_step_changed"]),
            patient.current_walkthrough_step_changed,
        )
        self.assertEqual(response.data["analytics_token"], str(patient.analytics_token))
        self.assertEqual(response.data["location"]["system"]["name"], patient.user.system.name)
        self.assertEqual(response.data["location"]["department"]["name"], patient.user.department.name)
        self.assertEqual(response.data["mrn"], patient.mrn)
        self.assertEqual(response.data["ssid"], patient.ssid)
        self.assertEqual(response.data["date_of_birth"], patient.date_of_birth)
        self.assertEqual(response.data["first_name"], patient.first_name)
        self.assertEqual(response.data["last_name"], patient.last_name)


    def test_get_me_patient_real_email(self):
        """Can a patient with an external email address set see their email?"""
        patient = self.create_patient(
            department=self.department
        )
        self.set_patient_creds(patient)
        patient.user.email = 'john.doe@example.com'
        patient.user.save()
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], patient.user.email)

    def test_get_me_patient_cannot_get_internal_email(self):
        """Does a patient with an internal email get a blank email response on a me request"""
        patient = self.create_patient(
            department=self.department
        )
        self.set_patient_creds(patient)
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("", response.data['email'])

        patient.user.email = "test@example.com"
        patient.user.save()
        response = self.client.get(self.uri)
        self.assertEqual(response.data["email"], patient.user.email)


    def test_patch_me_patient(self):
        """Can an authenticated patient user patch certain data on self?"""
        patient = self.create_patient(department=self.department)
        encounter = self.create_patient_encounter(patient=patient, department=self.department)

        # Pre assertion: Want to make sure fields we are about to patch are not filled out.
        self.assertEqual(patient.guide, "")

        self.set_patient_creds(patient)
        data = {
            "guide": "Jaz",
            "tour_complete": True,
            "onboarded": True,
        }
        response = self.client.patch(self.uri, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], patient.user.pk)
        self.assertEqual(response.data["guide"], "Jaz")
        patient.refresh_from_db()
        self.assertEqual(patient.guide, "Jaz")
        self.assertEqual(patient.tour_complete, True)
        self.assertEqual(patient.onboarded, True)
        # TODO: Remove once the frontend does not need anymore. Check after 01/01/2021.
        self.assertEqual(response.data["in_er"], False)
