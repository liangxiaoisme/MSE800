"""Password security helpers: PBKDF2 hashing + 6-digit reset code.

Key learning points: passwords are never stored in plaintext, and each
user gets an independent random salt. Uses only the Python standard
library, so no third-party dependency is required.
"""

import hashlib
import os
import secrets

# Number of PBKDF2 iterations. Higher = slower brute force (more secure).
_ITERATIONS = 200_000


def generate_salt() -> str:
    """Generate a 16-byte random salt as a hex string."""
    return os.urandom(16).hex()


def hash_password(password: str, salt: str) -> str:
    """Hash (password + salt) into a hex string using PBKDF2-HMAC-SHA256."""
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        _ITERATIONS,
    )
    return derived.hex()


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    """Check a password. Uses constant-time comparison to resist timing attacks."""
    candidate = hash_password(password, salt)
    return secrets.compare_digest(candidate, expected_hash)


def generate_reset_code() -> str:
    """Generate a 6-digit numeric code, e.g. '482915' (zero-padded)."""
    return f"{secrets.randbelow(1_000_000):06d}"
