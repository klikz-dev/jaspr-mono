import datetime
import logging
import uuid
from functools import cached_property
from typing import Any, Dict, Literal

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, Group
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from jaspr.apps.accounts.models import User
from jaspr.apps.clinics.models import Department
from jaspr.apps.kiosk.models import ActivateRecord, Encounter, Patient

from ....kiosk.models.patient_department_sharing import PatientDepartmentSharing
from ..exceptions import PatientAlreadyExistsError
from ..helpers import zulu_time_format

from .base import JasprBaseModelSerializer, JasprBaseSerializer
from .serializers import ToolsToGoVerificationSetupSerializer
from jaspr.apps.kiosk.activities.activity_utils import ActivityType

logger = logging.getLogger(__name__)


class DepartmentSerializer(JasprBaseModelSerializer):
    """ Intended for use by a Technician to return relevant Department """

    name = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ("id", "name")

    def get_name(self, dept: Department):
        if dept.clinic is not None:
            clinic_name = dept.clinic.name
            return f"{clinic_name} > {dept.name}"
        return dept.name


class TechnicianDepartmentBaseSerializerMixin():
    """
    This is the base serializer for handling department attached to technicians.
    """

    default_error_messages = {
        "improper_department": "Submitted department is not one of the available departments for this technician.",
        "no_department": "No departments submitted for this request. They are required."
    }

    @cached_property
    def available_department_ids(self):
        if "technician" in self.context:
            technician = self.context["technician"]
        else:
            technician = self.context["request"].user.technician
        query = technician.departmenttechnician_set.filter(
            status="active"
        ).values_list("department", flat=True)
        available_departments = list(query)
        return available_departments

    def validate_department(self, dept_id) -> None:
        if dept_id is None:
            return self.fail("no_department")

        if dept_id not in self.available_department_ids:
            return self.fail("improper_department")

        return dept_id

    def has_department(self, dept_id):
        if dept_id is None:
            return False

        if dept_id not in self.available_department_ids:
            return False

        return True


class TechnicianDepartmentSerializer(JasprBaseSerializer, TechnicianDepartmentBaseSerializerMixin):
    """
    This serializer handles validating a single department attached to a Technician and often their patient.
    """

    department = serializers.IntegerField(min_value=0)


class TechnicianDepartmentListSerializer(JasprBaseSerializer, TechnicianDepartmentBaseSerializerMixin):
    """
    This serializer handles validating a list of departments attached to Technician and often their patient.
    """

    departments = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
        allow_empty=False
    )

    def validate_departments(self, dept_ids):
        avail_depts = self.available_department_ids
        if avail_depts is None or len(avail_depts) == 0:
            self.fail("no_department")

        if dept_ids is None or len(dept_ids) == 0:
            self.fail("no_department")

        result = []
        for dept_id in dept_ids:
            value = self.validate_department(dept_id)
            result.append(value)

        return result


