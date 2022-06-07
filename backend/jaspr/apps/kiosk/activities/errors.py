
VALIDATION_ERRORS = {
    "not_all_blank": "Must provide at least one of name or phone number.",
    "list_required": "A list of required."
}


class ActivityValidationError(Exception):

    NOT_ALL_BLANK = "not_all_blank"
    LIST_REQUIRED = "list_required"

    def __init__(self, validation_type: str, field: str):
        self.validation_type = validation_type
        self.field = field
        self.message = VALIDATION_ERRORS[validation_type]
        super().__init__(self.message)
