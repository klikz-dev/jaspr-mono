import logging
from datetime import timedelta
from django.utils import timezone
from freezegun import freeze_time
import responses
from rest_framework import status
from jaspr.apps.test_infrastructure.mixins.jaspr_mixins import (
    JasprApiTokenMixin,
)
from jaspr.apps.kiosk.jobs import logger as jobs_logger
from jaspr.apps.test_infrastructure.testcases import JasprTestCase
from jaspr.apps.clinics.models import GlobalPreferences
from jaspr.apps.kiosk.activities.activity_utils import ActivityType
from jaspr.apps.kiosk.narrative_note import NarrativeNote
from jaspr.apps.epic.models import EpicSettings, EpicDepartmentSettings, NotesLog, PatientEhrIdentifier
from jaspr.apps.kiosk.jobs import check_for_unsent_notes


class NoteSyncingTestCase(JasprApiTokenMixin, JasprTestCase):
    fixtures = [
        "jaspr/apps/bootstrap/fixtures/jaspr_content.json",
    ]

    def setUp(self):
        super().setUp()
        GlobalPreferences.objects.update_or_create(timezone="America/New_York", consent_language="")
        self.system, self.clinic, self.department = self.create_full_healthcare_system()
        self.patient = self.create_patient(department=self.department)
        self.encounter = self.create_patient_encounter(patient=self.patient, department=self.department, fhir_id="efhirid")
        self.epic_settings = EpicSettings.objects.create(
            name="Test Provider",
            provider="Epic",
            iss_url="https://fakeprovider.com"
        )
        self.epic_department_settings = EpicDepartmentSettings.objects.create(
            epic_settings=self.epic_settings,
            department=self.department,
            location_code="abc",
            narrative_note_key="def",
            stability_plan_note_key="ghi",
            narrative_note_system_key="jkl",
            stability_plan_system_key="mno",
        )
        self.patient_ehr_identifier = PatientEhrIdentifier.objects.create(
            epic_settings=self.epic_settings,
            patient=self.patient,
            fhir_id="phirid"
        )

    @responses.activate
    def test_duplicate_notes_are_not_created(self):
        """When creating a new note, if the content matches the most recent note for that encounter of that type
        don't create the new note"""
        responses.add(responses.GET, 'https://fakeprovider.com/metadata',
                      json=self.epic_iss_metadata, status=status.HTTP_200_OK)
        responses.add(responses.POST, self.epic_token_url,
                      json={"access_token": "JWT..."}, status=status.HTTP_200_OK)
        responses.add(responses.POST, "https://fakeprovider.com/DocumentReference",
                      json={}, headers={"location": "sample/docfhir"}, status=status.HTTP_201_CREATED)
        self.encounter.add_activities([ActivityType.SuicideAssessment, ActivityType.StabilityPlan])
        self.encounter.save_answers({"ratePsych": 4, "copingHelpOthers": ["Volunteer"]})
        note = NarrativeNote(self.encounter)
        note.save_narrative_note()
        with self.assertRaises(Exception) as context:
            note.save_narrative_note()
        self.assertTrue(NotesLog.error_messages["duplicate"] in context.exception.messages)
        self.assertEqual(NotesLog.objects.filter(encounter=self.encounter).count(), 1)

    @responses.activate
    def test_idle_notes_auto_send_to_ehr(self):
        """Notes get auto sent if they are between 10 and 60 minutes of patient inactivity.  We do
        not send notes after 60 minutes as a fail safe to prevent potential code failures from sending
        duplicate notes to the EHR indefinitely"""
        responses.add(responses.GET, 'https://fakeprovider.com/metadata',
                      json=self.epic_iss_metadata, status=status.HTTP_200_OK)
        responses.add(responses.POST, self.epic_token_url,
                      json={"access_token": "JWT..."}, status=status.HTTP_200_OK)
        responses.add(responses.POST, "https://fakeprovider.com/DocumentReference",
                      json={}, headers={"location": "sample/docfhir"}, status=status.HTTP_201_CREATED)

        now = timezone.now()
        earlier = now - timedelta(minutes=20)
        with freeze_time(earlier):
            self.encounter.add_activities([ActivityType.SuicideAssessment, ActivityType.StabilityPlan])
            stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
            self.encounter.save_answers({"ratePsych": 4, "copingHelpOthers": ["Volunteer"]})
            stability_plan.assignedactivity.start_time = earlier
            stability_plan.assignedactivity.save()
            NotesLog.objects.create(
                encounter=self.encounter,
                note="test",
                note_type="stability_plan",
            )

        check_for_unsent_notes()
        self.assertEqual(responses.calls[-1].request.url, "https://fakeprovider.com/DocumentReference")

    @responses.activate
    def test_expired_notes_do_not_send(self):
        """Notes get auto sent if they are between 10 and 60 minutes of patient inactivity.  We do
        not send notes after 60 minutes as a fail safe to prevent potential code failures from sending
        duplicate notes to the EHR indefinitely"""
        now = timezone.now()
        earlier = now - timedelta(hours=2)
        with freeze_time(earlier):
            self.encounter.add_activities([ActivityType.SuicideAssessment, ActivityType.StabilityPlan])
            stability_plan = self.encounter.get_activity(ActivityType.StabilityPlan)
            self.encounter.save_answers({"ratePsych": 4, "copingHelpOthers": ["Volunteer"]})
            stability_plan.note_generated = earlier
            stability_plan.save()
            stability_plan.assignedactivity.start_time = earlier
            stability_plan.assignedactivity.save()
            NotesLog.objects.create(
                encounter=self.encounter,
                note="test",
                note_type="stability_plan",
            )

        check_for_unsent_notes()
        self.assertEqual(len(responses.calls), 0)

    def test_no_more_than_1000_notes_sent(self):
        """If we have sent 1000+ notes to the EHR for a specific note type for a single encounter, do
        not send additional notes.  Likely something has gone wrong and we don't want to spam Epic"""
        NotesLog.objects.bulk_create([
            NotesLog(status="sent", encounter=self.encounter, note="", note_type="narrative_note") for _ in range(1001)
        ])
        self.assertEqual(NotesLog.objects.count(), 1001)

        now = timezone.now()
        earlier = now - timedelta(minutes=20)
        with freeze_time(earlier):
            self.encounter.add_activities([ActivityType.SuicideAssessment])
            suicide_assessment = self.encounter.get_activity(ActivityType.SuicideAssessment)
            self.encounter.save_answers({"ratePsych": 4})
            suicide_assessment.assignedactivity.start_time = earlier
            suicide_assessment.assignedactivity.save()

        with self.assertLogs(jobs_logger, logging.WARNING) as l:
            check_for_unsent_notes()

        self.assertEqual(len(responses.calls), 0)
        self.assertEqual(NotesLog.objects.count(), 1001)

        self.assertIn(
            (
                f"More than 1,000 narrative notes have been sent to the EHR for encounter {self.encounter.pk}"
            ),
            l.output[0],
        )


    def test_note_does_not_get_sent_if_already_sent(self):
        """A note should not get sent to the EHR again if it has already been sent"""
        note = NotesLog.objects.create(
            status="sent",
            encounter=self.encounter,
            note="test",
            note_type="stability_plan",
        )
        note.send_to_ehr()
        self.assertEqual(len(responses.calls), 0)

    @responses.activate
    def test_sending_a_note_to_the_ehr_successfully_updates_status_to_sent(self):
        """After successfully sending a note to the EHR, the notes status should be marked as sent"""
        responses.add(responses.GET, 'https://fakeprovider.com/metadata',
                      json=self.epic_iss_metadata, status=status.HTTP_200_OK)
        responses.add(responses.POST, self.epic_token_url,
                      json={"access_token": "JWT..."}, status=status.HTTP_200_OK)
        responses.add(responses.POST, "https://fakeprovider.com/DocumentReference",
                      json={}, headers={"location": "sample/docfhir"}, status=status.HTTP_201_CREATED)
        self.encounter.add_activities([ActivityType.SuicideAssessment, ActivityType.StabilityPlan])
        self.encounter.save_answers({"ratePsych": 4, "copingHelpOthers": ["Volunteer"]})
        note = NarrativeNote(self.encounter)
        note_log = note.save_narrative_note()
        self.assertEqual(note_log.status, "sent")

    @responses.activate
    def test_sending_a_note_to_the_ehr_that_fails_should_update_status_to_fail(self):
        """If a note fails to send to the EHR, e.g. API is down, set the status to failure and log the
        response from the api"""
        responses.add(responses.GET, 'https://fakeprovider.com/metadata',
                      json=self.epic_iss_metadata, status=status.HTTP_200_OK)
        responses.add(responses.POST, self.epic_token_url,
                      json={"access_token": "JWT..."}, status=status.HTTP_200_OK)
        responses.add(responses.POST, "https://fakeprovider.com/DocumentReference",
                      json={}, status=status.HTTP_400_BAD_REQUEST)

        note_log = NotesLog.objects.create(
            encounter=self.encounter,
            note="test",
            note_type="stability_plan",
        )
        with self.assertRaises(Exception):
            note_log.send_to_ehr()
        self.assertEqual(note_log.status, 'failed')
