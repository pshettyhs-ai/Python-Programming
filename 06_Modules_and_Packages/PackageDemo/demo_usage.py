# =============================================================================
# demo_usage.py
# Author  : Pavan Shetty H S
# Date    : March 2024
# Topic   : Demonstrates importing from the PackageDemo package
# =============================================================================
#
# Notes from Pavan:
# This is how I'd actually USE the package I built. Run this from the
# 06_Modules_and_Packages directory (not from inside PackageDemo) with:
#   python -m PackageDemo.demo_usage
#
# Relative imports inside packages confused me a LOT initially. The error
# "attempted relative import with no known parent package" showed up
# multiple times until I understood that you need to run package code as
# a MODULE (-m flag) from the parent directory, not directly as a script.
# =============================================================================

# Importing directly from the package (thanks to __init__.py exposing these)
from PackageDemo import reverse_text, count_vowels, is_even, average

print("=" * 50)
print("    PACKAGE IMPORT DEMO")
print("=" * 50)

text = "Pavan Shetty"
print(f"\nreverse_text('{text}') = {reverse_text(text)}")
print(f"count_vowels('{text}') = {count_vowels(text)}")

nums = [2, 4, 6, 8, 9]
print(f"\nis_even(7) = {is_even(7)}")
print(f"average({nums}) = {average(nums)}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: cd 06_Modules_and_Packages && python3 -m PackageDemo.demo_usage
# =============================================================================
#
# NOTE: As this file's own header comment explains, it must be run as a
# package module from the PARENT directory (06_Modules_and_Packages),
# not directly from inside PackageDemo/ -- otherwise 'from PackageDemo
# import ...' fails with ModuleNotFoundError. The output below was
# captured by running exactly the command this file documents:
#   cd 06_Modules_and_Packages && python3 -m PackageDemo.demo_usage
#
# ==================================================
#     PACKAGE IMPORT DEMO
# ==================================================
#
# reverse_text('Pavan Shetty') = yttehS navaP
# count_vowels('Pavan Shetty') = 3
#
# is_even(7) = False
# average([2, 4, 6, 8, 9]) = 5.8
#
# ==================================================
#
# =============================================================================

