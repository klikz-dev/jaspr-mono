from rest_framework import status

from django.core.cache import cache
from jaspr.apps.api.v1.views import TechnicianTabletPinView
from jaspr.apps.test_infrastructure.testcases import (
    JasprApiTestCase,
)

class TestPatientTabletPinAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()
        self.uri = "/v1/patient/tablet-pin"

        self.system, self.clinic, self.department = self.create_full_healthcare_system()
        self.system.tablet_system_code = "systemcode"
        self.system.save()
        self.department.tablet_department_code = "departmentcode"
        self.department.save()

        self.patient = self.create_patient(department=self.department)
        self.encounter = self.create_patient_encounter(
            patient=self.patient, department=self.department
        )
        self.technician = self.create_technician(
            system=self.system, department=self.department
        )


    def test_department_pin_activation(self):
        pin = TechnicianTabletPinView.generate_code()
        department_cache_key = f"pin-code-department-{self.department.pk}-{pin}"
        cache.set(department_cache_key, {
            "encounter": self.encounter.pk,
            "technician": self.technician.pk
        }, 5000)

        response = self.client.post(
            self.uri,
            data={
                "departmentCode": self.department.tablet_department_code,
                "pinCode": pin
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.patient.user.pk, response.data["patient"]["id"])
        self.assertEqual(self.encounter.pk, response.data["session"]["encounter"])

    def test_system_pin_activation(self):
        pin = TechnicianTabletPinView.generate_code()
        system_cache_key = f"pin-code-system-{self.system.pk}-{pin}"
        cache.set(system_cache_key, {
            "encounter": self.encounter.pk,
            "technician": self.technician.pk
        }, 5000)

        response = self.client.post(
            self.uri,
            data={
                "systemCode": self.system.tablet_system_code,
                "pinCode": pin
            },
        )
        print(pin)
        print(self.patient.pk)
        import json
        print(json.dumps(response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.patient.user.pk, response.data["patient"]["id"])
        self.assertEqual(self.encounter.pk, response.data["session"]["encounter"])

    def test_department_pin_activation_incorrect_pin(self):
        pin = TechnicianTabletPinView.generate_code()
        department_cache_key = f"pin-code-department-{self.department.pk}-{pin}"
        cache.set(department_cache_key, {
            "encounter": self.encounter.pk,
            "technician": self.technician.pk
        }, 5000)

        response = self.client.post(
            self.uri,
            data={
                "departmentCode": self.department.tablet_department_code,
                "pinCode": "BADPIN"
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "The code entered is not valid")

    def test_department_pin_activation_incorrect_department(self):
        pin = TechnicianTabletPinView.generate_code()
        department_cache_key = f"pin-code-department-{self.department.pk}-{pin}"
        cache.set(department_cache_key, {
            "encounter": self.encounter.pk,
            "technician": self.technician.pk
        }, 5000)

        response = self.client.post(
            self.uri,
            data={
                "departmentCode": "BADCODE",
                "pinCode": pin
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")


