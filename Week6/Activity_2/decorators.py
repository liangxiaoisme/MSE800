# -*- coding: utf-8 -*-
"""
decorators.py - Custom decorator for the Zoo Application login system.
"""

from datetime import datetime
from functools import wraps


def log_admin_activity(func):
    """Decorator: logs every admin login attempt with a timestamp."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("----------------------------------------")
        print("  Admin Activity Log")
        print("  Function  : " + func.__name__)
        print("  Timestamp : " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("----------------------------------------")

        result = func(*args, **kwargs)

        print("  Function execution finished.")
        print("----------------------------------------\n")
        return result

    return wrapper
