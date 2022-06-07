import logging

from django.db import models
from django.utils import timezone
from model_utils import Choices
from simple_history.models import HistoricalRecords

from jaspr.apps.common.fields.encrypted_json_field import EncryptedJSONField
from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel
from jaspr.apps.kiosk.activities.intro.model import IntroActivity

logger = logging.getLogger(__name__)


class CustomOnboardingQuestions(JasprAbstractBaseModel, IntroActivity):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    answers = EncryptedJSONField(blank=True, null=True)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Custom Onboarding Question"
        verbose_name_plural = "Custom Onboarding Questions"

    def save(self, *args, **kwargs):
        answers = self.answers
        if answers:
            if answers.get("check_in_time0") is None and (
                answers.get("distress0") is not None
                and answers.get("frustration0") is not None
            ):
                answers.update({"check_in_time0": timezone.now().isoformat()})
                self.assignedactivity.encounter.create_patient_measurement(
                    distress=answers.get("distress0"),
                    frustration=answers.get("frustration0")
                )
        return super().save(*args, **kwargs)
