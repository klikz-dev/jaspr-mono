"""
Custom Django checks. Thanks to https://hakibenita.com/automating-the-boring-stuff-in-django-using-the-check-framework

    H001: `CheckConstraint` should use `jaspr.apps.common.constraints.EnhancedCheckConstraint` instead.
    H002: `UniqueConstraint` should use `jaspr.apps.common.constraints.EnhancedUniqueConstraint` instead.
    H003: Found constraint besides `CheckConstraint` and `UniqueConstraint`.
"""
from typing import Generator, List, Type

import django.apps
from django.core import checks
from django.db import models

from .constraints import _CONSTRAINT_DESCRIPTION_REGISTRY


def check_model_constraints(
    model: Type[models.Model],
) -> Generator[checks.Error, None, None]:
    """
    Check a single model's constraints and yield instances of `checks.Error` for each
    constraint's name that's not found in the registry.
    """
    for constraint in model._meta.constraints:
        if constraint.name not in _CONSTRAINT_DESCRIPTION_REGISTRY:
            if isinstance(constraint, models.CheckConstraint):
                yield checks.Error(
                    "CheckConstraint` should use `jaspr.apps.common.constraints.EnhancedCheckConstraint` instead",
                    hint="Use `EnhancedCheckConstraint`",
                    obj=model,
                    id="H001",
                )
            elif isinstance(constraint, models.UniqueConstraint):
                yield checks.Error(
                    "`UniqueConstraint` should use `jaspr.apps.common.constraints.EnhancedUniqueConstraint` instead.",
                    hint="Use `EnhancedUniqueConstraint`",
                    obj=model,
                    id="H002",
                )
            else:
                yield checks.Error(
                    "Found constraint besides `CheckConstraint` and `UniqueConstraint`.",
                    hint=(
                        "Probably should update this system check code to handle this "
                        "constraint (`jaspr.apps.common.checks`). Additionally, may "
                        "want/need to update the code at `jaspr.apps.common.constraints`."
                    ),
                    obj=model,
                    id="H003",
                )


@django.core.checks.register(checks.Tags.models)
def check_models(app_configs, **kwargs) -> List[checks.CheckMessage]:
    messages: List[checks.CheckMessage] = []
    for app in django.apps.apps.get_app_configs():
        # Skip third party apps (thanks to the article linked at the top for this one).
        # NOTE: This is potentially partially hacky. If we come up with, in the future,
        # a better/more robust way to determine if an app is local or a third-party
        # package it might be nice to replace this with that (whether we came up with
        # that working on this or something else).
        if app.path.find("site-packages") > -1:
            continue
        for model in app.get_models():
            for check_message in check_model_constraints(model):
                messages.append(check_message)
    return messages
