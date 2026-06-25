# 📒 Module 10 — Advanced Python: My Notes

**Started:** Jun 3, 2024
**Finished:** Jun 29, 2024
**Time spent:** ~30 hours

---

## What I learned this module

This module is where Python stopped feeling like "a simpler version of
what I already know" and started introducing genuinely new mental models.
Decorators, generators, and the GIL all required me to slow down
significantly compared to earlier modules.

### Decorators

Broke my brain for about 3 days. The `@decorator` syntax looked like pure
magic until I manually wrote out what it expands to —
`function = decorator(function)`. Once I saw it's literally just "pass
your function into another function, get something back, replace the
original name with that," the `@` syntax stopped feeling mysterious.

Forgot `functools.wraps` in an early attempt and got genuinely confused
debugging — stack traces showed `wrapper` everywhere instead of my actual
function names, which made tracing bugs through decorated functions much
harder than it should have been. Now `@functools.wraps(func)` is
automatic muscle memory whenever I write a decorator.

Decorator FACTORIES (`@retry(max_attempts=3)`) took an extra day to
understand — there's an additional layer of function nesting because
`@retry(3)` first CALLS `retry(3)`, which returns the actual decorator,
which THEN gets applied to the function. Three layers of functions
instead of two.

### Generators

This is the concept that, once understood, made me go back and mentally
re-evaluate code I'd already written. The realization that `yield` PAUSES
a function and remembers exactly where execution left off — without
needing to manually track state in a class — felt like discovering a
shortcut I didn't know existed.

The memory comparison demo (list of 100,000 ints vs equivalent generator)
made the practical value concrete instead of abstract. I'm now
consciously choosing generator expressions over list comprehensions when
I don't need the whole collection materialized at once, especially for
file processing.

Hit `StopIteration` confusion once — tried reusing an exhausted generator
expecting it to "restart" and got nothing. Learned generators are
single-use; need a fresh one each time.

### Iterators

Honestly felt a bit redundant after generators at first, since generators
ARE iterators with less boilerplate. But going through `__iter__`/`__next__`
manually helped me understand what a `for` loop is ACTUALLY doing under
the hood — repeatedly calling `next()` until it catches `StopIteration`
internally. That demystified a piece of Python I'd been using since week
one without ever questioning it.

Hit a real bug building a reporting feature later: looped over the same
custom iterator object twice (once for a total, once for details) and the
second loop did nothing because the iterator was already exhausted. Fixed
by separating "iterable" (returns a FRESH iterator each time) from
"iterator" (the actual stateful cursor) — a distinction I hadn't
appreciated until this exact bug forced me to.

### Context Managers

I'd been USING `with open(...) as f:` since Module 7 without
understanding the mechanism. Building my own `FileManager` class with
`__enter__`/`__exit__` finally exposed what's happening: `__enter__` runs
at the start, `__exit__` runs at the end NO MATTER WHAT — even when an
exception interrupts the block. Confirmed this experimentally by raising
an exception deliberately inside a `with` block and watching `__exit__`
still execute.

The `@contextmanager` decorator + generator pattern felt much more
natural to write than the full class version, once I already understood
generators from earlier in this module. Code before `yield` = setup, code
after `yield` = teardown.

### Multithreading & the GIL

This is where my embedded systems background (RTOS task concepts from
STM32 work) helped AND created a wrong assumption simultaneously. I
expected Python threads to behave like genuinely parallel hardware
execution. They don't, because of the GIL (Global Interpreter Lock) —
only one thread executes Python bytecode at any instant, regardless of
core count.

Ran an actual timing comparison (CPU-bound task, sequential vs threaded)
specifically to SEE this for myself rather than just take the explanation
on faith. The threaded version was NOT meaningfully faster — sometimes
slightly slower from thread-switching overhead. This was the single
biggest "wait, really?" moment of the whole module.

Deliberately caused a race condition (unsynchronized counter increment
across 5 threads) to understand WHY locks matter, then fixed it with
`threading.Lock()`. Seeing the WRONG count first, then the correct count
after adding a lock, made the concept stick far better than reading about
it would have.

### Multiprocessing

Directly answers the GIL limitation — each process gets its own
interpreter and memory space, so CPU-bound work genuinely parallelizes
across processes. Ran the same CPU-bound timing comparison as threading
and this time SAW close to a 2x speedup on two processes. That contrast
(threading: no speedup, multiprocessing: real speedup) is what made the
whole "threading for I/O, multiprocessing for CPU" rule finally feel
earned rather than just memorized advice.

**Scary moment:** forgot the `if __name__ == "__main__":` guard while
experimenting with `multiprocessing.Process` early on. On my system it
started recursively re-importing and spawning processes — had to
force-close the terminal. Now I treat that guard as completely
non-negotiable for any multiprocessing code.

Learned processes do NOT share memory like threads do — needed
`multiprocessing.Queue` to actually collect results back from worker
processes, since `Process.start()`/`.join()` don't return values directly
the way a normal function call would.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| Lost function identity in decorator | __name__ showed 'wrapper' everywhere in stack traces | Added @functools.wraps(func) |
| Confused decorator factory nesting | @retry(3) syntax didn't make sense at first | Traced through the 3 layers of functions manually |
| Reused an exhausted generator | Got nothing on second iteration | Created a fresh generator instance for re-iteration |
| Reused a custom iterator twice | Second loop did nothing (already exhausted) | Separated Iterable (__iter__ returns fresh iterator) from Iterator |
| Expected threading speedup for CPU work | No improvement, sometimes slightly slower | Learned about the GIL; switched to multiprocessing for CPU-bound work |
| Race condition on shared counter | Final count was wrong, inconsistent across runs | Used threading.Lock() to synchronize access |
| Forgot __name__ == "__main__" guard | multiprocessing recursively spawned processes uncontrollably | Always guard multiprocessing entry points |
| Tried sharing data between processes like threads | Changes in one process invisible to another | Used multiprocessing.Queue to pass data explicitly |

---

## Biggest mental shift this module

Before this module, my instinct was "more concurrency = always faster."
After actually measuring timing differences myself instead of trusting
explanations blindly, I now think in terms of: is this task waiting on
something external (I/O-bound → threading helps) or is this task pure
computation (CPU-bound → need multiprocessing, or just better algorithms
first). This distinction will directly shape decisions in the Web Scraper
project (threading, since it's mostly waiting on network requests).

---

## Lessons learned after this module

- Manually expand `@decorator` syntax mentally when confused — it's just
  function substitution
- Always use `functools.wraps` in decorators
- Generators trade "build everything upfront" for "compute on demand" —
  huge memory wins for large/infinite sequences
- A `for` loop is just `iter()` + repeated `next()` + catching `StopIteration`
- Context managers guarantee cleanup runs even when exceptions occur
- The GIL means Python threading doesn't help CPU-bound work — measure,
  don't assume
- Multiprocessing gives true parallelism but costs you shared memory —
  use Queue/Manager/Value explicitly when processes need to communicate
- ALWAYS guard multiprocessing code with `if __name__ == "__main__":`

Next up: Database Programming with SQLite — finally moving past flat
files (CSV/JSON) into something closer to how real applications persist
data.
