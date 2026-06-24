# =============================================================================
# Lists.py
# Author  : Pavan Shetty H S
# Date    : February 2024
# Topic   : Lists -- creation, indexing, slicing, methods
# =============================================================================
#
# Notes from Pavan:
# Lists are basically Python's version of dynamic arrays, but with a TON
# more built-in functionality than C arrays. No need to manually realloc
# memory or track size separately. Slicing especially blew my mind --
# it's like array operations I used to write manual loops for in C.
#
# =============================================================================

print("=" * 50)
print("       LISTS DEMO")
print("=" * 50)

# ---------------------
# Creating lists
# ---------------------
skills = ["Python", "C", "C++", "Embedded C"]
mixed = [1, "two", 3.0, True, [5, 6]]   # lists can hold mixed types!
empty = []

print(f"\nSkills: {skills}")
print(f"Mixed types: {mixed}")

# ---------------------
# Indexing
# ---------------------
print("\n[Indexing]")
print(f"  First skill : {skills[0]}")
print(f"  Last skill  : {skills[-1]}")
print(f"  Second-last : {skills[-2]}")

# ---------------------
# Slicing -- this is what really impressed me
# ---------------------
print("\n[Slicing] list[start:stop:step]")
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"  Full list      : {numbers}")
print(f"  numbers[2:5]   : {numbers[2:5]}")     # index 2,3,4
print(f"  numbers[:4]    : {numbers[:4]}")      # from start to 3
print(f"  numbers[6:]    : {numbers[6:]}")      # from 6 to end
print(f"  numbers[::2]   : {numbers[::2]}")     # every 2nd element
print(f"  numbers[::-1]  : {numbers[::-1]}")    # REVERSED -- super handy
print(f"  numbers[-3:]   : {numbers[-3:]}")     # last 3 elements

# ---------------------
# Adding elements
# ---------------------
print("\n[Adding elements]")
skills.append("Arduino")
print(f"  After append('Arduino'): {skills}")

skills.insert(1, "STM32")   # insert at specific index
print(f"  After insert(1, 'STM32'): {skills}")

skills.extend(["ESP32", "RTOS"])   # add multiple items
print(f"  After extend(['ESP32','RTOS']): {skills}")

# ---------------------
# Removing elements
# ---------------------
print("\n[Removing elements]")
skills.remove("STM32")   # removes by VALUE (first occurrence)
print(f"  After remove('STM32'): {skills}")

popped = skills.pop()    # removes and returns LAST item
print(f"  Popped: {popped} | List now: {skills}")

popped_index = skills.pop(0)   # removes item at specific index
print(f"  Popped index 0: {popped_index} | List now: {skills}")

del skills[0]   # del statement also works
print(f"  After del skills[0]: {skills}")

# ---------------------
# List methods
# ---------------------
print("\n[Useful methods]")
nums = [5, 2, 9, 1, 7, 3]
print(f"  Original: {nums}")
print(f"  sorted() (new list): {sorted(nums)}")
print(f"  Original unchanged : {nums}")

nums.sort()   # sorts IN PLACE -- this confused me at first since sorted() doesn't
print(f"  After nums.sort() (in-place): {nums}")

nums.reverse()
print(f"  After reverse(): {nums}")

print(f"  Count of 9 in list: {nums.count(9)}")
print(f"  Index of 7: {nums.index(7)}")
print(f"  Length: {len(nums)}")
print(f"  Max: {max(nums)}, Min: {min(nums)}, Sum: {sum(nums)}")

# ---------------------
# List comprehension -- the feature that changed how I write loops
# ---------------------
print("\n[List Comprehension]")
squares = [x**2 for x in range(1, 11)]
print(f"  Squares 1-10: {squares}")

evens = [x for x in range(1, 21) if x % 2 == 0]
print(f"  Evens 1-20: {evens}")

# Nested comprehension -- flattening a 2D list
matrix = [[1,2,3], [4,5,6], [7,8,9]]
flat = [num for row in matrix for num in row]
print(f"  Matrix: {matrix}")
print(f"  Flattened: {flat}")

# ---------------------
# Copying lists -- the bug I hit
# ---------------------
print("\n[Copying lists -- IMPORTANT GOTCHA]")
original = [1, 2, 3]
shallow_ref = original          # this is NOT a copy! Just another name for same list
real_copy = original.copy()     # this IS a proper copy
also_copy = original[:]         # slicing also makes a copy

shallow_ref.append(99)
print(f"  original after modifying shallow_ref: {original}  <-- changed too! same object")
print(f"  real_copy (unaffected): {real_copy}")
print(f"  also_copy (unaffected): {also_copy}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Lists.py
# =============================================================================
#
# ==================================================
#        LISTS DEMO
# ==================================================
#
# Skills: ['Python', 'C', 'C++', 'Embedded C']
# Mixed types: [1, 'two', 3.0, True, [5, 6]]
#
# [Indexing]
#   First skill : Python
#   Last skill  : Embedded C
#   Second-last : C++
#
# [Slicing] list[start:stop:step]
#   Full list      : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#   numbers[2:5]   : [2, 3, 4]
#   numbers[:4]    : [0, 1, 2, 3]
#   numbers[6:]    : [6, 7, 8, 9]
#   numbers[::2]   : [0, 2, 4, 6, 8]
#   numbers[::-1]  : [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
#   numbers[-3:]   : [7, 8, 9]
#
# [Adding elements]
#   After append('Arduino'): ['Python', 'C', 'C++', 'Embedded C', 'Arduino']
#   After insert(1, 'STM32'): ['Python', 'STM32', 'C', 'C++', 'Embedded C', 'Arduino']
#   After extend(['ESP32','RTOS']): ['Python', 'STM32', 'C', 'C++', 'Embedded C', 'Arduino', 'ESP32', 'RTOS']
#
# [Removing elements]
#   After remove('STM32'): ['Python', 'C', 'C++', 'Embedded C', 'Arduino', 'ESP32', 'RTOS']
#   Popped: RTOS | List now: ['Python', 'C', 'C++', 'Embedded C', 'Arduino', 'ESP32']
#   Popped index 0: Python | List now: ['C', 'C++', 'Embedded C', 'Arduino', 'ESP32']
#   After del skills[0]: ['C++', 'Embedded C', 'Arduino', 'ESP32']
#
# [Useful methods]
#   Original: [5, 2, 9, 1, 7, 3]
#   sorted() (new list): [1, 2, 3, 5, 7, 9]
#   Original unchanged : [5, 2, 9, 1, 7, 3]
#   After nums.sort() (in-place): [1, 2, 3, 5, 7, 9]
#   After reverse(): [9, 7, 5, 3, 2, 1]
#   Count of 9 in list: 1
#   Index of 7: 1
#   Length: 6
#   Max: 9, Min: 1, Sum: 27
#
# [List Comprehension]
#   Squares 1-10: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
#   Evens 1-20: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
#   Matrix: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#   Flattened: [1, 2, 3, 4, 5, 6, 7, 8, 9]
#
# [Copying lists -- IMPORTANT GOTCHA]
#   original after modifying shallow_ref: [1, 2, 3, 99]  <-- changed too! same object
#   real_copy (unaffected): [1, 2, 3]
#   also_copy (unaffected): [1, 2, 3]
#
# ==================================================
#
# =============================================================================

