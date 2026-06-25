# =============================================================================
# attendance_management.py
# Project : 10 - Attendance Management System
# Author  : Pavan Shetty H S
# Date    : October 2024
# =============================================================================
#
# Notes from Pavan:
# The final project of this repository, and deliberately the most
# "complete" one -- I tried to use a bit of everything I learned across
# all 14 modules here: OOP, SQLite with proper relational design,
# exception hierarchies, date handling, CSV export, and percentage-based
# reporting logic. This felt like a genuine capstone rather than just
# "one more CRUD app."
# =============================================================================

import sqlite3
import os
import datetime
import csv

DB_PATH = os.path.join(os.path.dirname(__file__), "attendance.db")


class AttendanceError(Exception):
    pass

class StudentNotFoundError(AttendanceError):
    pass

class DuplicateAttendanceError(AttendanceError):
    pass


class AttendanceSystem:
    def __init__(self, db_path=DB_PATH):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                branch TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                UNIQUE(student_id, date)
            )
        """)
        self.connection.commit()

    def add_student(self, student_id, name, branch):
        self.cursor.execute(
            "INSERT INTO students (student_id, name, branch) VALUES (?, ?, ?)",
            (student_id, name, branch)
        )
        self.connection.commit()

    def mark_attendance(self, student_id, status, date=None):
        if date is None:
            date = str(datetime.date.today())

        self.cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        if not self.cursor.fetchone():
            raise StudentNotFoundError(f"Student {student_id} not found")

        try:
            self.cursor.execute(
                "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                (student_id, date, status)
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise DuplicateAttendanceError(
                f"Attendance for student {student_id} on {date} already marked"
            )

    def mark_bulk_attendance(self, student_ids, status, date=None):
        """Mark the same status for multiple students at once (e.g. a
        whole class marked Present for a guest lecture). Tracks failures
        separately instead of letting one bad student_id abort the rest --
        this exact 'partial success' handling is something I didn't think
        about until testing with a typo'd student ID in the middle of a
        batch and watching the whole operation fail."""
        results = {"success": [], "failed": []}
        for sid in student_ids:
            try:
                self.mark_attendance(sid, status, date)
                results["success"].append(sid)
            except AttendanceError as e:
                results["failed"].append((sid, str(e)))
        return results

    def get_student_attendance(self, student_id):
        self.cursor.execute(
            "SELECT date, status FROM attendance WHERE student_id = ? ORDER BY date",
            (student_id,)
        )
        return self.cursor.fetchall()

    def attendance_percentage(self, student_id):
        records = self.get_student_attendance(student_id)
        if not records:
            return 0.0
        present_count = sum(1 for r in records if r[1] == "Present")
        return round((present_count / len(records)) * 100, 2)

    def class_summary(self, date=None):
        if date is None:
            date = str(datetime.date.today())
        self.cursor.execute(
            "SELECT status, COUNT(*) FROM attendance WHERE date = ? GROUP BY status",
            (date,)
        )
        return dict(self.cursor.fetchall())

    def defaulters_list(self, threshold=75):
        """Students below the attendance threshold -- the report every
        student dreads, and the report every department actually needs."""
        self.cursor.execute("SELECT student_id, name FROM students")
        all_students = self.cursor.fetchall()
        defaulters = []
        for sid, name in all_students:
            pct = self.attendance_percentage(sid)
            if pct < threshold:
                defaulters.append((sid, name, pct))
        return defaulters

    def export_report_csv(self, filepath):
        self.cursor.execute("SELECT student_id, name, branch FROM students")
        students = self.cursor.fetchall()

        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Student ID", "Name", "Branch", "Total Days", "Present", "Attendance %"])
            for sid, name, branch in students:
                records = self.get_student_attendance(sid)
                present = sum(1 for r in records if r[1] == "Present")
                pct = self.attendance_percentage(sid)
                writer.writerow([sid, name, branch, len(records), present, pct])
        return filepath

    def close(self):
        self.connection.close()


def print_menu():
    print("\n" + "=" * 42)
    print("      ATTENDANCE MANAGEMENT SYSTEM")
    print("=" * 42)
    print(" 1. Add Student")
    print(" 2. Mark Attendance (Single)")
    print(" 3. Mark Attendance (Bulk)")
    print(" 4. View Student Attendance")
    print(" 5. Class Summary (Today)")
    print(" 6. Defaulters List (<75%)")
    print(" 7. Export Report to CSV")
    print(" 8. Exit")


def main():
    sys_ = AttendanceSystem()
    while True:
        print_menu()
        choice = input("\nEnter Choice: ").strip()
        try:
            if choice == "1":
                sid = int(input("Student ID: "))
                name = input("Name: ")
                branch = input("Branch: ")
                sys_.add_student(sid, name, branch)
                print(f"\n✓ Student {name} added")

            elif choice == "2":
                sid = int(input("Student ID: "))
                status = input("Status (Present/Absent): ").strip().capitalize()
                sys_.mark_attendance(sid, status)
                print(f"\n✓ Attendance marked: {status}")

            elif choice == "3":
                ids_input = input("Student IDs (comma-separated): ")
                student_ids = [int(x.strip()) for x in ids_input.split(",")]
                status = input("Status (Present/Absent): ").strip().capitalize()
                results = sys_.mark_bulk_attendance(student_ids, status)
                print(f"\n✓ Marked {len(results['success'])} student(s) successfully")
                if results["failed"]:
                    print(f"✗ {len(results['failed'])} failed:")
                    for sid, reason in results["failed"]:
                        print(f"    Student {sid}: {reason}")

            elif choice == "4":
                sid = int(input("Student ID: "))
                records = sys_.get_student_attendance(sid)
                pct = sys_.attendance_percentage(sid)
                print(f"\n  Attendance records ({len(records)} total):")
                for date, status in records:
                    marker = "✓" if status == "Present" else "✗"
                    print(f"    {date}  {marker} {status}")
                print(f"\n  Overall Attendance: {pct}%")
                if pct < 75:
                    print("  ⚠ WARNING: Below 75% attendance threshold!")

            elif choice == "5":
                summary = sys_.class_summary()
                print(f"\n  Today's Summary:")
                print(f"    Present: {summary.get('Present', 0)}")
                print(f"    Absent : {summary.get('Absent', 0)}")

            elif choice == "6":
                defaulters = sys_.defaulters_list()
                if defaulters:
                    print(f"\n⚠ {len(defaulters)} student(s) below 75% attendance:")
                    for sid, name, pct in defaulters:
                        print(f"    [{sid}] {name}: {pct}%")
                else:
                    print("\n✓ No defaulters! Everyone is above 75%.")

            elif choice == "7":
                filename = input("Export filename (e.g. attendance_report.csv): ") or "attendance_report.csv"
                path = sys_.export_report_csv(filename)
                print(f"\n✓ Report exported to {path}")

            elif choice == "8":
                print("\nAttendance session closed. Goodbye!")
                sys_.close()
                break
            else:
                print("✗ Invalid choice.")
        except AttendanceError as e:
            print(f"\n✗ {type(e).__name__}: {e}")
        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")


if __name__ == "__main__":
    main()

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 attendance_management.py
# =============================================================================
#
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: Student ID: Name: Branch: 
# ✓ Student Pavan Shetty H S added
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: Student ID: Name: Branch: 
# ✓ Student Rahul Kumar added
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: Student ID: Name: Branch: 
# ✓ Student Priya Singh added
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: Student ID: Status (Present/Absent): 
# ✓ Attendance marked: Present
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: Student ID: Status (Present/Absent): 
# ✓ Attendance marked: Absent
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: Student IDs (comma-separated): Status (Present/Absent): 
# ✓ Marked 1 student(s) successfully
# ✗ 2 failed:
#     Student 22001: Attendance for student 22001 on 2026-06-21 already marked
#     Student 22999: Student 22999 not found
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: Student ID: 
#   Attendance records (1 total):
#     2026-06-21  ✓ Present
#
#   Overall Attendance: 100.0%
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: Student ID: 
#   Attendance records (1 total):
#     2026-06-21  ✗ Absent
#
#   Overall Attendance: 0.0%
#   ⚠ WARNING: Below 75% attendance threshold!
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: 
#   Today's Summary:
#     Present: 2
#     Absent : 1
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: 
# ⚠ 1 student(s) below 75% attendance:
#     [22002] Rahul Kumar: 0.0%
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: Export filename (e.g. attendance_report.csv): 
# ✓ Report exported to attendance_report.csv
#
# ==========================================
#       ATTENDANCE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Student
#  2. Mark Attendance (Single)
#  3. Mark Attendance (Bulk)
#  4. View Student Attendance
#  5. Class Summary (Today)
#  6. Defaulters List (<75%)
#  7. Export Report to CSV
#  8. Exit
#
# Enter Choice: 
# Attendance session closed. Goodbye!
#
# =============================================================================

