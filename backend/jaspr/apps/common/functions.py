from typing import Callable, Optional

from django.conf import settings
from django.core.validators import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import ValidationError as DRFValidationError
from rest_framework.views import exception_handler

from .constraints import (
    check_exception_for_constraint,
    drf_validation_error_from_constraint_spec,
)


def custom_drf_exception_handler(exc: Exception, context: dict) -> Optional[Response]:
    """
    Custom exception handler that currently adds a helpful
    'HAS-VALIDATION-ERROR' header to the response for the frontend
    if a validation error was thrown.

    NOTE/WARNING: This is currently used as the default exception
    error for DRF. Hence, be very careful about renaming or
    changing it as it affects every view/viewset for DRF
    that handles exceptions.
    """
    # If we ran into an exception that was found to be related to a database constraint
    # that we are aware of, we will raise a validation error instead (EBPI-831).
    if (constraint_spec := check_exception_for_constraint(exc)) is not None:
        exc = drf_validation_error_from_constraint_spec(
            constraint_spec, exc, settings.DEBUG
        )
    has_validation_error = False
    if isinstance(exc, (DRFValidationError, ValidationError)):
        has_validation_error = True
    # Call REST framework's default exception handler,
    # getting the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP header to the response.
    if response is not None and has_validation_error:
        response["Has-Validation-Error"] = "true"
    return response


def check_password_complexity(password: str) -> bool:
    """
    Right now, this function is used to set the `account.User`'s `password_complex`
    field. We don't enforce anything around that at the time of writing, though we
    may in the future.

    Also, right now we're defining a password as complex if it has at least eight
    characters, which consist of at least one lowercase character, one uppercase
    character, and one digit.
    """
    return len(password) >= 8 and all(
        any(map(f, password)) for f in [str.islower, str.isupper, str.isdigit]
    )


def sort_dict(d: dict, *, key: Callable = None, reverse: bool = False) -> dict:
    return {k: d[k] for k in sorted(d.keys(), key=key, reverse=reverse)}


def resolve_frontend_url(clinic_slug=None, technician=None):
    if technician is not None:
        clinic_slug = technician.system.organization_code

    if clinic_slug is None:
        clinic_slug = "nonclinic"

    url = settings.FRONTEND_URL_BASE.replace("*", clinic_slug)
    return url
