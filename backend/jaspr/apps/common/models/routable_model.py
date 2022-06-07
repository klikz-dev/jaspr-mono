from django.db import models
from model_utils import Choices

class RoutableModel(models.Model):
    """
    RoutableModel
    Required model to allow django-simple-history and django-model-utils to
    work together.  This provides a STATUS-Choices required for any model that
    uses StatusField.  Since virtually all of our models will inherit this, the
    HistoryRecord must use this model as a base. These are not used for
    anything but a placeholder.
    """

    # * NOTE/TODO: Is this still required?
    STATUS = Choices("choice1", "choice2")

    class Meta:
        abstract = True
