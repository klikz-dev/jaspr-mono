import logging

from model_utils import Choices
from simple_history.models import HistoricalRecords

from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel
from jaspr.apps.kiosk.activities.comfort_and_skills.model import ComfortAndSkillsActivity

logger = logging.getLogger(__name__)


class ComfortAndSkills(JasprAbstractBaseModel, ComfortAndSkillsActivity):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    history = HistoricalRecords(bases=[RoutableModel])


    class Meta:
        verbose_name = "Comfort and Skills"
        verbose_name_plural = "Comfort and Skills"