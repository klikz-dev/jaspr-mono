from pathlib import Path
from typing import ClassVar, Dict, Type

from django.core.management import call_command
from django.core.management.base import CommandParser
from django.core.management.commands import dumpdata
from jaspr.apps.bootstrap.fixtureize.base import FixtureGroup
from jaspr.apps.common.management.base import JasprBaseCommand


class Command(JasprBaseCommand):
    """
    Dump fixtures as defined and specified in `jaspr/apps/bootstrap/fixtures.py`.
    """

    help = __doc__

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "group",
            type=str,
            choices=FixtureGroup.all_group_names,
            help="The fixture group to dump the data from.",
        )
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            help=(
                "Specify the output. If not provided, will default to "
                "jaspr/apps/bootstrap/fixtures/jaspr_{fixture_group_name}.json"
            ),
        )
        parser.add_argument(
            "--indent",
            type=int,
            help="Specifies the indent level to use when pretty-printing output.",
        )

    def handle(self, *args, **options) -> str:  # TODO
        group_key = options.pop("group")
        output_file = options.pop("output")
        if output_file is None:
            output_file = str(
                Path("jaspr/apps/bootstrap/fixtures/") / f"jaspr_{group_key}.json"
            )
        fixture_group = FixtureGroup.from_name(group_key)()
        json_string = fixture_group.dumpdata(**options)
        with open(output_file, "w", newline="\n") as f:
            f.write(json_string)
        # return json_string
