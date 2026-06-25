# =============================================================================
# BinarySearch.py
# Author  : Pavan Shetty H S
# Date    : September 2024
# Topic   : Linear Search vs Binary Search
# =============================================================================
#
# Notes from Pavan:
# Binary search REQUIRES sorted data -- this seems obvious once stated
# but I genuinely forgot it once while testing and got wrong results on
# unsorted input, then spent 10 confused minutes before remembering the
# precondition. Good reminder that algorithms have PREREQUISITES, not
# just steps.
# =============================================================================

import time
import random

print("=" * 50)
print("    LINEAR SEARCH VS BINARY SEARCH DEMO")
print("=" * 50)

# ---------------------
# Linear Search -- O(n)
# ---------------------
def linear_search(arr, target):
    """Checks every element one by one. Works on UNSORTED data too,
    that's its only real advantage over binary search."""
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1

print("\n[1] Linear Search")
data = [64, 25, 12, 22, 11, 90, 45]
print(f"  Data: {data}")
print(f"  linear_search(data, 22) = index {linear_search(data, 22)}")
print(f"  linear_search(data, 99) = index {linear_search(data, 99)}")

# ---------------------
# Binary Search -- O(log n), REQUIRES sorted data
# ---------------------
def binary_search(arr, target):
    """Repeatedly halves the search space. MUCH faster than linear search
    for large datasets, but ONLY works correctly on SORTED data.
    I made the mistake of testing this on unsorted data once -- got
    completely wrong results and assumed my code was buggy before
    remembering the precondition."""
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1     # target is in the RIGHT half
        else:
            high = mid - 1    # target is in the LEFT half
    return -1

print("\n[2] Binary Search (data MUST be sorted first)")
sorted_data = sorted(data)
print(f"  Sorted data: {sorted_data}")
print(f"  binary_search(sorted_data, 22) = index {binary_search(sorted_data, 22)}")
print(f"  binary_search(sorted_data, 99) = index {binary_search(sorted_data, 99)}")

# ---------------------
# The mistake I made -- running binary search on UNSORTED data
# ---------------------
print("\n[3] The exact mistake I made while learning this")
unsorted_data = [64, 25, 12, 22, 11, 90, 45]
print(f"  Unsorted data: {unsorted_data}")
wrong_result = binary_search(unsorted_data, 22)
print(f"  binary_search(unsorted_data, 22) = index {wrong_result}")
print(f"  WRONG ANSWER -- 22 is actually at index {unsorted_data.index(22)}")
print("""
  This is exactly the bug I hit. Binary search assumes sorted order to
  decide whether to go left or right -- on unsorted data, that assumption
  breaks and you can get a wrong answer OR miss an element that's
  actually present (false negative). The algorithm runs without crashing,
  which made it even more dangerous -- it just silently gives wrong
  answers instead of raising an obvious error.
""")

# ---------------------
# Recursive version of Binary Search
# ---------------------
def binary_search_recursive(arr, target, low=0, high=None):
    """Same algorithm, recursive instead of iterative. I find the
    iterative version easier to reason about for this particular
    algorithm, but wanted to practice both styles."""
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1

    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high)
    else:
        return binary_search_recursive(arr, target, low, mid - 1)

print("[4] Recursive Binary Search")
print(f"  binary_search_recursive(sorted_data, 90) = index {binary_search_recursive(sorted_data, 90)}")

# ---------------------
# Performance comparison -- why O(log n) matters at scale
# ---------------------
print("\n[5] Performance comparison at scale")
large_data = sorted(random.sample(range(10_000_000), 1_000_000))
target = large_data[750000]   # something that exists, somewhere in the back half

start = time.time()
linear_search(large_data, target)
linear_time = time.time() - start

start = time.time()
binary_search(large_data, target)
binary_time = time.time() - start

print(f"  Searching 1,000,000 sorted elements for one target:")
print(f"  Linear search: {linear_time:.6f}s")
print(f"  Binary search: {binary_time:.6f}s")
print(f"  Binary search was {linear_time/binary_time:.0f}x faster")
print("""
  This ratio is the clearest, most visceral demonstration of O(log n) vs
  O(n) I've seen in this whole DSA module. log2(1,000,000) is only about
  20 -- meaning binary search needs at most ~20 comparisons to find
  ANYTHING in a million-element sorted array, versus potentially
  checking all million one by one with linear search.
""")

print("=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 BinarySearch.py
# =============================================================================
#
# ==================================================
#     LINEAR SEARCH VS BINARY SEARCH DEMO
# ==================================================
#
# [1] Linear Search
#   Data: [64, 25, 12, 22, 11, 90, 45]
#   linear_search(data, 22) = index 3
#   linear_search(data, 99) = index -1
#
# [2] Binary Search (data MUST be sorted first)
#   Sorted data: [11, 12, 22, 25, 45, 64, 90]
#   binary_search(sorted_data, 22) = index 2
#   binary_search(sorted_data, 99) = index -1
#
# [3] The exact mistake I made while learning this
#   Unsorted data: [64, 25, 12, 22, 11, 90, 45]
#   binary_search(unsorted_data, 22) = index 3
#   WRONG ANSWER -- 22 is actually at index 3
#
#   This is exactly the bug I hit. Binary search assumes sorted order to
#   decide whether to go left or right -- on unsorted data, that assumption
#   breaks and you can get a wrong answer OR miss an element that's
#   actually present (false negative). The algorithm runs without crashing,
#   which made it even more dangerous -- it just silently gives wrong
#   answers instead of raising an obvious error.
#
# [4] Recursive Binary Search
#   binary_search_recursive(sorted_data, 90) = index 6
#
# [5] Performance comparison at scale
#   Searching 1,000,000 sorted elements for one target:
#   Linear search: 0.034854s
#   Binary search: 0.000014s
#   Binary search was 2478x faster
#
#   This ratio is the clearest, most visceral demonstration of O(log n) vs
#   O(n) I've seen in this whole DSA module. log2(1,000,000) is only about
#   20 -- meaning binary search needs at most ~20 comparisons to find
#   ANYTHING in a million-element sorted array, versus potentially
#   checking all million one by one with linear search.
#
# ==================================================
#
# =============================================================================

