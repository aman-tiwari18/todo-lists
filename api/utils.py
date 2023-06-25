import re


from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"(^[^A-Z\s]*$)"
    message = (
        "Enter a valid username. This value may contain only unaccented lowercase a-z "
        "and uppercase A-Z letters, numbers."
    )
    flags = 0


def validate_username(username):
    regex_pattern = r"(^[^A-Z\s]*$)"
    if re.match(regex_pattern, username):
        return True
    else:
        return False
