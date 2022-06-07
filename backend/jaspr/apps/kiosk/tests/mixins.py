from jaspr.apps.common.tests.mixins import UidAndTokenTestMixin
from jaspr.apps.kiosk.authentication import JasprToolsToGoUidAndTokenAuthentication


class JasprToolsToGoUidAndTokenTestMixin(UidAndTokenTestMixin):
    token_generator = JasprToolsToGoUidAndTokenAuthentication.token_generator
