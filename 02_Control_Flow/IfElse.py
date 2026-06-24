# =============================================================================
# IfElse.py
# Author  : Pavan Shetty H S
# Date    : January 2024
# Topic   : Conditional Statements — if, elif, else
# =============================================================================
#
# Notes from Pavan:
# Syntax is way cleaner than C's if/else if/else chains. No parentheses
# required around conditions (though you can use them), and 'elif' instead
# of writing "else if" every time saves some typing.
#
# =============================================================================

print("=" * 50)
print("       IF-ELSE DEMO")
print("=" * 50)

# ---------------------
# Basic if-else
# ---------------------
marks = 78

print(f"\nMarks: {marks}")
if marks >= 90:
    print("Grade: A+")
elif marks >= 75:
    print("Grade: A")
elif marks >= 60:
    print("Grade: B")
elif marks >= 40:
    print("Grade: C")
else:
    print("Grade: Fail")

# ---------------------
# Ternary (conditional expression)
# ---------------------
# Python doesn't have ?: like C, but has this one-line alternative
age = 20
status = "Adult" if age >= 18 else "Minor"
print(f"\nAge {age} → Status: {status}")

# ---------------------
# Multiple conditions with logical operators
# ---------------------
username = "pavan_shetty"
password = "Secure@123"

if len(username) >= 5 and len(password) >= 8:
    print("\nLogin credentials meet length requirements.")
else:
    print("\nCredentials too short.")

# ---------------------
# Checking membership in condition
# ---------------------
allowed_branches = ["CSE", "ECE", "ISE", "EEE"]
my_branch = "ECE"

if my_branch in allowed_branches:
    print(f"\n{my_branch} is an eligible branch.")
else:
    print(f"\n{my_branch} is not eligible.")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 IfElse.py
# =============================================================================
#
# ==================================================
#        IF-ELSE DEMO
# ==================================================
#
# Marks: 78
# Grade: A
#
# Age 20 → Status: Adult
#
# Login credentials meet length requirements.
#
# ECE is an eligible branch.
#
# ==================================================
#
# =============================================================================

