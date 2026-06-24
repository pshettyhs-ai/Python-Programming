# 📒 Module 05 — Strings: My Notes

**Started:** Mar 4, 2024
**Finished:** Mar 22, 2024
**Time spent:** ~22 hours (regex alone ate up about 12 of those)

---

## What I learned this module

String handling itself (methods, formatting) was fairly quick to pick up
since the concepts map closely to what I already understood from C's
string.h functions, just with way more built-in convenience. Regex was
its own beast entirely.

### Key realizations

1. **Strings are immutable — every operation returns a NEW string.**
   `my_str.upper()` doesn't change `my_str`, it returns a new string that
   you need to capture: `my_str = my_str.upper()`. Forgot this constantly
   in week 1 and kept being confused why my "modifications" weren't
   sticking.

2. **f-strings are objectively the best formatting option** for anything
   I write going forward. I documented `%` and `.format()` because I see
   them in older code/StackOverflow answers from years ago, but f-strings
   are faster and more readable. Not going back.

3. **Regex really is a separate mini-language.** I spent almost two full
   days just building intuition for character classes (`\d`, `\w`, `\s`)
   before quantifiers (`*`, `+`, `?`, `{n}`) started making sense together.
   Kept a personal cheat sheet (in the comments at the top of
   RegularExpressions.py) that I referred to constantly.

4. **`re.match()` vs `re.search()` distinction is sneaky.** `match()` only
   checks from the START of the string — if your pattern would match
   somewhere in the middle but not at position 0, `match()` returns None
   while `search()` would find it. I had a bug where my email validator
   used `search()` instead of `match()` with anchors and accidentally
   accepted garbage like `"asdf pavan@gmail.com asdf"` as a valid email
   because search() found a VALID substring inside an invalid string.
   Fixed by using `^...$` anchors with match(), or fullmatch().

5. **Unanchored patterns are dangerous for validation.** `\d+` matches
   ANY digit sequence anywhere, including as a substring of something
   longer. For real validation you need `^` and `$` (or `re.fullmatch()`)
   to make sure the ENTIRE string matches, not just part of it.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| String "mutation" didn't stick | `my_str.upper()` result discarded | Reassign: `my_str = my_str.upper()` |
| Email validator too permissive | Used unanchored regex, garbage strings passed | Added `^` and `$` anchors |
| match() returned None unexpectedly | Pattern existed mid-string, not at start | Switched to `search()` or restructured pattern |
| Forgot raw strings for regex | Backslashes got interpreted as escape sequences | Always prefix regex patterns with `r"..."` |

---

## A genuinely confusing debugging session

I wrote a phone validation regex without the `r` prefix:
`pattern = "\d{10}"` instead of `r"\d{10}"`. It actually still worked in
this specific case because `\d` isn't a recognized Python escape sequence
so Python left it alone — but I got lucky. With patterns like `\b` (word
boundary in regex, but BACKSPACE in Python string escapes), forgetting
the raw string prefix would have silently broken things in a very
confusing way. Now I prefix EVERY regex pattern with `r"..."`, no
exceptions, even when I think I don't need to.

---

## Lessons learned after this module

- f-strings for all formatting, no exceptions going forward
- Regex needs to be practiced with REAL messy data, not just clean
  textbook examples — that's when the edge cases show up
- Always use raw strings (`r"..."`) for regex patterns
- Anchor your patterns (`^`, `$`) when doing full-string validation
- Keep a personal regex cheat sheet — I still refer to mine constantly

Next up: Modules and Packages — looking forward to organizing code into
reusable pieces instead of one giant script.
