import logging

from django.db import models
from jaspr.apps.common.constraints import EnhancedUniqueConstraint

from ...common.models import PatientCopingStrategyBaseModel

logger = logging.getLogger(__name__)


class PatientCopingStrategy(PatientCopingStrategyBaseModel):

    encounter = models.ForeignKey("kiosk.Encounter", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Patient Coping Strategy"
        verbose_name_plural = "Patient Coping Strategies"
        ordering = ["title"]

        constraints = (
            EnhancedUniqueConstraint(
                fields=["title", "encounter"],
                name="patientcopingstrategy_title_and_patient_encounter_unique_together",
                description="Title needs to be unique per encounter.",
            ),
        )
