# =============================================================================
# Polymorphism.py
# Author  : Pavan Shetty H S
# Date    : May 2024
# Topic   : Polymorphism -- method overriding, duck typing, operator overload
# =============================================================================
#
# Notes from Pavan:
# "Poly" = many, "morph" = forms. The term sounds intimidating but the
# concept is simple once you see it: same method name, different
# behavior depending on the object. Python's duck typing took this even
# further than I expected from my C++ background -- you don't even need
# a common parent class for polymorphism to work in Python.
# =============================================================================

print("=" * 50)
print("    POLYMORPHISM DEMO")
print("=" * 50)

# ---------------------
# Method Overriding (most common form of polymorphism)
# ---------------------
print("\n[1] Method Overriding")

class Shape:
    def area(self):
        return 0

    def describe(self):
        print(f"  This shape has area: {self.area()}")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):   # OVERRIDES parent's area()
        return round(3.14159 * self.radius ** 2, 2)

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):   # OVERRIDES parent's area()
        return self.length * self.width

shapes = [Circle(5), Rectangle(4, 6), Circle(2)]
for shape in shapes:
    shape.describe()   # SAME method call, DIFFERENT behavior per object

# ---------------------
# Duck Typing -- "if it walks like a duck and quacks like a duck..."
# ---------------------
print("\n[2] Duck Typing -- no shared parent class needed!")

class Duck:
    def sound(self):
        return "Quack!"

class Dog:
    def sound(self):
        return "Woof!"

class Robot:
    def sound(self):
        return "Beep boop!"

# These three classes share NO common parent, yet I can treat them
# uniformly because they all implement sound(). This surprised me coming
# from C++ where I'd have expected to need an abstract base class first.
def make_it_speak(thing):
    print(f"  {thing.sound()}")

print("  Calling make_it_speak() on unrelated classes:")
for entity in [Duck(), Dog(), Robot()]:
    make_it_speak(entity)

print("  None of these classes share a parent. Python doesn't care --")
print("  it just checks if the object HAS a sound() method. This is")
print("  duck typing: 'if it has the method I need, I don't care what it IS'")

# ---------------------
# Operator Overloading -- polymorphism applied to built-in operators
# ---------------------
print("\n[3] Operator Overloading")

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        # This makes the + operator work between two Vector objects
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        # Controls what print() shows for this object
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        # Controls what shows in REPL / debugging contexts
        return f"Vector(x={self.x}, y={self.y})"

v1 = Vector(2, 3)
v2 = Vector(4, 1)

print(f"  v1 = {v1}")
print(f"  v2 = {v2}")
print(f"  v1 + v2 = {v1 + v2}")    # this works because of __add__
print(f"  v1 - v2 = {v1 - v2}")
print(f"  v1 == Vector(2,3): {v1 == Vector(2, 3)}")

print("""
  Realization: + on Vector objects works because I defined __add__.
  Without it, Python would throw:
  TypeError: unsupported operand type(s) for +: 'Vector' and 'Vector'
  This is how Python lets custom classes "plug into" built-in syntax.
""")

# ---------------------
# Built-in polymorphism examples (things I already used without realizing)
# ---------------------
print("[4] Built-in polymorphism I'd been using without realizing it")
print(f"  len('hello') = {len('hello')}")
print(f"  len([1,2,3]) = {len([1,2,3])}")
print(f"  len({{'a':1,'b':2}}) = {len({'a':1,'b':2})}")
print("  Same len() function, completely different internal behavior")
print("  per type. This IS polymorphism, just built into Python already.")

print(f"\n  '+' on ints: {5 + 3}")
print(f"  '+' on strings: {'a' + 'b'}")
print(f"  '+' on lists: {[1,2] + [3,4]}")
print("  Same operator, different meaning per type -- also polymorphism.")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Polymorphism.py
# =============================================================================
#
# ==================================================
#     POLYMORPHISM DEMO
# ==================================================
#
# [1] Method Overriding
#   This shape has area: 78.54
#   This shape has area: 24
#   This shape has area: 12.57
#
# [2] Duck Typing -- no shared parent class needed!
#   Calling make_it_speak() on unrelated classes:
#   Quack!
#   Woof!
#   Beep boop!
#   None of these classes share a parent. Python doesn't care --
#   it just checks if the object HAS a sound() method. This is
#   duck typing: 'if it has the method I need, I don't care what it IS'
#
# [3] Operator Overloading
#   v1 = Vector(2, 3)
#   v2 = Vector(4, 1)
#   v1 + v2 = Vector(6, 4)
#   v1 - v2 = Vector(-2, 2)
#   v1 == Vector(2,3): True
#
#   Realization: + on Vector objects works because I defined __add__.
#   Without it, Python would throw:
#   TypeError: unsupported operand type(s) for +: 'Vector' and 'Vector'
#   This is how Python lets custom classes "plug into" built-in syntax.
#
# [4] Built-in polymorphism I'd been using without realizing it
#   len('hello') = 5
#   len([1,2,3]) = 3
#   len({'a':1,'b':2}) = 2
#   Same len() function, completely different internal behavior
#   per type. This IS polymorphism, just built into Python already.
#
#   '+' on ints: 8
#   '+' on strings: ab
#   '+' on lists: [1, 2, 3, 4]
#   Same operator, different meaning per type -- also polymorphism.
#
# ==================================================
#
# =============================================================================

