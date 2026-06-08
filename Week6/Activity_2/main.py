# -*- coding: utf-8 -*-
"""
main.py - Entry point for the Zoo Application admin login system.
Run this file to start the program.
"""

from auth import admin_login


def main():
    """Prompt user for credentials and authenticate."""
    print("--- Welcome to the Zoo Management System ---")

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    is_logged_in = admin_login(username, password)

    print()
    if is_logged_in:
        print("Access Granted. Welcome, Admin!")
    else:
        print("Access Denied. Please try again.")


if __name__ == "__main__":
    main()
