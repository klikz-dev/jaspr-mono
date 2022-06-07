from contextlib import nullcontext
from dataclasses import dataclass
from typing import Optional

from jaspr.apps.common.validators import JasprPasswordValidator, ValidationError
from jaspr.apps.test_infrastructure.testcases import JasprSimpleTestCase


@dataclass
class ValidatePasswordCase:
    password: Optional[str]
    min_characters: int
    expected_result: Optional[str] = None

    require_upper_case: bool = False
    require_lower_case: bool = False
    require_number: bool = False
    require_special_character: bool = False


class TestValidatePassword(JasprSimpleTestCase):
    Case = ValidatePasswordCase

    cases = [
        Case(None, 1, "Passwords must be at least 1 character."),
        Case("", 1, "Passwords must be at least 1 character."),
        Case("1", 1),
        Case("a", 1),
        Case("ab", 1),
        Case("ab", 2),
        Case("abc", 2),
        Case("abc", 4, "Passwords must be at least 4 characters."),
        Case(
            "abcd",
            3,
            "Passwords must be at least 3 characters and have at least one uppercase character.",
            require_upper_case=True,
        ),
        Case(
            "ABCD",
            3,
            "Passwords must be at least 3 characters and have at least one lowercase character.",
            require_lower_case=True,
        ),
        Case(
            "aBcD",
            3,
            "Passwords must be at least 3 characters and have at least one number.",
            require_number=True,
        ),
        Case(
            "1bCD",
            3,
            "Passwords must be at least 3 characters and have at least one special character.",
            require_special_character=True,
        ),
        Case(
            "ab3@",
            4,
            "Passwords must be at least 4 characters and have at least one uppercase character and one special character.",
            require_upper_case=True,
            require_special_character=True,
        ),
        Case(
            "aB#@",
            4,
            "Passwords must be at least 4 characters and have at least one lowercase character and one number.",
            require_lower_case=True,
            require_number=True,
        ),
        Case("aBcD", 4, require_lower_case=True, require_upper_case=True),
        Case(
            "aB#@",
            4,
            "Passwords must be at least 4 characters and have at least one lowercase character, one number, and one special character.",
            require_lower_case=True,
            require_number=True,
            require_special_character=True,
        ),
        Case(
            "aB3P",
            4,
            "Passwords must be at least 4 characters and have at least one uppercase character, one number, and one special character.",
            require_upper_case=True,
            require_number=True,
            require_special_character=True,
        ),
        Case(
            "aB3@",
            4,
            require_upper_case=True,
            require_number=True,
            require_special_character=True,
        ),
        Case(
            "aB31O7",
            5,
            "Passwords must be at least 5 characters and have at least one uppercase character, one lowercase character, one number, and one special character.",
            require_upper_case=True,
            require_lower_case=True,
            require_number=True,
            require_special_character=True,
        ),
        Case(
            "a12Bc@#",
            8,
            "Passwords must be at least 8 characters and have at least one uppercase character, one lowercase character, one number, and one special character.",
            require_upper_case=True,
            require_lower_case=True,
            require_number=True,
            require_special_character=True,
        ),
        Case(
            "aB3@",
            4,
            require_upper_case=True,
            require_lower_case=True,
            require_number=True,
            require_special_character=True,
        ),
    ]

    def run_and_test_case(self, case: ValidatePasswordCase) -> None:
        validator = JasprPasswordValidator(
            min_characters=case.min_characters,
            require_upper_case=case.require_upper_case,
            require_lower_case=case.require_lower_case,
            require_number=case.require_number,
            require_special_character=case.require_special_character,
        )
        with (
            nullcontext()
            if case.expected_result is None
            else self.assertRaises(ValidationError)
        ) as cm:
            result = validator(case.password)
        if case.expected_result is None:
            self.assertIsNone(result)
        else:
            # Make sure the `case` specified an expected error that is a string.
            self.assertIsInstance(case.expected_result, str)
            # Make sure the `case` specified an expected error message here.
            self.assertTrue(len(case.expected_result) >= 1)
            # Now check that the exception message is what is expected.
            self.assertEqual(cm.exception.messages, [case.expected_result])
            self.assertEqual(cm.exception.code, "invalid")

    def test_validate_password(self):
        for case in self.cases:
            with self.subTest(case=case):
                self.run_and_test_case(case)
