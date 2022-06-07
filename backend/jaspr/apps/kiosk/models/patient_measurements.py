import logging

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from model_utils import Choices

from jaspr.apps.common.fields import EncryptedPositiveSmallIntegerField
from jaspr.apps.common.models import JasprAbstractBaseModel

logger = logging.getLogger(__name__)


class PatientMeasurements(JasprAbstractBaseModel):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    encounter = models.ForeignKey(
        "kiosk.Encounter", on_delete=models.CASCADE, verbose_name="Encounter"
    )

    frustration = EncryptedPositiveSmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    distress = EncryptedPositiveSmallIntegerField(
        blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    screen = models.CharField(
        max_length=50,
        help_text="Screen where the measurement occurred",
        null=True,
        blank=True
    )
    ux_format = models.CharField(
        max_length=50,
        help_text="UX Format of the measurement",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Patient Measurement"
        verbose_name_plural = "Patient Measurements"
