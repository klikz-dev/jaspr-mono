from datetime import datetime, timedelta

from django.utils import timezone
from django.utils.functional import cached_property
from freezegun import freeze_time
from rest_framework import serializers, status

from jaspr.apps.kiosk.models import Patient, Technician, ProviderComment
from jaspr.apps.test_infrastructure.permissions_testcases import (
    JasprTestResourcePermissions,
)
from jaspr.apps.test_infrastructure.testcases import (
    JasprApiTestCase,
    JasprApiTransactionTestCase,
)


class TestTechnicianPatientProviderCommentsAPIPermissions(JasprTestResourcePermissions):
    """ Test for 401, 403, 404, 405 """

    # NOTE: Careful if/when debugging about this getting evaluated in the debugger
    # before `super().setUp` is called.
    @cached_property
    def patient(self) -> Patient:
        self.system = self.create_healthcare_system(name="Permissions Clinic")
        self.clinic = self.create_clinic(name="Clinic 1", system=self.system)
        self.department = self.create_department(
            clinic=self.clinic, name="Permissions Clinic Location"
        )
        patient = self.create_patient()
        encounter = self.create_patient_encounter(
            patient=patient, department=self.department
        )

        return patient

    def technician_factory_for_this_test(self) -> Technician:
        if getattr(self, "created_technician", None) is None:
            self.created_technician = self.create_technician(
                system=self.system, department=self.department
            )
        return self.created_technician

    # NOTE: If `JasprTestResourcePermissions` gets refactored to a significant degree,
    # this might break. Should be easy to tweak in that case if needed.
    def provider_comment_factory_for_this_test(self) -> ProviderComment:
        # Make sure this line is here so that the `self.patient` `@cached_property`
        # gets evaluated before anything else.
        current_encounter = self.patient.current_encounter
        return self.create_provider_comment(
            encounter=current_encounter,
            technician=self.technician_factory_for_this_test(),
        )

    def setUp(self):
        super().setUp(
            resource_pattern="technician/encounter/{encounter_id}/provider-comments",
            version_prefix="v1",
            factory_name="provider_comment_factory_for_this_test",
        )

        self.base_uri = self.base_uri.format(encounter_id=self.patient.current_encounter.pk)
        self.detail_uri = self.detail_uri.format(encounter_id=self.patient.current_encounter.pk)
        self.action_group_map["list"]["allowed_groups"] = ["Technician"]
        self.action_group_map["create"]["allowed_groups"] = ["Technician"]
        self.action_group_map["delete"]["allowed_groups"] = ["Technician"]
        self.action_group_map["update"]["allowed_groups"] = ["Technician"]
        self.action_group_map["retrieve"]["allowed_groups"] = ["Technician"]
        del self.action_group_map["partial_update"]
        self.groups["Technician"]["factory"] = self.technician_factory_for_this_test
