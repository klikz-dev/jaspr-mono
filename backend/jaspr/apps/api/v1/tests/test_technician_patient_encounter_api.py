import random
from datetime import date, timedelta
import datetime

from django.utils import timezone
import before_after
from freezegun import freeze_time
from rest_framework import status

from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase



class TestTechnicianPatientsEncounterAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.system, self.clinic, self.department = self.create_full_healthcare_system()
        self.patient = self.create_patient(department=self.department)
        self.encounter = self.create_patient_encounter(patient=self.patient, department=self.department)
        self.technician = self.create_technician(department=self.department)

        self.uri = f"/v1/technician/encounter"
        self.set_technician_creds(self.technician)

    def test_technician_creates_new_encounter(self):
        original_encounter_id = self.encounter.pk
        response = self.client.post(self.uri, {
            "patient": self.patient.pk
        })
        new_encounter_id = self.patient.current_encounter.pk


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(original_encounter_id, new_encounter_id)
        self.assertEqual(response.data["current_encounter"], new_encounter_id)

    def test_technician_cannot_create_new_encounter_for_patient_different_department(self):
        department2 = self.create_department(system=self.system)
        technician2 = self.create_technician(department=department2)
        self.set_patient_creds(technician2)
        response = self.client.post(self.uri, {
            "patient": self.patient.pk
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
