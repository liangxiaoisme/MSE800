from decorators import log_activity


@log_activity
def student_login(username):
    print(f"{username} logged into the system.")


@log_activity
def submit_assignment(username, assignment):
    print(f"{username} submitted {assignment}.")


@log_activity
def view_grades(username):
    print(f"{username} is viewing grades.")
