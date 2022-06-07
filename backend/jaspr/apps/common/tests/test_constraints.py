import logging
from typing import Generator, Type, Union

from django.db import IntegrityError, OperationalError
from django.db.models import CheckConstraint, Q, UniqueConstraint
from jaspr.apps.common.constraints import (
    _CONSTRAINT_DESCRIPTION_REGISTRY,
    EnhancedCheckConstraint,
    EnhancedCheckConstraintSpec,
    EnhancedUniqueConstraint,
    EnhancedUniqueConstraintSpec,
    check_exception_for_constraint,
    drf_validation_error_from_constraint_spec,
)
from jaspr.apps.common.constraints import logger as constraints_logger
from jaspr.apps.common.functions import custom_drf_exception_handler
from jaspr.apps.test_infrastructure.testcases import (
    JasprApiTestCase,
    JasprSimpleTestCase,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError as DRFValidationError


class TestConstraints(JasprSimpleTestCase):
    enhanced_constraint_classes = (EnhancedCheckConstraint, EnhancedUniqueConstraint)

    def example_constraint_of_each_class(
        self, *names: str,
    ) -> Generator[
        Union[
            Type[CheckConstraint],
            CheckConstraint,
            Type[UniqueConstraint],
            UniqueConstraint,
        ],
        None,
        None,
    ]:
        yield EnhancedCheckConstraint
        yield EnhancedCheckConstraint(
            check=Q(some_field="some_value"),
            name=names[0],
            description="Some check constraint helpful description",
        )
        yield EnhancedUniqueConstraint
        yield EnhancedUniqueConstraint(
            fields=["field1", "field2", "field3"],
            name=names[1],
            description="Some unique constraint helpful description",
        )

    def tearDown(self):
        super().tearDown()

        _CONSTRAINT_DESCRIPTION_REGISTRY.pop("some_constraint_name", None)
        _CONSTRAINT_DESCRIPTION_REGISTRY.pop("some_check_constraint_name", None)
        _CONSTRAINT_DESCRIPTION_REGISTRY.pop("some_unique_constraint_name", None)

    def test_enhanced_check_constraint_registered_and_error_messages(self):
        self.assertNotIn("some_check_constraint_name", _CONSTRAINT_DESCRIPTION_REGISTRY)
        constraint = EnhancedCheckConstraint(
            check=Q(some_field="some_value"),
            name="some_check_constraint_name",
            description="Some check constraint helpful description",
        )
        self.assertIsInstance(constraint, CheckConstraint)
        self.assertIn("some_check_constraint_name", _CONSTRAINT_DESCRIPTION_REGISTRY)
        spec = EnhancedCheckConstraintSpec(
            constraint=constraint,
            description="Some check constraint helpful description",
        )
        self.assertEqual(
            _CONSTRAINT_DESCRIPTION_REGISTRY["some_check_constraint_name"], spec
        )

        some_exception = Exception("Some exception")
        self.assertEqual(
            spec.error_message_generic(some_exception),
            "Something unexpected happened. Feel free to try again, and if the problem "
            "persists, contact support.",
        )
        self.assertEqual(
            spec.error_message_detailed(some_exception),
            (
                "CheckConstraint\nSome check constraint helpful description\n\n"
                f"(Check failed: {Q(some_field='some_value')})"
            ),
        )

    def test_enhanced_unique_constraint_registered_and_error_messages_no_condition(
        self,
    ):
        self.assertNotIn(
            "some_unique_constraint_name", _CONSTRAINT_DESCRIPTION_REGISTRY
        )
        constraint = EnhancedUniqueConstraint(
            fields=["field1", "field2", "field3"],
            name="some_unique_constraint_name",
            description="Some unique constraint helpful description",
        )
        self.assertIsInstance(constraint, UniqueConstraint)
        self.assertIn("some_unique_constraint_name", _CONSTRAINT_DESCRIPTION_REGISTRY)
        spec = EnhancedUniqueConstraintSpec(
            constraint=constraint,
            description="Some unique constraint helpful description",
        )
        self.assertEqual(
            _CONSTRAINT_DESCRIPTION_REGISTRY["some_unique_constraint_name"], spec
        )

        some_exception = Exception("Some exception")
        self.assertEqual(
            spec.error_message_generic(some_exception),
            "Something unexpected happened. Feel free to try again, and if the problem "
            "persists, contact support.",
        )
        self.assertEqual(
            spec.error_message_detailed(some_exception),
            (
                "UniqueConstraint\nSome unique constraint helpful description\n\n"
                f"(Fields: {constraint.fields})"
            ),
        )

    def test_enhanced_unique_constraint_registered_and_error_messages_with_condition(
        self,
    ):
        self.assertNotIn(
            "some_unique_constraint_name", _CONSTRAINT_DESCRIPTION_REGISTRY
        )
        constraint = EnhancedUniqueConstraint(
            fields=["field1", "field2", "field3"],
            name="some_unique_constraint_name",
            condition=Q(field1__startswith="light", field2__in=["value1", "value2"]),
            description="Some unique constraint helpful description",
        )
        self.assertIsInstance(constraint, UniqueConstraint)
        self.assertIn("some_unique_constraint_name", _CONSTRAINT_DESCRIPTION_REGISTRY)
        spec = EnhancedUniqueConstraintSpec(
            constraint=constraint,
            description="Some unique constraint helpful description",
        )
        self.assertEqual(
            _CONSTRAINT_DESCRIPTION_REGISTRY["some_unique_constraint_name"], spec
        )

        some_exception = Exception("Some exception")
        self.assertEqual(
            spec.error_message_generic(some_exception),
            "Something unexpected happened. Feel free to try again, and if the problem "
            "persists, contact support.",
        )
        self.assertEqual(
            spec.error_message_detailed(some_exception),
            (
                "UniqueConstraint\nSome unique constraint helpful description\n\n"
                f"(Fields: {constraint.fields})\n\n"
                f"(Condition: {Q(field1__startswith='light', field2__in=['value1', 'value2'])})"
            ),
        )

    def test_duplicate_constraint_names_cannot_be_registered(self):
        constraint = EnhancedCheckConstraint(
            check=Q(some_field="some_value"),
            name="some_constraint_name",
            description="Some helpful description",
        )

        generator = self.example_constraint_of_each_class(
            "some_constraint_name", "some_constraint_name"
        )
        while True:
            try:
                class_to_test = next(generator)
            except StopIteration:
                break

            with self.subTest(class_to_test=class_to_test):
                with self.assertRaises(AssertionError) as cm:
                    next(generator)
                self.assertEqual(
                    str(cm.exception),
                    "Constraint with `name=some_constraint_name` already present.",
                )

    def test_check_exception_for_constraint_not_integrity_error(self):
        constraint = EnhancedCheckConstraint(
            check=Q(some_field="some_value"),
            name="some_constraint_name",
            description="Some helpful description",
        )

        other_error = OperationalError(
            'Some text before... constraint "some_constraint_name" some text after.'
        )

        result = check_exception_for_constraint(other_error)
        self.assertIsNone(result)

    def test_check_exception_for_constraint_integrity_error_no_match(self):
        constraint = EnhancedCheckConstraint(
            check=Q(some_field="some_value"),
            name="some_constraint_name",
            description="Some helpful description",
        )

        integrity_error = IntegrityError(
            "Some integrity error without a constraint match (missing quotes after "
            "'constraint' so this won't match)"
        )

        result = check_exception_for_constraint(integrity_error)
        self.assertIsNone(result)

    def test_check_exception_for_constraint_integrity_error_match_in_registry(self):
        constraint = EnhancedCheckConstraint(
            check=Q(some_field="some_value"),
            name="some_constraint_name",
            description="Some helpful description",
        )

        integrity_error = IntegrityError(
            'Some text before... constraint "some_constraint_name" some text after.'
        )

        result = check_exception_for_constraint(integrity_error)
        self.assertIs(result, _CONSTRAINT_DESCRIPTION_REGISTRY["some_constraint_name"])

    def test_check_exception_for_constraint_warning_logged_if_constraint_not_in_registry(
        self,
    ):
        integrity_error = IntegrityError(
            'Some text before... constraint "some_not_registered_constraint" some text after.'
        )

        with self.assertLogs(constraints_logger, logging.WARNING) as l:
            result = check_exception_for_constraint(integrity_error)
        self.assertIsNone(result)
        self.assertIn(
            (
                f'Saw constraint name "some_not_registered_constraint" in '
                f"{str(integrity_error)} but it wasn't found in the registry."
            ),
            l.output[0],
        )

    def test_drf_validation_error_from_constraint_when_should_be_generic(self):
        constraint = EnhancedCheckConstraint(
            check=Q(some_field="some_value"),
            name="some_constraint_name",
            description="Some check constraint helpful description",
        )
        integrity_error = IntegrityError(
            'Some text before... constraint "some_constraint_name" some text after.'
        )
        spec = _CONSTRAINT_DESCRIPTION_REGISTRY["some_constraint_name"]
        # First, test `drf_validation_error_from_constraint_spec` directly.
        result = drf_validation_error_from_constraint_spec(spec, integrity_error, False)

        self.assertIsInstance(result, DRFValidationError)
        self.assertEqual(
            str(result.detail[0]),
            "Something unexpected happened. Feel free to try again, and if the problem "
            "persists, contact support.",
        )
        self.assertEqual(result.detail[0].code, "constraint")
        self.assertIs(result.__cause__, integrity_error)

        # Next, test the default DRF exception handler we use and make sure we got the expected response.
        with self.settings(DEBUG=False):
            response = custom_drf_exception_handler(integrity_error, {})

        self.assertEqual(response.data, result.detail)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_drf_validation_error_from_constraint_when_should_be_detailed(self):
        constraint = EnhancedCheckConstraint(
            check=Q(some_field="some_value"),
            name="some_constraint_name",
            description="Some check constraint helpful description",
        )
        integrity_error = IntegrityError(
            'Some text before... constraint "some_constraint_name" some text after.'
        )
        spec = _CONSTRAINT_DESCRIPTION_REGISTRY["some_constraint_name"]
        # First, test `drf_validation_error_from_constraint_spec` directly.
        result = drf_validation_error_from_constraint_spec(spec, integrity_error, True)

        self.assertIsInstance(result, DRFValidationError)
        self.assertEqual(
            str(result.detail[0]),
            (
                "CheckConstraint\nSome check constraint helpful description\n\n"
                f"(Check failed: {Q(some_field='some_value')})"
            ),
        )
        self.assertEqual(result.detail[0].code, "constraint")
        self.assertIs(result.__cause__, integrity_error)

        # Next, test the default DRF exception handler we use and make sure we got the
        # expected response.
        with self.settings(DEBUG=True):
            response = custom_drf_exception_handler(integrity_error, {})

        self.assertEqual(response.data, result.detail)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestConstraintsIntegrationInARequest(JasprApiTestCase):
    """
    The purpose of this test class is to pick an existing API endpoint that could
    potentially, as a part of the flow, have an error occur because of a constraint,
    and check that the response is handled correctly.

    There are two potential reasons, in my mind, at least now, as to when/why this
    test could be changed or removed in the future:
    1. We have a lot of constraints and have a number of tests in the regular API testing
    files that check for constraint errors.
    2. We change all endpoints that could trigger constraints to do things like `get_or_create`, etc.
    and effectively make constraint errors as things that should _almost never happen_. It would
    still be nice to be able to trigger one of those cases and be able to test the API response flow.

    One potential suggestion if one of the above two cases happens would be to wire
    up a test-only view and/or endpoint that would violate a constraint and make sure
    everything works properly with respect to the exception handling. This is nice
    potentially too to have in case Django's actual `IntegrityError` and/or
    `psycopg2`'s errors change their wording to where we have to update our regex
    that finds the constraint name.
    """

    def setUp(self):
        super().setUp()

        # NOTE: This is currently, at the time of writing, a URL where we could see a
        # db constraint get triggered. See class docstring, if that endpoint changes
        # ever these tests may need to change.
        self.uri = "/v1/patient/patient-activities"
        self.patient = self.create_patient()
        self.department = self.create_department()
        self.encounter = self.create_patient_encounter(patient=self.patient, department=self.department)
        self.set_patient_creds(self.patient)
        self.activity = self.create_activity()

    def make_request(self) -> Response:
        return self.client.post(
            self.uri,
            data={
                "activity": self.activity.id,
                "rating": 4,
                "save_for_later": False,
                "viewed": None,
            },
        )

    def test_constraint_response_generic_error_message(self):
        first_response = self.make_request()

        # First response should be good, we hadn't had a `PatientActivity` yet.
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

        with self.settings(DEBUG=False):
            second_response = self.make_request()

        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(second_response.data["non_field_errors"][0]),
            "Something unexpected happened. Feel free to try again, and if the problem "
            "persists, contact support.",
        )

    def test_constraint_response_detailed_error_message(self):
        first_response = self.make_request()

        # First response should be good, we hadn't had a `PatientActivity` yet.
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)

        with self.settings(DEBUG=True):
            second_response = self.make_request()

        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(second_response.data["non_field_errors"][0]),
            _CONSTRAINT_DESCRIPTION_REGISTRY[
                "unique_active_patient_activity"
            ].error_message_detailed(
                Exception(
                    "The `exception` argument isn't used right now so this should "
                    "still pass. If it ever fails, will probably need to update this "
                    "test."
                )
            ),
        )
