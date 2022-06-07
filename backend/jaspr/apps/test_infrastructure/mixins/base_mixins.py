import re
from typing import Any, Callable, ClassVar, Dict, List, Literal, Optional, Tuple, Type
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import Group, GroupManager
from django.test import TestCase, TransactionTestCase
from django.utils.text import slugify

from jaspr.apps.accounts.models import User
from jaspr.apps.clinics.models import HealthcareSystem, Clinic, Department

from jaspr.apps.common.decorators import classproperty
from jaspr.apps.test_infrastructure.enhanced_baker import baker

KwargsType = Dict[str, Any]


class MockGroupObjects:
    """
    Used to mock `Group.objects`, and allow
    `Group.objects.get(...)` to proxy to test
    methods that cache those values, etc. Essentially
    allows for lazy group creation/retrieval so that
    we don't have to set up multiple groups before
    every test.
    """

    def __init__(
        self, django_group_objects: GroupManager, retriever: Callable[[str], Group]
    ):
        # Using trailing underscores since we're mocking `Group.objects`,
        # and don't want to provide any conflicts.
        self.django_group_objects_ = django_group_objects
        self.retriever_ = retriever

    def get(self, **kwargs) -> Group:
        """
        Mocks `Group.objects.get()`.

        NOTE: At this point in the codebase, we don't query
        anything like `Group.objects.get(permissions__in...)`.
        We don't even use `permissions` at when querying `Group.objects`
        right now, we just use `Group.objects.get(name=)`.
        """
        retriever = super().__getattribute__("retriever_")
        return retriever(kwargs.get("name"))

    def __getattribute__(self, name: str) -> Any:
        if name == "get":
            return super().__getattribute__("get")
        else:
            django_group_objects = super().__getattribute__("django_group_objects_")
            return getattr(django_group_objects, name)


class BaseGroupMixin:
    """
    The base class for mixing in group related functionality into tests/testcases.
    Follow the naming conventions of snake casing the name of the group followed by
    `_group` as a `@classproperty` with caching behavior to minimize database queries
    (and unecessary group creations when they're never used) and allow `group_for` to
    find the correct group.
    """

    all_group_names: ClassVar[List[str]] = [
        settings.TECHNICIAN_GROUP_NAME,
        settings.PATIENT_GROUP_NAME,
    ]

    @classproperty(lazy=True)
    def is_transaction_test_case_but_not_test_case(cls) -> bool:
        return not issubclass(cls, TestCase) and issubclass(cls, TransactionTestCase)

    @classmethod
    def setUpClass(cls) -> None:
        cls._cached_groups: Dict[str, Group] = {}
        super().setUpClass()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.set_up_group_patching_and_initial_groups()
        super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._cached_groups.clear()
        super().tearDownClass()

    @classmethod
    def set_up_group_patching_and_initial_groups(cls) -> None:
        patch_group_objects(cls)
        # NOTE: This is plenty efficient (since only creating once per class and then
        # retrieving cached values), but not as efficient as maybe it could be. This
        # can always be optimized/ made faster in the future. The most ideal would be
        # that groups were either just always present in the database (via a migration
        # maybe), or that they're only created when accessed. That was hard to get
        # working with the way Django does stuff when I tried most recently so I opted
        # for this approach for now to allow `setUpTestData` to work nicely.
        cls._cached_groups: Dict[str, Group] = {
            name: Group(name=name) for name in cls.all_group_names
        }
        Group.objects.bulk_create(cls._cached_groups.values(), ignore_conflicts=True)
        groups_re_queried = Group.objects.filter(name__in=[*cls._cached_groups])
        for group_instance in groups_re_queried:
            assert group_instance.name in cls._cached_groups, "Pre-condition"
            cls._cached_groups[group_instance.name] = group_instance

    @classmethod
    def group_for(cls, group_name: str) -> Group:
        if cls.is_transaction_test_case_but_not_test_case:
            # NOTE/TODO: Our use of `TransactionTestCase`, at the time of writing, is
            # pretty scarce (as it should be). I tried to cache the value here in those
            # test cases, but ran into some transaction/atomicity/rollback problems.
            # Instead of trying to deep dive into it I figured this would be quite fine
            # for now. I think the problems were that, in a transaction test case, the
            # entire database is flushed in-between each test method, which means
            # caching at the class level is a no-no, so we'd need to have instance
            # caching in those cases. This could be improved in the future if need be.
            # My thought would be to treat `set_up_group_patching_and_initial_groups`,
            # `patch_group_objects`, and any other places as `cls`/`self` agnostic
            # (which they already should be) so that they could operate in either case
            # (but `cls` `_cached_groups` should still be set so test `@classmethod`s
            # still access the right thing I think). We'd need to add things to `setUp`
            # if `self.is_transaction_test_case_but_not_test_case` is `False` (or
            # something like that), and probably go from there.
            return Group.objects.get_or_create(name=group_name)[0]
        return cls._cached_groups[group_name]


