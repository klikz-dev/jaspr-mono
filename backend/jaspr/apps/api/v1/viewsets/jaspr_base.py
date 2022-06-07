from jaspr.apps.common.mixins import AssureNonFieldErrorsMixin
from jaspr.apps.kiosk.authentication import JasprTokenAuthentication, JasprTokenAuthenticationNoRenew


class JasprBaseViewSetMixin(AssureNonFieldErrorsMixin):
    authentication_classes = ()
    def get_authenticators(self):
        if self.request.headers.get("Heartbeat") == "ignore":
            return [JasprTokenAuthenticationNoRenew()]
        elif self.authentication_classes:
            return [auth() for auth in self.authentication_classes]
        return [JasprTokenAuthentication()]

