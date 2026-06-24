# =============================================================================
# Sets.py
# Author  : Pavan Shetty H S
# Date    : February 2024
# Topic   : Sets -- unordered collections of unique elements
# =============================================================================
#
# Notes from Pavan:
# Sets clicked for me immediately because I'd literally been writing manual
# "remove duplicates from array" loops in C using nested for-loops (O(n^2)
# garbage). set(my_list) does it in one line. The math-class venn diagram
# operations (union, intersection, difference) being built-in methods is
# genuinely satisfying to use.
#
# =============================================================================

print("=" * 50)
print("       SETS DEMO")
print("=" * 50)

# ---------------------
# Creating sets
# ---------------------
languages = {"Python", "C", "C++", "Java"}
empty_set = set()   # NOTE: {} creates an empty DICT, not a set! Gotcha.
from_list = set([1, 2, 2, 3, 3, 3, 4])   # duplicates auto-removed

print(f"\nLanguages: {languages}")
print(f"From list with dupes [1,2,2,3,3,3,4]: {from_list}")
print(f"{{}} creates: {type({})}  <-- NOT a set, watch out!")

# ---------------------
# Adding & removing elements
# ---------------------
print("\n[Add/Remove]")
skills = {"Python", "C"}
skills.add("Embedded C")
print(f"  After add: {skills}")

skills.update(["Arduino", "STM32"])   # add multiple at once
print(f"  After update: {skills}")

skills.discard("C")    # safe -- no error if not present
print(f"  After discard('C'): {skills}")

skills.discard("NotThere")  # no error even though it doesn't exist
print(f"  discard() on non-existent item: no error")

try:
    skills.remove("AlsoNotThere")  # remove() DOES throw error if missing
except KeyError as e:
    print(f"  remove() on non-existent item raised: KeyError {e}")

# ---------------------
# Set operations (the math I learned in school, finally useful!)
# ---------------------
print("\n[Set Operations]")
my_skills = {"Python", "C", "C++", "Embedded C", "Arduino"}
job_requires = {"Python", "C++", "JavaScript", "SQL"}

print(f"  My skills      : {my_skills}")
print(f"  Job requires   : {job_requires}")
print(f"  Union (|)      : {my_skills | job_requires}")
print(f"  Intersection (&): {my_skills & job_requires}  <-- matching skills")
print(f"  Difference (-) : {my_skills - job_requires}  <-- skills I have they don't need")
print(f"  Symmetric diff (^): {my_skills ^ job_requires}  <-- skills in only one set")

# ---------------------
# Practical use case: removing duplicates while preserving structure
# ---------------------
print("\n[Practical: Removing duplicates from a list]")
visitor_log = ["Pavan", "Rahul", "Pavan", "Sneha", "Rahul", "Pavan"]
unique_visitors = set(visitor_log)
print(f"  Visitor log: {visitor_log}")
print(f"  Unique visitors: {unique_visitors}")
print(f"  Total visits: {len(visitor_log)}, Unique visitors: {len(unique_visitors)}")

# ---------------------
# Checking subset/superset
# ---------------------
print("\n[Subset/Superset checks]")
basic_skills = {"Python", "C"}
all_skills = {"Python", "C", "C++", "Embedded C"}
print(f"  basic_skills issubset all_skills: {basic_skills.issubset(all_skills)}")
print(f"  all_skills issuperset basic_skills: {all_skills.issuperset(basic_skills)}")

# ---------------------
# Frozenset -- immutable version of set
# ---------------------
print("\n[Frozenset -- immutable set]")
frozen = frozenset(["read", "write"])
print(f"  Frozenset: {frozen}")
try:
    frozen.add("execute")
except AttributeError as e:
    print(f"  Tried to modify frozenset: {e}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Sets.py
# =============================================================================
#
# ==================================================
#        SETS DEMO
# ==================================================
#
# Languages: {'Java', 'Python', 'C', 'C++'}
# From list with dupes [1,2,2,3,3,3,4]: {1, 2, 3, 4}
# {} creates: <class 'dict'>  <-- NOT a set, watch out!
#
# [Add/Remove]
#   After add: {'Embedded C', 'Python', 'C'}
#   After update: {'Embedded C', 'STM32', 'Arduino', 'C', 'Python'}
#   After discard('C'): {'Embedded C', 'STM32', 'Arduino', 'Python'}
#   discard() on non-existent item: no error
#   remove() on non-existent item raised: KeyError 'AlsoNotThere'
#
# [Set Operations]
#   My skills      : {'Embedded C', 'Arduino', 'C++', 'C', 'Python'}
#   Job requires   : {'Python', 'SQL', 'JavaScript', 'C++'}
#   Union (|)      : {'C++', 'Embedded C', 'SQL', 'Arduino', 'C', 'JavaScript', 'Python'}
#   Intersection (&): {'Python', 'C++'}  <-- matching skills
#   Difference (-) : {'Embedded C', 'C', 'Arduino'}  <-- skills I have they don't need
#   Symmetric diff (^): {'Embedded C', 'SQL', 'JavaScript', 'Arduino', 'C'}  <-- skills in only one set
#
# [Practical: Removing duplicates from a list]
#   Visitor log: ['Pavan', 'Rahul', 'Pavan', 'Sneha', 'Rahul', 'Pavan']
#   Unique visitors: {'Pavan', 'Sneha', 'Rahul'}
#   Total visits: 6, Unique visitors: 3
#
# [Subset/Superset checks]
#   basic_skills issubset all_skills: True
#   all_skills issuperset basic_skills: True
#
# [Frozenset -- immutable set]
#   Frozenset: frozenset({'read', 'write'})
#   Tried to modify frozenset: 'frozenset' object has no attribute 'add'
#
# ==================================================
#
# =============================================================================

