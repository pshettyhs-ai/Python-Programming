# =============================================================================
# Operators.py
# Author  : Pavan Shetty H S
# Date    : January 2024
# Topic   : All Python Operators with Examples
# =============================================================================
#
# Notes from Pavan:
# Most operators are the same as C/C++. Key differences:
#   - // is integer division (floor division)
#   - ** is power operator (no need for pow() function)
#   - 'and', 'or', 'not' instead of &&, ||, !
#   - 'is' checks identity (memory address), not value equality
#
# The 'is' vs '==' thing caught me out multiple times. is checks if two
# variables point to the SAME object in memory. == checks if the values
# are equal. They're different and I kept mixing them up.
#
# =============================================================================

print("=" * 50)
print("         PYTHON OPERATORS")
print("=" * 50)

# ---------------------
# 1. Arithmetic Operators
# ---------------------
print("\n[1] ARITHMETIC OPERATORS")
a, b = 17, 5

print(f"  a = {a}, b = {b}")
print(f"  a + b  = {a + b}")    # Addition
print(f"  a - b  = {a - b}")    # Subtraction
print(f"  a * b  = {a * b}")    # Multiplication
print(f"  a / b  = {a / b}")    # Division (always returns float)
print(f"  a // b = {a // b}")   # Floor division (integer division like C)
print(f"  a % b  = {a % b}")    # Modulus/Remainder
print(f"  a ** b = {a ** b}")   # Power (17^5)

# ---------------------
# 2. Comparison Operators
# ---------------------
print("\n[2] COMPARISON OPERATORS")
x, y = 10, 20
print(f"  x={x}, y={y}")
print(f"  x == y : {x == y}")   # Equal
print(f"  x != y : {x != y}")   # Not equal
print(f"  x > y  : {x > y}")    # Greater than
print(f"  x < y  : {x < y}")    # Less than
print(f"  x >= y : {x >= y}")   # Greater than or equal
print(f"  x <= y : {x <= y}")   # Less than or equal

# ---------------------
# 3. Logical Operators
# ---------------------
print("\n[3] LOGICAL OPERATORS (and, or, not)")
p, q = True, False
print(f"  p={p}, q={q}")
print(f"  p and q : {p and q}")
print(f"  p or  q : {p or q}")
print(f"  not p   : {not p}")

# Practical example
marks = 72
attendance = 82
result = marks >= 50 and attendance >= 75
print(f"\n  Marks={marks}, Attendance={attendance}")
print(f"  Passed (marks>=50 and attendance>=75): {result}")

# ---------------------
# 4. Assignment Operators
# ---------------------
print("\n[4] ASSIGNMENT OPERATORS")
n = 10
print(f"  n = {n}")
n += 5;  print(f"  n += 5  → {n}")
n -= 3;  print(f"  n -= 3  → {n}")
n *= 2;  print(f"  n *= 2  → {n}")
n //= 4; print(f"  n //= 4 → {n}")
n **= 3; print(f"  n **= 3 → {n}")
n %= 7;  print(f"  n %= 7  → {n}")

# ---------------------
# 5. Bitwise Operators
# ---------------------
# These are really important in embedded systems!
print("\n[5] BITWISE OPERATORS (critical for embedded/hardware work)")
a, b = 12, 10    # 12 = 1100, 10 = 1010 in binary
print(f"  a = {a} (binary: {bin(a)})")
print(f"  b = {b} (binary: {bin(b)})")
print(f"  a & b  = {a & b}  (AND)  {bin(a & b)}")
print(f"  a | b  = {a | b}  (OR)   {bin(a | b)}")
print(f"  a ^ b  = {a ^ b}  (XOR)  {bin(a ^ b)}")
print(f"  ~a     = {~a}  (NOT)  {bin(~a)}")
print(f"  a << 1 = {a << 1}  (left shift)  {bin(a << 1)}")
print(f"  a >> 1 = {a >> 1}   (right shift) {bin(a >> 1)}")

