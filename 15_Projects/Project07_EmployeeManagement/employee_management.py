# =============================================================================
# employee_management.py
# Project : 07 - Employee Management System
# Author  : Pavan Shetty H S
# Date    : September 2024
# =============================================================================
#
# Notes from Pavan:
# This is the project where I deliberately put Abstraction (Module 9) to
# the test. Employee is an abstract base class -- every subclass MUST
# implement calculate_bonus(). I actually forgot to implement it in
# Manager initially during development and Python refused to let me
# instantiate the class at all, catching my mistake immediately instead
# of failing later when bonus calculation was actually called. Kept that
# exact bug story in my OOP module notes because it was such a clean
# demonstration of WHY abstraction is useful, not just academic.
# =============================================================================

import sqlite3
import os
import csv
from abc import ABC, abstractmethod

DB_PATH = os.path.join(os.path.dirname(__file__), "employees.db")


class EmployeeError(Exception):
    pass

class EmployeeNotFoundError(EmployeeError):
    pass


class Employee(ABC):
    """Abstract base class -- every employee type MUST define how
    their bonus is calculated."""
    def __init__(self, emp_id, name, department, base_salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.base_salary = base_salary

    @abstractmethod
    def calculate_bonus(self):
        pass

    def total_compensation(self):
        return self.base_salary + self.calculate_bonus()

    @abstractmethod
    def role(self):
        pass


class Developer(Employee):
    def calculate_bonus(self):
        return self.base_salary * 0.10   # 10% bonus

    def role(self):
        return "Developer"


class Manager(Employee):
    def __init__(self, emp_id, name, department, base_salary, team_size):
        super().__init__(emp_id, name, department, base_salary)
        self.team_size = team_size

    def calculate_bonus(self):
        return self.base_salary * 0.15 + (self.team_size * 1000)

    def role(self):
        return "Manager"


class Intern(Employee):
    def calculate_bonus(self):
        return 0   # interns don't get a bonus in this model

    def role(self):
        return "Intern"


class EmployeeDatabase:
    def __init__(self, db_path=DB_PATH):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT,
                role TEXT NOT NULL,
                base_salary REAL NOT NULL,
                team_size INTEGER DEFAULT 0
            )
        """)
        self.connection.commit()

    def add_employee(self, employee):
        team_size = getattr(employee, "team_size", 0)
        self.cursor.execute(
            "INSERT INTO employees (emp_id, name, department, role, base_salary, team_size) VALUES (?, ?, ?, ?, ?, ?)",
            (employee.emp_id, employee.name, employee.department, employee.role(), employee.base_salary, team_size)
        )
        self.connection.commit()

    def get_employee(self, emp_id):
        self.cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
        row = self.cursor.fetchone()
        if not row:
            raise EmployeeNotFoundError(f"Employee {emp_id} not found")
        return self._row_to_object(row)

    def _row_to_object(self, row):
        emp_id, name, dept, role, salary, team_size = row
        if role == "Developer":
            return Developer(emp_id, name, dept, salary)
        elif role == "Manager":
            return Manager(emp_id, name, dept, salary, team_size)
        elif role == "Intern":
            return Intern(emp_id, name, dept, salary)
        raise EmployeeError(f"Unknown role: {role}")

    def view_all(self):
        self.cursor.execute("SELECT * FROM employees")
        return [self._row_to_object(row) for row in self.cursor.fetchall()]

    def update_salary(self, emp_id, new_salary):
        self.cursor.execute("UPDATE employees SET base_salary = ? WHERE emp_id = ?", (new_salary, emp_id))
        self.connection.commit()
        if self.cursor.rowcount == 0:
            raise EmployeeNotFoundError(f"Employee {emp_id} not found")

    def delete_employee(self, emp_id):
        self.cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
        self.connection.commit()
        if self.cursor.rowcount == 0:
            raise EmployeeNotFoundError(f"Employee {emp_id} not found")

    def export_to_csv(self, filepath):
        employees = self.view_all()
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Department", "Role", "Base Salary", "Bonus", "Total"])
            for e in employees:
                writer.writerow([e.emp_id, e.name, e.department, e.role(),
                                  e.base_salary, e.calculate_bonus(), e.total_compensation()])
        return filepath

    def close(self):
        self.connection.close()


def print_menu():
    print("\n" + "=" * 42)
    print("      EMPLOYEE MANAGEMENT SYSTEM")
    print("=" * 42)
    print(" 1. Add Employee")
    print(" 2. View Employee")
    print(" 3. View All Employees")
    print(" 4. Update Salary")
    print(" 5. Delete Employee")
    print(" 6. Export to CSV")
    print(" 7. Exit")


def main():
    db = EmployeeDatabase()
    while True:
        print_menu()
        choice = input("\nEnter Choice: ").strip()
        try:
            if choice == "1":
                role = input("Role (Developer/Manager/Intern): ").strip().capitalize()
                emp_id = int(input("Employee ID: "))
                name = input("Name: ")
                dept = input("Department: ")
                salary = float(input("Base Salary: "))
                if role == "Manager":
                    team_size = int(input("Team Size: "))
                    emp = Manager(emp_id, name, dept, salary, team_size)
                elif role == "Developer":
                    emp = Developer(emp_id, name, dept, salary)
                elif role == "Intern":
                    emp = Intern(emp_id, name, dept, salary)
                else:
                    print("✗ Invalid role")
                    continue
                db.add_employee(emp)
                print(f"\n✓ {role} {name} added with Total Compensation: Rs.{emp.total_compensation():,.2f}")

            elif choice == "2":
                emp_id = int(input("Employee ID: "))
                emp = db.get_employee(emp_id)
                print(f"\n  Name       : {emp.name}")
                print(f"  Role       : {emp.role()}")
                print(f"  Department : {emp.department}")
                print(f"  Base Salary: Rs.{emp.base_salary:,.2f}")
                print(f"  Bonus      : Rs.{emp.calculate_bonus():,.2f}")
                print(f"  Total      : Rs.{emp.total_compensation():,.2f}")

            elif choice == "3":
                employees = db.view_all()
                print(f"\n  {'ID':5}{'Name':18}{'Role':12}{'Dept':12}{'Total Comp':12}")
                print("  " + "-" * 60)
                for e in employees:
                    print(f"  {e.emp_id:<5}{e.name:<18}{e.role():<12}{e.department:<12}Rs.{e.total_compensation():,.2f}")

            elif choice == "4":
                emp_id = int(input("Employee ID: "))
                new_salary = float(input("New Base Salary: "))
                db.update_salary(emp_id, new_salary)
                print(f"\n✓ Salary updated for employee {emp_id}")

            elif choice == "5":
                emp_id = int(input("Employee ID: "))
                db.delete_employee(emp_id)
                print(f"\n✓ Employee {emp_id} removed")

            elif choice == "6":
                filename = input("Export filename (e.g. employees.csv): ") or "employees.csv"
                path = db.export_to_csv(filename)
                print(f"\n✓ Exported to {path}")

            elif choice == "7":
                print("\nSession ended. Goodbye!")
                db.close()
                break
            else:
                print("✗ Invalid choice.")
        except EmployeeError as e:
            print(f"\n✗ {type(e).__name__}: {e}")
        except (ValueError, sqlite3.IntegrityError) as e:
            print(f"\n✗ Input error: {e}")


if __name__ == "__main__":
    main()

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 employee_management.py
# =============================================================================
#
#
# ==========================================
#       EMPLOYEE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Employee
#  2. View Employee
#  3. View All Employees
#  4. Update Salary
#  5. Delete Employee
#  6. Export to CSV
#  7. Exit
#
# Enter Choice: Role (Developer/Manager/Intern): Employee ID: Name: Department: Base Salary: 
# ✓ Developer Pavan Shetty H S added with Total Compensation: Rs.82,500.00
#
# ==========================================
#       EMPLOYEE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Employee
#  2. View Employee
#  3. View All Employees
#  4. Update Salary
#  5. Delete Employee
#  6. Export to CSV
#  7. Exit
#
# Enter Choice: Role (Developer/Manager/Intern): Employee ID: Name: Department: Base Salary: Team Size: 
# ✓ Manager Rahul Kumar added with Total Compensation: Rs.143,000.00
#
# ==========================================
#       EMPLOYEE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Employee
#  2. View Employee
#  3. View All Employees
#  4. Update Salary
#  5. Delete Employee
#  6. Export to CSV
#  7. Exit
#
# Enter Choice: Role (Developer/Manager/Intern): Employee ID: Name: Department: Base Salary: 
# ✓ Intern Sneha Rao added with Total Compensation: Rs.15,000.00
#
# ==========================================
#       EMPLOYEE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Employee
#  2. View Employee
#  3. View All Employees
#  4. Update Salary
#  5. Delete Employee
#  6. Export to CSV
#  7. Exit
#
# Enter Choice: 
#   ID   Name              Role        Dept        Total Comp  
#   ------------------------------------------------------------
#   101  Pavan Shetty H S  Developer   Engineering Rs.82,500.00
#   102  Rahul Kumar       Manager     Engineering Rs.143,000.00
#   103  Sneha Rao         Intern      Engineering Rs.15,000.00
#
# ==========================================
#       EMPLOYEE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Employee
#  2. View Employee
#  3. View All Employees
#  4. Update Salary
#  5. Delete Employee
#  6. Export to CSV
#  7. Exit
#
# Enter Choice: Employee ID: 
#   Name       : Rahul Kumar
#   Role       : Manager
#   Department : Engineering
#   Base Salary: Rs.120,000.00
#   Bonus      : Rs.23,000.00
#   Total      : Rs.143,000.00
#
# ==========================================
#       EMPLOYEE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Employee
#  2. View Employee
#  3. View All Employees
#  4. Update Salary
#  5. Delete Employee
#  6. Export to CSV
#  7. Exit
#
# Enter Choice: Employee ID: New Base Salary: 
# ✓ Salary updated for employee 101
#
# ==========================================
#       EMPLOYEE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Employee
#  2. View Employee
#  3. View All Employees
#  4. Update Salary
#  5. Delete Employee
#  6. Export to CSV
#  7. Exit
#
# Enter Choice: Employee ID: 
# ✓ Employee 103 removed
#
# ==========================================
#       EMPLOYEE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Employee
#  2. View Employee
#  3. View All Employees
#  4. Update Salary
#  5. Delete Employee
#  6. Export to CSV
#  7. Exit
#
# Enter Choice: 
#   ID   Name              Role        Dept        Total Comp  
#   ------------------------------------------------------------
#   101  Pavan Shetty H S  Developer   Engineering Rs.88,000.00
#   102  Rahul Kumar       Manager     Engineering Rs.143,000.00
#
# ==========================================
#       EMPLOYEE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Employee
#  2. View Employee
#  3. View All Employees
#  4. Update Salary
#  5. Delete Employee
#  6. Export to CSV
#  7. Exit
#
# Enter Choice: Export filename (e.g. employees.csv): 
# ✓ Exported to employees.csv
#
# ==========================================
#       EMPLOYEE MANAGEMENT SYSTEM
# ==========================================
#  1. Add Employee
#  2. View Employee
#  3. View All Employees
#  4. Update Salary
#  5. Delete Employee
#  6. Export to CSV
#  7. Exit
#
# Enter Choice: 
# Session ended. Goodbye!
#
# =============================================================================

