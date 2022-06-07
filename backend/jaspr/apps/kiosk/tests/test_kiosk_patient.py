"""Test operations on Patient"""
from copy import deepcopy

from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class TestPatient(JasprTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.system, cls.clinic, cls.department = cls.create_full_healthcare_system(
            name="Clinic One"
        )
        cls.department.name = "Location One"
        cls.department.save()

    def test_patient_creation(self):
        patient = self.create_patient(ssid="TestPatient1")

        self.assertEqual(patient.ssid, "TestPatient1")
        self.assertEqual(patient.status, "active")
        self.assertEqual(patient.user.email, f"ssid-testpatient1.jaspr@jasprhealth.com")

    def test_has_security_steps(self):
        patient = self.create_patient(ssid="TestPatient1")
        # self.assertFalse(patient.has_security_steps)
        encounter = self.create_security_question(patient=patient)
        self.assertFalse(encounter.has_security_steps)
        image = self.create_privacy_screen_image()
        encounter.privacy_screen_image = image
        encounter.save()
        self.assertTrue(encounter.has_security_steps)


    def test_patient_internal_external_emails(self):
        patient = self.create_patient(
            department=self.department, ssid="TestPatientEmail1"
        )
        self.assertTrue(patient.has_internal_email())
        patient.user.email = "john.doe@example.com"
        patient.user.save()
        self.assertFalse(patient.has_internal_email())
