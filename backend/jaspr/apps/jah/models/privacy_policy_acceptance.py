import logging

from django.db import models
from model_utils import Choices
from simple_history.models import HistoricalRecords

from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel

from jaspr.apps.kiosk.authentication import (
    JasprToolsToGoUidAndTokenAuthentication,
)

logger = logging.getLogger(__name__)


class PrivacyPolicyAcceptance(JasprAbstractBaseModel):

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    jah_account = models.ForeignKey(
        "jah.JAHAccount", on_delete=models.CASCADE, verbose_name="JAH Account"
    )

    # When we make changes to our privacy policy, we should bump the default value
    version = models.PositiveSmallIntegerField(default=1)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Privacy Policy Acceptance"
        verbose_name_plural = "Privacy Policy Acceptances"
