# =============================================================================
# inventory_management.py
# Project : 06 - Inventory Management System
# Author  : Pavan Shetty H S
# Date    : September 2024
# =============================================================================
#
# Notes from Pavan:
# Modeled this after a small electronics shop scenario (relevant to my
# embedded systems interest -- imagining tracking component stock:
# resistors, ICs, sensors). Added low-stock alerts after realizing a
# REAL inventory system needs to proactively warn about reordering, not
# just passively report current counts.
# =============================================================================

import sqlite3
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "inventory.db")


class InventoryError(Exception):
    pass

class ItemNotFoundError(InventoryError):
    pass

class InsufficientStockError(InventoryError):
    pass


class Inventory:
    def __init__(self, db_path=DB_PATH):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER NOT NULL DEFAULT 0,
                unit_price REAL NOT NULL,
                reorder_level INTEGER DEFAULT 10
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                change_type TEXT NOT NULL,
                quantity_change INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (item_id) REFERENCES items(item_id)
            )
        """)
        self.connection.commit()

    def add_item(self, name, category, quantity, unit_price, reorder_level=10):
        self.cursor.execute(
            "INSERT INTO items (name, category, quantity, unit_price, reorder_level) VALUES (?, ?, ?, ?, ?)",
            (name, category, quantity, unit_price, reorder_level)
        )
        self.connection.commit()
        item_id = self.cursor.lastrowid
        self._log(item_id, "INITIAL_STOCK", quantity)
        return item_id

    def restock(self, item_id, quantity):
        item = self._get_item(item_id)
        new_qty = item[3] + quantity
        self.cursor.execute("UPDATE items SET quantity = ? WHERE item_id = ?", (new_qty, item_id))
        self.connection.commit()
        self._log(item_id, "RESTOCK", quantity)
        return new_qty

    def sell_item(self, item_id, quantity):
        item = self._get_item(item_id)
        if item[3] < quantity:
            raise InsufficientStockError(
                f"Only {item[3]} units of '{item[1]}' available, requested {quantity}"
            )
        new_qty = item[3] - quantity
        self.cursor.execute("UPDATE items SET quantity = ? WHERE item_id = ?", (new_qty, item_id))
        self.connection.commit()
        self._log(item_id, "SALE", -quantity)
        return new_qty

    def _get_item(self, item_id):
        self.cursor.execute("SELECT * FROM items WHERE item_id = ?", (item_id,))
        item = self.cursor.fetchone()
        if not item:
            raise ItemNotFoundError(f"Item ID {item_id} not found")
        return item

    def low_stock_report(self):
        self.cursor.execute("SELECT * FROM items WHERE quantity <= reorder_level")
        return self.cursor.fetchall()

    def view_all_items(self):
        self.cursor.execute("SELECT * FROM items ORDER BY name")
        return self.cursor.fetchall()

    def search_item(self, keyword):
        self.cursor.execute(
            "SELECT * FROM items WHERE name LIKE ? OR category LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        )
        return self.cursor.fetchall()

    def inventory_value(self):
        self.cursor.execute("SELECT SUM(quantity * unit_price) FROM items")
        return self.cursor.fetchone()[0] or 0

    def _log(self, item_id, change_type, quantity_change):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO stock_log (item_id, change_type, quantity_change, timestamp) VALUES (?, ?, ?, ?)",
            (item_id, change_type, quantity_change, timestamp)
        )
        self.connection.commit()

    def close(self):
        self.connection.close()


def print_menu():
    print("\n" + "=" * 42)
    print("       INVENTORY MANAGEMENT SYSTEM")
    print("=" * 42)
    print(" 1. Add New Item")
    print(" 2. Restock Item")
    print(" 3. Sell/Issue Item")
    print(" 4. Search Item")
    print(" 5. View All Items")
    print(" 6. Low Stock Report")
    print(" 7. Total Inventory Value")
    print(" 8. Exit")


def main():
    inv = Inventory()
    while True:
        print_menu()
        choice = input("\nEnter Choice: ").strip()
        try:
            if choice == "1":
                name = input("Item Name: ")
                category = input("Category: ")
                qty = int(input("Initial Quantity: "))
                price = float(input("Unit Price: "))
                reorder = int(input("Reorder Level (default 10): ") or 10)
                item_id = inv.add_item(name, category, qty, price, reorder)
                print(f"\n✓ Item added with ID {item_id}")

            elif choice == "2":
                item_id = int(input("Item ID: "))
                qty = int(input("Quantity to add: "))
                new_qty = inv.restock(item_id, qty)
                print(f"\n✓ Restocked! New quantity: {new_qty}")

            elif choice == "3":
                item_id = int(input("Item ID: "))
                qty = int(input("Quantity to sell: "))
                new_qty = inv.sell_item(item_id, qty)
                print(f"\n✓ Sale recorded! Remaining quantity: {new_qty}")

            elif choice == "4":
                keyword = input("Search keyword: ")
                results = inv.search_item(keyword)
                print(f"\nFound {len(results)} item(s):")
                for i in results:
                    print(f"  [{i[0]}] {i[1]} ({i[2]}) - Qty: {i[3]}, Price: Rs.{i[4]:.2f}")

            elif choice == "5":
                items = inv.view_all_items()
                print(f"\n  {'ID':4}{'Name':20}{'Category':15}{'Qty':6}{'Price':10}")
                print("  " + "-" * 55)
                for i in items:
                    flag = " ⚠ LOW" if i[3] <= i[5] else ""
                    print(f"  {i[0]:<4}{i[1]:<20}{i[2]:<15}{i[3]:<6}Rs.{i[4]:<8.2f}{flag}")

            elif choice == "6":
                low_items = inv.low_stock_report()
                if low_items:
                    print(f"\n⚠ {len(low_items)} item(s) at or below reorder level:")
                    for i in low_items:
                        print(f"  [{i[0]}] {i[1]} - Current: {i[3]}, Reorder Level: {i[5]}")
                else:
                    print("\n✓ All items adequately stocked.")

            elif choice == "7":
                value = inv.inventory_value()
                print(f"\n  Total Inventory Value: Rs.{value:,.2f}")

            elif choice == "8":
                print("\nInventory session closed. Goodbye!")
                inv.close()
                break
            else:
                print("✗ Invalid choice.")
        except InventoryError as e:
            print(f"\n✗ {type(e).__name__}: {e}")
        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")


if __name__ == "__main__":
    main()

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 inventory_management.py
# =============================================================================
#
#
# ==========================================
#        INVENTORY MANAGEMENT SYSTEM
# ==========================================
#  1. Add New Item
#  2. Restock Item
#  3. Sell/Issue Item
#  4. Search Item
#  5. View All Items
#  6. Low Stock Report
#  7. Total Inventory Value
#  8. Exit
#
# Enter Choice: Item Name: Category: Initial Quantity: Unit Price: Reorder Level (default 10): 
# ✓ Item added with ID 1
#
# ==========================================
#        INVENTORY MANAGEMENT SYSTEM
# ==========================================
#  1. Add New Item
#  2. Restock Item
#  3. Sell/Issue Item
#  4. Search Item
#  5. View All Items
#  6. Low Stock Report
#  7. Total Inventory Value
#  8. Exit
#
# Enter Choice: Item Name: Category: Initial Quantity: Unit Price: Reorder Level (default 10): 
# ✓ Item added with ID 2
#
# ==========================================
#        INVENTORY MANAGEMENT SYSTEM
# ==========================================
#  1. Add New Item
#  2. Restock Item
#  3. Sell/Issue Item
#  4. Search Item
#  5. View All Items
#  6. Low Stock Report
#  7. Total Inventory Value
#  8. Exit
#
# Enter Choice: Item Name: Category: Initial Quantity: Unit Price: Reorder Level (default 10): 
# ✓ Item added with ID 3
#
# ==========================================
#        INVENTORY MANAGEMENT SYSTEM
# ==========================================
#  1. Add New Item
#  2. Restock Item
#  3. Sell/Issue Item
#  4. Search Item
#  5. View All Items
#  6. Low Stock Report
#  7. Total Inventory Value
#  8. Exit
#
# Enter Choice: 
#   ID  Name                Category       Qty   Price     
#   -------------------------------------------------------
#   1   Arduino Uno R3      Microcontroller25    Rs.650.00  
#   2   ESP32 Dev Board     WiFi Module    20    Rs.750.00  
#   3   L298N Motor Driver  Motor Driver   3     Rs.180.00   ⚠ LOW
#
# ==========================================
#        INVENTORY MANAGEMENT SYSTEM
# ==========================================
#  1. Add New Item
#  2. Restock Item
#  3. Sell/Issue Item
#  4. Search Item
#  5. View All Items
#  6. Low Stock Report
#  7. Total Inventory Value
#  8. Exit
#
# Enter Choice: 
# ⚠ 1 item(s) at or below reorder level:
#   [3] L298N Motor Driver - Current: 3, Reorder Level: 5
#
# ==========================================
#        INVENTORY MANAGEMENT SYSTEM
# ==========================================
#  1. Add New Item
#  2. Restock Item
#  3. Sell/Issue Item
#  4. Search Item
#  5. View All Items
#  6. Low Stock Report
#  7. Total Inventory Value
#  8. Exit
#
# Enter Choice: Item ID: Quantity to sell: 
# ✓ Sale recorded! Remaining quantity: 20
#
# ==========================================
#        INVENTORY MANAGEMENT SYSTEM
# ==========================================
#  1. Add New Item
#  2. Restock Item
#  3. Sell/Issue Item
#  4. Search Item
#  5. View All Items
#  6. Low Stock Report
#  7. Total Inventory Value
#  8. Exit
#
# Enter Choice: Item ID: Quantity to add: 
# ✓ Restocked! New quantity: 23
#
# ==========================================
#        INVENTORY MANAGEMENT SYSTEM
# ==========================================
#  1. Add New Item
#  2. Restock Item
#  3. Sell/Issue Item
#  4. Search Item
#  5. View All Items
#  6. Low Stock Report
#  7. Total Inventory Value
#  8. Exit
#
# Enter Choice: Search keyword: 
# Found 1 item(s):
#   [3] L298N Motor Driver (Motor Driver) - Qty: 23, Price: Rs.180.00
#
# ==========================================
#        INVENTORY MANAGEMENT SYSTEM
# ==========================================
#  1. Add New Item
#  2. Restock Item
#  3. Sell/Issue Item
#  4. Search Item
#  5. View All Items
#  6. Low Stock Report
#  7. Total Inventory Value
#  8. Exit
#
# Enter Choice: 
#   Total Inventory Value: Rs.32,140.00
#
# ==========================================
#        INVENTORY MANAGEMENT SYSTEM
# ==========================================
#  1. Add New Item
#  2. Restock Item
#  3. Sell/Issue Item
#  4. Search Item
#  5. View All Items
#  6. Low Stock Report
#  7. Total Inventory Value
#  8. Exit
#
# Enter Choice: 
#   ID  Name                Category       Qty   Price     
#   -------------------------------------------------------
#   1   Arduino Uno R3      Microcontroller20    Rs.650.00  
#   2   ESP32 Dev Board     WiFi Module    20    Rs.750.00  
#   3   L298N Motor Driver  Motor Driver   23    Rs.180.00  
#
# ==========================================
#        INVENTORY MANAGEMENT SYSTEM
# ==========================================
#  1. Add New Item
#  2. Restock Item
#  3. Sell/Issue Item
#  4. Search Item
#  5. View All Items
#  6. Low Stock Report
#  7. Total Inventory Value
#  8. Exit
#
# Enter Choice: 
# Inventory session closed. Goodbye!
#
# =============================================================================

