# =============================================================================
# Dictionaries.py
# Author  : Pavan Shetty H S
# Date    : February 2024
# Topic   : Dictionaries -- key-value pairs
# =============================================================================
#
# Notes from Pavan:
# Dictionaries are probably the single most useful data structure I've
# learned so far. Once I understood hash maps conceptually (from DSA
# studies later), dicts made way more sense -- O(1) average lookup time
# instead of scanning a whole list. I use these everywhere now: storing
# records, counting occurrences, caching/memoization, JSON-like data.
#
# =============================================================================

print("=" * 50)
print("       DICTIONARIES DEMO")
print("=" * 50)

# ---------------------
# Creating dictionaries
# ---------------------
student = {
    "name": "Pavan Shetty H S",
    "branch": "Electronics & Communication",
    "year": 3,
    "cgpa": 8.5
}
empty_dict = {}
from_pairs = dict([("a", 1), ("b", 2)])

print(f"\nStudent: {student}")
print(f"From pairs: {from_pairs}")

# ---------------------
# Accessing values
# ---------------------
print("\n[Accessing values]")
print(f"  student['name']: {student['name']}")
print(f"  student.get('cgpa'): {student.get('cgpa')}")
print(f"  student.get('phone', 'Not Provided'): {student.get('phone', 'Not Provided')}")

# The KeyError trap -- my early mistake
try:
    print(student['phone'])
except KeyError as e:
    print(f"  Direct access student['phone'] raised: KeyError {e}")
    print("  Lesson: use .get() with default when key might not exist!")

# ---------------------
# Adding & updating
# ---------------------
print("\n[Add/Update]")
student["phone"] = "9876543210"   # adds new key
print(f"  After adding phone: {student}")

student["year"] = 4   # updates existing key
print(f"  After updating year: {student['year']}")

student.update({"cgpa": 8.7, "active": True})  # update multiple at once
print(f"  After update(): {student}")

# ---------------------
# Removing
# ---------------------
print("\n[Removing]")
removed = student.pop("active")
print(f"  Popped 'active': {removed}")
print(f"  Dict now: {student}")

del student["phone"]
print(f"  After del student['phone']: {student}")

# ---------------------
# Iterating
# ---------------------
print("\n[Iterating]")
print("  Keys only:")
for key in student.keys():
    print(f"    {key}")

print("  Values only:")
for value in student.values():
    print(f"    {value}")

print("  Key-value pairs:")
for key, value in student.items():
    print(f"    {key}: {value}")

# ---------------------
# Dictionary comprehension
# ---------------------
print("\n[Dictionary Comprehension]")
squares = {x: x**2 for x in range(1, 6)}
print(f"  Squares dict: {squares}")

# Practical example: word frequency counter
text = "the quick brown fox jumps over the lazy dog the fox runs"
word_count = {}
for word in text.split():
    word_count[word] = word_count.get(word, 0) + 1
print(f"\n  Word frequency: {word_count}")

# Same thing using collections.Counter (found this later, much cleaner)
from collections import Counter
word_count2 = Counter(text.split())
print(f"  Using Counter: {dict(word_count2)}")
print(f"  Most common 2: {word_count2.most_common(2)}")

# ---------------------
# Nested dictionaries -- used heavily in my projects later
# ---------------------
print("\n[Nested Dictionaries]")
students_db = {
    "S101": {"name": "Rahul", "branch": "CSE", "cgpa": 8.2},
    "S102": {"name": "Pavan", "branch": "ECE", "cgpa": 9.1},
    "S103": {"name": "Sneha", "branch": "ISE", "cgpa": 7.8},
}
print(f"  Full DB: {students_db}")
print(f"  Student S102's name: {students_db['S102']['name']}")

for sid, info in students_db.items():
    print(f"    {sid}: {info['name']} ({info['branch']}) - CGPA {info['cgpa']}")

# ---------------------
# Checking membership
# ---------------------
print("\n[Membership checks]")
print(f"  'name' in student: {'name' in student}")   # checks KEYS by default
print(f"  'Pavan' in student.values(): {'Pavan Shetty H S' in student.values()}")

# ---------------------
# setdefault -- useful trick I picked up
# ---------------------
print("\n[setdefault()]")
inventory = {}
items = ["pen", "pen", "pencil", "eraser", "pen", "pencil"]
for item in items:
    inventory[item] = inventory.setdefault(item, 0) + 1
print(f"  Item counts using setdefault: {inventory}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Dictionaries.py
# =============================================================================
#
# ==================================================
#        DICTIONARIES DEMO
# ==================================================
#
# Student: {'name': 'Pavan Shetty H S', 'branch': 'Electronics & Communication', 'year': 3, 'cgpa': 8.5}
# From pairs: {'a': 1, 'b': 2}
#
# [Accessing values]
#   student['name']: Pavan Shetty H S
#   student.get('cgpa'): 8.5
#   student.get('phone', 'Not Provided'): Not Provided
#   Direct access student['phone'] raised: KeyError 'phone'
#   Lesson: use .get() with default when key might not exist!
#
# [Add/Update]
#   After adding phone: {'name': 'Pavan Shetty H S', 'branch': 'Electronics & Communication', 'year': 3, 'cgpa': 8.5, 'phone': '9876543210'}
#   After updating year: 4
#   After update(): {'name': 'Pavan Shetty H S', 'branch': 'Electronics & Communication', 'year': 4, 'cgpa': 8.7, 'phone': '9876543210', 'active': True}
#
# [Removing]
#   Popped 'active': True
#   Dict now: {'name': 'Pavan Shetty H S', 'branch': 'Electronics & Communication', 'year': 4, 'cgpa': 8.7, 'phone': '9876543210'}
#   After del student['phone']: {'name': 'Pavan Shetty H S', 'branch': 'Electronics & Communication', 'year': 4, 'cgpa': 8.7}
#
# [Iterating]
#   Keys only:
#     name
#     branch
#     year
#     cgpa
#   Values only:
#     Pavan Shetty H S
#     Electronics & Communication
#     4
#     8.7
#   Key-value pairs:
#     name: Pavan Shetty H S
#     branch: Electronics & Communication
#     year: 4
#     cgpa: 8.7
#
# [Dictionary Comprehension]
#   Squares dict: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
#
#   Word frequency: {'the': 3, 'quick': 1, 'brown': 1, 'fox': 2, 'jumps': 1, 'over': 1, 'lazy': 1, 'dog': 1, 'runs': 1}
#   Using Counter: {'the': 3, 'quick': 1, 'brown': 1, 'fox': 2, 'jumps': 1, 'over': 1, 'lazy': 1, 'dog': 1, 'runs': 1}
#   Most common 2: [('the', 3), ('fox', 2)]
#
# [Nested Dictionaries]
#   Full DB: {'S101': {'name': 'Rahul', 'branch': 'CSE', 'cgpa': 8.2}, 'S102': {'name': 'Pavan', 'branch': 'ECE', 'cgpa': 9.1}, 'S103': {'name': 'Sneha', 'branch': 'ISE', 'cgpa': 7.8}}
#   Student S102's name: Pavan
#     S101: Rahul (CSE) - CGPA 8.2
#     S102: Pavan (ECE) - CGPA 9.1
#     S103: Sneha (ISE) - CGPA 7.8
#
# [Membership checks]
#   'name' in student: True
#   'Pavan' in student.values(): True
#
# [setdefault()]
#   Item counts using setdefault: {'pen': 3, 'pencil': 2, 'eraser': 1}
#
# ==================================================
#
# =============================================================================

