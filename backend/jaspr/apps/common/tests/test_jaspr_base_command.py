import logging

from django.core.management import call_command
from django.test import SimpleTestCase
from jaspr.apps.common.management.base import JasprBaseCommand, logger


class CustomTestException(Exception):
    pass


class CommandToTest(JasprBaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--throw_test_exception",
            default=False,
            action="store_true",
            help="Throw an exception with this command.",
        )

    def handle(self, *app_labels, **options):
        if options["throw_test_exception"]:
            raise CustomTestException("BOOM!!!")
        return ""


class TestEBPIBaseCommand(SimpleTestCase):
    def setUp(self):
        self.command_instance = CommandToTest()

    def test_with_exception(self):
        """Is a thrown exception properly caught?"""
        with self.assertRaises(CustomTestException) as e, self.assertLogs(
            logger, logging.ERROR
        ) as l:
            result = call_command(self.command_instance, throw_test_exception=True)
        self.assertIn("Caught exception in management command!", l.output[0])
        self.assertIn("Class: ", l.output[0])
        self.assertIn(
            "jaspr.apps.common.tests.test_jaspr_base_command.CommandToTest", l.output[0]
        )
        self.assertIn("BOOM!!!", l.output[0])
        self.assertEqual(e.exception.__class__, CustomTestException)
        self.assertEqual(e.exception.args[0], "BOOM!!!")

    def test_without_exception(self):
        """If there isn't an exception thrown, does the command proceed normally?"""
        result = call_command(self.command_instance, throw_test_exception=False)
        self.assertEqual(result, "")
