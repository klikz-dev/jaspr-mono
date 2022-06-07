from typing import Optional

from django.core.validators import RegexValidator, ValidationError, _lazy_re_compile
from django.utils.translation import gettext_lazy as _

zero_positive_integer_validator = RegexValidator(
    _lazy_re_compile(r"^[0-9]+\Z"),
    message=_("Enter a valid positive integer."),
    code="invalid",
)


nonzero_positive_integer_validator = RegexValidator(
    _lazy_re_compile(r"^[1-9]+[0-9]*\Z"),
    message=_("Enter a valid nonzero positive integer."),
    code="invalid",
)


class JasprPasswordValidator:
    def __init__(
        self,
        *,
        min_characters: int,
        require_upper_case: bool,
        require_lower_case: bool,
        require_number: bool,
        require_special_character: bool,
    ):
        assert min_characters >= 1
        self.min_characters = min_characters
        self.require_upper_case = require_upper_case
        self.require_lower_case = require_lower_case
        self.require_number = require_number
        self.require_special_character = require_special_character

    def __call__(self, password: Optional[str]) -> None:
        if not password:
            password_valid = False
        elif len(password) < self.min_characters:
            password_valid = False
        elif self.require_upper_case and not "".join(filter(str.isupper, password)):
            password_valid = False
        elif self.require_lower_case and not "".join(filter(str.islower, password)):
            password_valid = False
        # NOTE: We'll be looser on the requirements here by allowing something more broad
        # than just a `0-9` digit. Instead, we'll allow anything that is considered
        # "numeric" according to `str.isnumeric` (vs using `str.isdigit`).
        elif self.require_number and not "".join(filter(str.isnumeric, password)):
            password_valid = False
        elif self.require_special_character and not "".join(
            filter(lambda s: not s.isalnum(), password)
        ):
            password_valid = False
        else:
            password_valid = True
        if not password_valid:
            raise self.construct_validation_error()

    def construct_validation_error(self) -> ValidationError:
        message = "Passwords must be at least %(min_characters)s character"
        if self.min_characters > 1:
            message += "s"
        extra = []
        if self.require_upper_case:
            extra.append("one uppercase character")
        if self.require_lower_case:
            extra.append("one lowercase character")
        if self.require_number:
            extra.append("one number")
        if self.require_special_character:
            extra.append("one special character")
        if not extra:
            message += "."
        elif len(extra) == 1:
            message += f" and have at least {extra[0]}."
        elif len(extra) == 2:
            message += f" and have at least {extra[0]} and {extra[1]}."
        else:
            message += f" and have at least {', '.join(extra[:-1])}, and {extra[-1]}."
        return ValidationError(
            _(message), code="invalid", params={"min_characters": self.min_characters}
        )
