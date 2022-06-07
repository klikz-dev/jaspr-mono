import logging

import requests
from django.db import IntegrityError
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.cache import cache
from requests.adapters import HTTPAdapter
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from urllib3.util.retry import Retry

from jaspr.apps.accounts.models import User
from jaspr.apps.epic.models import EpicDepartmentSettings, EpicSettings
from jaspr.apps.api.v1.serializers import (
    ActivateNewPatientSerializer,
    MeTechnicianSerializer,
    PatientSerializer,
    TechnicianEpicOauthLoginSerializer,
    EpicSmartLaunchSerializer,
)
from jaspr.apps.api.v1.views.login_base import LoginBaseView
from jaspr.apps.clinics.models import DepartmentTechnician
from jaspr.apps.epic.models import PatientEhrIdentifier
from jaspr.apps.kiosk.models import Encounter, Patient, Technician, PatientDepartmentSharing

logger = logging.getLogger("EPIC")

# Workaround to deal with weak DH keys used at Allina
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'


class TechnicianEpicOauthLoginView(LoginBaseView):
    """Expects a POST of code and state
    Returns token, Technician and patient context if set.
    Unsuccessful requests return validation errors as a 400 BAD REQUEST

    /v1/technician/epic-oauth-login
    """

    @staticmethod
    def generate_email(id, clinic_name):
        return f"{id}@{clinic_name.replace(' ', '_')}.jasprhealth.com"

    def create_user(self, fhir_id, department):
        clinic = department.clinic
        user = User.objects.create_user(email=self.generate_email(fhir_id, clinic.name))
        return user

    def create_technician(self, fhir_id, department, first_name="", last_name=""):
        try:
            user = self.create_user(fhir_id, department)
        except IntegrityError as e:
            logger.exception(f"Cannot create EPIC technician with fhir_id {fhir_id} since that user already exists")
            raise e

        user.groups.add(Group.objects.get(name=settings.TECHNICIAN_GROUP_NAME))
        technician = Technician.objects.create(
            user=user, system=department.clinic.system, fhir_id=fhir_id, first_name=first_name, last_name=last_name
        )
        DepartmentTechnician.objects.create(
            technician=technician, department=department
        )
        return technician

    @staticmethod
    def format_date(datestring: str) -> str:
        # Current date format defined in our EPIC implementation guide returns dates in the format YYYYMMDD
        year = datestring[0:4]
        month = datestring[4:6]
        day = datestring[6:8]
        return f"{year}-{month}-{day}"

    def create_patient(self,
                       mrn,
                       date_of_birth,
                       department,
                       epic_settings,
                       patient_fhir_id,
                       technician,
                       patient_first_name="",
                       patient_last_name="",
                       ):
        patient = ActivateNewPatientSerializer(
            data={
                "first_name": patient_first_name,
                "last_name": patient_last_name,
                "mrn": mrn,
                "date_of_birth": self.format_date(date_of_birth),
                "department": department.id,
                "fhir_id": patient_fhir_id
            },
            context={"technician": technician, "create_encounter": False, "oauth": True},
        )

        try:
            patient.is_valid(raise_exception=True)
        except Exception as e:
            logger.exception(f"Patient created during EPIC OAuth is invalid", exc_info=e)
            raise Exception("Patient created during EPIC OAuth is invalid")

        patient = patient.save()  # Save and return  PK
        patient.last_logged_in_at = None

        try:
            PatientEhrIdentifier.objects.create(
                patient=patient,
                epic_settings=epic_settings,
                fhir_id=patient_fhir_id,
            )
        except Exception as e:
            logger.exception("Failed to create PatientEHRIdentifier with value %s and patient %s",
                             patient_fhir_id,
                             patient.pk
            )
            raise e

        return patient

    def post(self, request: Request):
        logger.info("Epic OAuth resuming session with session key {%s}", request.session.session_key)
        login_epic_oauth_serializer = TechnicianEpicOauthLoginSerializer(
            data=request.data, context={"request": request, "view": self}
        )
        try:
            login_epic_oauth_serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.exception("Epic OAuth serializer validation failed", exc_info=e)
            raise e

        redirect_uri = login_epic_oauth_serializer.data["redirect_uri"]
        code = login_epic_oauth_serializer.data["code"]
        token_url = login_epic_oauth_serializer.data["token_url"]
        iss = login_epic_oauth_serializer.data["iss"]

        logger.info("Epic Oauth login received these values: {iss: %s, token_url: %s, code: %s, redirect_uri: %s",
                    iss,
                    token_url,
                    code,
                    redirect_uri
                    )

        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": settings.EPIC_CLIENT_ID,
        }

        logger.info("Epic OAuth making request to %s with payload {grant_type: %s, code: %s, redirect_uri: %s, client_id: %s}",
                    token_url, "authorization_code", code, redirect_uri, settings.EPIC_CLIENT_ID)

        request_session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.25)
        request_session.mount("https://", HTTPAdapter(max_retries=retries))

        try:
            response = request_session.post(token_url, data=payload)
        except requests.exceptions.RequestException as e:
            logger.warning(f"Unable to connect to the EPIC token_url", e)
            raise e

        if response.status_code != 200:
            return Response(
                {"nonFieldErrors": "Request to EPIC Failed"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = response.json()
        epic_smart_launch_serializer = EpicSmartLaunchSerializer(data=data)
        try:
            epic_smart_launch_serializer.is_valid(raise_exception=True)
            logger.info("Epic OAuth received the following tokens: %s",
                        "".join([f'\n\t{key}:: {value}' for key, value in epic_smart_launch_serializer.data.items()]))
        except Exception as e:
            logger.exception("Epic OAuth tokens not valid", exc_info=e)
            raise e

        dept_id = epic_smart_launch_serializer.data.get("dept_id")
        try:
            epic_department_settings = EpicDepartmentSettings.objects.get(
                location_code=dept_id
            )
            epic_settings = epic_department_settings.epic_settings
        except (EpicDepartmentSettings.DoesNotExist, EpicSettings.DoesNotExist):
            logger.exception("Epic OAuth unable to find department with location code %s", dept_id)
            return Response(
                {"non_field_errors": "Unable to find department"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if epic_settings.iss_url != iss and iss:
            epic_settings.iss_url = iss
            epic_settings.save()

        department = epic_department_settings.department
        technician_fhir_id = epic_smart_launch_serializer.data.get("practitioner_fhir_id")
        technician_first_name = epic_smart_launch_serializer.data.get("practitioner_first_name", "")
        technician_last_name = epic_smart_launch_serializer.data.get("pratictioner_last_name", "")

        try:
            # Fhir ID's are not unique across EPIC instances, so we also need to filter on department
            technician = Technician.objects.get(
                fhir_id=technician_fhir_id, system=department.clinic.system
            )
        except Technician.DoesNotExist:
            try:
                technician = self.create_technician(
                    fhir_id=technician_fhir_id,
                    department=department,
                    first_name=technician_first_name,
                    last_name=technician_last_name
                )
            except IntegrityError:
                logger.exception("Epic OAuth unable to find technician with fhir_id %s in system ",
                                 technician_fhir_id,
                                 department.clinic.system.name
                                 )
                return Response(
                    {"non_field_errors": "Unable to create technician"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # The technician may have been created during a previous encounter for a different department.
        # If we see this technician again but with a different department, we want to grant access to the new
        # department
        try:
            DepartmentTechnician.objects.get(
                technician=technician, department=department
            )
        except DepartmentTechnician.DoesNotExist:
            logger.info(f"Epic Oauth creating new Technician Department Record for existing technician {technician.pk}")
            DepartmentTechnician.objects.create(
                technician=technician, department=department
            )

        try:
            patient_ehr_identifier = PatientEhrIdentifier.objects.get(
                fhir_id=data.get("patient_fhir_id"), epic_settings=epic_settings
            )
            patient = patient_ehr_identifier.patient
        except (PatientEhrIdentifier.DoesNotExist, Patient.DoesNotExist):
            try:
                patient = self.create_patient(
                    mrn=data.get("mrn"),
                    date_of_birth=data.get('dob'),
                    department=epic_department_settings.department,
                    epic_settings=epic_settings,
                    patient_fhir_id=data.get("patient_fhir_id"),
                    technician=technician,
                    patient_first_name=data.get("patient_first_name", ""),
                    patient_last_name=data.get("patient_last_name"),
                )
            except Exception as e:
                logger.exception("Epic OAuth unable to create patient", exc_info=e)
                return Response(
                    {"error": "Unable to create patient"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        encounter = Encounter.objects.filter(
            patient=patient, department=department, fhir_id=data.get("encounter")
        ).first()

        patient_department_sharing = PatientDepartmentSharing.objects.filter(
            patient=patient, department=department
        )

        if not patient_department_sharing:
            PatientDepartmentSharing.objects.create(
                patient=patient, department=department
            )
            logger.info(f"Epic OAuth creating new patient department sharing "
                        f"for patient {patient.pk} and dept {department.pk}")

        if not encounter:
            Encounter.objects.create(
                patient=patient, department=department, fhir_id=data.get("encounter")
            )
            logger.info("Epic OAuth creating new patient encounter with fhir id %s", data.get("encounter"))

        session, token = self.create_jaspr_session(
            user=technician.user, user_type="Technician", in_er=True
        )

        response = {
            "technician": MeTechnicianSerializer(instance=technician).data,
            "patient": PatientSerializer(instance=patient).data,
            "token": token,
        }

        logger.info("Epic OAuth completed successfully")

        return Response(response, status=status.HTTP_200_OK)
