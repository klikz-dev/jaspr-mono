from typing import Dict

from .base import Fixture, FixtureGroup
from .tags import Tags


class RootFixtures(FixtureGroup):
    group_name = "root"

    @staticmethod
    def filter_fixtures(fixtures: Dict[str, Fixture]) -> Dict[str, Fixture]:
        return {k: v for k, v in fixtures.items() if v.tags & {Tags.ROOT}}


class MediaFixtures(FixtureGroup):
    group_name = "media"

    @staticmethod
    def filter_fixtures(fixtures: Dict[str, Fixture]) -> Dict[str, Fixture]:
        return {
            k: v
            for k, v in fixtures.items()
            # Grab the fixtures tagged with "media" that are not tagged for specific
            # environments.
            if v.tags & {Tags.ROOT, Tags.CONTENT}
            and not (v.tags & Tags.environment_tags)
        }


class ContentFixtures(FixtureGroup):
    group_name = "content"

    @staticmethod
    def filter_fixtures(fixtures: Dict[str, Fixture]) -> Dict[str, Fixture]:
        print("Content fixtures")
        print(fixtures)
        result = {
            k: v
            for k, v in fixtures.items()
            # Grab the fixtures tagged with "content" that are not tagged for specific
            # environments.
            if Tags.CONTENT in v.tags
            # & {Tags.ROOT, Tags.CONTENT} and not (v.tags & Tags.environment_tags)
        }
        print("-----")
        print(result)
        return result


class TaskFixtures(FixtureGroup):
    group_name = "task"

    @staticmethod
    def filter_fixtures(fixtures: Dict[str, Fixture]) -> Dict[str, Fixture]:
        return {
            k: v
            for k, v in fixtures.items()
            # Grab the fixtures tagged with "task" that are not tagged for specific
            # environments.
            if v.tags & {Tags.ROOT, Tags.TASK} and not (v.tags & Tags.environment_tags)
        }


class UserFixtures(FixtureGroup):
    group_name = "user"

    @staticmethod
    def filter_fixtures(fixtures: Dict[str, Fixture]) -> Dict[str, Fixture]:
        return {
            k: v
            for k, v in fixtures.items()
            # Grab the fixtures tagged with "user" that are not tagged for specific
            # environments.
            if v.tags & {Tags.ROOT, Tags.USER} and not (v.tags & Tags.environment_tags)
        }


class DevOnlyFixtures(FixtureGroup):
    group_name = "dev_only"

    @staticmethod
    def filter_fixtures(fixtures: Dict[str, Fixture]) -> Dict[str, Fixture]:
        return {k: v for k, v in fixtures.items() if v.tags & {Tags.ROOT, Tags.DEV}}

class SSIFixtures(FixtureGroup):
    group_name = "ssi"

    @staticmethod
    def filter_fixtures(fixtures: Dict[str, Fixture]) -> Dict[str, Fixture]:
        return {k: v for k, v in fixtures.items() if v.tags & {Tags.SSI}}


class DevWithoutAllUsersFixtures(FixtureGroup):
    group_name = "dev_without_all_users"

    @staticmethod
    def filter_fixtures(fixtures: Dict[str, Fixture]) -> Dict[str, Fixture]:
        return {
            k: v
            for k, v in fixtures.items()
            if v.tags & {Tags.ROOT, Tags.CONTENT, Tags.TASK, Tags.DEV}
            and Tags.satisfies_environment(Tags.DEV, v.tags)
        }


class DevWithAllUsersFixtures(FixtureGroup):
    group_name = "dev_with_all_users"

    @staticmethod
    def filter_fixtures(fixtures: Dict[str, Fixture]) -> Dict[str, Fixture]:
        return {
            k: v
            for k, v in fixtures.items()
            if v.tags & {Tags.ROOT, Tags.CONTENT, Tags.TASK, Tags.USER, Tags.DEV}
            and Tags.satisfies_environment(Tags.DEV, v.tags)
        }


class ProdFixtures(FixtureGroup):
    group_name = "prod"

    @staticmethod
    def filter_fixtures(fixtures: Dict[str, Fixture]) -> Dict[str, Fixture]:
        return {
            k: v
            for k, v in fixtures.items()
            # NOTE: Can put in `Tags.USER` once PII/fernet fields support is
            # implemented. May want to revisit exactly what "prod" means too then. Are
            # we dumping to prod or from prod? Could put those as different groups.
            if v.tags & {Tags.ROOT, Tags.CONTENT, Tags.TASK, Tags.PROD}
            and Tags.satisfies_environment(Tags.PROD, v.tags)
        }
