import logging
from django.db import models
from model_utils import Choices
from jaspr.apps.common.models import JasprAbstractBaseModel

logger = logging.getLogger(__name__)


class ProviderComment(JasprAbstractBaseModel):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))
    encounter = models.ForeignKey(
        'kiosk.Encounter', on_delete=models.CASCADE, verbose_name="Encounter"
    )
    technician = models.ForeignKey(
        "kiosk.Technician", on_delete=models.CASCADE
    )
    answer_key = models.CharField(
        max_length=100,
        help_text="Answer key of the question being referenced",
    )
    comment = models.CharField("Comment", max_length=10000)

    class Meta:
        verbose_name = "Provider Comment"
        verbose_name_plural = "Provider Comments"
