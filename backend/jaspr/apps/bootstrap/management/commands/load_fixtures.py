from pathlib import Path

from django.core.management import call_command
from django.core.management.base import CommandParser
from django.core.management.commands import loaddata
from jaspr.apps.bootstrap.fixtureize.base import FixtureGroup
from jaspr.apps.common.management.base import JasprBaseCommand


class Command(JasprBaseCommand):
    """
    Load the fixtures generated from calling `dump_fixtures` with the given
    group.
    """

    help = __doc__

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "group",
            type=str,
            nargs="?",
            default=None,
            choices=FixtureGroup.all_group_names,
            help=(
                "The fixture group to load the data from. If --input (-i) is "
                "specified this is not required."
            ),
        )
        parser.add_argument(
            "-i",
            "--input",
            type=str,
            help=(
                "Specify the input. If not provided, will default to "
                "jaspr/apps/bootstrap/fixtures/jaspr_{fixture_group_name}.json. "
                "Note `loaddata` caveats, can't be an arbitrary path but must be one "
                "currently that the Django fixture mechanisms can find."
            ),
        )

    def handle(self, *args, **options) -> str:  # TODO
        group_key = options.pop("group")
        loaddata_file = options.pop("input")
        assert (
            group_key is not None or loaddata_file is not None
        ), "Must specify at least one of --group or --input."
        if loaddata_file is None:
            loaddata_file = str(
                Path("jaspr/apps/bootstrap/fixtures/") / f"jaspr_{group_key}.json"
            )
        return call_command("loaddata", loaddata_file)
