# =============================================================================
# ContextManagers.py
# Author  : Pavan Shetty H S
# Date    : June 2024
# Topic   : Context Managers -- with statement, __enter__/__exit__
# =============================================================================
#
# Notes from Pavan:
# I'd been USING context managers since the File Handling module
# (with open(...) as f:) without understanding how they actually work.
# This is me finally peeling back that layer. Turns out it's a clean
# protocol: __enter__ runs at the start of 'with', __exit__ runs at the
# end NO MATTER WHAT, even if an exception happened inside.
# =============================================================================

print("=" * 50)
print("    CONTEXT MANAGERS DEMO")
print("=" * 50)

# ---------------------
# Building a custom context manager class
# ---------------------
print("\n[1] Custom context manager using __enter__ / __exit__")

class FileManager:
    """My own version of what 'open()' does internally, simplified.
    Built this specifically to understand the protocol, not because I'd
    actually replace the built-in open()."""

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"  [__enter__] Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file   # this becomes the 'as f' variable

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"  [__exit__] Closing {self.filename}")
        if self.file:
            self.file.close()
        if exc_type:
            print(f"  [__exit__] An exception occurred: {exc_type.__name__}: {exc_value}")
        # Returning False (or None) lets the exception propagate normally.
        # Returning True would SUPPRESS the exception -- learned this the
        # hard way after a context manager silently swallowed a real bug.
        return False

with FileManager("test_demo.txt", "w") as f:
    f.write("Testing custom context manager\n")
print("  File written and closed automatically")

with FileManager("test_demo.txt", "r") as f:
    print(f"  Content: {f.read().strip()}")

import os
os.remove("test_demo.txt")

# ---------------------
# What happens when an exception occurs inside 'with'
# ---------------------
print("\n[2] __exit__ runs even when an exception happens")
try:
    with FileManager("test_demo2.txt", "w") as f:
        f.write("before crash\n")
        raise ValueError("Something went wrong intentionally!")
except ValueError as e:
    print(f"  Caught outside the with block: {e}")
print("  Notice __exit__ STILL ran and closed the file, even though the")
print("  code inside 'with' crashed halfway through. This is the entire")
print("  guarantee that makes context managers valuable for cleanup.")
os.remove("test_demo2.txt")

# ---------------------
# The contextlib.contextmanager decorator -- a simpler way using generators
# ---------------------
print("\n[3] @contextmanager decorator -- simpler syntax using yield")
from contextlib import contextmanager
import time

@contextmanager
def timer_context(label):
    """Generator-based context manager. Code before yield = __enter__,
    code after yield = __exit__. This pattern felt more natural to me
    than writing a full class once I already understood generators."""
    print(f"  [Starting] {label}")
    start = time.time()
    yield   # this is where the 'with' block's code actually executes
    end = time.time()
    print(f"  [Finished] {label} took {end - start:.4f} seconds")

with timer_context("Sum of first million numbers"):
    total = sum(range(1000000))
print(f"  Result: {total}")

# ---------------------
# Practical: a context manager that yields a USABLE value
# ---------------------
print("\n[4] Context manager that provides a resource via yield")

@contextmanager
def database_connection(db_name):
    """Simulated database connection -- this exact pattern is what I use
    in the real SQLite modules (Module 11) for cursor management."""
    print(f"  [Connecting] to {db_name}")
    connection = {"db": db_name, "connected": True}   # fake connection object
    try:
        yield connection
    finally:
        print(f"  [Disconnecting] from {db_name}")
        connection["connected"] = False

with database_connection("students.db") as conn:
    print(f"  Using connection: {conn}")

# ---------------------
# Nested context managers
# ---------------------
print("\n[5] Multiple context managers in one 'with' statement")
with open("file_a.txt", "w") as fa, open("file_b.txt", "w") as fb:
    fa.write("Content A\n")
    fb.write("Content B\n")
print("  Both files opened and closed together")
os.remove("file_a.txt")
os.remove("file_b.txt")

# ---------------------
# Suppressing specific exceptions with contextlib.suppress
# ---------------------
print("\n[6] contextlib.suppress -- cleaner than empty try/except")
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("file_that_does_not_exist.txt")
print("  No crash, even though the file didn't exist -- suppress() handled it")
print("  Cleaner than writing try/except/pass for cases where I genuinely")
print("  don't care about a specific, expected exception type.")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 ContextManagers.py
# =============================================================================
#
# ==================================================
#     CONTEXT MANAGERS DEMO
# ==================================================
#
# [1] Custom context manager using __enter__ / __exit__
#   [__enter__] Opening test_demo.txt
#   [__exit__] Closing test_demo.txt
#   File written and closed automatically
#   [__enter__] Opening test_demo.txt
#   Content: Testing custom context manager
#   [__exit__] Closing test_demo.txt
#
# [2] __exit__ runs even when an exception happens
#   [__enter__] Opening test_demo2.txt
#   [__exit__] Closing test_demo2.txt
#   [__exit__] An exception occurred: ValueError: Something went wrong intentionally!
#   Caught outside the with block: Something went wrong intentionally!
#   Notice __exit__ STILL ran and closed the file, even though the
#   code inside 'with' crashed halfway through. This is the entire
#   guarantee that makes context managers valuable for cleanup.
#
# [3] @contextmanager decorator -- simpler syntax using yield
#   [Starting] Sum of first million numbers
#   [Finished] Sum of first million numbers took 0.0122 seconds
#   Result: 499999500000
#
# [4] Context manager that provides a resource via yield
#   [Connecting] to students.db
#   Using connection: {'db': 'students.db', 'connected': True}
#   [Disconnecting] from students.db
#
# [5] Multiple context managers in one 'with' statement
#   Both files opened and closed together
#
# [6] contextlib.suppress -- cleaner than empty try/except
#   No crash, even though the file didn't exist -- suppress() handled it
#   Cleaner than writing try/except/pass for cases where I genuinely
#   don't care about a specific, expected exception type.
#
# ==================================================
#
# =============================================================================

