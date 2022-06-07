import logging

from django.apps import apps
from django.db import models
from django.utils import timezone
from fernet_fields import EncryptedCharField
from model_utils import Choices
from simple_history.models import HistoricalRecords

from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel

logger = logging.getLogger(__name__)


class PatientDepartmentSharing(JasprAbstractBaseModel):

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    patient = models.ForeignKey(
        "kiosk.Patient", on_delete=models.CASCADE, verbose_name="Patient"
    )

    department = models.ForeignKey(
        "clinics.Department", on_delete=models.CASCADE, verbose_name="Department", null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "PatientDepartmentSharing"
        verbose_name_plural = "PatientDepartmentSharings"
