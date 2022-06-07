from taggit.models import Tag

from jaspr.apps.awsmedia.models import Media, PrivacyScreenImage
from jaspr.apps.jah.models import CommonConcern, ConversationStarter
from jaspr.apps.kiosk.models import (
    Activity,
    CopingStrategy,
    CopingStrategyCategory,
    GuideMessage,
    Helpline,
    NoteTemplate,
    Person,
    SharedStory,
    Topic,
)

from jaspr.apps.stability_plan.models import Step, Walkthrough, WalkthroughStep

from ..base import ModelFixture
from ..tags import Tags


class MediaFixture(ModelFixture):
    model = Media
    tags = {Tags.CONTENT}

    # NOTE: Currently has a `ForeignKey` to `taggit.Tag`.
    natural_foreign = True


class PrivacyScreenImageFixture(ModelFixture):
    model = PrivacyScreenImage
    tags = {Tags.CONTENT}


class ActivityFixture(ModelFixture):
    model = Activity
    tags = {Tags.CONTENT}


class CopingStrategyFixture(ModelFixture):
    model = CopingStrategy
    tags = {Tags.CONTENT}


class CopingStrategyCategoryFixture(ModelFixture):
    model = CopingStrategyCategory
    tags = {Tags.CONTENT}


class GuideMessageFixture(ModelFixture):
    model = GuideMessage
    tags = {Tags.CONTENT}


class HelplineFixture(ModelFixture):
    model = Helpline
    tags = {Tags.CONTENT}


class NoteTemplateFixture(ModelFixture):
    model = NoteTemplate
    tags = {Tags.CONTENT}


class PersonFixture(ModelFixture):
    model = Person
    tags = {Tags.CONTENT}


class SharedStoryFixture(ModelFixture):
    model = SharedStory
    tags = {Tags.CONTENT}


class TopicFixture(ModelFixture):
    model = Topic
    tags = {Tags.CONTENT}


class CommonConcernFixture(ModelFixture):
    model = CommonConcern
    tags = {Tags.CONTENT}


class ConversationStarterFixture(ModelFixture):
    model = ConversationStarter
    tags = {Tags.CONTENT}


class WalkthroughFixture(ModelFixture):
    model = Walkthrough
    tags = {Tags.CONTENT}


class WalkthroughStepFixture(ModelFixture):
    model = WalkthroughStep
    tags = {Tags.CONTENT}


class StepFixture(ModelFixture):
    model = Step
    tags = {Tags.CONTENT}

    # NOTE: Currently has a `GenericForeignKey` (involving `contenttypes.ContentType`),
    # so we definitely need this here.
    natural_foreign = True


class TagFixture(ModelFixture):
    model = Tag
    tags = {Tags.CONTENT, Tags.THIRD_PARTY}


