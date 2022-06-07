import logging

from django.db import models
from model_utils import Choices
from simple_history.models import HistoricalRecords

from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel

logger = logging.getLogger(__name__)


class JAHAccount(JasprAbstractBaseModel):

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    patient = models.OneToOneField(
        "kiosk.Patient", on_delete=models.CASCADE, verbose_name="Patient"
    )

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "JAH Account"
        verbose_name_plural = "JAH Accounts"
