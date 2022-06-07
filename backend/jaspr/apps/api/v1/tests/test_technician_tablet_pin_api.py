from rest_framework import status

from django.core.cache import cache
from jaspr.apps.api.v1.views import TechnicianTabletPinView
from jaspr.apps.test_infrastructure.testcases import (
    JasprApiTestCase,
)

class TestTechnicianTabletPinAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/technician/tablet-pin"

        self.system, self.clinic, self.department = self.create_full_healthcare_system()
        self.system.tablet_system_code = "systemcode1"
        self.system.save()
        self.department.tablet_department_code = "departmentcode1"
        self.department.save()

        self.patient = self.create_patient(department=self.department)
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.technician = self.create_technician(
            system=self.system, department=self.department
        )





    def test_department_pin_activation(self):
        self.set_technician_creds(self.technician)
        response = self.client.post(
            self.uri,
            data={
                "encounter": self.encounter.pk,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["pin"]), 6)
        cache_result = cache.get(f"pin-code-department-{self.department.pk}-{response.data['pin']}")
        self.assertIsNotNone(cache_result)
        self.assertEqual(cache_result["encounter"], self.encounter.pk)
        self.assertEqual(cache_result["technician"], self.technician.pk)

    def test_department_invalid_encounter(self):
        self.set_technician_creds(self.technician)
        response = self.client.post(
            self.uri,
            data={
                "encounter": 0,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_technician_assign_pin_no_patient_access(self):

        # This technician should not have access to patients in this system
        # Setup second system / technician / patient
        system2, clinic2, department2 = self.create_full_healthcare_system(
            name="System 2",
            department_kwargs={
                "name": "Dept Two"
            })
        department2.tablet_department_code = "systemcode2"
        department2.save()

        technician2 = self.create_technician(
            system=system2, department=department2
        )
        self.set_technician_creds(technician2)
        response = self.client.post(
            self.uri,
            data={
                "encounter": self.encounter.pk,  # Encounter from different system than technician
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



