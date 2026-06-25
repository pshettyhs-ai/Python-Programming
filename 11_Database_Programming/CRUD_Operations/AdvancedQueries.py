# =============================================================================
# AdvancedQueries.py
# Author  : Pavan Shetty H S
# Date    : July 2024
# Topic   : JOINs, Aggregations, Transactions
# =============================================================================
#
# Notes from Pavan:
# After basic CRUD felt comfortable, I wanted to push further into JOINs
# and aggregate functions because the projects ahead (Library Management,
# Employee Management) need related tables, not just single flat tables.
# =============================================================================

import sqlite3
import os

print("=" * 50)
print("    ADVANCED SQL QUERIES DEMO")
print("=" * 50)

db_path = "demo_advanced.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Setup: two related tables
cursor.execute("""
CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    dept_id INTEGER,
    salary REAL,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
)
""")

cursor.executemany(
    "INSERT INTO departments (dept_id, dept_name) VALUES (?, ?)",
    [(1, "Engineering"), (2, "Sales"), (3, "HR")]
)

cursor.executemany(
    "INSERT INTO employees (name, dept_id, salary) VALUES (?, ?, ?)",
    [
        ("Pavan Shetty H S", 1, 65000),
        ("Rahul Kumar", 1, 58000),
        ("Sneha Rao", 2, 52000),
        ("Arjun Mehta", 2, 49000),
        ("Divya Singh", 3, 45000),
        ("Unassigned Person", None, 30000),   # no department -- for testing JOIN types
    ]
)
connection.commit()

# ---------------------
# INNER JOIN -- only matching rows from both tables
# ---------------------
print("\n[1] INNER JOIN -- employees WITH a matching department")
cursor.execute("""
SELECT employees.name, departments.dept_name, employees.salary
FROM employees
INNER JOIN departments ON employees.dept_id = departments.dept_id
""")
for row in cursor.fetchall():
    print(f"  {row}")
print("  Notice: 'Unassigned Person' is MISSING -- INNER JOIN excludes")
print("  rows without a match in both tables.")

# ---------------------
# LEFT JOIN -- all rows from left table, matched or not
# ---------------------
print("\n[2] LEFT JOIN -- ALL employees, department shown as NULL if missing")
cursor.execute("""
SELECT employees.name, departments.dept_name
FROM employees
LEFT JOIN departments ON employees.dept_id = departments.dept_id
""")
for row in cursor.fetchall():
    print(f"  {row}")
print("  Now 'Unassigned Person' shows up WITH a None/NULL department.")
print("  This distinction (INNER vs LEFT) genuinely confused me until I")
print("  ran both side by side and SAW the different row counts.")

# ---------------------
# Aggregate functions -- COUNT, SUM, AVG, MAX, MIN
# ---------------------
print("\n[3] Aggregate functions")
cursor.execute("SELECT COUNT(*) FROM employees")
print(f"  Total employees: {cursor.fetchone()[0]}")

cursor.execute("SELECT AVG(salary) FROM employees")
print(f"  Average salary: {cursor.fetchone()[0]:.2f}")

cursor.execute("SELECT MAX(salary), MIN(salary) FROM employees")
max_sal, min_sal = cursor.fetchone()
print(f"  Max salary: {max_sal}, Min salary: {min_sal}")

# ---------------------
# GROUP BY -- aggregating per category
# ---------------------
print("\n[4] GROUP BY -- salary totals per department")
cursor.execute("""
SELECT departments.dept_name, COUNT(employees.emp_id), SUM(employees.salary)
FROM employees
INNER JOIN departments ON employees.dept_id = departments.dept_id
GROUP BY departments.dept_name
""")
for dept, count, total in cursor.fetchall():
    print(f"  {dept:15} | Employees: {count} | Total Salary: {total:,.2f}")

