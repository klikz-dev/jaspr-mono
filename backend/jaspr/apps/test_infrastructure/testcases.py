from django.test import SimpleTestCase, TestCase, TransactionTestCase
from rest_framework.test import APITestCase, APITransactionTestCase

from jaspr.apps.test_infrastructure.mixins.jaspr_mixins import (
    JasprApiTokenMixin,
    JasprTestCaseMixin,
)
from jaspr.apps.test_infrastructure.mixins.redis_mixins import RedisTestCaseMixin


class JasprSimpleTestCase(SimpleTestCase):
    """Base Test Case for Jaspr non-API tests that don't use the DB."""


class JasprTestCase(JasprTestCaseMixin, TestCase):
    """Base Test Case for Jaspr non-API tests."""


class JasprTransactionTestCase(JasprTestCaseMixin, TransactionTestCase):
    """Base Test Case for Jaspr non-API tests involging certain transaction behavior."""


class JasprApiTestCase(JasprApiTokenMixin, JasprTestCaseMixin, APITestCase):
    """Base Test Case for Jaspr API tests."""


class JasprApiTransactionTestCase(
    JasprApiTokenMixin, JasprTestCaseMixin, APITransactionTestCase
):
    """Base Test Case for Jaspr API tests involving certain transaction behavior."""


class JasprRedisTestCase(RedisTestCaseMixin, JasprTestCase):
    """Base Test Case for Jaspr non-API tests involving Redis."""


class JasprApiRedisTestCase(RedisTestCaseMixin, JasprApiTestCase):
    """Base Test Case for Jaspr API tests involving Redis."""
