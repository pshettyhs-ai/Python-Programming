# 📒 Module 04 — Data Structures: My Notes

**Started:** Feb 12, 2024
**Finished:** Feb 28, 2024
**Time spent:** ~20 hours (longest module so far)

---

## What I learned this module

This module took the longest because it's where Python's "batteries
included" philosophy really showed itself. Coming from C arrays (fixed
size, manual memory management, no built-in methods), having Lists,
Tuples, Sets, and Dictionaries with rich method sets felt like getting a
whole toolbox after only having a hammer.

### Key realizations

1. **Lists vs Tuples — mutability is the whole point.** I used to think
   "why would I ever choose a tuple over a list, lists can do everything."
   Wrong framing. Tuples being immutable means they're hashable (can be
   dict keys, set members) and signal "this shouldn't change" to anyone
   reading the code. I now default to tuples for fixed records like
   coordinates and RGB values.

2. **`{}` creates a dict, not an empty set.** This tripped me up badly.
   I wrote `my_set = {}` expecting an empty set and then got
   `AttributeError: 'dict' object has no attribute 'add'` when I tried
   `my_set.add(5)`. Must use `set()` for an empty set.

3. **Shallow copy vs deep copy is a real bug source.** `list2 = list1`
   doesn't copy anything — both names point to the same list object.
   Modifying one modifies "both" (because there's really only one).
   Learned to use `.copy()` or `list1[:]` for actual independent copies.
   This will matter even more once I get into nested structures (a
   shallow copy of a list-of-lists still shares the inner lists!).

4. **Sets eliminated a LOT of manual duplicate-removal code** I used to
   write in C with nested loops. `set(my_list)` does in one line what
   used to take me 8 lines of nested iteration and a "seen" tracking
   array.

5. **Dictionaries are basically hash maps**, which I'd only read about
   abstractly in my DSA textbook before this. Seeing `dict.get(key, default)`
   prevent KeyError crashes, and seeing how `collections.Counter` is
   built ON TOP of dict, made the underlying concept click much better
   than the textbook diagrams did.

6. **List comprehensions changed how I write loops entirely.** I went
   back and rewrote some of my Module 2 loop exercises as comprehensions
   just to practice the syntax. They're not always more readable (nested
   comprehensions especially can get cryptic) but for simple
   filter/transform operations they're genuinely better than a 4-line
   for loop.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| `{}` for empty set | AttributeError on .add() | Used `set()` instead |
| Shallow copy bug | Modifying a "copy" changed the original too | Used `.copy()` or `[:]` for real copies |
| KeyError on missing dict key | Direct `dict['missing_key']` access crashed | Switched to `.get(key, default)` |
| Forgot comma in single-tuple | `(42)` was just an int, not a tuple | Added trailing comma: `(42,)` |
| KeyError using remove() on set | `.remove()` on missing set item crashed | Used `.discard()` when item might not exist |
| Mutated list while iterating | Removing items from a list while looping skipped elements | Iterated over a copy: `for x in my_list[:]` |

---

## Optimization attempt: Word frequency counter

First wrote this manually with a plain dict and `.get(word, 0) + 1`
pattern. Later discovered `collections.Counter` does the exact same thing
with cleaner syntax AND comes with `.most_common(n)` built in. Replaced my
manual version. Good reminder to check the standard library before
reinventing something — Python's `collections` module alone has saved me
a lot of boilerplate (`defaultdict`, `Counter`, `OrderedDict`, `namedtuple`
are all things I want to explore more later).

---

## Lessons learned after this module

- Choose the right data structure for the job: list (ordered, mutable),
  tuple (ordered, immutable), set (unique, unordered), dict (key-value)
- Always be careful with copy semantics — `=` doesn't copy, it aliases
- Check `collections` module before writing manual counting/grouping logic
- List/dict comprehensions are great for simple transforms, but don't
  sacrifice readability for "one-liner" bragging rights

Next up: Strings — looking forward to regex since I've heard it's painful
but powerful.
