# =============================================================================
# bank_management.py
# Project : 03 - Bank Management System
# Author  : Pavan Shetty H S
# Date    : August 2024
# =============================================================================
#
# Notes from Pavan:
# This project is where everything from the OOP module finally came
# together for real -- encapsulation (private balance), abstraction
# (BankAccount base class), inheritance (account types), and custom
# exceptions (Module 8) all combined. Rewrote the class hierarchy THREE
# times during the OOP module while learning; this is the final version
# I'm actually using.
# =============================================================================

import sqlite3
import os
import datetime
from abc import ABC, abstractmethod

DB_PATH = os.path.join(os.path.dirname(__file__), "bank.db")


# ---------------------
# Custom exceptions -- distinguishing different failure types
# ---------------------
class BankError(Exception):
    """Base exception for all bank-related errors."""
    pass

class InsufficientFundsError(BankError):
    pass

class AccountNotFoundError(BankError):
    pass

class InvalidAmountError(BankError):
    pass


# ---------------------
# Abstract base class -- enforces a contract for account types
# ---------------------
class BankAccount(ABC):
    def __init__(self, account_number, holder_name, balance=0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.__balance = balance   # private (name-mangled), accessed via property

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        if amount > self.__balance:
            raise InsufficientFundsError(
                f"Insufficient funds. Available: Rs.{self.__balance:.2f}, Requested: Rs.{amount:.2f}"
            )
        self.__balance -= amount
        return self.__balance

    @abstractmethod
    def calculate_interest(self):
        """Every account type MUST define its own interest calculation."""
        pass

    @abstractmethod
    def account_type(self):
        pass


class SavingsAccount(BankAccount):
    INTEREST_RATE = 0.04   # 4% annual

    def calculate_interest(self):
        return self.balance * self.INTEREST_RATE

    def account_type(self):
        return "Savings"


class CurrentAccount(BankAccount):
    def calculate_interest(self):
        return 0   # current accounts typically don't earn interest

    def account_type(self):
        return "Current"


# ---------------------
# Bank class -- manages all accounts, persists to SQLite
# ---------------------
class Bank:
    def __init__(self, db_path=DB_PATH):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_number TEXT PRIMARY KEY,
                holder_name TEXT NOT NULL,
                account_type TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT NOT NULL,
                txn_type TEXT NOT NULL,
                amount REAL NOT NULL,
                balance_after REAL NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (account_number) REFERENCES accounts(account_number)
            )
        """)
        self.connection.commit()

    def create_account(self, account_number, holder_name, account_type, initial_deposit=0):
        self.cursor.execute(
            "INSERT INTO accounts (account_number, holder_name, account_type, balance) VALUES (?, ?, ?, ?)",
            (account_number, holder_name, account_type, initial_deposit)
        )
        self.connection.commit()
        if initial_deposit > 0:
            self._log_transaction(account_number, "OPENING_DEPOSIT", initial_deposit, initial_deposit)

    def get_account(self, account_number):
        self.cursor.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,))
        row = self.cursor.fetchone()
        if not row:
            raise AccountNotFoundError(f"Account {account_number} not found.")
        return row   # (account_number, holder_name, account_type, balance)

    def deposit(self, account_number, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        account = self.get_account(account_number)
        new_balance = account[3] + amount
        self.cursor.execute(
            "UPDATE accounts SET balance = ? WHERE account_number = ?",
            (new_balance, account_number)
        )
        self.connection.commit()
        self._log_transaction(account_number, "DEPOSIT", amount, new_balance)
        return new_balance

    def withdraw(self, account_number, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        account = self.get_account(account_number)
        if amount > account[3]:
            raise InsufficientFundsError(
                f"Insufficient funds. Available: Rs.{account[3]:.2f}"
            )
        new_balance = account[3] - amount
        self.cursor.execute(
            "UPDATE accounts SET balance = ? WHERE account_number = ?",
            (new_balance, account_number)
        )
        self.connection.commit()
        self._log_transaction(account_number, "WITHDRAW", amount, new_balance)
        return new_balance

    def transfer(self, from_account, to_account, amount):
        """Transfer between accounts -- uses a transaction so a failure
        partway through doesn't leave money 'missing' from the system.
        This is the exact lesson from Module 11's transaction notes,
        applied for real here."""
        try:
            self.withdraw(from_account, amount)
            self.deposit(to_account, amount)
            return True
        except BankError:
            self.connection.rollback()
            raise

    def mini_statement(self, account_number, limit=5):
        self.cursor.execute(
            "SELECT * FROM transactions WHERE account_number = ? ORDER BY txn_id DESC LIMIT ?",
            (account_number, limit)
        )
        return self.cursor.fetchall()

    def close_account(self, account_number):
        account = self.get_account(account_number)
        if account[3] > 0:
            raise BankError(f"Cannot close account with remaining balance Rs.{account[3]:.2f}. Withdraw first.")
        self.cursor.execute("DELETE FROM accounts WHERE account_number = ?", (account_number,))
        self.connection.commit()

    def _log_transaction(self, account_number, txn_type, amount, balance_after):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO transactions (account_number, txn_type, amount, balance_after, timestamp) VALUES (?, ?, ?, ?, ?)",
            (account_number, txn_type, amount, balance_after, timestamp)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()


def print_header():
    print("\n" + "=" * 42)
    print("        BANK MANAGEMENT SYSTEM")
    print("        SecureBank Pvt. Ltd.")
    print("=" * 42)


def print_menu():
    print("\n 1. Create New Account")
    print(" 2. Deposit Money")
    print(" 3. Withdraw Money")
    print(" 4. Check Balance")
    print(" 5. Transfer Funds")
    print(" 6. Mini Statement")
    print(" 7. Close Account")
    print(" 8. Exit")


def main():
    bank = Bank()
    print_header()

    while True:
        print_menu()
        choice = input("\nEnter Choice: ").strip()

        try:
            if choice == "1":
                acc_num = input("\nAccount Number (e.g. ACC-20240015): ")
                name = input("Account Holder Name: ")
                acc_type = input("Account Type (Savings/Current): ").strip().capitalize()
                deposit = float(input("Initial Deposit: ") or 0)
                bank.create_account(acc_num, name, acc_type, deposit)
                print(f"\n✓ Account {acc_num} created successfully for {name}")

            elif choice == "2":
                acc_num = input("\nAccount Number: ")
                amount = float(input("Enter Amount: "))
                new_balance = bank.deposit(acc_num, amount)
                account = bank.get_account(acc_num)
                print(f"\n-------- DEPOSIT RECEIPT --------")
                print(f"Account  : {acc_num}")
                print(f"Name     : {account[1]}")
                print(f"Amount   : Rs.{amount:,.2f}")
                print(f"Balance  : Rs.{new_balance:,.2f}")
                print(f"Date     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("----------------------------------")
                print("✓ Deposit Successful!")

            elif choice == "3":
                acc_num = input("\nAccount Number: ")
                amount = float(input("Enter Amount: "))
                new_balance = bank.withdraw(acc_num, amount)
                print(f"\n✓ Withdrawal Successful! New Balance: Rs.{new_balance:,.2f}")

            elif choice == "4":
                acc_num = input("\nAccount Number: ")
                account = bank.get_account(acc_num)
                print(f"\n  Holder  : {account[1]}")
                print(f"  Type    : {account[2]}")
                print(f"  Balance : Rs.{account[3]:,.2f}")

            elif choice == "5":
                from_acc = input("\nFrom Account: ")
                to_acc = input("To Account: ")
                amount = float(input("Amount: "))
                bank.transfer(from_acc, to_acc, amount)
                print(f"\n✓ Transferred Rs.{amount:,.2f} from {from_acc} to {to_acc}")

            elif choice == "6":
                acc_num = input("\nAccount Number: ")
                txns = bank.mini_statement(acc_num)
                print(f"\n----- LAST {len(txns)} TRANSACTIONS -----")
                for t in txns:
                    print(f"  {t[5]} | {t[2]:12} | Rs.{t[3]:>10,.2f} | Balance: Rs.{t[4]:,.2f}")

            elif choice == "7":
                acc_num = input("\nAccount Number to close: ")
                bank.close_account(acc_num)
                print(f"\n✓ Account {acc_num} closed successfully.")

            elif choice == "8":
                print("\nThank you for banking with us!")
                bank.close()
                break

            else:
                print("✗ Invalid choice.")

        except BankError as e:
            print(f"\n✗ {type(e).__name__}: {e}")
        except sqlite3.IntegrityError:
            print("\n✗ Account number already exists.")
        except ValueError:
            print("\n✗ Invalid input format.")


if __name__ == "__main__":
    main()

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 bank_management.py
# =============================================================================
#
#
# ==========================================
#         BANK MANAGEMENT SYSTEM
#         SecureBank Pvt. Ltd.
# ==========================================
#
#  1. Create New Account
#  2. Deposit Money
#  3. Withdraw Money
#  4. Check Balance
#  5. Transfer Funds
#  6. Mini Statement
#  7. Close Account
#  8. Exit
#
# Enter Choice: 
# Account Number (e.g. ACC-20240015): Account Holder Name: Account Type (Savings/Current): Initial Deposit: 
# ✓ Account ACC-20240015 created successfully for Pavan Shetty H S
#
#  1. Create New Account
#  2. Deposit Money
#  3. Withdraw Money
#  4. Check Balance
#  5. Transfer Funds
#  6. Mini Statement
#  7. Close Account
#  8. Exit
#
# Enter Choice: 
# Account Number (e.g. ACC-20240015): Account Holder Name: Account Type (Savings/Current): Initial Deposit: 
# ✓ Account ACC-20240016 created successfully for Rahul Kumar
#
#  1. Create New Account
#  2. Deposit Money
#  3. Withdraw Money
#  4. Check Balance
#  5. Transfer Funds
#  6. Mini Statement
#  7. Close Account
#  8. Exit
#
# Enter Choice: 
# Account Number (e.g. ACC-20240015): Account Holder Name: Account Type (Savings/Current): Initial Deposit: 
# ✓ Account ACC-20240017 created successfully for Priya Singh
#
#  1. Create New Account
#  2. Deposit Money
#  3. Withdraw Money
#  4. Check Balance
#  5. Transfer Funds
#  6. Mini Statement
#  7. Close Account
#  8. Exit
#
# Enter Choice: 
# Account Number: 
#   Holder  : Pavan Shetty H S
#   Type    : Savings
#   Balance : Rs.25,000.00
#
#  1. Create New Account
#  2. Deposit Money
#  3. Withdraw Money
#  4. Check Balance
#  5. Transfer Funds
#  6. Mini Statement
#  7. Close Account
#  8. Exit
#
# Enter Choice: 
# Account Number: Enter Amount: 
# -------- DEPOSIT RECEIPT --------
# Account  : ACC-20240015
# Name     : Pavan Shetty H S
# Amount   : Rs.5,000.00
# Balance  : Rs.30,000.00
# Date     : 2026-06-21 07:14:46
# ----------------------------------
# ✓ Deposit Successful!
#
#  1. Create New Account
#  2. Deposit Money
#  3. Withdraw Money
#  4. Check Balance
#  5. Transfer Funds
#  6. Mini Statement
#  7. Close Account
#  8. Exit
#
# Enter Choice: 
# Account Number: Enter Amount: 
# ✓ Withdrawal Successful! New Balance: Rs.13,000.00
#
#  1. Create New Account
#  2. Deposit Money
#  3. Withdraw Money
#  4. Check Balance
#  5. Transfer Funds
#  6. Mini Statement
#  7. Close Account
#  8. Exit
#
# Enter Choice: 
# From Account: To Account: Amount: 
# ✓ Transferred Rs.1,000.00 from ACC-20240015 to ACC-20240016
#
#  1. Create New Account
#  2. Deposit Money
#  3. Withdraw Money
#  4. Check Balance
#  5. Transfer Funds
#  6. Mini Statement
#  7. Close Account
#  8. Exit
#
# Enter Choice: 
# Account Number: 
# ----- LAST 3 TRANSACTIONS -----
#   2026-06-21 07:14:46 | WITHDRAW     | Rs.  1,000.00 | Balance: Rs.29,000.00
#   2026-06-21 07:14:46 | DEPOSIT      | Rs.  5,000.00 | Balance: Rs.30,000.00
#   2026-06-21 07:14:46 | OPENING_DEPOSIT | Rs. 25,000.00 | Balance: Rs.25,000.00
#
#  1. Create New Account
#  2. Deposit Money
#  3. Withdraw Money
#  4. Check Balance
#  5. Transfer Funds
#  6. Mini Statement
#  7. Close Account
#  8. Exit
#
# Enter Choice: 
# Account Number: Enter Amount: 
# ✓ Withdrawal Successful! New Balance: Rs.0.00
#
#  1. Create New Account
#  2. Deposit Money
#  3. Withdraw Money
#  4. Check Balance
#  5. Transfer Funds
#  6. Mini Statement
#  7. Close Account
#  8. Exit
#
# Enter Choice: 
# Account Number to close: 
# ✓ Account ACC-20240017 closed successfully.
#
#  1. Create New Account
#  2. Deposit Money
#  3. Withdraw Money
#  4. Check Balance
#  5. Transfer Funds
#  6. Mini Statement
#  7. Close Account
#  8. Exit
#
# Enter Choice: 
# Thank you for banking with us!
#
# =============================================================================

