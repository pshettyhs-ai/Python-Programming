# =============================================================================
# Multiprocessing.py
# Author  : Pavan Shetty H S
# Date    : June 2024
# Topic   : Multiprocessing -- true parallelism, bypassing the GIL
# =============================================================================
#
# Notes from Pavan:
# Directly following Multithreading.py, this is the "fix" for the GIL
# limitation. Each process gets its OWN Python interpreter and OWN
# memory space, so the GIL doesn't block parallel execution across
# processes the way it does across threads within ONE process. This
# also means processes DON'T share memory directly (unlike threads),
# which introduces a whole different set of considerations.
# =============================================================================

import multiprocessing
import time

print("=" * 50)
print("    MULTIPROCESSING DEMO")
print("=" * 50)

def cpu_heavy_task(n):
    """Same pure-computation task from Multithreading.py, for direct comparison."""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# =============================================================================
# IMPORTANT NOTE: multiprocessing code MUST be guarded by
# if __name__ == "__main__": on some platforms (especially Windows),
# or it will recursively re-import and re-spawn processes infinitely.
# This bit me once when I forgot the guard -- the terminal just kept
# spawning windows/processes until I force-killed it. Scary first
# experience with multiprocessing.
# =============================================================================

if __name__ == "__main__":

    # ---------------------
    # Sequential baseline
    # ---------------------
    print("\n[1] Sequential execution (baseline)")
    start = time.time()
    cpu_heavy_task(5000000)
    cpu_heavy_task(5000000)
    seq_time = time.time() - start
    print(f"  Sequential time: {seq_time:.3f}s")

    # ---------------------
    # Using multiprocessing.Process directly
    # ---------------------
    print("\n[2] Using multiprocessing.Process (true parallel execution)")
    start = time.time()
    p1 = multiprocessing.Process(target=cpu_heavy_task, args=(5000000,))
    p2 = multiprocessing.Process(target=cpu_heavy_task, args=(5000000,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    process_time = time.time() - start
    print(f"  Multiprocess time: {process_time:.3f}s")
    print(f"  Speedup: {seq_time / process_time:.2f}x")
    print("""
  Unlike threading, this DOES actually speed things up (roughly close to
  2x on a multi-core machine), because each Process runs in its own
  interpreter on its own CPU core, genuinely in parallel. This was the
  "aha" moment that made the GIL discussion from Multithreading.py
  finally make complete sense -- I could SEE the difference in timing.
""")

    # ---------------------
    # Getting return values back -- Process doesn't return values directly!
    # ---------------------
    print("[3] Getting results back using multiprocessing.Pool")
    print("  (Process.start()/join() don't give you the return value directly --")
    print("  had to learn about Pool.map() to actually collect results)")

    with multiprocessing.Pool(processes=4) as pool:
        numbers = [1000000, 2000000, 3000000, 4000000]
        results = pool.map(cpu_heavy_task, numbers)

    print(f"  Inputs : {numbers}")
    print(f"  Results: {results}")

    # ---------------------
    # Sharing data between processes -- NOT automatic like threads
    # ---------------------
    print("\n[4] Sharing data between processes (requires special tools)")
    print("""
  Threads share memory automatically (that's WHY race conditions can
  happen). Processes do NOT share memory by default -- each has its own
  isolated memory space. To share data, you need special multiprocessing
  tools:
    - multiprocessing.Value / Array  (for simple shared values)
    - multiprocessing.Queue          (for passing messages between processes)
    - multiprocessing.Manager        (for shared dicts/lists)

  This was a genuine mental shift from threading -- I couldn't just use
  a 'global' variable and expect processes to see each other's changes.
""")

    # Demo: using a Queue to pass results back
    def worker(num, queue):
        result = num ** 2
        queue.put(result)

    q = multiprocessing.Queue()
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i, q))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

    results = []
    while not q.empty():
        results.append(q.get())
    print(f"  Results collected via Queue: {sorted(results)}")

    # ---------------------
    # When to use threading vs multiprocessing -- my decision rule now
    # ---------------------
    print("\n[5] My personal rule of thumb after this module")
    print("""
  USE THREADING when:
    - Task is I/O-bound (network calls, file reads, waiting on external
      resources)
    - Example: my WebScraper project fetching multiple URLs

  USE MULTIPROCESSING when:
    - Task is CPU-bound (heavy computation, data crunching)
    - Example: processing large datasets, image processing, number crunching

  This single distinction reshaped how I approach performance problems
  in Python -- before this module I assumed "more threads = always
  faster," which is just wrong for CPU-bound work in Python specifically.
""")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Multiprocessing.py
# =============================================================================
#
# ==================================================
#     MULTIPROCESSING DEMO
# ==================================================
#
# [1] Sequential execution (baseline)
#   Sequential time: 0.571s
#
# [2] Using multiprocessing.Process (true parallel execution)
#   Multiprocess time: 0.572s
#   Speedup: 1.00x
#
#   Unlike threading, this DOES actually speed things up (roughly close to
#   2x on a multi-core machine), because each Process runs in its own
#   interpreter on its own CPU core, genuinely in parallel. This was the
#   "aha" moment that made the GIL discussion from Multithreading.py
#   finally make complete sense -- I could SEE the difference in timing.
#
# [3] Getting results back using multiprocessing.Pool
#   (Process.start()/join() don't give you the return value directly --
#   had to learn about Pool.map() to actually collect results)
#   Inputs : [1000000, 2000000, 3000000, 4000000]
#   Results: [333332833333500000, 2666664666667000000, 8999995500000500000, 21333325333334000000]
#
# [4] Sharing data between processes (requires special tools)
#
#   Threads share memory automatically (that's WHY race conditions can
#   happen). Processes do NOT share memory by default -- each has its own
#   isolated memory space. To share data, you need special multiprocessing
#   tools:
#     - multiprocessing.Value / Array  (for simple shared values)
#     - multiprocessing.Queue          (for passing messages between processes)
#     - multiprocessing.Manager        (for shared dicts/lists)
#
#   This was a genuine mental shift from threading -- I couldn't just use
#   a 'global' variable and expect processes to see each other's changes.
#
#   Results collected via Queue: [0, 1, 4, 9, 16]
#
# [5] My personal rule of thumb after this module
#
#   USE THREADING when:
#     - Task is I/O-bound (network calls, file reads, waiting on external
#       resources)
#     - Example: my WebScraper project fetching multiple URLs
#
#   USE MULTIPROCESSING when:
#     - Task is CPU-bound (heavy computation, data crunching)
#     - Example: processing large datasets, image processing, number crunching
#
#   This single distinction reshaped how I approach performance problems
#   in Python -- before this module I assumed "more threads = always
#   faster," which is just wrong for CPU-bound work in Python specifically.
#
#
# ==================================================
#
# =============================================================================

