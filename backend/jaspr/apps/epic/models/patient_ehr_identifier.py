from django.db import models
from model_utils import Choices

from jaspr.apps.common.models import JasprAbstractBaseModel


class PatientEhrIdentifier(JasprAbstractBaseModel):
    STATUS = Choices("active")

    fhir_id = models.CharField(blank=True, max_length=64, verbose_name='FHIR ID')

    epic_settings = models.ForeignKey("epic.EpicSettings", on_delete=models.CASCADE)
    patient = models.ForeignKey("kiosk.Patient", on_delete=models.CASCADE)
