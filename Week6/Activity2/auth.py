# -*- coding: utf-8 -*-
"""
auth.py - Authentication logic for the Zoo Application login system.
The admin_login function is decorated with @log_admin_activity.
"""

from decorators import log_admin_activity

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "zoo2026"


@log_admin_activity
def admin_login(username, password):
    """Verify admin credentials. Returns True if valid, False otherwise."""
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("  -> Login successful!")
        return True
    else:
        print("  -> Login failed: Invalid username or password.")
        return False
