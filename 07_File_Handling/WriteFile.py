# =============================================================================
# WriteFile.py
# Author  : Pavan Shetty H S
# Date    : April 2024
# Topic   : Writing to Files -- modes, append, overwrite
# =============================================================================
#
# Notes from Pavan:
# The file mode ('w', 'a', 'r', 'x', etc.) matters A LOT. I once opened a
# file with 'w' mode thinking it would just let me write to it, not
# realizing 'w' WIPES the existing content first. Lost a day's worth of
# test data that way. Lesson burned into memory now.
# =============================================================================

import os

print("=" * 50)
print("       FILE WRITING DEMO")
print("=" * 50)

log_path = "activity_log.txt"

# ---------------------
# 'w' mode -- write (OVERWRITES existing content!)
# ---------------------
print("\n[1] 'w' mode -- creates new file OR overwrites existing")
with open(log_path, "w") as f:
    f.write("Log started\n")
    f.write("Entry 1: Program initialized\n")

with open(log_path, "r") as f:
    print(f.read())

# ---------------------
# 'a' mode -- append (adds to end, doesn't erase)
# ---------------------
print("[2] 'a' mode -- appends without erasing existing content")
with open(log_path, "a") as f:
    f.write("Entry 2: User logged in\n")
    f.write("Entry 3: Data processed\n")

with open(log_path, "r") as f:
    print(f.read())

# ---------------------
# THE MISTAKE I MADE -- using 'w' when I meant 'a'
# ---------------------
print("[3] Demonstrating the mistake I made")
with open(log_path, "w") as f:   # OOPS -- this wipes everything above!
    f.write("This overwrote everything that came before it\n")

with open(log_path, "r") as f:
    print(f.read())
print("  ^ Notice: Entries 1, 2, 3 are GONE. This is the bug that cost me data.")
print("  Lesson: ALWAYS double check 'w' vs 'a' before running file-writing code.")

# ---------------------
# writelines() -- write multiple lines from a list
# ---------------------
print("\n[4] writelines() -- write a list of strings")
lines = [
    "Student: Pavan\n",
    "Student: Rahul\n",
    "Student: Sneha\n"
]
with open(log_path, "w") as f:
    f.writelines(lines)   # NOTE: doesn't add newlines automatically, I add \n myself

with open(log_path, "r") as f:
    print(f.read())

# ---------------------
# 'x' mode -- exclusive creation (fails if file already exists)
# ---------------------
print("[5] 'x' mode -- fails if file already exists (safety mode)")
try:
    with open(log_path, "x") as f:   # log_path already exists from above
        f.write("This won't work")
except FileExistsError as e:
    print(f"  Caught error: {e}")
    print("  Useful when you want to make SURE you're not overwriting something")

# ---------------------
# Writing with explicit flush (rare, but useful for live logging)
# ---------------------
print("\n[6] Forcing immediate write with flush()")
with open(log_path, "w") as f:
    f.write("Important log entry\n")
    f.flush()   # forces write to disk immediately, doesn't wait for buffer
print("  Used flush() to force immediate disk write (useful in long-running scripts)")

# Cleanup
os.remove(log_path)
print(f"\n  Cleaned up: {log_path} removed")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 WriteFile.py
# =============================================================================
#
# ==================================================
#        FILE WRITING DEMO
# ==================================================
#
# [1] 'w' mode -- creates new file OR overwrites existing
# Log started
# Entry 1: Program initialized
#
# [2] 'a' mode -- appends without erasing existing content
# Log started
# Entry 1: Program initialized
# Entry 2: User logged in
# Entry 3: Data processed
#
# [3] Demonstrating the mistake I made
# This overwrote everything that came before it
#
#   ^ Notice: Entries 1, 2, 3 are GONE. This is the bug that cost me data.
#   Lesson: ALWAYS double check 'w' vs 'a' before running file-writing code.
#
# [4] writelines() -- write a list of strings
# Student: Pavan
# Student: Rahul
# Student: Sneha
#
# [5] 'x' mode -- fails if file already exists (safety mode)
#   Caught error: [Errno 17] File exists: 'activity_log.txt'
#   Useful when you want to make SURE you're not overwriting something
#
# [6] Forcing immediate write with flush()
#   Used flush() to force immediate disk write (useful in long-running scripts)
#
#   Cleaned up: activity_log.txt removed
#
# ==================================================
#
# =============================================================================

