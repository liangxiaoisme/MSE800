class student_info:
    def get_info(self):
        self.name = input("Enter student name: ")
        self.age = input("Enter student age: ")
        self.student_id = input("Enter student ID: ")

    def show_info(self):
        print(f'Name: {self.name}, Age: {self.age}, Student ID: {self.student_id}')


def main():

    student_list = []

    for i in range(3):
        print(f"\n---- The student information of No {i + 1} ----")
        student = student_info()
        student.get_info()
        student_list.append(student)
    
    print ('\n---- The student information of all students ----')
    for student in student_list:
        student.show_info()

if __name__ == "__main__":
    main()