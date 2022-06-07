import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from model_utils import Choices
from simple_history.models import HistoricalRecords

from jaspr.apps.common.constraints import EnhancedUniqueConstraint
from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel

from ..common.fields import EncryptedJSONField
from .constants import FRONTEND_RENDER_TYPE_CHOICES

logger = logging.getLogger(__name__)


class Walkthrough(JasprAbstractBaseModel):
    """ Container for ordered steps. Allows for labelling, making inactive or setting as a draft. """

    STATUS = Choices("active", "inactive", "draft")

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    history = HistoricalRecords(bases=[RoutableModel])

    def __str__(self):
        return f"{self.name}"


def get_walkthrough_content_types_filter():
    class_names = [
        ("awsmedia", "media"),
        ("kiosk", "guidemessage"),
        ("kiosk", "copingstrategy"),
        ("kiosk", "helpline"),
        ("kiosk", "sharedstory"),
        ("kiosk", "activity"),
    ]

    filter_q = Q()
    for app_label, model in class_names:
        filter_q |= Q(app_label=app_label, model=model)

    return filter_q


class Step(JasprAbstractBaseModel):
    """ Defines possible Steps for all Walkthroughs. """

    STATUS = Choices(
        "active",
        "draft",
    )

    name = models.CharField(
        max_length=100, unique=True, help_text="Administrative shorthand name."
    )

    notes = models.TextField(
        blank=True,
        help_text="Administrative notes about this step. Not publicly viewable.",
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Default Content Type",
        related_name="step_set",
        limit_choices_to=get_walkthrough_content_types_filter,
        null=True,
        blank=True,
    )
    content_object = GenericForeignKey()
    object_id = models.IntegerField(
        verbose_name="Default Object ID", db_index=True, null=True, blank=True
    )

    frontend_render_type = models.CharField(
        choices=FRONTEND_RENDER_TYPE_CHOICES, max_length=25
    )

    skip_if_blank = models.BooleanField("Skip If Blank", default=False)

    function = models.CharField(blank=True, max_length=100)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class WalkthroughStep(JasprAbstractBaseModel):
    """ Each record connects a Walkthrough to a Step with a particular Order. """

    STATUS = Choices(
        "active",
        "draft",
    )

    walkthrough = models.ForeignKey(Walkthrough, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.PROTECT)
    order = models.PositiveSmallIntegerField(default=0)

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Walkthrough Step"
        verbose_name_plural = "Walkthrough Steps"

        ordering = ["order"]

        constraints = (
            EnhancedUniqueConstraint(
                fields=["walkthrough", "order"],
                condition=Q(status="active"),
                name="unique_walkthrough_step_order",
                description="Unique order required when active.",
            ),
            EnhancedUniqueConstraint(
                fields=["walkthrough", "step"],
                condition=Q(status="active"),
                name="unique_walkthrough_with_step",
                description="Unique walkthrough and step together required when active.",
            ),
        )

    def __str__(self):
        return f"{self.walkthrough} - {self.step}"


class PatientWalkthrough(JasprAbstractBaseModel):
    """
    Each row defines which Walkthrough a particular Patient is using.
    This allows additions of Walkthroughs in the future even while a Patient has a previously defined Walkthrough,
    so new Patients can get a newer Walkthrough version and previous Patients are not necessarily updated.
    """

    STATUS = Choices("active", "inactive")

    patient = models.ForeignKey("kiosk.Patient", on_delete=models.CASCADE)
    walkthrough = models.ForeignKey(Walkthrough, on_delete=models.PROTECT)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = "Patient Walkthrough"
        verbose_name_plural = "Patient Walkthroughs"

        # Constraint: Make sure there is only 1 active PatientWalkthrough at a time for a given patient.
        constraints = (
            EnhancedUniqueConstraint(
                fields=["patient"],
                condition=Q(status="active"),
                name="unique_active_patient",
                description="Each patient can only have one active walkthrough at a time.",
            ),
        )

    # TODO Further, if a patient has begun a Walkthrough and the Walkthrough has not reset, the PatientWalkthrough cannot be modified.

    history = HistoricalRecords(bases=[RoutableModel])

    def __str__(self):
        return f"{self.patient} - {self.walkthrough.name}"


class PatientWalkthroughStep(JasprAbstractBaseModel):
    """ Each row in this table defines an (unordered) step for a particular PatientWalkthrough """

    STATUS = Choices("active", "inactive")

    patient_walkthrough = models.ForeignKey(
        PatientWalkthrough, on_delete=models.CASCADE
    )

    step = models.ForeignKey(Step, on_delete=models.PROTECT)

    order = models.PositiveSmallIntegerField(
        default=0, help_text="Copied from Walkthrough Step"
    )

    value = EncryptedJSONField(blank=True, null=True)

    # this field is here and on Step. Maybe it is duplicative?
    # but it also allows for more flexibility in case the render type can vary with a particular step.
    # if this turns out not to be the case, this field can be removed.
    frontend_render_type = models.CharField(
        choices=FRONTEND_RENDER_TYPE_CHOICES, max_length=25
    )

    history = HistoricalRecords(bases=[RoutableModel])

    class Meta:
        verbose_name = "Patient Walkthrough Step"
        verbose_name_plural = "Patient Walkthrough Steps"

        ordering = ["order"]
        constraints = (
            # This constraint fails for supportive people and coping strategies.
            # Leaving this note here to remind us.
            # Constraint: Make sure there is only 1 active PatientWalkthroughStep at a time for a given patient.
            #     EnhancedUniqueConstraint(
            #         fields=['patient_walkthrough', 'step'],
            #         condition=Q(status='active'),
            #         name='unique_active_patientwalkthroughstep',
            #     ),
            # Ensure there is a unique order for each active record that share Patient and WalkthroughStep.
            EnhancedUniqueConstraint(
                fields=[
                    "patient_walkthrough",
                    "step",
                    "order",
                ],
                condition=Q(status="active"),
                name="unique_active_patientwalkthroughsteporder",
                description="Each active patient walkthrough step must be unique.",
            ),
        )

    def __str__(self):
        return f"{self.patient_walkthrough} - {self.step}"

    # TODO: enforce non-editability with patient step -- just add ...
