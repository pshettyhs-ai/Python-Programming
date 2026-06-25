# =============================================================================
# LinkedList.py
# Author  : Pavan Shetty H S
# Date    : September 2024
# Topic   : Singly Linked List implementation from scratch
# =============================================================================
#
# Notes from Pavan:
# Implemented linked lists in C during my data structures course, so the
# CONCEPT wasn't new -- pointers/Node structs are exactly what this is.
# What's different in Python: no manual malloc/free, garbage collector
# handles memory, and "pointers" are just object references. Felt
# noticeably easier to implement here than it did in C.
# =============================================================================

print("=" * 50)
print("    SINGLY LINKED LIST DEMO")
print("=" * 50)

class Node:
    """A single node holding data and a reference to the next node."""
    def __init__(self, data):
        self.data = data
        self.next = None   # this 'next' is exactly like a C pointer, just safer

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, data):
        """Add a node to the END of the list. O(n) without a tail pointer --
        I initially didn't track a tail, traversed the whole list every
        append. Optimized later (see notes below)."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def prepend(self, data):
        """Add a node to the BEGINNING. O(1) -- much faster than append."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def delete(self, data):
        """Delete the first node matching 'data'."""
        if self.head is None:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    def search(self, data):
        """Returns True if data exists in the list. O(n)."""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def reverse(self):
        """Reverses the linked list in place.
        This took me a few tries to get right -- the classic
        prev/current/next pointer juggling. Drew it out on paper
        before I trusted my code."""
        prev = None
        current = self.head
        while current:
            next_node = current.next   # save next before we overwrite it
            current.next = prev        # reverse the link
            prev = current              # move prev forward
            current = next_node         # move current forward
        self.head = prev

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " -> ".join(elements) + " -> None"

    def __len__(self):
        return self.size

# ---------------------
# Testing the implementation
# ---------------------
print("\n[1] Building a linked list")
ll = LinkedList()
ll.append(10)
ll.append(20)
ll.append(30)
ll.prepend(5)
print(f"  List: {ll.display()}")
print(f"  Size: {len(ll)}")

print("\n[2] Searching")
print(f"  search(20): {ll.search(20)}")
print(f"  search(99): {ll.search(99)}")

print("\n[3] Deleting")
ll.delete(20)
print(f"  After delete(20): {ll.display()}")

print("\n[4] Reversing")
ll.reverse()
print(f"  After reverse(): {ll.display()}")

# ---------------------
# Optimization note: tracking a tail pointer
# ---------------------
print("\n[5] Optimization I made after profiling my first version")
print("""
  My very first version of append() traversed the ENTIRE list every time
  to find the last node -- O(n) per append, making building a list of N
  elements O(n^2) overall. After learning about amortized complexity in
  my DSA interview prep, I optimized by tracking a 'tail' pointer:

    self.tail = new_node   # update after every append

  This turns append() into O(1), making building a list of N elements
  O(n) overall. Left the O(n) version above for teaching clarity, but
  my actual project implementations use the tail-tracking version.
""")

print("=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 LinkedList.py
# =============================================================================
#
# ==================================================
#     SINGLY LINKED LIST DEMO
# ==================================================
#
# [1] Building a linked list
#   List: 5 -> 10 -> 20 -> 30 -> None
#   Size: 4
#
# [2] Searching
#   search(20): True
#   search(99): False
#
# [3] Deleting
#   After delete(20): 5 -> 10 -> 30 -> None
#
# [4] Reversing
#   After reverse(): 30 -> 10 -> 5 -> None
#
# [5] Optimization I made after profiling my first version
#
#   My very first version of append() traversed the ENTIRE list every time
#   to find the last node -- O(n) per append, making building a list of N
#   elements O(n^2) overall. After learning about amortized complexity in
#   my DSA interview prep, I optimized by tracking a 'tail' pointer:
#
#     self.tail = new_node   # update after every append
#
#   This turns append() into O(1), making building a list of N elements
#   O(n) overall. Left the O(n) version above for teaching clarity, but
#   my actual project implementations use the tail-tracking version.
#
# ==================================================
#
# =============================================================================

