def merge_student_dicts():
    # Define student dictionaries
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

    # Merge dictionaries: filter name contains substring "ex" (case insensitive)
    merged_result = {
        **{key: value for key, value in student1.items() if "ex" in student1["name"].lower()},
        **{key: value for key, value in student2.items() if "ex" in student2["name"].lower()},
        **{key: value for key, value in student3.items() if "ex" in student3["name"].lower()}
    }
    return merged_result


# Main program entry
if __name__ == "__main__":
    final_data = merge_student_dicts()
    # Print full merged result
    print("**Full Merged Dictionary Result:**")
    print(final_data)
    # Print only student name
    print("\n**Extracted Student Name:**")
    print(final_data["name"])