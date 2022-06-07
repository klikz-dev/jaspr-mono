import logging
from django import template
from django.db import models
from django.template import Context
from model_utils import Choices
from simple_history.models import HistoricalRecords
from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel

logger = logging.getLogger(__name__)


class NoteTemplate(JasprAbstractBaseModel):

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    name = models.CharField(max_length=255)

    template = models.TextField()

    history = HistoricalRecords(bases=[RoutableModel])

    def __str__(self):
        return f"({self.pk}) {self.name}"

    class Meta:
        verbose_name = "Note Template"
        verbose_name_plural = "Note Templates"

    def render(self, context={}) -> str:
        context = Context(context)
        try:
            rendered_template = template.Template(self.template).render(context)
        except Exception as e:
            logger.exception(f"Unable to render template {self.pk}")
            raise e

        return rendered_template

