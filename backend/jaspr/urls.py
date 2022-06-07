"""Jaspr base urls"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django_otp.admin import OTPAdminSite

otp_admin_site = OTPAdminSite(OTPAdminSite.name)
for model_cls, model_admin in admin.site._registry.items():
    otp_admin_site.register(model_cls, model_admin.__class__)

urlpatterns = [
    re_path(r"session_security/", include("session_security.urls")),
    re_path(r"^ebpiadmin/", otp_admin_site.urls),
    re_path(r"^django-rq/", include("django_rq.urls")),
    re_path(r"", include("jaspr.apps.api.urls")),
]

otp_admin_site.site_header = "Jaspr Administration"

if settings.SHOW_DEVADMIN:
    urlpatterns += [
        re_path("^devadmin/", admin.site.urls),
    ]

if settings.DEBUG:
    from django.views.static import serve  # noqa

    urlpatterns += [
        re_path(r"", include("django.contrib.staticfiles.urls")),
        re_path(
            r"^media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
        ),
    ]

    # Django Debug Toolbar (https://github.com/jazzband/django-debug-toolbar)
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar  # noqa

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

    # Django Silk (Profiling) (https://github.com/jazzband/django-silk)
    if "silk" in settings.INSTALLED_APPS:
        urlpatterns = [
            path("silk/", include("silk.urls", namespace="silk"))
        ] + urlpatterns
