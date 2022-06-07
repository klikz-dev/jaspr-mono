from django.db.models import QuerySet
from jaspr.apps.clinics.models import GlobalPreferences, HealthcareSystem, Clinic, Department, Preferences
from jaspr.apps.test_infrastructure.enhanced_baker import baker
from jaspr.apps.test_infrastructure.testcases import JasprTestCase


class ClinicTestCase(JasprTestCase):
    def create_healthcare_system(self, name):
        """
        Helper function; creates clinic for use in therapist-supervisor
        model.
        """

        clinic = baker.make(HealthcareSystem, name=name)
        return clinic


class TestClinics(ClinicTestCase):
    def setUp(self):
        super(TestClinics, self).setUp()
        self.system1 = self.create_healthcare_system(name="System One")
        self.system2 = self.create_healthcare_system(name="System Two")
        self.clinic1 = self.create_clinic(name="Clinic One", system=self.system1)
        self.clinic2 = self.create_clinic(name="Clinic Two", system=self.system2)
        self.department1 = self.create_department(clinic=self.clinic1)
        self.department2 = self.create_department(name="Dept 2", clinic=self.clinic1)
        self.department3 = self.create_department(clinic=self.clinic2)

    def test_get_clinics_json_return_list_of_dicts(self):
        """Does the Clinic.locations() method return a list of dictionaries?"""
        clinics = self.system1.get_clinics_json()
        self.assertEqual(type(clinics), list)
        self.assertEqual(len(clinics), 2)

    def test_get_clinics_return_query_set(self):
        """Does the Clinic.locations() method return a list of dictionaries?"""
        clinics = self.system1.get_clinics()
        self.assertEqual(type(clinics), QuerySet)
        self.assertEqual(len(list(clinics)), 2)

    def test_clinics_created(self):

        all_systems = HealthcareSystem.objects.all()
        self.assertTrue(len(all_systems), 2)

        all_systems_names = (all_systems[0].name, all_systems[1].name)
        self.assertIn("System One", all_systems_names)
        self.assertIn("System Two", all_systems_names)

    def test_clinic_creation_create_unassigned_location(self):
        """ Test creating a clinic creates an unassigned location for that
        clinic"""

        self.assertEqual(self.department1.name, "unassigned")
        self.assertEqual(self.department2.name, "Dept 2")
        self.assertEqual(self.department3.name, "unassigned")

    def test_clinic_update_does_not_create_new_department(self):
        """ Test updating a clinic does not affect unassigned clinic location"""

        self.clinic1.name = "Something else"
        self.clinic1.save()

        departments = Department.objects.filter(clinic=self.clinic1)
        department_names = []
        for cl in departments:
            department_names.append(cl.name)

        self.assertEqual(len(departments), 2)
        self.assertIn("unassigned", department_names)
        self.assertIn(self.department1.name, department_names)
        self.assertIn(self.department2.name, department_names)

    def test_subclinics(self):
        """ Do subclinics get made and associated with a clinic? """

        departments = Department.objects.all()
        self.assertEqual(len(departments), 3)

        clinic1_departments = Department.objects.filter(clinic=self.clinic1)
        self.assertEqual(len(clinic1_departments), 2)

        clinic2_departments = Department.objects.filter(clinic=self.clinic2)
        self.assertEqual(len(clinic2_departments), 1)


class TestPreferences(ClinicTestCase):
    def setUp(self):
        super(TestPreferences, self).setUp()
        self.global_preferences, _ = GlobalPreferences.objects.get_or_create(id="global_preferences", consent_language="")
        self.global_preferences.timezone = "Americas/New_York"
        self.global_preferences.save()
        self.system = self.create_healthcare_system(name="System One")
        self.clinic = self.create_clinic(name="Clinic One", system=self.system)
        self.clinic2 = self.create_clinic(name='Clinic Two', system=self.system)
        self.department = self.create_department(clinic=self.clinic)
        self.department2 = self.create_department(clinic=self.clinic2)

    def test_preferences(self):
        system_preferences = Preferences.objects.create(timezone="Africa/Addis_Ababa", consent_language="")
        clinic2_preferences = Preferences.objects.create(timezone="Americas/Los_Angeles", consent_language="")
        self.system.preferences = system_preferences
        self.clinic2.preference = clinic2_preferences
        self.system.save()
        self.clinic2.save()
        assert self.department.get_preferences().timezone == self.system.preferences.timezone
        assert self.clinic.get_preferences().timezone, self.system.preferences.timezone
        assert self.system.get_preferences().timezone, self.system.preferences.timezone
        assert self.department2.get_preferences().timezone, self.clinic2.preferences.timezone

    def test_global_preferences(self):
        assert self.department.get_preferences().timezone == self.global_preferences.timezone

