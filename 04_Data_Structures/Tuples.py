# =============================================================================
# Tuples.py
# Author  : Pavan Shetty H S
# Date    : February 2024
# Topic   : Tuples -- immutable sequences
# =============================================================================
#
# Notes from Pavan:
# At first I thought "why use a tuple when list does everything and more?"
# Then I learned: immutability is a FEATURE, not a limitation. Tuples are
# faster, hashable (can be dict keys / set elements), and signal intent --
# "this data shouldn't change." I use them for coordinates, RGB values,
# fixed records now.
#
# =============================================================================

print("=" * 50)
print("       TUPLES DEMO")
print("=" * 50)

# ---------------------
# Creating tuples
# ---------------------
coordinates = (12.9716, 77.5946)   # lat, long of Bangalore
single_item = (42,)                 # NOTE: comma needed for single-item tuple!
no_parens = 1, 2, 3                 # parentheses are optional actually
empty = ()

print(f"\nCoordinates: {coordinates}")
print(f"Single item tuple: {single_item}  (type: {type(single_item)})")

# Common mistake I made: forgetting the comma
not_a_tuple = (42)   # this is just an int in parentheses!
print(f"(42) without comma: {not_a_tuple}  (type: {type(not_a_tuple)})  <-- NOT a tuple!")

# ---------------------
# Immutability demonstration
# ---------------------
print("\n[Immutability]")
point = (10, 20)
print(f"  point = {point}")
try:
    point[0] = 99
except TypeError as e:
    print(f"  Tried point[0]=99, got error: {e}")

# ---------------------
# Indexing and slicing (same as lists)
# ---------------------
print("\n[Indexing & Slicing]")
rgb = (255, 128, 0)
print(f"  RGB: {rgb}")
print(f"  Red={rgb[0]}, Green={rgb[1]}, Blue={rgb[2]}")

skills = ("Python", "C", "C++", "Embedded C", "Arduino")
print(f"  skills[1:3]: {skills[1:3]}")
print(f"  skills[::-1]: {skills[::-1]}")

# ---------------------
# Tuple unpacking -- used this constantly once I learned it
# ---------------------
print("\n[Tuple Unpacking]")
person = ("Pavan", 22, "ECE")
name, age, branch = person
print(f"  Unpacked: name={name}, age={age}, branch={branch}")

# Unpacking with * for "rest" elements
first, *middle, last = (1, 2, 3, 4, 5)
print(f"  first={first}, middle={middle}, last={last}")

# Swapping using tuples (same trick as lists, but this IS literally tuple packing)
a, b = 5, 10
a, b = b, a
print(f"  After swap: a={a}, b={b}")

# ---------------------
# Tuple methods (only 2 exist! count and index)
# ---------------------
print("\n[Tuple methods -- only count() and index() since immutable]")
numbers = (1, 2, 3, 2, 4, 2, 5)
print(f"  Tuple: {numbers}")
print(f"  count(2): {numbers.count(2)}")
print(f"  index(4): {numbers.index(4)}")

# ---------------------
# Why use tuples? -- as dictionary keys (lists CAN'T do this)
# ---------------------
print("\n[Tuples as dictionary keys -- lists cannot do this!]")
distances = {
    (0, 0): 0,
    (1, 1): 1.41,
    (3, 4): 5.0
}
print(f"  Distance lookup table: {distances}")
print(f"  Distance at (3,4): {distances[(3, 4)]}")

try:
    bad_dict = {[1, 2]: "value"}  # this will fail!
except TypeError as e:
    print(f"  Tried using a list as key: {e}")

# ---------------------
# Returning multiple values from functions (tuples under the hood)
# ---------------------
print("\n[Functions returning tuples]")
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)/len(numbers)

data = [23, 45, 12, 67, 34]
lo, hi, avg = get_stats(data)
print(f"  Data: {data}")
print(f"  Min={lo}, Max={hi}, Avg={avg:.2f}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Tuples.py
# =============================================================================
#
# ==================================================
#        TUPLES DEMO
# ==================================================
#
# Coordinates: (12.9716, 77.5946)
# Single item tuple: (42,)  (type: <class 'tuple'>)
# (42) without comma: 42  (type: <class 'int'>)  <-- NOT a tuple!
#
# [Immutability]
#   point = (10, 20)
#   Tried point[0]=99, got error: 'tuple' object does not support item assignment
#
# [Indexing & Slicing]
#   RGB: (255, 128, 0)
#   Red=255, Green=128, Blue=0
#   skills[1:3]: ('C', 'C++')
#   skills[::-1]: ('Arduino', 'Embedded C', 'C++', 'C', 'Python')
#
# [Tuple Unpacking]
#   Unpacked: name=Pavan, age=22, branch=ECE
#   first=1, middle=[2, 3, 4], last=5
#   After swap: a=10, b=5
#
# [Tuple methods -- only count() and index() since immutable]
#   Tuple: (1, 2, 3, 2, 4, 2, 5)
#   count(2): 3
#   index(4): 4
#
# [Tuples as dictionary keys -- lists cannot do this!]
#   Distance lookup table: {(0, 0): 0, (1, 1): 1.41, (3, 4): 5.0}
#   Distance at (3,4): 5.0
#   Tried using a list as key: unhashable type: 'list'
#
# [Functions returning tuples]
#   Data: [23, 45, 12, 67, 34]
#   Min=12, Max=67, Avg=36.20
#
# ==================================================
#
# =============================================================================

