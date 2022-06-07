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
from ..exceptions import PatientAlreadyExistsError

from ..helpers import zulu_time_format
from .helpers import (
    assert_validation_error_thrown,
)

from jaspr.apps.api.v1.serializers import (
    ActivateNewPatientSerializer,
)
from jaspr.apps.kiosk.models import ActivateRecord, Patient

class TestTechnicianPatientsAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="technician/patients",
            version_prefix="v1",
        )

        self.action_group_map["list"]["detail"] = True
        self.action_group_map["list"]["allowed_groups"] = ["Technician"]
        self.action_group_map["update"]["allowed_groups"] = ["Technician"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Technician"]
        # Will test create in another section of unit tests
        self.action_group_map.pop("create")


class TestTechnicianPatientsAPIRetrieve(JasprApiTestCase):
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

        self.patient_data = {
            "mrn": "Patient-5",
            "first_name": "Buggz",
            "last_name": "Bunny",
            "date_of_birth": datetime.date(year=1967, month=8, day=25),  # 1967-08-25
        }
        self.now = timezone.now()
        with freeze_time(self.now):
            self.patient = self.create_patient(**self.patient_data)

        self.create_patient_department_sharing(department=self.department, patient=self.patient)

        self.patient_data["department"] = self.department
        self.uri = f"/v1/technician/patients/{self.patient.pk}"
        self.set_technician_creds(self.technician)

    def test_technician_cannot_retrieve_patient_from_other_clinic(self):
        """ Is a tech barred from retrieving patient from other clinic?"""
        other_clinic = self.create_healthcare_system(name="other")
        other_technician = self.create_technician(system=other_clinic)
        self.set_technician_creds(other_technician)
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def test_technician_cannot_retrieve_patient_from_other_department(self):
        """ Is a tech barred from retrieving patient from a different clinic location within same clinic?"""
        other_department = self.create_department(
            clinic=self.clinic, name="Other Clinic Location"
        )

        other_patient_data = {
            "mrn": "Patient-6",
            "first_name": "Road",
            "last_name": "Runner",
            "date_of_birth": datetime.date(year=1967, month=8, day=25),  # 1967-08-25
            "department": other_department,
        }

        other_patient = self.create_patient(**other_patient_data)
        other_uri = f"/v1/technician/patients/{other_patient.pk}"
        response = self.client.get(other_uri)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def test_retrieve_patient(self):
        """ Can tech retrieve a patient that shares one of their clinic locations with all new data?"""
        response = self.client.get(self.uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        patient = Patient.objects.get(pk=response.data["id"])
        self.assertEqual(patient.ssid, None)
        self.assertEqual(patient.departments[0], self.department.id)
        self.assertEqual(patient.first_name, "Buggz")
        self.assertEqual(patient.last_name, "Bunny")
        self.assertEqual(
            patient.date_of_birth, datetime.date(year=1967, month=8, day=25)
        )
        self.assertEqual(patient.mrn, "Patient-5")

        self.assertEqual(len(response.data), 15)
        self.assertEqual(self.patient.pk, response.data["id"])
        self.assertEqual(None, response.data["current_encounter"])
        self.assertEqual(self.patient.mrn, response.data["mrn"])
        self.assertEqual(self.patient.ssid, response.data["ssid"])
        self.assertEqual(
            zulu_time_format(self.patient.created), response.data["created"]
        )
        self.assertEqual(self.patient.tour_complete, response.data["tour_complete"])
        self.assertEqual(
            self.patient.tools_to_go_status, response.data["tools_to_go_status"]
        )
        self.assertEqual(self.patient.user.email, response.data["email"])
        self.assertEqual(self.patient.user.mobile_phone, response.data["mobile_phone"])
        self.assertEqual(self.patient.first_name, response.data["first_name"])
        self.assertEqual(self.patient.last_name, response.data["last_name"])
        self.assertEqual(
            self.patient.date_of_birth.isoformat(), response.data["date_of_birth"]
        )
        self.assertEqual(
            self.patient.departments[0], response.data["departments"][0]
        )
        self.assertEqual(
            str(self.patient.analytics_token), response.data["analytics_token"]
        )


class TestTechnicianPatientsAPIUpdate(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.technician = self.create_technician()
        self.department_technician = (
            self.technician.departmenttechnician_set.get(department__name="unassigned")
        )
        self.department = self.department_technician.department
        self.clinic = self.department.clinic
        self.system = self.clinic.system

        self.patient_data = {
            "mrn": "Patient-5",
            "first_name": "Buggz",
            "last_name": "Bunny",
            "date_of_birth": datetime.date(year=1967, month=8, day=25),  # 1967-08-25
        }
        self.patient = self.create_patient(**self.patient_data)
        self.patient_data["department"] = self.department.id
        self.create_patient_department_sharing(patient=self.patient, department=self.department)
        self.uri = f"/v1/technician/patients/{self.patient.pk}"
        self.set_technician_creds(self.technician)

    def test_technician_cannot_update_patient_from_other_clinic(self):
        """ Is a tech barred from updating patient from other clinic?"""
        other_clinic = self.create_healthcare_system(name="other")
        other_technician = self.create_technician(system=other_clinic)
        self.set_technician_creds(other_technician)

        data = {
            "mrn": "Patient-6",
            "first_name": "Buggz",
            "last_name": "Bunny",
            "date_of_birth": datetime.date(year=1967, month=8, day=25),  # 1967-08-25
            "department": self.department.pk,
        }

        response = self.client.put(self.uri, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def test_technician_cannot_update_patient_from_other_department(self):
        """ Is a tech barred from updating patient from other clinic location and shared clinic?"""
        other_department = self.create_department(
            clinic=self.clinic, name="Other Clinic Location"
        )

        other_patient_data = {
            "mrn": "Patient-6",
            "first_name": "Road",
            "last_name": "Runner",
            "date_of_birth": datetime.date(year=1967, month=8, day=25),  # 1967-08-25
        }
        other_patient = self.create_patient(**other_patient_data)

        other_patient_data["department"] = other_department

        other_patient_data["mrn"] = "Patient-6-update"
        other_patient_data["department"] = other_department.pk
        other_uri = f"/v1/technician/patients/{other_patient.pk}"
        response = self.client.put(other_uri, other_patient_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def test_partial_update_patient_is_not_allowed(self):
        """ Is tech barred from updating only one field?"""

        data = {
            "ssid": "Patient-6",
        }
        response = self.client.patch(self.uri, data)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, response.data
        )

    def test_update_patient(self):
        """ Can tech update a patient that shares one of their clinic locations with all new data?"""

        other_department = self.create_department(
            name="other", clinic=self.clinic
        )
        self.create_department_technician(
            department=other_department, technician=self.technician
        )

        data = {
            "mrn": "Patient-6",
            "first_name": "Elmer",
            "last_name": "Fudd",
            "date_of_birth": datetime.date(year=1967, month=8, day=26),  # 1967-08-25
            "departments": [other_department.pk],
        }
        response = self.client.put(self.uri, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.mrn, "Patient-6")
        self.assertEqual(self.patient.first_name, "Elmer")
        self.assertEqual(self.patient.last_name, "Fudd")
        self.assertEqual(
            self.patient.date_of_birth, datetime.date(year=1967, month=8, day=26)
        )
        self.assertEqual(self.patient.departments[0], other_department.id)

    def test_update_patient_with_department_not_of_the_technician(self):
        """ Can tech update a patient with department that they don't share?"""

        other_department = self.create_department(
            name="other", clinic=self.clinic
        )
        self.create_patient_department_sharing(
            patient=self.patient,
            department=other_department
        )

        data = {
            "mrn": "Patient-6",
            "first_name": "Elmer",
            "last_name": "Fudd",
            "date_of_birth": datetime.date(year=1967, month=8, day=26),  # 1967-08-25
            "departments": [other_department.pk],
        }
        response = self.client.put(self.uri, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["departments"][0],
            "Submitted department is not one of the available departments for this technician.",
        )

    def test_update_patient_with_ssid_instead_of_mrn(self):
        """ Can tech update a patient with ssid instead of mrn?"""

        other_department = self.create_department(
            name="other", clinic=self.clinic
        )
        self.create_department_technician(
            department=other_department, technician=self.technician
        )
        self.create_patient_department_sharing(
            patient=self.patient,
            department=other_department
        )

        data = {
            "ssid": "Patient-6",
            "first_name": "",
            "last_name": "",
            "date_of_birth": None,
            "departments": [other_department.pk],
            "mrn": "",
        }
        print(self.uri)
        print(data)
        response = self.client.put(self.uri, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.ssid, "Patient-6")
        self.assertEqual(self.patient.mrn, "")
        self.assertEqual(self.patient.first_name, "")
        self.assertEqual(self.patient.last_name, "")
        self.assertEqual(self.patient.date_of_birth, None)
        self.assertEqual(self.patient.departments[0], other_department.pk)

    def test_update_patient_with_duplicate_mrn(self):
        """ Can tech update a patient to be the same as an already existing patient with same mrn?"""
        data = self.patient_data
        data["departments"] = [self.patient.departments[0]]

        response = self.client.put(self.uri, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.mrn, self.patient_data["mrn"])

    def test_update_patient_with_ssid_and_mrn_results_in_error(self):
        """ Is an error generated when mrn and ssid are used during update of a patient?"""

        data = {
            "ssid": "Patient-6",
            "first_name": "",
            "last_name": "",
            "date_of_birth": None,
            "departments": [self.department.pk],
            "mrn": "Patient-5",
        }

        response = self.client.put(self.uri, data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )
        self.assertEqual(
            response.data,
            {
                "non_field_errors": [
                    "Patients cannot have an SSID and any of 'First Name', 'Last Name', 'Date of Birth', or 'MRN'."
                ]
            },
        )

    def test_update_patient_with_ssid_and_first_name_results_in_error(self):
        """ Is an error generated when first_name and ssid are used during update of a patient?"""
        data = {
            "ssid": "Patient-6",
            "first_name": "Elmer",
            "last_name": "",
            "date_of_birth": None,
            "departments": [self.department.pk],
            "mrn": "",
        }
        response = self.client.put(self.uri, data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )
        self.assertEqual(
            response.data,
            {
                "non_field_errors": [
                    "Patients cannot have an SSID and any of 'First Name', 'Last Name', 'Date of Birth', or 'MRN'."
                ]
            },
        )

    def test_update_patient_delete_ssid_with_no_mrn(self):
        """ Is an error generated when ssid is removed and mrn is not added?"""
        data = {
            "ssid": "",
            "first_name": "Elmer",
            "last_name": "",
            "date_of_birth": None,
            "departments": [self.department.pk],
            "mrn": "",
        }
        response = self.client.put(self.uri, data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )
        self.assertEqual(
            response.data,
            {
                "non_field_errors": [
                    "When SSID is not provided 'First Name', 'Last Name', 'Date of Birth', and 'MRN' are required."
                ]
            },
        )

    def test_update_patient_delete_ssid_with_mrn_swap(self):
        """ Can ssid be swapped for mrn?"""

        # set up patient as an SSID patient.
        self.patient.ssid = "f1769e"
        self.patient.date_of_birth = None
        self.patient.first_name = ""
        self.patient.last_name = ""
        self.patient.save()

        data = {
            "id": self.patient.pk,
            "ssid": "",
            "first_name": "Elmer",
            "last_name": "Fudd",
            "date_of_birth": datetime.date(year=1967, month=8, day=25),  # 1967-08-25
            "departments": [self.department.pk],
            "mrn": "elmer1967fudd",
        }

        response = self.client.put(self.uri, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        self.patient.refresh_from_db()
        self.assertEqual(self.patient.ssid, None)

    def test_update_patient_delete_ssid_with_mrn_swap_missing_ssid_field(self):
        """ Can ssid be swapped for mrn?"""

        # set up patient as an SSID patient.
        self.patient.ssid = "f1769e"
        self.patient.date_of_birth = None
        self.patient.first_name = ""
        self.patient.last_name = ""
        self.patient.save()

        data = {
            "id": self.patient.pk,
            # "ssid": "",   -- not including this field as frontend doesn't when ssid not present.
            "first_name": "Elmer",
            "last_name": "Fudd",
            "date_of_birth": datetime.date(year=1967, month=8, day=25),  # 1967-08-25
            "departments": [self.department.pk],
            "mrn": "elmer1967fudd",
        }

        response = self.client.put(self.uri, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        self.patient.refresh_from_db()
        self.assertEqual(self.patient.ssid, None)

    def test_wrong_clinic(self):
        """
        `Patient`'s clinic location does not belong to the `Technician`'s clinic.
        """
        other_clinic = self.create_clinic()
        other_department = self.create_department(name="Other Dept", clinic=other_clinic)
        data = {
            "ssid": "Patient-6",
            "first_name": "",
            "last_name": "",
            "date_of_birth": None,
            "departments": [other_department.pk],
            "mrn": "",
        }
        response = self.client.put(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["departments"][0], "Submitted department is not one of the available departments for this technician.")

    def test_wrong_department_within_clinic(self):
        """
        `Patient`'s clinic location does not correspond to one of the `Technician`s
        `ClinicLocationTechnician` records.
        """
        other_department_within_clinic = self.create_department(
            name="Other Dept", clinic=self.clinic
        )
        data = {
            "ssid": "Patient-6",
            "first_name": "",
            "last_name": "",
            "date_of_birth": None,
            "departments": [other_department_within_clinic.pk],
            "mrn": "",
        }
        response = self.client.put(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["departments"][0], "Submitted department is not one of the available departments for this technician.")

    def test_correct_department_but_not_active(self):
        """
        `Patient`'s clinic location corresponds to one of the `Technician`s
        `ClinicLocationTechnician` records but the record is not active?
        """
        self.department_technician.status = "inactive"
        self.department_technician.save()
        data = {
            "ssid": "Patient-6",
            "first_name": "",
            "last_name": "",
            "date_of_birth": None,
            "department": self.department.pk,
            "mrn": "",
        }
        response = self.client.put(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestTechnicianPatientsListAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/technician/patients"
        self.technician = self.create_technician()
        self.set_technician_creds(self.technician)

    def test_no_recent_patients(self):
        response = self.client.get(self.uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_one_recent_patient(self):
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        now = timezone.now()
        with freeze_time(now):
            patient = self.create_patient(
                date_of_birth=date(year=1967, month=8, day=25),  # 1967-08-25
            )
            self.create_patient_department_sharing(patient=patient, department=department)
            encounter = self.create_patient_encounter(
                patient=patient, department=department
            )
            latest_record = self.create_activate_record(
                technician=self.technician, patient=patient, timestamp=now
            )
        earlier = now - timedelta(hours=36)
        with freeze_time(earlier):
            first_record = self.create_activate_record(
                technician=self.technician, patient=patient, timestamp=earlier
            )
        response = self.client.get(self.uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        response_dict = response.data[0]
        self.assertEqual(len(response_dict), 19)
        self.assertEqual(patient.pk, response_dict["id"])
        self.assertEqual(encounter.pk, response_dict["current_encounter"])
        self.assertEqual(patient.mrn, response_dict["mrn"])
        self.assertEqual(patient.ssid, response_dict["ssid"])
        self.assertEqual(zulu_time_format(patient.created), response_dict["created"])
        self.assertEqual(patient.tour_complete, response_dict["tour_complete"])
        self.assertEqual(
            patient.tools_to_go_status, response_dict["tools_to_go_status"]
        )
        self.assertEqual(patient.first_name, response_dict["first_name"])
        self.assertEqual(patient.last_name, response_dict["last_name"])
        self.assertEqual(
            patient.date_of_birth.isoformat(), response_dict["date_of_birth"]
        )
        self.assertEqual("", response_dict['email'])
        self.assertEqual(patient.user.mobile_phone, response_dict["mobile_phone"])
        self.assertEqual(str(patient.analytics_token), response_dict["analytics_token"])

        # TODO add path assertion test / start_time test


    def test_recent_patients_filters_by_technician_department(self):
        """ Do only patients who share clinic location appear in list? """
        system = self.technician.system

        # create patient and clinic location that will be filtered out.
        other_clinic = self.create_clinic(name="Other Clinic", system=system)
        other_department = self.create_department(name="Other Dept", clinic=other_clinic)
        other_patient = self.create_patient()
        other_technician = self.create_technician(
            system=system, department=other_department
        )
        self.create_activate_record(
            technician=other_technician,
            patient=other_patient,
            timestamp=timezone.now(),
        )

        # create patient and clinic location that will be found
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        patient = self.create_patient()
        self.create_patient_department_sharing(patient=patient, department=department)
        self.create_activate_record(
            technician=self.technician,
            patient=patient,
            timestamp=timezone.now(),
        )

        response = self.client.get(self.uri)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], patient.pk)

    def test_recent_patients_correctly_sets_last_logged_in_at(self):
        """ Are patients ordered by their last log in irrespective of technician? """

        # Create other technician who shares clinic location with technician
        other_technician = self.create_technician(system=self.technician.system)

        # ClinicLocationTechician records are made automagically.
        # As proof we compare their clinic location
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        other_technician_department = (
            other_technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        self.assertEqual(other_technician_department, department)

        # and use that clinic location for the patient
        patient = self.create_patient()
        self.create_patient_department_sharing(patient=patient, department=department)

        now = timezone.now()
        self.create_activate_record(
            technician=other_technician,
            patient=patient,
            timestamp=now,
        )

        self.create_activate_record(
            technician=self.technician,
            patient=patient,
            timestamp=now - timedelta(seconds=1),
        )

        response = self.client.get(self.uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], patient.pk)
        self.assertEqual(response.data[0]["last_logged_in_at"], now)

    def test_recent_patients_max_number(self):
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        pks_and_latest = []
        start = timezone.now() - timedelta(seconds=360)
        seconds_counter = 0
        # NOTE/TODO (Test-Speedup-Possibility): If/when speeding up the tests if that
        # becomes necessary, this _could be_ refactored to use `bulk_create`, and/or
        # this test could just be removed if the logic changes or we just want to trust
        # that we're returning 30 patients max. I didn't think it was worth it for now
        # to make the test a little more complicated (with `bulk_create` etc.) for a
        # maybe quarter to half of a second speedup.
        for _ in range(31):
            patient = self.create_patient()
            self.create_patient_department_sharing(patient=patient, department=department)
            latest = start + timedelta(seconds=seconds_counter)
            self.create_activate_record(
                technician=self.technician,
                patient=patient,
                timestamp=latest,
            )
            if random.choice(range(2)):
                self.create_activate_record(
                    technician=self.technician,
                    patient=patient,
                    timestamp=latest,
                )
            seconds_counter += 1
            if random.choice(range(4)):
                latest = start + timedelta(seconds=seconds_counter)
                self.create_activate_record(
                    technician=self.technician,
                    patient=patient,
                    timestamp=start + timedelta(seconds=seconds_counter),
                )
                seconds_counter += 1
            pks_and_latest.append((patient.pk, latest))

        other_technician = self.create_technician(system=self.technician.system)
        other_record = self.create_activate_record(
            technician=other_technician,
            patient=self.create_patient(),
            timestamp=start - timedelta(seconds=1),
        )
        response = self.client.get(self.uri)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 30)
        for (pk, latest), data in zip(reversed(pks_and_latest[-30:]), response.data):
            self.assertEqual(data["id"], pk)
            self.assertEqual(data["last_logged_in_at"], latest)

    def test_empty_query(self):
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        now = timezone.now()
        with freeze_time(now):
            patient = self.create_patient(
                date_of_birth=date(year=1967, month=8, day=25),  # 1967-08-25
            )
            self.create_patient_department_sharing(patient=patient, department=department)
            encounter = self.create_patient_encounter(patient=patient, department=department)
            latest_record = self.create_activate_record(
                technician=self.technician, patient=patient, timestamp=now
            )
        earlier = now - timedelta(hours=36)
        with freeze_time(earlier):
            first_record = self.create_activate_record(
                technician=self.technician, patient=patient, timestamp=earlier
            )

        query = {"q": ""}
        response = self.client.get(self.uri, data=query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        response_dict = response.data[0]
        self.assertEqual(len(response_dict), 19)
        self.assertEqual(patient.pk, response_dict["id"])
        self.assertEqual(encounter.pk, response_dict["current_encounter"])
        self.assertEqual(patient.mrn, response_dict["mrn"])
        self.assertEqual(patient.ssid, response_dict["ssid"])
        self.assertEqual(zulu_time_format(patient.created), response_dict["created"])
        self.assertEqual(patient.tour_complete, response_dict["tour_complete"])
        self.assertEqual(
            patient.tools_to_go_status, response_dict["tools_to_go_status"]
        )
        self.assertEqual(patient.first_name, response_dict["first_name"])
        self.assertEqual(patient.last_name, response_dict["last_name"])
        self.assertEqual(
            patient.date_of_birth.isoformat(), response_dict["date_of_birth"]
        )
        self.assertEqual(response_dict["email"], "")
        self.assertEqual(patient.user.mobile_phone, response_dict["mobile_phone"])
        self.assertEqual(str(patient.analytics_token), response_dict["analytics_token"])


    def test_dob_query(self):
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        dob1 = date.today()
        dob2 = date.today() - timedelta(days=1)
        later = timezone.now()
        earlier = later - timedelta(hours=36)
        patient1 = self.create_patient(
            date_of_birth=dob1
        )
        patient2 = self.create_patient(
            date_of_birth=dob2
        )
        self.create_patient_department_sharing(patient=patient1, department=department)
        self.create_patient_department_sharing(patient=patient2, department=department)
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=later
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=later
        )

        query = {"q": dob1.strftime("%m/%d/%Y").lstrip("0").replace(" 0", " ")}
        response = self.client.get(self.uri, data=query)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], patient1.pk)

    def test_mrn_query(self):
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        mrn1 = "MRN1"
        mrn2 = "MRN2"
        later = timezone.now()
        earlier = later - timedelta(hours=36)
        patient1 = self.create_patient(mrn=mrn1)
        patient2 = self.create_patient(mrn=mrn2)
        self.create_patient_department_sharing(patient=patient1, department=department)
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=later
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=later
        )

        query = {"q": mrn1}
        response = self.client.get(self.uri, data=query)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], patient1.pk)

    def test_mrn_no_match(self):
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        mrn1 = "MRN1"
        mrn2 = "MRN2"
        later = timezone.now()
        earlier = later - timedelta(hours=36)
        patient1 = self.create_patient(mrn=mrn1)
        patient2 = self.create_patient(mrn=mrn2)
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=later
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=later
        )

        query = {"q": "FaKeMrN"}
        response = self.client.get(self.uri, data=query)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_partial_dob_match(self):
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        dob1 = date(1990, 5, 20)
        dob2 = date(1991, 5, 24)
        later = timezone.now()
        earlier = later - timedelta(hours=36)
        patient1 = self.create_patient(
            date_of_birth=dob1
        )
        patient2 = self.create_patient(
            date_of_birth=dob2
        )
        self.create_patient_department_sharing(patient=patient1, department=department)
        self.create_patient_department_sharing(patient=patient2, department=department)
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=later
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=later
        )

        query = {"q": "05/20"}
        response = self.client.get(self.uri, data=query)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], patient1.pk)

    def test_multiple_partial_dob_match(self):
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        dob1 = date(1990, 5, 20)
        dob2 = date(1991, 5, 20)
        later = timezone.now()
        earlier = later - timedelta(hours=36)
        patient1 = self.create_patient(
            date_of_birth=dob1
        )
        patient2 = self.create_patient(
            date_of_birth=dob2
        )
        self.create_patient_department_sharing(patient=patient1, department=department)
        self.create_patient_department_sharing(patient=patient2, department=department)
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=later
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=later
        )

        query = {"q": "5/20"}
        response = self.client.get(self.uri, data=query)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(patient1.pk in (response.data[0]["id"], response.data[1]["id"]))
        self.assertTrue(patient2.pk in (response.data[0]["id"], response.data[1]["id"]))

    def test_single_digit_partial_dob_match(self):
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        dob1 = date(1990, 1, 2)
        dob2 = date(1991, 1, 2)
        later = timezone.now()
        earlier = later - timedelta(hours=36)
        patient1 = self.create_patient(
            date_of_birth=dob1
        )
        patient2 = self.create_patient(
            date_of_birth=dob2
        )
        self.create_patient_department_sharing(patient=patient1, department=department)
        self.create_patient_department_sharing(patient=patient2, department=department)
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=later
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=later
        )

        query = {"q": "1/2"}
        response = self.client.get(self.uri, data=query)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(patient1.pk in (response.data[0]["id"], response.data[1]["id"]))
        self.assertTrue(patient2.pk in (response.data[0]["id"], response.data[1]["id"]))

    def test_solo_single_digit_partial_dob_match(self):
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        dob1 = date(1990, 1, 2)
        dob2 = date(1991, 1, 20)
        later = timezone.now()
        earlier = later - timedelta(hours=36)
        patient1 = self.create_patient(
            date_of_birth=dob1
        )
        patient2 = self.create_patient(
            date_of_birth=dob2
        )
        self.create_patient_department_sharing(patient=patient1, department=department)
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=later
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient2, timestamp=later
        )

        query = {"q": "1/2"}
        response = self.client.get(self.uri, data=query)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], patient1.pk)

    def test_missing_dob_match(self):
        department = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            )
            .get(department__name="unassigned")
            .department
        )
        dob1 = None
        later = timezone.now()
        earlier = later - timedelta(hours=36)
        patient1 = self.create_patient(
            date_of_birth=dob1
        )
        self.create_patient_department_sharing(patient=patient1, department=department)
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=earlier
        )
        self.create_activate_record(
            technician=self.technician, patient=patient1, timestamp=later
        )

        query = {"q": "10/1"}
        response = self.client.get(self.uri, data=query)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class TestTechnicianPatientsViewSetAPI(JasprApiTestCase):
    serializer_class = ActivateNewPatientSerializer
    def setUp(self):
        super().setUp()

        self.uri = "/v1/technician/patients"
        self.technician = self.create_technician()
        self.department_technician = (
            self.technician.departmenttechnician_set.select_related(
                "department"
            ).get(department__name="unassigned")
        )
        self.department = self.department_technician.department
        self.clinic = self.department.clinic
        self.system = self.clinic.system
        self.set_technician_creds(self.technician)

    def test_create_patient_with_ssid(self):
        data = {
            "ssid": "Patient-1",
            "department": self.department.pk
        }

        response = self.client.post(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient = Patient.objects.all().first()
        self.assertEqual(patient.user.email, "ssid-patient-1.jaspr@jasprhealth.com")
        self.assertEqual(patient.ssid, "Patient-1")
        self.assertEqual(patient.departments[0], self.department.id)
        self.assertEqual(patient.first_name, "")
        self.assertEqual(patient.last_name, "")
        self.assertIsNone(patient.date_of_birth, "")
        self.assertEqual(patient.mrn, "")

    def test_create_patient_with_mrn(self):
        data = {
            "mrn": "Patient-5",
            "firstName": "Buggz",
            "lastName": "Bunny",
            "dateOfBirth": "1967-08-25",
            "department": self.department.pk
        }

        response = self.client.post(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        patient = Patient.objects.all().first()
        self.assertTrue(patient.user.email.endswith(".jaspr@jasprhealth.com"))
        self.assertEqual(patient.ssid, None)
        self.assertEqual(patient.departments[0], self.department.id)
        self.assertEqual(patient.first_name, "Buggz")
        self.assertEqual(patient.last_name, "Bunny")
        self.assertEqual(patient.date_of_birth, datetime.date(1967, 8, 25))
        self.assertEqual(patient.mrn, "Patient-5")

    def test_create_and_search_patient_with_mrn(self):
        data = {
            "mrn": "Patient-5",
            "firstName": "Buggz",
            "lastName": "Bunny",
            "dateOfBirth": "1967-08-25",
            "department": self.department.pk
        }
        response = self.client.post(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        search_response = self.client.get(self.uri, data={"q": data["mrn"]})
        self.assertEqual(search_response.status_code, status.HTTP_200_OK, search_response.data)
        self.assertEqual(len(search_response.data), 1)

    def test_no_ssid_or_mrn_provided(self):
        data = {"department": self.department.id}
        response = self.client.post(self.uri, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("ssid", response.data)
        self.assertNotIn("mrn", response.data)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "When SSID is not provided 'First Name', 'Last Name', 'Date of Birth', and 'MRN' are required.",
        )

    def test_ssid_and_mrn_provided(self):
        data = {
            "ssid": "247",
            "mrn": "1",
            "department": self.department.id,
        }
        response = self.client.post(self.uri, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("ssid", response.data)
        self.assertNotIn("mrn", response.data)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Patients cannot have an SSID and any of 'First Name', 'Last Name', 'Date of Birth', or 'MRN'.",
        )

    def test_mrn_provided_but_not_other_fields(self):
        data = {"mrn": "1", "department": self.department.id}
        response = self.client.post(self.uri, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("ssid", response.data)
        self.assertNotIn("mrn", response.data)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "When MRN is provided 'First Name', 'Last Name', and 'Date of Birth', are required.",
        )

    def test_invalid_ssid_too_many_characters(self):
        """
        Does an SSID with too many characters return the correct validation error?
        """
        data = {
            "ssid": "1" * 26,
            "department": self.department.id,
        }
        response = self.client.post(self.uri, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ssid", response.data)
        self.assertIn("25", response.data["ssid"][0])

    def test_invalid_ssid_no_regex_match(self):
        """
        Does an SSID that doesn't match the regex in the `RegexValidator` return the
        correct validation error?
        """
        data = {
            "ssid": "aA0-_&$%",
            "department": self.department.id,
        }
        response = self.client.post(self.uri, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ssid", response.data)
        self.assertIn(
            "SSIDs can only contain letters, numbers, hyphens, and underscores.",
            response.data["ssid"][0],
        )

    def test_create_patient_while_token_missing_after_authentication(self):
        """
        Does duplicate technician fail gracefully activating patient at same time as its clone?

        UPDATE: After migrating away from single session only expiring tokens, this test
        still passed exactly as is.
        """
        data = {
            "ssid": "Patient-1",
            "department": self.department.id,
        }

        def run_before(*a, **k):
            response = self.client.post(self.uri, data=data)
            self.assertEqual(
                response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
            )

        with before_after.before(
            "jaspr.apps.accounts.models.LoggedOutAuthToken.objects.create",
            run_before,
        ):
            self.client.post(self.uri, data=data)

    def test_create_patient_with_already_existing_ssid(self):
        patient = self.create_patient(
            ssid="old-patient", department=self.department
        )

        data = {
            "ssid": "old-patient",
            "department": self.department.id,
        }

        response = self.client.post(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT, response.data)

        exception = PatientAlreadyExistsError(patient=patient)

        expected = {
            "message": str(exception),
            "object": {
                "id": patient.pk,
                "analytics_token": str(patient.analytics_token),
                "current_encounter": None,
                "current_encounter_created": None,
                "current_encounter_department": None,
                "first_name": "",
                "last_name": "",
                "date_of_birth": None,
                "email": "",
                "mobile_phone": "",
                "mrn": "",
                "activities": {"csa": False, "csp": False, "skills": False},
                "ssid": "old-patient",
                "suggest_new_encounter": None,
                "departments": [self.department.pk],
                "last_logged_in_at": None,
                "tools_to_go_status": "Not Started",
                "tour_complete": False,
                "created": zulu_time_format(patient.created),
            },
        }
        self.maxDiff = None
        self.assertDictEqual(expected, response.data)

    def test_create_patient_with_already_existing_ssid_in_other_clinic(self):
        """ Does a technician get generic error for patients with other clinic location. """
        dept2 = self.create_department(name="dept 2")
        patient = self.create_patient(ssid="old-patient")  # other clinic id = 2
        self.create_patient_department_sharing(department=dept2, patient=patient)
        self.create_department_technician(department=dept2, technician=self.technician)

        data = {
            "ssid": "old-patient",
            "department": self.department.id,
        }

        response = self.client.post(self.uri, data=data)
        self.assertEqual(
            response.status_code, status.HTTP_409_CONFLICT, response.data
        )

        self.assertEqual(
            "The information entered matches an existing patient record.",
            response.data["message"],
        )


    def test_create_patient_with_already_existing_user_jaspr_email(self):
        data = {
            "ssid": "246",
            "department": self.department.id,
        }
        # Create a `Patient` via the API using the activate new patient endpoint
        # here, which should set the underlying user's `email` to
        # '246.jaspr@jasprhealth.com'.
        self.client.post(self.uri, data=data)
        # We need to re-login the `Technician` since the activate endpoint logs out the
        # `Technician`, returning the token for the `Patient`.
        old_patient = Patient.objects.get(ssid="246")
        old_patient.delete()
        # Clear the credentials, so that we don't get a 401 response from submitting
        # with an expired token.
        self.client.credentials()
        # Now set the credentials again, getting the new token.
        self.set_technician_creds(self.technician)
        response = self.client.post(self.uri, data=data)

        # Even though `old_patient` was deleted, the underlying `User`'s email
        # '246.jaspr@jasprhealth.com' will still be exist/be there, because the
        # underlying `User` isn't deleted, so that SSID is still considered taken, so
        # we show the same error message.
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )
        self.assertEqual(
            ActivateNewPatientSerializer.default_error_messages["generic"],
            response.data["non_field_errors"][0],
        )

    def test_wrong_clinic(self):
        """
        `Patient`'s clinic location does not belong to the `Technician`'s clinic.
        """
        other_system = self.create_healthcare_system(name="Other System")
        other_clinic = self.create_clinic(name="Other Clinic", system=other_system)
        other_department = self.create_department(name="Other Dept", clinic=other_clinic)
        data = {
            "ssid": "Patient-1",
            "department": other_department.id,
        }
        response = self.client.post(self.uri, data=data)

        assert_validation_error_thrown(
            self, response, "department", "improper_department"
        )

    def test_wrong_department_within_clinic(self):
        """
        `Patient`'s clinic location does not correspond to one of the `Technician`s
        `ClinicLocationTechnician` records.
        """
        other_department_within_clinic = self.create_department(
            name="other dept",
            clinic=self.clinic
        )
        data = {
            "ssid": "Patient-1",
            "department": other_department_within_clinic.id,
        }
        response = self.client.post(self.uri, data=data)

        assert_validation_error_thrown(
            self, response, "department", "improper_department"
        )

    def test_correct_department_but_not_active(self):
        """
        `Patient`'s clinic location corresponds to one of the `Technician`s
        `ClinicLocationTechnician` records but the record is not active?
        """
        department = self.create_department(name="Dept.", clinic=self.clinic)
        self.department_technician = self.create_department_technician(
            department=department,
            technician=self.technician,
            status="inactive",
        )
        patient = self.create_patient(department=department)
        data = {
            "ssid": "Patient-1",
            "department": department.id,
        }
        response = self.client.post(self.uri, data=data)

        assert_validation_error_thrown(self, response, "department", ...)