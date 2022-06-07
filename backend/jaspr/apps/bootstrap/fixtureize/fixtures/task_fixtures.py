from scheduler.models import CronJob, JobArg, JobKwarg, RepeatableJob

from ..base import ModelFixture
from ..tags import Tags


class CronJobFixture(ModelFixture):
    model = CronJob
    tags = {Tags.TASK}


class RepeatableJobFixture(ModelFixture):
    model = RepeatableJob
    tags = {Tags.TASK}


# TODO: `JobArg`s should only dump here ones that are pointing to `CronJob`s or
# `RepeatableJob`s, not `ScheduledJob`s. May involve adding a queryset and doing a
# natural serialization here. See EBPI-933.
class JobArgFixture(ModelFixture):
    model = JobArg
    tags = {Tags.TASK}

    # NOTE: Currently has a `GenericForeignKey` (involving `contenttypes.ContentType`),
    # so we definitely need this here.
    natural_foreign = True


# TODO: `JobKwarg`s should only dump here ones that are pointing to `CronJob`s or
# `RepeatableJob`s, not `ScheduledJob`s. May involve adding a queryset and doing a
# natural serialization here. See EBPI-933.
class JobKwargFixture(ModelFixture):
    model = JobKwarg
    tags = {Tags.TASK}

    # NOTE: Currently has a `GenericForeignKey` (involving `contenttypes.ContentType`),
    # so we definitely need this here.
    natural_foreign = True
