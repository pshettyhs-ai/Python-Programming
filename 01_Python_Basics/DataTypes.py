# =============================================================================
# DataTypes.py
# Author  : Pavan Shetty H S
# Date    : January 2024
# Topic   : Python Data Types — Complete Overview
# =============================================================================
#
# Notes from Pavan:
# Python has way more built-in types than C. In C you have int, float, char,
# double, and that's mostly it. Python has int, float, complex, str, list,
# tuple, set, dict, bool, bytes — all with rich built-in methods.
#
# Most surprising thing: Python integers have no size limit. You can have
# a number with 1000 digits. Try that in C without a library!
#
# =============================================================================

print("=" * 50)
print("     PYTHON DATA TYPES DEMO")
print("=" * 50)

# ---------------------
# 1. Numeric Types
# ---------------------
print("\n[1] NUMERIC TYPES")

# int — no size limit unlike C's int (32/64 bit)
age = 22
big_num = 99999999999999999999999999  # Try this in C!
binary_num = 0b1010      # binary literal (value: 10)
octal_num = 0o17         # octal literal  (value: 15)
hex_num = 0xFF           # hex literal    (value: 255)

print(f"  int        : {age}    | type: {type(age)}")
print(f"  big int    : {big_num}")
print(f"  binary 0b1010 = {binary_num}")
print(f"  octal  0o17   = {octal_num}")
print(f"  hex    0xFF   = {hex_num}")

# float — IEEE 754 double precision (same as C's double)
pi = 3.14159
sci = 2.5e3    # 2500.0
print(f"\n  float      : {pi}  | type: {type(pi)}")
print(f"  scientific : {sci}     | 2.5e3 = {sci}")

# complex — I never used this before Python. Useful for signal processing!
c = 3 + 4j
print(f"\n  complex    : {c}")
print(f"  real part  : {c.real}")
print(f"  imag part  : {c.imag}")
print(f"  magnitude  : {abs(c)}")  # sqrt(3^2 + 4^2) = 5.0

# ---------------------
# 2. Boolean
# ---------------------
print("\n[2] BOOLEAN")
is_engineer = True
is_expert = False

print(f"  True   : {is_engineer}")
print(f"  False  : {is_expert}")
print(f"  bool is subclass of int: True == 1 is {True == 1}")
print(f"  True + True = {True + True}")    # 2 — surprised me!
print(f"  True * 5    = {True * 5}")        # 5

# ---------------------
# 3. String
# ---------------------
print("\n[3] STRING")
single = 'Hello'
double = "World"
multi  = """This is
a multiline
string"""

print(f"  Single quotes : {single}")
print(f"  Double quotes : {double}")
print(f"  Multiline     :\n{multi}")
print(f"  Length of 'Hello': {len(single)}")
print(f"  Uppercase : {single.upper()}")
print(f"  Concatenate: {single + ' ' + double}")

# ---------------------
# 4. List
# ---------------------
print("\n[4] LIST (ordered, mutable)")
skills = ["Python", "C", "Embedded C", "Arduino"]
print(f"  List      : {skills}")
print(f"  Length    : {len(skills)}")
print(f"  Index [0] : {skills[0]}")
print(f"  Index [-1]: {skills[-1]}")   # last element
skills.append("STM32")
print(f"  After append: {skills}")

# ---------------------
# 5. Tuple
# ---------------------
print("\n[5] TUPLE (ordered, immutable)")
coords = (17.38, 76.15)    # lat/long of Mangalore region
print(f"  Tuple     : {coords}")
print(f"  Latitude  : {coords[0]}")
print(f"  Longitude : {coords[1]}")
# coords[0] = 18  # This would throw TypeError — tuples are immutable

# ---------------------
# 6. Set
# ---------------------
print("\n[6] SET (unordered, unique elements)")
languages = {"Python", "C", "C++", "Python", "C"}  # duplicates removed
print(f"  Set       : {languages}")
print(f"  Length    : {len(languages)}")
languages.add("Java")
print(f"  After add : {languages}")

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(f"\n  Union        : {a | b}")
print(f"  Intersection : {a & b}")
print(f"  Difference   : {a - b}")

