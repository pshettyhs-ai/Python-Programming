# =============================================================================
# Multithreading.py
# Author  : Pavan Shetty H S
# Date    : June 2024
# Topic   : Multithreading -- threading module, GIL
# =============================================================================
#
# Notes from Pavan:
# This was the module where my embedded systems background actually
# helped instead of confusing me -- I already understood threads
# conceptually from RTOS concepts (FreeRTOS tasks on STM32). What threw
# me off completely was the GIL (Global Interpreter Lock). Coming in, I
# expected Python threads to give true parallel CPU execution like
# separate hardware cores running independently. They DON'T, because of
# the GIL, and that single fact reshaped how I think about when to use
# threading at all in Python.
# =============================================================================

import threading
import time
import requests

print("=" * 50)
print("    MULTITHREADING DEMO")
print("=" * 50)

# ---------------------
# Basic thread creation
# ---------------------
print("\n[1] Creating and starting threads")

def print_numbers():
    for i in range(5):
        print(f"  Number: {i}")
        time.sleep(0.1)

def print_letters():
    for letter in "ABCDE":
        print(f"  Letter: {letter}")
        time.sleep(0.1)

t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)

t1.start()
t2.start()
t1.join()   # wait for t1 to finish before continuing
t2.join()   # wait for t2 to finish before continuing
print("  Both threads completed (notice output is INTERLEAVED, not sequential)")

# ---------------------
# The GIL -- why CPU-bound tasks DON'T speed up with threading
# ---------------------
print("\n[2] The GIL problem -- CPU-bound work doesn't parallelize")

def cpu_heavy_task(n):
    """Pure computation -- no I/O waiting involved."""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# Single-threaded timing
start = time.time()
cpu_heavy_task(5000000)
cpu_heavy_task(5000000)
single_thread_time = time.time() - start
print(f"  Sequential (no threads): {single_thread_time:.3f}s")

# Multi-threaded timing -- SHOULD be faster if threads were truly parallel
start = time.time()
t1 = threading.Thread(target=cpu_heavy_task, args=(5000000,))
t2 = threading.Thread(target=cpu_heavy_task, args=(5000000,))
t1.start()
t2.start()
t1.join()
t2.join()
multi_thread_time = time.time() - start
print(f"  Threaded (2 threads)   : {multi_thread_time:.3f}s")
print("""
  My genuine surprise here: the threaded version is NOT meaningfully
  faster, sometimes even slightly SLOWER due to thread-switching overhead.
  This is the GIL (Global Interpreter Lock) -- only ONE thread executes
  Python bytecode at a time, ever, regardless of how many CPU cores exist.
  Threading in Python does NOT give true parallelism for CPU-bound work.
  This single realization is why Module 10 also covers Multiprocessing --
  THAT'S the tool for CPU-bound parallelism, not threading.
""")

# ---------------------
# Where threading actually shines: I/O-bound tasks
# ---------------------
print("[3] Threading DOES help for I/O-bound tasks (waiting on network/disk)")

def fetch_url(url):
    """I/O-bound -- most of the time here is spent WAITING for a network
    response, not computing. This is where the GIL doesn't matter, because
    while one thread waits on I/O, it releases the GIL and lets another
    thread run."""
    try:
        response = requests.get(url, timeout=5)
        print(f"  Fetched {url} -- status {response.status_code}")
    except Exception as e:
        print(f"  Failed to fetch {url}: {e}")

urls = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/1",
]

print("  (Network demo -- skipped actual calls in this offline note,")
print("  but the real pattern I used in WebScraping.py looks like this:)")
print("""
  threads = []
  for url in urls:
      t = threading.Thread(target=fetch_url, args=(url,))
      threads.append(t)
      t.start()
  for t in threads:
      t.join()

  3 requests with 1-second delay each:
    Sequential: ~3 seconds (1+1+1)
    Threaded  : ~1 second (all waiting simultaneously)

  This is a REAL speedup, unlike the CPU-bound example above, because
  the bottleneck is NETWORK WAIT TIME, not CPU computation.
""")

# ---------------------
# Race conditions -- the bug I caused on purpose to understand locks
# ---------------------
print("[4] Race conditions and Lock")

counter = 0

def increment_unsafe():
    global counter
    for _ in range(100000):
        counter += 1   # NOT atomic! Read-modify-write can be interrupted mid-operation

threads = [threading.Thread(target=increment_unsafe) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"  Expected: 500000, Got: {counter}")
print("  ^ Often WRONG due to race conditions -- multiple threads read/write")
print("  'counter' simultaneously and steps get lost between threads.")

# Fixed version using Lock
counter_safe = 0
lock = threading.Lock()

def increment_safe():
    global counter_safe
    for _ in range(100000):
        with lock:   # only ONE thread can hold this lock at a time
            counter_safe += 1

threads = [threading.Thread(target=increment_safe) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"  With Lock - Expected: 500000, Got: {counter_safe}")
print("  Using threading.Lock() as a 'with' context manager fixed it --")
print("  guarantees only one thread modifies counter_safe at a time.")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Multithreading.py
# =============================================================================
#
# ==================================================
#     MULTITHREADING DEMO
# ==================================================
#
# [1] Creating and starting threads
#   Number: 0
#   Letter: A
#   Number: 1
#   Letter: B
#   Letter: C
#   Number: 2
#   Letter: D
#   Number: 3
#   Number: 4
#   Letter: E
#   Both threads completed (notice output is INTERLEAVED, not sequential)
#
# [2] The GIL problem -- CPU-bound work doesn't parallelize
#   Sequential (no threads): 0.599s
#   Threaded (2 threads)   : 0.580s
#
#   My genuine surprise here: the threaded version is NOT meaningfully
#   faster, sometimes even slightly SLOWER due to thread-switching overhead.
#   This is the GIL (Global Interpreter Lock) -- only ONE thread executes
#   Python bytecode at a time, ever, regardless of how many CPU cores exist.
#   Threading in Python does NOT give true parallelism for CPU-bound work.
#   This single realization is why Module 10 also covers Multiprocessing --
#   THAT'S the tool for CPU-bound parallelism, not threading.
#
# [3] Threading DOES help for I/O-bound tasks (waiting on network/disk)
#   (Network demo -- skipped actual calls in this offline note,
#   but the real pattern I used in WebScraping.py looks like this:)
#
#   threads = []
#   for url in urls:
#       t = threading.Thread(target=fetch_url, args=(url,))
#       threads.append(t)
#       t.start()
#   for t in threads:
#       t.join()
#
#   3 requests with 1-second delay each:
#     Sequential: ~3 seconds (1+1+1)
#     Threaded  : ~1 second (all waiting simultaneously)
#
#   This is a REAL speedup, unlike the CPU-bound example above, because
#   the bottleneck is NETWORK WAIT TIME, not CPU computation.
#
# [4] Race conditions and Lock
#   Expected: 500000, Got: 500000
#   ^ Often WRONG due to race conditions -- multiple threads read/write
#   'counter' simultaneously and steps get lost between threads.
#   With Lock - Expected: 500000, Got: 500000
#   Using threading.Lock() as a 'with' context manager fixed it --
#   guarantees only one thread modifies counter_safe at a time.
#
# ==================================================
#
# =============================================================================

