# =============================================================================
# mathops.py
# Author  : Pavan Shetty H S
# Part of : PackageDemo package
# =============================================================================

def is_even(n):
    """Returns True if n is even."""
    return n % 2 == 0

def average(numbers):
    """Returns the average of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def is_prime(n):
    """Checks primality."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 mathops.py
# =============================================================================
#
# NOTE: This module defines functions only and calls none of them at
# module level, so running it directly produces no output at all. This
# is correct -- the functions are meant to be imported and used by
# other code (see demo_usage.py for that).
#
# (no output)
#
# =============================================================================

