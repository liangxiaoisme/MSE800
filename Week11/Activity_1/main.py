"""Console UI entry point.

Handles only the menu and input/output; all business logic is delegated
to the auth module. Keeping this layer free of business rules means the
UI can be swapped (console -> web -> GUI) without touching auth.
"""

import sys
from getpass import getpass

import auth


def _input(label: str) -> str:
    """Read a line of trimmed text input."""
    return input(label).strip()


def _password(label: str) -> str:
    """Read a password, hiding it on a real terminal.

    getpass reads directly from the terminal and hides typing. In a
    non-interactive environment (e.g. VSCode's "Run" Output panel, the
    debug console, or piped input) there is no real terminal and getpass
    would block forever, so we detect that and fall back to plain input().
    """
    if sys.stdin.isatty():
        return getpass(label)
    return input(label)


def _header(title: str) -> None:
    """Print a framed section header."""
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)


def handle_register() -> None:
    """Collect registration data and call the auth service."""
    _header("Register New Account")
    email = _input("Email: ")
    username = _input("Username (3-20 chars): ")
    full_name = _input("Full name: ")
    dob = _input("Date of birth (YYYY-MM-DD): ")
    print("(Note: the password is hidden while typing — just type and press Enter.)")
    password = _password("Password (>=8 chars, letters + digits): ")
    ok, msg = auth.register(email, username, full_name, dob, password)
    print(f"\n{'[OK]' if ok else '[ERROR]'} {msg}")


def handle_login() -> None:
    """Prompt for credentials and show the profile on success."""
    _header("Login")
    email = _input("Email: ")
    print("(Note: the password is hidden while typing — just type and press Enter.)")
    password = _password("Password: ")
    ok, msg, user = auth.login(email, password)
    print(f"\n{'[OK]' if ok else '[ERROR]'} {msg}")
    if ok and user:
        _header("Your Profile")
        print(f"Email        : {user.email}")
        print(f"Username     : {user.username}")
        print(f"Full name    : {user.full_name}")
        print(f"Date of birth: {user.dob}")


def handle_forgot_password() -> None:
    """Send a reset code (simulated email) and reset the password."""
    _header("Forgot Password")
    email = _input("Email: ")
    msg, email_body = auth.request_reset_code(email)
    print(f"\n[System] {msg}")
    if email_body:
        # The simulated email the user would receive
        print("\n" + "-" * 40)
        print(email_body)
        print("-" * 40)
    code = _input("\nEnter reset code: ")
    new_password = _password("Enter new password: ")
    ok, result = auth.reset_password(email, code, new_password)
    print(f"\n{'[OK]' if ok else '[ERROR]'} {result}")


def main() -> None:
    """Run the top-level menu loop."""
    actions = {
        "1": ("Register", handle_register),
        "2": ("Login", handle_login),
        "3": ("Forgot password", handle_forgot_password),
        "4": ("Exit", None),
    }
    while True:
        _header("User Account Management")
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")
        choice = _input("\nChoose an option: ")

        if choice == "4":
            print("Goodbye.")
            return
        action = actions.get(choice)
        if action is None:
            print("[ERROR] Invalid choice. Please pick 1-4.")
            continue
        action[1]()  # each handler manages its own prompts and feedback


if __name__ == "__main__":
    main()
