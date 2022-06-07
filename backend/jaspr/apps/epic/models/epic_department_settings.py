from django.db import models
from model_utils import Choices

from jaspr.apps.clinics.models import Department
from jaspr.apps.common.models import JasprAbstractBaseModel

from .epic_settings import EpicSettings


class EpicDepartmentSettings(JasprAbstractBaseModel):
    STATUS = Choices("active")

    epic_settings = models.ForeignKey(EpicSettings, on_delete=models.CASCADE)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name="Department",
        blank=True,
        null=True,
    )

    location_code = models.CharField(
        "Location Code",
        max_length=64,
        blank=True,
        null=True,
        help_text="Key used to determine the location during oauth."
                  "This must match the ENCDEPID stored in Epic for the department",
    )

    narrative_note_key = models.CharField(
        "Narrative Note Type Code", max_length=100, blank=True
    )
    stability_plan_note_key = models.CharField(
        "Stability Plan Type Code", max_length=100, blank=True
    )
    narrative_note_system_key = models.CharField(
        "Narrative Note System Code", max_length=100, blank=True
    )
    stability_plan_system_key = models.CharField(
        "Narrative Note System Code", max_length=100, blank=True
    )

    class Meta:
        verbose_name = "Epic Department Settings"
        verbose_name_plural = "Epic Department Settings"
        unique_together = (("epic_settings", "location_code"),)

    @classmethod
    def for_department(clz, department):
        department_ehr = (
            clz.objects.filter(department=department, status="active")
            .select_related("epic_settings")
            .first()
        )
        return department_ehr
