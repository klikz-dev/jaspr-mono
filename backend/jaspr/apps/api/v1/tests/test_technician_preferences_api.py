from rest_framework import status

from jaspr.apps.clinics.models import Preferences, GlobalPreferences
from jaspr.apps.test_infrastructure.testcases import (
    JasprApiTestCase
)


class TestTechnicianPreferencesAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.global_preferences, _ = GlobalPreferences.objects.get_or_create(
            id="global_preferences", consent_language=""
        )
        self.global_preferences.timezone = "America/Los_Angeles"
        self.global_preferences.provider_notes = True
        self.global_preferences.save()
        self.department_preferences = Preferences.objects.create(timezone="	America/Phoenix", provider_notes=True,
                                                                 consent_language="")
        self.clinic_preferences = Preferences.objects.create(timezone="America/Denver", provider_notes=True,
                                                             consent_language="")
        self.system_preferences = Preferences.objects.create(timezone="America/New_York", provider_notes=True,
                                                             consent_language="")

        self.department = self.create_department(preferences=self.department_preferences)
        self.technician = self.create_technician(department=self.department)

        self.clinic = self.department.clinic
        self.clinic.preferences = self.clinic_preferences
        self.clinic.save()
        self.system = self.clinic.system
        self.system.preferences = self.system_preferences
        self.system.save()

        self.uri = f"/v1/technician/preferences"
        self.set_technician_creds(self.technician)




    def test_technician_can_retrieve_preferences(self):
        response = self.client.get(f"{self.uri}?department={self.department.pk}")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["timezone"], self.department_preferences.timezone)

        response = self.client.get(f"{self.uri}?clinic={self.clinic.pk}")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["timezone"], self.clinic_preferences.timezone)

        response = self.client.get(f"{self.uri}?system={self.system.pk}")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["timezone"], self.system_preferences.timezone)

        response = self.client.get(self.uri)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["timezone"], self.global_preferences.timezone)

    def test_technician_cannot_retrieve_preferences_when_not_a_member(self):
        other_system = self.create_healthcare_system(name="other")
        other_technician = self.create_technician(system=other_system)
        self.set_technician_creds(other_technician)

        response = self.client.get(f"{self.uri}?department={self.department.pk}")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        response = self.client.get(f"{self.uri}?clinic={self.clinic.pk}")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        response = self.client.get(f"{self.uri}?system={self.system.pk}")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        response = self.client.get(self.uri)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["timezone"], self.global_preferences.timezone)


