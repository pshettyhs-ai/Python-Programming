# =============================================================================
# ReadFile.py
# Author  : Pavan Shetty H S
# Date    : April 2024
# Topic   : Reading Files in Python
# =============================================================================
#
# Notes from Pavan:
# Python's `with open(...) as f:` pattern (context manager) is something
# I now consider non-negotiable. Before I understood it, I was manually
# calling f.close() and forgetting it half the time, especially when an
# exception happened mid-read and skipped my close() call entirely.
# `with` guarantees the file closes even if an error occurs inside the block.
# =============================================================================

import os

print("=" * 50)
print("       FILE READING DEMO")
print("=" * 50)

# First, let's create a sample file to read from
sample_path = "sample_notes.txt"
with open(sample_path, "w") as f:
    f.write("Line 1: Python is fun\n")
    f.write("Line 2: File handling is essential\n")
    f.write("Line 3: Context managers prevent resource leaks\n")
    f.write("Line 4: Pavan Shetty H S - Learning Python\n")

# ---------------------
# Method 1: read() -- reads entire file as one string
# ---------------------
print("\n[1] f.read() -- entire file as one string")
with open(sample_path, "r") as f:
    content = f.read()
print(content)

# ---------------------
# Method 2: readline() -- reads one line at a time
# ---------------------
print("[2] f.readline() -- one line at a time")
with open(sample_path, "r") as f:
    line1 = f.readline()
    line2 = f.readline()
print(f"  First line : {line1.strip()}")
print(f"  Second line: {line2.strip()}")

# ---------------------
# Method 3: readlines() -- all lines as a list
# ---------------------
print("\n[3] f.readlines() -- list of all lines")
with open(sample_path, "r") as f:
    all_lines = f.readlines()
print(f"  Type: {type(all_lines)}")
for i, line in enumerate(all_lines):
    print(f"  [{i}] {line.strip()}")

# ---------------------
# Method 4: Iterating directly over file object (most memory-efficient)
# ---------------------
print("\n[4] Iterating directly -- best for LARGE files (doesn't load all into memory)")
with open(sample_path, "r") as f:
    for line_num, line in enumerate(f, start=1):
        print(f"  Line {line_num}: {line.strip()}")

# ---------------------
# Without 'with' -- the OLD way I should avoid
# ---------------------
print("\n[5] Without context manager (NOT recommended, but you'll see this in old code)")
f = open(sample_path, "r")
data = f.read()
f.close()  # easy to forget this, especially if an exception happens above!
print(f"  Read {len(data)} characters (had to manually close file)")

# ---------------------
# Handling file not found
# ---------------------
print("\n[6] Handling missing files gracefully")
try:
    with open("does_not_exist.txt", "r") as f:
        content = f.read()
except FileNotFoundError as e:
    print(f"  Caught error: {e}")

# ---------------------
# Reading with encoding specified (learned this after a UnicodeDecodeError)
# ---------------------
print("\n[7] Specifying encoding explicitly")
with open(sample_path, "r", encoding="utf-8") as f:
    content = f.read()
print(f"  Read {len(content)} characters with explicit UTF-8 encoding")

# Cleanup
os.remove(sample_path)
print(f"\n  Cleaned up: {sample_path} removed")

print("\n" + "=" * 50)

# =============================================================================
# Debugging note: Had a UnicodeDecodeError once when reading a file with
# special characters (rupee symbol in an expense tracker draft). Fixed by
# explicitly specifying encoding="utf-8" in open(). Default encoding can
# vary by OS/locale, so I now ALWAYS specify it explicitly.
# =============================================================================

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 ReadFile.py
# =============================================================================
#
# ==================================================
#        FILE READING DEMO
# ==================================================
#
# [1] f.read() -- entire file as one string
# Line 1: Python is fun
# Line 2: File handling is essential
# Line 3: Context managers prevent resource leaks
# Line 4: Pavan Shetty H S - Learning Python
#
# [2] f.readline() -- one line at a time
#   First line : Line 1: Python is fun
#   Second line: Line 2: File handling is essential
#
# [3] f.readlines() -- list of all lines
#   Type: <class 'list'>
#   [0] Line 1: Python is fun
#   [1] Line 2: File handling is essential
#   [2] Line 3: Context managers prevent resource leaks
#   [3] Line 4: Pavan Shetty H S - Learning Python
#
# [4] Iterating directly -- best for LARGE files (doesn't load all into memory)
#   Line 1: Line 1: Python is fun
#   Line 2: Line 2: File handling is essential
#   Line 3: Line 3: Context managers prevent resource leaks
#   Line 4: Line 4: Pavan Shetty H S - Learning Python
#
# [5] Without context manager (NOT recommended, but you'll see this in old code)
#   Read 148 characters (had to manually close file)
#
# [6] Handling missing files gracefully
#   Caught error: [Errno 2] No such file or directory: 'does_not_exist.txt'
#
# [7] Specifying encoding explicitly
#   Read 148 characters with explicit UTF-8 encoding
#
#   Cleaned up: sample_notes.txt removed
#
# ==================================================
#
# =============================================================================

