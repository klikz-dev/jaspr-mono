from django.apps import AppConfig


class CommonConfig(AppConfig):
    name = "jaspr.apps.common"
    verbose_name = "Common"

    def ready(self):
        # Import the system checks that should run.
        import jaspr.apps.common.checks  # noqa
