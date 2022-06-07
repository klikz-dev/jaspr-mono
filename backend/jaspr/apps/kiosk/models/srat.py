import logging
from django.db import models
from django.utils import timezone
from model_utils import Choices
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator, MinValueValidator
from fernet_fields import EncryptedCharField, EncryptedDateTimeField

from jaspr.apps.common.fields import EncryptedPositiveSmallIntegerField, EncryptedSmallIntegerField
from jaspr.apps.common.fields.encrypted_json_field import EncryptedJSONField
from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel
from jaspr.apps.kiosk.activities.suicide_assessment.model import SuicideAssessmentActivity, SCORING_CURRENT_ATTEMPT, \
    SCORING_NO_CURRENT_ATTEMPT, SCORING_RISK_LOW, SCORING_RISK_MODERATE, SCORING_RISK_HIGH, \
    SCORING_SUICIDE_NO_PLAN_OR_INTENT, SCORING_SUICIDE_PLAN_OR_INTENT, SCORING_SUICIDE_PLAN_AND_INTENT, \
    SCORING_SUICIDE_INDEX_SCORE_WISH_TO_LIVE, SCORING_SUICIDE_INDEX_SCORE_AMBIVALENT, \
    SCORING_SUICIDE_INDEX_SCORE_WISH_TO_DIE

logger = logging.getLogger(__name__)


class Srat(JasprAbstractBaseModel, SuicideAssessmentActivity):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    answers = EncryptedJSONField(blank=True, null=True)

    note_generated = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Last Note Generated Time",
        db_index=True
    )

    rate_psych_section_viewed = EncryptedDateTimeField(
        blank=True,
        help_text='rate_psych section first viewed at this datetime.',
        null=True
    )

    scoring_score = EncryptedPositiveSmallIntegerField(
        "Scoring - Score",
        blank=True,
        null=True,
        default=None,
        editable=False,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
    )

    SCORING_CURRENT_ATTEMPT_CHOICES = Choices(
        SCORING_CURRENT_ATTEMPT,
        SCORING_NO_CURRENT_ATTEMPT,
    )

    scoring_current_attempt = EncryptedCharField(
        "Scoring - Current Attempt",
        max_length=31,
        blank=True,
        null=True,
        choices=SCORING_CURRENT_ATTEMPT_CHOICES,
        default=None,
        editable=False,
    )

    SCORING_SUICIDE_PLAN_AND_INTENT_CHOICES = Choices(
        SCORING_SUICIDE_PLAN_AND_INTENT,
        SCORING_SUICIDE_PLAN_OR_INTENT,
        SCORING_SUICIDE_NO_PLAN_OR_INTENT,
    )

    scoring_suicide_plan_and_intent = EncryptedCharField(
        "Scoring - Suicide Plan and Intent",
        max_length=31,
        blank=True,
        null=True,
        choices=SCORING_SUICIDE_PLAN_AND_INTENT_CHOICES,
        default=None,
        editable=False,
    )

    SCORING_RISK_CHOICES = Choices(
        SCORING_RISK_LOW, SCORING_RISK_MODERATE, SCORING_RISK_HIGH
    )

    scoring_risk = EncryptedCharField(
        "Scoring - Risk",
        max_length=15,
        blank=True,
        null=True,
        choices=SCORING_RISK_CHOICES,
        default=None,
        editable=False,
    )

    scoring_suicide_index_score = EncryptedSmallIntegerField(
        "Scoring - Suicide Index Score",
        blank=True,
        null=True,
        default=None,
        editable=False,
        validators=[MinValueValidator(-2), MaxValueValidator(2)],
    )

    SCORING_SUICIDE_INDEX_SCORE_TYPOLOGY_CHOICES = Choices(
        SCORING_SUICIDE_INDEX_SCORE_WISH_TO_LIVE,
        SCORING_SUICIDE_INDEX_SCORE_AMBIVALENT,
        SCORING_SUICIDE_INDEX_SCORE_WISH_TO_DIE,
    )

    scoring_suicide_index_score_typology = EncryptedCharField(
        "Scoring - Suicide Index Score Typology",
        max_length=15,
        blank=True,
        null=True,
        choices=SCORING_SUICIDE_INDEX_SCORE_TYPOLOGY_CHOICES,
        default=None,
        editable=False,
    )

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Suicide Risk Assessment Type"
        verbose_name_plural = "Suicide Risk Assessment Types"

    def save(self, *args, **kwargs):
        if self.answers and not self.rate_psych_section_viewed:
            self.rate_psych_section_viewed = timezone.now()
        super().save(*args, **kwargs)

