# =============================================================================
# Functions.py
# Author  : Pavan Shetty H S
# Date    : February 2024
# Topic   : Function Definition, Parameters, Return Values, Scope
# =============================================================================
#
# Notes from Pavan:
# Functions in Python feel so much lighter than C. No need to declare
# return type or parameter types upfront. Default arguments and keyword
# arguments are things C doesn't have natively, and they save SO much
# code duplication once you get used to them.
#
# =============================================================================

print("=" * 50)
print("       FUNCTIONS DEMO")
print("=" * 50)

# ---------------------
# Basic function
# ---------------------
def greet(name):
    """Simple function that greets a person by name."""
    return f"Hello, {name}! Welcome to Python."

print("\n[1] Basic function")
print(greet("Pavan"))

# ---------------------
# Function with default parameter
# ---------------------
def greet_with_title(name, title="Mr."):
    """Default parameter -- if title not provided, uses 'Mr.'"""
    return f"Hello, {title} {name}!"

print("\n[2] Default parameters")
print(greet_with_title("Shetty"))
print(greet_with_title("Shetty", "Dr."))

# ---------------------
# Multiple return values (Python's tuple trick)
# ---------------------
def get_min_max(numbers):
    """Returns both min and max -- Python lets you return multiple values
    using tuples, unlike C where you'd need pointers or a struct."""
    return min(numbers), max(numbers)

print("\n[3] Multiple return values")
nums = [45, 12, 78, 23, 90, 5]
low, high = get_min_max(nums)
print(f"  Numbers: {nums}")
print(f"  Min={low}, Max={high}")

# ---------------------
# *args -- variable number of positional arguments
# ---------------------
def sum_all(*args):
    """*args collects extra positional arguments into a tuple."""
    total = 0
    for num in args:
        total += num
    return total

print("\n[4] *args -- variable arguments")
print(f"  sum_all(1,2,3) = {sum_all(1, 2, 3)}")
print(f"  sum_all(1,2,3,4,5) = {sum_all(1, 2, 3, 4, 5)}")

# ---------------------
# **kwargs -- variable number of keyword arguments
# ---------------------
def print_profile(**kwargs):
    """**kwargs collects extra keyword arguments into a dict."""
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print("\n[5] **kwargs -- variable keyword arguments")
print_profile(name="Pavan", branch="ECE", year=3, cgpa=8.5)

# ---------------------
# Combining args and kwargs
# ---------------------
def student_record(student_id, *skills, **details):
    print(f"\n  Student ID: {student_id}")
    print(f"  Skills: {skills}")
    print(f"  Details: {details}")

print("\n[6] Combining *args and **kwargs")
student_record(101, "Python", "C", "Embedded C", name="Pavan", cgpa=8.5)

# ---------------------
# Variable Scope
# ---------------------
print("\n[7] Variable Scope (local vs global)")

counter = 0   # global variable

def increment_wrong():
    # This creates a NEW local variable 'counter', doesn't touch global!
    # This confused me badly when I first hit this — I expected the
    # outer counter to change but it didn't.
    counter = 100
    return counter

def increment_correct():
    global counter   # explicitly tell Python to use the global variable
    counter += 1
    return counter

print(f"  Initial counter: {counter}")
increment_wrong()
print(f"  After increment_wrong(): {counter}  <-- unchanged! local shadow")
increment_correct()
print(f"  After increment_correct(): {counter}  <-- changed via global keyword")

# ---------------------
# Nested functions and closures
# ---------------------
print("\n[8] Nested functions / closures")

def outer_function(message):
    def inner_function():
        print(f"  Inner says: {message}")  # accesses outer's variable
    return inner_function

my_func = outer_function("Hello from closure!")
my_func()

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Functions.py
# =============================================================================
#
# ==================================================
#        FUNCTIONS DEMO
# ==================================================
#
# [1] Basic function
# Hello, Pavan! Welcome to Python.
#
# [2] Default parameters
# Hello, Mr. Shetty!
# Hello, Dr. Shetty!
#
# [3] Multiple return values
#   Numbers: [45, 12, 78, 23, 90, 5]
#   Min=5, Max=90
#
# [4] *args -- variable arguments
#   sum_all(1,2,3) = 6
#   sum_all(1,2,3,4,5) = 15
#
# [5] **kwargs -- variable keyword arguments
#   name: Pavan
#   branch: ECE
#   year: 3
#   cgpa: 8.5
#
# [6] Combining *args and **kwargs
#
#   Student ID: 101
#   Skills: ('Python', 'C', 'Embedded C')
#   Details: {'name': 'Pavan', 'cgpa': 8.5}
#
# [7] Variable Scope (local vs global)
#   Initial counter: 0
#   After increment_wrong(): 0  <-- unchanged! local shadow
#   After increment_correct(): 1  <-- changed via global keyword
#
# [8] Nested functions / closures
#   Inner says: Hello from closure!
#
# ==================================================
#
# =============================================================================

