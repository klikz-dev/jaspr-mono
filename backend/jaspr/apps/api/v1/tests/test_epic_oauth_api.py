import jwt
import responses
import secrets
import time
from datetime import timedelta

from urllib.parse import urlparse, parse_qs
from django.utils import timezone
from django.conf import settings
from django.core.cache import cache
from jaspr.apps.clinics.models import DepartmentTechnician
from jaspr.apps.epic.models import EpicSettings, EpicDepartmentSettings, PatientEhrIdentifier
from jaspr.apps.kiosk.models import Encounter, Patient, PatientDepartmentSharing, Technician
from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from rest_framework import status


authorize_url = "https://fakeprovider.com/fhir/oauth2/authorize"
token_url = "https://fakeprovider.com/fhir/oauth2/token"
iss_metadata = {
    "rest": [
        {
            "security": {
                "extension": [
                    {
                        "extension": [
                            {
                                "valueUri": authorize_url,
                                "url": "authorize"
                            },
                            {
                                "valueUri": token_url,
                                "url": "token"
                            }
                        ],
                    }
                ],
            }
        }
    ]
}


class TestEpicOauthRedirectAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.uri = "/v1/technician/epic/oauth"

    @responses.activate
    def test_epic_redirect_returns_correct_response(self):
        responses.add(responses.GET, 'https://fakeprovider.com/metadata',
                      json=iss_metadata, status=status.HTTP_200_OK)

        iss="https://fakeprovider.com"
        launch_token="ey.launchtokenjwt"

        response = self.client.get(f"{self.uri}?iss={iss}&launch={launch_token}",
                                   headers={"Accept": "application/json+fhir"})
        status_code = response.status_code
        query = parse_qs(response.url)
        url = urlparse(response.url)

        self.assertEqual(status_code, 302, "Redirect status code given")
        self.assertEqual(query["launch"][0], launch_token, "Launch token set in query parameters")
        self.assertEqual(f"{url.scheme}://{url.netloc}{url.path}", authorize_url,
                         "Authorize token url correctly fetched from metadata")