class BaseTestCaseMixin:
    """
    Collection of helper methods for tests.
    Useful for both API and non-API tests.
    """

    @staticmethod
    def extract_nested_kwargs(
        prefix: str, kwargs: KwargsType
    ) -> Tuple[KwargsType, KwargsType]:
        """
        Takes in a `prefix` and a dictionary `kwargs` and returns two dictionaries.

        First Dictionary: Take all the keys in `kwargs` that start with
        `f"{prefix}__"`, remove them, then remove `f"{prefix}__"` from the start of
        the key, and then insert each key and value into a new dictionary; that's the
        first dictionary.

        Second Dictionary: Take all the keys in `kwargs` that don't start with
        `user__`, remove them, and insert each key and value into a new dictionary;
        that's the second dictionary.
        """
        assert not prefix.endswith("__"), (
            "`prefix` should not end in double underscores. "
            "This method will add them when needed."
        )
        extracted_kwargs: KwargsType = {}
        non_extracted_kwargs: KwargsType = {}
        for key, value in kwargs.items():
            if key.startswith(f"{prefix}__"):
                extracted_kwargs[re.sub(fr"^{prefix}__", "", key)] = value
            else:
                non_extracted_kwargs[key] = value
        return extracted_kwargs, non_extracted_kwargs

    @classproperty
    def base_incrementor(cls) -> int:
        """
        Can be helpful with generating unique values when running tests.
        Due to how Django tests work and how we're using it,
        this shouldn't need to be thread safe.
        """
        current_value = getattr(cls, "_base_incrementor", 0)
        new_value = current_value + 1
        cls._base_incrementor = new_value
        return new_value

    @classmethod
    def create_user(cls, group: Optional[Group] = None, **kwargs) -> User:
        """Helper function to create a `User`."""
        kwargs.setdefault("email", "user@test.com")
        kwargs.setdefault("password", "password")
        user = User.objects.create_user(**kwargs)
        if group:
            user.groups.add(group)
        return user

    @classmethod
    def create_underlying_user(cls, group_name: str, **kwargs) -> User:
        """
        Helper function to create a `User` for a `Patient`, `Therapist`, etc.
        or other type that has a foreign key to `User`.
        """
        if "email" not in kwargs:
            # Only access the `base_incrementor` if we have to.
            kwargs["email"] = f"{group_name.lower()}-{cls.base_incrementor}@example.com"
        # NOTE: Whatever is subclassing/mixing in this class should also
        # subclass/mix in `BaseGroupMixin` or a subclass of that.
        group = cls.group_for(group_name)
        return cls.create_user(group, **kwargs)

    @classmethod
    def create_full_healthcare_system(cls,
                                      name=None,
                                      system=None,
                                      clinic=None,
                                      department=None,
                                      system_kwargs=None,
                                      clinic_kwargs=None,
                                      department_kwargs=None,
                                      skip_clinic=False,
                                      skip_department=False):

        if system_kwargs is None:
            system_kwargs = {}

        if name is not None:
            system_kwargs["name"] = name

        if clinic_kwargs is None:
            clinic_kwargs = {}

        if department_kwargs is None:
            department_kwargs = {}

        if system is None:
            if clinic is not None:
                system = clinic.system
            elif department is not None:
                system = department.clinic.system
            else:
                system_name = system_kwargs.pop("name", "Generic Test System")
                organization_code = system_kwargs.pop("organization_code", None)
                if organization_code is None:
                    organization_code = slugify(system_name)

                system = HealthcareSystem.objects.filter(organization_code=organization_code, name=system_name).first()

                if not system:
                    system = baker.make(
                        HealthcareSystem,
                        name=system_name,
                        organization_code=organization_code,
                        **system_kwargs
                    )

        if clinic is None and not skip_clinic:
            if department is not None:
                clinic = department.clinic
            else:
                clinic_name = clinic_kwargs.pop("name", "unassigned")
                clinic = Clinic.objects.filter(
                    system=system, name=clinic_name
                ).first()
                if not clinic:
                    clinic = baker.make(
                        Clinic,
                        system=system,
                        name=clinic_name,
                        **clinic_kwargs
                    )

        if department is None and not skip_department:
            department_name = department_kwargs.pop("name", "unassigned")
            department = Department.objects.filter(
                clinic=clinic, name=department_name
            ).first()

            if not department:
                department = baker.make(
                    Department,
                    clinic=clinic,
                    name=department_name,
                    **department_kwargs
                )

        return system, clinic, department

    @classmethod
    def create_healthcare_system(cls, **kwargs) -> HealthcareSystem:
        system, _, _ = cls.create_full_healthcare_system(system_kwargs=kwargs, skip_clinic=True, skip_department=True)
        return system

    @classmethod
    def create_clinic(cls, **kwargs) -> Clinic:
        system = kwargs.pop("system", None)
        _, clinic, _ = cls.create_full_healthcare_system(system=system, clinic_kwargs=kwargs, skip_department=True)
        return clinic

    @classmethod
    def create_department(cls, **kwargs):
        system = kwargs.pop("system", None)
        clinic = kwargs.pop("clinic", None)
        _, _, department = cls.create_full_healthcare_system(system=system, clinic=clinic, department_kwargs=kwargs)
        return department


def patch_group_objects(cls: Type[BaseGroupMixin]) -> None:
    django_group_objects = Group.objects
    mock_group_objects = MockGroupObjects(django_group_objects, cls.group_for)
    patcher = patch.object(Group, "objects", new=mock_group_objects)
    patcher.start()
    # Assuming that `cls` is a subclass of `unittest.TestCase` or something similar
    # that has an `addClassCleanup` method.
    cls.addClassCleanup(patcher.stop)
