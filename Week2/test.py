# Global variable to store student objects
student_list = []


class Student:

    # Function to set student data
    def set_data(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id

    # Function to display student info
    def display_info(self):
        return f"Name: {self.name}, Age: {self.name}"


# Function to collect student data
def collect_students():
    print("Enter details for at least 3 students:\n")

    for i in range(3):
        print(f"Student {i+1}")

        # Local variables
        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        student_id = input("Enter student ID: ")

        student = Student()

        # Set data using class function
        student.set_data(name, age, student_id)

        # Add student to global list
        student_list.append(student)

        print()


# Function to display students in order
def display_students():
    print("\nList of Students (Names and Ages):")

    # Sort students by name
    sorted_students = sorted(student_list, key=lambda s: s.age)

    for student in sorted_students:
        print(student.display_info())


# Standard Python entry point as main function
if __name__ == "__main__":
    collect_students()
    display_students()