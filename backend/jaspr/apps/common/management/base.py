import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class JasprBaseCommand(BaseCommand):
    """
    The base management command for all management commands across Jaspr.

    Wraps the subclass `handle` method in a try/catch block, logging the exception if
    there is one uncaught.
    """

    def __init__(self, *args, **kwargs):
        """
        Override execute, and while executing have `handle` point
        to our wrapped handle so that we can catch exceptions there.
        """
        super().__init__(*args, **kwargs)
        # Set up the proxying of the subclass `handle`.
        self.proxied_handle = self.handle
        self.handle = self.wrapped_handle

    def wrapped_handle(self, *args, **kwargs):
        """
        Assumes `self.proxied_handle` will be set prior to calling this to point to
        the actual `self.handle` that was defined by the subclass.
        """
        try:
            return self.proxied_handle(*args, **kwargs)
        except Exception as e:
            logger.exception(
                "Caught exception in management command!\n"
                "Class: %s\n"
                "Exception: %s",
                self.__class__,
                e,
            )
            raise
