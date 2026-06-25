# =============================================================================
# Queue.py
# Author  : Pavan Shetty H S
# Date    : September 2024
# Topic   : Queue -- FIFO data structure
# =============================================================================
#
# Notes from Pavan:
# Made a mistake initially using a plain Python list for the queue with
# list.pop(0) to dequeue. Worked correctly but I later learned pop(0) is
# O(n) because EVERY remaining element has to shift left by one index.
# Switched to collections.deque, which is implemented as a doubly linked
# list internally and gives O(1) for both ends. Real lesson here: "it
# works correctly" and "it performs well" are different questions.
# =============================================================================

from collections import deque

print("=" * 50)
print("    QUEUE DEMO")
print("=" * 50)

class Queue:
    """FIFO -- First In, First Out. Think of a line at a billing counter."""
    def __init__(self):
        self._items = deque()   # using deque, NOT list, for O(1) operations

    def enqueue(self, item):
        self._items.append(item)        # add to the RIGHT end

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()     # remove from the LEFT end -- O(1) with deque!

    def front(self):
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __str__(self):
        return f"Queue({list(self._items)})"

# ---------------------
# Basic usage
# ---------------------
print("\n[1] Basic queue operations")
q = Queue()
q.enqueue("Customer A")
q.enqueue("Customer B")
q.enqueue("Customer C")
print(f"  Queue: {q}")
print(f"  front(): {q.front()}")
print(f"  dequeue(): {q.dequeue()}")
print(f"  After dequeue: {q}")

# ---------------------
# The performance lesson: list.pop(0) vs deque.popleft()
# ---------------------
print("\n[2] Why I switched from list to deque -- the performance lesson")
import time

# Bad approach: using a list
def bad_queue_test(n):
    items = list(range(n))
    while items:
        items.pop(0)   # O(n) every single time -- shifts ALL remaining elements

# Good approach: using deque
def good_queue_test(n):
    items = deque(range(n))
    while items:
        items.popleft()   # O(1) every time

n = 20000
start = time.time()
bad_queue_test(n)
bad_time = time.time() - start

start = time.time()
good_queue_test(n)
good_time = time.time() - start

print(f"  list.pop(0) for {n} items: {bad_time:.4f}s")
print(f"  deque.popleft() for {n} items: {good_time:.4f}s")
print(f"  deque was {bad_time/good_time:.1f}x faster")
print("""
  This is a genuinely measurable difference, not a theoretical one. My
  first draft of the Attendance Management project used a plain list as
  a processing queue and felt sluggish with larger datasets -- switching
  to deque was a direct, visible fix.
""")

# ---------------------
# Practical use case: Simulating a print queue / task scheduler
# ---------------------
print("[3] Practical: Simple task scheduler simulation")

task_queue = Queue()
tasks = ["Print Document 1", "Print Document 2", "Print Document 3"]
for t in tasks:
    task_queue.enqueue(t)

print("  Processing tasks in order received (FIFO):")
while not task_queue.is_empty():
    current_task = task_queue.dequeue()
    print(f"    Processing: {current_task}")

# ---------------------
# Circular Queue -- a variant I read about for fixed-size buffers
# ---------------------
print("\n[4] Circular Queue (fixed-size, useful for embedded buffer scenarios)")

class CircularQueue:
    """Fixed-size queue that wraps around. Genuinely relevant to my
    embedded systems interest -- this is basically how a hardware ring
    buffer works for UART/sensor data buffering on microcontrollers."""
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.front_idx = 0
        self.rear_idx = -1
        self.count = 0

    def enqueue(self, item):
        if self.count == self.capacity:
            print(f"  Queue full! Cannot add {item}")
            return False
        self.rear_idx = (self.rear_idx + 1) % self.capacity
        self.queue[self.rear_idx] = item
        self.count += 1
        return True

    def dequeue(self):
        if self.count == 0:
            print("  Queue is empty!")
            return None
        item = self.queue[self.front_idx]
        self.front_idx = (self.front_idx + 1) % self.capacity
        self.count -= 1
        return item

cq = CircularQueue(3)
cq.enqueue("A")
cq.enqueue("B")
cq.enqueue("C")
cq.enqueue("D")   # should fail, queue is full
print(f"  Dequeued: {cq.dequeue()}")
cq.enqueue("D")   # now succeeds, there's room after dequeue
print(f"  Dequeued: {cq.dequeue()}")
print(f"  Dequeued: {cq.dequeue()}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Queue.py
# =============================================================================
#
# ==================================================
#     QUEUE DEMO
# ==================================================
#
# [1] Basic queue operations
#   Queue: Queue(['Customer A', 'Customer B', 'Customer C'])
#   front(): Customer A
#   dequeue(): Customer A
#   After dequeue: Queue(['Customer B', 'Customer C'])
#
# [2] Why I switched from list to deque -- the performance lesson
#   list.pop(0) for 20000 items: 0.0340s
#   deque.popleft() for 20000 items: 0.0006s
#   deque was 52.6x faster
#
#   This is a genuinely measurable difference, not a theoretical one. My
#   first draft of the Attendance Management project used a plain list as
#   a processing queue and felt sluggish with larger datasets -- switching
#   to deque was a direct, visible fix.
#
# [3] Practical: Simple task scheduler simulation
#   Processing tasks in order received (FIFO):
#     Processing: Print Document 1
#     Processing: Print Document 2
#     Processing: Print Document 3
#
# [4] Circular Queue (fixed-size, useful for embedded buffer scenarios)
#   Queue full! Cannot add D
#   Dequeued: A
#   Dequeued: B
#   Dequeued: C
#
# ==================================================
#
# =============================================================================