class ActivateNewPatientSerializer(TechnicianDepartmentSerializer):
    default_error_messages = {
        "patient_exists_ssid": "A patient with that SSID already exists.",
        "generic": (
            "We were unable to create the patient. Double check the information "
            "filled out and try again. If this problem persists, contact support."
        ),
        "improper_department": "Submitted department is not one of the available departments for this technician.",
        "no_department": "No departments submitted for this request. They are required."
    }

    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    mrn = serializers.CharField(required=False, allow_blank=True, max_length=255)
    activities = serializers.DictField(required=False)

    ssid = serializers.RegexField(
        r"^[-a-zA-Z0-9_]*\Z",
        required=False,
        allow_blank=True,
        allow_null=True,
        default=None,
        error_messages={
            "invalid": "SSIDs can only contain letters, numbers, hyphens, and underscores."
        },
        max_length=25,
    )

    @staticmethod
    def default_email_for(field: Literal["mrn", "ssid"], value: str) -> str:
        assert field in ("mrn", "ssid")
        prefix_end = ".jaspr"
        if field == "mrn":
            # Example: "123e4715-e89b-12d3-a436-426612174000.jaspr"
            prefix = f"{uuid.uuid4()}{prefix_end}"
        else:
            # Example: "ssid-333543.jaspr"
            prefix = f"ssid-{value}{prefix_end}"
        return f"{prefix}@jasprhealth.com"

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Make sure we have a `new` `Patient`."""
        data = super().validate(attrs)
        initial_data_to_check = {
            "first_name": data.get("first_name") or "",
            "last_name": data.get("last_name") or "",
            "date_of_birth": data.get("date_of_birth") or None,
            "mrn": data.get("mrn") or "",
            "ssid": data.get("ssid") or "",
        }
        Patient.validate_required_fields_together(**initial_data_to_check)

        if mrn := data.get("mrn"):
            assert not data.get("ssid")
            data["check_by"] = "mrn"
            default_email = self.default_email_for("mrn", mrn)

            ## Search in application space for any duplicate patients at the requested system since mrn is encrypted
            ## and can't be filtered in the db
            if not self.context.get("oauth", False):
                system_patient_ids = PatientDepartmentSharing.objects.filter(
                    department__clinic__system=self.context["request"].user.technician.system_id
                ).values_list("patient_id", flat=True)
                patients = Patient.objects.filter(id__in=system_patient_ids).values("id", "mrn")
                for patient in patients:
                    if patient["mrn"] != "" and patient["mrn"] == mrn:
                        patient = Patient.objects.get(pk=patient["id"])
                        raise PatientAlreadyExistsError(patient=patient)
        else:
            ssid = data["ssid"]
            assert ssid
            data["check_by"] = "ssid"
            filter_by = Q(ssid=ssid)
            default_email = self.default_email_for("ssid", ssid)

            if patient := Patient.objects.filter(filter_by).first():
                raise PatientAlreadyExistsError(patient=patient)

        # The last check we perform is to make sure that there isn't a `User` with the
        # email address that will be assigned.
        # Possible Cases:
        #   1) a user with a patient record, not in current clinic.
        #   2) a user without a patient record (a technician for example).
        #   3) a patient with an mrn that can't be checked because it is encrypted.
        if User.objects.filter(email=default_email).exists():
            self.fail("generic")

        data["department"] = data.get("department")

        return data

    def create(self, validated_data: Dict[str, Any]) -> Patient:
        with transaction.atomic():
            check_by = validated_data.pop("check_by")
            if check_by == "mrn":
                mrn = validated_data["mrn"]
                default_email = self.default_email_for("mrn", mrn)
            else:
                ssid = validated_data["ssid"]
                default_email = self.default_email_for("ssid", ssid)

            user_kwargs = {
                "email": default_email,
                "password": BaseUserManager().make_random_password(),
                "password_complex": True,
                "is_active": True,
            }
            user = User.objects.create(**user_kwargs)
            user.groups.add(Group.objects.get(name=settings.PATIENT_GROUP_NAME))
            department = validated_data.pop("department")
            activities = validated_data.pop("activities", {})
            csp = activities.pop("csp", False)
            csa = activities.pop("csa", False)
            skills = activities.pop("skills", False)
            create_encounter = self.context.get("create_encounter", False)
            patient = Patient.objects.create(**validated_data, user=user)
            if create_encounter:
                encounter = Encounter.objects.create(patient=patient, department_id=department)
                activities_to_add = []
                if skills:
                    activities_to_add.append(ActivityType.ComfortAndSkills)
                if csa:
                    activities_to_add.append(ActivityType.SuicideAssessment)
                if csp:
                    activities_to_add.append(ActivityType.StabilityPlan)
                if activities_to_add:
                    encounter.add_activities(activities_to_add)


            PatientDepartmentSharing.objects.create(
                department_id=department,
                patient=patient,
                status="active"
            )

            return patient


class ActivateExistingPatientSerializer(TechnicianDepartmentSerializer):
    default_error_messages = {
        "department_mismatch": "The patient's department is not one of the available departments for this technician.",
        "improper_department": "Submitted department is not one of the available departments for this technician.",
        "no_department": "No departments submitted for this request. They are required."
    }

    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all()
    )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data = super().validate(attrs)
        department_id = data["department"]
        all_pds = data["patient"].patientdepartmentsharing_set.all()
        found = False
        for pds in all_pds:
            if pds.department_id == department_id:
                found = True
                break
        if not found:
            self.fail("department_mismatch")
        return data

    def create(self, validated_data: Dict[str, Any]) -> Patient:
        # Just return the `Patient`. Not updating or saving anything right now.
        return validated_data["patient"]


class ReadOnlyTechnicianPatientSerializer(JasprBaseModelSerializer, TechnicianDepartmentBaseSerializerMixin):
    created = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    mobile_phone = serializers.SerializerMethodField()
    current_encounter = serializers.SerializerMethodField()
    current_encounter_created = serializers.SerializerMethodField()
    current_encounter_department = serializers.SerializerMethodField()
    suggest_new_encounter = serializers.SerializerMethodField()
    last_logged_in_at = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()
    departments = serializers.SerializerMethodField()

    def get_current_encounter(self, patient: Patient):
        try:
            return patient.current_encounter.pk
        except AttributeError:
            return None

    def get_current_encounter_created(self, patient: Patient):
        try:
            return patient.current_encounter.created
        except AttributeError:
            return None

    def get_current_encounter_department(self, patient: Patient):
        try:
            return patient.current_encounter.department.pk
        except AttributeError:
            return None

    def get_suggest_new_encounter(self, patient: Patient):
        now = timezone.now()
        try:
            timediff = now - patient.current_encounter.modified
            return timediff.days > 3
        except AttributeError:
            return None


    def get_last_logged_in_at(self, obj: Patient) -> datetime.datetime:
        # NOTE: Should currently be added to the `Patient` from a `QuerySet` annotation.
        try:
            return obj.last_logged_in_at
        except AttributeError:
            activate_record = ActivateRecord.objects.filter(
                patient_id=obj.pk,
                technician__system=self.context["request"].user.technician.system,
            ).order_by("-timestamp").values("timestamp").first()
            if activate_record:
                return activate_record.get("timestamp", None)
            return None

    def get_created(self, obj: Patient):
        return zulu_time_format(obj.created)

    def get_email(self, obj: Patient) -> str:
        return "" if obj.has_internal_email() else obj.user.email

    def get_mobile_phone(self, obj: Patient) -> str:
        mobile_phone = obj.user.mobile_phone
        return "" if not mobile_phone else mobile_phone.as_e164

    def get_departments(self, patient: Patient):
        all_pds = patient.departments
        result = []
        for pds in all_pds:
            if self.has_department(pds):
                result.append(pds)
        return result

    def get_activities(self, obj: Patient):
        encounter = obj.current_encounter
        if encounter:
            return {
                "csp": encounter.has_activity(ActivityType.StabilityPlan),
                "csa": encounter.has_activity(ActivityType.SuicideAssessment),
                "skills": encounter.has_activity(ActivityType.ComfortAndSkills)
            }
        return {
            "csp": False,
            "csa": False,
            "skills": False,
        }


    class Meta:
        model = Patient
        fields = [
            "id",
            "current_encounter",
            "current_encounter_created",
            "current_encounter_department",
            "suggest_new_encounter",
            "first_name",
            "last_name",
            "date_of_birth",
            "mrn",
            "email",
            "mobile_phone",
            "ssid",
            "departments",
            "activities",
            "last_logged_in_at",
            "tools_to_go_status",
            "tour_complete",
            "created",
            "analytics_token",
        ]
        read_only_fields = fields


class PatientSerializer(TechnicianDepartmentListSerializer, JasprBaseModelSerializer):
    created = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    mobile_phone = serializers.SerializerMethodField()
    current_encounter = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    def get_current_encounter(self, patient: Patient):
        try:
            return patient.current_encounter.pk
        except AttributeError:
            return None

    def get_activities(self, obj: Patient):
        encounter = obj.current_encounter
        if encounter:
            return {
                "csp": encounter.has_activity(ActivityType.StabilityPlan),
                "csa": encounter.has_activity(ActivityType.SuicideAssessment),
                "skills": encounter.has_activity(ActivityType.ComfortAndSkills)
            }
        return {
            "csp": False,
            "csa": False,
            "skills": False,
        }

        return {
            "csa": "Not Assigned",
            "lethal_means": "Not Assigned",
            "crisis_stability_plan": "Not Assigned",
            "review": "Not Started",
        }

        return {
            "csa": None,
            "lethal_means": None,
            "crisis_stability_plan": None,
            "review": None,
            "ehr_note_sent": None,
        }

    def get_email(self, obj: Patient) -> str:
        return "" if obj.has_internal_email() else obj.user.email

    def get_mobile_phone(self, obj: Patient) -> str:
        mobile_phone = obj.user.mobile_phone
        return "" if not mobile_phone else mobile_phone.as_e164

    def get_created(self, obj: Patient):
        return zulu_time_format(obj.created)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Make sure correct combination of fields are supplied."""
        data = super().validate(attrs)
        initial_data_to_check = {
            "first_name": data.get("first_name") or "",
            "last_name": data.get("last_name") or "",
            "date_of_birth": data.get("date_of_birth") or None,
            "mrn": data.get("mrn") or "",
            "ssid": data.get("ssid") or "",
        }
        Patient.validate_required_fields_together(**initial_data_to_check)
        data["departments"] = data.get("departments")

        # TODO I'm not sure where attrs are getting set, but they don't include all data in the request
        request_data = self.context["request"].data

        if 'email' in request_data and \
                request_data['email'].endswith('jaspr@jasprhealth.com'):
            # TODO Can't set to email key because it doesn't exist in validated data
            raise serializers.ValidationError("Cannot set patient email to internal email")

        if ('email' in request_data or 'mobile_phone' in request_data) and \
                self.instance.tools_to_go_status == Patient.TOOLS_TO_GO_SETUP_FINISHED:
            raise serializers.ValidationError(
                "Cannot set patient JAH Credentials after patient has completed JAH Setup")

        return data

    def update(self, instance: Patient, validated_data: dict) -> Patient:
        # Have to set all fields to "" if they have not appeared,
        # so as to force removing data from non-mentioned fields.
        request_data = self.context["request"].data

        put_data = {
            "first_name": validated_data.get("first_name") or "",
            "last_name": validated_data.get("last_name") or "",
            "date_of_birth": validated_data.get("date_of_birth") or None,
            "mrn": validated_data.get("mrn") or "",
            "ssid": validated_data.get("ssid") or "",
        }

        for k, v in put_data.items():
            setattr(instance, k, v)
        instance.save()

        departments = validated_data.get("departments")
        all_pds = instance.patientdepartmentsharing_set.filter(status="active").all()

        # check for removed departments that the technician doesn't have the right to remove
        for pds in all_pds:
            if self.has_department(pds.department_id):
                found = False
                for dept in departments:
                    if dept == pds.department_id:
                        found = True
                        break
                if not found:
                    # if we got here, they have the permissions to delete
                    pds.status = "inactive"
                    pds.save()

        # check for newly added departments
        for dept in departments:
            if self.has_department(pds.department_id):
                found = False
                for pds in all_pds:
                    if dept == pds.department_id:
                        found = True
                        break
                if not found:
                    PatientDepartmentSharing.objects.create(
                        patient=instance,
                        department_id=dept,
                        status="active"
                    )

        jah_email_updated = 'email' in request_data and instance.email != request_data['email']
        jah_mobile_phone_updated = 'mobile_phone' in request_data and instance.mobile_phone != request_data[
            'mobile_phone']

        if jah_email_updated or jah_mobile_phone_updated:
            tools_to_go_serializer = ToolsToGoVerificationSetupSerializer(
                instance,
                data=self.context["request"].data,
                context=self.context
            )
            tools_to_go_serializer.is_valid(raise_exception=True)
            tools_to_go_serializer.save()

        return instance

    class Meta:
        model = Patient
        fields = [
            "id",
            "current_encounter",
            "first_name",
            "last_name",
            "date_of_birth",
            "mrn",
            "ssid",
            "email",
            "mobile_phone",
            "departments",
            "activities",
            "tools_to_go_status",
            "tour_complete",
            "created",
            "analytics_token",
        ]
        read_only_fields = [
            "created",
            "activities",
            "current_encounter",
            "departments",
            "tools_to_go_status",
            "tour_complete",
        ]
