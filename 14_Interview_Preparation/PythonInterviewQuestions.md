# 🎯 Python Interview Questions — My Preparation Notes

**Compiled by:** Pavan Shetty H S
**Last updated:** October 2024

---

## How I'm using this document

I started collecting these questions from mock interviews with seniors,
campus placement prep sessions, and questions I genuinely got wrong while
practicing on coding platforms. These aren't copy-pasted from a single
source — they're a working document I keep updating as I encounter new
questions or realize my old answers were incomplete.

I've marked questions with 🔴 if I personally got them wrong at least
once during practice, as an honest signal to myself about what needs
more review.

---

## Section 1: Python Fundamentals

### Q1. What is the difference between a list and a tuple?

Lists are mutable (can be changed after creation), tuples are immutable.
Because tuples are immutable, they're hashable and can be used as
dictionary keys or set elements — lists cannot. Tuples are also slightly
faster to iterate over due to Python's internal optimizations for
immutable objects.

### Q2. 🔴 What's the difference between `is` and `==`?

I got this wrong in an early mock interview. `==` checks value equality
(do these objects have the same VALUE), `is` checks identity (are these
literally the SAME object in memory, same id()). Two lists with identical
contents are `==` but not `is`, unless they're literally the same object
reference.

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # True -- same values
print(a is b)  # False -- different objects in memory
```

### Q3. What are Python's mutable and immutable data types?

- **Mutable**: list, dict, set, bytearray
- **Immutable**: int, float, str, tuple, frozenset, bool

### Q4. 🔴 What is the GIL (Global Interpreter Lock)?

This question came up when I mentioned multithreading on my resume during
a mock interview, and I fumbled the explanation initially. The GIL is a
mutex that allows only ONE thread to execute Python bytecode at a time,
even on multi-core systems. This means Python threading does NOT give
true parallelism for CPU-bound tasks — only I/O-bound tasks benefit from
threading, since waiting threads release the GIL. For CPU-bound
parallelism, use multiprocessing instead, since each process has its own
interpreter and GIL.

### Q5. What's the difference between `*args` and `**kwargs`?

`*args` collects extra positional arguments into a tuple. `**kwargs`
collects extra keyword arguments into a dictionary. Both let a function
accept a variable, unknown-in-advance number of arguments.

### Q6. How does Python manage memory?

Python uses automatic memory management via reference counting plus a
cyclic garbage collector (for reference cycles that reference counting
alone can't catch, like two objects referencing each other). I genuinely
didn't know about the cyclic garbage collector part until researching
this question specifically — assumed reference counting alone was the
whole story.

### Q7. 🔴 What is a mutable default argument bug?

```python
def add_item(item, items=[]):   # DANGEROUS!
    items.append(item)
    return items
```

The default list `[]` is created ONCE when the function is DEFINED, not
each time it's called. So calling `add_item('a')` then `add_item('b')`
without explicitly passing `items` will give `['a', 'b']` instead of two
separate single-item lists, because both calls share the SAME default
list object. I genuinely hit a version of this bug myself in Module 3
(Functions) with a memoization cache — for THAT specific use case the
shared default was intentional and useful, but I now know it's usually
considered a footgun when unintentional. Fix: use `items=None` and
initialize inside the function if needed.

### Q8. What is duck typing?

"If it walks like a duck and quacks like a duck, it's a duck." Python
doesn't check an object's TYPE before calling a method — it just tries to
call it. If the object has the method, it works, regardless of
inheritance or declared type. Covered this hands-on in Polymorphism.py
(Module 9) with unrelated classes all implementing `sound()`.

### Q9. Explain list comprehension vs generator expression.

List comprehension `[x for x in range(10)]` builds the ENTIRE list in
memory immediately. Generator expression `(x for x in range(10))`
produces values lazily, one at a time, on demand — far more
memory-efficient for large or infinite sequences, at the cost of being
single-use (can't iterate twice without creating a new one).

### Q10. What are decorators?

Functions that take another function as input and return a modified
version of it, typically adding behavior before/after the original
function runs, without modifying the original function's code directly.
`@decorator` syntax is shorthand for `func = decorator(func)`.

---

## Section 2: Slightly Trickier / "Gotcha" Questions

### Q11. 🔴 What does this print?

```python
x = 5
def func():
    print(x)
    x = 10
func()
```

I got this WRONG initially, guessed it would print `5`. The actual answer
is `UnboundLocalError: local variable 'x' referenced before assignment`.
Because `x` is ASSIGNED somewhere inside the function (even after the
print statement), Python treats `x` as a LOCAL variable for the ENTIRE
function scope, including the print line before the assignment. This was
a genuinely confusing one until I understood Python decides variable
scope at COMPILE time based on whether there's an assignment anywhere in
the function, not based on execution order.

### Q12. What's the output of `print(0.1 + 0.2 == 0.3)`?

`False`. Classic floating-point precision issue — not Python-specific,
exists in essentially all languages using IEEE 754 floating point
(including C, which I'd already seen this in before Python even). 0.1
and 0.2 can't be represented EXACTLY in binary floating point, so their
sum isn't exactly 0.3. Use `math.isclose()` or round to a fixed decimal
precision for float comparisons.

### Q13. What does `range(5)` actually produce?

A `range` object, not a list — it's a lazy sequence that generates
values on demand, doesn't store all 5 values in memory at once. Only
materializes into an actual list if you explicitly call `list(range(5))`.

### Q14. 🔴 What's the difference between shallow copy and deep copy?

Got tripped up by this exact thing in Module 4 before I ever heard the
interview-question version of it. Shallow copy (`.copy()` or `[:]`)
copies the OUTER container but inner mutable objects (like nested lists)
are still SHARED references. Deep copy (`copy.deepcopy()`) recursively
copies everything, including nested objects, so modifying the copy never
affects the original at any level.

### Q15. What is the difference between `__str__` and `__repr__`?

`__str__` controls the "informal", readable string representation, used
by `print()` and `str()`. `__repr__` controls the "official"
representation, ideally one that could recreate the object, used by the
REPL and inside containers like lists when you print a list of objects.
If `__str__` isn't defined, Python falls back to `__repr__`.

---

## Section 3: Things I keep forgetting and need to drill

- The exact rule for `*args`/`**kwargs` ordering in function signatures
  (positional → *args → keyword/default → **kwargs)
- Difference between `@staticmethod` and `@classmethod` (staticmethod
  doesn't receive self OR cls; classmethod receives cls but not self)
- `is` vs `==` — I still occasionally default to `is` for string/number
  comparisons out of habit before catching myself
- Time complexity of common dict/set operations (O(1) average, O(n) worst
  case due to hash collisions — easy to forget the worst-case caveat)

---

*This is a living document. I add to it every time I get something wrong
in practice or a mock interview, which is honestly often.*
