# =============================================================================
# LambdaFunctions.py
# Author  : Pavan Shetty H S
# Date    : February 2024
# Topic   : Lambda (Anonymous) Functions
# =============================================================================
#
# Notes from Pavan:
# Lambdas felt pointless to me at first - "why not just write a normal
# function?" But once I started using map/filter/sorted with key functions,
# I understood. They're for short, throwaway functions you need inline,
# usually as arguments to other functions.
#
# Rule I follow now: if the lambda needs more than one line of logic,
# write a proper function instead. Don't force everything into a lambda.
#
# =============================================================================

print("=" * 50)
print("       LAMBDA FUNCTIONS DEMO")
print("=" * 50)

# ---------------------
# Basic lambda vs regular function
# ---------------------
print("\n[1] Lambda vs regular function")

def square_normal(x):
    return x * x

square_lambda = lambda x: x * x

print(f"  Normal function: square_normal(5) = {square_normal(5)}")
print(f"  Lambda function: square_lambda(5) = {square_lambda(5)}")

# Lambda with multiple arguments
add = lambda a, b: a + b
print(f"  add(3, 7) = {add(3, 7)}")

# ---------------------
# Lambda with map() -- apply function to every item
# ---------------------
print("\n[2] lambda + map()")
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(f"  Original: {numbers}")
print(f"  Squared : {squared}")

celsius = [0, 20, 37, 100]
fahrenheit = list(map(lambda c: (c * 9/5) + 32, celsius))
print(f"  Celsius   : {celsius}")
print(f"  Fahrenheit: {fahrenheit}")

# ---------------------
# Lambda with filter() -- keep items where condition is True
# ---------------------
print("\n[3] lambda + filter()")
nums = list(range(1, 21))
evens = list(filter(lambda x: x % 2 == 0, nums))
print(f"  Numbers 1-20: {nums}")
print(f"  Evens only  : {evens}")

# ---------------------
# Lambda with sorted() -- custom sort key
# ---------------------
print("\n[4] lambda + sorted() -- this is where lambdas really shine")
students = [
    {"name": "Rahul", "cgpa": 8.2},
    {"name": "Pavan", "cgpa": 9.1},
    {"name": "Sneha", "cgpa": 7.8},
]

# Sort by cgpa, descending
sorted_students = sorted(students, key=lambda s: s["cgpa"], reverse=True)
print("  Sorted by CGPA (highest first):")
for s in sorted_students:
    print(f"    {s['name']}: {s['cgpa']}")

# ---------------------
# Lambda with reduce() -- accumulate a single result
# ---------------------
print("\n[5] lambda + functools.reduce()")
from functools import reduce
nums = [1, 2, 3, 4, 5]
product = reduce(lambda a, b: a * b, nums)
print(f"  Numbers: {nums}")
print(f"  Product (via reduce): {product}")

# ---------------------
# When NOT to use lambda (my own rule of thumb)
# ---------------------
print("\n[6] When lambda gets too complex -- DON'T do this")
# Bad practice (hard to read):
# process = lambda x: x*2 if x > 0 else (x*-1 if x < -10 else 0)
# Better as a real function:

def process(x):
    """Clearer than cramming this logic into a lambda."""
    if x > 0:
        return x * 2
    elif x < -10:
        return x * -1
    else:
        return 0

print(f"  process(5) = {process(5)}")
print(f"  process(-15) = {process(-15)}")
print("  (Wrote this as a real function instead of a lambda for readability)")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 LambdaFunctions.py
# =============================================================================
#
# ==================================================
#        LAMBDA FUNCTIONS DEMO
# ==================================================
#
# [1] Lambda vs regular function
#   Normal function: square_normal(5) = 25
#   Lambda function: square_lambda(5) = 25
#   add(3, 7) = 10
#
# [2] lambda + map()
#   Original: [1, 2, 3, 4, 5]
#   Squared : [1, 4, 9, 16, 25]
#   Celsius   : [0, 20, 37, 100]
#   Fahrenheit: [32.0, 68.0, 98.6, 212.0]
#
# [3] lambda + filter()
#   Numbers 1-20: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
#   Evens only  : [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
#
# [4] lambda + sorted() -- this is where lambdas really shine
#   Sorted by CGPA (highest first):
#     Pavan: 9.1
#     Rahul: 8.2
#     Sneha: 7.8
#
# [5] lambda + functools.reduce()
#   Numbers: [1, 2, 3, 4, 5]
#   Product (via reduce): 120
#
# [6] When lambda gets too complex -- DON'T do this
#   process(5) = 10
#   process(-15) = 15
#   (Wrote this as a real function instead of a lambda for readability)
#
# ==================================================
#
# =============================================================================

