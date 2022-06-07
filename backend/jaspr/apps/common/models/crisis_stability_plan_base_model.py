import logging
from typing import List

from django.core.exceptions import ValidationError
from django.apps import apps
from django.db import models
from django.db.models.fields import Field
from fernet_fields import EncryptedCharField
from model_utils import Choices
from simple_history.models import HistoricalRecords

from jaspr.apps.common.decorators import classproperty
from jaspr.apps.common.fields import EncryptedArrayField, EncryptedJSONField, EncryptedBooleanField
from jaspr.apps.common.models import JasprAbstractBaseModel, RoutableModel

logger = logging.getLogger(__name__)


class CrisisStabilityPlanBaseModel(JasprAbstractBaseModel):
    """The Crisis Stability plan is used both in the ED and JAH.  When initializing a JAH CSP
    we copy from the ED to JAH a new isolated copy.  We use the same base model to ensure that
    the schema between the ED and JAH versions of the model are identical"""

    SUPPORTIVE_PERSON_NAME_MAX_LENGTH = 45
    SUPPORTIVE_PERSON_PHONE_MAX_LENGTH = 21

    STATUS = Choices(("active", "Active"), ("archived", "Archived"))

    # --- SSF-A ---
    reasons_live = EncryptedArrayField(
        models.CharField(max_length=10000), size=5, blank=True, null=True
    )

    # --- Make Home Safer ---
    strategies_general = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    strategies_firearm = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    strategies_medicine = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    strategies_places = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    strategies_other = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    strategies_custom = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    means_support_yes_no = EncryptedBooleanField(null=True)
    means_support_who = EncryptedCharField(blank=True, null=True, max_length=10000)

    # --- Plan to Cope ---
    coping_body = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    coping_distract = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    coping_help_others = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    coping_courage = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    coping_senses = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    supportive_people = EncryptedJSONField(blank=True, null=True)
    coping_top = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    ws_stressors = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    ws_thoughts = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    ws_feelings = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    ws_actions = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )
    ws_top = EncryptedArrayField(
        models.CharField(max_length=10000), blank=True, null=True
    )

    history = HistoricalRecords(bases=[RoutableModel], inherit=True)

    class Meta:
        abstract = True

    @property
    def supportive_people_flattened(self):
        """
        Here so that `check_and_reduce_top_for` can handle `supportive_people`, which
        isn't a `list` of strings. That makes it act like a list of strings.
        """
        value = [f"{d['name']} ({d['phone']})" for d in self.supportive_people or []]
        return value

    def check_and_reduce_top_for(
        self, top_field_name: str, *field_names_to_check: str
    ) -> None:
        top_field = getattr(self, top_field_name)
        # Don't proceed if the value is already empty/null.
        if not top_field:
            return
        assert isinstance(top_field, list), f"`{top_field_name}` should be a `list`."
        field_names_and_values_to_check = (
            (name, value)
            for name, value in (
                (name, getattr(self, name)) for name in field_names_to_check
            )
            if value
        )
        check_against = set()
        for field_name, field_value in field_names_and_values_to_check:
            if not field_value:
                continue
            assert isinstance(field_value, list), f"`{field_name}` should be a `list`."
            check_against |= set(field_value)
        new_top_field = [v for v in top_field if v in check_against]
        if len(new_top_field) != len(top_field):
            setattr(self, top_field_name, new_top_field)

    @classmethod
    def get_serializer(clz):
        # Importing here, otherwise we get circular dependency errors
        from jaspr.apps.api.v1.serializers.crisis_stability_plan import (
            CrisisStabilityPlanSerializer,
        )

        crisis_stability_plan_serializer = CrisisStabilityPlanSerializer
        crisis_stability_plan_serializer.Meta.model = clz
        return crisis_stability_plan_serializer

    @staticmethod
    def get_csp_fields_filter():
        all_fields = [f.name for f  in CrisisStabilityPlanBaseModel._meta.get_fields()]
        return filter(lambda field: field != "status", all_fields)


    @classproperty(lazy=True)
    def coping_fields(cls) -> List[Field]:
        """
        Return the fields associated with coping strategies, excluding coping_top.
        """
        return list(
            filter(
                lambda field: field.name
                and field.name.startswith("coping_")
                and field.name != "coping_top",
                cls._meta.get_fields(include_parents=False),
            )
        )

    def validate_and_sanitize_supportive_people(self) -> None:
        value = self.supportive_people
        if value is not None and not isinstance(value, list):
            raise ValidationError(
                "Supportive people should either be `None` or a `list`."
            )
        if not value:
            return
        sanitized_value = []
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                raise ValidationError(
                    f"Supportive people index {index}: Item should be a `dict`."
                )
            name = item.get("name")
            if name is not None and not isinstance(name, str):
                raise ValidationError(
                    f"Supportive people index {index}: The `name` should be a `str`."
                )
            if name and len(name) > self.SUPPORTIVE_PERSON_NAME_MAX_LENGTH:
                raise ValidationError(
                    f"Supportive people index {index}: The `name` can be at most {self.SUPPORTIVE_PERSON_NAME_MAX_LENGTH} characters."
                )
            phone = item.get("phone")
            if phone is not None and not isinstance(phone, str):
                raise ValidationError(
                    f"Supportive people index {index}: The `phone` should be a `str`."
                )
            if phone and len(phone) > self.SUPPORTIVE_PERSON_PHONE_MAX_LENGTH:
                raise ValidationError(
                    f"Supportive people index {index}: The `phone` can be at most {self.SUPPORTIVE_PERSON_PHONE_MAX_LENGTH} characters."
                )
            # Ignore the items that have name and phone both empty.
            if name or phone:
                sanitized_value.append({"name": name or "", "phone": phone or ""})
        self.supportive_people = sanitized_value

    def save(self, *args, **kwargs):
        self.validate_and_sanitize_supportive_people()
        self.check_and_reduce_top_for(
            "coping_top",
            "coping_body",
            "coping_distract",
            "coping_help_others",
            "coping_courage",
            "coping_senses",
            "supportive_people_flattened",
        )
        self.check_and_reduce_top_for(
            "ws_top", "ws_stressors", "ws_thoughts", "ws_feelings", "ws_actions"
        )
        return super().save(*args, **kwargs)
