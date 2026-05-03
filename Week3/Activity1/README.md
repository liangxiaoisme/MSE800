# Database Design for Student Enrollment System

## Project Overview

This repository contains the database design for a university student enrollment system. The goal is to design a normalized relational schema that manages students, courses, lecturers, and enrollment records.

## Core Entities and Attributes

1. **Student**: `Student_id (PK)`, `Student_name`
2. **Course**: `Course_id (PK)`, `Course_name`
3. **Lecturer**: `Lecturer_id (PK)`, `Lecturer_name`, `Lecturer_department`, `Lecturer_email`, `Course_id (FK)`
4. **Enrollment**: `Enrollment_date (PK)`, `Student_id (FK)`, `Course_id (FK)`

## Database Relationships

### 1. Many-to-Many (M:N): Students ↔ Courses
A student can enroll in many courses, and a course can have many students. Resolved by the `Enrollment` junction table, which holds both `Student_id` and `Course_id` as foreign keys.

### 2. One-to-Many (1:N): Course → Lecturer
One course is assigned to one lecturer, but a lecturer can teach multiple courses. `Course_id` is stored as a FK in the `Lecturer` table.

## Conclusion

Foreign keys are placed on the "Many" side of each relationship, keeping the schema clean and free of redundancy — making it easy to query and maintain.
