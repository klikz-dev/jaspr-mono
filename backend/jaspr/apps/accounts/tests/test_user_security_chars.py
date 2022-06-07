from itertools import combinations
from typing import Union

from jaspr.apps.accounts.models import User
from jaspr.apps.accounts.security import (
    DEFAULT_ALLOWED_CHARS,
    generate_multiple_unique_secure_random_strings,
)
from jaspr.apps.test_infrastructure.testcases import JasprSimpleTestCase, JasprTestCase


class SecurityCharsTestMixin:
    def _assert_current_security_chars_consistency(
        self: Union[JasprTestCase, JasprSimpleTestCase], chars: str
    ) -> None:
        self.assertEqual(len(chars), 100)
        groups = [chars[start : start + 25] for start in range(0, 100, 25)]
        for n, pair in enumerate(combinations(groups, 2)):
            first = pair[0]
            second = pair[1]
            with self.subTest(n=n, first=first, second=second):
                self.assertNotEqual(first, second)


class TestUserSecurityChars(SecurityCharsTestMixin, JasprTestCase):
    def test_setting_user_password_updates_current_security_chars(self):
        user = User()

        self.assertEqual(user.current_security_chars, "")
        user.set_password("someOtherPassw0rd@!21")
        chars = user.current_security_chars
        self._assert_current_security_chars_consistency(user.current_security_chars)

        user.current_security_chars = "a" * 100
        self.assertEqual(user.current_security_chars, "a" * 100)
        user.set_password("someOtherPassw0rd@!21")
        chars = user.current_security_chars
        self.assertNotEqual(chars, "a" * 100)
        self._assert_current_security_chars_consistency(user.current_security_chars)

    def test_saving_user_updates_current_security_chars_if_not_present_or_wrong_length(
        self,
    ):
        user = self.create_user()
        self._assert_current_security_chars_consistency(user.current_security_chars)

        # Let's set them empty (and check that `""` or `None` are both handled).
        for empty_like_value in ("", None):
            with self.subTest(empty_like_value=empty_like_value):
                user.current_security_chars = empty_like_value
                user.save()
                chars = user.current_security_chars
                self._assert_current_security_chars_consistency(chars)
                # Once it's already consistent, re-saving shouldn't re-generate any
                # chars.
                user.save()
                user.refresh_from_db()
                self.assertEqual(user.current_security_chars, chars)

        # Now let's try to slightly change the length.
        try_to_change_to_chars = chars[:-1]
        user.current_security_chars = try_to_change_to_chars
        user.save()
        self.assertNotEqual(try_to_change_to_chars, user.current_security_chars)
        self._assert_current_security_chars_consistency(user.current_security_chars)


class TestGenerateMultipleUniqueSecureRandomStrings(
    SecurityCharsTestMixin, JasprSimpleTestCase
):
    def test_all_strings_unique_down_to_last_character(self):
        exclude = "".join(set(DEFAULT_ALLOWED_CHARS) - set("abcd"))
        strings = generate_multiple_unique_secure_random_strings(
            4, 25, exclude=exclude, enforce_exclude_length=False
        )
        chars = "".join(strings)
        self.assertTrue(all(len(set(s)) <= 4 for s in strings))
        # When we get down to the last string it should only be one character. It's
        # possible other ones could only be one character as well, so we just make sure
        # at least one of them is.
        self.assertTrue(any(len(set(s)) == 1 for s in strings))
        self._assert_current_security_chars_consistency(chars)
