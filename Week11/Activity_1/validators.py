"""Input format validation.

Each function returns (is_valid, error_message).
Decoupled from the UI and business logic, so rules are easy to change
and can be unit-tested on their own.
"""

import re
from datetime import date

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_email(email: str):
    """Check that the email matches a basic name@domain.tld shape."""
    if not _EMAIL_RE.match(email):
        return False, "Invalid email format."
    return True, ""


def validate_username(username: str):
    """Check that the username is 3-20 letters / digits / underscores."""
    if not re.match(r"^[A-Za-z0-9_]{3,20}$", username):
        return False, "Username must be 3-20 letters / digits / underscores."
    return True, ""


def validate_password(password: str):
    """Check that the password is >=8 chars and has both letters and digits."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return False, "Password must contain both letters and digits."
    return True, ""


def validate_full_name(name: str):
    """Check that the full name is between 2 and 60 characters."""
    length = len(name.strip())
    if length < 2 or length > 60:
        return False, "Full name must be 2-60 characters."
    return True, ""


def validate_dob(dob: str):
    """Check DOB is YYYY-MM-DD, in the past, and within 120 years."""
    try:
        birth = date.fromisoformat(dob.strip())
    except ValueError:
        return False, "Date of birth must be in YYYY-MM-DD format."
    today = date.today()
    if birth >= today:
        return False, "Date of birth must be in the past."
    if (today.year - birth.year) > 120:
        return False, "Date of birth is unrealistically old."
    return True, ""
