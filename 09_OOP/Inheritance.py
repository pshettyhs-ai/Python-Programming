# =============================================================================
# Inheritance.py
# Author  : Pavan Shetty H S
# Date    : May 2024
# Topic   : Inheritance -- single, multiple, multilevel
# =============================================================================
#
# Notes from Pavan:
# This took me almost a week to feel comfortable with, specifically
# multiple inheritance and the Method Resolution Order (MRO). Single
# inheritance is intuitive. Multiple inheritance is where things got
# genuinely confusing -- which parent's method actually gets called when
# both parents define the same method name?
# =============================================================================

print("=" * 50)
print("    INHERITANCE DEMO")
print("=" * 50)

# ---------------------
# Single Inheritance
# ---------------------
print("\n[1] Single Inheritance")

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print(f"  Name: {self.name}, Age: {self.age}")

    def introduce(self):
        print(f"  Hi, I'm {self.name}")

class Employee(Person):   # Employee INHERITS from Person
    def __init__(self, name, age, employee_id, salary):
        super().__init__(name, age)   # call parent constructor
        self.employee_id = employee_id
        self.salary = salary

    def display(self):
        super().display()   # reuse parent's display, then extend it
        print(f"  Employee ID: {self.employee_id}, Salary: {self.salary}")

emp = Employee("Pavan Shetty H S", 22, "EMP101", 45000)
emp.display()
emp.introduce()   # inherited method, works without redefining it

# ---------------------
# Multilevel Inheritance
# ---------------------
print("\n[2] Multilevel Inheritance (Person -> Employee -> Manager)")

class Manager(Employee):
    def __init__(self, name, age, employee_id, salary, team_size):
        super().__init__(name, age, employee_id, salary)
        self.team_size = team_size

    def display(self):
        super().display()
        print(f"  Team Size: {self.team_size}")

mgr = Manager("Sneha Rao", 35, "MGR001", 90000, 12)
mgr.display()
mgr.introduce()   # inherited all the way from Person, 2 levels up

# ---------------------
# Multiple Inheritance -- where things got genuinely confusing
# ---------------------
print("\n[3] Multiple Inheritance")

class Swimmer:
    def move(self):
        print("  Swimming through water")

class Flyer:
    def move(self):
        print("  Flying through air")

class Duck(Swimmer, Flyer):   # inherits from BOTH
    pass

duck = Duck()
duck.move()
print("  ^ Called Swimmer's move() because Swimmer is listed FIRST")
print("  This is Method Resolution Order (MRO) at work.")

print(f"\n  MRO for Duck: {[cls.__name__ for cls in Duck.__mro__]}")
print("  Python checks classes in this exact order to find methods.")

# ---------------------
# Method Resolution Order (MRO) -- the diamond problem
# ---------------------
print("\n[4] The Diamond Problem and MRO (C3 Linearization)")

class A:
    def greet(self):
        print("  Greet from A")

class B(A):
    def greet(self):
        print("  Greet from B")

class C(A):
    def greet(self):
        print("  Greet from C")

class D(B, C):   # Diamond shape: D -> B,C -> A
    pass

d = D()
d.greet()
print(f"  MRO for D: {[cls.__name__ for cls in D.__mro__]}")
print("""
  This confused me for DAYS. I expected Python to maybe raise an
  ambiguity error like some languages do, but Python uses C3
  linearization to deterministically pick B's greet() over C's,
  because B is listed first AND comes before C in the inheritance order.
  Reading the MRO list explicitly (via __mro__) was the thing that
  finally made this click for me instead of just guessing.
""")

# ---------------------
# isinstance() and issubclass() with inheritance
# ---------------------
print("[5] isinstance() and issubclass() checks")
print(f"  isinstance(mgr, Manager): {isinstance(mgr, Manager)}")
print(f"  isinstance(mgr, Employee): {isinstance(mgr, Employee)}  <-- True, inherited!")
print(f"  isinstance(mgr, Person): {isinstance(mgr, Person)}  <-- True, 2 levels up!")
print(f"  issubclass(Manager, Person): {issubclass(Manager, Person)}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Inheritance.py
# =============================================================================
#
# ==================================================
#     INHERITANCE DEMO
# ==================================================
#
# [1] Single Inheritance
#   Name: Pavan Shetty H S, Age: 22
#   Employee ID: EMP101, Salary: 45000
#   Hi, I'm Pavan Shetty H S
#
# [2] Multilevel Inheritance (Person -> Employee -> Manager)
#   Name: Sneha Rao, Age: 35
#   Employee ID: MGR001, Salary: 90000
#   Team Size: 12
#   Hi, I'm Sneha Rao
#
# [3] Multiple Inheritance
#   Swimming through water
#   ^ Called Swimmer's move() because Swimmer is listed FIRST
#   This is Method Resolution Order (MRO) at work.
#
#   MRO for Duck: ['Duck', 'Swimmer', 'Flyer', 'object']
#   Python checks classes in this exact order to find methods.
#
# [4] The Diamond Problem and MRO (C3 Linearization)
#   Greet from B
#   MRO for D: ['D', 'B', 'C', 'A', 'object']
#
#   This confused me for DAYS. I expected Python to maybe raise an
#   ambiguity error like some languages do, but Python uses C3
#   linearization to deterministically pick B's greet() over C's,
#   because B is listed first AND comes before C in the inheritance order.
#   Reading the MRO list explicitly (via __mro__) was the thing that
#   finally made this click for me instead of just guessing.
#
# [5] isinstance() and issubclass() checks
#   isinstance(mgr, Manager): True
#   isinstance(mgr, Employee): True  <-- True, inherited!
#   isinstance(mgr, Person): True  <-- True, 2 levels up!
#   issubclass(Manager, Person): True
#
# ==================================================
#
# =============================================================================

