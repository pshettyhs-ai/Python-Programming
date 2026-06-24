# 📒 Module 08 — Exception Handling: My Notes

**Started:** Apr 18, 2024
**Finished:** Apr 27, 2024
**Time spent:** ~10 hours

---

## What I learned this module

I'd already been using try/except informally since the File Handling
module without truly understanding the full structure (else, finally,
exception hierarchies). This module was about going back and properly
learning the mechanics instead of just pattern-matching code I'd seen
online.

### Key realizations

1. **`else` on try blocks runs ONLY when no exception occurred.** I didn't
   know this clause existed for a while. It's useful for separating "the
   risky operation" from "what to do after it succeeds" — keeps the try
   block minimal (only the actual risky line) instead of putting
   everything inside try, which can accidentally catch exceptions from
   code that wasn't actually risky.

2. **`finally` ALWAYS runs**, success, failure, even if there's a `return`
   inside the try or except block. This makes it the right place for
   cleanup code (closing files, releasing resources) — though I now know
   `with` statements handle file closing automatically, so finally is more
   relevant for other cleanup like closing database connections in the
   Database module ahead.

3. **Catching generic `Exception` is a trap I want to avoid.** It "works"
   in the sense that it catches everything, but it also HIDES bugs I
   didn't mean to suppress. If I catch `Exception` broadly to handle
   "file not found," I'd also silently swallow a typo-induced
   `NameError` or `AttributeError` that I actually wanted to see and fix.
   Now my rule: catch the SPECIFIC exception type I expect, and only use
   bare `Exception` as a last-resort safety net at the outermost level of
   a program (like wrapping a whole main() function for a CLI tool so it
   doesn't crash ugly in front of a user).

4. **Custom exceptions became genuinely useful once I started designing
   the Bank Management project.** Generic `ValueError` for everything
   doesn't let me distinguish "insufficient funds" from "account frozen"
   from "wrong PIN" when catching errors. Building an exception hierarchy
   (`BankError` as base, with `InsufficientFundsBankError`,
   `AccountFrozenError`, `InvalidPINError` as subclasses) means I can
   catch the BASE class to handle "any bank error generically," or catch
   a SPECIFIC subclass when I need different handling logic.

5. **`raise` without arguments inside an except block re-raises the SAME
   exception**, preserving the original traceback. Different from
   `raise SomeNewException(...)` which starts a fresh traceback. Useful
   when I want to log something and then let the error propagate normally.

6. **`raise ... from ...` for exception chaining** was new to me — lets
   you wrap a low-level exception in a higher-level, more meaningful one
   while keeping the original cause attached (`__cause__`). Saw this used
   in a library's source code and wanted to understand how to do it myself.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| Caught Exception too broadly | A typo (NameError) got silently swallowed by a broad except | Narrowed to specific exception types |
| Didn't know else existed | Put "success" logic inside try block, risking catching unrelated errors | Moved success-path code to else block |
| Forgot finally runs even with return | Assumed cleanup wouldn't happen if function returned early from try | Tested it explicitly — finally DOES still run |
| Confusing 'raise' vs 'raise NewException()' | Wanted to re-raise as-is but created a new exception, losing original traceback | Used bare 'raise' to preserve original traceback |

---

## Why custom exceptions matter (a realization, not really a "bug")

Before this module, my instinct for any error condition was: `raise
ValueError("something went wrong")`. The problem becomes obvious once you
have a program complex enough to have MULTIPLE distinct error conditions
that need different handling. If everything is a ValueError, my except
block can't tell "insufficient funds" apart from "invalid account number"
without parsing the error message STRING, which is fragile and ugly.
Custom exception classes make the error TYPE itself meaningful.

---

## Lessons learned after this module

- Catch specific exceptions, not bare Exception, except as an outer
  safety net
- Use else for success-path logic, keep try blocks minimal
- finally is for guaranteed cleanup, runs no matter what
- Build exception hierarchies for any non-trivial application — this
  will directly shape how I write the Bank Management System project
- `raise` (bare) re-raises preserving traceback; use it when logging then
  propagating

Next up: OOP — Classes and Objects. This is the module I've been most
anticipating and most nervous about, since everyone says OOP is where
people either "get" Python or stay stuck at beginner level forever.
