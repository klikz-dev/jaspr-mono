import logging

from django.db import models
from model_utils import Choices


from ...common.models import CrisisStabilityPlanBaseModel

logger = logging.getLogger(__name__)


class CrisisStabilityPlan(CrisisStabilityPlanBaseModel):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    jah_account = models.OneToOneField(
        "jah.JAHAccount", on_delete=models.CASCADE, verbose_name="JAH Account"
    )

    class Meta:
        verbose_name = "JAH Crisis Stability Plan"
        verbose_name_plural = "JAH Crisis Stability Plans"
