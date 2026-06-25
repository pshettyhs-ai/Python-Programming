# 🎯 DSA Interview Questions — My Preparation Notes

**Compiled by:** Pavan Shetty H S
**Last updated:** October 2024

---

## Context

These questions are organized by the data structures I implemented in
Module 13. I'm including time/space complexity analysis for each since
that's almost always the actual follow-up question in real interviews,
not just "can you solve it."

---

## Section 1: Arrays & Strings

### Q1. What is the time complexity of accessing an element in a Python list by index?

O(1) — Python lists are implemented as dynamic arrays internally, so
indexing is direct memory address calculation, not a traversal.

### Q2. 🔴 What's the time complexity of `list.append()`? What about `list.insert(0, x)`?

I initially assumed BOTH were O(1) since they're both "adding one
element." Wrong for `insert(0, x)`. `append()` is amortized O(1) (occasionally
O(n) when the underlying array needs to resize, but averaged out over
many calls it's O(1)). `insert(0, x)` is O(n) because EVERY existing
element has to shift one position to make room at the front. This is
exactly the lesson from Queue.py in Module 13 — `list.pop(0)` has the
same O(n) shifting problem, which is why I switched to `collections.deque`
for queue operations.

### Q3. How would you find the first non-repeating character in a string?

```python
def first_non_repeating(s):
    from collections import Counter
    counts = Counter(s)
    for char in s:
        if counts[char] == 1:
            return char
    return None
```

O(n) time using a Counter for frequency lookup, O(n) space. My first
attempt used nested loops (check each character against all others) —
O(n²). Realized I could trade space for time using a hash map (Counter),
a pattern I now recognize as a recurring interview theme.

---

## Section 2: Linked Lists

### Q4. How do you detect a cycle in a linked list?

Floyd's Cycle Detection (the "tortoise and hare" algorithm) — two
pointers, one moving 1 step at a time, one moving 2 steps at a time. If
there's a cycle, the fast pointer eventually laps the slow pointer and
they meet. If no cycle, the fast pointer reaches the end (`None`) first.
O(n) time, O(1) space — no extra data structure needed, which is the
elegant part.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

### Q5. How do you reverse a linked list?

Implemented this exact thing in LinkedList.py (Module 13) using the
prev/current/next pointer technique. O(n) time, O(1) space for the
iterative version. A recursive version is also possible but uses O(n)
space due to the call stack.

### Q6. 🔴 What's the time complexity of finding the middle of a linked list?

Got this wrong initially — assumed you'd need to count the length first
(one pass), then traverse again to the midpoint (second pass), making it
"two passes but still O(n)." That's correct but not OPTIMAL. The
slow/fast pointer technique (same family as cycle detection) finds the
middle in a SINGLE pass — when fast reaches the end, slow is at the
middle. Still O(n) time complexity-wise either way, but the single-pass
version is the answer interviewers are usually looking for.

---

## Section 3: Stacks & Queues

### Q7. How would you implement a queue using two stacks?

```python
class QueueUsingStacks:
    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def enqueue(self, item):
        self.stack_in.append(item)

    def dequeue(self):
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        return self.stack_out.pop()
```

This was a genuinely interesting one to work through. Push everything
onto `stack_in`. When you need to dequeue, if `stack_out` is empty, dump
ALL of `stack_in` into `stack_out` (which reverses the order, turning
LIFO into FIFO). Amortized O(1) per operation — each element only gets
moved between stacks once, total.

### Q8. How do you check if an expression has balanced parentheses?

Implemented in Stack.py (Module 13). Push opening brackets, pop and
match on closing brackets, the expression is balanced only if the stack
ends EMPTY and every closing bracket matched the most recent unmatched
opener.

---

## Section 4: Trees

### Q9. 🔴 What's the time complexity of search/insert/delete in a Binary Search Tree?

I answered "O(log n)" confidently and was then asked "always?" which I
hadn't considered. The honest answer: O(log n) ONLY if the tree is
reasonably balanced. In the WORST case (degenerate tree, e.g. built by
inserting already-sorted data), it degrades to O(n) — essentially
becoming a linked list. I actually proved this to myself in Tree.py by
comparing the HEIGHT of a balanced-insertion-order tree against a
sorted-insertion-order tree with the same node count.

### Q10. What's the difference between BFS and DFS traversal of a tree?

BFS (level-order) visits nodes level by level using a QUEUE. DFS
(pre/in/post-order) goes deep down one branch before backtracking,
typically using recursion (or an explicit stack). Implemented all of
these — inorder traversal of a BST specifically produces SORTED output,
which was the realization that made BSTs click for me conceptually.

### Q11. How do you find the height of a binary tree?

```python
def height(node):
    if node is None:
        return -1   # or 0, depending on convention -- I use -1 for empty tree
    return 1 + max(height(node.left), height(node.right))
```

O(n) time (must visit every node), O(h) space for the recursion stack,
where h is the tree's height.

---

## Section 5: Graphs

### Q12. When would you use BFS vs DFS?

BFS: shortest path in an UNWEIGHTED graph, level-order processing,
"closest" anything. Uses a queue. DFS: exploring all possible paths,
cycle detection, topological sorting, maze-solving. Uses a stack or
recursion. I connected this directly to Stack.py/Queue.py in my own
notes — BFS is basically "Queue.py's traversal cousin," DFS is "Stack.py's
traversal cousin."

### Q13. 🔴 Does BFS find the shortest path in a WEIGHTED graph?

Initially assumed yes, since BFS finds shortest path in general. Wrong —
BFS only guarantees shortest path in UNWEIGHTED graphs (or graphs where
all edges have equal weight). For weighted graphs, you need Dijkstra's
algorithm (or Bellman-Ford if negative weights are possible). I haven't
implemented Dijkstra's from scratch yet — noting this as a clear gap to
close before final interview prep.

---

## Section 6: Sorting & Searching

### Q14. Compare the time complexities of common sorting algorithms.

| Algorithm | Best | Average | Worst | Space | Stable? |
|---|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |

Implemented and timing-benchmarked all of these in Module 13 — seeing
the gap between O(n²) and O(n log n) widen visibly as input size grew
made this table feel earned rather than memorized.

### Q15. 🔴 Why is Quick Sort's worst case O(n²)?

Got partial credit on this one in a mock interview — explained the
WHAT but fumbled the WHY initially. If the pivot choice is consistently
bad (e.g., always picking the smallest or largest remaining element,
which happens with naive first-element pivot selection on already-sorted
data), each partition only removes ONE element instead of roughly
HALVING the remaining data. This turns what should be log(n) levels of
recursion into n levels, each doing O(n) partitioning work, giving O(n²)
total. Verified this exact scenario experimentally in MergeSort.py by
timing a bad-pivot version against a middle-pivot version on sorted input.

### Q16. Why does binary search require sorted data?

Because the algorithm's core decision (go left or go right) relies on
the assumption that everything to the left of the midpoint is smaller
and everything to the right is larger. On unsorted data this assumption
is false, so the algorithm can't reliably eliminate half the search
space each step — it may give a wrong answer (false negative) without
any error or crash, which I actually experienced firsthand and documented
in BinarySearch.py.

---

## My honest gaps to close before real interviews

- Dijkstra's algorithm for weighted shortest path (haven't implemented)
- Dynamic programming beyond basic memoization (Fibonacci-level only so far)
- Self-balancing trees (AVL/Red-Black) — understand WHY they're needed,
  haven't implemented one
- Heap / priority queue implementation from scratch

Tracking these honestly here instead of pretending I've covered
everything — better to know my own gaps than to discover them live in
an interview.
