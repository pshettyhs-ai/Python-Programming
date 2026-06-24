# =============================================================================
# CustomModule.py
# Author  : Pavan Shetty H S
# Date    : March 2024
# Topic   : Creating and Using Custom Modules
# =============================================================================
#
# Notes from Pavan:
# A "module" in Python is literally just any .py file. That simplicity
# surprised me -- I expected some special module-creation syntax like C's
# header files. You just write functions/classes in a file, then import
# that file's name (minus .py) elsewhere. Much less ceremony than C's
# .h/.c split.
#
# This file demonstrates math utility functions I'd typically split into
# their own module (e.g. math_utils.py) and import elsewhere.
# =============================================================================

print("=" * 50)
print("    CUSTOM MODULE DEMO")
print("=" * 50)

# ---------------------
# These functions simulate what would live in a separate "math_utils.py"
# file. In a real project, I'd save these in their own file and do:
#   import math_utils
#   or
#   from math_utils import add, is_prime
# ---------------------

def add(a, b):
    """Adds two numbers."""
    return a + b

def subtract(a, b):
    """Subtracts b from a."""
    return a - b

def is_prime(n):
    """Checks if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def factorial(n):
    """Calculates factorial iteratively (chose iterative over recursive
    here to avoid recursion depth issues for large n)."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# ---------------------
# The __name__ == "__main__" pattern
# ---------------------
# This is one of the most important patterns I learned. Code inside this
# block ONLY runs when the file is executed directly, NOT when imported
# as a module elsewhere. Took me a while to understand why this matters --
# without it, "test code" would run every time someone imports my module!
# ---------------------

if __name__ == "__main__":
    print("\nThis file is being run directly (not imported)")
    print(f"  add(5, 3) = {add(5, 3)}")
    print(f"  subtract(10, 4) = {subtract(10, 4)}")
    print(f"  is_prime(17) = {is_prime(17)}")
    print(f"  is_prime(18) = {is_prime(18)}")
    print(f"  factorial(6) = {factorial(6)}")
    print(f"\n  __name__ value here: '{__name__}'")
else:
    print(f"  This module was imported. __name__ = '{__name__}'")

# =============================================================================
# Notes on how I'd actually use this:
#
# In another file, I would do:
#   import CustomModule
#   result = CustomModule.add(5, 3)
#
# Or:
#   from CustomModule import add, is_prime
#   result = add(5, 3)
#
# Or with an alias:
#   import CustomModule as cm
#   result = cm.add(5, 3)
# =============================================================================

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 CustomModule.py
# =============================================================================
#
# ==================================================
#     CUSTOM MODULE DEMO
# ==================================================
#
# This file is being run directly (not imported)
#   add(5, 3) = 8
#   subtract(10, 4) = 6
#   is_prime(17) = True
#   is_prime(18) = False
#   factorial(6) = 720
#
#   __name__ value here: '__main__'
#
# =============================================================================

