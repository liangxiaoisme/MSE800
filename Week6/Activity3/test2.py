# Define the student dictionaries
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

# Merge dictionaries with condition: name contains "ex"
merged_student = {
    **{k: v for k, v in student1.items() if "ex" in student1["name"]},
    **{k: v for k, v in student2.items() if "ex" in student2["name"]},
    **{k: v for k, v in student3.items() if "ex" in student3["name"]}
}

# Print the final result with ** format
print("**Merged Result:**")
print(merged_student)