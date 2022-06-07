from django.apps import AppConfig


class APIConfig(AppConfig):
    name = "jaspr.apps.api"
    verbose_name = "API"

    def ready(self):
        # Import the system checks that should run.
        import jaspr.apps.api.checks  # noqa
