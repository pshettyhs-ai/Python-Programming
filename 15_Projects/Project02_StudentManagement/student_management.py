# =============================================================================
# student_management.py
# Project : 02 - Student Management System
# Author  : Pavan Shetty H S
# Date    : August 2024
# =============================================================================
#
# Notes from Pavan:
# This was my first project using SQLite (Module 11 concepts applied for
# real). First draft used a JSON file for storage, which worked fine for
# small datasets but I rewrote it to use SQLite once I realized I wanted
# searching/filtering capability that a flat file made awkward. Keeping
# this rewrite as a lesson in choosing the right persistence layer for
# the job.
# =============================================================================

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "students.db")


class StudentManagementSystem:
    def __init__(self, db_path=DB_PATH):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                branch TEXT NOT NULL,
                semester INTEGER,
                cgpa REAL CHECK(cgpa >= 0 AND cgpa <= 10),
                phone TEXT,
                email TEXT UNIQUE
            )
        """)
        self.connection.commit()

    def add_student(self, student_id, name, branch, semester, cgpa, phone, email):
        try:
            self.cursor.execute(
                """INSERT INTO students (student_id, name, branch, semester, cgpa, phone, email)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (student_id, name, branch, semester, cgpa, phone, email)
            )
            self.connection.commit()
            return True, "Student Added Successfully."
        except sqlite3.IntegrityError as e:
            return False, f"Error: {e} (Student ID or email might already exist)"

    def search_student(self, student_id):
        self.cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        return self.cursor.fetchone()

    def search_by_name(self, name):
        self.cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{name}%",))
        return self.cursor.fetchall()

    def update_student(self, student_id, field, new_value):
        valid_fields = {"name", "branch", "semester", "cgpa", "phone", "email"}
        if field not in valid_fields:
            return False, f"Invalid field '{field}'"
        # NOTE: f-string used here ONLY for the column NAME (not user data),
        # which is safe since we validate against valid_fields above.
        # The actual VALUE still goes through a parameterized query.
        query = f"UPDATE students SET {field} = ? WHERE student_id = ?"
        self.cursor.execute(query, (new_value, student_id))
        self.connection.commit()
        if self.cursor.rowcount == 0:
            return False, "Student not found."
        return True, "Student Updated Successfully."

    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        self.connection.commit()
        if self.cursor.rowcount == 0:
            return False, "Student not found."
        return True, "Student Deleted Successfully."

    def view_all_students(self):
        self.cursor.execute("SELECT * FROM students ORDER BY student_id")
        return self.cursor.fetchall()

    def generate_report(self):
        self.cursor.execute("SELECT COUNT(*), AVG(cgpa), MAX(cgpa), MIN(cgpa) FROM students")
        count, avg_cgpa, max_cgpa, min_cgpa = self.cursor.fetchone()
        return {
            "total_students": count,
            "average_cgpa": round(avg_cgpa, 2) if avg_cgpa else 0,
            "highest_cgpa": max_cgpa,
            "lowest_cgpa": min_cgpa
        }

    def close(self):
        self.connection.close()


def print_header():
    print("\n" + "=" * 42)
    print("     STUDENT MANAGEMENT SYSTEM v2.0")
    print("     Developed by: Pavan Shetty H S")
    print("=" * 42)


def print_menu():
    print("\n 1. Add New Student")
    print(" 2. Search Student")
    print(" 3. Update Student Details")
    print(" 4. Delete Student Record")
    print(" 5. View All Students")
    print(" 6. Generate Report")
    print(" 7. Exit")


