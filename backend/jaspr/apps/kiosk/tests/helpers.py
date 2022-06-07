from datetime import timedelta
from itertools import product
from typing import Any, Dict, List, Sequence, Tuple

from django.test import SimpleTestCase, override_settings
from django.utils.functional import cached_property

from jaspr.apps.kiosk.models import JasprSessionError, JasprSessionUserFacingError


class AnyValid:
    """Helper class that represents any valid value."""


class Parametrizer:
    def __init__(self, mapping: Dict[str, Sequence[Any]], sequences: Sequence[Tuple]):
        self.mapping = mapping
        self.sequences = sequences

    @cached_property
    def result(self) -> Dict[Tuple, Any]:
        values_list = list(self.mapping.values())
        parametrizations = []
        for sequence in self.sequences:
            current_parametrization = [()]
            for index, value in enumerate(sequence):
                add_on = values_list[index] if value is AnyValid else (value,)
                current_parametrization = [
                    (*growing_list, valid_value)
                    for growing_list, valid_value in product(
                        current_parametrization, add_on
                    )
                ]
            parametrizations.extend(current_parametrization)
        length = len(self.mapping)
        return {p[:length]: p[length:] for p in parametrizations}

    @cached_property
    def all_mapping_parametrizations(self) -> List[Tuple]:
        return list(product(*self.mapping.values()))


@override_settings(
    IN_ER_TECHNICIAN_DEFAULT_TOKEN_EXPIRES_AFTER=timedelta(hours=1),
    IN_ER_PATIENT_DEFAULT_TOKEN_EXPIRES_AFTER=timedelta(hours=2),
    AT_HOME_PATIENT_DEFAULT_TOKEN_EXPIRES_AFTER=timedelta(hours=3),
    AT_HOME_PATIENT_LONG_LIVED_TOKEN_EXPIRES_AFTER=timedelta(hours=4),
    IN_ER_TECHNICIAN_DEFAULT_TOKEN_MIN_REFRESH_INTERVAL_SECONDS=60,
    IN_ER_PATIENT_DEFAULT_TOKEN_MIN_REFRESH_INTERVAL_SECONDS=120,
    AT_HOME_PATIENT_DEFAULT_TOKEN_MIN_REFRESH_INTERVAL_SECONDS=180,
    AT_HOME_PATIENT_LONG_LIVED_TOKEN_MIN_REFRESH_INTERVAL_SECONDS=240,
)
class JasprSessionParametrizationTestMixin(SimpleTestCase):
    jaspr_session_params_valid_value_mapping = {
        "in_er": [True, False],
        "from_native": [True, False],
        "long_lived": [True, False],
    }

    technician_combinations = (
        # Think of it this way:
        # If it's allowed:
        # (`in_er`, `from_native`, `long_lived`, `expected_expiration_timedelta`, `expected_min_refresh_interval_timedelta`)
        # If it's not allowed:
        # (`in_er`, `from_native`, `long_lived`, `expected_exception_class`, `expected_exception_message`)
        (True, False, False, timedelta(hours=1), timedelta(seconds=60)),
        (
            False,
            AnyValid,
            AnyValid,
            JasprSessionUserFacingError,
            "Technicians can only access Jaspr in the ER right now.",
        ),
        (
            True,
            True,
            AnyValid,
            JasprSessionUserFacingError,
            "Technicians cannot access native Jaspr apps right now.",
        ),
        (
            True,
            False,
            True,
            JasprSessionError,
            "Technicians cannot have long lived tokens.",
        ),
    )

    patient_combinations = (
        # Think of it this way:
        # If it's allowed:
        # (`in_er`, `from_native`, `long_lived`, `expected_expiration_timedelta`, `expected_min_refresh_interval_timedelta`)
        # If it's not allowed:
        # (`in_er`, `from_native`, `long_lived`, `expected_exception_class`, `expected_exception_message`)
        (True, False, False, timedelta(hours=2), timedelta(seconds=120)),
        (False, AnyValid, False, timedelta(hours=3), timedelta(seconds=180)),
        (False, AnyValid, True, timedelta(hours=4), timedelta(seconds=240)),
        (
            True,
            True,
            AnyValid,
            JasprSessionUserFacingError,
            "Patients cannot access Jaspr in the ER from native apps right now.",
        ),
        (
            True,
            False,
            True,
            JasprSessionError,
            "Patients cannot have long lived tokens in the ER.",
        ),
    )
