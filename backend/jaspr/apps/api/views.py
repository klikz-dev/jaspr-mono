import logging

from jaspr.apps.common.health_checks import HealthCheckType, internal_health_check
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.request import Request
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def health_check(request: Request) -> Response:
    could_not_reach: HealthCheckType = internal_health_check()
    if could_not_reach:
        message = f"Could not connect to {' + '.join(could_not_reach)}."
        return Response(
            {"success": False, "message": message},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response({"success": True, "message": "Ok."}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def catch_roadrunner(request: Request) -> Response:
    from sentry_sdk import add_breadcrumb

    logger.info("About to catch roadrunner...")
    add_breadcrumb(
        category="scheme", message="Laying the trail of crumbs...", level="info"
    )
    return Response({"caught": True, "sound": "beep beep", "extra": 1 / 0})  # noqa
