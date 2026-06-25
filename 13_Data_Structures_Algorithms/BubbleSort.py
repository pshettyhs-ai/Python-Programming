# =============================================================================
# BubbleSort.py
# Author  : Pavan Shetty H S
# Date    : September 2024
# Topic   : Bubble Sort + other O(n^2) sorts (Selection, Insertion)
# =============================================================================
#
# Notes from Pavan:
# Bubble sort is everyone's "first" sorting algorithm, and for good
# reason -- it's the easiest to understand intuitively (repeatedly swap
# adjacent out-of-order elements). But it's also genuinely bad for large
# data, O(n^2). I implement it anyway because understanding WHY it's
# slow matters more than just being told "use Python's sort() instead."
# =============================================================================

import time
import random

print("=" * 50)
print("    BUBBLE SORT & FRIENDS DEMO")
print("=" * 50)

# ---------------------
# Bubble Sort
# ---------------------
def bubble_sort(arr):
    """Repeatedly swaps adjacent elements if they're in the wrong order.
    After each full pass, the largest unsorted element 'bubbles up' to
    its correct position at the end."""
    arr = arr.copy()   # don't mutate the original, learned this habit
                        # after accidentally sorting test data in place
                        # and confusing my own comparison tests
    n = len(arr)
    for i in range(n):
        swapped = False   # optimization: if no swaps happen, array is sorted
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]   # Python swap trick
                swapped = True
        if not swapped:
            break   # early exit if already sorted -- saves passes
    return arr

print("\n[1] Bubble Sort")
test_data = [64, 34, 25, 12, 22, 11, 90]
print(f"  Original: {test_data}")
print(f"  Sorted  : {bubble_sort(test_data)}")

# ---------------------
# Selection Sort
# ---------------------
def selection_sort(arr):
    """Finds the MINIMUM element each pass, swaps it into position.
    Fewer swaps than bubble sort, but same O(n^2) comparisons."""
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

print("\n[2] Selection Sort")
print(f"  Original: {test_data}")
print(f"  Sorted  : {selection_sort(test_data)}")

# ---------------------
# Insertion Sort
# ---------------------
def insertion_sort(arr):
    """Builds the sorted array one element at a time, like sorting
    playing cards in your hand. Genuinely efficient for SMALL or
    NEARLY-SORTED data -- a detail I didn't expect to matter until I
    read it's actually used as a fallback inside Python's built-in
    Timsort for small sub-arrays."""
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

print("\n[3] Insertion Sort")
print(f"  Original: {test_data}")
print(f"  Sorted  : {insertion_sort(test_data)}")

# ---------------------
# Performance comparison -- proving these are O(n^2)
# ---------------------
print("\n[4] Performance comparison on larger data")
sizes = [100, 500, 1000]
for size in sizes:
    data = [random.randint(1, 10000) for _ in range(size)]

    start = time.time()
    bubble_sort(data)
    bubble_time = time.time() - start

    start = time.time()
    data.copy().sort()   # Python's built-in Timsort, for comparison
    builtin_time = time.time() - start

    print(f"  n={size:5}: bubble_sort={bubble_time:.5f}s | built-in sort={builtin_time:.6f}s")

print("""
  Watching bubble_sort's time roughly QUADRUPLE when I doubled n (the
  O(n^2) signature) versus the built-in sort barely changing was the
  moment Big-O stopped being an abstract exam concept and started being
  something I could literally watch happen on my own screen.
""")

print("=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 BubbleSort.py
# =============================================================================
#
# ==================================================
#     BUBBLE SORT & FRIENDS DEMO
# ==================================================
#
# [1] Bubble Sort
#   Original: [64, 34, 25, 12, 22, 11, 90]
#   Sorted  : [11, 12, 22, 25, 34, 64, 90]
#
# [2] Selection Sort
#   Original: [64, 34, 25, 12, 22, 11, 90]
#   Sorted  : [11, 12, 22, 25, 34, 64, 90]
#
# [3] Insertion Sort
#   Original: [64, 34, 25, 12, 22, 11, 90]
#   Sorted  : [11, 12, 22, 25, 34, 64, 90]
#
# [4] Performance comparison on larger data
#   n=  100: bubble_sort=0.00023s | built-in sort=0.000010s
#   n=  500: bubble_sort=0.00714s | built-in sort=0.000052s
#   n= 1000: bubble_sort=0.03023s | built-in sort=0.000108s
#
#   Watching bubble_sort's time roughly QUADRUPLE when I doubled n (the
#   O(n^2) signature) versus the built-in sort barely changing was the
#   moment Big-O stopped being an abstract exam concept and started being
#   something I could literally watch happen on my own screen.
#
# ==================================================
#
# =============================================================================

