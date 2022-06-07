import logging

from django.db import models
from model_utils import Choices
from django.utils import timezone
from simple_history.models import HistoricalRecords

from jaspr.apps.common.fields.encrypted_json_field import EncryptedJSONField
from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel
from jaspr.apps.kiosk.activities.outro.model import OutroActivity

logger = logging.getLogger(__name__)


class Outro(JasprAbstractBaseModel, OutroActivity):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    answers = EncryptedJSONField(blank=True, null=True)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Outro Question Answers"
        verbose_name_plural = "Outro Question Answers"

    def save(self, *args, **kwargs):
        answers = self.answers
        if answers:
            if answers.get("check_in_time1") is None and (
                answers.get("distress1") is not None
                and answers.get("frustration1") is not None
            ):
                answers.update({"check_in_time1": timezone.now().isoformat()})

                self.assignedactivity.encounter.create_patient_measurement(
                    distress=answers.get("distress1"),
                    frustration = answers.get("frustration1")
                )

            if answers.get("check_in_time2") is None and (
                answers.get("distress2") is not None
                and answers.get("frustration2") is not None
            ):
                answers.update({"check_in_time2": timezone.now().isoformat()})

                self.assignedactivity.encounter.create_patient_measurement(
                    distress=answers.get("distress2"),
                    frustration=answers.get("frustration2")
                )

        return super().save(*args, **kwargs)
