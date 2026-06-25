# 🎯 Coding Problems — Practice Log

**Compiled by:** Pavan Shetty H S
**Last updated:** October 2024

---

## About this file

These are coding problems I worked through during interview prep, mostly
sourced from LeetCode-style practice and a few from actual mock
interviews. I'm including my FIRST attempt's approach alongside the
optimized version where relevant, because the optimization JOURNEY is
more useful for my own learning than just having the final clean
solution memorized.

---

## Problem 1: Two Sum

**Problem:** Given an array of integers and a target, return indices of
the two numbers that add up to the target.

**My first attempt (brute force):**
```python
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```
O(n²) time, O(1) space. Worked, but I knew immediately this wouldn't
scale.

**Optimized version (hash map):**
```python
def two_sum(nums, target):
    seen = {}   # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```
O(n) time, O(n) space. The realization that clicked: instead of checking
EVERY pair, just remember what I've already seen and check if its
"partner" (target - current number) exists in that memory. Classic
trade-off — used more space to save a huge amount of time.

---

## Problem 2: Reverse a String In-Place

**Problem:** Reverse a list of characters in place.

```python
def reverse_string(s):
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return s
```
O(n) time, O(1) extra space (true in-place, only swapping). Two-pointer
technique — this pattern showed up again and again once I started
recognizing it, connects to the string reversal I did differently
(using a stack) in Stack.py during Module 13.

---

## Problem 3: 🔴 Find Duplicate in Array

**Problem:** Given an array of n+1 integers where each integer is
between 1 and n, find the duplicate.

**My first attempt:**
```python
def find_duplicate_v1(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)
```
O(n) time, O(n) space. This worked and I initially thought I was done.

**What the interviewer actually wanted (constant space):**
```python
def find_duplicate_v2(nums):
    # Floyd's cycle detection applied to array-as-linked-list
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow2 = nums[0]
    while slow != slow2:
        slow = nums[slow]
        slow2 = nums[slow2]
    return slow
```
This one genuinely humbled me. I was happy with my O(n) space solution
until asked "can you do it in O(1) space?" The trick: treat the array
itself as a linked list where `nums[i]` points to the NEXT index to
visit, then apply Floyd's cycle detection (the SAME tortoise-and-hare
algorithm from my DSA interview notes on linked list cycle detection).
A duplicate value guarantees a "cycle" forms in this implicit
linked-list view. This connected two topics I'd studied separately
(arrays, linked list cycle detection) in a way I hadn't anticipated —
good reminder that DSA topics aren't actually as separate as the module
folders make them look.

---

## Problem 4: Valid Anagram

**Problem:** Given two strings, determine if one is an anagram of the other.

```python
def is_anagram(s1, s2):
    if len(s1) != len(s2):
        return False
    from collections import Counter
    return Counter(s1) == Counter(s2)
```
O(n) time, O(1) space (bounded alphabet size, technically O(k) where k
is alphabet size). Used `Counter` instead of manually building frequency
dicts — directly reused the pattern from my word-frequency counter
exercise in Dictionaries.py (Module 4).

---

## Problem 5: Merge Two Sorted Lists

**Problem:** Merge two sorted linked lists into one sorted linked list.

```python
def merge_two_lists(l1, l2):
    dummy = Node(0)
    current = dummy
    while l1 and l2:
        if l1.data <= l2.data:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    current.next = l1 if l1 else l2
    return dummy.next
```
O(n+m) time, O(1) extra space (just rewiring existing nodes, not
creating new ones). This is LITERALLY the merge step from my MergeSort.py
implementation (Module 13), just applied to linked lists instead of
arrays. Recognizing this connection made the problem trivial once I
spotted the pattern instead of solving it from scratch.

---

## Problem 6: 🔴 Maximum Subarray (Kadane's Algorithm)

**Problem:** Find the contiguous subarray with the largest sum.

**My first (wrong direction) attempt:**
```python
def max_subarray_brute(nums):
    max_sum = float('-inf')
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            current_sum = sum(nums[i:j+1])
            max_sum = max(max_sum, current_sum)
    return max_sum
```
O(n³) actually (due to `sum()` re-summing the slice each time) — even
worse than the O(n²) I initially assumed. Definitely too slow for large
inputs.

**Kadane's Algorithm (the one I had to look up and study properly):**
```python
def max_subarray(nums):
    max_sum = current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum
```
O(n) time, O(1) space. The insight that took me genuine time to
internalize: at each position, decide whether to EXTEND the previous
subarray or START FRESH from the current element — extend only if the
running sum is still helping (positive), otherwise the past is dragging
you down and you're better off restarting. This is my first real taste
of dynamic programming "decide based on the best sub-solution so far"
thinking, beyond the Fibonacci memoization from Module 3.

---

## Practice Log Summary

| Date | Problem | Result | Notes |
|---|---|---|---|
| Oct 3, 2024 | Two Sum | Solved, optimized | Hash map pattern, very reusable |
| Oct 4, 2024 | Reverse String | Solved first try | Two-pointer pattern |
| Oct 7, 2024 | Find Duplicate | Solved brute force, needed hint for O(1) space | Floyd's cycle detection on arrays — humbling |
| Oct 9, 2024 | Valid Anagram | Solved first try | Reused Counter pattern from Module 4 |
| Oct 12, 2024 | Merge Sorted Lists | Solved, recognized pattern fast | Same logic as MergeSort.py's merge step |
| Oct 15, 2024 | Max Subarray | Needed to research Kadane's | First real DP "beyond Fibonacci" problem |

---

## Honest reflection

The pattern I notice across this whole log: problems that connect to
something I ALREADY built from scratch in Module 13 (merge logic, cycle
detection, frequency counting) go much faster than genuinely novel
problems (Kadane's algorithm was new thinking, not a recombination of
existing knowledge). This is making me want to deliberately study more
classic DP patterns next, since that's clearly still a weaker area for
me than arrays/linked lists/trees at this point.
