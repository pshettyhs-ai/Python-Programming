# 📒 Module 09 — Object-Oriented Programming: My Notes

**Started:** May 2, 2024
**Finished:** May 24, 2024
**Time spent:** ~38 hours (by far the longest module — almost 3.5 weeks)

---

## Why this module took so long

Everyone told me OOP is the module where you either "get" programming at
a deeper level or stay stuck writing procedural scripts forever. I took
that warning seriously and refused to rush through it. I rewrote the Bank
Management project's class structure probably four separate times during
this module just to practice different design choices.

### Key realizations, concept by concept

**Classes & Objects**
The `self` parameter confused me for the first few days — I kept forgetting
to include it in method definitions and got `TypeError: missing 1 required
positional argument: 'self'` constantly. What finally clicked: `self` is
just "the specific object this method was called on," explicitly passed
instead of implicit like C++'s `this`. Once I stopped fighting it and just
accepted "first parameter of every instance method is self, always," it
became automatic.

The class-variable vs instance-variable distinction caused a real bug in
an early draft of Student Management — I expected all Student objects to
share a counter via a class variable, but assigning to it through an
INSTANCE (`student.counter = x`) creates a new instance variable that
shadows the class variable instead of modifying the shared one. Took
genuine debugging time to understand why my "shared" counter wasn't
actually shared anymore after one assignment.

**Constructors**
Learned that `__init__` isn't technically "the constructor" in the purest
sense — `__new__` creates the object, `__init__` initializes it. For
practical purposes I only ever touch `__init__`. The `@classmethod`
pattern for "alternative constructors" (like `Date.from_string()`) was a
genuinely useful pattern I didn't expect — Python doesn't support
constructor overloading like Java/C++, and this is the idiomatic
workaround.

**Inheritance**
Single and multilevel inheritance felt natural almost immediately —
basically the same mental model as C++ but cleaner syntax. Multiple
inheritance and MRO (Method Resolution Order) is where I genuinely
struggled for several days. The "diamond problem" example
(`class D(B, C)` where both B and C inherit from A) made me expect some
kind of ambiguity error. Instead Python resolves it deterministically via
C3 linearization, and B's method wins because B is listed first. Printing
`ClassName.__mro__` explicitly was the debugging tool that actually made
this click — I stopped guessing and started just checking the resolution
order directly.

**Polymorphism**
Duck typing surprised me — coming from a brief C++ exposure where I
expected polymorphism to REQUIRE a common base class, Python doesn't care.
If an object has the method you're calling, it works, regardless of
inheritance relationships. `Duck`, `Dog`, and `Robot` in my demo share
literally no parent class and polymorphism still works fine because they
all implement `sound()`.

Operator overloading (`__add__`, `__sub__`, `__eq__`, `__str__`) was fun
to experiment with via a Vector class. Realized `__str__` controls
`print()` output while `__repr__` controls REPL/debug representation —
mixed these up at first and wondered why my print statements looked
different from what showed up when I just typed the variable name in the
interactive shell.

**Encapsulation**
This was the most philosophically different concept from what I expected.
Python has NO true private variables — `__balance` style double-underscore
attributes are just name-mangled (renamed internally to
`_ClassName__balance`), not actually enforced. I could still access
`acc._BankAccount__balance` directly if I really wanted to. Coming from
expecting hard access control like C++'s `private` keyword, this felt
almost reckless at first. Read about Python's design philosophy here —
"we're all consenting adults," trusting developers to respect naming
conventions (`_protected`, `__private`) rather than enforcing them with
compiler errors.

`@property` decorators became my preferred pattern for anything needing
validation — lets me write `obj.value = x` syntax while running validation
logic behind the scenes, like the Temperature class example where setting
celsius below absolute zero raises a ValueError. Best of both worlds:
clean attribute syntax, controlled behavior.

**Abstraction**
Took the longest to see the actual point of, separate from inheritance.
My early confusion: "isn't ABC + abstractmethod just... inheritance with
extra steps?" The distinction that finally clicked: abstraction is about
FORCING subclasses to implement specific methods (enforced at
instantiation time, not just at call time) and preventing the base class
from being instantiated directly at all. It's a CONTRACT.

I actually hit this exact protection later while building the Employee
Management project — forgot to implement `calculate_bonus()` in a
subclass and Python refused to even let me CREATE the object
(`TypeError: Can't instantiate abstract class ... with abstract method
calculate_bonus`), which caught my mistake immediately instead of letting
it surface later as an `AttributeError` at some random point when the
method actually got called.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| Forgot `self` parameter | TypeError: missing 1 required positional argument | Always include self as first param in instance methods |
| Class variable "broke" after instance assignment | Expected shared counter, got per-instance shadow | Modify class variables via ClassName.var, not instance.var |
| MRO confusion (diamond inheritance) | Wrong assumption about which parent's method wins | Printed __mro__ explicitly to see actual resolution order |
| Mixed up __str__ vs __repr__ | print() output looked different from REPL display | Learned __str__ = print(), __repr__ = debug/REPL representation |
| Expected true private variables | Could still access "private" __attr via name mangling | Accepted Python's convention-based privacy model |
| Forgot abstract method in subclass | TypeError at instantiation, not at call time | Implemented ALL abstract methods before instantiating |
| Tried instantiating abstract base class directly | TypeError: Can't instantiate abstract class | Understood this is the entire point — only subclasses should be created |

---

## Optimization / design reflection

Rewrote the Bank Management System's class hierarchy three times during
this module as my understanding of encapsulation and abstraction matured:

1. **First draft:** One giant `BankAccount` class with if/elif chains for
   account type behavior (savings vs current vs fixed deposit).
2. **Second draft:** Split into subclasses with inheritance, but exposed
   `balance` as a plain public attribute — realized this let any code
   directly set `account.balance = 999999999` with zero validation.
3. **Final draft (used in the actual project):** Private `__balance` with
   `@property` getter, validated `deposit()`/`withdraw()` methods, and an
   abstract `BankAccount` base class that forces every account type to
   implement its own interest calculation method.

This iteration is honestly the clearest evidence I have of actually
LEARNING something this module rather than just reading about it.

---

## Lessons learned after this module

- `self` is just an explicit reference to "this object" — stop fighting it
- Class variables are shared; instance assignment creates a shadow, not
  a mutation of the shared value
- Print `__mro__` when multiple inheritance behavior is unclear — don't guess
- Python's encapsulation is convention-based, not enforced — respect the
  underscore conventions anyway, they communicate intent clearly
- `@property` is the cleanest way to add validation without breaking
  attribute-style syntax
- Abstract base classes are a CONTRACT — they catch missing implementations
  at instantiation time, which is genuinely useful, not just academic

Next up: Advanced Python — decorators, generators, context managers, and
finally multithreading/multiprocessing, which I've been curious about
since I started this whole journey because of how relevant they are to
embedded systems work too.
