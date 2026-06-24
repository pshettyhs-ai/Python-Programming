# =============================================================================
# TypeCasting.py
# Author  : Pavan Shetty H S
# Date    : January 2024
# Topic   : Type Conversion (Implicit & Explicit)
# =============================================================================
#
# Notes from Pavan:
# Python does implicit conversion (type coercion) automatically in some
# cases, like int + float = float. But for most things, especially user
# input, I have to explicitly cast. Documenting the gotchas I found below.
#
# =============================================================================

print("=" * 50)
print("       TYPE CASTING DEMO")
print("=" * 50)

# ---------------------
# Implicit Type Conversion (Python does it automatically)
# ---------------------
print("\n[1] IMPLICIT CONVERSION")
a = 10        # int
b = 3.5       # float
c = a + b     # Python auto-converts int to float for the operation
print(f"  int {a} + float {b} = {c}  (type: {type(c).__name__})")

x = True
y = 10
z = x + y     # bool is treated as int (True=1, False=0)
print(f"  bool {x} + int {y} = {z}  (type: {type(z).__name__})")

# ---------------------
# Explicit Type Conversion
# ---------------------
print("\n[2] EXPLICIT CONVERSION (typecasting)")

# str to int
age_str = "25"
age_int = int(age_str)
print(f"  int('{age_str}') = {age_int}  (type: {type(age_int).__name__})")

# str to float
price_str = "499.99"
price_float = float(price_str)
print(f"  float('{price_str}') = {price_float}")

# int to str
count = 42
count_str = str(count)
print(f"  str({count}) = '{count_str}'  (type: {type(count_str).__name__})")

# int to float
num = 7
num_float = float(num)
print(f"  float({num}) = {num_float}")

# float to int (TRUNCATES, doesn't round!)
pi = 3.99999
pi_int = int(pi)
print(f"  int({pi}) = {pi_int}  <-- truncates, doesn't round! Caught me off guard.")

# ---------------------
# GOTCHA: int() on invalid string crashes
# ---------------------
print("\n[3] COMMON ERRORS I HIT")
try:
    bad = int("hello")
except ValueError as e:
    print(f"  int('hello') failed: {e}")

try:
    bad2 = int("3.5")   # Can't directly convert decimal string to int!
except ValueError as e:
    print(f"  int('3.5') failed: {e}")
    print(f"  Fix: int(float('3.5')) = {int(float('3.5'))}")

# ---------------------
# List/Tuple/Set conversions
# ---------------------
print("\n[4] COLLECTION TYPE CASTING")
my_list = [1, 2, 3, 2, 1]
my_tuple = tuple(my_list)
my_set = set(my_list)     # removes duplicates!

print(f"  list  : {my_list}")
print(f"  tuple : {my_tuple}")
print(f"  set   : {my_set}  <-- duplicates removed automatically")

back_to_list = list(my_set)
print(f"  set back to list: {back_to_list}")

# String to list of characters
word = "Python"
char_list = list(word)
print(f"\n  list('{word}') = {char_list}")

# ---------------------
# bool() conversions — what counts as True/False
# ---------------------
print("\n[5] BOOL CONVERSIONS — Truthy and Falsy values")
test_values = [0, 1, -1, "", "hello", [], [1], {}, None, 0.0]
for val in test_values:
    print(f"  bool({val!r:10}) = {bool(val)}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 TypeCasting.py
# =============================================================================
#
# ==================================================
#        TYPE CASTING DEMO
# ==================================================
#
# [1] IMPLICIT CONVERSION
#   int 10 + float 3.5 = 13.5  (type: float)
#   bool True + int 10 = 11  (type: int)
#
# [2] EXPLICIT CONVERSION (typecasting)
#   int('25') = 25  (type: int)
#   float('499.99') = 499.99
#   str(42) = '42'  (type: str)
#   float(7) = 7.0
#   int(3.99999) = 3  <-- truncates, doesn't round! Caught me off guard.
#
# [3] COMMON ERRORS I HIT
#   int('hello') failed: invalid literal for int() with base 10: 'hello'
#   int('3.5') failed: invalid literal for int() with base 10: '3.5'
#   Fix: int(float('3.5')) = 3
#
# [4] COLLECTION TYPE CASTING
#   list  : [1, 2, 3, 2, 1]
#   tuple : (1, 2, 3, 2, 1)
#   set   : {1, 2, 3}  <-- duplicates removed automatically
#   set back to list: [1, 2, 3]
#
#   list('Python') = ['P', 'y', 't', 'h', 'o', 'n']
#
# [5] BOOL CONVERSIONS — Truthy and Falsy values
#   bool(0         ) = False
#   bool(1         ) = True
#   bool(-1        ) = True
#   bool(''        ) = False
#   bool('hello'   ) = True
#   bool([]        ) = False
#   bool([1]       ) = True
#   bool({}        ) = False
#   bool(None      ) = False
#   bool(0.0       ) = False
#
# ==================================================
#
# =============================================================================

