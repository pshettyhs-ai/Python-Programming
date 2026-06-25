# 🎯 OOP Interview Questions — My Preparation Notes

**Compiled by:** Pavan Shetty H S
**Last updated:** October 2024

---

## Why a separate file for OOP

OOP questions kept showing up as a distinct CATEGORY in every mock
interview I did, often as a dedicated 10-15 minute segment separate from
general Python syntax questions. Decided to keep these organized
separately since the OOP module (Module 9) took me the longest of
anything in this whole repository, and I want this prep to reflect that
same depth.

---

## Section 1: Core Concepts

### Q1. What are the four pillars of OOP?

Encapsulation, Inheritance, Polymorphism, Abstraction. I use the mnemonic
"EIPA" — though honestly I just remember it now from having implemented
all four in Module 9's files (Encapsulation.py, Inheritance.py,
Polymorphism.py, Abstraction.py).

### Q2. What is the difference between a class and an object?

A class is a blueprint/template. An object is a specific INSTANCE created
from that blueprint, with its own actual data. `class Student:` defines
the shape; `s1 = Student("Pavan", "ECE")` creates one real object
following that shape.

### Q3. 🔴 What's the difference between class variables and instance variables?

I genuinely got bitten by this exact issue while building the Student
Management project — expected a class variable used as a shared counter
to update across all instances, but assigning to it via an INSTANCE
(`student.counter = x`) created a new instance-level variable that
SHADOWS the class variable instead of modifying the shared one. Class
variables are shared across ALL instances of a class; instance variables
are unique to each individual object. To actually modify a class
variable, you must do it via the CLASS itself
(`ClassName.variable = x`), not through an instance.

### Q4. Explain `self` in Python classes.

`self` is an explicit reference to "the specific object this method was
called on" — Python passes it automatically as the first argument to
every instance method, but you must explicitly INCLUDE it in the method
DEFINITION. Other languages (like Java/C++) have an implicit `this`;
Python makes it explicit, which I initially found odd but now actually
prefer because it's clearer where instance data comes from.

### Q5. What is `__init__`? Is it a constructor?

`__init__` initializes a NEWLY created object — it runs automatically
right after object creation. Strictly speaking, `__new__` is what
actually CREATES the object; `__init__` just sets it up afterward. For
99% of practical purposes, `__init__` is what people mean when they say
"the constructor" in Python, and that's a fine simplification for most
interview answers, but I like knowing the more precise distinction.

---

## Section 2: Inheritance

### Q6. What is Method Resolution Order (MRO)?

The order Python searches through a class hierarchy to find a method or
attribute, especially relevant for multiple inheritance. Python uses C3
linearization. You can inspect it directly via `ClassName.__mro__`. This
was the single tool that made multiple inheritance actually make sense
to me — I stopped guessing and just printed the MRO directly when unsure.

### Q7. 🔴 Explain the diamond problem and how Python resolves it.

When class D inherits from both B and C, and both B and C inherit from a
common class A, calling a method defined in A (and possibly overridden in
both B and C) could be ambiguous — which version does D get? I expected
Python to either raise an error or pick unpredictably. It does neither —
C3 linearization deterministically resolves this based on the ORDER
classes are listed in the inheritance declaration
(`class D(B, C):` favors B's version over C's, assuming both override the
same method). Verified this myself by printing `D.__mro__` rather than
trusting the explanation blindly.

### Q8. What's the difference between method overriding and method overloading?

Overriding: a subclass redefines a method that exists in its parent class
with the SAME signature, changing its behavior. Python supports this
directly. Overloading: defining MULTIPLE versions of the same method name
with DIFFERENT parameter signatures — Python does NOT support this
natively (unlike Java/C++). The common Python workaround is default
arguments, `*args`/`**kwargs`, or `@classmethod` for alternative
constructors, as I used in `Date.from_string()` in Constructors.py.

### Q9. What does `super()` do?

Calls a method from the parent class, typically used to extend (not
completely replace) parent behavior in an overridden method, especially
common in `__init__` to ensure parent initialization still runs alongside
the child's own setup.

---

## Section 3: Polymorphism & Duck Typing

### Q10. What is duck typing and how does it relate to polymorphism?

Python doesn't check an object's declared TYPE before calling a method —
it just attempts the call. If the object happens to have that method, it
works, regardless of inheritance hierarchy. This means polymorphism in
Python doesn't strictly REQUIRE a shared base class, unlike languages
with stricter static typing. Demonstrated this with unrelated `Duck`,
`Dog`, `Robot` classes all implementing `sound()` with zero shared
inheritance.

### Q11. What is operator overloading? Give an example.

Defining special "dunder" methods (`__add__`, `__sub__`, `__eq__`, etc.)
on a custom class to make built-in operators (`+`, `-`, `==`) work with
instances of that class. Built a `Vector` class where `v1 + v2` works
because I defined `__add__` to combine the x/y components.

---

## Section 4: Encapsulation & Abstraction

### Q12. 🔴 Does Python have true private variables?

This was a genuine surprise to me during Module 9, and apparently a
common interview gotcha too. NO — Python's "private" attributes
(double-underscore prefix, like `__balance`) are only NAME-MANGLED
(internally renamed to `_ClassName__balance`), not truly enforced. You
CAN still access them directly if you know the mangled name. Python's
philosophy here is convention-based ("we're all consenting adults"),
relying on developers respecting `_protected` / `__private` naming
conventions rather than the language enforcing hard access control like
C++'s `private` keyword does.

### Q13. What's the purpose of `@property`?

Lets you define methods that behave like attributes from the OUTSIDE
(`obj.value` instead of `obj.get_value()`), while still allowing
validation logic to run behind the scenes via a setter. Used this in a
`Temperature` class to reject impossible values (below absolute zero)
while keeping clean attribute-style syntax for valid use.

### Q14. What is an abstract class? Why use one when regular inheritance exists?

A class that CANNOT be instantiated directly, used to define a CONTRACT
that subclasses must fulfill (via `@abstractmethod`-decorated methods
that subclasses are FORCED to implement, checked at instantiation time
by Python). The distinction from "just inheritance" that took me longest
to internalize: abstraction is specifically about enforcing that certain
methods MUST be implemented before an object can even be created, not
just about reusing code. Personally hit this protection while building
the Employee Management project — forgot to implement a required method
in a subclass and Python refused to let me instantiate it at all,
catching my mistake immediately rather than later when the missing
method actually got called.

### Q15. Can you instantiate a class that inherits from an ABC but doesn't implement all abstract methods?

No — Python raises `TypeError: Can't instantiate abstract class
<ClassName> with abstract method <method_name>` at the moment you try to
create an instance, not when the missing method is actually called. This
is genuinely useful, not just academic — it surfaces incomplete
implementations immediately instead of letting a bug hide until some
later code path happens to call the missing method.

---

## My honest self-assessment after compiling this

OOP is the section of Python I feel most confident discussing in an
interview now, mostly BECAUSE I struggled with it the longest during
actual learning (Module 9 took 3.5 weeks). The questions I marked 🔴 are
ones where I genuinely got the WRONG answer first, then had to actually
understand why before the correct answer stuck. I trust those answers
more than ones I just read and accepted without friction.