# ---------------------
# 7. Dictionary
# ---------------------
print("\n[7] DICTIONARY (key-value pairs)")
student = {
    "name"   : "Pavan Shetty H S",
    "branch" : "Electronics",
    "cgpa"   : 8.5,
    "skills" : ["Python", "C", "Embedded C"]
}
print(f"  Dict      : {student}")
print(f"  Name      : {student['name']}")
print(f"  CGPA      : {student['cgpa']}")
print(f"  Skills    : {student['skills']}")
student["year"] = 3   # adding new key
print(f"  After add : year = {student['year']}")

# ---------------------
# 8. None Type
# ---------------------
print("\n[8] NONE TYPE")
result = None
print(f"  None      : {result}")
print(f"  Type      : {type(result)}")
print(f"  Is None   : {result is None}")

# ---------------------
# Type Checking Summary
# ---------------------
print("\n[9] TYPE CHECKING")
items = [42, 3.14, "hello", True, [1,2], (3,4), {5,6}, {"a":1}, None]
for item in items:
    print(f"  {str(item):20} → {type(item).__name__}")

print("\n" + "=" * 50)
print("  Data Types demo complete!")
print("=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 DataTypes.py
# =============================================================================
#
# ==================================================
#      PYTHON DATA TYPES DEMO
# ==================================================
#
# [1] NUMERIC TYPES
#   int        : 22    | type: <class 'int'>
#   big int    : 99999999999999999999999999
#   binary 0b1010 = 10
#   octal  0o17   = 15
#   hex    0xFF   = 255
#
#   float      : 3.14159  | type: <class 'float'>
#   scientific : 2500.0     | 2.5e3 = 2500.0
#
#   complex    : (3+4j)
#   real part  : 3.0
#   imag part  : 4.0
#   magnitude  : 5.0
#
# [2] BOOLEAN
#   True   : True
#   False  : False
#   bool is subclass of int: True == 1 is True
#   True + True = 2
#   True * 5    = 5
#
# [3] STRING
#   Single quotes : Hello
#   Double quotes : World
#   Multiline     :
# This is
# a multiline
# string
#   Length of 'Hello': 5
#   Uppercase : HELLO
#   Concatenate: Hello World
#
# [4] LIST (ordered, mutable)
#   List      : ['Python', 'C', 'Embedded C', 'Arduino']
#   Length    : 4
#   Index [0] : Python
#   Index [-1]: Arduino
#   After append: ['Python', 'C', 'Embedded C', 'Arduino', 'STM32']
#
# [5] TUPLE (ordered, immutable)
#   Tuple     : (17.38, 76.15)
#   Latitude  : 17.38
#   Longitude : 76.15
#
# [6] SET (unordered, unique elements)
#   Set       : {'C++', 'Python', 'C'}
#   Length    : 3
#   After add : {'C++', 'Java', 'Python', 'C'}
#
#   Union        : {1, 2, 3, 4, 5, 6}
#   Intersection : {3, 4}
#   Difference   : {1, 2}
#
# [7] DICTIONARY (key-value pairs)
#   Dict      : {'name': 'Pavan Shetty H S', 'branch': 'Electronics', 'cgpa': 8.5, 'skills': ['Python', 'C', 'Embedded C']}
#   Name      : Pavan Shetty H S
#   CGPA      : 8.5
#   Skills    : ['Python', 'C', 'Embedded C']
#   After add : year = 3
#
# [8] NONE TYPE
#   None      : None
#   Type      : <class 'NoneType'>
#   Is None   : True
#
# [9] TYPE CHECKING
#   42                   → int
#   3.14                 → float
#   hello                → str
#   True                 → bool
#   [1, 2]               → list
#   (3, 4)               → tuple
#   {5, 6}               → set
#   {'a': 1}             → dict
#   None                 → NoneType
#
# ==================================================
#   Data Types demo complete!
# ==================================================
#
# =============================================================================

