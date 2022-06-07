import logging
from django.db import models
from model_utils import Choices
from jaspr.apps.common.models import JasprAbstractBaseModel

logger = logging.getLogger(__name__)


class AssignmentLocks(JasprAbstractBaseModel):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))
    activity = models.ForeignKey(
        "kiosk.AssignedActivity", on_delete=models.CASCADE
    )
    locked = models.BooleanField(
        "Locked?",
        default=False,
        help_text="Indicates whether or not the assignment is locked",
    )
    acknowledged = models.BooleanField(
        default=False, help_text="Indicates whether the patient has acknowledge the assignment lock change"
    )

    class Meta:
        verbose_name = "Assessment Lock"
        verbose_name_plural = "Assessment Locks"
        ordering = ["-modified"]
