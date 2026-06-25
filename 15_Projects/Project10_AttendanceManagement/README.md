# 📋 Project 10: Attendance Management System

**Author:** Pavan Shetty H S
**Built:** October 2024 (the capstone project of this repository)

---

## Project Overview

The final and most "complete" project in this repository. I deliberately
tried to apply a bit of everything from across all 14 modules here: OOP
design, SQLite with proper relational constraints (including a UNIQUE
constraint to prevent double-marking attendance), custom exception
hierarchies, date handling, bulk operations with partial-failure
handling, CSV export, and percentage-based reporting logic. This felt
like a genuine capstone rather than just "one more CRUD app" — the kind
of project where earlier lessons from the whole repository actually got
combined together.

## Features

- Add students with branch tracking
- Mark attendance for individual students (Present/Absent)
- **Bulk attendance marking** for multiple students at once, with
  partial-success handling (one bad student ID doesn't abort the whole
  batch — a lesson learned directly from testing with a typo mid-batch)
- Duplicate attendance prevention (can't mark the same student twice on
  the same date — enforced at the database level via UNIQUE constraint)
- Individual student attendance history with percentage calculation
- Daily class-wide summary (Present/Absent counts)
- Defaulters list — students below 75% attendance threshold
- Full CSV report export with per-student statistics

## Folder Structure

```
Project10_AttendanceManagement/
├── attendance_management.py
├── attendance.db
├── README.md
└── requirements.txt
```

## Flowchart

```
   Bulk Attendance Flow:
   ┌─────────┐
   │  Start    │
   └────┬─────┘
        │
  ┌─────▼──────────────┐
  │ For each student_id:  │
  └─────┬──────────────┘
        │
  ┌─────▼──────────┐
  │ Try mark_attendance│
  └──┬──────────┬───┘
     │success    │ fails (not found / duplicate)
┌────▼────┐ ┌────▼─────────┐
│ Add to    │ │ Add to failed │
│ success    │ │ list w/ reason  │
│ list        │ └────┬─────────┘
└────┬────┘      │
     └─────┬──────┘
           │ (continue loop, don't abort)
     ┌─────▼──────┐
     │ Return both   │
     │ success+failed │
     │ lists           │
     └─────┬──────┘
           │
      ┌────▼────┐
      │   End    │
      └─────────┘
```

## Class Diagram

```
┌──────────────────────────────────┐
│          AttendanceSystem               │
├──────────────────────────────────┤
│ - connection, cursor                       │
├──────────────────────────────────┤
│ + add_student(id, name, branch)               │
│ + mark_attendance(id, status, date)             │
│ + mark_bulk_attendance(ids, status, date)         │
│ + get_student_attendance(id)                       │
│ + attendance_percentage(id)                          │
│ + class_summary(date)                                  │
│ + defaulters_list(threshold)                              │
│ + export_report_csv(filepath)                                │
└──────────────────────────────────┘

Exception Hierarchy:
  AttendanceError (base)
  ├── StudentNotFoundError
  └── DuplicateAttendanceError

Database Constraint:
  UNIQUE(student_id, date) -- enforces one attendance record
  per student per day at the DATABASE level, not just application logic
```

## Algorithm

**Attendance Percentage Calculation:**
1. Fetch all attendance records for a student, ordered by date
2. Count records where status = 'Present'
3. Percentage = (present_count / total_records) × 100, rounded to 2 decimals
4. Students with zero records return 0.0% (avoids division by zero)

**Defaulters Detection:**
1. Iterate every student in the system
2. Calculate each student's attendance percentage
3. Flag any student below the threshold (default 75%, a common
   real-world academic requirement)

## Requirements

```
# No external packages required -- uses sqlite3, datetime, csv (all built-in)
```

## Installation Steps

```bash
cd 15_Projects/Project10_AttendanceManagement
python attendance_management.py
```

## Sample Inputs & Outputs

```
==========================================
      ATTENDANCE MANAGEMENT SYSTEM
==========================================
 1. Add Student
 2. Mark Attendance (Single)
 3. Mark Attendance (Bulk)
 4. View Student Attendance
 5. Class Summary (Today)
 6. Defaulters List (<75%)
 7. Export Report to CSV
 8. Exit

Enter Choice: 1
Student ID: 1
Name: Pavan Shetty H S
Branch: ECE

✓ Student Pavan Shetty H S added

Enter Choice: 3
Student IDs (comma-separated): 1, 2, 3
Status (Present/Absent): Present

✓ Marked 1 student(s) successfully
✗ 2 failed:
    Student 2: Student 2 not found
    Student 3: Student 3 not found

Enter Choice: 2
Student ID: 1
Status (Present/Absent): Present

✗ DuplicateAttendanceError: Attendance for student 1 on 2024-10-12 already marked

Enter Choice: 4
Student ID: 1

  Attendance records (1 total):
    2024-10-12  ✓ Present

  Overall Attendance: 100.0%

Enter Choice: 6

✓ No defaulters! Everyone is above 75%.
```

## Screenshots

> See `/Images/Screenshots/project10_*.png`:
> - `project10_menu.png`
> - `project10_bulk_partial_failure.png` — shows graceful handling of
>   mixed success/failure in bulk marking
> - `project10_duplicate_error.png`
> - `project10_student_history.png`
> - `project10_defaulters_list.png`
> - `project10_csv_export.png`

## Learning Outcomes

- Designed a real UNIQUE database constraint to enforce a business rule
  (one attendance record per student per day) at the data layer, not
  just hoping application code remembers to check
- Built genuinely useful partial-failure handling for bulk operations —
  a typo'd student ID in the middle of a batch shouldn't silently abort
  everyone else's attendance from being recorded
- Combined nearly every module's concepts into one cohesive capstone:
  OOP structure, custom exceptions, SQLite relational design, date
  handling, CSV export, and percentage-based business reporting
- Genuinely satisfying to finish this repository's project section with
  something that feels like a complete, real, deployable mini-application

## Future Enhancements

- [ ] QR-code or biometric check-in integration (connects to my
      embedded systems interest — Arduino/ESP32 could feed attendance
      events into this system via the REST API patterns from Module 12)
- [ ] Monthly/semester-wide attendance trend charts
- [ ] Automated low-attendance email alerts (Module 12 EmailAutomation.py)
- [ ] Web-based dashboard instead of CLI

---

## Closing note on this repository

This project marks the end of roughly 9 months of consistent Python
learning, documented module by module, mistake by mistake, in this
repository. Looking back at `01_Python_Basics/HelloWorld.py` after
building this attendance system feels like looking at a completely
different skill level — which is exactly the point of keeping all of it
here instead of cleaning up and hiding the early, rough work.

— Pavan Shetty H S
