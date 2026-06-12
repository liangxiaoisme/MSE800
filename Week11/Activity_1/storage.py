"""JSON file persistence layer.

The business layer (auth) talks only to this module.
To switch to SQLite/a database later, only this file changes; auth stays put.
"""

import json
import os
from typing import Optional

from user import User

# Data file lives in the same directory as this script
_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def _load_all() -> dict:
    """Read the whole JSON file; return an empty dict if missing or corrupt."""
    if not os.path.exists(_FILE):
        return {}
    try:
        with open(_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_all(data: dict) -> None:
    """Write the whole dict back to the JSON file."""
    with open(_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_user(email: str) -> Optional[User]:
    """Look up a user by email (case-insensitive); return None if not found."""
    record = _load_all().get(email.lower())
    return User.from_dict(record) if record else None


def save_user(user: User) -> None:
    """Insert or update a user record (keyed by lowercase email)."""
    data = _load_all()
    data[user.email.lower()] = user.to_dict()
    _save_all(data)


def user_exists(email: str) -> bool:
    """Check whether an email is already registered."""
    return email.lower() in _load_all()
