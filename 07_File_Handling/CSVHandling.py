# =============================================================================
# CSVHandling.py
# Author  : Pavan Shetty H S
# Date    : April 2024
# Topic   : Reading and Writing CSV Files
# =============================================================================
#
# Notes from Pavan:
# Before learning the csv module, I tried parsing CSV files manually with
# .split(","). Worked fine until I hit a field that itself contained a
# comma (like an address "Bangalore, Karnataka") and my parsing broke
# completely. The csv module handles quoting/escaping correctly, which
# manual splitting does not. Lesson: don't reinvent well-solved problems.
# =============================================================================

import csv
import os

print("=" * 50)
print("       CSV HANDLING DEMO")
print("=" * 50)

csv_path = "students.csv"

# ---------------------
# Writing CSV with csv.writer
# ---------------------
print("\n[1] Writing CSV with csv.writer")
with open(csv_path, "w", newline="") as f:
    # newline="" is required on Windows to prevent extra blank lines
    # I learned this after seeing weird blank rows between every record
    writer = csv.writer(f)
    writer.writerow(["StudentID", "Name", "Branch", "CGPA"])   # header
    writer.writerow([101, "Pavan Shetty H S", "ECE", 8.5])
    writer.writerow([102, "Rahul Kumar", "CSE", 7.8])
    writer.writerow([103, "Sneha Rao", "ISE", 9.1])
    writer.writerow([104, "Address Example", "Bangalore, Karnataka", 8.0])  # has a comma!

print(f"  Wrote {csv_path}")

# ---------------------
# Reading CSV with csv.reader
# ---------------------
print("\n[2] Reading CSV with csv.reader")
with open(csv_path, "r", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)   # grab header row separately
    print(f"  Header: {header}")
    for row in reader:
        print(f"  Row: {row}")

print("  Notice: 'Bangalore, Karnataka' stayed as ONE field, not split by its comma!")
print("  This is exactly what manual .split(',') would have broken.")

# ---------------------
# DictWriter and DictReader -- much more readable, what I use now
# ---------------------
print("\n[3] DictWriter -- write using dictionaries (more readable code)")
students = [
    {"id": 201, "name": "Arjun", "branch": "EEE", "cgpa": 8.2},
    {"id": 202, "name": "Divya", "branch": "ECE", "cgpa": 9.0},
]

dict_csv_path = "students_dict.csv"
with open(dict_csv_path, "w", newline="") as f:
    fieldnames = ["id", "name", "branch", "cgpa"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(students)

print(f"  Wrote {dict_csv_path} using DictWriter")

print("\n[4] DictReader -- read rows as dictionaries")
with open(dict_csv_path, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['name']} ({row['branch']}) - CGPA: {row['cgpa']}")
        # NOTE: row['cgpa'] is a STRING here, not a float!
        # Caught me out -- had to explicitly do float(row['cgpa']) for math

# ---------------------
# Practical use: filtering and processing CSV data
# ---------------------
print("\n[5] Practical: Finding students with CGPA > 8.5")
with open(dict_csv_path, "r", newline="") as f:
    reader = csv.DictReader(f)
    toppers = [row for row in reader if float(row["cgpa"]) > 8.5]

print(f"  Toppers: {[s['name'] for s in toppers]}")

# Cleanup
os.remove(csv_path)
os.remove(dict_csv_path)
print(f"\n  Cleaned up temp CSV files")

print("\n" + "=" * 50)

# =============================================================================
# Debugging note: csv.DictReader returns EVERY value as a string, even
# numbers. Tried comparing row['cgpa'] > 8.5 directly once and got
# TypeError: '>' not supported between instances of 'str' and 'float'.
# Always cast numeric CSV fields explicitly before doing math/comparisons.
# =============================================================================

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 CSVHandling.py
# =============================================================================
#
# ==================================================
#        CSV HANDLING DEMO
# ==================================================
#
# [1] Writing CSV with csv.writer
#   Wrote students.csv
#
# [2] Reading CSV with csv.reader
#   Header: ['StudentID', 'Name', 'Branch', 'CGPA']
#   Row: ['101', 'Pavan Shetty H S', 'ECE', '8.5']
#   Row: ['102', 'Rahul Kumar', 'CSE', '7.8']
#   Row: ['103', 'Sneha Rao', 'ISE', '9.1']
#   Row: ['104', 'Address Example', 'Bangalore, Karnataka', '8.0']
#   Notice: 'Bangalore, Karnataka' stayed as ONE field, not split by its comma!
#   This is exactly what manual .split(',') would have broken.
#
# [3] DictWriter -- write using dictionaries (more readable code)
#   Wrote students_dict.csv using DictWriter
#
# [4] DictReader -- read rows as dictionaries
#   Arjun (EEE) - CGPA: 8.2
#   Divya (ECE) - CGPA: 9.0
#
# [5] Practical: Finding students with CGPA > 8.5
#   Toppers: ['Divya']
#
#   Cleaned up temp CSV files
#
# ==================================================
#
# =============================================================================

