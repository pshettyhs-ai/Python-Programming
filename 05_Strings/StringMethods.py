# =============================================================================
# StringMethods.py
# Author  : Pavan Shetty H S
# Date    : March 2024
# Topic   : String Methods & Manipulation
# =============================================================================
#
# Notes from Pavan:
# Strings in Python are IMMUTABLE -- every "modification" actually creates
# a new string object. This was an adjustment from C's char arrays which
# you can mutate in place. Took me a moment to realize why
# my_string[0] = 'X' throws an error.
#
# =============================================================================

print("=" * 50)
print("       STRING METHODS DEMO")
print("=" * 50)

text = "  Pavan Shetty H S  "

# ---------------------
# Immutability demo
# ---------------------
print("\n[Strings are immutable]")
s = "Hello"
try:
    s[0] = "J"
except TypeError as e:
    print(f"  Tried s[0]='J': {e}")
print("  Workaround: create a new string instead")
s = "J" + s[1:]
print(f"  New string: {s}")

# ---------------------
# Case methods
# ---------------------
print("\n[Case Conversion]")
print(f"  Original: '{text}'")
print(f"  upper()  : '{text.upper()}'")
print(f"  lower()  : '{text.lower()}'")
print(f"  title()  : '{text.title()}'")
print(f"  swapcase(): '{'Hello World'.swapcase()}'")
print(f"  capitalize(): '{'python programming'.capitalize()}'")

# ---------------------
# Whitespace handling
# ---------------------
print("\n[Whitespace]")
print(f"  Original: '{text}'")
print(f"  strip()  : '{text.strip()}'")     # removes both ends
print(f"  lstrip() : '{text.lstrip()}'")    # removes left only
print(f"  rstrip() : '{text.rstrip()}'")    # removes right only

# ---------------------
# Searching & checking
# ---------------------
print("\n[Searching & Checking]")
sentence = "Python is a powerful programming language"
print(f"  Sentence: '{sentence}'")
print(f"  startswith('Python'): {sentence.startswith('Python')}")
print(f"  endswith('language'): {sentence.endswith('language')}")
print(f"  find('powerful'): {sentence.find('powerful')}")    # returns index, -1 if not found
print(f"  find('Java'): {sentence.find('Java')}")
print(f"  count('a'): {sentence.count('a')}")
print(f"  'powerful' in sentence: {'powerful' in sentence}")

# Validation methods -- super useful for input validation
print("\n[Validation methods]")
print(f"  '12345'.isdigit(): {'12345'.isdigit()}")
print(f"  'Python3'.isalpha(): {'Python3'.isalpha()}")   # False -- has a digit
print(f"  'Python'.isalpha(): {'Python'.isalpha()}")
print(f"  'Python3'.isalnum(): {'Python3'.isalnum()}")
print(f"  '   '.isspace(): {'   '.isspace()}")
print(f"  'HELLO'.isupper(): {'HELLO'.isupper()}")

# ---------------------
# Splitting & Joining
# ---------------------
print("\n[Split & Join]")
csv_line = "Pavan,ECE,3,8.5"
parts = csv_line.split(",")
print(f"  '{csv_line}'.split(',') = {parts}")

sentence2 = "Python is fun"
words = sentence2.split()   # splits on whitespace by default
print(f"  '{sentence2}'.split() = {words}")

joined = "-".join(words)
print(f"  '-'.join({words}) = '{joined}'")

# ---------------------
# Replace
# ---------------------
print("\n[Replace]")
greeting = "Hello World, Hello Python"
print(f"  Original: '{greeting}'")
print(f"  replace('Hello','Hi'): '{greeting.replace('Hello', 'Hi')}'")
print(f"  replace('Hello','Hi',1): '{greeting.replace('Hello', 'Hi', 1)}'  (only first occurrence)")

# ---------------------
# Slicing strings (same as lists!)
# ---------------------
print("\n[Slicing]")
name = "Pavan Shetty"
print(f"  name = '{name}'")
print(f"  name[0:5] = '{name[0:5]}'")
print(f"  name[-6:] = '{name[-6:]}'")
print(f"  name[::-1] = '{name[::-1]}'  (reversed)")

# ---------------------
# Checking palindrome (practical example)
# ---------------------
print("\n[Practical: Palindrome check]")
def is_palindrome(s):
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

test_words = ["madam", "Python", "A man a plan a canal Panama"]
for word in test_words:
    print(f"  '{word}' is palindrome: {is_palindrome(word)}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 StringMethods.py
# =============================================================================
#
# ==================================================
#        STRING METHODS DEMO
# ==================================================
#
# [Strings are immutable]
#   Tried s[0]='J': 'str' object does not support item assignment
#   Workaround: create a new string instead
#   New string: Jello
#
# [Case Conversion]
#   Original: '  Pavan Shetty H S  '
#   upper()  : '  PAVAN SHETTY H S  '
#   lower()  : '  pavan shetty h s  '
#   title()  : '  Pavan Shetty H S  '
#   swapcase(): 'hELLO wORLD'
#   capitalize(): 'Python programming'
#
# [Whitespace]
#   Original: '  Pavan Shetty H S  '
#   strip()  : 'Pavan Shetty H S'
#   lstrip() : 'Pavan Shetty H S  '
#   rstrip() : '  Pavan Shetty H S'
#
# [Searching & Checking]
#   Sentence: 'Python is a powerful programming language'
#   startswith('Python'): True
#   endswith('language'): True
#   find('powerful'): 12
#   find('Java'): -1
#   count('a'): 4
#   'powerful' in sentence: True
#
# [Validation methods]
#   '12345'.isdigit(): True
#   'Python3'.isalpha(): False
#   'Python'.isalpha(): True
#   'Python3'.isalnum(): True
#   '   '.isspace(): True
#   'HELLO'.isupper(): True
#
# [Split & Join]
#   'Pavan,ECE,3,8.5'.split(',') = ['Pavan', 'ECE', '3', '8.5']
#   'Python is fun'.split() = ['Python', 'is', 'fun']
#   '-'.join(['Python', 'is', 'fun']) = 'Python-is-fun'
#
# [Replace]
#   Original: 'Hello World, Hello Python'
#   replace('Hello','Hi'): 'Hi World, Hi Python'
#   replace('Hello','Hi',1): 'Hi World, Hello Python'  (only first occurrence)
#
# [Slicing]
#   name = 'Pavan Shetty'
#   name[0:5] = 'Pavan'
#   name[-6:] = 'Shetty'
#   name[::-1] = 'yttehS navaP'  (reversed)
#
# [Practical: Palindrome check]
#   'madam' is palindrome: True
#   'Python' is palindrome: False
#   'A man a plan a canal Panama' is palindrome: True
#
# ==================================================
#
# =============================================================================

