from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from textwrap import dedent
from typing import Dict, Optional, Sequence, Union

from django.db import IntegrityError
from django.db.models import CheckConstraint, Q, UniqueConstraint
from rest_framework.serializers import ValidationError as DRFValidationError

logger = logging.getLogger(__name__)


@dataclass
class EnhancedConstraintSpec:
    constraint: Union[CheckConstraint, UniqueConstraint]
    # A user-friendly/human readable description of the constraint.
    description: str

    def error_message_generic(self, exception: Exception) -> str:
        return (
            "Something unexpected happened. Feel free to try again, and if the problem "
            "persists, contact support."
        )

    def error_message_detailed(self, exception: Exception) -> str:
        raise NotImplementedError(
            "Subclasses should implement a detailed error message."
        )


@dataclass
class EnhancedCheckConstraintSpec(EnhancedConstraintSpec):
    constraint: CheckConstraint

    def error_message_detailed(self, exception: Exception) -> str:
        return dedent(
            f"""
            {self.constraint.__class__.__name__}
            {self.description}

            (Check failed: {self.constraint.check})
            """
        ).strip()


@dataclass
class EnhancedUniqueConstraintSpec(EnhancedConstraintSpec):
    constraint: UniqueConstraint

    def error_message_detailed(self, exception: Exception) -> str:
        error_message = dedent(
            f"""
        {self.constraint.__class__.__name__}
        {self.description}

        (Fields: {self.constraint.fields})
        """
        ).strip()
        if self.constraint.condition is not None:
            error_message += f"\n\n(Condition: {self.constraint.condition})"
        return error_message


# Map of the `name` of the constraint to the `constraint_type`, `constraint_description`,
_CONSTRAINT_DESCRIPTION_REGISTRY: Dict[str, EnhancedConstraintSpec] = {}


class EnhancedCheckConstraint:
    def __new__(self, *, check: Q, name: str, description: str) -> CheckConstraint:
        constraint = CheckConstraint(check=check, name=name)
        assert (
            constraint.name not in _CONSTRAINT_DESCRIPTION_REGISTRY
        ), f"Constraint with `name={constraint.name}` already present."
        _CONSTRAINT_DESCRIPTION_REGISTRY[constraint.name] = EnhancedCheckConstraintSpec(
            constraint, description
        )
        return constraint


class EnhancedUniqueConstraint:
    def __new__(
        self,
        *,
        fields: Sequence[str],
        name: str,
        condition: Q = None,
        description: str,
    ) -> UniqueConstraint:
        constraint = UniqueConstraint(fields=fields, name=name, condition=condition)
        assert (
            constraint.name not in _CONSTRAINT_DESCRIPTION_REGISTRY
        ), f"Constraint with `name={constraint.name}` already present."
        _CONSTRAINT_DESCRIPTION_REGISTRY[
            constraint.name
        ] = EnhancedUniqueConstraintSpec(constraint, description)
        return constraint


_CONSTRAINT_REGEX = re.compile(r"constraint\s+\"(\S+)\"")


def check_exception_for_constraint(
    exception: Exception,
) -> Optional[EnhancedConstraintSpec]:
    if isinstance(exception, IntegrityError):
        exception_string = str(exception)
        if match := _CONSTRAINT_REGEX.search(exception_string):
            constraint_name = match.group(1)
            if constraint_name in _CONSTRAINT_DESCRIPTION_REGISTRY:
                return _CONSTRAINT_DESCRIPTION_REGISTRY[constraint_name]
            logger.warning(
                'Saw constraint name "%s" in %s but it wasn\'t found in the registry.',
                constraint_name,
                exception_string,
            )


def drf_validation_error_from_constraint_spec(
    spec: EnhancedConstraintSpec, exc: Exception, show_detailed: bool
) -> DRFValidationError:
    if show_detailed:
        error_message = spec.error_message_detailed(exc)
    else:
        error_message = spec.error_message_generic(exc)
    new_exc = DRFValidationError(error_message, code="constraint")
    # NOTE: Intentionally use `raise from` to set the `__context__` and let python's
    # machinery handle anything else in terms of the other details of exception
    # handling. We'll catch it right after it's raised.
    try:
        raise new_exc from exc
    except new_exc.__class__ as e:
        new_exc = e
    return new_exc
