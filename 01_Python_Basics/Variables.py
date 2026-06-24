# =============================================================================
# Variables.py
# Author  : Pavan Shetty H S
# Date    : January 2024
# Topic   : Variables, Constants, and Naming Conventions
# =============================================================================
#
# Notes from Pavan:
# Biggest difference from C: No type declaration. Python figures it out.
# At first this felt wrong — I kept wanting to write "int x = 5;"
# But it grows on you. Dynamic typing is powerful once you trust it.
#
# BUG I HIT: Variable names are case-sensitive. Spent 20 mins debugging
# because I used 'Name' in one place and 'name' in another. Classic.
#
# =============================================================================

# ---------------------
# Basic Variable Assignment
# ---------------------
name = "Pavan Shetty H S"          # string
age = 22                             # integer
gpa = 8.5                            # float
is_student = True                    # boolean

print("--- Basic Variables ---")
print(f"Name       : {name}")
print(f"Age        : {age}")
print(f"GPA        : {gpa}")
print(f"Is Student : {is_student}")

# ---------------------
# Dynamic Typing
# ---------------------
# In Python, a variable can change type (unlike C/C++)
x = 10
print(f"\nx is int    : {x}, type: {type(x)}")

x = 10.5
print(f"x is float  : {x}, type: {type(x)}")

x = "now a string"
print(f"x is string : {x}, type: {type(x)}")

# ---------------------
# Multiple Assignment
# ---------------------
# Python trick that C doesn't have — assign multiple variables in one line
a, b, c = 10, 20, 30
print(f"\na={a}, b={b}, c={c}")

# Assign same value to multiple variables
p = q = r = 100
print(f"p={p}, q={q}, r={r}")

# Swap without temp variable (this one impressed me)
# In C you need a temp variable. Python does it elegantly.
x, y = 5, 10
print(f"\nBefore swap: x={x}, y={y}")
x, y = y, x
print(f"After swap : x={x}, y={y}")

# ---------------------
# Constants (Python convention)
# ---------------------
# Python has no true constants (unlike #define in C)
# Convention: use ALL_CAPS to indicate a constant
PI = 3.14159
MAX_SIZE = 100
DB_HOST = "localhost"

print(f"\nPI       : {PI}")
print(f"MAX_SIZE : {MAX_SIZE}")
print(f"DB_HOST  : {DB_HOST}")

# ---------------------
# Variable Naming Rules
# ---------------------
# VALID names
student_name = "Rahul"       # snake_case (Python standard)
studentAge = 20              # camelCase (valid but not Pythonic)
_private_var = "internal"    # underscore prefix = "private" by convention
MAX_VALUE = 999              # ALL_CAPS = constant convention

# INVALID names (would throw SyntaxError):
# 2name = "error"           # can't start with digit
# my-name = "error"         # hyphen not allowed
# class = "error"           # 'class' is a keyword

print("\n--- Valid Variable Names ---")
print(f"student_name : {student_name}")
print(f"studentAge   : {studentAge}")

# ---------------------
# Checking type and id
# ---------------------
city = "Mangalore"
print(f"\nVariable : {city}")
print(f"Type     : {type(city)}")
print(f"ID (memory address): {id(city)}")

# ---------------------
# Deleting a variable
# ---------------------
temp = "temporary"
print(f"\ntemp before del: {temp}")
del temp
# print(temp)  # This would throw NameError — uncomment to see it

# ---------------------
# None — Python's null
# ---------------------
result = None
print(f"\nresult = {result}")
print(f"result is None: {result is None}")

# In embedded systems context: None is like a NULL pointer in C.
# Very useful for "not yet assigned" states.

print("\n--- Program Complete ---")

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Variables.py
# =============================================================================
#
# --- Basic Variables ---
# Name       : Pavan Shetty H S
# Age        : 22
# GPA        : 8.5
# Is Student : True
#
# x is int    : 10, type: <class 'int'>
# x is float  : 10.5, type: <class 'float'>
# x is string : now a string, type: <class 'str'>
#
# a=10, b=20, c=30
# p=100, q=100, r=100
#
# Before swap: x=5, y=10
# After swap : x=10, y=5
#
# PI       : 3.14159
# MAX_SIZE : 100
# DB_HOST  : localhost
#
# --- Valid Variable Names ---
# student_name : Rahul
# studentAge   : 20
#
# Variable : Mangalore
# Type     : <class 'str'>
# ID (memory address): 140713775347952
#
# temp before del: temporary
#
# result = None
# result is None: True
#
# --- Program Complete ---
#
# =============================================================================

