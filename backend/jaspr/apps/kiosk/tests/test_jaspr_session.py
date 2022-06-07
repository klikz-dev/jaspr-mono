import logging
from contextlib import ExitStack
from datetime import timedelta
from types import MethodType
from unittest.mock import patch

from django.db import connection, transaction
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from freezegun import freeze_time
from jaspr.apps.kiosk.apps import (
    _auth_token_original_get_queryset_,
    _get_queryset_with_jaspr_session_,
)
from jaspr.apps.kiosk.authentication import JasprTokenAuthentication
from jaspr.apps.kiosk.models import (
    JasprSession,
    JasprSessionError,
    JasprSessionUserFacingError,
)
from jaspr.apps.kiosk.models import logger as jaspr_models_logger
from jaspr.apps.test_infrastructure.testcases import (
    JasprTestCase,
    JasprTransactionTestCase,
)
from knox.models import AuthToken, AuthTokenManager

from .helpers import JasprSessionParametrizationTestMixin, Parametrizer


class TestJasprSession(JasprSessionParametrizationTestMixin, JasprTestCase):
    def assert_exceptions_match_and_log_critical_if_internal(
        self,
        e1: JasprSessionError,
        e2: JasprSessionError,
        logging_watcher=None,
    ):
        self.assertEqual(type(e1), type(e2), "Should be same exception type.")
        self.assertEqual(e1.user, e2.user)
        self.assertEqual(e1.user_type, e2.user_type)
        self.assertEqual(e1.in_er, e2.in_er)
        self.assertEqual(e1.from_native, e2.from_native)
        self.assertEqual(e1.long_lived, e2.long_lived)
        self.assertEqual(e1.internal, e2.internal)
        self.assertEqual(e1.args, e2.args)
        if isinstance(e1, JasprSessionUserFacingError):
            self.assertFalse(e1.internal)
        elif isinstance(e1, JasprSession):
            # `JasprSession`, if standalone (I.E. not an instance of a subclass of
            # `JasprSession`), should only have `internal=True` right now. This can be
            # removed later if we change the logic here, but want to check for
            # consistency in the code right now at the time of writing.
            self.assertTrue(e1.internal)
        # Exceptions should log critical if internal.
        if e1.internal:
            self.assertIn(
                f"Saw `internal=True` {e1.__class__.__name__} for user_id={e1.user.id}, "
                f"user_type={e1.user_type}, in_er={e1.in_er}, from_native={e1.from_native}, "
                f"long_lived={e1.long_lived}",
                # NOTE: If for whatever reason we have other logging that goes on after
                # our `logging.exception`, like generic/global logging, etc. that
                # somehow is caught before whatever surrounding `self.assertLogs`
                # context manager exits, the `-1` could potentially be wrong. At the
                # time of writing that's not happening though, and given the granuarity
                # of code with which we run the `assertLogs` with, it's very unlikely,
                # but we use `logging_watcher.output` as part of the error message if
                # this ever failed because of a code change, etc.
                logging_watcher.output[-1],
                logging_watcher.output,
            )

    def test_technician_combinations(self):
        technician = self.create_technician()
        parametrizer = Parametrizer(
            self.jaspr_session_params_valid_value_mapping, self.technician_combinations
        )
        result = parametrizer.result
        now = timezone.now()
        with freeze_time(now):
            for (
                in_er,
                from_native,
                long_lived,
            ) in parametrizer.all_mapping_parametrizations:
                with self.subTest(
                    in_er=in_er, from_native=from_native, long_lived=long_lived
                ):
                    expected = result[(in_er, from_native, long_lived)]
                    if isinstance(expected[0], timedelta):
                        session = JasprSession.create(
                            user=technician.user,
                            user_type="Technician",
                            in_er=in_er,
                            from_native=from_native,
                            long_lived=long_lived,
                        )[0]
                        self.assertEqual(session.user_type, "Technician")
                        self.assertEqual(session.in_er, in_er)
                        self.assertEqual(session.from_native, from_native)
                        self.assertEqual(session.long_lived, long_lived)
                        self.assertEqual(session.auth_token.created, now)
                        self.assertEqual(session.auth_token.expiry, now + expected[0])
                    else:
                        error_class, error_message = expected
                        with ExitStack() as stack:
                            if error_class is JasprSessionError:
                                logging_watcher = stack.enter_context(
                                    self.assertLogs(
                                        jaspr_models_logger, level=logging.ERROR
                                    )
                                )
                            else:
                                logging_watcher = None
                            cm = stack.enter_context(
                                self.assertRaises(JasprSessionError)
                            )
                            JasprSession.create(
                                user=technician.user,
                                user_type="Technician",
                                in_er=in_er,
                                from_native=from_native,
                                long_lived=long_lived,
                            )
                        self.assert_exceptions_match_and_log_critical_if_internal(
                            error_class(
                                error_message,
                                user=technician.user,
                                user_type="Technician",
                                in_er=in_er,
                                from_native=from_native,
                                long_lived=long_lived,
                            ),
                            cm.exception,
                            logging_watcher,
                        )

    def test_patient_combinations(self):
        patient = self.create_patient()
        parametrizer = Parametrizer(
            self.jaspr_session_params_valid_value_mapping, self.patient_combinations,
        )
        result = parametrizer.result
        now = timezone.now()
        with freeze_time(now):
            for (
                in_er,
                from_native,
                long_lived,
            ) in parametrizer.all_mapping_parametrizations:
                with self.subTest(
                    in_er=in_er, from_native=from_native, long_lived=long_lived
                ):
                    expected = result[(in_er, from_native, long_lived)]
                    if isinstance(expected[0], timedelta):
                        session = JasprSession.create(
                            user=patient.user,
                            user_type="Patient",
                            in_er=in_er,
                            from_native=from_native,
                            long_lived=long_lived,
                        )[0]
                        self.assertEqual(session.user_type, "Patient")
                        self.assertEqual(session.in_er, in_er)
                        self.assertEqual(session.from_native, from_native)
                        self.assertEqual(session.long_lived, long_lived)
                        self.assertEqual(session.auth_token.created, now)
                        self.assertEqual(session.auth_token.expiry, now + expected[0])
                    else:
                        error_class, error_message = expected
                        with ExitStack() as stack:
                            if error_class is JasprSessionError:
                                logging_watcher = stack.enter_context(
                                    self.assertLogs(
                                        jaspr_models_logger, level=logging.ERROR
                                    )
                                )
                            else:
                                logging_watcher = None
                            cm = stack.enter_context(
                                self.assertRaises(JasprSessionError)
                            )
                            JasprSession.create(
                                user=patient.user,
                                user_type="Patient",
                                in_er=in_er,
                                from_native=from_native,
                                long_lived=long_lived,
                            )
                        self.assert_exceptions_match_and_log_critical_if_internal(
                            error_class(
                                error_message,
                                user=patient.user,
                                user_type="Patient",
                                in_er=in_er,
                                from_native=from_native,
                                long_lived=long_lived,
                            ),
                            cm.exception,
                            logging_watcher,
                        )

    def test_token_returned_from_create(self):
        for user_type in ("Technician", "Patient"):
            with self.subTest(user_type=user_type):
                if user_type == "Technician":
                    jaspr_instance = self.create_technician()
                else:
                    jaspr_instance = self.create_patient()
                user = jaspr_instance.user
                session, token = JasprSession.create(
                    user=user,
                    user_type=user_type,
                    in_er=True,
                    from_native=False,
                    long_lived=False,
                )
                self.assertEqual(session.user_type, user_type)
                self.assertEqual(session.auth_token.user, user)
                self.assertTrue(session.in_er)
                self.assertFalse(session.from_native)
                self.assertFalse(session.long_lived)
                if user_type == "Technician":
                    self.assertEqual(session.auth_token.user.technician, jaspr_instance)
                else:
                    self.assertEqual(session.auth_token.user.patient, jaspr_instance)

                # Now check that the token successfully authenticates.
                authentication = JasprTokenAuthentication()
                (
                    authenticated_user,
                    authenticated_token,
                ) = authentication.authenticate_credentials(token.encode())
                self.assertEqual(authenticated_token, session.auth_token)
                self.assertEqual(authenticated_user, session.auth_token.user)

    def test_patched_knox_auth_token_objects_manager(self):
        # Make sure the initial patching is set up and working correctly.
        self.assertEqual(
            AuthToken.objects.get_queryset,
            MethodType(_get_queryset_with_jaspr_session_, AuthToken.objects),
        )
        self.assertEqual(
            AuthToken.objects.get_queryset.__func__, _get_queryset_with_jaspr_session_
        )
        self.assertIsNotNone(_auth_token_original_get_queryset_)
        # NOTE: At the time of writing, knox does not have a `get_queryset` method on
        # their `AuthToken.objects` manager. If they ever did, this would fail and we
        # should update it accordingly.
        self.assertEqual(
            super(type(AuthToken.objects).__mro__[1], AuthToken.objects).get_queryset,
            _auth_token_original_get_queryset_,
            AuthToken.objects,
        )

        # NOTE: We're testing a very specific functionality here where the underlying
        # user type shouldn't matter, so we just pick 'Patient'.
        user_type = "Patient"
        first_patient = self.create_patient()
        first_user = first_patient.user
        first_session, first_token = JasprSession.create(
            user=first_user,
            user_type=user_type,
            in_er=True,
            from_native=False,
            long_lived=False,
        )
        with CaptureQueriesContext(connection) as queries:
            authentication = JasprTokenAuthentication()
            (
                authenticated_user,
                authenticated_token,
            ) = authentication.authenticate_credentials(first_token.encode())
            first_retrieved_session = authenticated_token.jaspr_session
            first_num_queries = len(queries.captured_queries)
        self.assertEqual(authenticated_token, first_session.auth_token)
        self.assertEqual(authenticated_user, first_session.auth_token.user)
        self.assertEqual(first_session, first_retrieved_session)

        second_patient = self.create_patient()
        second_user = second_patient.user
        second_session, second_token = JasprSession.create(
            user=second_user,
            user_type=user_type,
            in_er=True,
            from_native=False,
            long_lived=False,
        )
        manager_to_patch_with = AuthTokenManager()
        with patch.object(
            AuthToken.objects, "get_queryset", _auth_token_original_get_queryset_
        ), CaptureQueriesContext(connection) as queries:
            # Make sure the patch applied successfully as intended.
            self.assertEqual(
                AuthToken.objects.get_queryset, _auth_token_original_get_queryset_
            )
            authentication = JasprTokenAuthentication()
            (
                authenticated_user,
                authenticated_token,
            ) = authentication.authenticate_credentials(second_token.encode())
            second_retrieved_session = authenticated_token.jaspr_session
            second_num_queries = len(queries.captured_queries)
        self.assertEqual(authenticated_token, second_session.auth_token)
        self.assertEqual(authenticated_user, second_session.auth_token.user)
        self.assertEqual(second_session, second_retrieved_session)

        # Now let's compare the results two `authenticate_credentials` calls. We do a
        # strict comparison to show that the second call adds one query in order to
        # access the `jaspr_session`, and the first call is one fewer queries because
        # the `select_related` was successfully applied.
        self.assertGreater(second_num_queries, first_num_queries)
        self.assertEqual(second_num_queries, first_num_queries + 1)