class TestEpicOauthLoginAPI(JasprApiTestCase):
    def setUp(self):
        super().setUp()

        self.system = self.create_healthcare_system(name="Epic Health System")
        self.clinic = self.create_clinic(name="Clinic 1", system=self.system)
        self.department = self.create_department(
            clinic=self.clinic, name="Epic Department Location"
        )
        self.epic_settings = EpicSettings.objects.create(name="Epic System", provider="Epic")
        self.epic_department_settings = EpicDepartmentSettings.objects.create(
            epic_settings=self.epic_settings,
            department=self.department,
            location_code="valid_location",
        )

        self.auth_response = {
            "access_token": "ey.jwt...",
            "token_type": "bearer",
            "expires_in": 3600,
            "scope": "user/DocumentReference.Write user/Patient.Read user/Practitioner.Read launch",
            "state": "abcrandomnumber123",
            "csn": "35886",
            "dob": "19851011",
            "dept_id": self.epic_department_settings.location_code,
            "location": "fhir82620691",
            "encounter": "fhir12345",
            "encounter_date": "2020-09-10",
            "mrn": "ABCD123",
            "patient": "fhir8526",
            "patient_fhir_id": "fhir8526",
            "patient_first_name": "Jonny",
            "patient_last_name": "Jones",
            "practitioner_fhir_id": "fhir59198465",
            "practitioner_first_name": "Sally",
            "practitioner_last_name": "Sue",
        }

        responses.add(responses.GET, 'https://fakeprovider.com/metadata',
                      json=iss_metadata, status=status.HTTP_200_OK)

        responses.add(responses.POST, "https://fakeprovider.com/fhir/oauth2/token",
                      json=self.auth_response, status=status.HTTP_200_OK)

        self.oauth_session_state = secrets.token_urlsafe(32)
        self.iss = "https://fakeprovider.com"

        self.uri = "/v1/technician/epic-oauth-login"
        self.now = timezone.now()
        self.future = self.now + timedelta(minutes=5)

        private_key = settings.JASPR_PRIVATE_KEY
        epoch_time = int(time.time())

        self.encoded_jwt = jwt.encode(
            {
                "sub": self.oauth_session_state,
                "exp": epoch_time + (60 * 4),
                "nbf": epoch_time - 60,
                "iat": epoch_time,
            },
            private_key,
            algorithm="RS384",
        )

        cache.set(
            f"oauth-session-{self.oauth_session_state}",
            self.iss,
            timeout=60 * 5
        )

    @responses.activate
    def test_epic_oauth_login_can_get_session_and_validate_successfully(self):
        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_epic_oauth_fails_successfully_if_session_not_found(self):
        self.client.session.flush()
        cache.delete(f"oauth-session-{self.oauth_session_state}")
        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["nonFieldErrors"][0], "Validation state is not set on the user session")


    def test_epic_oauth_fails_successfully_if_session_state_invalid(self):
        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": "INVALID STATE"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["nonFieldErrors"][0], "Validation state is not valid")

    @responses.activate
    def test_epic_oauth_unavailable_department_fails_successfully(self):
        auth_response = self.auth_response
        auth_response["dept_id"] = "UNKNOWN_LOCATION"
        responses.replace(responses.POST, token_url,
                      json=auth_response, status=status.HTTP_200_OK)

        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"], "Unable to find department")

    @responses.activate
    def test_epic_oauth_patient_created_successfully(self):
        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        qs = PatientEhrIdentifier.objects.filter(
            fhir_id=self.auth_response["patient_fhir_id"], epic_settings=self.epic_settings
        )
        patient_identifier = qs.first()
        self.assertEqual(qs.count(), 1)

        patient = patient_identifier.patient
        self.assertIsNotNone(self.department in patient.departments)
        self.assertEqual(patient.first_name, "Jonny")
        self.assertEqual(patient.last_name, "Jones")
        self.assertEqual(PatientDepartmentSharing.objects.filter(patient=patient).count(), 1)

    @responses.activate
    def test_epic_oauth_validation_fails_successfully(self):
        auth_response = self.auth_response
        del auth_response["patient_fhir_id"]
        responses.replace(responses.POST, token_url,
                          json=auth_response, status=status.HTTP_200_OK)

        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["patientFhirId"][0], "This field is required.")

    @responses.activate
    def test_epic_oauth_technician_created_successfully(self):
        responses.replace(responses.POST, token_url,
                          json=self.auth_response, status=status.HTTP_200_OK)

        self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        technician = Technician.objects.get(fhir_id=self.auth_response["practitioner_fhir_id"])
        self.assertIsNotNone(technician)
        self.assertEqual(technician.departmenttechnician_set.filter(department=self.department).count(), 1)
        self.assertIn("Technician", list(technician.user.groups.all().values_list('name', flat=True)))

    @responses.activate
    def test_epic_oauth_existing_technician_added_to_new_department(self):
        technician = self.create_technician(
            fhir_id=self.auth_response["practitioner_fhir_id"],
            system=self.department.clinic.system,
            department=self.department,
            first_name=self.auth_response["practitioner_first_name"],
            last_name=self.auth_response["practitioner_last_name"]
        )

        department2 = self.create_department(
            clinic=self.clinic, name="Epic Department Location 2"
        )

        epic_department_settings2 = EpicDepartmentSettings.objects.create(
            epic_settings=self.epic_settings,
            department=department2,
            location_code="valid_location_2",
        )

        auth_response = self.auth_response
        auth_response["dept_id"] = epic_department_settings2.location_code

        responses.replace(responses.POST, token_url,
                          json=auth_response, status=status.HTTP_200_OK)

        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DepartmentTechnician.objects.filter(technician=technician).count(), 2)

    @responses.activate
    def test_epic_oauth_existing_technician_returns(self):
        technician = self.create_technician(
            fhir_id=self.auth_response["practitioner_fhir_id"],
            system=self.department.clinic.system,
            department=self.department,
            first_name=self.auth_response["practitioner_first_name"],
            last_name=self.auth_response["practitioner_last_name"]
        )

        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DepartmentTechnician.objects.filter(technician=technician).count(), 1)

    @responses.activate
    def test_epic_oauth_new_patient_created(self):
        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        pei = PatientEhrIdentifier.objects.get(
            fhir_id=self.auth_response["patient_fhir_id"],
            epic_settings=self.epic_settings,
        )
        patient = pei.patient
        pds = PatientDepartmentSharing.objects.filter(patient=patient, department=self.department)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(patient)
        self.assertEqual(pds.count(), 1)

    @responses.activate
    def test_epic_oauth_existing_patient_encounter_returns(self):
        patient = self.create_patient()
        PatientDepartmentSharing.objects.create(patient=patient, department=self.department)
        PatientEhrIdentifier.objects.create(
            patient=patient,
            fhir_id=self.auth_response["patient_fhir_id"],
            epic_settings=self.epic_settings,
        )
        Encounter.objects.create(
            patient=patient,
            fhir_id=self.auth_response["encounter"],
            department=self.department
        )

        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Encounter.objects.filter(patient=patient).count(), 1)
        self.assertEqual(PatientEhrIdentifier.objects.filter(patient=patient).count(), 1)
        self.assertEqual(PatientDepartmentSharing.objects.filter(patient=patient).count(), 1)

    @responses.activate
    def test_epic_oauth_existing_patient_returns_to_department_for_new_encounter(self):
        patient = self.create_patient()
        PatientDepartmentSharing.objects.create(patient=patient, department=self.department)
        PatientEhrIdentifier.objects.create(
            patient=patient,
            fhir_id=self.auth_response["patient_fhir_id"],
            epic_settings=self.epic_settings,
        )
        Encounter.objects.create(
            patient=patient,
            fhir_id="old_encounter_id",
            department=self.department
        )

        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Encounter.objects.filter(patient=patient).count(), 2)
        self.assertEqual(PatientEhrIdentifier.objects.filter(patient=patient).count(), 1)
        self.assertEqual(PatientDepartmentSharing.objects.filter(patient=patient).count(), 1)

    @responses.activate
    def test_epic_oauth_existing_patient_returns_to_new_department(self):
        department2 = self.create_department(
            clinic=self.clinic, name="Epic Department Location 2"
        )

        patient = self.create_patient()
        PatientDepartmentSharing.objects.create(patient=patient, department=department2)
        PatientEhrIdentifier.objects.create(
            patient=patient,
            fhir_id=self.auth_response["patient_fhir_id"],
            epic_settings=self.epic_settings,
        )
        Encounter.objects.create(
            patient=patient,
            fhir_id="old_encounter_id",
            department=self.department
        )

        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Encounter.objects.filter(patient=patient).count(), 2)
        self.assertEqual(PatientEhrIdentifier.objects.filter(patient=patient).count(), 1)
        self.assertEqual(PatientDepartmentSharing.objects.filter(patient=patient).count(), 2)

    @responses.activate
    def test_epic_oauth_token_server_unavailable(self):
        responses.replace(responses.POST, token_url, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        response = self.client.post(self.uri, {
            "redirect_uri": "https://localhost",
            "code": 12345,
            "state": self.encoded_jwt
        })

        self.assertEqual(response.data["nonFieldErrors"], "Request to EPIC Failed")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)