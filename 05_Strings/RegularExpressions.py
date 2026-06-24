# =============================================================================
# RegularExpressions.py
# Author  : Pavan Shetty H S
# Date    : March 2024
# Topic   : Regular Expressions (regex) using the 're' module
# =============================================================================
#
# Notes from Pavan:
# This took me 5 DAYS to get comfortable with. Regex syntax feels like a
# completely different language stuffed inside Python strings. I kept a
# cheat sheet open in another tab for the first 2 weeks of using this.
# Still look things up regularly, and that's fine -- nobody memorizes
# regex from scratch.
#
# Cheat sheet I built for myself while learning:
#   \d  = digit           \D = not digit
#   \w  = word char        \W = not word char
#   \s  = whitespace       \S = not whitespace
#   .   = any char (except newline)
#   *   = 0 or more        + = 1 or more       ? = 0 or 1
#   ^   = start of string  $  = end of string
#   []  = character set    {} = exact repetition count
#
# =============================================================================

import re

print("=" * 50)
print("    REGULAR EXPRESSIONS DEMO")
print("=" * 50)

# ---------------------
# re.search() -- finds first match anywhere in string
# ---------------------
print("\n[1] re.search() -- find pattern anywhere")
text = "My phone number is 9876543210"
match = re.search(r"\d{10}", text)
if match:
    print(f"  Found: {match.group()}")
    print(f"  Position: {match.span()}")

# ---------------------
# re.match() -- only checks from the START of string
# ---------------------
print("\n[2] re.match() -- only matches from beginning")
print(f"  match('Python', 'Python is fun'): {re.match(r'Python', 'Python is fun')}")
print(f"  match('fun', 'Python is fun'): {re.match(r'fun', 'Python is fun')}")
print("  (returns None because 'fun' isn't at the START)")

# ---------------------
# re.findall() -- finds ALL matches as a list
# ---------------------
print("\n[3] re.findall() -- all matches")
text2 = "Call 9876543210 or 8765432109 for support"
numbers = re.findall(r"\d{10}", text2)
print(f"  Text: '{text2}'")
print(f"  All numbers found: {numbers}")

# ---------------------
# re.sub() -- find and replace using patterns
# ---------------------
print("\n[4] re.sub() -- pattern-based replace")
messy = "Pavan   has    too    many    spaces"
cleaned = re.sub(r"\s+", " ", messy)   # replace multiple spaces with single space
print(f"  Before: '{messy}'")
print(f"  After : '{cleaned}'")

# ---------------------
# Email validation -- the example that finally made regex click for me
# ---------------------
print("\n[5] Practical: Email validation")
email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

test_emails = [
    "pavan.shetty@gmail.com",
    "invalid-email",
    "test@domain",
    "good.email123@company.co.in"
]

for email in test_emails:
    is_valid = bool(re.match(email_pattern, email))
    status = "✓ VALID" if is_valid else "✗ INVALID"
    print(f"  {email:35} {status}")

# ---------------------
# Phone number validation (Indian format)
# ---------------------
print("\n[6] Practical: Indian phone number validation")
phone_pattern = r"^[6-9]\d{9}$"   # starts with 6-9, total 10 digits

test_phones = ["9876543210", "1234567890", "98765432", "8123456789"]
for phone in test_phones:
    is_valid = bool(re.match(phone_pattern, phone))
    status = "✓ VALID" if is_valid else "✗ INVALID"
    print(f"  {phone:15} {status}")

# ---------------------
# Extracting structured data
# ---------------------
print("\n[7] Practical: Extracting data from log lines")
log_line = "2024-03-15 14:32:10 ERROR Failed to connect to database"
log_pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)"

match = re.match(log_pattern, log_line)
if match:
    date, time, level, message = match.groups()
    print(f"  Date    : {date}")
    print(f"  Time    : {time}")
    print(f"  Level   : {level}")
    print(f"  Message : {message}")

# ---------------------
# Compiling patterns for reuse (performance tip I learned later)
# ---------------------
print("\n[8] Compiled patterns -- faster for repeated use")
pin_pattern = re.compile(r"^\d{6}$")   # Indian PIN code
test_pins = ["575001", "12345", "ABCDEF"]
for pin in test_pins:
    print(f"  '{pin}' valid PIN: {bool(pin_pattern.match(pin))}")

print("\n" + "=" * 50)

# =============================================================================
# Debugging note: I once wrote r"\d+" thinking it would match ONLY a 10-digit
# number, but it matched ANY sequence of 1+ digits including partial matches
# inside longer numbers. Learned the hard way that you need explicit
# boundaries (^...$) or exact quantifiers ({10}) for strict validation.
# =============================================================================

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 RegularExpressions.py
# =============================================================================
#
# ==================================================
#     REGULAR EXPRESSIONS DEMO
# ==================================================
#
# [1] re.search() -- find pattern anywhere
#   Found: 9876543210
#   Position: (19, 29)
#
# [2] re.match() -- only matches from beginning
#   match('Python', 'Python is fun'): <re.Match object; span=(0, 6), match='Python'>
#   match('fun', 'Python is fun'): None
#   (returns None because 'fun' isn't at the START)
#
# [3] re.findall() -- all matches
#   Text: 'Call 9876543210 or 8765432109 for support'
#   All numbers found: ['9876543210', '8765432109']
#
# [4] re.sub() -- pattern-based replace
#   Before: 'Pavan   has    too    many    spaces'
#   After : 'Pavan has too many spaces'
#
# [5] Practical: Email validation
#   pavan.shetty@gmail.com              ✓ VALID
#   invalid-email                       ✗ INVALID
#   test@domain                         ✗ INVALID
#   good.email123@company.co.in         ✓ VALID
#
# [6] Practical: Indian phone number validation
#   9876543210      ✓ VALID
#   1234567890      ✗ INVALID
#   98765432        ✗ INVALID
#   8123456789      ✓ VALID
#
# [7] Practical: Extracting data from log lines
#   Date    : 2024-03-15
#   Time    : 14:32:10
#   Level   : ERROR
#   Message : Failed to connect to database
#
# [8] Compiled patterns -- faster for repeated use
#   '575001' valid PIN: True
#   '12345' valid PIN: False
#   'ABCDEF' valid PIN: False
#
# ==================================================
#
# =============================================================================

