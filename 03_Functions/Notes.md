# 📒 Module 03 — Functions: My Notes

**Started:** Jan 29, 2024
**Finished:** Feb 9, 2024
**Time spent:** ~14 hours

---

## What I learned this module

This is where Python started feeling genuinely different from C, not just
syntactically lighter. The flexibility around function arguments is
something C just doesn't offer without a lot of boilerplate (function
overloading doesn't even exist in C; you'd need separate function names
or variadic macros which are painful).

### Key realizations

1. **Default arguments eliminate so much repetition.** In C, if I wanted
   a function with "optional" parameters, I'd often write multiple
   overloaded-looking functions or pass sentinel values like -1 to mean
   "not provided." Python's `def func(x, y=10):` solves this directly.

2. **`*args` and `**kwargs` order rule took practice.** I kept forgetting
   that the order must be: positional → `*args` → keyword/default → `**kwargs`.
   Wrote `Arguments.py` specifically to drill this into memory because I
   got `SyntaxError: positional argument follows keyword argument` more
   than once.

3. **The mutable default argument trap (haven't hit it yet here, but read
   about it while studying memoization).** Using `def f(x, memo={})` works
   for the Fibonacci memoization trick ON PURPOSE in my Recursion.py file,
   but I now know this is usually considered a bug-prone pattern because
   the default dict is created ONCE when the function is defined, not each
   call. For the memo cache it's actually useful behavior, but for general
   use I now default to `def f(x, memo=None): memo = memo or {}` instead.

4. **Lambda functions are NOT a replacement for normal functions.** I went
   through a phase of trying to lambda-ify everything because it felt
   "more Pythonic" — wrong instinct. Readability lost. Now I only use
   lambdas for short throwaway logic passed into `sorted()`, `map()`,
   `filter()`.

5. **Recursion depth limit is real.** Hit `RecursionError: maximum
   recursion depth exceeded` while testing a broken Fibonacci function
   that was missing its base case. The stack trace was honestly terrifying
   the first time — hundreds of lines repeating the same function call.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| Global variable not updating | Forgot `global` keyword inside function | Added `global counter` before modifying it |
| SyntaxError with args | Put keyword arg before positional arg in a call | Reordered: positional first, then keyword |
| Infinite recursion | Forgot base case in a test recursive function | Added proper base case, tested with small n first |
| Naive Fibonacci too slow | fibonacci(35) took forever | Learned memoization, added a memo dict cache |
| Mixed up positional argument order | Called describe_pet("Tommy", "dog") instead of (animal, name) | Started using keyword arguments for clarity when order isn't obvious |

---

## Optimization attempt: Fibonacci

This was my first real taste of "the same correct logic can have wildly
different performance." Recursive naive Fibonacci is O(2^n) — tried running
`fibonacci(40)` and gave up waiting after about a minute. Memoized version
computes `fibonacci_memo(50)` instantly. This pushed me to actually care
about time complexity instead of treating it as an abstract DSA-course
concept. It's the first time Big-O felt like something with real
consequences rather than an exam topic.

---

## Lessons learned after this module

- Function signatures are a form of documentation — name your parameters well
- Don't over-engineer with lambdas; clarity > cleverness
- Always think about base cases FIRST when writing recursive functions
- Memoization is a genuinely simple, genuinely powerful optimization technique

Next up: Data Structures (Lists, Tuples, Sets, Dictionaries) — looking
forward to this one since I'll finally be able to build slightly bigger
programs.
