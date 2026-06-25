# 📒 Module 11 — Database Programming: My Notes

**Started:** Jul 2, 2024
**Finished:** Jul 19, 2024
**Time spent:** ~19 hours

---

## What I learned this module

This is the module where things started feeling "real" — applications
that persist meaningful structured data instead of flat CSV/JSON files I
manually re-parse every time. SQLite being built into Python's standard
library (no server install needed) made this a much gentler entry point
than I expected; I'd assumed databases would require setting up MySQL or
PostgreSQL just to learn the basics.

### Key realizations

1. **Parameterized queries are NOT optional, they're the whole point of
   safety.** I deliberately built a vulnerable query using an f-string
   and then ran `"Pavan' OR '1'='1"` through it to SEE SQL injection work
   on my own test database. Watching the malicious input return ALL rows
   instead of zero made the danger concrete in a way that just reading
   "SQL injection is bad" never would have. Now `?` placeholders are
   completely automatic for me — never f-strings, never `.format()`,
   never `%` formatting for SQL with variable data.

2. **Foreign keys are NOT enforced by default in SQLite.** Genuinely
   surprised me — I assumed declaring `FOREIGN KEY (student_id)
   REFERENCES students(student_id)` would automatically prevent invalid
   references. It doesn't, unless you explicitly run
   `PRAGMA foreign_keys = ON` for each connection. Without it, SQLite
   will silently let you insert orphaned rows referencing IDs that don't
   exist.

3. **INNER JOIN vs LEFT JOIN — needed to run both side by side to
   actually understand the difference**, not just read the definitions.
   INNER JOIN only returns rows that match in BOTH tables; LEFT JOIN
   returns ALL rows from the left table regardless of match, filling in
   NULL where there's no match. I added a deliberately unmatched employee
   (no department) specifically to see this difference in the result
   counts.

4. **WHERE filters rows, HAVING filters GROUPS.** Tried using WHERE with
   an aggregate function (`WHERE AVG(salary) > 50000`) directly and got
   an error — that's specifically what pushed me to learn WHY HAVING
   exists as a separate clause instead of just memorizing "use HAVING
   after GROUP BY" as an arbitrary rule.

5. **`executemany()` is much cleaner than looping individual INSERT
   statements.** Earlier draft of the Database setup had a manual for
   loop calling `cursor.execute()` once per record. Replaced with
   `executemany()` once I found it — same result, less code, and I'd
   guess better performance for genuinely large batches (haven't
   benchmarked this myself yet, want to test later).

6. **Transactions (commit/rollback) give real safety for multi-step
   operations.** Simulated a failure mid-transaction (an intentional
   ValueError after an UPDATE but before commit) and confirmed
   `rollback()` actually undid the change. This is directly relevant to
   the Bank Management project — a money transfer involves TWO updates
   (debit one account, credit another), and if the second update fails,
   I need the first to roll back too, or money disappears into nowhere.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| Used f-string to build SQL query | Worked initially, but vulnerable to injection | Switched to parameterized ? placeholders |
| Foreign key violation silently allowed | Inserted orphaned row referencing nonexistent student_id | Added PRAGMA foreign_keys = ON |
| Confused INNER JOIN and LEFT JOIN results | Expected same row count from both, got different counts | Ran both side-by-side with a deliberately unmatched test row |
| WHERE with aggregate function failed | Tried WHERE AVG(salary) > 50000, got an error | Learned to use HAVING instead, after GROUP BY |
| Forgot connection.commit() | Changes appeared to "disappear" on reconnect | Learned commit() is required to persist writes, not automatic |
| Didn't close connection | Got "database is locked" error on a second script run | Always close connections (or use a context-manager wrapper) |

---

## Optimization attempt: bulk insert performance

Started with a manual loop calling `execute()` once per row for inserting
test data (50+ rows for benchmark testing). Switched to `executemany()`
and the code got noticeably shorter and easier to read, though I haven't
done a rigorous timing benchmark yet to quantify the actual performance
difference — that's something I want to circle back to once I'm
comfortable with the `timeit` module.

---

## Lessons learned after this module

- ALWAYS use parameterized queries (`?` placeholders) — no exceptions,
  ever, regardless of how "trusted" the input source seems
- Enable foreign key constraints explicitly with PRAGMA — don't assume
  they're on by default
- Test INNER JOIN vs LEFT JOIN with deliberately unmatched data to see
  real behavior differences, not just memorized definitions
- WHERE filters rows before grouping; HAVING filters after aggregation
- Use transactions (commit/rollback) for any multi-step operation where
  partial completion would leave data in a broken state
- Always close database connections when done

Next up: APIs and Automation — REST APIs, web scraping, email and PDF
automation. This is the module I'm most excited about because it
connects directly to things I want to build for IoT/embedded projects
later (calling APIs from sensor data pipelines, etc.)
