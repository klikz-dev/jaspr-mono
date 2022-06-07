from functools import cached_property
from typing import List

from django.apps import apps
from django.db import transaction
from rest_framework import serializers

from .supportive_person import SupportivePersonSerializer
from jaspr.apps.kiosk.helpers import update_coping_fields
from jaspr.apps.kiosk.models import CopingStrategyCategory


class CrisisStabilityPlanSerializer(serializers.ModelSerializer):
    supportive_people = serializers.ListField(
        child=SupportivePersonSerializer(),
        allow_null=True,
        required=False,
    )

    # Temp fix for devices running version 1.1.6.  Remove Q4 2021
    def to_representation(self, *args, **kwargs):
        ret = super().to_representation(*args, **kwargs)
        reasons_live = ret.get("reasons_live", [])
        ret["reasons_live"] = reasons_live
        return ret

    class Meta:
        model = None
        fields = [
            "reasons_live",
            "strategies_general",
            "strategies_firearm",
            "strategies_medicine",
            "strategies_places",
            "strategies_other",
            "strategies_custom",
            "means_support_yes_no",
            "means_support_who",
            "coping_body",
            "coping_distract",
            "coping_help_others",
            "coping_courage",
            "coping_senses",
            "supportive_people",
            "coping_top",
            "ws_stressors",
            "ws_thoughts",
            "ws_feelings",
            "ws_actions",
            "ws_top",
        ]

    def _has_changed(self, instance, new_values):
        for answer_key in self.Meta.fields:
            original_value = getattr(instance, answer_key)
            if answer_key not in new_values:
                new_value = None
            else:
                new_value = new_values[answer_key]
            if original_value is not new_value:
                return True
        return False

    @transaction.atomic
    def update(self, instance, validated_data):

        old_instance = instance
        instance = (
            type(instance).objects.select_for_update().get(pk=instance.pk)
        )

        instance = super().update(instance, validated_data)

        update_coping_fields(old_instance, instance)

        return instance
