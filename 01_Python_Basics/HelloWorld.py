# =============================================================================
# HelloWorld.py
# Author  : Pavan Shetty H S
# Date    : January 2024
# Topic   : My very first Python script
# =============================================================================
#
# Notes from Pavan:
# Coming from C/C++, the first thing that felt weird was no semicolons and no
# curly braces. Took me half a day to stop putting them out of habit.
# Also the print syntax is cleaner than printf — I'll give Python that.
#
# In C:   printf("Hello, World!\n");
# Python: print("Hello, World!")    <-- so much simpler
#
# =============================================================================

# Basic print
print("Hello, World!")

# Print with formatting
print("=" * 40)
print("  Hello from Pavan Shetty H S!")
print("  Aspiring Software & Embedded Engineer")
print("=" * 40)

# Multiple values in one print
name = "Pavan"
language = "Python"
print("My name is", name, "and I'm learning", language)

# Using f-strings (learned this in week 2, way cleaner)
year = 2024
print(f"Started Python journey in {year}")

# Print with sep and end parameters
# sep controls what goes between multiple arguments (default is space)
# end controls what comes at the end (default is newline \n)
print("Python", "is", "awesome", sep="-")
print("This won't end with newline ", end="")
print("...continuing on same line")

# Checking Python version (useful when setting up new machines)
import sys
print(f"\nPython version: {sys.version}")
print(f"Version info  : {sys.version_info.major}.{sys.version_info.minor}")

# =============================================================================
# Expected Output:
# Hello, World!
# ========================================
#   Hello from Pavan Shetty H S!
#   Aspiring Software & Embedded Engineer
# ========================================
# My name is Pavan and I'm learning Python
# Started Python journey in 2024
# Python-is-awesome
# This won't end with newline ...continuing on same line
# =============================================================================

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 HelloWorld.py
# =============================================================================
#
# Hello, World!
# ========================================
#   Hello from Pavan Shetty H S!
#   Aspiring Software & Embedded Engineer
# ========================================
# My name is Pavan and I'm learning Python
# Started Python journey in 2024
# Python-is-awesome
# This won't end with newline ...continuing on same line
#
# Python version: 3.12.3 (main, Mar  3 2026, 12:15:18) [GCC 13.3.0]
# Version info  : 3.12
#
# =============================================================================

