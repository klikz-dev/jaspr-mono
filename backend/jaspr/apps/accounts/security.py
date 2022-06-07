import inspect
import random
import secrets
from typing import List, Set

from django.utils.crypto import get_random_string

DEFAULT_ALLOWED_CHARS: str = inspect.signature(get_random_string).parameters[
    "allowed_chars"
].default
assert isinstance(DEFAULT_ALLOWED_CHARS, str)
assert len(DEFAULT_ALLOWED_CHARS) >= 52
assert (
    "a" in DEFAULT_ALLOWED_CHARS
    and "Z" in DEFAULT_ALLOWED_CHARS
    and "9" in DEFAULT_ALLOWED_CHARS
)


def generate_multiple_unique_secure_random_strings(
    number: int,
    length: int,
    exclude: str = None,
    *,
    enforce_exclude_length: bool = True,
) -> List[str]:
    assert number >= 1 and number <= 10
    assert length >= 1 and length <= 100
    excluded_set: Set[str] = set() if not exclude else set(exclude)
    allowed_set: Set[str] = set(DEFAULT_ALLOWED_CHARS) - excluded_set
    if enforce_exclude_length:
        assert (
            len(allowed_set) >= 40
        ), "Can't `exclude` too many characters otherwise this may not be secure enough."

    strings: List[str] = []
    for n in range(number):
        allowed_chars = "".join(allowed_set)
        random_string = get_random_string(length=length, allowed_chars=allowed_chars)
        assert len(random_string) == length
        allowed_set.discard(secrets.choice(random_string))
        strings.append(random_string)

    # Since each one generated has one less character in `allowed_chars`, shuffle so
    # that the order for that isn't consistent.
    random.shuffle(strings)
    return strings
