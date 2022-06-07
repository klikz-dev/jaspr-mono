from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from django.utils import timezone
from freezegun import freeze_time
from rest_framework import status

from jaspr.apps.kiosk.models import Patient

class TestTechnicianPatientsJAHCredentials(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/technician/patients"

        self.system, self.clinic, self.department = self.create_full_healthcare_system()

        self.technician = self.create_technician(department=self.department)


        self.set_technician_creds(self.technician)

        self.patient_data = {
            "ssid": "jah-credential-patient",
            "department": self.department,
        }
        self.now = timezone.now()
        with freeze_time(self.now):
            self.patient = self.create_patient(**self.patient_data)

    def test_technician_cannot_set_jah_email_to_internal_email_address(self):
        """Technicians cannot set user email to a *.jaspr@jasprhealth.com email address"""

        data = {
            "ssid": "jah-credential-patient",
            "email": "john.jaspr@jasprhealth.com",
            "mobilePhone": "5555555555",
            "departments": [self.department.id]
        }

        response = self.client.put(f"{self.uri}/{self.patient.pk}", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_technician_cannot_set_jah_credentials_if_patient_has_completed_jah_setup(self):
        self.patient.tools_to_go_status = Patient.TOOLS_TO_GO_SETUP_FINISHED
        self.patient.save()

        data = {
            "ssid": self.patient.ssid,
            "email": "john.jaspr@jasprhealth.com",
            "mobilePhone": "5555555555",
            "departments": [self.department.id]
        }

        response = self.client.put(f"{self.uri}/{self.patient.pk}", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_technician_can_set_jah_credentials(self):
        self.patient.tools_to_go_status = Patient.TOOLS_TO_GO_EMAIL_SENT
        self.patient.save()
        data = {
            "ssid": self.patient.ssid,
            "email": "john.doe@example.com",
            "mobilePhone": "5005550006",
            "departments": [self.department.id]
        }

        response = self.client.put(f"{self.uri}/{self.patient.pk}", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient.refresh_from_db()
        self.assertEqual(data['email'], self.patient.user.email)
        self.assertEqual(data['mobilePhone'], self.patient.user.mobile_phone)
