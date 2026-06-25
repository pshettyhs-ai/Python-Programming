# =============================================================================
# Stack.py
# Author  : Pavan Shetty H S
# Date    : September 2024
# Topic   : Stack -- LIFO data structure
# =============================================================================
#
# Notes from Pavan:
# Python's list already has append()/pop() which work perfectly as a
# stack (both O(1) at the END of a list). I implement a wrapper class
# anyway for two reasons: (1) practice understanding the underlying
# concept properly, (2) restrict the interface so future-me can't
# accidentally do something un-stack-like (like inserting in the middle).
# =============================================================================

print("=" * 50)
print("    STACK DEMO")
print("=" * 50)

class Stack:
    """LIFO -- Last In, First Out. Think of a stack of plates."""
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)   # add to the END (top of stack)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()   # remove from the END

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __str__(self):
        return f"Stack({self._items})"

# ---------------------
# Basic usage
# ---------------------
print("\n[1] Basic stack operations")
s = Stack()
s.push(10)
s.push(20)
s.push(30)
print(f"  After pushing 10, 20, 30: {s}")
print(f"  peek(): {s.peek()}")
print(f"  pop(): {s.pop()}")
print(f"  After pop: {s}")

# ---------------------
# Practical use case 1: Balanced parentheses checker
# ---------------------
print("\n[2] Practical: Balanced parentheses checker")
print("  Classic stack interview question -- I see this constantly in")
print("  interview prep material, so wanted to actually implement it.")

def is_balanced(expression):
    stack = Stack()
    pairs = {')': '(', '}': '{', ']': '['}

    for char in expression:
        if char in "({[":
            stack.push(char)
        elif char in ")}]":
            if stack.is_empty() or stack.pop() != pairs[char]:
                return False
    return stack.is_empty()

test_expressions = [
    "(a + b) * (c - d)",
    "{[()]}",
    "(a + b]",
    "((a + b)",
    "[{()}]"
]
for expr in test_expressions:
    print(f"  '{expr}' -> Balanced: {is_balanced(expr)}")

# ---------------------
# Practical use case 2: Reversing a string using a stack
# ---------------------
print("\n[3] Practical: Reverse a string using a stack")

def reverse_string_stack(s):
    stack = Stack()
    for char in s:
        stack.push(char)
    result = ""
    while not stack.is_empty():
        result += stack.pop()
    return result

print(f"  reverse_string_stack('Pavan'): {reverse_string_stack('Pavan')}")

# ---------------------
# Practical use case 3: Evaluating postfix expressions
# ---------------------
print("\n[4] Practical: Postfix (Reverse Polish Notation) evaluation")

def evaluate_postfix(expression):
    """Example: '5 3 +' = 8 (5 + 3)
    Took some practice to mentally parse postfix notation correctly --
    operators come AFTER their operands, opposite of normal infix math."""
    stack = Stack()
    tokens = expression.split()

    for token in tokens:
        if token.lstrip('-').isdigit():
            stack.push(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.push(a + b)
            elif token == '-':
                stack.push(a - b)
            elif token == '*':
                stack.push(a * b)
            elif token == '/':
                stack.push(a / b)
    return stack.pop()

postfix_tests = ["5 3 +", "10 2 /", "4 5 * 3 +", "8 2 3 * +"]
for expr in postfix_tests:
    print(f"  '{expr}' = {evaluate_postfix(expr)}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Stack.py
# =============================================================================
#
# ==================================================
#     STACK DEMO
# ==================================================
#
# [1] Basic stack operations
#   After pushing 10, 20, 30: Stack([10, 20, 30])
#   peek(): 30
#   pop(): 30
#   After pop: Stack([10, 20])
#
# [2] Practical: Balanced parentheses checker
#   Classic stack interview question -- I see this constantly in
#   interview prep material, so wanted to actually implement it.
#   '(a + b) * (c - d)' -> Balanced: True
#   '{[()]}' -> Balanced: True
#   '(a + b]' -> Balanced: False
#   '((a + b)' -> Balanced: False
#   '[{()}]' -> Balanced: True
#
# [3] Practical: Reverse a string using a stack
#   reverse_string_stack('Pavan'): navaP
#
# [4] Practical: Postfix (Reverse Polish Notation) evaluation
#   '5 3 +' = 8
#   '10 2 /' = 5.0
#   '4 5 * 3 +' = 23
#   '8 2 3 * +' = 14
#
# ==================================================
#
# =============================================================================

