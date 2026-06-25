# 📒 Module 13 — Data Structures & Algorithms: My Notes

**Started:** Sep 2, 2024
**Finished:** Sep 28, 2024
**Time spent:** ~34 hours

---

## What I learned this module

Up to this point I'd been using Python's built-in `list`, `dict`, `set`
for basically everything, which is genuinely fine for real applications
(Python's built-ins are heavily optimized C implementations under the
hood). This module was specifically about implementing the classics
FROM SCRATCH to understand what's actually happening internally, since
this is also core interview preparation material.

### Linked List

Already understood the concept from a C data structures course (pointers
and structs), so this was more about translating the same idea into
Python's object model. Genuinely easier in Python — no manual
malloc/free, garbage collector handles cleanup automatically. My first
`append()` implementation traversed the WHOLE list every time to find
the end (O(n) per append), which I optimized later by tracking a `tail`
pointer after reading about amortized complexity during interview prep.

### Stack

Python's list already does everything a stack needs via `append()`/
`pop()`. Built a wrapper class anyway specifically to restrict the
interface — prevents future-me from accidentally doing something
un-stack-like, and forced me to actually understand LIFO behavior rather
than just trusting list methods. The balanced-parentheses checker and
postfix expression evaluator were the exercises that made stacks feel
genuinely USEFUL rather than just academically interesting.

### Queue

This is where I learned a real performance lesson, not just a syntax
lesson. My first queue implementation used a plain list with
`list.pop(0)` to dequeue. It WORKED correctly. It was also O(n) per
dequeue because every remaining element has to shift left by one index
internally — meaning a queue built on a list is secretly O(n²) for n
operations. Switched to `collections.deque` (doubly-linked-list internally,
O(1) at both ends) and measured an actual timing difference to confirm
this wasn't just theoretical. This directly connects to the
Multithreading module — "correct" and "performant" are different
questions, and I need to ask both.

### Tree (Binary Search Tree)

Hardest topic in this module, harder than I expected. The recursion
required for insert/search/traversal took real, deliberate practice — I
drew dozens of tree diagrams on paper before the recursive logic stopped
feeling like guesswork I was hoping would work. The realization that
INORDER traversal of a valid BST always produces SORTED output was the
moment this topic actually clicked for me, rather than just being
abstract recursive code.

Also deliberately tested what happens when you insert already-sorted
data into a BST — confirmed it degenerates into something close to a
linked list (height ≈ n instead of height ≈ log n), which is exactly WHY
self-balancing trees (AVL, Red-Black) exist. Haven't implemented a
self-balancing tree from scratch yet — noted as a TODO for future study.

### Graph

Felt like a natural extension after trees (a tree IS technically a
constrained graph). Used adjacency-list representation (dict of lists)
instead of an adjacency matrix for memory efficiency on sparse graphs.
BFS and DFS connected back directly to Stack.py and Queue.py from
earlier in this same module — BFS uses a queue, DFS uses a stack (or
recursion, which is really just the call stack doing the same job
implicitly). That connection tied the whole module together for me far
better than treating each data structure as an isolated topic.

Modeled a small friend-network graph for testing instead of abstract
node labels (A, B, C) — made traversal results easier to reason about
intuitively ("of course Pavan's direct friends get visited before
friends-of-friends in BFS").

### Sorting Algorithms

Implemented Bubble Sort, Selection Sort, and Insertion Sort (all O(n²))
followed by Merge Sort and Quick Sort (O(n log n) average case). Ran
actual timing comparisons rather than trusting Big-O notation as pure
abstraction — watching bubble sort's time roughly QUADRUPLE when I
doubled the input size, while merge/quick sort scaled much more gently,
made complexity analysis feel like a measurable engineering property
instead of an exam topic.

Deliberately tested Quick Sort's worst case — confirmed that naive
first-element pivot selection on already-sorted input degrades toward
O(n²), then compared against middle-element pivot selection which avoids
that specific failure mode. Wanted to verify this myself rather than
just accept the textbook claim.

### Searching Algorithms

Made the exact mistake the textbooks warn about: ran binary search on
UNSORTED data and got a wrong answer that didn't even look obviously
wrong — no crash, no error, just silently incorrect output. Took several
confused minutes assuming my code was buggy before remembering binary
search REQUIRES sorted input as a precondition, not just a suggestion.
This was a good lesson that algorithms have prerequisites, not just
steps — violating a precondition doesn't always fail loudly.

The scale comparison (1,000,000-element sorted array, linear vs binary
search) gave the most visceral demonstration of O(log n) vs O(n) I've
encountered in this whole module — binary search needing roughly 20
comparisons versus potentially a million for linear search.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| O(n) append on linked list | Traversed whole list every append | Added tail pointer tracking for O(1) append |
| O(n) dequeue using list.pop(0) | Queue performance degraded on larger data | Switched to collections.deque |
| Recursion felt like guesswork on trees | Couldn't predict traversal output mentally | Drew tree diagrams by hand repeatedly until patterns clicked |
| RecursionError on deep graph DFS | Default Python recursion limit (1000) exceeded | Wrote an iterative DFS using an explicit stack |
| Binary search on unsorted data | Got wrong answer silently, no crash | Remembered binary search REQUIRES sorted input as precondition |
| Assumed Big-O was purely theoretical | Didn't expect to SEE quadratic vs linearithmic difference directly | Ran actual timing benchmarks comparing algorithms at increasing sizes |
| Quicksort slow on sorted data | First-element pivot caused near-worst-case behavior | Switched to middle-element pivot selection |

---

## Optimization attempts worth remembering

1. **Linked list append:** O(n) → O(1) per append via tail pointer tracking
2. **Queue dequeue:** O(n) → O(1) per dequeue via switching list → deque
3. **DFS on deep graphs:** Recursive (depth-limited) → Iterative with
   explicit stack (no depth limit beyond available memory)
4. **Quicksort pivot choice:** First-element (vulnerable to sorted-input
   worst case) → Middle-element (more resilient, though not foolproof)

---

## Lessons learned after this module

- "Works correctly" and "performs well" are genuinely different
  questions — test both
- Recursive thinking takes deliberate practice, especially for trees;
  drawing diagrams helped more than reading explanations
- BFS↔Queue and DFS↔Stack are not coincidental pairings — understanding
  one data structure deepens understanding of the algorithm built on it
- Algorithms have PRECONDITIONS (sorted data, etc.) — violating them can
  fail silently rather than loudly, which is more dangerous
- Big-O differences are measurable, not just theoretical — benchmark
  when in doubt instead of trusting intuition alone

Next up: Interview Preparation — consolidating everything from modules
1-13 into a structured review, plus the 10 portfolio projects where all
of this finally gets applied to build complete, working applications.
