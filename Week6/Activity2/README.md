# Zoo Application - Admin Login System

A simple command-line login system for a Zoo Application's admin user.
Built for **MSE800 Week 6 - Activity 2**.

## Project Structure

```
Activity2/
├── main.py          # Entry point - handles user input & displays result
├── auth.py          # Authentication logic (admin_login function)
├── decorators.py    # Defines the @log_admin_activity decorator
└── README.md        # This file
```

## How It Works

1. `main.py` prompts the user for a username and password.
2. `auth.admin_login()` is called to verify the credentials.
3. The `@log_admin_activity` decorator from `decorators.py` automatically logs
   every login attempt with the function name and current timestamp.
4. The result ("Access Granted" or "Access Denied") is displayed.

## Default Credentials

| Field    | Value      |
|----------|------------|
| Username | `admin`    |
| Password | `zoo2026`  |

## Decorator Implementation

The `@log_admin_activity` decorator in `decorators.py` wraps the
`admin_login` function. Each time `admin_login` is called, the decorator:

- Prints a log header with the function name and current timestamp
- Executes the original `admin_login` function
- Prints a footer and returns the original result unchanged

```python
def log_admin_activity(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  Function  : {func.__name__}")
        print(f"  Timestamp : {datetime.now()}")
        result = func(*args, **kwargs)
        print("  Function execution finished.")
        return result
    return wrapper
```

## How to Run

```bash
cd MSE800/Week6/Activity2
python main.py
```

## Sample Output

```
--- Welcome to the Zoo Management System ---
Enter username: admin
Enter password: zoo2026
----------------------------------------
  Admin Activity Log
  Function  : admin_login
  Timestamp : 2026-05-17 09:10:00
----------------------------------------
  -> Login successful!
  Function execution finished.
----------------------------------------

Access Granted. Welcome, Admin!
```

## Requirements Met

- [x] Zoo Application login system
- [x] Admin user authentication
- [x] At least one decorator (`@log_admin_activity`)
- [x] Clean modular structure (3 files)
