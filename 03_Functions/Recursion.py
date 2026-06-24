# =============================================================================
# Recursion.py
# Author  : Pavan Shetty H S
# Date    : February 2024
# Topic   : Recursive Functions
# =============================================================================
#
# Notes from Pavan:
# Recursion always takes me a moment to mentally re-load, even though I
# learned it in C first. The trick that finally made it click for me:
# trust the recursive call to do its job correctly for the smaller problem,
# don't try to trace through every single call in your head.
#
# Python's default recursion limit is 1000 (sys.getrecursionlimit()).
# Hit a RecursionError once when I forgot a base case. Good reminder that
# infinite recursion crashes just like infinite loops, just with a
# different error message and a much scarier stack trace.
#
# =============================================================================

import sys

print("=" * 50)
print("       RECURSION DEMO")
print("=" * 50)

print(f"\nDefault recursion limit: {sys.getrecursionlimit()}")

# ---------------------
# Classic example: Factorial
# ---------------------
def factorial(n):
    """Base case: factorial(0) = 1
    Recursive case: factorial(n) = n * factorial(n-1)"""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print("\n[1] Factorial")
for i in [0, 1, 5, 10]:
    print(f"  factorial({i}) = {factorial(i)}")

# ---------------------
# Fibonacci -- naive recursive version
# ---------------------
def fibonacci(n):
    """Naive version -- exponential time complexity O(2^n)
    Got VERY slow when I tried fibonacci(35). Learned about memoization
    after this to fix it (see below)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("\n[2] Fibonacci (naive recursion)")
fib_sequence = [fibonacci(i) for i in range(10)]
print(f"  First 10 Fibonacci numbers: {fib_sequence}")

# ---------------------
# Fibonacci with memoization -- much faster
# ---------------------
def fibonacci_memo(n, memo={}):
    """Optimized version using a memo dict to cache results.
    This was my first real exposure to Dynamic Programming concepts.
    Turned O(2^n) into O(n) -- massive difference for large n."""
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]

print("\n[3] Fibonacci (memoized -- much faster)")
print(f"  fibonacci_memo(30) = {fibonacci_memo(30)}")
print(f"  fibonacci_memo(50) = {fibonacci_memo(50)}")
print("  (naive version would take forever for n=50)")

# ---------------------
# Sum of digits (recursive)
# ---------------------
def sum_of_digits(n):
    """Base case: single digit returns itself
    Recursive case: last digit + sum_of_digits(remaining digits)"""
    if n < 10:
        return n
    return n % 10 + sum_of_digits(n // 10)

print("\n[4] Sum of digits")
print(f"  sum_of_digits(12345) = {sum_of_digits(12345)}")

# ---------------------
# Reverse a string recursively
# ---------------------
def reverse_string(s):
    """Base case: empty string or single char
    Recursive case: last char + reverse of remaining string"""
    if len(s) <= 1:
        return s
    return s[-1] + reverse_string(s[:-1])

print("\n[5] Reverse string recursively")
print(f"  reverse_string('Pavan') = {reverse_string('Pavan')}")

# ---------------------
# GCD using recursion (Euclidean algorithm)
# ---------------------
def gcd(a, b):
    """Classic Euclidean algorithm, did this in C class too."""
    if b == 0:
        return a
    return gcd(b, a % b)

print("\n[6] GCD (Euclidean algorithm)")
print(f"  gcd(48, 18) = {gcd(48, 18)}")

# ---------------------
# What happens with no base case (commented out -- crashes!)
# ---------------------
print("\n[7] What happens without a base case (demonstration, not run)")
print("""
  def broken_recursion(n):
      return broken_recursion(n - 1)   # NO base case!

  Calling this throws:
  RecursionError: maximum recursion depth exceeded
""")

print("=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Recursion.py
# =============================================================================
#
# ==================================================
#        RECURSION DEMO
# ==================================================
#
# Default recursion limit: 1000
#
# [1] Factorial
#   factorial(0) = 1
#   factorial(1) = 1
#   factorial(5) = 120
#   factorial(10) = 3628800
#
# [2] Fibonacci (naive recursion)
#   First 10 Fibonacci numbers: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
#
# [3] Fibonacci (memoized -- much faster)
#   fibonacci_memo(30) = 832040
#   fibonacci_memo(50) = 12586269025
#   (naive version would take forever for n=50)
#
# [4] Sum of digits
#   sum_of_digits(12345) = 15
#
# [5] Reverse string recursively
#   reverse_string('Pavan') = navaP
#
# [6] GCD (Euclidean algorithm)
#   gcd(48, 18) = 6
#
# [7] What happens without a base case (demonstration, not run)
#
#   def broken_recursion(n):
#       return broken_recursion(n - 1)   # NO base case!
#
#   Calling this throws:
#   RecursionError: maximum recursion depth exceeded
#
# ==================================================
#
# =============================================================================

