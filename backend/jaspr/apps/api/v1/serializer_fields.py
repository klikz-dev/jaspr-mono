from django.utils import timezone
from rest_framework import serializers


class CurrentPatientDefault:
    """
    Thanks to DRF's `CurrentUserDefault` for the implementation.

    See: https://github.com/encode/django-rest-framework/blob/9d06e43d05abf1ec57f15566b29ad53ac418ae05/rest_framework/fields.py#L281
    Also See: https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    """

    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].user.patient

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class CurrentPatientEncounterDefault:
    """
    Thanks to DRF's `CurrentUserDefault` for the implementation.

    See: https://github.com/encode/django-rest-framework/blob/9d06e43d05abf1ec57f15566b29ad53ac418ae05/rest_framework/fields.py#L281
    Also See: https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    """

    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].user.patient.current_encounter

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class CurrentEncounterDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].auth.jaspr_session.encounter

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class CurrentTechnicianDefault:
    """
    Thanks to DRF's `CurrentUserDefault` for the implementation.

    See: https://github.com/encode/django-rest-framework/blob/9d06e43d05abf1ec57f15566b29ad53ac418ae05/rest_framework/fields.py#L281
    Also See: https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    """

    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].user.technician

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class ContextDefault:
    requires_context = True

    def __init__(self, context_key: str) -> None:
        self.context_key = context_key

    def __call__(self, serializer_field):
        return serializer_field.context[self.context_key]

    def __repr__(self):
        return f"{self.__class__.__name__}(context_key={self.context_key})"


class ContextUserDefault(ContextDefault):
    def __init__(self, context_key: str = "user") -> None:
        super().__init__(context_key)


class ViewedTimestampField(serializers.DateTimeField):
    """
    Thanks to https://github.com/encode/django-rest-framework/blob/9811a29a5a1348f1a5de30a9a7a5d0f8d2fd4843/rest_framework/fields.py#L633
    for the `BooleanField` mixin components.
    """

    default_error_messages = {
        "invalid": "Must be a valid boolean.",
        "no_false": "'false' is not an allowed option. Specify either 'true' or 'null'.",
    }
    TRUE_VALUES = {
        "t",
        "T",
        "y",
        "Y",
        "yes",
        "YES",
        "true",
        "True",
        "TRUE",
        "on",
        "On",
        "ON",
        "1",
        1,
        True,
    }
    FALSE_VALUES = {
        "f",
        "F",
        "n",
        "N",
        "no",
        "NO",
        "false",
        "False",
        "FALSE",
        "off",
        "Off",
        "OFF",
        "0",
        0,
        0.0,
        False,
    }
    NULL_VALUES = {"null", "Null", "NULL", "", None}

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("allow_null", True)
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            if data in self.TRUE_VALUES:
                return timezone.now()
            elif data in self.FALSE_VALUES:
                self.fail("no_false")
            elif data in self.NULL_VALUES and self.allow_null:
                return None
        except TypeError:  # Input is an unhashable type
            pass
        self.fail("invalid")
