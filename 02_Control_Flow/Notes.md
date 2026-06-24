# 📒 Module 02 — Control Flow: My Notes

**Started:** Jan 15, 2024
**Finished:** Jan 22, 2024
**Time spent:** ~8 hours

---

## What I learned this module

Control flow felt very familiar coming from C — if/elif/else and for/while
loops follow the same logic I already knew. The differences were mostly
syntactic, but a few Python-specific quirks genuinely surprised me.

### Key realizations

1. **`range()` is exclusive of the stop value.** `range(5)` → 0,1,2,3,4.
   I wrote a loop expecting 5 iterations to include the number 5 itself
   and got an off-by-one bug in my very first "print multiplication table"
   exercise. Now I just mentally read `range(n)` as "n times, starting
   from 0" instead of thinking about boundaries.

2. **`for...else` and `while...else` exist!** I didn't know this was a
   thing until I saw it in a forum post about searching algorithms. The
   `else` block runs only if the loop completes WITHOUT a `break`. It's
   genuinely useful for search patterns ("did I find it or not") but I
   rarely see it used in real code — most people prefer a flag variable
   because the `else` placement is non-obvious to readers. I'll probably
   use a flag variable in production code but I'm glad I know this exists.

3. **`pass` as a no-op.** Used heavily when I'm sketching out a program's
   skeleton — defining all my functions and classes first with `pass`
   bodies, then filling in logic one at a time. This became my standard
   workflow for the Student Management project later.

4. **Nested if statements get unreadable fast.** I wrote a loan eligibility
   checker with 3 levels of nesting (see NestedIf.py) and immediately
   didn't like how it looked. Refactored it into early-return style inside
   a function and it was SO much cleaner. This is now my default approach
   for multi-condition checks.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| Off-by-one in range() | Expected range(5) to include 5 | Remembered: range(n) = 0 to n-1 |
| Infinite while loop | Forgot to decrement counter variable | Always double check loop variable updates BEFORE running |
| Used break instead of continue | Loop exited completely when I wanted to skip one iteration | Re-read logic, swapped to continue |
| Confusing nested-if logic | 3-level nested if was hard to trace mentally | Refactored to early-return pattern in a function |

---

## A mistake worth remembering

I once wrote a `while True` loop for a menu system and forgot to put a
`break` condition that could actually be reached because I had a typo in
my comparison (`==` vs `=` muscle memory from... wait, Python doesn't even
allow `=` in conditions, it throws a SyntaxError immediately. That actually
saved me — in C this kind of typo silently compiles and causes weird bugs.
One thing Python genuinely does better here.)

The actual bug was different: my break condition checked `user_choice == 6`
but I'd cast user_choice to int AFTER the check, so it was always comparing
a string to an int and never matching. Classic input-type carelessness.

---

## Lessons learned after this module

- Always cast input() before comparing to numbers (recurring theme from
  module 1 — I keep relearning this lesson in new contexts)
- Deeply nested conditionals are a code smell — refactor early
- Trace through loop boundaries on paper before running, especially with
  range() and slicing later on

Next up: Functions.
