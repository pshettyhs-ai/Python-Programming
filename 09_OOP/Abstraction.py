# =============================================================================
# Abstraction.py
# Author  : Pavan Shetty H S
# Date    : May 2024
# Topic   : Abstraction -- abstract base classes, abstractmethod
# =============================================================================
#
# Notes from Pavan:
# Abstraction was the OOP concept that took me longest to see the POINT
# of, separate from inheritance. My early confusion: "isn't this just
# inheritance again?" The distinction clicked once I understood:
# abstraction is about FORCING subclasses to implement certain methods,
# and preventing the base class itself from being instantiated directly.
# It's a CONTRACT, not just code reuse.
# =============================================================================

from abc import ABC, abstractmethod

print("=" * 50)
print("    ABSTRACTION DEMO")
print("=" * 50)

# ---------------------
# Abstract Base Class using ABC module
# ---------------------
print("\n[1] Abstract Base Class -- enforcing a contract")

class PaymentMethod(ABC):
    """Abstract base class -- defines WHAT subclasses must implement,
    not HOW. Cannot be instantiated directly."""

    @abstractmethod
    def process_payment(self, amount):
        """Every payment method MUST implement this."""
        pass

    @abstractmethod
    def get_payment_details(self):
        """Every payment method MUST implement this too."""
        pass

    def print_receipt(self, amount):
        # This is a CONCRETE method -- shared by all subclasses, not abstract
        print(f"  Receipt: Rs.{amount} processed via {self.get_payment_details()}")

# ---------------------
# Trying to instantiate the abstract class directly -- fails!
# ---------------------
print("\n[2] Attempting to instantiate abstract class directly")
try:
    pm = PaymentMethod()
except TypeError as e:
    print(f"  Caught error: {e}")
    print("  This is the WHOLE POINT of abstraction -- you CANNOT create")
    print("  a 'generic payment method', only specific implementations.")

# ---------------------
# Concrete subclasses MUST implement all abstract methods
# ---------------------
print("\n[3] Concrete implementations")

class CreditCardPayment(PaymentMethod):
    def __init__(self, card_number):
        self.card_number = card_number

    def process_payment(self, amount):
        print(f"  Processing Rs.{amount} via Credit Card ending in {self.card_number[-4:]}")
        return True

    def get_payment_details(self):
        return f"Credit Card (***{self.card_number[-4:]})"

class UPIPayment(PaymentMethod):
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def process_payment(self, amount):
        print(f"  Processing Rs.{amount} via UPI ({self.upi_id})")
        return True

    def get_payment_details(self):
        return f"UPI ({self.upi_id})"

cc = CreditCardPayment("4532123456789012")
upi = UPIPayment("pavan@okhdfcbank")

cc.process_payment(1500)
cc.print_receipt(1500)   # inherited concrete method, works automatically

print()
upi.process_payment(750)
upi.print_receipt(750)

# ---------------------
# What happens if a subclass FORGETS to implement an abstract method
# ---------------------
print("\n[4] What happens if a subclass forgets an abstract method")
print("""
  class IncompletePayment(PaymentMethod):
      def process_payment(self, amount):
          pass
      # Forgot to implement get_payment_details()!

  incomplete = IncompletePayment()
  # This raises:
  # TypeError: Can't instantiate abstract class IncompletePayment with
  # abstract method get_payment_details
""")
print("  This 'forces' me to actually implement everything the base class")
print("  demands -- Python catches this at INSTANTIATION time, not later")
print("  when I accidentally call the missing method. Caught a bug exactly")
print("  like this while building the Employee Management project later --")
print("  forgot to implement calculate_bonus() in a subclass and Python")
print("  refused to let me even create the object, which was actually")
print("  helpful instead of annoying.")

# ---------------------
# Polymorphism + Abstraction working together
# ---------------------
print("\n[5] Abstraction enables clean polymorphism")
payments = [cc, upi]
total = 0
for p in payments:
    p.process_payment(500)
    total += 500
print(f"  Processed {len(payments)} payments via different methods, total Rs.{total}")
print("  Each object knows HOW to process itself -- I don't need if/elif")
print("  chains checking 'if type is CreditCard, do X, elif UPI, do Y'")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Abstraction.py
# =============================================================================
#
# ==================================================
#     ABSTRACTION DEMO
# ==================================================
#
# [1] Abstract Base Class -- enforcing a contract
#
# [2] Attempting to instantiate abstract class directly
#   Caught error: Can't instantiate abstract class PaymentMethod without an implementation for abstract methods 'get_payment_details', 'process_payment'
#   This is the WHOLE POINT of abstraction -- you CANNOT create
#   a 'generic payment method', only specific implementations.
#
# [3] Concrete implementations
#   Processing Rs.1500 via Credit Card ending in 9012
#   Receipt: Rs.1500 processed via Credit Card (***9012)
#
#   Processing Rs.750 via UPI (pavan@okhdfcbank)
#   Receipt: Rs.750 processed via UPI (pavan@okhdfcbank)
#
# [4] What happens if a subclass forgets an abstract method
#
#   class IncompletePayment(PaymentMethod):
#       def process_payment(self, amount):
#           pass
#       # Forgot to implement get_payment_details()!
#
#   incomplete = IncompletePayment()
#   # This raises:
#   # TypeError: Can't instantiate abstract class IncompletePayment with
#   # abstract method get_payment_details
#
#   This 'forces' me to actually implement everything the base class
#   demands -- Python catches this at INSTANTIATION time, not later
#   when I accidentally call the missing method. Caught a bug exactly
#   like this while building the Employee Management project later --
#   forgot to implement calculate_bonus() in a subclass and Python
#   refused to let me even create the object, which was actually
#   helpful instead of annoying.
#
# [5] Abstraction enables clean polymorphism
#   Processing Rs.500 via Credit Card ending in 9012
#   Processing Rs.500 via UPI (pavan@okhdfcbank)
#   Processed 2 payments via different methods, total Rs.1000
#   Each object knows HOW to process itself -- I don't need if/elif
#   chains checking 'if type is CreditCard, do X, elif UPI, do Y'
#
# ==================================================
#
# =============================================================================

