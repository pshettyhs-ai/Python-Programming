# =============================================================================
# Constructors.py
# Author  : Pavan Shetty H S
# Date    : May 2024
# Topic   : Constructors (__init__), Destructors (__del__)
# =============================================================================
#
# Notes from Pavan:
# __init__ is NOT technically the constructor in the strictest sense --
# __new__ is what actually CREATES the object, __init__ just INITIALIZES
# it after creation. I only learned this distinction from a StackOverflow
# deep-dive; for 99% of practical purposes you only ever touch __init__.
# =============================================================================

print("=" * 50)
print("    CONSTRUCTORS & DESTRUCTORS DEMO")
print("=" * 50)

# ---------------------
# Basic constructor
# ---------------------
class Account:
    def __init__(self, account_holder, initial_balance=0):
        print(f"  [Constructor called for {account_holder}]")
        self.account_holder = account_holder
        self.balance = initial_balance
        self.account_number = self._generate_account_number()

    def _generate_account_number(self):
        # Simple deterministic generator for demo purposes
        return f"ACC{hash(self.account_holder) % 100000:05d}"

    def __del__(self):
        # Destructor -- called when object is about to be destroyed
        # (garbage collected). I rarely use this in practice; Python's
        # garbage collector handles memory automatically, unlike C where
        # you MUST manually free() everything you malloc(). I mostly
        # learned __del__ exists for completeness, not because I need it
        # often.
        print(f"  [Destructor called for {self.account_holder}'s account]")

print("\n[1] Constructor runs automatically on object creation")
acc1 = Account("Pavan Shetty H S", 5000)
print(f"  Account Number: {acc1.account_number}")
print(f"  Balance: {acc1.balance}")

# ---------------------
# Default parameter values in constructor
# ---------------------
print("\n[2] Default parameter in constructor")
acc2 = Account("Rahul Kumar")   # no initial_balance given, defaults to 0
print(f"  {acc2.account_holder}'s balance: {acc2.balance}")

# ---------------------
# Multiple constructors via classmethod (Python doesn't support
# overloading like C++/Java, this is the workaround I learned)
# ---------------------
print("\n[3] Simulating multiple constructors using @classmethod")

class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_string):
        """Alternative constructor that parses 'DD-MM-YYYY' format.
        This pattern is how Python handles what other languages do with
        constructor overloading."""
        day, month, year = map(int, date_string.split("-"))
        return cls(day, month, year)   # calls __init__ under the hood

    def display(self):
        print(f"  Date: {self.day:02d}/{self.month:02d}/{self.year}")

d1 = Date(15, 8, 2024)            # normal constructor
d2 = Date.from_string("26-01-2024")  # alternative constructor

print("  Created via normal constructor:")
d1.display()
print("  Created via from_string() classmethod:")
d2.display()

# ---------------------
# del keyword vs __del__ method -- distinction I had to look up
# ---------------------
print("\n[4] del keyword vs object destruction")
temp_account = Account("Temporary User", 100)
print("  About to delete reference with 'del'...")
del temp_account
# Note: __del__ may or may not print IMMEDIATELY here depending on
# reference counting and garbage collection timing. This unpredictability
# is exactly why I don't rely on __del__ for critical cleanup logic --
# I use context managers (with statements) instead, which run
# deterministically.

print("\n  My takeaway: I went looking for __del__ expecting it to behave")
print("  like C's free()/destructor calls, predictable and immediate.")
print("  It's NOT reliable for that in Python due to garbage collection")
print("  timing. For deterministic cleanup, use context managers instead.")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Constructors.py
# =============================================================================
#
# ==================================================
#     CONSTRUCTORS & DESTRUCTORS DEMO
# ==================================================
#
# [1] Constructor runs automatically on object creation
#   [Constructor called for Pavan Shetty H S]
#   Account Number: ACC76346
#   Balance: 5000
#
# [2] Default parameter in constructor
#   [Constructor called for Rahul Kumar]
#   Rahul Kumar's balance: 0
#
# [3] Simulating multiple constructors using @classmethod
#   Created via normal constructor:
#   Date: 15/08/2024
#   Created via from_string() classmethod:
#   Date: 26/01/2024
#
# [4] del keyword vs object destruction
#   [Constructor called for Temporary User]
#   About to delete reference with 'del'...
#   [Destructor called for Temporary User's account]
#
#   My takeaway: I went looking for __del__ expecting it to behave
#   like C's free()/destructor calls, predictable and immediate.
#   It's NOT reliable for that in Python due to garbage collection
#   timing. For deterministic cleanup, use context managers instead.
#
# ==================================================
#   [Destructor called for Pavan Shetty H S's account]
#   [Destructor called for Rahul Kumar's account]
#
# =============================================================================