def main():
    sms = StudentManagementSystem()
    print_header()

    while True:
        print_menu()
        choice = input("\nEnter Choice: ").strip()

        if choice == "1":
            print("\n----- ADD NEW STUDENT -----")
            try:
                sid = int(input("Student ID   : "))
                name = input("Name         : ")
                branch = input("Branch       : ")
                semester = int(input("Semester     : "))
                cgpa = float(input("CGPA         : "))
                phone = input("Phone        : ")
                email = input("Email        : ")
                success, message = sms.add_student(sid, name, branch, semester, cgpa, phone, email)
                print(f"\n{'✓' if success else '✗'} {message}")
                if success:
                    print(f"  ID: {sid} | Name: {name} | Branch: {branch}")
            except ValueError:
                print("✗ Invalid input. Please enter correct data types.")

        elif choice == "2":
            print("\n----- SEARCH STUDENT -----")
            search_type = input("Search by (1) ID or (2) Name? ").strip()
            if search_type == "1":
                sid = int(input("Enter Student ID: "))
                result = sms.search_student(sid)
                if result:
                    print(f"\n  Found: {result}")
                else:
                    print("\n  ✗ No student found with that ID.")
            else:
                name = input("Enter name (partial match OK): ")
                results = sms.search_by_name(name)
                if results:
                    print(f"\n  Found {len(results)} match(es):")
                    for r in results:
                        print(f"    {r}")
                else:
                    print("\n  ✗ No matches found.")

        elif choice == "3":
            print("\n----- UPDATE STUDENT -----")
            sid = int(input("Enter Student ID to update: "))
            field = input("Field to update (name/branch/semester/cgpa/phone/email): ").strip()
            new_value = input("New value: ")
            success, message = sms.update_student(sid, field, new_value)
            print(f"\n{'✓' if success else '✗'} {message}")

        elif choice == "4":
            print("\n----- DELETE STUDENT -----")
            sid = int(input("Enter Student ID to delete: "))
            confirm = input(f"Are you sure you want to delete student {sid}? (y/n): ")
            if confirm.lower() == "y":
                success, message = sms.delete_student(sid)
                print(f"\n{'✓' if success else '✗'} {message}")
            else:
                print("  Deletion cancelled.")

        elif choice == "5":
            print("\n----- ALL STUDENTS -----")
            students = sms.view_all_students()
            if students:
                print(f"\n  {'ID':6}{'Name':20}{'Branch':15}{'Sem':5}{'CGPA':6}")
                print("  " + "-" * 55)
                for s in students:
                    print(f"  {s[0]:<6}{s[1]:<20}{s[2]:<15}{s[3]:<5}{s[4]:<6}")
            else:
                print("  No students in database.")

        elif choice == "6":
            print("\n----- REPORT -----")
            report = sms.generate_report()
            print(f"  Total Students : {report['total_students']}")
            print(f"  Average CGPA   : {report['average_cgpa']}")
            print(f"  Highest CGPA   : {report['highest_cgpa']}")
            print(f"  Lowest CGPA    : {report['lowest_cgpa']}")

        elif choice == "7":
            print("\nThank you for using Student Management System!")
            sms.close()
            break

        else:
            print("✗ Invalid choice. Please select 1-7.")


