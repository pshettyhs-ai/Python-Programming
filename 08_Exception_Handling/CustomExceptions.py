# =============================================================================
# CustomExceptions.py
# Author  : Pavan Shetty H S
# Date    : April 2024
# Topic   : Creating Custom Exception Classes
# =============================================================================
#
# Notes from Pavan:
# Custom exceptions weren't obviously useful to me at first -- "why not
# just use ValueError for everything?" The answer clicked once I started
# building the Bank Management project later: when I catch exceptions,
# I want to distinguish "insufficient funds" from "invalid account number"
# from "account is frozen" -- they need DIFFERENT handling logic. Generic
# exceptions can't give me that distinction cleanly.
# =============================================================================

print("=" * 50)
print("    CUSTOM EXCEPTIONS DEMO")
print("=" * 50)

# ---------------------
# Basic custom exception -- just inherit from Exception
# ---------------------
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the available balance."""
    pass

class InvalidAccountError(Exception):
    """Raised when an account number doesn't exist."""
    pass

# ---------------------
# Custom exception with extra data attached
# ---------------------
class InsufficientFundsErrorDetailed(Exception):
    """Custom exception that carries extra context data."""
    def __init__(self, balance, requested_amount):
        self.balance = balance
        self.requested_amount = requested_amount
        self.shortfall = requested_amount - balance
        message = (f"Cannot withdraw Rs.{requested_amount}. "
                   f"Available balance is only Rs.{balance} "
                   f"(short by Rs.{self.shortfall})")
        super().__init__(message)   # pass formatted message to base Exception

# ---------------------
# Using basic custom exceptions
# ---------------------
print("\n[1] Basic custom exception usage")

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(f"Cannot withdraw {amount}, balance is {balance}")
    return balance - amount

try:
    withdraw(1000, 5000)
except InsufficientFundsError as e:
    print(f"  Caught: {e}")

# ---------------------
# Using the detailed custom exception with extra attributes
# ---------------------
print("\n[2] Custom exception with attached data")

def withdraw_detailed(balance, amount):
    if amount > balance:
        raise InsufficientFundsErrorDetailed(balance, amount)
    return balance - amount

try:
    withdraw_detailed(1000, 5000)
except InsufficientFundsErrorDetailed as e:
    print(f"  Caught: {e}")
    print(f"  Balance was: {e.balance}")
    print(f"  Shortfall  : {e.shortfall}")

# ---------------------
# Exception hierarchy -- building a family of related custom exceptions
# ---------------------
print("\n[3] Custom exception hierarchy (used in my Bank Management project)")

class BankError(Exception):
    """Base exception for all bank-related errors."""
    pass

class InsufficientFundsBankError(BankError):
    """Specific bank error for insufficient funds."""
    pass

class AccountFrozenError(BankError):
    """Specific bank error for frozen accounts."""
    pass

class InvalidPINError(BankError):
    """Specific bank error for incorrect PIN."""
    pass

def process_transaction(account_status, balance, amount, pin_correct):
    if account_status == "frozen":
        raise AccountFrozenError("This account is frozen. Contact support.")
    if not pin_correct:
        raise InvalidPINError("Incorrect PIN entered.")
    if amount > balance:
        raise InsufficientFundsBankError(f"Insufficient funds. Balance: {balance}")
    return balance - amount

# Testing each scenario
test_cases = [
    ("frozen", 5000, 1000, True),
    ("active", 5000, 1000, False),
    ("active", 500, 1000, True),
    ("active", 5000, 1000, True),
]

for status, bal, amt, pin_ok in test_cases:
    try:
        new_balance = process_transaction(status, bal, amt, pin_ok)
        print(f"  Transaction OK. New balance: {new_balance}")
    except BankError as e:
        # Catching the BASE class catches ALL subclasses too!
        # This is the "aha" moment for why exception hierarchies are useful
        print(f"  {type(e).__name__}: {e}")

# ---------------------
# Re-raising exceptions
# ---------------------
print("\n[4] Re-raising an exception after logging it")

def risky_operation():
    try:
        return 10 / 0
    except ZeroDivisionError as e:
        print(f"  Logging error before re-raising: {e}")
        raise   # re-raises the SAME exception, preserving original traceback

try:
    risky_operation()
except ZeroDivisionError:
    print("  Caught the re-raised exception at the outer level")

# ---------------------
# Chaining exceptions with 'raise ... from'
# ---------------------
print("\n[5] Exception chaining (raise ... from ...)")

def load_config():
    try:
        with open("config_xyz.json") as f:
            pass
    except FileNotFoundError as original_error:
        raise RuntimeError("Could not initialize application") from original_error

try:
    load_config()
except RuntimeError as e:
    print(f"  Caught: {e}")
    print(f"  Original cause: {e.__cause__}")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 CustomExceptions.py
# =============================================================================
#
# ==================================================
#     CUSTOM EXCEPTIONS DEMO
# ==================================================
#
# [1] Basic custom exception usage
#   Caught: Cannot withdraw 5000, balance is 1000
#
# [2] Custom exception with attached data
#   Caught: Cannot withdraw Rs.5000. Available balance is only Rs.1000 (short by Rs.4000)
#   Balance was: 1000
#   Shortfall  : 4000
#
# [3] Custom exception hierarchy (used in my Bank Management project)
#   AccountFrozenError: This account is frozen. Contact support.
#   InvalidPINError: Incorrect PIN entered.
#   InsufficientFundsBankError: Insufficient funds. Balance: 500
#   Transaction OK. New balance: 4000
#
# [4] Re-raising an exception after logging it
#   Logging error before re-raising: division by zero
#   Caught the re-raised exception at the outer level
#
# [5] Exception chaining (raise ... from ...)
#   Caught: Could not initialize application
#   Original cause: [Errno 2] No such file or directory: 'config_xyz.json'
#
# ==================================================
#
# =============================================================================

