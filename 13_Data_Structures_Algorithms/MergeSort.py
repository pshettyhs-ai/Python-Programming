# =============================================================================
# MergeSort.py
# Author  : Pavan Shetty H S
# Date    : September 2024
# Topic   : Merge Sort + Quick Sort -- O(n log n) divide-and-conquer sorts
# =============================================================================
#
# Notes from Pavan:
# This is where "divide and conquer" stopped being a vague textbook
# phrase and started being something I could trace through manually.
# Merge sort's recursion pattern is similar to what I practiced in
# Recursion.py (Module 3) -- break a big problem into smaller identical
# subproblems until trivially solvable, then combine results.
# =============================================================================

import time
import random

print("=" * 50)
print("    MERGE SORT & QUICK SORT DEMO")
print("=" * 50)

# ---------------------
# Merge Sort
# ---------------------
def merge_sort(arr):
    """Divide: split array in half recursively until single elements.
    Conquer: merge sorted halves back together in correct order.
    O(n log n) guaranteed, regardless of input order -- unlike quicksort
    which has a worst case I'll cover below."""
    if len(arr) <= 1:
        return arr   # base case -- a single element is already "sorted"

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return _merge(left_half, right_half)

def _merge(left, right):
    """Merges two ALREADY SORTED lists into one sorted list.
    This merge step is the part that confused me initially -- I kept
    wanting to just concatenate and re-sort, missing the entire point
    that merging two sorted lists can be done in O(n) with a single pass."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements (one side will have leftovers)
    result.extend(left[i:])
    result.extend(right[j:])
    return result

print("\n[1] Merge Sort")
test_data = [38, 27, 43, 3, 9, 82, 10]
print(f"  Original: {test_data}")
print(f"  Sorted  : {merge_sort(test_data)}")

# ---------------------
# Quick Sort
# ---------------------
def quick_sort(arr):
    """Picks a 'pivot', partitions array into [smaller than pivot] and
    [larger than pivot], recursively sorts each partition.
    Average case O(n log n), but worst case O(n^2) if pivot choice is
    consistently bad (e.g. always picking the smallest/largest element,
    which happens with already-sorted data and naive pivot selection)."""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]   # middle element as pivot -- avoids
                                   # worst-case behavior on already-sorted
                                   # data better than always picking first/last
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

print("\n[2] Quick Sort")
print(f"  Original: {test_data}")
print(f"  Sorted  : {quick_sort(test_data)}")

# ---------------------
# The worst-case scenario I tested deliberately
# ---------------------
print("\n[3] Quick Sort's worst case -- tested this myself")
print("""
  Read that quicksort degrades to O(n^2) on already-sorted data IF you
  naively pick the FIRST element as pivot every time (each partition
  only removes ONE element instead of splitting roughly in half).
  Wanted to verify this myself instead of just trusting the claim.
""")

def quick_sort_bad_pivot(arr):
    """Deliberately bad version -- always picks FIRST element as pivot."""
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quick_sort_bad_pivot(left) + [pivot] + quick_sort_bad_pivot(right)

sorted_data_small = list(range(800))   # already sorted -- worst case trigger

start = time.time()
quick_sort_bad_pivot(sorted_data_small)
bad_pivot_time = time.time() - start

start = time.time()
quick_sort(sorted_data_small)   # middle-pivot version
good_pivot_time = time.time() - start

print(f"  Bad pivot (first element) on sorted data: {bad_pivot_time:.4f}s")
print(f"  Better pivot (middle element)            : {good_pivot_time:.4f}s")
print(f"  Bad pivot was {bad_pivot_time/good_pivot_time:.1f}x slower on this input")
print("  Confirmed the textbook claim is real, not just theoretical.")

# ---------------------
# Performance comparison: Merge Sort vs Quick Sort vs Bubble Sort
# ---------------------
print("\n[4] Performance comparison -- O(n log n) vs O(n^2)")
sizes = [1000, 5000]
for size in sizes:
    data = [random.randint(1, 100000) for _ in range(size)]

    start = time.time()
    merge_sort(data)
    merge_time = time.time() - start

    start = time.time()
    quick_sort(data)
    quick_time = time.time() - start

    print(f"  n={size}: merge_sort={merge_time:.5f}s | quick_sort={quick_time:.5f}s")

print("""
  Both stay roughly proportional to n*log(n) as size grows, instead of
  exploding quadratically like bubble_sort did in BubbleSort.py. Seeing
  this side by side made the O(n log n) vs O(n^2) distinction feel like
  a real, measurable engineering decision rather than an academic label.
""")

print("=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 MergeSort.py
# =============================================================================
#
# ==================================================
#     MERGE SORT & QUICK SORT DEMO
# ==================================================
#
# [1] Merge Sort
#   Original: [38, 27, 43, 3, 9, 82, 10]
#   Sorted  : [3, 9, 10, 27, 38, 43, 82]
#
# [2] Quick Sort
#   Original: [38, 27, 43, 3, 9, 82, 10]
#   Sorted  : [3, 9, 10, 27, 38, 43, 82]
#
# [3] Quick Sort's worst case -- tested this myself
#
#   Read that quicksort degrades to O(n^2) on already-sorted data IF you
#   naively pick the FIRST element as pivot every time (each partition
#   only removes ONE element instead of splitting roughly in half).
#   Wanted to verify this myself instead of just trusting the claim.
#
#   Bad pivot (first element) on sorted data: 0.0139s
#   Better pivot (middle element)            : 0.0005s
#   Bad pivot was 28.7x slower on this input
#   Confirmed the textbook claim is real, not just theoretical.
#
# [4] Performance comparison -- O(n log n) vs O(n^2)
#   n=1000: merge_sort=0.00121s | quick_sort=0.00100s
#   n=5000: merge_sort=0.00728s | quick_sort=0.00597s
#
#   Both stay roughly proportional to n*log(n) as size grows, instead of
#   exploding quadratically like bubble_sort did in BubbleSort.py. Seeing
#   this side by side made the O(n log n) vs O(n^2) distinction feel like
#   a real, measurable engineering decision rather than an academic label.
#
# ==================================================
#
# =============================================================================

