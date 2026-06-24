# 📒 Module 07 — File Handling: My Notes

**Started:** Apr 4, 2024
**Finished:** Apr 16, 2024
**Time spent:** ~15 hours

---

## What I learned this module

This is the module where my programs stopped feeling like throwaway
scripts and started feeling like actual TOOLS that persist data. Up until
now, every program lost all its state the moment it ended. Being able to
write to a file and read it back next time felt like a genuine milestone.

### Key realizations

1. **`with open(...) as f:` is not optional ceremony — it actually
   matters.** Before understanding context managers, I manually called
   `f.close()` and forgot it constantly, especially in functions with
   multiple return paths or when an exception occurred mid-function and
   skipped my cleanup code entirely. `with` guarantees the file closes no
   matter what happens inside the block, even on exceptions.

2. **'w' mode WIPES the file first. I learned this by losing data.**
   Opened a log file in 'w' mode thinking I was just "writing to it",
   not realizing it truncates existing content immediately upon opening.
   Lost an afternoon's worth of test log entries. Now I always pause and
   consciously think "do I want overwrite or append" before choosing 'w'
   vs 'a'.

3. **Don't manually parse CSV with `.split(",")`.** Worked for simple
   cases, broke immediately on any field containing a comma (like an
   address). The `csv` module handles quoting and escaping correctly.
   Lesson here is bigger than CSV specifically: if Python has a standard
   library module for a well-known file format, use it instead of
   hand-rolling a parser.

4. **`csv.DictReader` returns every value as a STRING**, even numbers.
   Tried to filter students by `row['cgpa'] > 8.5` directly and got
   `TypeError: '>' not supported between instances of 'str' and 'float'`.
   Now I always explicitly cast numeric CSV fields.

5. **JSON's dump/dumps and load/loads naming convention took practice
   to internalize.** My mnemonic: the 's' suffix versions work with
   strings (dumps = dict to string, loads = string to dict), the
   non-s versions work directly with file objects.

6. **Not everything is JSON-serializable.** Tried serializing a `datetime`
   object directly and got `TypeError: Object of type datetime is not
   JSON serializable`. Fixed by converting to `.isoformat()` string first.

7. **`newline=""` matters when writing CSV on Windows.** Without it, I got
   extra blank lines between every row in the output file. This is a
   Windows-specific line-ending quirk (`\r\n` vs `\n`) that the csv module
   docs explicitly warn about.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| Lost data with 'w' mode | Opened existing log file in write mode, content wiped | Switched to 'a' (append) where appropriate; now double-check mode before running |
| Manual CSV parsing broke | `.split(",")` split a field that contained a comma | Used the `csv` module instead |
| TypeError comparing CSV numbers | DictReader values are strings | Explicitly cast with `float()`/`int()` |
| UnicodeDecodeError | Read a file with special characters without specifying encoding | Always pass `encoding="utf-8"` explicitly |
| Extra blank lines in CSV (Windows) | Didn't pass `newline=""` to open() | Added `newline=""` parameter |
| TypeError serializing datetime | Tried `json.dumps()` on an object with a datetime field | Converted datetime to `.isoformat()` string first |
| Mixed up dump/dumps | Used `json.dump()` when writing to a string variable | Remembered: 's' = string version |

---

## Optimization / good habit I picked up

Iterating directly over a file object (`for line in f:`) instead of
calling `.readlines()` first when processing large files. `.readlines()`
loads everything into memory as a list immediately; direct iteration reads
lazily, line by line. Doesn't matter for my small test files, but it's a
habit I want established before I work with anything genuinely large.

---

## Lessons learned after this module

- Always use `with` for file operations — no exceptions
- Pause and think before choosing 'w' vs 'a' — this mistake cost me data once
- Use standard library modules (csv, json) instead of manual string parsing
- Cast numeric values explicitly when reading from CSV
- Specify encoding explicitly to avoid platform-dependent surprises

Next up: Exception Handling — I've been informally handling a few errors
already (FileNotFoundError, JSONDecodeError) but want to actually
understand try/except/finally properly instead of copy-pasting patterns.