# ---------------------
# HAVING -- filtering AFTER aggregation (different from WHERE)
# ---------------------
print("\n[5] HAVING -- filter on aggregated results")
cursor.execute("""
SELECT departments.dept_name, AVG(employees.salary) as avg_salary
FROM employees
INNER JOIN departments ON employees.dept_id = departments.dept_id
GROUP BY departments.dept_name
HAVING avg_salary > 50000
""")
print("  Departments with average salary > 50000:")
for row in cursor.fetchall():
    print(f"    {row}")
print("""
  My note: WHERE filters rows BEFORE grouping happens, HAVING filters
  groups AFTER aggregation. Tried using WHERE with AVG() directly once
  and got an error -- that's what pushed me to actually learn the
  distinction instead of guessing.
""")

# ---------------------
# Transactions -- commit and rollback
# ---------------------
print("[6] Transactions -- commit() vs rollback()")
try:
    cursor.execute("UPDATE employees SET salary = salary * 1.1 WHERE dept_id = 1")
    # Simulating an error mid-transaction
    raise ValueError("Simulated failure during transaction!")
    connection.commit()
except ValueError as e:
    print(f"  Error occurred: {e}")
    connection.rollback()   # undoes the salary update above
    print("  Rolled back -- salary update was UNDONE")

cursor.execute("SELECT name, salary FROM employees WHERE dept_id = 1")
print(f"  Engineering salaries after rollback: {cursor.fetchall()}")
print("  Confirms the 10% raise was NOT applied -- rollback worked correctly.")

connection.close()
os.remove(db_path)
print(f"\n  Cleanup: removed {db_path}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 AdvancedQueries.py
# =============================================================================
#
# ==================================================
#     ADVANCED SQL QUERIES DEMO
# ==================================================
#
# [1] INNER JOIN -- employees WITH a matching department
#   ('Pavan Shetty H S', 'Engineering', 65000.0)
#   ('Rahul Kumar', 'Engineering', 58000.0)
#   ('Sneha Rao', 'Sales', 52000.0)
#   ('Arjun Mehta', 'Sales', 49000.0)
#   ('Divya Singh', 'HR', 45000.0)
#   Notice: 'Unassigned Person' is MISSING -- INNER JOIN excludes
#   rows without a match in both tables.
#
# [2] LEFT JOIN -- ALL employees, department shown as NULL if missing
#   ('Pavan Shetty H S', 'Engineering')
#   ('Rahul Kumar', 'Engineering')
#   ('Sneha Rao', 'Sales')
#   ('Arjun Mehta', 'Sales')
#   ('Divya Singh', 'HR')
#   ('Unassigned Person', None)
#   Now 'Unassigned Person' shows up WITH a None/NULL department.
#   This distinction (INNER vs LEFT) genuinely confused me until I
#   ran both side by side and SAW the different row counts.
#
# [3] Aggregate functions
#   Total employees: 6
#   Average salary: 49833.33
#   Max salary: 65000.0, Min salary: 30000.0
#
# [4] GROUP BY -- salary totals per department
#   Engineering     | Employees: 2 | Total Salary: 123,000.00
#   HR              | Employees: 1 | Total Salary: 45,000.00
#   Sales           | Employees: 2 | Total Salary: 101,000.00
#
# [5] HAVING -- filter on aggregated results
#   Departments with average salary > 50000:
#     ('Engineering', 61500.0)
#     ('Sales', 50500.0)
#
#   My note: WHERE filters rows BEFORE grouping happens, HAVING filters
#   groups AFTER aggregation. Tried using WHERE with AVG() directly once
#   and got an error -- that's what pushed me to actually learn the
#   distinction instead of guessing.
#
# [6] Transactions -- commit() vs rollback()
#   Error occurred: Simulated failure during transaction!
#   Rolled back -- salary update was UNDONE
#   Engineering salaries after rollback: [('Pavan Shetty H S', 65000.0), ('Rahul Kumar', 58000.0)]
#   Confirms the 10% raise was NOT applied -- rollback worked correctly.
#
#   Cleanup: removed demo_advanced.db
#
# ==================================================
#
# =============================================================================

