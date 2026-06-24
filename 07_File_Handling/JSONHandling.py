# =============================================================================
# JSONHandling.py
# Author  : Pavan Shetty H S
# Date    : April 2024
# Topic   : Reading and Writing JSON Files
# =============================================================================
#
# Notes from Pavan:
# JSON felt instantly familiar because it maps almost 1:1 to Python dicts
# and lists. json.dumps()/json.loads() for strings, json.dump()/json.load()
# for files (note the missing 's' for file operations -- mixed this up
# constantly in week 1).
# =============================================================================

import json
import os

print("=" * 50)
print("       JSON HANDLING DEMO")
print("=" * 50)

# ---------------------
# Python dict <-> JSON string
# ---------------------
print("\n[1] dict to JSON string (json.dumps)")
student = {
    "name": "Pavan Shetty H S",
    "branch": "Electronics",
    "year": 3,
    "cgpa": 8.5,
    "skills": ["Python", "C", "Embedded C"],
    "is_active": True,
    "internship": None
}

json_string = json.dumps(student, indent=4)
print(json_string)

print("\n[2] JSON string back to dict (json.loads)")
parsed = json.loads(json_string)
print(f"  Parsed name: {parsed['name']}")
print(f"  Parsed skills: {parsed['skills']}")
print(f"  Type after parsing: {type(parsed)}")

# ---------------------
# Writing JSON to a FILE (json.dump -- no 's')
# ---------------------
print("\n[3] Writing JSON to file (json.dump -- no 's' at the end)")
json_path = "student_data.json"
with open(json_path, "w") as f:
    json.dump(student, f, indent=4)
print(f"  Wrote {json_path}")

# ---------------------
# Reading JSON from a FILE (json.load -- no 's')
# ---------------------
print("\n[4] Reading JSON from file (json.load -- no 's')")
with open(json_path, "r") as f:
    loaded_data = json.load(f)
print(f"  Loaded: {loaded_data}")

# ---------------------
# The mixup I made constantly: dump vs dumps, load vs loads
# ---------------------
print("\n[5] My cheat sheet for remembering the difference:")
print("""
  json.dumps(obj)        -> dict to STRING        (s = string)
  json.loads(string)     -> STRING to dict         (s = string)
  json.dump(obj, file)   -> dict directly to FILE  (no s)
  json.load(file)        -> FILE directly to dict  (no s)

  Mnemonic I use: the 's' versions deal with strings (s for string),
  the non-s versions deal with file objects directly.
""")

# ---------------------
# Working with a list of records (common real-world pattern)
# ---------------------
print("[6] Practical: Storing a list of student records")
students_db = [
    {"id": 101, "name": "Pavan", "cgpa": 8.5},
    {"id": 102, "name": "Rahul", "cgpa": 7.8},
    {"id": 103, "name": "Sneha", "cgpa": 9.1},
]

db_path = "students_db.json"
with open(db_path, "w") as f:
    json.dump(students_db, f, indent=2)

with open(db_path, "r") as f:
    loaded_db = json.load(f)

print(f"  Loaded {len(loaded_db)} student records")
for s in loaded_db:
    print(f"    {s['id']}: {s['name']} - CGPA {s['cgpa']}")

# ---------------------
# Handling JSON decode errors
# ---------------------
print("\n[7] Handling malformed JSON")
bad_json = "{name: 'Pavan', missing quotes}"  # invalid JSON syntax
try:
    json.loads(bad_json)
except json.JSONDecodeError as e:
    print(f"  Caught JSONDecodeError: {e}")
    print("  Lesson: JSON requires DOUBLE quotes for keys/strings, not single quotes!")

# ---------------------
# Custom encoding -- handling non-serializable types
# ---------------------
print("\n[8] Handling non-JSON-serializable types (like datetime)")
from datetime import datetime

record = {"event": "Login", "timestamp": datetime.now()}
try:
    json.dumps(record)
except TypeError as e:
    print(f"  Caught error: {e}")
    print("  Fix: convert datetime to string first, or use default= parameter")

record_fixed = {"event": "Login", "timestamp": datetime.now().isoformat()}
print(f"  Fixed version: {json.dumps(record_fixed)}")

# Cleanup
os.remove(json_path)
os.remove(db_path)
print(f"\n  Cleaned up temp JSON files")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 JSONHandling.py
# =============================================================================
#
# ==================================================
#        JSON HANDLING DEMO
# ==================================================
#
# [1] dict to JSON string (json.dumps)
# {
#     "name": "Pavan Shetty H S",
#     "branch": "Electronics",
#     "year": 3,
#     "cgpa": 8.5,
#     "skills": [
#         "Python",
#         "C",
#         "Embedded C"
#     ],
#     "is_active": true,
#     "internship": null
# }
#
# [2] JSON string back to dict (json.loads)
#   Parsed name: Pavan Shetty H S
#   Parsed skills: ['Python', 'C', 'Embedded C']
#   Type after parsing: <class 'dict'>
#
# [3] Writing JSON to file (json.dump -- no 's' at the end)
#   Wrote student_data.json
#
# [4] Reading JSON from file (json.load -- no 's')
#   Loaded: {'name': 'Pavan Shetty H S', 'branch': 'Electronics', 'year': 3, 'cgpa': 8.5, 'skills': ['Python', 'C', 'Embedded C'], 'is_active': True, 'internship': None}
#
# [5] My cheat sheet for remembering the difference:
#
#   json.dumps(obj)        -> dict to STRING        (s = string)
#   json.loads(string)     -> STRING to dict         (s = string)
#   json.dump(obj, file)   -> dict directly to FILE  (no s)
#   json.load(file)        -> FILE directly to dict  (no s)
#
#   Mnemonic I use: the 's' versions deal with strings (s for string),
#   the non-s versions deal with file objects directly.
#
# [6] Practical: Storing a list of student records
#   Loaded 3 student records
#     101: Pavan - CGPA 8.5
#     102: Rahul - CGPA 7.8
#     103: Sneha - CGPA 9.1
#
# [7] Handling malformed JSON
#   Caught JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
#   Lesson: JSON requires DOUBLE quotes for keys/strings, not single quotes!
#
# [8] Handling non-JSON-serializable types (like datetime)
#   Caught error: Object of type datetime is not JSON serializable
#   Fix: convert datetime to string first, or use default= parameter
#   Fixed version: {"event": "Login", "timestamp": "2026-06-21T07:14:38.113712"}
#
#   Cleaned up temp JSON files
#
# ==================================================
#
# =============================================================================

