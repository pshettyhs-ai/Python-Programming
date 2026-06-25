# =============================================================================
# DatabaseSetup.py
# Author  : Pavan Shetty H S
# Date    : July 2024
# Topic   : SQLite -- connecting, creating tables, schema design
# =============================================================================
#
# Notes from Pavan:
# SQLite is built INTO Python's standard library (sqlite3 module) -- no
# separate server install needed, unlike MySQL/PostgreSQL which I tried
# setting up once and gave up on for local learning purposes. SQLite
# stores everything in a single .db file, perfect for learning and for
# small projects without needing a dedicated database server running.
# =============================================================================

import sqlite3
import os

print("=" * 50)
print("    SQLITE DATABASE SETUP DEMO")
print("=" * 50)

db_path = "demo_college.db"

# ---------------------
# Connecting to a database (creates the file if it doesn't exist)
# ---------------------
print("\n[1] Connecting to SQLite database")
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
print(f"  Connected to {db_path}")
print("  (File created automatically since it didn't exist before)")

# ---------------------
# Creating a table -- schema design
# ---------------------
print("\n[2] Creating a table with proper schema design")
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    branch TEXT NOT NULL,
    cgpa REAL CHECK(cgpa >= 0 AND cgpa <= 10),
    phone TEXT UNIQUE,
    email TEXT UNIQUE,
    enrollment_date TEXT DEFAULT CURRENT_DATE
)
""")
connection.commit()
print("  Table 'students' created with constraints:")
print("    - student_id: auto-incrementing primary key")
print("    - name, branch: required (NOT NULL)")
print("    - cgpa: CHECK constraint (0-10 range)")
print("    - phone, email: UNIQUE constraints")
print("    - enrollment_date: defaults to current date")

# ---------------------
# Creating a related table (foreign key relationship)
# ---------------------
print("\n[3] Creating related table with FOREIGN KEY")
cursor.execute("""
CREATE TABLE IF NOT EXISTS marks (
    mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    score INTEGER CHECK(score >= 0 AND score <= 100),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
""")
connection.commit()
print("  Table 'marks' created, linked to 'students' via foreign key")
print("""
  My note on this: enabling foreign key enforcement in SQLite requires
  an explicit PRAGMA statement -- it's OFF by default, which surprised
  me. Without it, SQLite will silently let you insert a marks row with
  a student_id that doesn't exist in the students table!
""")
cursor.execute("PRAGMA foreign_keys = ON")

# ---------------------
# Inspecting the schema
# ---------------------
print("[4] Inspecting table schema")
cursor.execute("PRAGMA table_info(students)")
columns = cursor.fetchall()
print("  Columns in 'students' table:")
for col in columns:
    # col format: (cid, name, type, notnull, default_value, pk)
    print(f"    {col[1]:20} {col[2]:10} {'NOT NULL' if col[3] else ''}")

# ---------------------
# Listing all tables
# ---------------------
print("\n[5] Listing all tables in the database")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"  Tables: {[t[0] for t in tables]}")

# ---------------------
# Closing connection properly
# ---------------------
connection.close()
print("\n  Connection closed.")

# Cleanup for repeated demo runs
os.remove(db_path)
print(f"  Demo cleanup: removed {db_path}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 DatabaseSetup.py
# =============================================================================
#
# ==================================================
#     SQLITE DATABASE SETUP DEMO
# ==================================================
#
# [1] Connecting to SQLite database
#   Connected to demo_college.db
#   (File created automatically since it didn't exist before)
#
# [2] Creating a table with proper schema design
#   Table 'students' created with constraints:
#     - student_id: auto-incrementing primary key
#     - name, branch: required (NOT NULL)
#     - cgpa: CHECK constraint (0-10 range)
#     - phone, email: UNIQUE constraints
#     - enrollment_date: defaults to current date
#
# [3] Creating related table with FOREIGN KEY
#   Table 'marks' created, linked to 'students' via foreign key
#
#   My note on this: enabling foreign key enforcement in SQLite requires
#   an explicit PRAGMA statement -- it's OFF by default, which surprised
#   me. Without it, SQLite will silently let you insert a marks row with
#   a student_id that doesn't exist in the students table!
#
# [4] Inspecting table schema
#   Columns in 'students' table:
#     student_id           INTEGER    
#     name                 TEXT       NOT NULL
#     branch               TEXT       NOT NULL
#     cgpa                 REAL       
#     phone                TEXT       
#     email                TEXT       
#     enrollment_date      TEXT       
#
# [5] Listing all tables in the database
#   Tables: ['students', 'sqlite_sequence', 'marks']
#
#   Connection closed.
#   Demo cleanup: removed demo_college.db
#
# ==================================================
#
# =============================================================================

