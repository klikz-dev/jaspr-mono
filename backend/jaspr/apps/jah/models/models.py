import logging

from django.db import models
from model_utils import Choices

from jaspr.apps.common.models import JasprAbstractBaseModel

logger = logging.getLogger(__name__)


class ConversationStarter(JasprAbstractBaseModel):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))
    content = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Conversation Starter"
        verbose_name_plural = "Conversation Starters"
        ordering = ["order"]

    def __str__(self):
        if len(self.content) > 80:
            return f"{self.content[:75]}...."
        return self.content


class CommonConcern(JasprAbstractBaseModel):
    STATUS = Choices(("active", "Active"), ("archived", "Archived"))
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Common Concern"
        verbose_name_plural = "Common Concerns"
        ordering = ["order"]

    def __str__(self):
        if len(self.title) > 55:
            return f"{self.title[:50]}...."
        return self.title
