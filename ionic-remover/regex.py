import re

from typing import Optional, Pattern

# Compiled regular expressions
REGEX_ELEMENT = re.compile(r"<(/)?(Ion[A-Z]\w+)([^>]*)>")
REGEX_CLASS_NAME = re.compile(r"(className\s*=\s*\")")
REGEX_CAPITAL_LETTER = re.compile(r"[A-Z]")  # Skip the first character

# Lazily compiled regular expressions
regex_import: Optional[Pattern[str]] = None


def get_import_regex(remove_capacitor: bool):
    global regex_import
    if regex_import is None:
        if remove_capacitor:
            import_prefixes = "(ionic(-native)?|capacitor)"
        else:
            import_prefixes = "ionic(-native)?"

        regex_import = re.compile(
            r"import(\s+\w+\s*,?)?(\s*{[^}]*}\s*)?((from)?\s*\"@" + import_prefixes + r"\/[^\"\s]+\"\s*;?\s*)")

    return regex_import
