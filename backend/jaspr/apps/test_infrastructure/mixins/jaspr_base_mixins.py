import uuid
from typing import Generator

from django.conf import settings
from django.db.models import CharField, DateField
from model_bakery.generators import default_mapping as default_baker_mapping
from model_bakery.recipe import seq

from jaspr.apps.clinics.models import HealthcareSystem, Clinic, Department, DepartmentTechnician
from jaspr.apps.kiosk.models import Patient, Technician
from jaspr.apps.test_infrastructure.enhanced_baker import baker
from jaspr.apps.test_infrastructure.mixins.base_mixins import (
    BaseGroupMixin,
    BaseTestCaseMixin,
)

from jaspr.apps.kiosk.models.patient_department_sharing import PatientDepartmentSharing


class JasprBaseTestCaseMixin(BaseGroupMixin, BaseTestCaseMixin):
    """
    Collection of helper methods for tests involving kiosk.
    Useful for both API and non-API tests. Only methods that
    involve creating user types are defined here
    (I.E. `Technician`s, `Patient`s, etc.). More specific methods
    should be defined in a subclass or subclasses.
    """

    ssid_seq: Generator[str, None, None] = seq("Test-SSID")

    @classmethod
    def next_ssid(cls) -> str:
        return next(cls.ssid_seq)

    @classmethod
    def create_technician(cls, **kwargs) -> Technician:
        """
        Helper function to create a `Technician`.
        Can optionally pass in `clinic` or `department`
        as kwargs, and the correct/relevant model instances will
        be created in that case.
        """
        user_kwargs, technician_kwargs = cls.extract_nested_kwargs("user", kwargs)

        system = technician_kwargs.pop("system", None)
        if system is None:
            system = cls.create_healthcare_system()

        department = technician_kwargs.pop("department", None)
        if department is None:
            department = cls.create_department(system=system)

        if "user" not in technician_kwargs and "user_id" not in technician_kwargs:
            technician_kwargs["user"] = cls.create_underlying_user(
                settings.TECHNICIAN_GROUP_NAME, **user_kwargs
            )

        technician = baker.make(Technician, system=system, **technician_kwargs)

        cls.create_department_technician(
            technician=technician,
            department=department
        )

        return technician

    @classmethod
    def create_patient(cls, **kwargs) -> Patient:
        """Helper function to create a `Patient`."""
        user_kwargs, patient_kwargs = cls.extract_nested_kwargs("user", kwargs)

        department = None
        if "department" in patient_kwargs:
            department = patient_kwargs.pop("department")

        if "mrn" in patient_kwargs:
            char_generator = default_baker_mapping[CharField]
            date_generator = default_baker_mapping[DateField]
            # NOTE: `char_generator` currently generates characters _of that length_,
            # so we'll keep them small to ease readability of we ever have to see
            # values printed out, etc.
            patient_kwargs.setdefault("first_name", char_generator(max_length=8))
            patient_kwargs.setdefault("last_name", char_generator(max_length=8))
            patient_kwargs.setdefault("date_of_birth", date_generator())
        elif "ssid" not in patient_kwargs:
            patient_kwargs["ssid"] = cls.next_ssid()

        if "user" not in patient_kwargs and "user_id" not in patient_kwargs:
            # Match the logic in `ActivateNewPatientSerializer` for consistency.
            if "ssid" in patient_kwargs:
                user_kwargs.setdefault(
                    "email", f'ssid-{patient_kwargs["ssid"]}.jaspr@jasprhealth.com'
                )
            patient_kwargs["user"] = cls.create_underlying_user(
                settings.PATIENT_GROUP_NAME, **user_kwargs
            )

        patient = baker.make(Patient, **patient_kwargs)

        if department is not None:
            baker.make(PatientDepartmentSharing, patient=patient, department=department)

        return patient

    @classmethod
    def create_patient_department_sharing(cls, **kwargs):
        return baker.make(PatientDepartmentSharing, **kwargs)

    @classmethod
    def create_tools_to_go_patient(cls, **kwargs) -> Patient:
        """
        Helper function to create a `Patient` with `tools_to_go_status`
        set to `Patient.TOOLS_TO_GO_SETUP_FINISHED`.
        """
        kwargs.setdefault("user__mobile_phone", "+15005550006")
        kwargs.setdefault("tools_to_go_status", Patient.TOOLS_TO_GO_SETUP_FINISHED)
        return cls.create_patient(**kwargs)

    @classmethod
    def create_department_technician(cls, **kwargs) -> DepartmentTechnician:
        if "technician" not in kwargs:
            kwargs["technician"] = cls.create_technician()

        if "department" not in kwargs:
            kwargs["department"] = cls.create_department()

        return baker.make(DepartmentTechnician, **kwargs)
