# =============================================================================
# Iterators.py
# Author  : Pavan Shetty H S
# Date    : June 2024
# Topic   : Iterators -- __iter__, __next__, the Iterator Protocol
# =============================================================================
#
# Notes from Pavan:
# Learning iterators AFTER generators felt backwards in hindsight --
# generators are actually a SHORTCUT for building iterators without
# manually writing __iter__/__next__. But going through the manual
# version helped me understand what's happening "under the hood" of
# every for loop I've ever written.
# =============================================================================

print("=" * 50)
print("    ITERATORS DEMO")
print("=" * 50)

# ---------------------
# Understanding what makes something "iterable"
# ---------------------
print("\n[1] iter() and next() -- what a for loop does behind the scenes")

my_list = [10, 20, 30]
my_iterator = iter(my_list)   # this is what 'for' calls automatically
print(f"  iter(my_list) gives: {my_iterator}")
print(f"  next() = {next(my_iterator)}")
print(f"  next() = {next(my_iterator)}")
print(f"  next() = {next(my_iterator)}")
try:
    next(my_iterator)
except StopIteration:
    print("  next() raised StopIteration -- this is EXACTLY how 'for' knows")
    print("  when to stop looping! A for loop is just repeatedly calling")
    print("  next() until it catches StopIteration internally.")

# ---------------------
# Building a custom iterator class -- the manual way
# ---------------------
print("\n[2] Custom Iterator class (implementing the protocol manually)")

class CountUpTo:
    """A custom iterator that counts from 1 up to a maximum value.
    Needed to implement BOTH __iter__ and __next__ for this to work
    with a for loop -- forgetting either one breaks the protocol."""

    def __init__(self, maximum):
        self.maximum = maximum
        self.current = 0

    def __iter__(self):
        # Must return an object with __next__. Returning self works because
        # this class itself implements __next__ below.
        return self

    def __next__(self):
        if self.current < self.maximum:
            self.current += 1
            return self.current
        else:
            raise StopIteration   # REQUIRED to signal "no more values"

counter = CountUpTo(5)
print("  Using for loop on custom iterator:")
for num in counter:
    print(f"    {num}", end=" ")
print()

# ---------------------
# Why a SECOND loop over the same object gives NOTHING
# ---------------------
print("\n[3] The gotcha: iterators get EXHAUSTED, can't reuse directly")
print("  Looping over the SAME counter object again:")
for num in counter:
    print(f"    {num}", end=" ")
print("  (nothing printed!) <-- self.current is already at maximum")
print("""
  This bit me when building a reporting feature for Inventory Management --
  I tried to loop over the same custom iterator twice (once to calculate
  a total, once to print details) and the second loop silently did
  nothing. Had to either create a NEW iterator instance each time, or
  separate __iter__ from __next__ properly (return a fresh iterator
  object from __iter__ instead of self, if reuse is needed).
""")

# ---------------------
# Iterable vs Iterator -- the distinction that confused me
# ---------------------
print("[4] Iterable vs Iterator -- not the same thing!")
print("""
  ITERABLE: anything with __iter__() that returns an iterator.
            (lists, tuples, dicts, strings, sets, custom classes)
  ITERATOR: anything with BOTH __iter__() and __next__().
            (the actual "moving cursor" object that tracks position)

  A list is ITERABLE but is NOT itself an iterator -- calling iter(list)
  creates a SEPARATE iterator object each time, which is exactly why you
  CAN loop over the same list multiple times (each 'for' call gets a
  fresh iterator), but you canNOT loop over the same iterator object
  twice once it's exhausted.
""")

my_list2 = [1, 2, 3]
print(f"  hasattr(my_list2, '__next__'): {hasattr(my_list2, '__next__')}  <-- False, list is not an iterator")
print(f"  hasattr(my_list2, '__iter__'): {hasattr(my_list2, '__iter__')}  <-- True, list IS iterable")

it1 = iter(my_list2)
it2 = iter(my_list2)
print(f"  iter(my_list2) called twice gives DIFFERENT objects: {it1 is it2}")

# ---------------------
# A proper reusable iterable (separating Iterable from Iterator)
# ---------------------
print("\n[5] A proper REUSABLE iterable class (fixes the exhaustion problem)")

class EvenNumbers:
    """This class is ITERABLE -- __iter__ returns a FRESH iterator each
    time, so the same EvenNumbers object CAN be looped over multiple
    times, unlike my CountUpTo example above."""

    def __init__(self, maximum):
        self.maximum = maximum

    def __iter__(self):
        return EvenNumberIterator(self.maximum)

class EvenNumberIterator:
    def __init__(self, maximum):
        self.maximum = maximum
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.maximum:
            raise StopIteration
        value = self.current
        self.current += 2
        return value

evens = EvenNumbers(10)
print("  First loop:", end=" ")
for n in evens:
    print(n, end=" ")
print("\n  Second loop (works fine this time!):", end=" ")
for n in evens:
    print(n, end=" ")
print()

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Iterators.py
# =============================================================================
#
# ==================================================
#     ITERATORS DEMO
# ==================================================
#
# [1] iter() and next() -- what a for loop does behind the scenes
#   iter(my_list) gives: <list_iterator object at 0x7fc9d8da56c0>
#   next() = 10
#   next() = 20
#   next() = 30
#   next() raised StopIteration -- this is EXACTLY how 'for' knows
#   when to stop looping! A for loop is just repeatedly calling
#   next() until it catches StopIteration internally.
#
# [2] Custom Iterator class (implementing the protocol manually)
#   Using for loop on custom iterator:
#     1     2     3     4     5 
#
# [3] The gotcha: iterators get EXHAUSTED, can't reuse directly
#   Looping over the SAME counter object again:
#   (nothing printed!) <-- self.current is already at maximum
#
#   This bit me when building a reporting feature for Inventory Management --
#   I tried to loop over the same custom iterator twice (once to calculate
#   a total, once to print details) and the second loop silently did
#   nothing. Had to either create a NEW iterator instance each time, or
#   separate __iter__ from __next__ properly (return a fresh iterator
#   object from __iter__ instead of self, if reuse is needed).
#
# [4] Iterable vs Iterator -- not the same thing!
#
#   ITERABLE: anything with __iter__() that returns an iterator.
#             (lists, tuples, dicts, strings, sets, custom classes)
#   ITERATOR: anything with BOTH __iter__() and __next__().
#             (the actual "moving cursor" object that tracks position)
#
#   A list is ITERABLE but is NOT itself an iterator -- calling iter(list)
#   creates a SEPARATE iterator object each time, which is exactly why you
#   CAN loop over the same list multiple times (each 'for' call gets a
#   fresh iterator), but you canNOT loop over the same iterator object
#   twice once it's exhausted.
#
#   hasattr(my_list2, '__next__'): False  <-- False, list is not an iterator
#   hasattr(my_list2, '__iter__'): True  <-- True, list IS iterable
#   iter(my_list2) called twice gives DIFFERENT objects: False
#
# [5] A proper REUSABLE iterable class (fixes the exhaustion problem)
#   First loop: 0 2 4 6 8 10 
#   Second loop (works fine this time!): 0 2 4 6 8 10 
#
# ==================================================
#
# =============================================================================

