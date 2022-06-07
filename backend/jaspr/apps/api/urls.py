from django.conf import settings
from django.urls import include, re_path

from .views import catch_roadrunner, health_check

app_name = "api"
urlpatterns = [
    re_path(r"v1/", include("jaspr.apps.api.v1.urls")),
    re_path("health-check", health_check),
]
if settings.USE_SENTRY and settings.ALLOW_SENTRY_TEST:
    urlpatterns += [re_path("wile-e-coyote", catch_roadrunner)]
