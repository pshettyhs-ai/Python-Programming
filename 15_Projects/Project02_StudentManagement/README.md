# 🎓 Project 2: Student Management System

**Author:** Pavan Shetty H S
**Built:** August 2024 (~4 days, including a full rewrite)

---

## Project Overview

A complete CRUD application for managing student records — add, search,
update, delete, view all, and generate summary reports. This is my
first project using SQLite as a real persistence layer instead of flat
files. The first draft actually used a JSON file for storage; I rewrote
it to use SQLite once I wanted searching/filtering capability that a
flat file made awkward to implement cleanly.

## Features

- Add new student records with validation
- Search by Student ID (exact) or Name (partial match using SQL LIKE)
- Update individual fields without rewriting the whole record
- Delete records with a confirmation prompt (learned this the hard way
  after an earlier version deleted without confirming — once)
- View all students in a formatted table
- Generate summary statistics report (count, average/max/min CGPA)
- Data persists between runs via SQLite database file

## Folder Structure

```
Project02_StudentManagement/
├── student_management.py   # Main application
├── students.db               # SQLite database (created on first run)
├── README.md
└── requirements.txt
```

## Flowchart

```
        ┌──────────┐
        │  Start    │
        └────┬─────┘
             │
      ┌──────▼──────┐
      │ Connect DB    │
      │ Create table   │
      │  if needed     │
      └──────┬──────┘
             │
      ┌──────▼──────┐
      │ Show Menu     │◄─────────────┐
      └──────┬──────┘                │
             │                        │
    ┌────────▼─────────┐             │
    │ Add/Search/Update/ │             │
    │ Delete/View/Report  │── loop ────┘
    └────────┬─────────┘
             │ Exit chosen
      ┌──────▼──────┐
      │ Close DB conn │
      └──────┬──────┘
             │
        ┌────▼────┐
        │   End    │
        └─────────┘
```

## Class Diagram

```
┌──────────────────────────────────────┐
│       StudentManagementSystem           │
├──────────────────────────────────────┤
│ - connection: sqlite3.Connection         │
│ - cursor: sqlite3.Cursor                 │
├──────────────────────────────────────┤
│ + add_student(...)                       │
│ + search_student(student_id)             │
│ + search_by_name(name)                   │
│ + update_student(id, field, value)       │
│ + delete_student(student_id)             │
│ + view_all_students()                    │
│ + generate_report()                      │
│ + close()                                │
│ - _create_table()                        │
└──────────────────────────────────────┘
```

## Algorithm

1. On startup, connect to (or create) `students.db` and ensure the
   `students` table exists
2. Display the main menu in a loop
3. Route user choice to the corresponding method
4. For Add: validate input types, insert via parameterized query,
   handle UNIQUE constraint violations gracefully
5. For Search: support both exact ID lookup and partial name matching
6. For Update: validate the target field name against an allow-list
   before building the query (prevents arbitrary column injection)
7. For Delete: require explicit confirmation before executing
8. On Exit: close the database connection cleanly

## Requirements

```
# No external packages required -- uses Python's built-in sqlite3 module
```

## Installation Steps

```bash
cd 15_Projects/Project02_StudentManagement
python student_management.py
```

## Execution Guide

```bash
python student_management.py
```

## Sample Inputs & Outputs

```
==========================================
     STUDENT MANAGEMENT SYSTEM v2.0
     Developed by: Pavan Shetty H S
==========================================

 1. Add New Student
 2. Search Student
 3. Update Student Details
 4. Delete Student Record
 5. View All Students
 6. Generate Report
 7. Exit

Enter Choice: 1

----- ADD NEW STUDENT -----
Student ID   : 1001
Name         : Rahul Kumar
Branch       : Computer Science
Semester     : 5
CGPA         : 8.7
Phone        : 9876543210
Email        : rahul@example.com

✓ Student Added Successfully.
  ID: 1001 | Name: Rahul Kumar | Branch: Computer Science

Enter Choice: 5

----- ALL STUDENTS -----

  ID    Name                Branch         Sem  CGPA
  -------------------------------------------------------
  1001  Rahul Kumar         Computer Science5    8.7

Enter Choice: 1

----- ADD NEW STUDENT -----
Student ID   : 1001
Name         : Duplicate Test
Branch       : ECE
Semester     : 3
CGPA         : 7.5
Phone        : 9876543211
Email        : dup@example.com

✗ Error: UNIQUE constraint failed: students.student_id (Student ID or email might already exist)

Enter Choice: 6

----- REPORT -----
  Total Students : 1
  Average CGPA   : 8.7
  Highest CGPA   : 8.7
  Lowest CGPA    : 8.7
```

## Screenshots

> See `/Images/Screenshots/project02_*.png`:
> - `project02_menu.png` — main menu
> - `project02_add_student.png` — successful add operation
> - `project02_duplicate_error.png` — UNIQUE constraint error handling
> - `project02_search.png` — search by name results
> - `project02_report.png` — generated report view

## Learning Outcomes

- First real application of SQLite CRUD operations from Module 11
- Learned to validate field names against an allow-list before building
  dynamic SQL (the update_student method) — prevents accidentally
  exposing arbitrary column manipulation
- Practiced handling `sqlite3.IntegrityError` gracefully instead of
  letting constraint violations crash the program
- Understood WHY I rewrote the JSON version to SQLite — flat files get
  awkward fast once you need filtering/searching beyond simple lookups

## Future Enhancements

- [ ] Export student list to CSV/PDF
- [ ] Add a GPA trend chart per student across semesters
- [ ] Multi-field search (branch + semester combined filters)
- [ ] Basic authentication before allowing delete operations
