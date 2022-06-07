import logging

from django.db import models
from jaspr.apps.common.constraints import EnhancedUniqueConstraint

from ...common.models import PatientCopingStrategyBaseModel

logger = logging.getLogger(__name__)


class PatientCopingStrategy(PatientCopingStrategyBaseModel):

    jah_account = models.ForeignKey(
        "jah.JAHAccount", on_delete=models.CASCADE, verbose_name="JAH Account"
    )

    class Meta:
        verbose_name = "Patient Coping Strategy"
        verbose_name_plural = "Patient Coping Strategies"
        ordering = ["title"]

        constraints = (
            EnhancedUniqueConstraint(
                fields=["title", "jah_account"],
                name="patientcopingstrategy_title_and_patient_jah_account_unique_together",
                description="Title needs to be unique per JAH account.",
            ),
        )
