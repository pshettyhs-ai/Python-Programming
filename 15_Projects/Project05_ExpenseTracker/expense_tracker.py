# =============================================================================
# expense_tracker.py
# Project : 05 - Personal Expense Tracker
# Author  : Pavan Shetty H S
# Date    : August 2024
# =============================================================================
#
# Notes from Pavan:
# Built this one for genuinely PERSONAL use -- I actually wanted a tool
# to track my own monthly spending while a student. Started with a
# simple JSON file (kept it, didn't rewrite to SQLite this time, since
# the data is small and personal, no need for query complexity). Added
# PDF export later using Module 12 skills once I wanted to email myself
# a monthly summary.
# =============================================================================

import json
import os
import datetime
from collections import defaultdict

DATA_PATH = os.path.join(os.path.dirname(__file__), "expenses.json")


class ExpenseTracker:
    def __init__(self, data_path=DATA_PATH):
        self.data_path = data_path
        self.expenses = self._load()

    def _load(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                return json.load(f)
        return []

    def _save(self):
        with open(self.data_path, "w") as f:
            json.dump(self.expenses, f, indent=2)

    def add_expense(self, category, description, amount, date=None):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if date is None:
            date = str(datetime.date.today())
        entry = {
            "id": len(self.expenses) + 1,
            "date": date,
            "category": category,
            "description": description,
            "amount": amount
        }
        self.expenses.append(entry)
        self._save()
        return entry

    def delete_expense(self, expense_id):
        original_len = len(self.expenses)
        self.expenses = [e for e in self.expenses if e["id"] != expense_id]
        self._save()
        return len(self.expenses) < original_len

    def view_all(self):
        return self.expenses

    def filter_by_category(self, category):
        return [e for e in self.expenses if e["category"].lower() == category.lower()]

    def filter_by_month(self, year, month):
        prefix = f"{year}-{month:02d}"
        return [e for e in self.expenses if e["date"].startswith(prefix)]

    def total_spent(self, expenses=None):
        target = expenses if expenses is not None else self.expenses
        return sum(e["amount"] for e in target)

    def category_breakdown(self, expenses=None):
        target = expenses if expenses is not None else self.expenses
        breakdown = defaultdict(float)
        for e in target:
            breakdown[e["category"]] += e["amount"]
        return dict(breakdown)

    def highest_expense(self):
        if not self.expenses:
            return None
        return max(self.expenses, key=lambda e: e["amount"])


def print_menu():
    print("\n" + "=" * 42)
    print("       PERSONAL EXPENSE TRACKER")
    print("       Maintained by Pavan Shetty H S")
    print("=" * 42)
    print(" 1. Add Expense")
    print(" 2. View All Expenses")
    print(" 3. Filter by Category")
    print(" 4. Filter by Month")
    print(" 5. Monthly Summary")
    print(" 6. Delete Expense")
    print(" 7. Exit")


def main():
    tracker = ExpenseTracker()

    while True:
        print_menu()
        choice = input("\nEnter Choice: ").strip()

        try:
            if choice == "1":
                category = input("Category (Food/Transport/Bills/Education/Other): ")
                description = input("Description: ")
                amount = float(input("Amount: "))
                entry = tracker.add_expense(category, description, amount)
                print(f"\n✓ Expense added: [{entry['id']}] {entry['category']} - Rs.{entry['amount']:.2f}")

            elif choice == "2":
                expenses = tracker.view_all()
                if not expenses:
                    print("\n  No expenses recorded yet.")
                else:
                    print(f"\n  {'ID':4}{'Date':12}{'Category':15}{'Description':20}{'Amount':10}")
                    print("  " + "-" * 61)
                    for e in expenses:
                        print(f"  {e['id']:<4}{e['date']:<12}{e['category']:<15}{e['description']:<20}Rs.{e['amount']:.2f}")
                    print(f"\n  Total: Rs.{tracker.total_spent():.2f}")

            elif choice == "3":
                category = input("Enter category: ")
                results = tracker.filter_by_category(category)
                print(f"\n  Found {len(results)} expense(s) in '{category}':")
                for e in results:
                    print(f"    [{e['id']}] {e['date']} - {e['description']}: Rs.{e['amount']:.2f}")
                print(f"\n  Subtotal: Rs.{tracker.total_spent(results):.2f}")

            elif choice == "4":
                year = int(input("Year (e.g. 2024): "))
                month = int(input("Month (1-12): "))
                results = tracker.filter_by_month(year, month)
                print(f"\n  Found {len(results)} expense(s) for {year}-{month:02d}:")
                for e in results:
                    print(f"    [{e['id']}] {e['category']}: Rs.{e['amount']:.2f}")
                print(f"\n  Total for month: Rs.{tracker.total_spent(results):.2f}")

            elif choice == "5":
                breakdown = tracker.category_breakdown()
                total = tracker.total_spent()
                print("\n----- MONTHLY SUMMARY -----")
                for category, amount in sorted(breakdown.items(), key=lambda x: -x[1]):
                    percentage = (amount / total * 100) if total else 0
                    bar = "█" * int(percentage / 5)
                    print(f"  {category:15} Rs.{amount:>10.2f}  {bar} {percentage:.1f}%")
                print(f"\n  Total Spending: Rs.{total:.2f}")
                top = tracker.highest_expense()
                if top:
                    print(f"  Highest single expense: {top['description']} - Rs.{top['amount']:.2f}")

            elif choice == "6":
                expense_id = int(input("Enter expense ID to delete: "))
                if tracker.delete_expense(expense_id):
                    print(f"\n✓ Expense {expense_id} deleted.")
                else:
                    print(f"\n✗ Expense {expense_id} not found.")

            elif choice == "7":
                print("\nKeep tracking, keep saving! Goodbye.")
                break

            else:
                print("✗ Invalid choice.")

        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")


if __name__ == "__main__":
    main()

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 expense_tracker.py
# =============================================================================
#
#
# ==========================================
#        PERSONAL EXPENSE TRACKER
#        Maintained by Pavan Shetty H S
# ==========================================
#  1. Add Expense
#  2. View All Expenses
#  3. Filter by Category
#  4. Filter by Month
#  5. Monthly Summary
#  6. Delete Expense
#  7. Exit
#
# Enter Choice: Category (Food/Transport/Bills/Education/Other): Description: Amount: 
# ✓ Expense added: [1] Food - Rs.2500.00
#
# ==========================================
#        PERSONAL EXPENSE TRACKER
#        Maintained by Pavan Shetty H S
# ==========================================
#  1. Add Expense
#  2. View All Expenses
#  3. Filter by Category
#  4. Filter by Month
#  5. Monthly Summary
#  6. Delete Expense
#  7. Exit
#
# Enter Choice: Category (Food/Transport/Bills/Education/Other): Description: Amount: 
# ✓ Expense added: [2] Transport - Rs.1800.00
#
# ==========================================
#        PERSONAL EXPENSE TRACKER
#        Maintained by Pavan Shetty H S
# ==========================================
#  1. Add Expense
#  2. View All Expenses
#  3. Filter by Category
#  4. Filter by Month
#  5. Monthly Summary
#  6. Delete Expense
#  7. Exit
#
# Enter Choice: Category (Food/Transport/Bills/Education/Other): Description: Amount: 
# ✓ Expense added: [3] Bills - Rs.1200.00
#
# ==========================================
#        PERSONAL EXPENSE TRACKER
#        Maintained by Pavan Shetty H S
# ==========================================
#  1. Add Expense
#  2. View All Expenses
#  3. Filter by Category
#  4. Filter by Month
#  5. Monthly Summary
#  6. Delete Expense
#  7. Exit
#
# Enter Choice: Category (Food/Transport/Bills/Education/Other): Description: Amount: 
# ✓ Expense added: [4] Education - Rs.999.00
#
# ==========================================
#        PERSONAL EXPENSE TRACKER
#        Maintained by Pavan Shetty H S
# ==========================================
#  1. Add Expense
#  2. View All Expenses
#  3. Filter by Category
#  4. Filter by Month
#  5. Monthly Summary
#  6. Delete Expense
#  7. Exit
#
# Enter Choice: 
#   ID  Date        Category       Description         Amount    
#   -------------------------------------------------------------
#   1   2026-06-21  Food           Groceries           Rs.2500.00
#   2   2026-06-21  Transport      Fuel                Rs.1800.00
#   3   2026-06-21  Bills          Electricity         Rs.1200.00
#   4   2026-06-21  Education      Online Course       Rs.999.00
#
#   Total: Rs.6499.00
#
# ==========================================
#        PERSONAL EXPENSE TRACKER
#        Maintained by Pavan Shetty H S
# ==========================================
#  1. Add Expense
#  2. View All Expenses
#  3. Filter by Category
#  4. Filter by Month
#  5. Monthly Summary
#  6. Delete Expense
#  7. Exit
#
# Enter Choice: Enter category: 
#   Found 1 expense(s) in 'Food':
#     [1] 2026-06-21 - Groceries: Rs.2500.00
#
#   Subtotal: Rs.2500.00
#
# ==========================================
#        PERSONAL EXPENSE TRACKER
#        Maintained by Pavan Shetty H S
# ==========================================
#  1. Add Expense
#  2. View All Expenses
#  3. Filter by Category
#  4. Filter by Month
#  5. Monthly Summary
#  6. Delete Expense
#  7. Exit
#
# Enter Choice: Year (e.g. 2024): Month (1-12): 
#   Found 4 expense(s) for 2026-06:
#     [1] Food: Rs.2500.00
#     [2] Transport: Rs.1800.00
#     [3] Bills: Rs.1200.00
#     [4] Education: Rs.999.00
#
#   Total for month: Rs.6499.00
#
# ==========================================
#        PERSONAL EXPENSE TRACKER
#        Maintained by Pavan Shetty H S
# ==========================================
#  1. Add Expense
#  2. View All Expenses
#  3. Filter by Category
#  4. Filter by Month
#  5. Monthly Summary
#  6. Delete Expense
#  7. Exit
#
# Enter Choice: 
# ----- MONTHLY SUMMARY -----
#   Food            Rs.   2500.00  ███████ 38.5%
#   Transport       Rs.   1800.00  █████ 27.7%
#   Bills           Rs.   1200.00  ███ 18.5%
#   Education       Rs.    999.00  ███ 15.4%
#
#   Total Spending: Rs.6499.00
#   Highest single expense: Groceries - Rs.2500.00
#
# ==========================================
#        PERSONAL EXPENSE TRACKER
#        Maintained by Pavan Shetty H S
# ==========================================
#  1. Add Expense
#  2. View All Expenses
#  3. Filter by Category
#  4. Filter by Month
#  5. Monthly Summary
#  6. Delete Expense
#  7. Exit
#
# Enter Choice: Enter expense ID to delete: 
# ✓ Expense 2 deleted.
#
# ==========================================
#        PERSONAL EXPENSE TRACKER
#        Maintained by Pavan Shetty H S
# ==========================================
#  1. Add Expense
#  2. View All Expenses
#  3. Filter by Category
#  4. Filter by Month
#  5. Monthly Summary
#  6. Delete Expense
#  7. Exit
#
# Enter Choice: 
#   ID  Date        Category       Description         Amount    
#   -------------------------------------------------------------
#   1   2026-06-21  Food           Groceries           Rs.2500.00
#   3   2026-06-21  Bills          Electricity         Rs.1200.00
#   4   2026-06-21  Education      Online Course       Rs.999.00
#
#   Total: Rs.4699.00
#
# ==========================================
#        PERSONAL EXPENSE TRACKER
#        Maintained by Pavan Shetty H S
# ==========================================
#  1. Add Expense
#  2. View All Expenses
#  3. Filter by Category
#  4. Filter by Month
#  5. Monthly Summary
#  6. Delete Expense
#  7. Exit
#
# Enter Choice: 
# Keep tracking, keep saving! Goodbye.
#
# =============================================================================

