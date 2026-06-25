# =============================================================================
# CRUD.py
# Author  : Pavan Shetty H S
# Date    : July 2024
# Topic   : CRUD Operations -- Create, Read, Update, Delete
# =============================================================================
#
# Notes from Pavan:
# CRUD is the foundation of basically every database-backed application.
# The biggest lesson from this file: NEVER use Python f-strings or %
# formatting to build SQL queries with user input. Use parameterized
# queries (the ? placeholder) instead. I deliberately wrote a vulnerable
# version below to understand SQL injection before fixing it properly --
# seeing the exploit work on my OWN test database made the danger
# concrete instead of abstract.
# =============================================================================

import sqlite3
import os

print("=" * 50)
print("    CRUD OPERATIONS DEMO")
print("=" * 50)

db_path = "demo_crud.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    branch TEXT NOT NULL,
    cgpa REAL
)
""")
connection.commit()

# ---------------------
# CREATE -- inserting records
# ---------------------
print("\n[1] CREATE -- INSERT records")

# Single insert with parameterized query (SAFE way)
cursor.execute(
    "INSERT INTO students (name, branch, cgpa) VALUES (?, ?, ?)",
    ("Pavan Shetty H S", "ECE", 8.7)
)
connection.commit()
print(f"  Inserted 1 record. New row id: {cursor.lastrowid}")

# Bulk insert with executemany -- much cleaner than looping individual inserts
students_data = [
    ("Rahul Kumar", "CSE", 7.9),
    ("Sneha Rao", "ISE", 9.1),
    ("Arjun Mehta", "EEE", 8.2),
    ("Divya Singh", "ECE", 8.9),
]
cursor.executemany(
    "INSERT INTO students (name, branch, cgpa) VALUES (?, ?, ?)",
    students_data
)
connection.commit()
print(f"  Bulk inserted {len(students_data)} records using executemany()")

# ---------------------
# READ -- querying records
# ---------------------
print("\n[2] READ -- SELECT records")

cursor.execute("SELECT * FROM students")
all_students = cursor.fetchall()
print(f"  All students ({len(all_students)} total):")
for row in all_students:
    print(f"    {row}")

print("\n  Filtering with WHERE clause:")
cursor.execute("SELECT name, cgpa FROM students WHERE cgpa > ?", (8.5,))
toppers = cursor.fetchall()
print(f"  Toppers (CGPA > 8.5): {toppers}")

print("\n  Using fetchone() for a single result:")
cursor.execute("SELECT * FROM students WHERE student_id = ?", (1,))
single = cursor.fetchone()
print(f"  Student with id=1: {single}")

print("\n  Sorting results:")
cursor.execute("SELECT name, cgpa FROM students ORDER BY cgpa DESC")
sorted_students = cursor.fetchall()
print(f"  Sorted by CGPA (highest first): {sorted_students}")

# ---------------------
# UPDATE -- modifying records
# ---------------------
print("\n[3] UPDATE -- modify existing records")
cursor.execute(
    "UPDATE students SET cgpa = ? WHERE name = ?",
    (9.0, "Rahul Kumar")
)
connection.commit()
print(f"  Rows affected: {cursor.rowcount}")

cursor.execute("SELECT name, cgpa FROM students WHERE name = ?", ("Rahul Kumar",))
print(f"  Updated record: {cursor.fetchone()}")

# ---------------------
# DELETE -- removing records
# ---------------------
print("\n[4] DELETE -- remove records")
cursor.execute("DELETE FROM students WHERE name = ?", ("Arjun Mehta",))
connection.commit()
print(f"  Rows deleted: {cursor.rowcount}")

cursor.execute("SELECT name FROM students")
remaining = [row[0] for row in cursor.fetchall()]
print(f"  Remaining students: {remaining}")

# ---------------------
# THE SQL INJECTION DANGER -- why I never use string formatting for SQL
# ---------------------
print("\n[5] SQL Injection demonstration (why parameterized queries matter)")
print("  Simulating a VULNERABLE query built with string formatting:")

malicious_input = "Pavan' OR '1'='1"
vulnerable_query = f"SELECT * FROM students WHERE name = '{malicious_input}'"
print(f"  Resulting query: {vulnerable_query}")
print("  ^ This 'OR 1=1' trick would return ALL rows, bypassing the name")
print("  filter entirely -- a classic SQL injection attack pattern.")
print("  In a login system, this exact pattern can bypass authentication!")

cursor.execute(vulnerable_query)   # Running it to PROVE the danger is real
injected_results = cursor.fetchall()
print(f"  Vulnerable query actually returned {len(injected_results)} rows")
print("  (should have returned 0 if 'Pavan' OR '1'='1' was treated as data)")

print("\n  The SAFE version using a parameterized query:")
cursor.execute("SELECT * FROM students WHERE name = ?", (malicious_input,))
safe_results = cursor.fetchall()
print(f"  Safe query returned {len(safe_results)} rows")
print("  ^ The ? placeholder treats malicious_input as PURE DATA, not as")
print("  part of the SQL syntax, so the injection attempt fails harmlessly.")
print("  Lesson burned into memory: ALWAYS use ? placeholders, NEVER")
print("  f-strings or .format() or % to build SQL queries with variable data.")

# ---------------------
# Closing the connection
# ---------------------
connection.close()
os.remove(db_path)
print(f"\n  Cleanup: removed {db_path}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 CRUD.py
# =============================================================================
#
# ==================================================
#     CRUD OPERATIONS DEMO
# ==================================================
#
# [1] CREATE -- INSERT records
#   Inserted 1 record. New row id: 1
#   Bulk inserted 4 records using executemany()
#
# [2] READ -- SELECT records
#   All students (5 total):
#     (1, 'Pavan Shetty H S', 'ECE', 8.7)
#     (2, 'Rahul Kumar', 'CSE', 7.9)
#     (3, 'Sneha Rao', 'ISE', 9.1)
#     (4, 'Arjun Mehta', 'EEE', 8.2)
#     (5, 'Divya Singh', 'ECE', 8.9)
#
#   Filtering with WHERE clause:
#   Toppers (CGPA > 8.5): [('Pavan Shetty H S', 8.7), ('Sneha Rao', 9.1), ('Divya Singh', 8.9)]
#
#   Using fetchone() for a single result:
#   Student with id=1: (1, 'Pavan Shetty H S', 'ECE', 8.7)
#
#   Sorting results:
#   Sorted by CGPA (highest first): [('Sneha Rao', 9.1), ('Divya Singh', 8.9), ('Pavan Shetty H S', 8.7), ('Arjun Mehta', 8.2), ('Rahul Kumar', 7.9)]
#
# [3] UPDATE -- modify existing records
#   Rows affected: 1
#   Updated record: ('Rahul Kumar', 9.0)
#
# [4] DELETE -- remove records
#   Rows deleted: 1
#   Remaining students: ['Pavan Shetty H S', 'Rahul Kumar', 'Sneha Rao', 'Divya Singh']
#
# [5] SQL Injection demonstration (why parameterized queries matter)
#   Simulating a VULNERABLE query built with string formatting:
#   Resulting query: SELECT * FROM students WHERE name = 'Pavan' OR '1'='1'
#   ^ This 'OR 1=1' trick would return ALL rows, bypassing the name
#   filter entirely -- a classic SQL injection attack pattern.
#   In a login system, this exact pattern can bypass authentication!
#   Vulnerable query actually returned 4 rows
#   (should have returned 0 if 'Pavan' OR '1'='1' was treated as data)
#
#   The SAFE version using a parameterized query:
#   Safe query returned 0 rows
#   ^ The ? placeholder treats malicious_input as PURE DATA, not as
#   part of the SQL syntax, so the injection attempt fails harmlessly.
#   Lesson burned into memory: ALWAYS use ? placeholders, NEVER
#   f-strings or .format() or % to build SQL queries with variable data.
#
#   Cleanup: removed demo_crud.db
#
# ==================================================
#
# =============================================================================

