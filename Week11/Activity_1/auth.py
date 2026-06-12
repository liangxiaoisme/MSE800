"""Authentication business logic: register / login / forgot password / reset.

Each function returns (success?, message[, user]).
The UI layer only displays the message and doesn't need to know how
any of this is implemented internally.
"""

from datetime import datetime, timedelta

import security
import storage
import validators
from user import User

# How long a reset code stays valid (minutes)
_CODE_VALID_MINUTES = 10


def register(email: str, username: str, full_name: str, dob: str, password: str):
    """Create a new account after validating every field."""
    # Validate all fields up front so the user sees the first problem
    for ok, msg in (
        validators.validate_email(email),
        validators.validate_username(username),
        validators.validate_full_name(full_name),
        validators.validate_dob(dob),
        validators.validate_password(password),
    ):
        if not ok:
            return False, msg

    if storage.user_exists(email):
        return False, "This email is already registered."

    # Generate an independent salt and store the hashed password
    salt = security.generate_salt()
    user = User(
        email=email.lower(),
        username=username,
        full_name=full_name.strip(),
        dob=dob.strip(),
        password_hash=security.hash_password(password, salt),
        salt=salt,
    )
    storage.save_user(user)
    return True, "Registration successful."


def login(email: str, password: str):
    """Authenticate with email + password."""
    user = storage.get_user(email)
    # Use the same message whether the email is unknown or the password is wrong,
    # to avoid revealing whether the email exists
    if user is None or not security.verify_password(password, user.salt, user.password_hash):
        return False, "Invalid email or password.", None
    return True, f"Welcome back, {user.full_name}!", user


def request_reset_code(email: str):
    """Generate a 6-digit reset code and "send the email" (print to console).

    Returns the same message whether or not the email exists, to prevent
    account enumeration. Returns (message_for_user, simulated_email_or_None).
    """
    user = storage.get_user(email)
    generic = "If that email is registered, a reset code has been sent."
    if user is None:
        return generic, None

    code = security.generate_reset_code()
    user.reset_code = code
    user.reset_expires = (datetime.now() + timedelta(minutes=_CODE_VALID_MINUTES)).isoformat()
    user.reset_used = False
    storage.save_user(user)

    email_body = (
        f"[Simulated email -> {user.email}]\n"
        f"Your password reset code is: {code} "
        f"(valid for {_CODE_VALID_MINUTES} minutes)"
    )
    return generic, email_body


def reset_password(email: str, code: str, new_password: str):
    """Set a new password after validating the reset code."""
    user = storage.get_user(email)
    if user is None:
        return False, "Reset failed. Please check your details."

    # The code must be unused and match the input
    if user.reset_used or user.reset_code != code:
        return False, "Reset code is invalid or already used."
    # The code must not be expired
    if datetime.now() > datetime.fromisoformat(user.reset_expires):
        return False, "Reset code has expired."

    ok, msg = validators.validate_password(new_password)
    if not ok:
        return False, msg

    # Reset the password and rotate the salt so the new hash is fully
    # independent; also invalidate the reset code
    new_salt = security.generate_salt()
    user.salt = new_salt
    user.password_hash = security.hash_password(new_password, new_salt)
    user.reset_used = True
    user.reset_code = None
    storage.save_user(user)
    return True, "Password reset successfully. You can now log in."
