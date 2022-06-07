from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


class TestTechnicianDepartmentsAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="technician/departments",
            version_prefix="v1",
            factory_name="create_department",
        )

        self.action_group_map["list"]["allowed_groups"] = ["Technician"]


class TestTechnicianDepartmentsAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.technician = self.create_technician()
        self.department_technician = (
            self.technician.departmenttechnician_set.get(department__name="unassigned")
        )
        self.department = (
            self.department_technician.department
        )
        self.clinic = self.department.clinic
        self.system = self.clinic.system
        self.uri = f"/v1/technician/departments"
        self.set_technician_creds(self.technician)

    def test_list_no_departments_because_department_technician_not_present(
        self,
    ):
        # This is a required record for finding the clinic location. By deleting it,
        # we're also making sure it's required for the `Technician` to see the
        # `ClinicLocation`.
        self.department_technician.delete()
        response = self.client.get(self.uri)

        # NOTE: Currently, at the time of writing,
        # `SatisfiesClinicLocationIPWhitelistingFromTechnician` is included in
        # `permissions_classes`, which will throw a `403` if the `Technician` does not
        # have any `ClinicLocationTechnician` records associated with it.
        self.assertEqual(response.status_code, 403)

    def test_list_single_department(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"], self.department.pk
        )
        self.assertEqual(
            response.data[0]["name"], f"{self.department.clinic.name} > {self.department.name}"
        )

    def test_list_multiple_departments(self):
        other_department1 = self.create_department(
            name="Other Dept 1",
            clinic=self.clinic
        )
        other_department2 = self.create_department(
            name="Other Dept 2",
            clinic=self.clinic
        )
        other_department3 = self.create_department(
            name="Other Dept 3",
            clinic=self.clinic
        )

        other_system = self.create_healthcare_system(name="Other System")
        other_clinic = self.create_clinic(name="Other Clinic", system=other_system)
        other_department_in_other_clinic = self.create_department(
            name="Should not be in list",
            clinic=other_clinic
        )

        other_technician_in_clinic_different_locations = self.create_technician(
            system=self.system,
            department=other_department1,
        )
        self.create_department_technician(
            technician=other_technician_in_clinic_different_locations,
            department=other_department2,
        )

        other_technician_in_clinic_with_shared_location = self.create_technician(
            system=self.system,
            department=self.department,
        )

        other_technician_in_other_clinic = self.create_technician(
            system=other_system,
            department=other_department_in_other_clinic
        )

        self.create_department_technician(
            technician=self.technician,
            department=other_department3,
        )

        response = self.client.get(self.uri)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        department_ids = {
            self.department.pk,
            other_department3.pk,
        }
        self.assertIn(response.data[0]["id"], department_ids)
        self.assertNotEqual(
            response.data[0]["id"], response.data[1]["id"], department_ids
        )
