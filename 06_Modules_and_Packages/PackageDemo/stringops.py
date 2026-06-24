# =============================================================================
# stringops.py
# Author  : Pavan Shetty H S
# Part of : PackageDemo package
# =============================================================================

def reverse_text(text):
    """Reverses a string."""
    return text[::-1]

def count_vowels(text):
    """Counts vowels in a string (case-insensitive)."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in text if char in vowels)

def title_case(text):
    """Converts text to title case."""
    return text.title()

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 stringops.py
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

