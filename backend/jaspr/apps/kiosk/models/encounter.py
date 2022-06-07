import logging
import re

from django.apps import apps
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from fernet_fields import EncryptedCharField, EncryptedDateTimeField
from model_utils import Choices
from simple_history.models import HistoricalRecords


from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel
from jaspr.apps.kiosk.activities.manager import ActivityManagerMixin
from jaspr.apps.kiosk.activities.activity_utils import ActivityStatus
from jaspr.apps.kiosk.narrative_note import NarrativeNote

logger = logging.getLogger(__name__)


class Encounter(JasprAbstractBaseModel, ActivityManagerMixin):

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    start_time = EncryptedDateTimeField(
        null=True,
        blank=True,
        help_text="Session start time",
    )

    end_time = EncryptedDateTimeField(
        null=True,
        blank=True,
        help_text="Session end time",
    )

    patient = models.ForeignKey(
        "kiosk.Patient", on_delete=models.CASCADE, verbose_name="Patient"
    )

    department = models.ForeignKey(
        "clinics.Department", on_delete=models.CASCADE, verbose_name="Department", null=True
    )

    fhir_id = models.CharField(max_length=256, verbose_name="FHIR IDs", null=True, blank=True)

    privacy_screen_image = models.ForeignKey(
        "awsmedia.PrivacyScreenImage",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name="Chosen Privacy Screen Image",
        help_text="This image has been chosen by this patient to be the image they use in their privacy screen.",
    )

    encrypted_question = EncryptedCharField(
        "Security Question", max_length=255, default=" "
    )

    encrypted_answer = EncryptedCharField(
        "Security Answer", max_length=255, default=" "
    )

    # account_locked_at = models.DateTimeField("Account Locked At", null=True, blank=True)

    session_validation_attempts = models.PositiveSmallIntegerField(
        "Session Validation Attempts",
        default=0,
        help_text="Number of times that session-validate has been called without success up to 6.  After 6 attempts, all further attempts are failed automatically without recording.",
    )
    last_heartbeat = models.DateTimeField(
        "Last Heartbeat",
        null=True,
        blank=True,
        help_text="Last time frontend pinged backend using heartbeat endpoint.",
    )
    session_lock = models.BooleanField(
        default=False,
        help_text="When True, patient must validate session to gain access to endpoints requiring recent heartbeat.",
        verbose_name="Session Lock",
    )
    current_section_uid = EncryptedCharField(
        "Current Section UID",
        blank=True,
        null=True,
        max_length=63,
    )
    technician_operated = models.BooleanField(
        default=False,
        help_text="Indicates that the provider assisted the patient directly in answering questions",
        verbose_name="Technician Operated"
    )

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Encounter"
        verbose_name_plural = "Encounters"

    def create_patient_measurement(self, **kwargs):
        PatientMeasurements = apps.get_model("kiosk", "PatientMeasurements")
        PatientMeasurements.objects.create(encounter=self, **kwargs)

    @cached_property
    def section_uid_ordered_list(self):
        return list(self.sections_dictionary)

    def get_safe_index(self, section_uid: str) -> int:
        try:
            return self.section_uid_ordered_list.index(section_uid)
        except ValueError:
            return -1

    def reset_lockout(self):
        """Reset encounter lockouts so a patient can resume their session"""
        self.account_locked_at = None
        self.session_validation_attempts = 0
        self.session_lock = False
        self.last_heartbeat = timezone.now()
        self.save()

    @property
    def has_security_steps(self):
        """
        Returns `True` if the privacy screen image is set and
        security question answer is set.
        """

        if self.privacy_screen_image_id is None:
            return False
        return self.encrypted_question is not None

    @property
    def activities_last_modified(self):
        activities = [activity.get_active_module() for activity in self.filter_activities(active_only=True) if
                      activity.get_status() != ActivityStatus.NOT_STARTED]

        return max([activity.modified for activity in activities]) if activities else None

    @property
    def narrative_note(self):
        """ Produce Narrative Note for Technician. """
        note = NarrativeNote(self)
        return {
            "narrative_note": note.render_narrative_note(),
            "stability_plan_note": note.render_stability_plan_note()
        }




