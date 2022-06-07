from typing import FrozenSet, Set

from jaspr.apps.common.decorators import classproperty


class Tags:
    # NOTE: Root fixtures are ones that should always be dumped and loaded because
    # critical parts of the entire system may not function properly without them. I.E.
    # they should _always_ be there on a fresh loading of data, and the entire code
    # expects them.
    ROOT = "root"

    # NOTE: Current hypothesis is that most fixtures we'd load/dump can be separated
    # into data that is strictly content, and data that is related to a `User` in some
    # way, and data that is related to background tasks.
    CONTENT = "content"
    USER = "user"
    TASK = "task"

    # NOTE: These are environment-related tags.
    DEV = "dev"
    LOCAL = "local"
    PROD = "prod"

    # NOTE: These two tags are currently just for readability/documentation and to
    # remind developers looking at it what is `Jaspr` related and what isn't.
    DJANGO = "django"
    THIRD_PARTY = "third_party"

    @classproperty(lazy=True)
    def category_tags(cls) -> FrozenSet[str]:
        return frozenset([cls.CONTENT, cls.USER])

    @classproperty(lazy=True)
    def environment_tags(cls) -> FrozenSet[str]:
        return frozenset([cls.DEV, cls.LOCAL, cls.PROD])

    @classmethod
    def satisfies_environment(cls, environment_tag: str, tags: Set[str]) -> bool:
        """
        Check that for the given `environment_tag`, either it is in `tags` or the
        `tags` does not contain any other environments.
        """
        assert environment_tag in cls.environment_tags
        return environment_tag in tags or not (
            (cls.environment_tags - {environment_tag}) & tags
        )
