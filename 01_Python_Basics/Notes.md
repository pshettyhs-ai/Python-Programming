# 📒 Module 01 — Python Basics: My Notes

**Started:** Jan 3, 2024
**Finished:** Jan 14, 2024
**Time spent:** ~12 hours over 2 weeks (slower than I expected for "basics")

---

## What I learned this module

This was my entry point into Python, coming from about 2 years of C and a
semester of C++ in college. I expected this to be a quick refresher week,
but honestly the *philosophy* of Python took longer to absorb than the
syntax itself.

### Key realizations

1. **No semicolons, no braces — indentation IS the syntax.**
   This sounds simple but it changes how you think about code blocks.
   I had a bug on day 2 where I mixed tabs and spaces in the same file and
   got `IndentationError: unindent does not match any outer indentation level`.
   Took me embarrassingly long to spot it because tabs and spaces *look*
   identical in most editors. Fixed it by setting VS Code to "render
   whitespace" and converting everything to spaces (4 spaces, PEP8 standard).

2. **Dynamic typing is a double-edged sword.**
   Coming from C where you declare `int x;` upfront, Python's "just assign
   it" approach felt unsafe at first. No more "variable not declared"
   compiler errors catching my mistakes early. But it's also why
   prototyping in Python is so much faster — you're not fighting the
   compiler over types.

3. **input() always returns a string.** This is the single most common
   mistake I see beginners (including past-me) make. Spent way too long
   debugging why `"5" + "3"` gave `"53"` instead of `8`.

4. **Python integers have arbitrary precision.** No overflow like in C's
   `int` (which wraps around at INT_MAX). You can compute `2**1000` and
   Python just... does it. As an embedded guy used to worrying about
   8-bit/16-bit overflow, this felt almost like cheating.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| IndentationError | Mixed tabs/spaces | Set editor to spaces-only, 4-space indent |
| TypeError on input | Tried `int_input + int_input` without casting | Always wrap input() in int()/float() |
| Confused `is` vs `==` | Used `is` to compare string values | `is` checks identity, `==` checks value — use `==` for value comparison |
| int("3.5") crashed | Tried direct string-to-int on decimal string | Convert to float first, then int |

---

## Things I want to revisit later

- [ ] Read more about Python's memory model (why small ints are cached -5 to 256)
- [ ] Understand `__pycache__` folder — what's actually in those .pyc files?
- [ ] Look into f-string formatting specifiers more deeply (`:.2f`, `:>10`, etc.)

---

## Honest reflection

I thought "basics" would take 2-3 days. It took two weeks because I kept
going down rabbit holes — reading about why Python caches small integers,
why `0.1 + 0.2 != 0.3` (floating point representation, same issue exists
in C too, just never noticed it there), and generally over-researching
instead of just writing code.

**Lesson for future modules:** Build first, deep-dive later. I'll keep a
separate "deep dive" notes file if curiosity strikes mid-module instead of
stalling progress.

Next up: Control Flow.
