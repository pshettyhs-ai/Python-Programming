# =============================================================================
# ClassesObjects.py
# Author  : Pavan Shetty H S
# Date    : May 2024
# Topic   : Classes and Objects -- the foundation of OOP
# =============================================================================
#
# Notes from Pavan:
# This is where I started, and honestly OOP in Python felt LESS rigid
# than C++ (which I'd touched briefly in college). No need for separate
# .h declarations, no explicit access specifiers required (though Python
# has conventions for "private" using underscores, more on that in
# Encapsulation.py). The self parameter confused me hard initially --
# kept forgetting to include it in method definitions and getting
# "missing 1 required positional argument" errors.
# =============================================================================

print("=" * 50)
print("    CLASSES AND OBJECTS DEMO")
print("=" * 50)

# ---------------------
# Basic class definition
# ---------------------
class Student:
    """A simple class representing a student."""

    # Class variable -- shared across ALL instances (learned this distinction
    # the hard way, see notes below)
    college_name = "PES Institute of Technology"

    def __init__(self, name, branch, cgpa):
        # Instance variables -- unique to EACH object
        self.name = name
        self.branch = branch
        self.cgpa = cgpa

    def display_info(self):
        """Instance method -- 'self' refers to the specific object calling it."""
        print(f"  Name   : {self.name}")
        print(f"  Branch : {self.branch}")
        print(f"  CGPA   : {self.cgpa}")
        print(f"  College: {Student.college_name}")

    def is_eligible_for_scholarship(self):
        return self.cgpa >= 8.5

# ---------------------
# Creating objects (instantiation)
# ---------------------
print("\n[1] Creating objects from a class")
s1 = Student("Pavan Shetty H S", "ECE", 8.7)
s2 = Student("Rahul Kumar", "CSE", 7.9)

print("Student 1:")
s1.display_info()
print("\nStudent 2:")
s2.display_info()

# ---------------------
# Class variable vs instance variable -- the distinction that confused me
# ---------------------
print("\n[2] Class variables vs Instance variables")
print(f"  s1.college_name: {s1.college_name}")
print(f"  s2.college_name: {s2.college_name}")
print("  Both share the SAME class variable")

# Modifying class variable through the CLASS affects all instances
Student.college_name = "New Institute Name"
print(f"\n  After Student.college_name = 'New Institute Name':")
print(f"  s1.college_name: {s1.college_name}")
print(f"  s2.college_name: {s2.college_name}  <-- both changed!")

# But modifying through an INSTANCE creates a new instance variable
# that SHADOWS the class variable, only for that instance
s1.college_name = "Pavan's Override"
print(f"\n  After s1.college_name = 'Pavan's Override' (instance-level):")
print(f"  s1.college_name: {s1.college_name}  <-- only s1 changed")
print(f"  s2.college_name: {s2.college_name}  <-- s2 still has the class value")
print("  This distinction caused a confusing bug in an early draft of my")
print("  Student Management project where I expected ALL students to share")
print("  a counter, but instance-level assignment broke that sharing.")

# ---------------------
# Calling methods
# ---------------------
print("\n[3] Calling instance methods")
print(f"  Is s1 eligible for scholarship? {s1.is_eligible_for_scholarship()}")
print(f"  Is s2 eligible for scholarship? {s2.is_eligible_for_scholarship()}")

# ---------------------
# Checking object type and attributes
# ---------------------
print("\n[4] Inspecting objects")
print(f"  type(s1): {type(s1)}")
print(f"  isinstance(s1, Student): {isinstance(s1, Student)}")
print(f"  s1.__dict__: {s1.__dict__}")   # all instance attributes as a dict

# ---------------------
# Dynamically adding attributes (Python allows this -- surprised me)
# ---------------------
print("\n[5] Dynamically adding new attributes at runtime")
s1.phone_number = "9876543210"   # not defined in __init__, but Python allows it
print(f"  Added phone_number dynamically: {s1.phone_number}")
print("  Note: this works because Python objects have flexible __dict__")
print("  storage by default, unlike C structs with fixed members.")
print("  (I generally AVOID doing this in real code -- it makes object")
print("  shape unpredictable. Better to define all attributes in __init__.)")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 ClassesObjects.py
# =============================================================================
#
# ==================================================
#     CLASSES AND OBJECTS DEMO
# ==================================================
#
# [1] Creating objects from a class
# Student 1:
#   Name   : Pavan Shetty H S
#   Branch : ECE
#   CGPA   : 8.7
#   College: PES Institute of Technology
#
# Student 2:
#   Name   : Rahul Kumar
#   Branch : CSE
#   CGPA   : 7.9
#   College: PES Institute of Technology
#
# [2] Class variables vs Instance variables
#   s1.college_name: PES Institute of Technology
#   s2.college_name: PES Institute of Technology
#   Both share the SAME class variable
#
#   After Student.college_name = 'New Institute Name':
#   s1.college_name: New Institute Name
#   s2.college_name: New Institute Name  <-- both changed!
#
#   After s1.college_name = 'Pavan's Override' (instance-level):
#   s1.college_name: Pavan's Override  <-- only s1 changed
#   s2.college_name: New Institute Name  <-- s2 still has the class value
#   This distinction caused a confusing bug in an early draft of my
#   Student Management project where I expected ALL students to share
#   a counter, but instance-level assignment broke that sharing.
#
# [3] Calling instance methods
#   Is s1 eligible for scholarship? True
#   Is s2 eligible for scholarship? False
#
# [4] Inspecting objects
#   type(s1): <class '__main__.Student'>
#   isinstance(s1, Student): True
#   s1.__dict__: {'name': 'Pavan Shetty H S', 'branch': 'ECE', 'cgpa': 8.7, 'college_name': "Pavan's Override"}
#
# [5] Dynamically adding new attributes at runtime
#   Added phone_number dynamically: 9876543210
#   Note: this works because Python objects have flexible __dict__
#   storage by default, unlike C structs with fixed members.
#   (I generally AVOID doing this in real code -- it makes object
#   shape unpredictable. Better to define all attributes in __init__.)
#
# ==================================================
#
# =============================================================================

