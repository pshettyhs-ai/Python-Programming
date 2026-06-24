# =============================================================================
# NestedIf.py
# Author  : Pavan Shetty H S
# Date    : January 2024
# Topic   : Nested If Statements
# =============================================================================
#
# Notes from Pavan:
# Nested ifs get messy fast. I learned (the hard way, after a 6-level deep
# nested if in an early project draft) that more than 2-3 levels of nesting
# usually means I should refactor into functions or use early returns.
#
# =============================================================================

print("=" * 50)
print("       NESTED IF DEMO")
print("=" * 50)

# ---------------------
# Example: Loan Eligibility Checker
# ---------------------
age = 28
income = 45000
credit_score = 720

print(f"\nApplicant: Age={age}, Income={income}, Credit Score={credit_score}")

if age >= 21:
    print("Age requirement: PASSED")
    if income >= 30000:
        print("Income requirement: PASSED")
        if credit_score >= 700:
            print("Credit score requirement: PASSED")
            print("\n✓ RESULT: Loan APPROVED")
        else:
            print("Credit score requirement: FAILED")
            print("\n✗ RESULT: Loan REJECTED (low credit score)")
    else:
        print("Income requirement: FAILED")
        print("\n✗ RESULT: Loan REJECTED (insufficient income)")
else:
    print("Age requirement: FAILED")
    print("\n✗ RESULT: Loan REJECTED (underage)")

# ---------------------
# Better way: Flattening with early returns (inside a function)
# ---------------------
# This is the refactor I eventually learned to prefer - avoids the "staircase"
print("\n--- Cleaner approach using early-exit logic ---")

def check_loan_eligibility(age, income, credit_score):
    """Same logic as above but flattened - much easier to read."""
    if age < 21:
        return "REJECTED (underage)"
    if income < 30000:
        return "REJECTED (insufficient income)"
    if credit_score < 700:
        return "REJECTED (low credit score)"
    return "APPROVED"

result = check_loan_eligibility(age, income, credit_score)
print(f"Result: {result}")

# Test with a failing case
result2 = check_loan_eligibility(19, 50000, 750)
print(f"Test case (age=19): {result2}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 NestedIf.py
# =============================================================================
#
# ==================================================
#        NESTED IF DEMO
# ==================================================
#
# Applicant: Age=28, Income=45000, Credit Score=720
# Age requirement: PASSED
# Income requirement: PASSED
# Credit score requirement: PASSED
#
# ✓ RESULT: Loan APPROVED
#
# --- Cleaner approach using early-exit logic ---
# Result: APPROVED
# Test case (age=19): REJECTED (underage)
#
# ==================================================
#
# =============================================================================

