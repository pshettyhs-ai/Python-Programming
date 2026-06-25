# =============================================================================
# Encapsulation.py
# Author  : Pavan Shetty H S
# Date    : May 2024
# Topic   : Encapsulation -- private/protected attributes, properties
# =============================================================================
#
# Notes from Pavan:
# This was genuinely confusing at first because Python doesn't have TRUE
# private variables like C++'s private keyword. It's all CONVENTION based
# on underscore prefixes, and Python "trusts" you to respect it. Coming
# from a language with enforced access control, this felt almost
# dangerously loose. Spent time reading WHY Python designed it this way --
# the philosophy is "we're all consenting adults here."
# =============================================================================

print("=" * 50)
print("    ENCAPSULATION DEMO")
print("=" * 50)

# ---------------------
# Public, Protected, Private -- Python's underscore conventions
# ---------------------
print("\n[1] Public vs Protected (_) vs Private (__) attributes")

class BankAccount:
    def __init__(self, account_holder, balance):
        self.account_holder = balance and account_holder   # public
        self.account_holder = account_holder                # public attribute
        self._account_type = "Savings"                       # protected (convention: internal use, subclasses OK)
        self.__balance = balance                              # private (name-mangled)

    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

acc = BankAccount("Pavan Shetty H S", 10000)
print(f"  Public access works fine: acc.account_holder = {acc.account_holder}")
print(f"  Protected (still accessible, but 'shouldn't' be touched directly): {acc._account_type}")

# ---------------------
# The private attribute name mangling surprise
# ---------------------
print("\n[2] Private attribute (__balance) -- name mangling")
try:
    print(acc.__balance)
except AttributeError as e:
    print(f"  Direct access failed: {e}")

print(f"  Using getter method instead: acc.get_balance() = {acc.get_balance()}")

# This actually still works -- Python "private" is just name-mangled,
# not truly enforced. Found this while debugging and was surprised.
print(f"\n  Sneaky access via name mangling: acc._BankAccount__balance = {acc._BankAccount__balance}")
print("""
  My takeaway: Python's "private" with __ is really just a naming
  convention with light enforcement via mangling (renames it to
  _ClassName__attr internally). It discourages accidental access but
  doesn't STOP a determined person. The Python philosophy here is
  trust-based: leading underscore (_) means "internal, please don't
  touch", double underscore (__) means "really internal, mangled to
  avoid subclass naming collisions" -- neither is a hard security
  boundary like C++'s private.
""")

# ---------------------
# Using @property for controlled access (the "Pythonic" way)
# ---------------------
print("[3] Using @property -- the cleaner, Pythonic approach I now prefer")

class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        """Getter -- accessed like an attribute, not a method call."""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Setter -- runs validation before allowing the change."""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is not possible")
        self._celsius = value

    @property
    def fahrenheit(self):
        """Computed property -- not stored, calculated on access."""
        return (self._celsius * 9/5) + 32

temp = Temperature(25)
print(f"  temp.celsius = {temp.celsius}  (looks like attribute access, but it's a method!)")
print(f"  temp.fahrenheit = {temp.fahrenheit}  (computed on the fly)")

temp.celsius = 30   # uses the setter, runs validation
print(f"  After temp.celsius = 30: {temp.celsius}")

try:
    temp.celsius = -300   # should fail validation
except ValueError as e:
    print(f"  Tried setting -300: {e}")

print("""
  Realization: @property lets me write attribute-style syntax
  (obj.value = x) while still running validation logic behind the
  scenes, like a setter method would in Java/C++. This feels like the
  best of both worlds -- clean syntax AND control. This is now my
  default approach whenever I need validated/computed attributes.
""")

print("=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Encapsulation.py
# =============================================================================
#
# ==================================================
#     ENCAPSULATION DEMO
# ==================================================
#
# [1] Public vs Protected (_) vs Private (__) attributes
#   Public access works fine: acc.account_holder = Pavan Shetty H S
#   Protected (still accessible, but 'shouldn't' be touched directly): Savings
#
# [2] Private attribute (__balance) -- name mangling
#   Direct access failed: 'BankAccount' object has no attribute '__balance'
#   Using getter method instead: acc.get_balance() = 10000
#
#   Sneaky access via name mangling: acc._BankAccount__balance = 10000
#
#   My takeaway: Python's "private" with __ is really just a naming
#   convention with light enforcement via mangling (renames it to
#   _ClassName__attr internally). It discourages accidental access but
#   doesn't STOP a determined person. The Python philosophy here is
#   trust-based: leading underscore (_) means "internal, please don't
#   touch", double underscore (__) means "really internal, mangled to
#   avoid subclass naming collisions" -- neither is a hard security
#   boundary like C++'s private.
#
# [3] Using @property -- the cleaner, Pythonic approach I now prefer
#   temp.celsius = 25  (looks like attribute access, but it's a method!)
#   temp.fahrenheit = 77.0  (computed on the fly)
#   After temp.celsius = 30: 30
#   Tried setting -300: Temperature below absolute zero is not possible
#
#   Realization: @property lets me write attribute-style syntax
#   (obj.value = x) while still running validation logic behind the
#   scenes, like a setter method would in Java/C++. This feels like the
#   best of both worlds -- clean syntax AND control. This is now my
#   default approach whenever I need validated/computed attributes.
#
# ==================================================
#
# =============================================================================

