import logging

from django.http import HttpRequest
from django.test import RequestFactory

from jaspr.apps.api.v1.permissions import (
    SatisfiesClinicIPWhitelistingFromPatient,
    SatisfiesClinicIPWhitelistingFromTechnician,
)
from jaspr.apps.api.v1.permissions import logger as v1_permissions_logger
from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class TestSatisfiesClinicLocationIPWhitelisting(JasprTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Setup two different systems
        cls.system1 = cls.create_healthcare_system(name="System 1")
        cls.system2 = cls.create_healthcare_system(name="System 2")

        # No IP WhiteList
        cls.clinic_no_ip_whitelist = cls.create_clinic(
            name="clinic_no_ip_whitelist",
            system=cls.system1
        )
        cls.department_no_ip_whitelist = cls.create_department(
            name="department_no_ip_whitelist",
            clinic=cls.clinic_no_ip_whitelist
        )

        # System1: Clinics with Whitelist
        cls.clinic_with_whitelist_system1 = cls.create_clinic(
            name="Clinic 2",
            system=cls.system1,
            ip_addresses_whitelist=[
                "192.192.192.195",
                "192.191.192.195",
                "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            ],
            ip_address_ranges_whitelist=[
                "192.168.100.0/22",
                "2002:db8::/34",
            ],
        )
        cls.department_with_whitelist_system1 = cls.create_department(
            name="department_with_whitelist_system1",
            clinic=cls.clinic_with_whitelist_system1
        )

        cls.another_clinic_with_whitelist_system1 = cls.create_clinic(
            name="another_clinic_with_whitelist_system1",
            system=cls.system1,
            ip_addresses_whitelist=[
                "192.192.192.195",
                "192.193.192.195",
                "2001:0db8:85a3:0000:0000:8a2e:0370:7335",
            ],
            ip_address_ranges_whitelist=[
                "192.178.100.0/22",
                "2003:db7::/34",
            ],
        )
        cls.another_department_with_whitelist_system1 = cls.create_department(
            name="another_department_with_whitelist_system1",
            clinic=cls.another_clinic_with_whitelist_system1
        )

        # System 2: Clinic with Whitelist
        cls.clinic_with_whitelist_system2 = cls.create_clinic(
            name="clinic_with_whitelist_system2",
            system=cls.system2,
            # NOTE: Same as `cls.department13` so that we can make sure we're
            # filtering down to the correct clinics by, if `cls.department13` is
            # not included and an IP from it is specified, then we know we're not
            # getting other clinics/clinic locations included too.
            ip_addresses_whitelist=[
                "192.192.192.195",
                "192.193.192.195",
                "2001:0db8:85a3:0000:0000:8a2e:0370:7335",
            ],
            ip_address_ranges_whitelist=[
                "192.178.100.0/22",
                "2003:db7::/34",
            ],
        )
        cls.department_with_whitelist_system2 = cls.create_department(
            name="department_with_whitelist_system2",
            clinic=cls.clinic_with_whitelist_system2
        )

        cls.technician = cls.create_technician(
            system=cls.system1,
            department=cls.department_no_ip_whitelist
        )
        cls.patient = cls.create_patient(department=cls.department_no_ip_whitelist)

        cls.factory = RequestFactory()
        cls.request = cls.factory.get("/sample-testing-endpoint/")

    def check_technician_permissions(self, request: HttpRequest = None) -> bool:
        request = request or self.request
        request.user = self.technician.user
        self.permission = SatisfiesClinicIPWhitelistingFromTechnician()
        # NOTE: At the time of writing we're not using and/or needing the `View`, so
        # everything should still work here.
        return self.permission.has_permission(request, None)

    def check_patient_permissions(self, request: HttpRequest = None) -> bool:
        request = request or self.request
        request.user = self.patient.user
        self.permission = SatisfiesClinicIPWhitelistingFromPatient()
        # NOTE: At the time of writing we're not using and/or needing the `View`, so
        # everything should still work here.
        return self.permission.has_permission(request, None)

    def test_technician_no_departments(self):
        self.technician.departmenttechnician_set.all().delete()
        with self.assertLogs(v1_permissions_logger, logging.WARNING) as l:
            result = self.check_technician_permissions()
        self.assertFalse(result)
        self.assertIn(
            (
                f"(permission={self.permission}, request={self.request}, view={None}) "
                "No departments returned."
            ),
            l.output[0],
        )

    def test_technician_no_locations_with_whitelisting(self):
        # NOTE: By default, newly created `Clinic`s don't specify IP whitelisting, so
        # we don't need to do anything.
        result = self.check_technician_permissions()
        self.assertTrue(result)

    def test_technician_cannot_get_client_ip(self):
        self.create_department_technician(
            technician=self.technician,
            department=self.department_with_whitelist_system1
        )
        request = self.factory.get(
            "/sample-technician-testing-endpoint/", REMOTE_ADDR=""
        )
        with self.assertLogs(v1_permissions_logger, logging.WARNING) as l:
            result = self.check_technician_permissions(request)
        self.assertFalse(result)
        self.assertIn(
            (
                f"(permission={self.permission}, request={request}, view={None}) "
                "Couldn't get client's IP Address."
            ),
            l.output[0],
        )

    def test_patient_cannot_get_client_ip(self):
        request = self.factory.get("/sample-patient-testing-endpoint/", REMOTE_ADDR="")
        self.patient = self.create_patient(department=self.department_with_whitelist_system1)
        self.encounter = self.create_patient_encounter(
            patient=self.patient,
            department=self.department_with_whitelist_system1
        )
        with self.assertLogs(v1_permissions_logger, logging.WARNING) as l:
            result = self.check_patient_permissions(request)
        self.assertFalse(result)
        self.assertIn(
            (
                f"(permission={self.permission}, request={request}, view={None}) "
                "Couldn't get client's IP Address."
            ),
            l.output[0],
        )

    def test_technician_ip_satisfied(self):
        self.create_department_technician(
            technician=self.technician,
            department=self.department_with_whitelist_system1
        )
        request = self.factory.get(
            "/sample-technician-testing-endpoint/", REMOTE_ADDR="192.192.192.195"
        )
        result = self.check_technician_permissions(request)
        self.assertTrue(result)

    def test_technician_ip_satisfied_with_multiple_departments(self):
        self.create_department_technician(
            technician=self.technician,
            department=self.department_with_whitelist_system1
        )
        self.create_department_technician(
            technician=self.technician,
            department=self.another_department_with_whitelist_system1
        )
        request = self.factory.get(
            "/sample-technician-testing-endpoint/",
            REMOTE_ADDR="2003:0db7:0000:0000:0000:0000:1234:4321",
        )
        result = self.check_technician_permissions(request)
        self.assertTrue(result)

    def test_patient_ip_satisfied(self):
        self.patient = self.create_patient(department=self.department_with_whitelist_system1)
        self.encounter = self.create_patient_encounter(
            patient=self.patient,
            department=self.department_with_whitelist_system1
        )
        request = self.factory.get(
            "/sample-patient-testing-endpoint/",
            REMOTE_ADDR="2002:0db8:0000:0000:0000:0000:1234:4321",
        )
        result = self.check_patient_permissions(request)
        self.assertTrue(result)

    def test_technician_ip_not_satisfied(self):
        self.create_department_technician(
            technician=self.technician, department=self.department_with_whitelist_system1
        )
        request = self.factory.get(
            "/sample-technician-testing-endpoint/",
            REMOTE_ADDR="192.178.100.118",
        )
        result = self.check_technician_permissions(request)
        self.assertFalse(result)

    def test_patient_ip_not_satisfied(self):
        self.patient = self.create_patient(department=self.department_with_whitelist_system1)
        self.encounter = self.create_patient_encounter(
            patient=self.patient,
            department=self.department_with_whitelist_system1
        )
        request = self.factory.get(
            "/sample-patient-testing-endpoint/",
            REMOTE_ADDR="2001:0db8:85a3:0000:0000:8a2e:0370:7335",
        )
        result = self.check_patient_permissions(request)
        self.assertFalse(result)
