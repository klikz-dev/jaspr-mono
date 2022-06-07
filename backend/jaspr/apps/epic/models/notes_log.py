import logging
import base64
import requests
import json
from django.apps import apps
from jaspr.apps.common.models import JasprAbstractBaseModel
from jaspr.apps.common.jobs.messaging import email_engineering
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import ValidationError
from django.db import models
from model_utils import Choices
from fernet_fields import EncryptedTextField


logger = logging.getLogger(__name__)


class NotesLog(JasprAbstractBaseModel):
    STATUS = Choices(
        ("not-sent", "Not Sent"),
        ("in-progress", "In Progress"),
        ("failed", "Failed"),
        ("sent", "Sent")
    )
    NOTE_TYPES = Choices(
        ("narrative_note", "Narrative Note"),
        ("stability_plan", "Stability Plan"),
    )

    error_messages = {
        "duplicate": "Duplicate note already exists"
    }

    encounter = models.ForeignKey('kiosk.Encounter', on_delete=models.CASCADE)

    trigger = models.CharField(
        "Trigger",
        max_length=120,
        blank=True,
        null=True,
        help_text="What triggered the note to be sent to an EMR?",
    )

    note = EncryptedTextField(
        "Note",
        blank=True,
        help_text="Text of the note sent to the EMR"
    )

    note_type = models.CharField(
        "Note Type",
        choices=NOTE_TYPES,
        max_length=15,
    )

    fhir_id = models.CharField(
        max_length=256,
        verbose_name="FHIR ID",
        null=True,
        blank=True,
        help_text="ID of the note saved in the EMR"
    )

    sent_to_ehr = models.BooleanField(
        "Sent to EHR",
        default=False,
        help_text="Indicates if the note was sent to an EMR or only copied locally"
    )

    sent_by = models.ForeignKey("kiosk.Technician", on_delete=models.CASCADE, null=True, blank=True)

    response = models.TextField(
        blank=True,
        null=True,
        help_text="Response from EHR Server after saving"
    )

    def clean(self) -> None:
        last_note = NotesLog.objects.filter(
            encounter=self.encounter,
            note_type=self.note_type,
        ).exclude(pk=self.pk).order_by("-created").first()

        if last_note and last_note.note == self.note:
            logger.info("Not saving %s because it is identical to the last note for encounter %s."
                        "The EHR Fhir ID for the previous note is %s",
                        last_note.note_type, self.encounter.pk, last_note.fhir_id)
            raise ValidationError(self.error_messages["duplicate"])

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            self.full_clean()
        super().save(*args, **kwargs)

    def send_to_ehr(self) -> None:
        PatientEhrIdentifier = apps.get_model("epic", "PatientEhrIdentifier")

        if self.status == 'sent':
            # This note has already been sent
            return
        elif self.status == 'failed':
            logger.info("Attempting to resend failed note %s", self.pk)

        epic_department_settings = (
            self.encounter.department.get_department_ehr()
        )
        if not bool(epic_department_settings):
            # Department is not connected to an EHR.
            return

        epic_settings = epic_department_settings.epic_settings
        encounter = self.encounter
        patient = encounter.patient

        if self.note_type == "stability_plan":
            note_key = epic_department_settings.stability_plan_note_key
            system_key = epic_department_settings.stability_plan_system_key
        elif self.note_type == "narrative_note":
            note_key = epic_department_settings.narrative_note_key
            system_key = epic_department_settings.narrative_note_system_key
        else:
            raise ImproperlyConfigured("Unexpected Note Type")

        try:
            access_token = epic_settings.get_access_token()
        except Exception as e:
            logger.exception("Unable to get EHR access token", exc_info=e)
            raise e

        patient_ehr_identifier = PatientEhrIdentifier.objects.get(
            patient=self.encounter.patient, epic_settings=epic_department_settings.epic_settings
        )

        if not patient_ehr_identifier.fhir_id:
            raise Exception(f"Patient {patient.pk} does not have a FHIR ID set")

        if not encounter.fhir_id:
            raise Exception(f"Encounter {encounter.pk} does not have a FHIR ID set")

        document_reference_url = f"{epic_settings.iss_url}/DocumentReference"

        payload = {
            "type": {
                "coding": [
                    {"system": system_key, "code": note_key}
                ]
            },
            "subject": {"reference": patient_ehr_identifier.fhir_id},
            "content": [
                {
                    "attachment": {
                        "contentType": "text/plain",
                        "data": base64.b64encode(
                            self.note.encode("utf-8")
                        ).decode(
                            "utf-8"
                        ),
                    }
                }
            ],
            "context": {
                "encounter": {"reference": encounter.fhir_id}
            },
        }

        self.status = "in-progress"
        self.save()

        save_note_response = requests.post(
            document_reference_url,
            json.dumps(payload),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

        if save_note_response.status_code == 201:
            self.fhir_id = save_note_response.headers.get("Location").split("/")[-1]
            self.sent_to_ehr = True
            self.response = save_note_response.text
            self.status = "sent"
            self.save()
        else:
            logger.exception("Saving note to EPIC failed with response code %s and body %s",
                             save_note_response.status_code,
                             save_note_response.text
                             )
            logger.info(json.dumps(payload))
            self.response = save_note_response.text
            self.status = "failed"
            self.save()

            email_engineering("Saving note to EHR failed",
                              f"Sending note to EHR failed for encounter {encounter}. Check the logs for more details")
            raise Exception("Unable to save note into EHR")
