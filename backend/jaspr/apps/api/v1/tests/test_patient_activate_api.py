import datetime
from collections import OrderedDict


from django.utils import timezone
from knox.models import AuthToken
from rest_framework import status

from jaspr.apps.api.v1.serializers import (
    ActivateExistingPatientSerializer,
    ActivateNewPatientSerializer,
    ReadOnlyAuthTokenSerializer,
)
from jaspr.apps.kiosk.models import ActivateRecord, Patient
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase


from ..helpers import zulu_time_format
from .helpers import (
    assert_auth_token_string_valid,
    assert_kiosk_instance_logged_out,
    assert_patient_logged_in,
    assert_validation_error_thrown,
    patient_before_login_setup_kwargs,
)


class TestTechnicianActivatePatientAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    def setUp(self):
        super().setUp(
            resource_pattern="technician/activate-patient",
            version_prefix="v1",
        )

        self.action_group_map["create"]["allowed_groups"] = ["Technician"]



class TestTechnicianActivatePatientAPIExisting(JasprApiTestCase):
    serializer_class = ActivateExistingPatientSerializer

    def setUp(self):
        super().setUp()

        self.technician = self.create_technician()
        self.uri = "/v1/technician/activate-patient"
        self.department_technician = (
            self.technician.departmenttechnician_set.get(department__name="unassigned")
        )
        self.department = self.department_technician.department
        self.clinic = self.department.clinic
        self.system = self.clinic.system
        self.set_technician_creds(self.technician)

    def test_technician_can_activate_existing_patient_by_pk(self):
        """
        Can the technician activate existing patient by `pk` providing the `patient` `pk`?
        """
        patient = self.create_patient(
            **patient_before_login_setup_kwargs(),
            ssid="Existing",
            department=self.department,
        )
        encounter = self.create_patient_encounter(patient=patient)
        encounter.last_heartbeat = timezone.now() - datetime.timedelta(minutes=11)
        encounter.session_lock = True
        encounter.session_validation_attempts = 5
        encounter.save()

        data = {
            "new": False,
            "patient": patient.pk,
            "department": self.department.id,
        }

        time_before = timezone.now()
        response = self.client.post(self.uri, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        assert_auth_token_string_valid(self, response.data["token"], patient)
        auth_token = AuthToken.objects.get(user=patient.user)
        self.assertIs(auth_token.jaspr_session.in_er, True)
        # NOTE: If `Technician` native app support ever gets implemented, we could do
        # something like update this test to randomly specify `from_native` or not and
        # makes sure the value here is consistent with that (basically, if the
        # `Technician` is `from_native`, then we assume the `Patient` is also
        # `from_native` since at the time of writing it's a physical handoff).
        self.assertIs(auth_token.jaspr_session.from_native, False)
        self.assertIs(auth_token.jaspr_session.long_lived, False)
        self.assertEqual(
            response.data,
            ReadOnlyAuthTokenSerializer(
                auth_token, context={"token_string": response.data["token"]}
            ).data,
        )

        self.assertEqual(
            ActivateRecord.objects.filter(
                technician=self.technician, patient=patient, new=False
            ).count(),
            1,
        )
        assert_kiosk_instance_logged_out(self, self.technician, True, time_before)

        patient.refresh_from_db()
        encounter.refresh_from_db()
        assert_patient_logged_in(self, patient, True, time_before, encounter=encounter)

    def test_wrong_department(self):
        """
        `Patient`'s clinic location does not belong to the `Technician`'s clinic.
        """
        other_system = self.create_healthcare_system(name="Other System")
        other_clinic = self.create_clinic(name="other Clinci", system=other_system)
        other_department = self.create_department(name="Other Dept", clinic=other_clinic)
        patient = self.create_patient(department=other_department)
        data = {
            "patient": patient.pk,
            "department": self.department.id,
        }
        response = self.client.post(self.uri, data=data)

        assert_validation_error_thrown(
            self, response, "non_field_errors", "department_mismatch"
        )

    def test_wrong_department_within_clinic(self):
        """
        `Patient`'s clinic location does not correspond to one of the `Technician`s
        `ClinicLocationTechnician` records?
        """
        other_department_within_clinic = self.create_department(
            name="One More Dept.",
            clinic=self.clinic
        )
        patient = self.create_patient(
            department=other_department_within_clinic
        )
        data = {
            "patient": patient.pk,
            "department": other_department_within_clinic.id,
        }
        response = self.client.post(self.uri, data=data)

        assert_validation_error_thrown(
            self, response, "department", "improper_department"
        )

    def test_correct_department_but_not_active(self):
        """
        `Patient`'s department corresponds to one of the `Technician`s
        `ClinicLocationTechnician` records but the record is not active?
        """
        department = self.create_department(name="Another Dept", clinic=self.clinic)
        self.department_technician = self.create_department_technician(
            department=department,
            technician=self.technician,
            status="inactive",
        )
        patient = self.create_patient(department=department)
        data = {
            "patient": patient.pk,
            "department": department.id,
        }
        response = self.client.post(self.uri, data=data)

        assert_validation_error_thrown(self, response, "department", "improper_department")

    def test_department_does_not_match_patients(self):
        """
        The clinic location corresponds to one of the `Technician`s
        `ClinicLocationTechnician` records but does not match the `Patient`s clinic
        location.
        """
        other_department = self.create_department(name="Other Dept.", clinic=self.clinic)
        patient = self.create_patient(department=other_department)
        data = {
            "patient": patient.pk,
            "department": self.department.id,
        }
        response = self.client.post(self.uri, data=data)

        assert_validation_error_thrown(
            self, response, "non_field_errors", "department_mismatch"
        )

    def test_department_valid_but_no_patient_with_pk(self):
        """
        The clinic location corresponds to one of the `Technician`s
        `ClinicLocationTechnician` records but the provided `pk` does not correspond
        to any existing `Patient`.
        """
        self.set_technician_creds(self.technician)
        patient = self.create_patient()
        pk = patient.pk
        assert pk and isinstance(pk, int)
        patient.delete()
        data = {
            "patient": pk,
            "department": self.department.id,
        }
        response = self.client.post(self.uri, data=data)

        assert_validation_error_thrown(self, response, "patient", ...)
