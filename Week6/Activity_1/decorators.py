from datetime import datetime



def log_activity(func):

    def wrapper(*args, **kwargs):
        print("===================================")
        print(f"Function: {func.__name__}")
        print(f"Time: {datetime.now()}")
        print("Activity started...")

        result = func(*args, **kwargs)

        print("Activity completed.")
        print("===================================\n")

        return result

    return wrapper
