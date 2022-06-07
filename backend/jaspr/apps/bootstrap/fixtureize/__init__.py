# NOTE: It's important that `.fixtures` and `.fixture_groups` get imported so that
# `__init_subclass__` machinery runs and populates fixture and fixture group
# registries.
from .base import *  # noqa
from .fixture_groups import *  # noqa
from .fixtures import *  # noqa
from .tags import *  # noqa
