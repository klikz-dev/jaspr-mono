from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import ValidationError as DRFValidationError
from rest_framework.settings import api_settings

from .constraints import (
    check_exception_for_constraint,
    drf_validation_error_from_constraint_spec,
)


class AssureNonFieldErrorsMixin:
    """
    A mixin (that should be included before something like
    `APIView` or `viewsets.GenericViewSet`, etc.) that converts
    a list of errors to a dictionary with that list set as the
    value of the non field errors key.
    """

    def handle_exception(self, exc: Exception) -> Response:
        """
        Since we're raising validation errors in the view/viewset, we want to
        convert a list of validation errors to a dictionary with
        the list as the value corresponding to the non field errors key.
        """
        # If we ran into an exception that was found to be related to a database
        # constraint that we are aware of, we will raise a validation error instead
        # (EBPI-831).
        # NOTE: This is also in the custom global DRF exception handler. Should be a
        # very small/negligible performance impact since `isinstance` checks are cached
        # and we're only making one extra check here. This allows us to still
        # standardize non field errors to the dictionary below this, as, at the time of
        # writing, the constriant handler here is the only piece of code that runs to
        # check if an exception should be converted into a `DRFValidationError`
        # instead.
        if (constraint_spec := check_exception_for_constraint(exc)) is not None:
            exc = drf_validation_error_from_constraint_spec(
                constraint_spec, exc, settings.DEBUG
            )
        if isinstance(exc, (DRFValidationError, ValidationError)) and isinstance(
            exc.detail, list
        ):
            exc.detail = {api_settings.NON_FIELD_ERRORS_KEY: exc.detail}
        return super().handle_exception(exc)
