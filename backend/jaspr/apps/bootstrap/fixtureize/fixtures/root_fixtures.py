from django.contrib.auth.models import Group

from ..base import ModelFixture
from ..tags import Tags


class GroupFixture(ModelFixture):
    model = Group
    tags = {Tags.ROOT, Tags.USER, Tags.DJANGO}
