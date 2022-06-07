import logging

from django.db import models
from model_utils import Choices

from ..activities.stability_plan.model import StabilityPlanActivity
from ...common.models import CrisisStabilityPlanBaseModel
from jaspr.apps.common.fields.encrypted_json_field import EncryptedJSONField

logger = logging.getLogger(__name__)


class CrisisStabilityPlan(CrisisStabilityPlanBaseModel, StabilityPlanActivity):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    # Stores additional answers that may be added to the CSP QuestionList but are not core CSP answers.  These
    # answers stay in the ED and are not copied to JAH
    answers = EncryptedJSONField(blank=True, null=True)

    note_generated = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Last Note Generated Time",
        db_index=True
    )

    class Meta:
        verbose_name = "Crisis Stability Plan"
        verbose_name_plural = "Crisis Stability Plans"