if __name__ == "__main__":
    main()

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 student_management.py
# =============================================================================
#
#
# ==========================================
#      STUDENT MANAGEMENT SYSTEM v2.0
#      Developed by: Pavan Shetty H S
# ==========================================
#
#  1. Add New Student
#  2. Search Student
#  3. Update Student Details
#  4. Delete Student Record
#  5. View All Students
#  6. Generate Report
#  7. Exit
#
# Enter Choice: 
# ----- ADD NEW STUDENT -----
# Student ID   : Name         : Branch       : Semester     : CGPA         : Phone        : Email        : 
# ✓ Student Added Successfully.
#   ID: 1 | Name: Pavan Shetty H S | Branch: CSE
#
#  1. Add New Student
#  2. Search Student
#  3. Update Student Details
#  4. Delete Student Record
#  5. View All Students
#  6. Generate Report
#  7. Exit
#
# Enter Choice: 
# ----- ADD NEW STUDENT -----
# Student ID   : Name         : Branch       : Semester     : CGPA         : Phone        : Email        : 
# ✓ Student Added Successfully.
#   ID: 2 | Name: Rahul Kumar | Branch: ECE
#
#  1. Add New Student
#  2. Search Student
#  3. Update Student Details
#  4. Delete Student Record
#  5. View All Students
#  6. Generate Report
#  7. Exit
#
# Enter Choice: 
# ----- ADD NEW STUDENT -----
# Student ID   : Name         : Branch       : Semester     : CGPA         : Phone        : Email        : 
# ✓ Student Added Successfully.
#   ID: 3 | Name: Priya Singh | Branch: CSE
#
#  1. Add New Student
#  2. Search Student
#  3. Update Student Details
#  4. Delete Student Record
#  5. View All Students
#  6. Generate Report
#  7. Exit
#
# Enter Choice: 
# ----- ALL STUDENTS -----
#
#   ID    Name                Branch         Sem  CGPA  
#   -------------------------------------------------------
#   1     Pavan Shetty H S    CSE            5    8.9   
#   2     Rahul Kumar         ECE            5    7.5   
#   3     Priya Singh         CSE            5    9.2   
#
#  1. Add New Student
#  2. Search Student
#  3. Update Student Details
#  4. Delete Student Record
#  5. View All Students
#  6. Generate Report
#  7. Exit
#
# Enter Choice: 
# ----- SEARCH STUDENT -----
# Search by (1) ID or (2) Name? Enter Student ID: 
#   Found: (1, 'Pavan Shetty H S', 'CSE', 5, 8.9, '9876543210', 'pavan@uni.edu')
#
#  1. Add New Student
#  2. Search Student
#  3. Update Student Details
#  4. Delete Student Record
#  5. View All Students
#  6. Generate Report
#  7. Exit
#
# Enter Choice: 
# ----- SEARCH STUDENT -----
# Search by (1) ID or (2) Name? Enter name (partial match OK): 
#   Found 1 match(es):
#     (3, 'Priya Singh', 'CSE', 5, 9.2, '9876543212', 'priya@uni.edu')
#
#  1. Add New Student
#  2. Search Student
#  3. Update Student Details
#  4. Delete Student Record
#  5. View All Students
#  6. Generate Report
#  7. Exit
#
# Enter Choice: 
# ----- UPDATE STUDENT -----
# Enter Student ID to update: Field to update (name/branch/semester/cgpa/phone/email): New value: 
# ✓ Student Updated Successfully.
#
#  1. Add New Student
#  2. Search Student
#  3. Update Student Details
#  4. Delete Student Record
#  5. View All Students
#  6. Generate Report
#  7. Exit
#
# Enter Choice: 
# ----- DELETE STUDENT -----
# Enter Student ID to delete: Are you sure you want to delete student 3? (y/n): 
# ✓ Student Deleted Successfully.
#
#  1. Add New Student
#  2. Search Student
#  3. Update Student Details
#  4. Delete Student Record
#  5. View All Students
#  6. Generate Report
#  7. Exit
#
# Enter Choice: 
# ----- REPORT -----
#   Total Students : 2
#   Average CGPA   : 8.45
#   Highest CGPA   : 8.9
#   Lowest CGPA    : 8.0
#
#  1. Add New Student
#  2. Search Student
#  3. Update Student Details
#  4. Delete Student Record
#  5. View All Students
#  6. Generate Report
#  7. Exit
#
# Enter Choice: 
# ----- ALL STUDENTS -----
#
#   ID    Name                Branch         Sem  CGPA  
#   -------------------------------------------------------
#   1     Pavan Shetty H S    CSE            5    8.9   
#   2     Rahul Kumar         ECE            5    8.0   
#
#  1. Add New Student
#  2. Search Student
#  3. Update Student Details
#  4. Delete Student Record
#  5. View All Students
#  6. Generate Report
#  7. Exit
#
# Enter Choice: 
# Thank you for using Student Management System!
#
# =============================================================================

