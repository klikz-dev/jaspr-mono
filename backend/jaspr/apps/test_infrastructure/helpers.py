from contextlib import contextmanager

from django.db import transaction


class IntentionalTransactionRollback(Exception):
    """
    The specific exception subclass that should be raised at the end of a section of
    code within a transaction and then caught to have that transaction roll back.

    The reason this exception (instead of just `Exception` in general or some other
    exception, etc.) is being raised is to hopefully create consistent behavior and
    recognition in the code for this sort of strategy. The initial pattern I created
    this exception class for is below:

    ```
    # Iterate over some variations we want to test.
    for ...:
        # Start a `subTest` with those variations, and expect the
        # `IntentionalTransactionRollback` to be thrown (indicating the code exited
        # smoothly) once the block of code finishes. Then enter a transaction and run
        # the code, throwing `IntentionalTransactionRollback` at the end. It will exit
        # the transaction block first, causing the transaction to roll back and then
        # hit the `assertRaises` block, causing the code to continue running and the
        # `subTest` to pass.
        with self.subTest(...), self.assertRaises(IntentionalTransactionRollback), transaction.atomic():
            ...
            raise IntentionalTransactionRollback
    ```

    I encapsulated part of the above idea into a context manager below called
    `enter_transaction_then_roll_back`. So that I didn't have to depend on a
    `SimpleTestCase` instance, I just catch `IntentionalTransactionRollback` at the
    end and `pass`, instead of doing `assertRaises`. I didn't encapsulate the `for
    ...` and `with self.subTest(...)` part of the above example. For now that can be
    done in the individual test cases, and there should be some examples in the tests
    that use this pattern. One place to look at the time of writing for an example of
    how `enter_transaction_then_roll_back` below is used is in
    `test_tools_to_go_verification_flow_api.py`.
    """


@contextmanager
def enter_transaction_then_roll_back():
    """
    Enter a transaction, and intentionally roll it back after exiting (assuming the
    block(s) of code within this context manager ran normally without raising an
    uncaught exception).
    """
    try:
        with transaction.atomic():
            yield
            raise IntentionalTransactionRollback
    except IntentionalTransactionRollback:
        pass
