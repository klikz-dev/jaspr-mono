import json
from typing import Any, Dict, List, Optional, Union

from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer


# NOTE: Thanks to https://www.pydanny.com/pretty-formatting-json-django-admin.html for
# the base code.
# Other NOTE: This assumes that `json_like` is a safe object to `mark_safe` at the end
# of the function. Be aware of that!
def format_json_pretty(
    # NOTE: This is not an accurate typing for json-like, but python's `typing` can't
    # yet fully express JSON. If it can, and it's easy to do in the future, we could
    # replace this. For now though, this _could_ catch cases where clearly
    # non-json-like data was passed in so it's better than nothing.
    json_like: Union[Dict[str, Any], List[Any], float, int, bool, str, None],
    *,
    sort_keys: bool = True,
    indent: Optional[int] = 2,
    truncate_to: Optional[int] = None,
):
    """
    Function to display pretty version of json-like data (I.E. `dict`s, `list`s, etc.).
    """
    # Convert the json-like object to (if specified) a sorted, indented JSON string
    json_string = json.dumps(json_like, sort_keys=sort_keys, indent=indent)
    if truncate_to is not None:
        # Truncate the data. Alter as needed
        json_string = json_string[:truncate_to]
    # Get the Pygments formatter
    formatter = HtmlFormatter(style="colorful")
    # Highlight the data
    highlighted = highlight(json_string, JsonLexer(), formatter)
    # Get the stylesheet
    style = "<style>" + formatter.get_style_defs() + "</style><br>"
    # Safe the output
    return mark_safe(style + highlighted)
