"""
Custom Django system checks for our API. These are meant to be used/extended over
time as we see fit. NOTE that, at the time of writing, these do not necessarily catch
all potential permissions/security problems, etc. They catch basic ones and try to
help catch permissions (at the time of writing) problems related to ordering and lack
of inclusion. For example though, right now, we don't detect custom
`get_permissions()` calls. In the future, we could monkeypatch every `APIView`
subclass during the test and catch those errors, etc. but this is what we're doing
for now.

H004: Should not have duplicate permissions in `permissions_classes`.
H005: Should have `IsInER` specified when `IsTechnician` is specified.
H006: Should have `SatisfiesClinicLocationIPWhitelistingFromTechnician` specified when `IsTechnician` is specified.
H007: `IsTechnician`, `IsInER`, and `SatisfiesClinicLocationIPWhitelistingFromTechnician` are not in the correct order.
H008: For `IsPatient`, `IsInER` and `SatisfiesClinicLocationIPWhitelistingFromPatient` must either both be specified, or neither.
H009: `IsPatient`, `IsInER`, and `SatisfiesClinicLocationIPWhitelistingFromPatient` are not in the correct order."
"""
from itertools import chain
from typing import List, Sequence, Set, Type, Union

import django.apps
from django.core import checks
from rest_framework.views import APIView

from jaspr.apps.api.v1.permissions import (
    IsInER,
    IsPatient,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromPatient,
    SatisfiesClinicIPWhitelistingFromTechnician,
)
from jaspr.apps.kiosk.authentication import JasprTokenAuthentication


def check_api_view_permissions_consistency(
    api_view_class: Type[APIView],
) -> List[checks.Error]:
    """
    Check a single `APIView` class/subclass for permissions consistency.
    """
    errors: List[check.Error] = []
    if not hasattr(api_view_class, "permission_classes"):
        return errors
    permissions_classes = api_view_class.permission_classes
    if not isinstance(permissions_classes, (list, tuple)):
        permissions_classes = [*permissions_classes]
    authentication_classes = api_view_class.authentication_classes

    if len(permissions_classes) != len(set(permissions_classes)):
        errors.append(
            checks.Error(
                "Should not have duplicate permissions in `permissions_classes`.",
                hint="Remove duplicate permissions.",
                obj=api_view_class,
                id="H004",
            )
        )

    if IsTechnician in permissions_classes:
        # If we don't have `JasprTokenAuthentication` we don't need the `IsInER`
        # permission since that checks from the `JasprSession`.
        # `SatisfiesClinicLocationIPWhitelistingFromTechnician` is sufficient in the
        # non `JasprTokenAuthentication` cases since it will actually check at the IP
        # level.
        if (
            JasprTokenAuthentication in authentication_classes
            and IsInER not in permissions_classes
        ):
            errors.append(
                checks.Error(
                    "Should have `IsInER` specified when `IsTechnician` is specified.",
                    hint="Add `IsInER` after `IsTechnician`.",
                    obj=api_view_class,
                    id="H005",
                )
            )
        if (
            SatisfiesClinicIPWhitelistingFromTechnician
            not in permissions_classes
        ):
            errors.append(
                checks.Error(
                    (
                        "Should have `SatisfiesClinicLocationIPWhitelistingFromTechnician` "
                        "specified when `IsTechnician` is specified."
                    ),
                    hint=(
                        "Add `SatisfiesClinicLocationIPWhitelistingFromTechnician` after "
                        "`IsTechnician` and `IsInER`.",
                    ),
                    obj=api_view_class,
                    id="H006",
                )
            )
        if (
            IsInER in permissions_classes
            and SatisfiesClinicIPWhitelistingFromTechnician
            in permissions_classes
        ):
            is_technician_index = permissions_classes.index(IsTechnician)
            in_er_index = permissions_classes.index(IsInER)
            department_index = permissions_classes.index(
                SatisfiesClinicIPWhitelistingFromTechnician
            )
            if not (is_technician_index < in_er_index < department_index):
                errors.append(
                    checks.Error(
                        (
                            "`IsTechnician`, `IsInER`, and `SatisfiesClinicLocationIPWhitelistingFromTechnician` "
                            "are not in the correct order."
                        ),
                        hint="Put them in the correct order.",
                        obj=api_view_class,
                        id="H007",
                    )
                )

    if IsPatient in permissions_classes:
        if (
            IsInER in permissions_classes
            and SatisfiesClinicIPWhitelistingFromPatient
            not in permissions_classes
            or IsInER not in permissions_classes
            and SatisfiesClinicIPWhitelistingFromPatient in permissions_classes
        ):
            errors.append(
                checks.Error(
                    (
                        "For `IsPatient`, `IsInER` and `SatisfiesClinicLocationIPWhitelistingFromPatient` "
                        "must either both be specified, or neither."
                    ),
                    hint="Correctly specify either both or neither.",
                    obj=api_view_class,
                    id="H008",
                )
            )
        if (
            IsInER in permissions_classes
            and SatisfiesClinicIPWhitelistingFromPatient in permissions_classes
        ):
            is_patient_index = permissions_classes.index(IsPatient)
            in_er_index = permissions_classes.index(IsInER)
            department_index = permissions_classes.index(
                SatisfiesClinicIPWhitelistingFromPatient
            )
            if not (is_patient_index < in_er_index < department_index):
                errors.append(
                    checks.Error(
                        (
                            "`IsPatient`, `IsInER`, and `SatisfiesClinicLocationIPWhitelistingFromPatient` "
                            "are not in the correct order."
                        ),
                        hint="Put them in the correct order.",
                        obj=api_view_class,
                        id="H009",
                    )
                )

    return errors


# NOTE: We specify `checks.Tags.urls` and `checks.Tags.security` because these checks
# could be argued to be related to both. We definitely want the URLs to be loaded and
# ready before this (so the `APIView` and `ViewSet`s are imported and ready
# everywhere). I think Django does that regardless before calling system checks, but
# tagging `checks.Tags.urls` here just to be safe.
@django.core.checks.register(checks.Tags.urls, checks.Tags.security)
def check_api_permissions_consistency(
    app_configs, **kwargs
) -> List[checks.CheckMessage]:
    def get_all_subclasses(cls: Type) -> Set[Type]:
        subclasses: Set[Type] = set(cls.__subclasses__())
        return subclasses.union(set(chain(*map(get_all_subclasses, subclasses))))

    messages: List[checks.CheckMessage] = []
    for api_view_class_or_subclass in {APIView}.union(get_all_subclasses(APIView)):
        messages.extend(
            check_api_view_permissions_consistency(api_view_class_or_subclass)
        )
    return messages
