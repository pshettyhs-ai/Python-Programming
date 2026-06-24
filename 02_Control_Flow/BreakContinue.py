# =============================================================================
# BreakContinue.py
# Author  : Pavan Shetty H S
# Date    : January 2024
# Topic   : break, continue, pass statements
# =============================================================================
#
# Notes from Pavan:
# 'pass' was new to me - C doesn't have an equivalent. It's literally a
# no-op, used as a placeholder when syntax requires a statement but you
# don't want to do anything yet. I use it constantly when stubbing out
# functions during planning.
#
# =============================================================================

print("=" * 50)
print("    BREAK, CONTINUE, PASS DEMO")
print("=" * 50)

# ---------------------
# break -- exits the loop entirely
# ---------------------
print("\n[1] break -- stop at first multiple of 7")
for num in range(1, 50):
    if num % 7 == 0:
        print(f"  Found first multiple of 7: {num}")
        break

# ---------------------
# continue -- skips current iteration, continues loop
# ---------------------
print("\n[2] continue -- print only odd numbers from 1-10")
for num in range(1, 11):
    if num % 2 == 0:
        continue   # skip even numbers
    print(f"  Odd: {num}", end="  ")
print()

# ---------------------
# pass -- does nothing, placeholder
# ---------------------
print("\n[3] pass -- placeholder for incomplete code")
for num in range(1, 6):
    if num == 3:
        pass  # TODO: add special handling for 3 later
    print(f"  Processing: {num}")

# Common real use of pass — stubbing out a function during planning
def calculate_tax(income):
    pass  # TODO: implement tax calculation logic next week

print("\n  Function 'calculate_tax' defined but not implemented (pass used)")

# Stub class while designing architecture
class FutureFeature:
    pass

print("  Class 'FutureFeature' stubbed for later development")

# ---------------------
# break and continue together
# ---------------------
print("\n[4] Combined example -- find primes up to 30")
print("  Primes:", end=" ")
for num in range(2, 31):
    is_prime = True
    for divisor in range(2, int(num ** 0.5) + 1):
        if num % divisor == 0:
            is_prime = False
            break          # no need to check further divisors
    if not is_prime:
        continue           # skip to next number
    print(num, end=" ")
print()

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 BreakContinue.py
# =============================================================================
#
# ==================================================
#     BREAK, CONTINUE, PASS DEMO
# ==================================================
#
# [1] break -- stop at first multiple of 7
#   Found first multiple of 7: 7
#
# [2] continue -- print only odd numbers from 1-10
#   Odd: 1    Odd: 3    Odd: 5    Odd: 7    Odd: 9  
#
# [3] pass -- placeholder for incomplete code
#   Processing: 1
#   Processing: 2
#   Processing: 3
#   Processing: 4
#   Processing: 5
#
#   Function 'calculate_tax' defined but not implemented (pass used)
#   Class 'FutureFeature' stubbed for later development
#
# [4] Combined example -- find primes up to 30
#   Primes: 2 3 5 7 11 13 17 19 23 29 
#
# ==================================================
#
# =============================================================================