class TestJasprSessionPolicies(JasprTransactionTestCase):
    def test_single_patient_in_er_policy(self):
        """
        Can there only be one `JasprSession(user_type='Patient', in_er=True, ...)`
        present at a time?

        NOTE: Some of the `JasprSession.create` calls are wrapped in transaction to
        simulate actual behavior. Some are not, since the policy should work in
        either case (`transaction.on_commit` with a `TransactionTestCase` will
        properly just run right away).
        """
        system, clinic, department = self.create_full_healthcare_system()
        technician = self.create_technician(system=system, department=department)
        patient = self.create_patient()
        first_session = JasprSession.create(
            user=technician.user,
            user_type="Technician",
            in_er=True,
            from_native=False,
            long_lived=False,
        )[0]
        with transaction.atomic():
            second_session = JasprSession.create(
                user=patient.user,
                user_type="Patient",
                in_er=True,
                from_native=False,
                long_lived=False,
            )[0]
            second_session_auth_token = second_session.auth_token
        third_session = JasprSession.create(
            user=patient.user,
            user_type="Patient",
            in_er=False,
            from_native=True,
            long_lived=True,
        )[0]
        fourth_session = JasprSession.create(
            user=patient.user,
            user_type="Patient",
            in_er=True,
            from_native=False,
            long_lived=False,
        )[0]
        # Make sure the `fourth_session` `transaction.on_commit` logic ran properly
        # even when not wrapped in a transaction.
        with self.assertRaises(AuthToken.DoesNotExist):
            second_session_auth_token.refresh_from_db()
        with self.assertRaises(JasprSession.DoesNotExist):
            second_session.refresh_from_db()
        # Make sure we didn't delete ourself.
        fourth_session.refresh_from_db()
        fourth_session_auth_token = fourth_session.auth_token
        with transaction.atomic():
            fifth_session = JasprSession.create(
                user=patient.user,
                user_type="Patient",
                in_er=True,
                from_native=False,
                long_lived=False,
            )[0]
        sixth_session = JasprSession.create(
            user=patient.user,
            user_type="Patient",
            in_er=False,
            from_native=False,
            long_lived=False,
        )[0]
        seventh_session = JasprSession.create(
            user=patient.user,
            user_type="Patient",
            in_er=False,
            from_native=True,
            long_lived=False,
        )[0]
        eighth_session = JasprSession.create(
            user=patient.user,
            user_type="Patient",
            in_er=False,
            from_native=False,
            long_lived=True,
        )[0]
        # The second and fourth sessions should be deleted by the creation of the fifth
        # session, since we allow at most one `JasprSession` with 'Patient`
        # `user_type` and `in_er=True`.
        self.assertEqual(
            JasprSession.objects.filter(
                auth_token__pk__in=[
                    second_session_auth_token.pk,
                    fourth_session_auth_token.pk,
                ]
            ).count(),
            0,
        )
        self.assertEqual(JasprSession.objects.all().count(), 6)
        # Make sure the `fifth_session` `transaction.on_commit` logic ran properly when
        # wrapped in a transaction.
        with self.assertRaises(AuthToken.DoesNotExist):
            fourth_session_auth_token.refresh_from_db()
        with self.assertRaises(JasprSession.DoesNotExist):
            fourth_session.refresh_from_db()
        fifth_session.refresh_from_db()