#
#
# class TestTechnicianPatientAmendmentAPI(JasprApiTestCase):
#     def setUp(self):
#         super().setUp()
#         self.uri = "/v1/technician/patients/{patient_id}/amendments/{amendment_id}"
#         self.system = self.create_healthcare_system(name="Amendment System")
#         self.clinic = self.create_clinic(name="Amendment Clinic", system=self.system)
#         self.department = self.create_department(
#             clinic=self.clinic, name="Amendment Clinic Location"
#         )
#         self.patient = self.create_patient(department=self.department)
#         self.encounter = self.create_patient_encounter(
#             patient=self.patient, department=self.department
#         )
#         self.encounter.get_current_session()
#         self.patient_session = self.patient.current_patient_session
#         self.technician = self.create_technician(
#             system=self.system, department=self.department
#         )
#         self.set_technician_creds(self.technician)
#
#     def prepare_full_uri(self, patient_id: int, amendment_id: int = None) -> str:
#         prepared_url = self.uri.format(patient_id=patient_id, amendment_id=amendment_id)
#         if amendment_id is None:
#             # Remove `"/None"` from the end.
#             return prepared_url[: -(1 + len(str(None)))]
#         return prepared_url
#
#     def make_amendment(self, **kwargs) -> Amendment:
#         kwargs.setdefault("patient_session", self.patient_session)
#         kwargs.setdefault("technician", self.technician)
#         return self.create_amendment(**kwargs)
#
#     @cached_property
#     def datetime_field_instance(self) -> serializers.DateTimeField:
#         return serializers.DateTimeField()
#
#     def stringify_datetime(self, dt: datetime) -> str:
#         return self.datetime_field_instance.to_representation(dt)
#
#     def test_technician_can_list_amendments_belonging_to_patients_current_patient_session(
#         self,
#     ):
#         other_patient = self.create_patient(department=self.department)
#         other_patient_encounter = self.create_patient_encounter(
#             patient=other_patient, department=self.department
#         )
#         other_patient_encounter.create_new_session()
#         other_patient_session = other_patient.current_patient_session
#         other_technician = self.create_technician(
#             system=self.system, department=self.department
#         )
#
#         now = timezone.now()
#         a_second_ago = now - timedelta(seconds=1)
#         two_seconds_ago = now - timedelta(seconds=2)
#         amendment1 = self.make_amendment(created=a_second_ago)
#         amendment2 = self.make_amendment(created=now)
#         amendment3 = self.make_amendment(
#             technician=other_technician, created=two_seconds_ago
#         )
#         # Make sure these aren't included in the response.
#         self.make_amendment(
#             patient_session=other_patient_session, technician=self.technician
#         )
#         self.create_amendment()
#         uri = self.prepare_full_uri(self.patient.id)
#         response = self.client.get(uri)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(
#             response.data,
#             [
#                 {
#                     "id": amendment2.id,
#                     "comment": amendment2.comment,
#                     "created": self.stringify_datetime(now),
#                     "modified": self.stringify_datetime(amendment2.modified),
#                     "technician": {
#                         "id": self.technician.id,
#                         "email": self.technician.user.email,
#                         "can_edit": True,
#                     },
#                 },
#                 {
#                     "id": amendment1.id,
#                     "comment": amendment1.comment,
#                     "created": self.stringify_datetime(a_second_ago),
#                     "modified": self.stringify_datetime(amendment1.modified),
#                     "technician": {
#                         "id": self.technician.id,
#                         "email": self.technician.user.email,
#                         "can_edit": True,
#                     },
#                 },
#                 {
#                     "id": amendment3.id,
#                     "comment": amendment3.comment,
#                     "created": self.stringify_datetime(two_seconds_ago),
#                     "modified": self.stringify_datetime(amendment3.modified),
#                     "technician": {
#                         "id": other_technician.id,
#                         "email": other_technician.user.email,
#                         "can_edit": False,
#                     },
#                 },
#             ],
#         )
#
#     def test_technician_can_create_amendment(self):
#         now = timezone.now()
#         other_amendment = self.make_amendment(comment="Here's a comment.")
#         uri = self.prepare_full_uri(self.patient.id)
#         response = self.client.post(uri, data={"comment": "Here's another comment."})
#
#         amendment = Amendment.objects.exclude(pk=other_amendment.pk).get()
#         self.assertEqual(
#             response.data,
#             {
#                 "id": amendment.id,
#                 "comment": "Here's another comment.",
#                 "created": self.stringify_datetime(amendment.created),
#                 "modified": self.stringify_datetime(amendment.modified),
#                 "technician": {
#                     "id": self.technician.id,
#                     "email": self.technician.user.email,
#                     "can_edit": True,
#                 },
#             },
#         )
#         self.assertGreaterEqual(amendment.created, now)
#
#     def test_technician_can_edit_amendment_that_technician_created(self):
#         now = timezone.now()
#         with freeze_time(now - timedelta(seconds=1)):
#             amendment = self.make_amendment(comment="Here's a comment.")
#         uri = self.prepare_full_uri(self.patient.id, amendment.id)
#         before_update = timezone.now()
#         response = self.client.put(uri, data={"comment": "Here's an updated comment."})
#
#         amendment.refresh_from_db()
#         self.assertEqual(
#             response.data,
#             {
#                 "id": amendment.id,
#                 "comment": "Here's an updated comment.",
#                 "created": self.stringify_datetime(amendment.created),
#                 "modified": self.stringify_datetime(amendment.modified),
#                 "technician": {
#                     "id": self.technician.id,
#                     "email": self.technician.user.email,
#                     "can_edit": True,
#                 },
#             },
#         )
#         self.assertEqual(amendment.created, now - timedelta(seconds=1))
#         self.assertGreaterEqual(amendment.modified, now)
#
#     def test_technician_can_delete_amendment_that_technician_created(self):
#         now = timezone.now()
#         with freeze_time(now - timedelta(seconds=1)):
#             amendment = self.make_amendment(comment="Here's a comment.")
#         uri = self.prepare_full_uri(self.patient.id, amendment.id)
#         before_update = timezone.now()
#         response = self.client.delete(uri)
#
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         amendment.refresh_from_db()
#         self.assertEqual(amendment.status, "deleted")
#         self.assertEqual(amendment.created, now - timedelta(seconds=1))
#         self.assertGreaterEqual(amendment.modified, now)
#
#     def test_technician_cannot_edit_amendment_that_other_technician_created(self):
#         other_technician = self.create_technician(
#             system=self.system, department=self.department
#         )
#         amendment = self.make_amendment(
#             technician=other_technician, comment="Here's a comment."
#         )
#         uri = self.prepare_full_uri(self.patient.id, amendment.id)
#         response = self.client.put(uri, data={"comment": "Here's an updated comment."})
#
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_technician_cannot_delete_amendment_that_other_technician_created(self):
#         other_technician = self.create_technician(
#             system=self.system, department=self.department
#         )
#         amendment = self.make_amendment(
#             technician=other_technician, comment="Here's a comment."
#         )
#         uri = self.prepare_full_uri(self.patient.id, amendment.id)
#         response = self.client.delete(uri)
#
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_technician_forbidden_from_managing_amendments_if_no_shared_clinic(self):
#         other_system = self.create_healthcare_system(name="Some Other Clinic")
#         other_clinic = self.create_clinic(name="Other Clinic", system=other_system)
#         other_department = self.create_department(
#             clinic=other_clinic, name="Some Other Clinic Location"
#         )
#         # Create a different `Technician`, which will be at a different clinic than
#         # `self.technician` by default.
#         technician = self.create_technician(
#             system=other_system, department=other_department
#         )
#         self.set_technician_creds(technician)
#         # Hits two separate views.
#         for case in ("list", "update"):
#             with self.subTest(case=case):
#                 if case == "list":
#                     uri = self.prepare_full_uri(self.patient.id)
#                     response = self.client.get(uri)
#                 else:
#                     amendment = self.make_amendment(technician=technician)
#                     uri = self.prepare_full_uri(self.patient.id, amendment.id)
#                     response = self.client.put(uri, data={"comment": "updated comment"})
#
#                 self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
