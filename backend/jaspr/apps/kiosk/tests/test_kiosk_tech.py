"""Test operations on Technician"""
from django.core.exceptions import ValidationError
from jaspr.apps.clinics.models import DepartmentTechnician
from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class TestTechnician(JasprTestCase):
    def setUp(self):
        super().setUp()
        # kt_ means it is the tech clinic
        self.tech_system = self.create_healthcare_system(name="Clinic One")
        self.tech_clinic = self.create_clinic(
            system=self.tech_system, name="Location One"
        )
        self.tech_department = self.create_department(
            clinic=self.tech_clinic, name="Department One"
        )

        self.system = self.create_healthcare_system(name="Clinic Not")
        self.clinic = self.create_clinic(
            system=self.system, name="Location Not"
        )
        self.department = self.create_department(
            clinic=self.clinic, name="Department Not"
        )

    def test_technician_creation_department_for_clinic(self):

        technician = self.create_technician(
            system=self.tech_system,
            department=self.tech_department
        )
        technician_department = DepartmentTechnician.objects.get(
            technician=technician
        )

        self.assertEqual(technician.system, self.tech_system)
        self.assertEqual(
            technician_department.department, self.tech_department
        )

    def test_technician_creation_department__not_for_clinic(self):

        technician = self.create_technician(system=self.tech_system, department=self.tech_department)

        with self.assertRaises(ValidationError):
            DepartmentTechnician.objects.create(
                technician=technician, department=self.department
            )
