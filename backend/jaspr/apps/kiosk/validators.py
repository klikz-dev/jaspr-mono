from inspect import getmembers
from typing import List, Optional

from django.core.validators import ValidationError
from jaspr.apps.common.validators import zero_positive_integer_validator

from .constants import ActionNames

# NOTE: Will be set by `validate_action_that_is_jah_only` the first time and populated.
JAH_ACTIONS: List[str] = []


def validate_action_with_section_uid(action: str, section_uid: Optional[str]) -> None:
    if action in (ActionNames.SUBMIT, ActionNames.ARRIVE) and not section_uid:
        raise ValidationError(f"A section uid is required with action {action}.")


def validate_action_with_extra(action: str, extra: Optional[str]) -> None:
    if action in (
        ActionNames.WATCH,
        ActionNames.JAH_WALKTHROUGH_ARRIVE,
        ActionNames.JAH_WALKTHROUGH_CLICKED_MORE_INFO,
        ActionNames.JAH_USER_COPY,
        ActionNames.JAH_OPEN_CONCERN,
    ):
        # If we have one of the actions that the `extra` field is expected for, make
        # sure it's present.
        if not extra:
            raise ValidationError(f"The `extra` field is required for action {action}.")


def validate_action_that_is_jah_only(action: str, in_er: bool) -> None:
    global JAH_ACTIONS
    if not JAH_ACTIONS:
        JAH_ACTIONS = [
            value
            for (name, value) in getmembers(ActionNames)
            if name.isupper()
            and isinstance(value, str)
            and name.startswith("JAH_")
            and value.startswith("JAH")
        ]
    if action in JAH_ACTIONS and in_er:
        raise ValidationError(
            f"Must not be in the ER (JAH required) for action {action}."
        )
