from __future__ import annotations

import json
import logging
import sys
from io import StringIO
from typing import Any, ClassVar, Dict, List, Literal, Optional, Set, Tuple, Type, Union

from django.core.management import call_command
from django.db.models import Model
from django.utils.functional import cached_property

from jaspr.apps.common.decorators import classproperty

logger = logging.getLogger(__name__)


class Fixture:
    # NOTE: These two class variables are populated `__init_subclass__` below.
    _abstract: ClassVar[bool]
    _declared_fixtures: ClassVar[Dict[str, Type[Fixture]]] = {}

    # Django `dumpdata` command defaults
    # (https://docs.djangoproject.com/en/dev/ref/django-admin/#dumpdata)

    # https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-dumpdata-all
    all: bool = False
    # https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-dumpdata-format
    format: Literal["xml", "json", "jsonl", "yaml"] = "json"
    # https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-dumpdata-indent
    indent: Optional[int] = None
    # https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-dumpdata-exclude
    exclude: Set[str] = {}
    # https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-dumpdata-database
    database: str = "default"
    # https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-dumpdata-natural-foreign
    natural_foreign: bool = False
    # https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-dumpdata-natural-primary
    natural_primary: bool = False
    # https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-dumpdata-output
    output: Optional[str] = None

    tags: ClassVar[Set[str]] = {}

    def __init_subclass__(cls, abstract: bool = False):
        super().__init_subclass__()
        cls._abstract = abstract
        if not abstract:
            cls._declared_fixtures[cls.get_key()] = cls

    def prepare_dumpdata_kwargs(self) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {}

        kwargs.setdefault("all", self.all)
        kwargs.setdefault("format", self.format)
        kwargs.setdefault("indent", self.indent)
        kwargs.setdefault("exclude", self.exclude)
        kwargs.setdefault("database", self.database)
        kwargs.setdefault("natural_foreign", self.natural_foreign)
        kwargs.setdefault("natural_primary", self.natural_primary)
        kwargs.setdefault("output", self.output)

        return kwargs


class AppFixture(Fixture, abstract=True):
    app_label: ClassVar[str]

    @classmethod
    def get_key(cls) -> str:
        return cls.app_label

    def dumpdata(self, **other_options: Dict[str, Any]) -> str:  # TODO:
        kwargs = self.prepare_dumpdata_kwargs()
        return call_command("dumpdata", self.app_label, **{**kwargs, **other_options})

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(app_label={self.app_label})"


class ModelFixture(Fixture, abstract=True):
    # https://docs.djangoproject.com/en/dev/ref/django-admin/#cmdoption-dumpdata-pks
    pks: Optional[str] = None

    model: ClassVar[Type[Model]]

    @classproperty(lazy=True)
    def app_label(cls) -> str:
        return cls.model._meta.app_label

    @classproperty(lazy=True)
    def model_name(cls) -> str:
        return cls.model.__name__

    @classmethod
    def get_key(cls) -> str:
        return f"{cls.app_label}.{cls.model_name}"

    def prepare_dumpdata_kwargs(self) -> Dict[str, Any]:
        kwargs = super().prepare_dumpdata_kwargs()

        kwargs.setdefault("pks", self.pks)

        return kwargs

    def dumpdata(self, **other_options: Dict[str, Any]) -> str:  # TODO:
        app_label = self.app_label
        model_name = self.model_name
        kwargs = self.prepare_dumpdata_kwargs()
        return call_command(
            "dumpdata", f"{app_label}.{model_name}", **{**kwargs, **other_options}
        )

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(app_label={self.app_label}, model_name={self.model_name})"


class FixtureGroup:
    _declared_fixture_groups: ClassVar[Dict[str, Type[FixtureGroup]]] = {}

    def __init_subclass__(cls, abstract: bool = False):
        super().__init_subclass__()
        cls._abstract = abstract
        if not abstract:
            cls._declared_fixture_groups[cls.group_name] = cls

    @classproperty
    def all_group_names(cls) -> List[str]:
        return [*cls._declared_fixture_groups.keys()]

    @classmethod
    def from_name(cls, group_name: str) -> Type[FixtureGroup]:
        return cls._declared_fixture_groups[group_name]

    @staticmethod
    def filter_fixtures(fixtures: Dict[str, Fixture]) -> Dict[str, Fixture]:
        raise NotImplementedError("Subclasses must implement this method.")

    @cached_property
    def fixtures(self) -> Dict[str, Fixture]:
        return {
            key: fixture()
            for key, fixture in self.filter_fixtures(Fixture._declared_fixtures).items()
        }

    def dumpdata(self, **options: Dict[str, Any]) -> str:  # TODO
        count = len(self.fixtures)
        logger.info("%s about to dump %d fixtures", self.__class__.__name__, count)
        all_data: List[Dict[str, Any]] = []
        # Thanks to `django-fixture-magic` for the initial inspiration for
        # `unique_seen` here and the strategy for merging the different `json.dumps`
        # outputs (see
        # https://github.com/davedash/django-fixture-magic/blob/001194742b3165dc61541bc4532febaba9c1552d/fixture_magic/management/commands/merge_fixtures.py#L40)
        unique_seen: Set[Tuple[str, str]] = set()
        dumped_counts: Dict[str, int] = {}

        for number, (key, fixture) in enumerate(self.fixtures.items()):
            logger.info("%d/%d dumping %s", number + 1, count, key)
            string_io = StringIO()
            sys.stdout = string_io
            try:
                # NOTE/TODO: Do we want to pass these options?
                fixture.dumpdata(**{**options, "output": None})
            finally:
                sys.stdout = sys.__stdout__
            output = json.loads(string_io.getvalue())
            string_io.close()
            assert isinstance(output, list), "Should have a `list` at this point."
            not_seen, seen = 0, 0
            for value in output:
                # NOTE/TODO: Might need/want to have a way to handle when
                # `natural_primary=True` here.
                model, pk = value["model"], value["pk"]
                if (model, pk) in unique_seen:
                    seen += 1
                else:
                    all_data.append(value)
                    unique_seen.add((model, pk))
                    not_seen += 1
            logger.info(
                "%d/%d dumped %s (%d, %d)", number + 1, count, key, not_seen, seen
            )
            dumped_counts[key] = not_seen

        indent_option = options.get("indent")
        logger.info(
            "%s dumped %d fixtures: \n\n%s\n",
            self.__class__.__name__,
            count,
            json.dumps(dumped_counts, indent=indent_option or 2),
        )
        return json.dumps(
            all_data, indent=int(indent_option) if indent_option else None
        )
