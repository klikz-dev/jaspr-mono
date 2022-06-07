import responses
from rest_framework import status

from jaspr.apps.clinics.models import GlobalPreferences
from jaspr.apps.kiosk.models import NoteTemplate
from jaspr.apps.epic.models import NotesLog, EpicSettings, EpicDepartmentSettings, PatientEhrIdentifier
from jaspr.apps.kiosk.narrative_note import NarrativeNote

from jaspr.apps.test_infrastructure.testcases import JasprApiTestCase
from jaspr.apps.kiosk.activities.activity_utils import ActivityType


class TestTechnicianNotesLogAPI(JasprApiTestCase):
    fixtures = [
        "jaspr/apps/bootstrap/fixtures/jaspr_content.json",
    ]

    def setUp(self):
        super().setUp()

        self.department = self.create_department(
            name="Epic Dept 1"
        )

        self.integrated_department = self.create_department(name="Epic Integrated Dept 1")
        self.epic_settings = EpicSettings.objects.create(name="Epic System", provider="Epic",
                                                         iss_url="https://fakeprovider.com")
        EpicDepartmentSettings.objects.create(
            epic_settings=self.epic_settings,
            department=self.integrated_department,
            location_code="valid_location",
        )

        self.department = self.create_department(name="Department 1")
        self.patient = self.create_patient()
        self.uri = "/v1/technician/notes-log"
        stability_plan_template = NoteTemplate.objects.get(name="Default Stability Plan")
        narrative_note_template = NoteTemplate.objects.get(name="Default Narrative Note")
        GlobalPreferences.objects.update_or_create(
            pk="global_preferences",
            defaults={
                "stability_plan_template": stability_plan_template,
                "narrative_note_template": narrative_note_template,
                "timezone": "America/New_York",
                "provider_notes": False,
                "consent_language": ""
            }
        )

    def test_non_integrated_success(self):
        """ Does a properly formed request work? """

        self.create_patient_department_sharing(patient=self.patient, department=self.department)
        encounter = self.create_patient_encounter(patient=self.patient, department=self.department)

        technician = self.create_technician(system=self.department.clinic.system)
        self.create_department_technician(technician=technician, department=self.department)

        self.set_technician_creds(technician)
        encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        response = self.client.post(self.uri, data={
            "encounter": encounter.pk,
            "narrativeNote": True,
            "stabilityPlanNote": True,
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note_count = NotesLog.objects.filter(
            encounter=encounter,
            trigger="/technician/notes-log",
            sent_to_ehr=False,
        ).count()
        self.assertEqual(note_count, 2, "Patient has two manually triggered notes")

    @responses.activate
    def test_integrated_success(self):
        """ Does a properly formed request work? """
        responses.add(responses.GET, 'https://fakeprovider.com/metadata',
                      json=self.epic_iss_metadata, status=status.HTTP_200_OK)
        responses.add(responses.POST, self.epic_token_url,
                      json={"access_token": "JWT..."}, status=status.HTTP_200_OK)
        responses.add(responses.POST, "https://fakeprovider.com/DocumentReference",
                      json={}, headers={"location":"sample/docfhir"}, status=status.HTTP_201_CREATED)

        self.create_patient_department_sharing(patient=self.patient, department=self.integrated_department)
        encounter = self.create_patient_encounter(patient=self.patient, department=self.integrated_department)

        encounter.add_activities([ActivityType.StabilityPlan, ActivityType.SuicideAssessment])
        PatientEhrIdentifier.objects.create(
            patient=self.patient,
            fhir_id="fhir123",
            epic_settings=self.epic_settings,
        )
        encounter.fhir_id="fhirenc123"
        encounter.save()

        technician = self.create_technician(system=self.integrated_department.clinic.system)
        self.create_department_technician(technician=technician, department=self.integrated_department)

        self.set_technician_creds(technician)
        response = self.client.post(self.uri, data={
            "encounter": encounter.pk,
            "narrativeNote": True,
            "stabilityPlanNote": True,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        note_count = NotesLog.objects.filter(
            encounter=encounter,
            trigger="/technician/notes-log",
            sent_to_ehr = True,
            fhir_id="docfhir",
            sent_by=technician,
        ).count()
        self.assertEqual(note_count, 2, "Patient has two manually triggered notes saved to the EHR")


    def test_non_existent_encounter(self):
        """ If a patient session id is invalid, do we throw an error? """

        self.create_patient_department_sharing(patient=self.patient, department=self.department)
        encounter = self.create_patient_encounter(patient=self.patient, department=self.department)

        technician = self.create_technician(system=self.department.clinic.system)
        self.create_department_technician(technician=technician, department=self.department)

        self.set_technician_creds(technician)
        response = self.client.post(self.uri, data={
            "encounter": "12345",
            "narrativeNote": True
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_technician_does_not_have_access_to_patient(self):
        """ If a technician does not have access to the patient, do we throw an error? """
        self.create_patient_department_sharing(patient=self.patient, department=self.department)
        encounter = self.create_patient_encounter(patient=self.patient, department=self.department)

        technician = self.create_technician(system=self.department.clinic.system)

        self.set_technician_creds(technician)
        response = self.client.post(self.uri, data={
            "encounter": encounter.pk,
            "narrativeNote": True,
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_technician_can_retrieve_notes(self):
        technician = self.create_technician(department=self.department)
        self.set_technician_creds(technician)
        patient = self.create_patient(department=self.department)
        encounter = self.create_patient_encounter(patient=patient, department=self.department)
        ## Save note for current encounter
        NarrativeNote(encounter).save_narrative_note(sender=technician, trigger="")
        response = self.client.get(f"{self.uri}?patient={patient.pk}")
        self.assertEqual(len(response.data), 0, "Notes Log only returns notes for previous encounters")

        self.create_patient_encounter(patient=patient, department=self.department)

        response = self.client.get(f"{self.uri}?patient={patient.pk}")
        self.assertEqual(len(response.data), 1, "Notes Log only returns notes for previous encounters")

        self.assertEqual(response.status_code, status.HTTP_200_OK)