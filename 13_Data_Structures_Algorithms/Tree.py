# =============================================================================
# Tree.py
# Author  : Pavan Shetty H S
# Date    : September 2024
# Topic   : Binary Search Tree implementation
# =============================================================================
#
# Notes from Pavan:
# Trees were conceptually the hardest DSA topic for me, harder than
# linked lists even. The recursion required for insert/search/traversal
# took real practice to feel natural. Drew dozens of tree diagrams on
# paper before the recursive logic stopped feeling like guesswork.
# =============================================================================

print("=" * 50)
print("    BINARY SEARCH TREE DEMO")
print("=" * 50)

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        """Public method -- kicks off the recursive helper."""
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        """BST rule: smaller values go LEFT, larger values go RIGHT."""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    # ---------------------
    # Tree Traversals -- the part that confused me most
    # ---------------------
    def inorder(self):
        """LEFT -> ROOT -> RIGHT. For a BST, this gives SORTED order!
        This was the realization that made BSTs click for me -- inorder
        traversal of a valid BST always produces sorted output."""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder(self):
        """ROOT -> LEFT -> RIGHT. Useful for copying/serializing a tree."""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder(self):
        """LEFT -> RIGHT -> ROOT. Useful for safely deleting a tree."""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def height(self):
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if node is None:
            return -1
        return 1 + max(self._height_recursive(node.left), self._height_recursive(node.right))

    def find_min(self):
        if self.root is None:
            return None
        current = self.root
        while current.left:
            current = current.left
        return current.value

    def find_max(self):
        if self.root is None:
            return None
        current = self.root
        while current.right:
            current = current.right
        return current.value

# ---------------------
# Building and testing the BST
# ---------------------
print("\n[1] Building a BST")
bst = BinarySearchTree()
values = [50, 30, 70, 20, 40, 60, 80, 10]
for v in values:
    bst.insert(v)
print(f"  Inserted: {values}")

print("\n[2] Tree traversals")
print(f"  Inorder   (sorted!): {bst.inorder()}")
print(f"  Preorder            : {bst.preorder()}")
print(f"  Postorder           : {bst.postorder()}")

print("\n[3] Search operations")
print(f"  search(40): {bst.search(40)}")
print(f"  search(99): {bst.search(99)}")

print("\n[4] Tree properties")
print(f"  Height   : {bst.height()}")
print(f"  Min value: {bst.find_min()}")
print(f"  Max value: {bst.find_max()}")

# ---------------------
# Why BST search is O(log n) -- and when it ISN'T
# ---------------------
print("\n[5] The gotcha I learned about BST performance")
print("""
  BST search is O(log n) ONLY if the tree is reasonably balanced. If you
  insert ALREADY SORTED data (1, 2, 3, 4, 5...), every new node becomes
  the right child of the previous one, and the tree degenerates into
  basically a LINKED LIST -- O(n) search instead of O(log n)!

  I proved this to myself below:
""")

balanced_bst = BinarySearchTree()
for v in [50, 30, 70, 20, 40, 60, 80]:   # inserted in a balanced order
    balanced_bst.insert(v)
print(f"  Balanced tree height (7 nodes): {balanced_bst.height()}")

degenerate_bst = BinarySearchTree()
for v in [10, 20, 30, 40, 50, 60, 70]:   # inserted in SORTED order
    degenerate_bst.insert(v)
print(f"  Degenerate tree height (7 sorted nodes): {degenerate_bst.height()}")
print("""
  Both have 7 nodes, but the degenerate one is MUCH taller, meaning
  searches take longer. This is exactly why self-balancing trees
  (AVL, Red-Black) exist -- something I want to study further, but
  haven't implemented from scratch yet. Noting it here as a TODO.
""")

print("=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Tree.py
# =============================================================================
#
# ==================================================
#     BINARY SEARCH TREE DEMO
# ==================================================
#
# [1] Building a BST
#   Inserted: [50, 30, 70, 20, 40, 60, 80, 10]
#
# [2] Tree traversals
#   Inorder   (sorted!): [10, 20, 30, 40, 50, 60, 70, 80]
#   Preorder            : [50, 30, 20, 10, 40, 70, 60, 80]
#   Postorder           : [10, 20, 40, 30, 60, 80, 70, 50]
#
# [3] Search operations
#   search(40): True
#   search(99): False
#
# [4] Tree properties
#   Height   : 3
#   Min value: 10
#   Max value: 80
#
# [5] The gotcha I learned about BST performance
#
#   BST search is O(log n) ONLY if the tree is reasonably balanced. If you
#   insert ALREADY SORTED data (1, 2, 3, 4, 5...), every new node becomes
#   the right child of the previous one, and the tree degenerates into
#   basically a LINKED LIST -- O(n) search instead of O(log n)!
#
#   I proved this to myself below:
#
#   Balanced tree height (7 nodes): 2
#   Degenerate tree height (7 sorted nodes): 6
#
#   Both have 7 nodes, but the degenerate one is MUCH taller, meaning
#   searches take longer. This is exactly why self-balancing trees
#   (AVL, Red-Black) exist -- something I want to study further, but
#   haven't implemented from scratch yet. Noting it here as a TODO.
#
# ==================================================
#
# =============================================================================

