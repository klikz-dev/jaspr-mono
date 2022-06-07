import logging

from simple_history.models import HistoricalRecords
from model_utils import Choices
from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel
from jaspr.apps.common.fields.encrypted_json_field import EncryptedJSONField
from jaspr.apps.kiosk.activities.lethal_means.model import LethalMeansActivity

logger = logging.getLogger(__name__)


class LethalMeans(JasprAbstractBaseModel, LethalMeansActivity):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    answers = EncryptedJSONField(blank=True, null=True)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Lethal Means Counseling"
        verbose_name_plural = "Lethal Means Counselings"

