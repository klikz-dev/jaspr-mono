import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from ..permissions import (
    IsAuthenticated,
    IsInER,
    IsTechnician,
    SatisfiesClinicIPWhitelistingFromTechnician,
)
from .base import JasprBaseView

logger = logging.getLogger(__name__)


class TechnicianHeartbeatView(JasprBaseView):
    """
    NOTE: At the time of writing, this is an interesting `View`, in that a few things
    are going on here.

    1. The `IsTechnician` permission doesn't actually do anything right now (other
    than deciding if a `403` or `204` response is returned). It's there because, in
    the future, we want to keep this endpoint available and reserved for being a
    heartbeat-esque endpoint for `Technician`s specifically. The current
    implementation may not need/use it, but we still want to keep it specific to the
    `Technician` so to speak.
    2. Related to the above ^, the reason `IsTechnician` doesn't do anything is
    because `IsAuthenticated`, at the time of writing, has all of the logic within
    itself to extend the underlying `JasprSession`'s `AuthToken`'s `expiry` field.
    Our custom `JasprTokenAuthentication` has its own custom refresh logic that has
    both how far to extend it (when doing so), and also how often to allow extending
    (I.E. can only extend, at the time of writing, at most once every X seconds
    depending on parameters on the `JasprSession`).

    NOTE/Maybe TODO: All that being said (above), at the time of writing, I think
    that keeping it this way for now keeps things clean, and allows a custom/special
    sort of heartbeat functionality in the future if needed. If we wanted to actually
    _only enable expiry for `Technician`s_, then we might want to do something with
    `authentication_classes` set to a subclassed `JasprTokenAuthentication` that
    restricts the actual logic functionality to `"Technician"`-only `JasprSession`s
    (which should be pretty straightforward I'd think).
    """

    permission_classes = (
        IsAuthenticated,
        IsTechnician,
        IsInER,
        SatisfiesClinicIPWhitelistingFromTechnician,
    )

    def post(self, request: Request) -> Response:
        # The `JasprTokenAuthentication` `authentication_class` (in
        # `authentication_classes` in `JasprBaseView`) has all the logic in it, at the
        # time of writing, to update the `AuthToken`'s `expiry` depending on the
        # `user_type`. Realistically, we don't need `IsTechnician` even present at the
        # time of writing on the permissions, since this is basically a noop/do nothing
        # endpoint that simply relies upon the (mostly stock) auto-refreshing
        # functionality from our knox `AuthToken`s. See the above docstring for this
        # view for more details.
        return Response(status=status.HTTP_204_NO_CONTENT)
