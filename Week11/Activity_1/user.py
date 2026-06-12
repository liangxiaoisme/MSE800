"""User domain model.

Separates "what the data looks like" from "how the data is stored":
changing the storage backend (JSON -> database) won't affect this file.
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class User:  # pylint: disable=too-many-instance-attributes
    """A registered user account.

    A plain data container; the extra attributes are intentional fields
    (profile info + password-reset state), so the attribute count is fine.
    """

    email: str                            # login identifier + simulated inbox
    username: str                         # display name
    full_name: str                        # full name (personal info)
    dob: str                              # date of birth YYYY-MM-DD (personal info)
    password_hash: str                    # salted password hash (never plaintext)
    salt: str                             # per-user random salt
    reset_code: Optional[str] = None      # current password reset code
    reset_expires: Optional[str] = None   # reset code expiry time (ISO string)
    reset_used: bool = True               # whether the reset code has been used

    def to_dict(self) -> dict:
        """Convert to a plain dict for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Rebuild a User object from a dict loaded from JSON."""
        return cls(**data)
