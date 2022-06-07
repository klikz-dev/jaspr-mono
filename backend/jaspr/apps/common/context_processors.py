from django.conf import settings


def environment(request):
    return {
        "ENVIRONMENT": settings.ENVIRONMENT,
        "IS_RELEASE": settings.ENVIRONMENT == "development" and settings.GIT_BRANCH == "release"
    }