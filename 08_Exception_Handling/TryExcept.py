# =============================================================================
# TryExcept.py
# Author  : Pavan Shetty H S
# Date    : April 2024
# Topic   : try, except, else, finally
# =============================================================================
#
# Notes from Pavan:
# I'd already been using try/except informally in the File Handling module
# (catching FileNotFoundError, JSONDecodeError) without fully understanding
# the structure. This module is me going back to properly learn the WHY
# and HOW, not just copy-pasting patterns that seemed to work.
# =============================================================================

print("=" * 50)
print("    TRY-EXCEPT DEMO")
print("=" * 50)

# ---------------------
# Basic try-except
# ---------------------
print("\n[1] Basic try-except")
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"  Caught error: {e}")

# ---------------------
# Catching multiple specific exceptions
# ---------------------
print("\n[2] Multiple except blocks for different errors")

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("  Error: Cannot divide by zero")
        return None
    except TypeError:
        print("  Error: Both inputs must be numbers")
        return None

print(f"  safe_divide(10, 2) = {safe_divide(10, 2)}")
safe_divide(10, 0)
safe_divide(10, "two")

# ---------------------
# Catching multiple exceptions in ONE except block
# ---------------------
print("\n[3] Catching multiple exception types together")
def process_value(val):
    try:
        return int(val) * 2
    except (ValueError, TypeError) as e:
        print(f"  Caught error: {type(e).__name__}: {e}")
        return None

process_value("abc")
process_value(None)

# ---------------------
# else clause -- runs ONLY if no exception occurred
# ---------------------
print("\n[4] else clause -- code that runs only on SUCCESS")
def divide_with_else(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("  Division failed")
    else:
        print(f"  Division succeeded: {result}")  # only runs if try succeeded

divide_with_else(10, 2)
divide_with_else(10, 0)

# ---------------------
# finally -- ALWAYS runs, success or failure
# ---------------------
print("\n[5] finally -- always runs (cleanup code)")
def read_with_finally(filename):
    try:
        f = open(filename, "r")
        content = f.read()
        return content
    except FileNotFoundError:
        print(f"  File '{filename}' not found")
        return None
    finally:
        print("  finally block: cleanup always happens here")

read_with_finally("nonexistent_file_xyz.txt")

# ---------------------
# Catching the generic Exception (use SPARINGLY -- learned this lesson)
# ---------------------
print("\n[6] Generic Exception catch (use carefully!)")
try:
    risky_list = [1, 2, 3]
    print(risky_list[10])
except Exception as e:
    print(f"  Caught generic exception: {type(e).__name__}: {e}")
print("""
  My note on this: catching bare 'Exception' hides WHAT actually went
  wrong and can mask bugs you didn't intend to catch. I now try to catch
  SPECIFIC exceptions whenever I know what could go wrong, and only use
  generic Exception as a last-resort safety net at a program's outer edge.
""")

# ---------------------
# Getting full exception details
# ---------------------
print("[7] Inspecting exception details")
try:
    x = 1 / 0
except Exception as e:
    print(f"  Exception type: {type(e).__name__}")
    print(f"  Exception args: {e.args}")
    print(f"  Exception str : {str(e)}")

# ---------------------
# Nested try-except
# ---------------------
print("\n[8] Nested try-except blocks")
def parse_and_divide(a_str, b_str):
    try:
        a = int(a_str)
        b = int(b_str)
        try:
            return a / b
        except ZeroDivisionError:
            print("  Inner: division by zero")
            return None
    except ValueError:
        print("  Outer: invalid number format")
        return None

parse_and_divide("10", "0")
parse_and_divide("abc", "5")
print(f"  parse_and_divide('20','4') = {parse_and_divide('20', '4')}")

# ---------------------
# Common built-in exceptions reference (things I've actually hit)
# ---------------------
print("\n[9] Common exceptions I've personally encountered")
exceptions_table = [
    ("ValueError", "int('abc') -- invalid conversion"),
    ("TypeError", "'5' + 5 -- mismatched types"),
    ("ZeroDivisionError", "10 / 0"),
    ("IndexError", "my_list[100] -- index out of range"),
    ("KeyError", "my_dict['missing_key']"),
    ("FileNotFoundError", "open('does_not_exist.txt')"),
    ("AttributeError", "'hello'.nonexistent_method()"),
    ("ImportError", "import nonexistent_module"),
    ("NameError", "using a variable that was never defined"),
]
for exc, example in exceptions_table:
    print(f"  {exc:20} -> {example}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 TryExcept.py
# =============================================================================
#
# ==================================================
#     TRY-EXCEPT DEMO
# ==================================================
#
# [1] Basic try-except
#   Caught error: division by zero
#
# [2] Multiple except blocks for different errors
#   safe_divide(10, 2) = 5.0
#   Error: Cannot divide by zero
#   Error: Both inputs must be numbers
#
# [3] Catching multiple exception types together
#   Caught error: ValueError: invalid literal for int() with base 10: 'abc'
#   Caught error: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
#
# [4] else clause -- code that runs only on SUCCESS
#   Division succeeded: 5.0
#   Division failed
#
# [5] finally -- always runs (cleanup code)
#   File 'nonexistent_file_xyz.txt' not found
#   finally block: cleanup always happens here
#
# [6] Generic Exception catch (use carefully!)
#   Caught generic exception: IndexError: list index out of range
#
#   My note on this: catching bare 'Exception' hides WHAT actually went
#   wrong and can mask bugs you didn't intend to catch. I now try to catch
#   SPECIFIC exceptions whenever I know what could go wrong, and only use
#   generic Exception as a last-resort safety net at a program's outer edge.
#
# [7] Inspecting exception details
#   Exception type: ZeroDivisionError
#   Exception args: ('division by zero',)
#   Exception str : division by zero
#
# [8] Nested try-except blocks
#   Inner: division by zero
#   Outer: invalid number format
#   parse_and_divide('20','4') = 5.0
#
# [9] Common exceptions I've personally encountered
#   ValueError           -> int('abc') -- invalid conversion
#   TypeError            -> '5' + 5 -- mismatched types
#   ZeroDivisionError    -> 10 / 0
#   IndexError           -> my_list[100] -- index out of range
#   KeyError             -> my_dict['missing_key']
#   FileNotFoundError    -> open('does_not_exist.txt')
#   AttributeError       -> 'hello'.nonexistent_method()
#   ImportError          -> import nonexistent_module
#   NameError            -> using a variable that was never defined
#
# ==================================================
#
# =============================================================================