# Embedded use case: setting/clearing bits in a register
register = 0b00000000
BIT3 = (1 << 3)    # mask for bit 3
register |= BIT3   # SET bit 3
print(f"\n  Embedded example:")
print(f"  Register after setting bit3: {bin(register)}")
register &= ~BIT3  # CLEAR bit 3
print(f"  Register after clearing bit3: {bin(register)}")

# ---------------------
# 6. Identity Operators
# ---------------------
print("\n[6] IDENTITY OPERATORS (is, is not)")
a = [1, 2, 3]
b = [1, 2, 3]
c = a            # c points to SAME object as a

print(f"  a == b  : {a == b}")    # True  — same values
print(f"  a is b  : {a is b}")    # False — different objects
print(f"  a is c  : {a is c}")    # True  — same object!
print(f"  id(a)={id(a)}, id(b)={id(b)}, id(c)={id(c)}")

# Small integers are cached in Python (-5 to 256)
x = 100
y = 100
print(f"\n  x=100, y=100 → x is y: {x is y}  (small ints are cached)")
x = 1000
y = 1000
print(f"  x=1000, y=1000 → x is y: {x is y} (large ints not cached)")

# ---------------------
# 7. Membership Operators
# ---------------------
print("\n[7] MEMBERSHIP OPERATORS (in, not in)")
fruits = ["apple", "banana", "mango"]
print(f"  fruits = {fruits}")
print(f"  'mango' in fruits    : {'mango' in fruits}")
print(f"  'grape' not in fruits: {'grape' not in fruits}")

text = "Pavan Shetty"
print(f"\n  '{text}' contains 'Shetty': {'Shetty' in text}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Operators.py
# =============================================================================
#
# ==================================================
#          PYTHON OPERATORS
# ==================================================
#
# [1] ARITHMETIC OPERATORS
#   a = 17, b = 5
#   a + b  = 22
#   a - b  = 12
#   a * b  = 85
#   a / b  = 3.4
#   a // b = 3
#   a % b  = 2
#   a ** b = 1419857
#
# [2] COMPARISON OPERATORS
#   x=10, y=20
#   x == y : False
#   x != y : True
#   x > y  : False
#   x < y  : True
#   x >= y : False
#   x <= y : True
#
# [3] LOGICAL OPERATORS (and, or, not)
#   p=True, q=False
#   p and q : False
#   p or  q : True
#   not p   : False
#
#   Marks=72, Attendance=82
#   Passed (marks>=50 and attendance>=75): True
#
# [4] ASSIGNMENT OPERATORS
#   n = 10
#   n += 5  → 15
#   n -= 3  → 12
#   n *= 2  → 24
#   n //= 4 → 6
#   n **= 3 → 216
#   n %= 7  → 6
#
# [5] BITWISE OPERATORS (critical for embedded/hardware work)
#   a = 12 (binary: 0b1100)
#   b = 10 (binary: 0b1010)
#   a & b  = 8  (AND)  0b1000
#   a | b  = 14  (OR)   0b1110
#   a ^ b  = 6  (XOR)  0b110
#   ~a     = -13  (NOT)  -0b1101
#   a << 1 = 24  (left shift)  0b11000
#   a >> 1 = 6   (right shift) 0b110
#
#   Embedded example:
#   Register after setting bit3: 0b1000
#   Register after clearing bit3: 0b0
#
# [6] IDENTITY OPERATORS (is, is not)
#   a == b  : True
#   a is b  : False
#   a is c  : True
#   id(a)=139841496599360, id(b)=139841496601152, id(c)=139841496599360
#
#   x=100, y=100 → x is y: True  (small ints are cached)
#   x=1000, y=1000 → x is y: True (large ints not cached)
#
# [7] MEMBERSHIP OPERATORS (in, not in)
#   fruits = ['apple', 'banana', 'mango']
#   'mango' in fruits    : True
#   'grape' not in fruits: True
#
#   'Pavan Shetty' contains 'Shetty': True
#
# ==================================================
#
# =============================================================================

