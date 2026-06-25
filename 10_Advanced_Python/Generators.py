# =============================================================================
# Generators.py
# Author  : Pavan Shetty H S
# Date    : June 2024
# Topic   : Generators -- yield, generator expressions
# =============================================================================
#
# Notes from Pavan:
# Generators finally clicked when I compared them to how a C iterator
# pattern would work manually -- maintaining state between calls without
# recomputing from scratch, but without writing a whole struct + functions
# to track position. 'yield' pauses a function and remembers EXACTLY
# where it left off, which felt like genuine magic until I understood
# it's just saved execution state.
# =============================================================================

import sys

print("=" * 50)
print("    GENERATORS DEMO")
print("=" * 50)

# ---------------------
# Regular function vs generator function
# ---------------------
print("\n[1] Regular function (returns everything at once)")

def get_squares_list(n):
    """Builds the ENTIRE list in memory before returning anything."""
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

squares_list = get_squares_list(5)
print(f"  Result: {squares_list}")

print("\n[2] Generator function (yields one value at a time)")

def get_squares_gen(n):
    """yield PAUSES execution and returns one value at a time.
    Doesn't build the whole list in memory."""
    for i in range(n):
        yield i ** 2

squares_gen = get_squares_gen(5)
print(f"  Generator object: {squares_gen}")
print(f"  Type: {type(squares_gen)}")
print("  Iterating manually with next():")
print(f"    next() = {next(squares_gen)}")
print(f"    next() = {next(squares_gen)}")
print(f"    next() = {next(squares_gen)}")
print("  Or just loop over it normally:")
for val in get_squares_gen(5):
    print(f"    {val}", end=" ")
print()

# ---------------------
# Memory comparison -- the thing that made this click
# ---------------------
print("\n[3] Memory usage comparison -- this is WHY generators matter")
big_list = [i for i in range(100000)]
big_gen = (i for i in range(100000))   # generator expression

print(f"  List of 100,000 ints:      {sys.getsizeof(big_list):,} bytes")
print(f"  Generator (same range):    {sys.getsizeof(big_gen):,} bytes")
print("  ^ The generator barely uses any memory because it doesn't store")
print("  values, it computes them ON DEMAND. For huge datasets or infinite")
print("  sequences, this difference is the entire point.")

# ---------------------
# Generator that would be IMPOSSIBLE as a regular list (infinite sequence)
# ---------------------
print("\n[4] Infinite generator -- can't do this with a normal list!")

def infinite_counter(start=0):
    """An infinite sequence. A regular function returning a list would
    never finish running -- it would try to build an infinitely long list
    and crash with MemoryError eventually. Generators handle this fine
    because they only compute what's actually requested."""
    n = start
    while True:
        yield n
        n += 1

counter = infinite_counter(1)
print("  First 5 values from an infinite generator:")
for _ in range(5):
    print(f"    {next(counter)}", end=" ")
print()

# ---------------------
# Generator expressions -- like list comprehensions but lazy
# ---------------------
print("\n[5] Generator expressions (parentheses instead of brackets)")
nums = [1, 2, 3, 4, 5]
squared_list = [x**2 for x in nums]       # list comprehension -- eager
squared_gen = (x**2 for x in nums)        # generator expression -- lazy

print(f"  List comprehension: {squared_list}")
print(f"  Generator expression: {squared_gen}  (not evaluated yet)")
print(f"  Converted to list: {list(squared_gen)}")

# ---------------------
# Practical example: reading a large file lazily (line by line)
# ---------------------
print("\n[6] Practical: Lazy file processing pattern")

def read_large_file_lines(filepath):
    """In real use, this would read a huge file line-by-line without
    loading the whole thing into memory. I use this exact pattern when
    processing log files."""
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()

# Quick demo file
with open("temp_demo.txt", "w") as f:
    for i in range(5):
        f.write(f"Log line {i}\n")

for line in read_large_file_lines("temp_demo.txt"):
    print(f"  {line}")

import os
os.remove("temp_demo.txt")

# ---------------------
# StopIteration -- what happens when a generator is exhausted
# ---------------------
print("\n[7] StopIteration -- generators can only be consumed ONCE")
small_gen = (x for x in range(3))
print(f"  {next(small_gen)}")
print(f"  {next(small_gen)}")
print(f"  {next(small_gen)}")
try:
    next(small_gen)
except StopIteration:
    print("  Caught StopIteration -- generator is exhausted, can't reuse it")
print("  Lesson: if you need to iterate again, create a NEW generator,")
print("  you can't 'rewind' an exhausted one.")

# ---------------------
# send() -- generators can receive values too (advanced, rarely used by me)
# ---------------------
print("\n[8] Two-way generators with send() (advanced, rarely needed)")

def echo_generator():
    while True:
        received = yield
        print(f"  Generator received: {received}")

gen = echo_generator()
next(gen)   # prime the generator (must advance to first yield)
gen.send("Hello")
gen.send("World")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Generators.py
# =============================================================================
#
# ==================================================
#     GENERATORS DEMO
# ==================================================
#
# [1] Regular function (returns everything at once)
#   Result: [0, 1, 4, 9, 16]
#
# [2] Generator function (yields one value at a time)
#   Generator object: <generator object get_squares_gen at 0x7f280c0a79f0>
#   Type: <class 'generator'>
#   Iterating manually with next():
#     next() = 0
#     next() = 1
#     next() = 4
#   Or just loop over it normally:
#     0     1     4     9     16 
#
# [3] Memory usage comparison -- this is WHY generators matter
#   List of 100,000 ints:      800,984 bytes
#   Generator (same range):    192 bytes
#   ^ The generator barely uses any memory because it doesn't store
#   values, it computes them ON DEMAND. For huge datasets or infinite
#   sequences, this difference is the entire point.
#
# [4] Infinite generator -- can't do this with a normal list!
#   First 5 values from an infinite generator:
#     1     2     3     4     5 
#
# [5] Generator expressions (parentheses instead of brackets)
#   List comprehension: [1, 4, 9, 16, 25]
#   Generator expression: <generator object <genexpr> at 0x7f280c182260>  (not evaluated yet)
#   Converted to list: [1, 4, 9, 16, 25]
#
# [6] Practical: Lazy file processing pattern
#   Log line 0
#   Log line 1
#   Log line 2
#   Log line 3
#   Log line 4
#
# [7] StopIteration -- generators can only be consumed ONCE
#   0
#   1
#   2
#   Caught StopIteration -- generator is exhausted, can't reuse it
#   Lesson: if you need to iterate again, create a NEW generator,
#   you can't 'rewind' an exhausted one.
#
# [8] Two-way generators with send() (advanced, rarely needed)
#   Generator received: Hello
#   Generator received: World
#
# ==================================================
#
# =============================================================================

