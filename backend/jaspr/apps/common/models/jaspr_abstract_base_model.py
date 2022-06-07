from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel

class JasprAbstractBaseModel(TimeStampedModel):
    """
    JasprAbstractBaseModel
    Base model for all models in Jaspr; adds the StatusField to all
    models.
    """

    status = StatusField()

    class Meta:
        abstract = True
        
        
