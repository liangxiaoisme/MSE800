from users import (
    student_login,
    submit_assignment,
    view_grades
)


def main():

    student_login("Mohammad")

    submit_assignment(
        "Mohammad",
        "Python Decorator Project"
    )

    view_grades("Alex")


if __name__ == "__main__":
    main()
