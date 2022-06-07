from __future__ import annotations
from django.db import models
from model_utils import Choices
from simple_history.models import HistoricalRecords

from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel

class PatientCopingStrategyBaseModel(JasprAbstractBaseModel):
    """Each record tracks a custom coping strategy created by a patient.
    Custom coping strategies are not shared between patients or encounters.
    There can be many custom coping strategies for one encounter as well as the JAH CSP.
    """

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    title = models.CharField(
        max_length=100,
        help_text="Public title of this coping strategy, currently used to connect frontend to backend as a key.",
    )
    category = models.ForeignKey(
        'kiosk.CopingStrategyCategory',
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_coping_strategy_category",
    )

    history = HistoricalRecords(bases=[RoutableModel], inherit=True)

    class Meta:
        abstract = True

    # TODO: make sure that we cannot under any cirmcumstance create records with the same title as a coping strategy.
    def __str__(self):
        return self.title
