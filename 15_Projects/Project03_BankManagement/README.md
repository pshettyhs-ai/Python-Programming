# 🏦 Project 3: Bank Management System

**Author:** Pavan Shetty H S
**Built:** August 2024 (rewrote the class hierarchy 3 times during design)

---

## Project Overview

A console-based banking application supporting account creation,
deposits, withdrawals, transfers, mini statements, and account closure.
This project is where OOP from Module 9 finally came together for real —
encapsulation (private balance with controlled access), abstraction
(BankAccount as an abstract base class), inheritance (Savings/Current
account types), and custom exception hierarchies (Module 8) all combine
here.

I rewrote the class structure three separate times while learning OOP
concepts in Module 9, each time fixing a design flaw I'd recognized:
first draft used a single class with if/elif chains for account-type
behavior; second draft split into subclasses but exposed `balance` as a
raw public attribute (no validation); the final version (used here) has
a private balance with validated deposit/withdraw methods and an
abstract base class forcing every account type to define its own
interest calculation.

## Features

- Create Savings or Current accounts with different interest rules
- Deposit and withdraw with input validation
- Inter-account fund transfers using database transactions (rollback on
  failure, so money never "disappears" if a transfer fails partway through)
- Mini statement showing recent transaction history
- Account closure (blocked if balance isn't zero, to prevent
  accidentally losing funds)
- Custom exception hierarchy for precise error handling

## Folder Structure

```
Project03_BankManagement/
├── bank_management.py   # Main application
├── bank.db                # SQLite database (created on first run)
├── README.md
└── requirements.txt
```

## Flowchart

```
        ┌──────────┐
        │  Start    │
        └────┬─────┘
             │
      ┌──────▼──────┐
      │ Connect to DB │
      │ Create tables  │
      └──────┬──────┘
             │
      ┌──────▼──────┐
      │ Show Menu     │◄─────────────┐
      └──────┬──────┘                │
             │                        │
    ┌────────▼─────────┐             │
    │ Create/Deposit/    │             │
    │ Withdraw/Transfer/  │── loop ────┘
    │ Statement/Close      │
    └────────┬─────────┘
             │ Exit
      ┌──────▼──────┐
      │ Close DB conn │
      └──────┬──────┘
        ┌────▼────┐
        │   End    │
        └─────────┘
```

## Class Diagram

```
┌──────────────────────────┐
│  <<abstract>> BankAccount   │
├──────────────────────────┤
│ - __balance: float (private)│
│ # account_number             │
│ # holder_name                 │
├──────────────────────────┤
│ + balance (property)          │
│ + deposit(amount)              │
│ + withdraw(amount)             │
│ + calculate_interest() *abs*    │
│ + account_type() *abstract*     │
└─────────────┬────────────┘
              │
      ┌───────┴────────┐
      │                  │
┌─────▼──────┐   ┌──────▼──────┐
│SavingsAccount│   │CurrentAccount │
├─────────────┤   ├─────────────┤
│+calculate_   │   │+calculate_    │
│ interest()    │   │ interest()     │
│+account_type()│   │+account_type() │
└─────────────┘   └─────────────┘

┌──────────────────────────────┐
│              Bank                │
├──────────────────────────────┤
│ - connection, cursor               │
├──────────────────────────────┤
│ + create_account(...)              │
│ + deposit(account, amount)          │
│ + withdraw(account, amount)         │
│ + transfer(from, to, amount)        │
│ + mini_statement(account)           │
│ + close_account(account)            │
└──────────────────────────────┘

Exception Hierarchy:
  BankError (base)
  ├── InsufficientFundsError
  ├── AccountNotFoundError
  └── InvalidAmountError
```

## Algorithm

**Transfer Funds (the most complex operation):**
1. Attempt to withdraw amount from source account
2. If withdrawal succeeds, attempt to deposit amount into destination
3. If EITHER step fails, rollback the database transaction so no partial
   transfer occurs (money isn't deducted without being credited
   somewhere)
4. Log both legs of the transaction with timestamps

## Requirements

```
# No external packages required -- uses sqlite3, datetime (both built-in)
```

## Installation Steps

```bash
cd 15_Projects/Project03_BankManagement
python bank_management.py
```

## Execution Guide

```bash
python bank_management.py
```

## Sample Inputs & Outputs

```
==========================================
        BANK MANAGEMENT SYSTEM
        SecureBank Pvt. Ltd.
==========================================

 1. Create New Account
 2. Deposit Money
 3. Withdraw Money
 4. Check Balance
 5. Transfer Funds
 6. Mini Statement
 7. Close Account
 8. Exit

Enter Choice: 1

Account Number (e.g. ACC-20240015): ACC-20240015
Account Holder Name: Pavan Shetty H S
Account Type (Savings/Current): Savings
Initial Deposit: 20000

✓ Account ACC-20240015 created successfully for Pavan Shetty H S

Enter Choice: 2

Account Number: ACC-20240015
Enter Amount: 5000

-------- DEPOSIT RECEIPT --------
Account  : ACC-20240015
Name     : Pavan Shetty H S
Amount   : Rs.5,000.00
Balance  : Rs.25,000.00
Date     : 2024-08-15 14:32:10
----------------------------------
✓ Deposit Successful!

Enter Choice: 3

Account Number: ACC-20240015
Enter Amount: 100000

✗ InsufficientFundsError: Insufficient funds. Available: Rs.25000.00

Enter Choice: 6

Account Number: ACC-20240015

----- LAST 2 TRANSACTIONS -----
  2024-08-15 14:32:10 | DEPOSIT      | Rs.   5,000.00 | Balance: Rs.25,000.00
  2024-08-15 14:30:02 | OPENING_DEPOSIT | Rs.  20,000.00 | Balance: Rs.20,000.00
```

## Screenshots

> See `/Images/Screenshots/project03_*.png`:
> - `project03_menu.png` — main menu
> - `project03_account_created.png` — successful account creation
> - `project03_deposit_receipt.png` — deposit receipt
> - `project03_insufficient_funds.png` — withdrawal error handling
> - `project03_transfer.png` — successful fund transfer

## Learning Outcomes

- Applied abstraction (ABC + abstractmethod) to force every account
  type to implement its own interest logic
- Used encapsulation properly — balance is private, only modifiable
  through validated deposit/withdraw methods
- Implemented a real custom exception hierarchy and saw the value of
  catching the BASE class generically vs specific subclasses precisely
- Applied database transactions (commit/rollback) to a genuinely
  meaningful scenario — fund transfers — where partial failure would be
  a real, serious bug (money disappearing)

## Future Enhancements

- [ ] Add a Fixed Deposit account type with maturity date logic
- [ ] PIN-based authentication before transactions
- [ ] Monthly interest auto-credit via a scheduled job
- [ ] Export full statement to PDF (connects to Module 12's PDF skills)
