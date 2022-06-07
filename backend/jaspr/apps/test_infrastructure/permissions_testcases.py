import unittest
from contextlib import contextmanager
from types import MethodType
from typing import Type

from rest_framework import status
from rest_framework.test import APITestCase

from jaspr.apps.test_infrastructure.mixins.jaspr_mixins import (
    JasprApiTokenMixin,
    JasprTestCaseMixin,
)


class NoopObject:
    """
    Used by an instances of `BaseTestResourcePermissions`
    as the return value of the `self.factory(...)` call
    so that a detail route can be generated even if
    the permissions test doesn't supply a factory/object.
    """

    # Just define the primary key as returning `1`.
    pk = 1


class JasprTestResourcePermissions(JasprApiTokenMixin, JasprTestCaseMixin, APITestCase):
    """Test 401 403, and 405 for a resource."""

    @classmethod
    def setUpClass(cls):
        if cls is JasprTestResourcePermissions:
            raise unittest.SkipTest(
                "Skip `JasprTestResourcePermissions` tests; it's a base class."
            )
        super().setUpClass()

    def create_noop_object(self, *args, **kwargs) -> Type[NoopObject]:
        """
        NOTE: In `setUp`, `self.factory` expects a callable,
        so this can be used if nothing is supplied
        for `factory_name`.
        """
        return NoopObject

    def setUp(
        self, resource_pattern=None, version_prefix=None, factory_name=None, **kwargs
    ):
        assert resource_pattern is not None, "Need to define kwarg: `resource_pattern`"
        assert version_prefix is not None, "Need to define kwarg: `version_prefix`"
        if factory_name is None:
            factory_name = "create_noop_object"

        super().setUp()

        self.groups = {
            # A special group that is not really in the DB.
            "Anonymous": {"factory": None, "set_creds": None},
            "Technician": {
                "factory": getattr(self, "create_technician"),
                "set_creds": getattr(self, "set_technician_creds"),
                # Subclasses can override this to default to certain `kwargs` for
                # `set_technician_creds`
                "set_creds_kwargs": {},
            },
            "Patient": {
                "factory": getattr(self, "create_patient"),
                "set_creds": getattr(self, "set_patient_creds"),
                # Subclasses can override this to default to certain `kwargs` for
                # `set_patient_creds`
                "set_creds_kwargs": {},
            },
        }

        self.action_group_map = {
            "create": {"method": "post", "detail": False, "allowed_groups": []},
            "list": {"method": "get", "detail": False, "allowed_groups": []},
            "partial_update": {"method": "patch", "detail": True, "allowed_groups": []},
            "retrieve": {"method": "get", "detail": True, "allowed_groups": []},
            "update": {"method": "put", "detail": True, "allowed_groups": []},
            "delete": {"method": "delete", "detail": True, "allowed_groups": []},
        }

        self.factory_kwargs = kwargs
        self.factory = getattr(self, factory_name)
        self.object = self.factory(**self.factory_kwargs)

        self.resource = ""
        self.base_uri = f"/{version_prefix}/{resource_pattern}"
        self.detail_uri = f"{self.base_uri}/{self.object.pk}"

    def test_permissions_of_forbidden_groups(self):
        """Do users in a forbidden group get expected errors?"""

        # get a list of the allowed groups for this uri, without respect to action
        all_allowed_groups = []
        all_allowed_detail_groups = []
        all_allowed_base_uri_groups = []
        # print("Inside test")
        # print(self.action_group_map)
        for action in self.action_group_map:
            all_allowed_groups.extend(self.action_group_map[action]["allowed_groups"])
            if self.action_group_map[action]["detail"]:
                all_allowed_detail_groups.extend(
                    self.action_group_map[action]["allowed_groups"]
                )
            # NOTE: Some tests override `detail_uri` to match `base_uri`. In those cases,
            # if we're at a detail endpoint and the base matches the detail, then
            # technically `all_allowed_base_uri_groups` should be extended in addition
            # to `all_allowed_detail_groups`.
            if (
                not self.action_group_map[action]["detail"]
                or self.detail_uri == self.base_uri
            ):
                all_allowed_base_uri_groups.extend(
                    self.action_group_map[action]["allowed_groups"]
                )

        all_allowed_groups = list(set(all_allowed_groups))
        all_allowed_detail_groups = list(set(all_allowed_detail_groups))
        all_allowed_base_uri_groups = list(set(all_allowed_base_uri_groups))

        # now iterate through all groups
        for group in self.groups:
            # print(group)

            if factory := self.groups[group]["factory"]:
                instance = factory()
                set_creds_kwargs = self.groups[group]["set_creds_kwargs"]
                if "encounter" in set_creds_kwargs:
                    encounter = self.create_patient_encounter(patient=instance)
                    set_creds_kwargs["encounter"] = encounter

                self.groups[group]["set_creds"](instance, **set_creds_kwargs)

            for action in self.action_group_map:
                # print('    {}'.format(action))
                action_info = self.action_group_map[action]
                uri = self.detail_uri if action_info["detail"] else self.base_uri
                #print('{}        {}'.format(action, uri))

                if group in action_info["allowed_groups"]:
                    pass
                    # print('        allowed, testing skipped')

                else:
                    # print('        banned')

                    client_method = getattr(self.client, action_info["method"])

                    # order of finding an error
                    # 404  HTTP_404_NOT_FOUND
                    #     -- no URI
                    # 401  HTTP_401_UNAUTHORIZED
                    #     -- URI will not respond to unauthenticated user
                    # 403  HTTP_403_FORBIDDEN
                    #     -- this authenticated user doesn't have permission to view URI
                    # 405  HTTP_405_METHOD_NOT_ALLOWED
                    #    -- this method is not available on URI to authenticated users
                    #       with permissions to access this URI

                    if action_info["detail"] and not all_allowed_detail_groups:
                        expected_status_code = status.HTTP_404_NOT_FOUND

                    elif not action_info["detail"] and not all_allowed_base_uri_groups:
                        expected_status_code = status.HTTP_404_NOT_FOUND

                    elif group == "Anonymous":
                        expected_status_code = status.HTTP_401_UNAUTHORIZED
                        self.client.credentials()

                    elif group not in all_allowed_groups:
                        expected_status_code = status.HTTP_403_FORBIDDEN

                    else:
                        expected_status_code = status.HTTP_405_METHOD_NOT_ALLOWED

                    response = client_method(uri)
                    # print('        {}'.format(response.status_code))

                    msg = "Expecting {}, instead found {} with {} and user with group {}.".format(
                        expected_status_code, response.status_code, action, group
                    )
                    self.assertEqual(expected_status_code, response.status_code, msg)
