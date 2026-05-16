# Define the three student dictionaries
student1 = {
    "name": "Alex",
    "age": 42,
    "course": "Data Analytics",
    "city": "Auckland",
    "status": "Lecturer"
}

student2 = {
    "name": "Sophia",
    "age": 29,
    "course": "Software Engineering",
    "city": "Wellington",
    "status": "Student"
}

student3 = {
    "name": "Michael",
    "age": 35,
    "course": "Cyber Security",
    "city": "Christchurch",
    "status": "Researcher"
}

# Function to merge dictionaries with condition: name contains "azw" (case-insensitive)
def merge_students_with_azw(*students):
    merged = []
    for student in students:
        # Convert name to lowercase for case-insensitive check
        if "azw" in student["name"].lower():
            merged.append(student)
    return merged

# Execute the function
final_result = merge_students_with_azw(student1, student2, student3)

# Print the result clearly (matches the "**" requirement in the question)
print("** Merged Result (students with 'azw' in name): **")
print(final_result)