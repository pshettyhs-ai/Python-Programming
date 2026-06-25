# 📦 Project 6: Inventory Management System

**Author:** Pavan Shetty H S
**Built:** September 2024

---

## Project Overview

Inventory tracking system modeled loosely after a small electronics shop
scenario — relevant to my embedded systems interest, imagining tracking
component stock like resistors, ICs, and sensors. Added proactive
low-stock alerts after realizing a REAL inventory system needs to warn
about reordering rather than just passively reporting current counts on
request.

## Features

- Add new inventory items with category, quantity, price, reorder level
- Restock existing items
- Sell/issue items with stock validation (can't sell more than available)
- Search items by name or category
- View all items with low-stock visual flagging
- Dedicated low-stock report for proactive reordering
- Total inventory value calculation
- Full stock change audit log

## Folder Structure

```
Project06_InventoryManagement/
├── inventory_management.py
├── inventory.db
├── README.md
└── requirements.txt
```

## Flowchart

```
   Sell Item Flow:
   ┌─────────┐
   │ Start    │
   └────┬────┘
        │
  ┌─────▼──────┐
  │ Item exists? │── No ──► ItemNotFoundError
  └─────┬──────┘
        │ Yes
  ┌─────▼───────────┐
  │ Sufficient stock?  │── No ──► InsufficientStockError
  └─────┬───────────┘
        │ Yes
  ┌─────▼──────────┐
  │ Decrement quantity │
  │ Log SALE entry      │
  └─────┬──────────┘
        │
   ┌────▼────┐
   │   End    │
   └─────────┘
```

## Class Diagram

```
┌──────────────────────────────┐
│            Inventory               │
├──────────────────────────────┤
│ - connection, cursor                │
├──────────────────────────────┤
│ + add_item(...)                      │
│ + restock(item_id, quantity)           │
│ + sell_item(item_id, quantity)          │
│ + search_item(keyword)                   │
│ + view_all_items()                        │
│ + low_stock_report()                       │
│ + inventory_value()                         │
│ - _get_item(item_id)                          │
│ - _log(item_id, change_type, qty_change)        │
└──────────────────────────────┘

Exception Hierarchy:
  InventoryError (base)
  ├── ItemNotFoundError
  └── InsufficientStockError
```

## Algorithm

**Low Stock Detection:**
1. Every item has a `reorder_level` threshold set at creation
2. `low_stock_report()` runs a single SQL query:
   `WHERE quantity <= reorder_level`
3. View All Items also flags any item meeting this condition inline
   with a ⚠ marker, so the warning is visible without running a separate
   report

## Requirements

```
# No external packages required -- uses sqlite3, datetime (both built-in)
```

## Installation Steps

```bash
cd 15_Projects/Project06_InventoryManagement
python inventory_management.py
```

## Sample Inputs & Outputs

```
==========================================
       INVENTORY MANAGEMENT SYSTEM
==========================================
 1. Add New Item
 2. Restock Item
 3. Sell/Issue Item
 4. Search Item
 5. View All Items
 6. Low Stock Report
 7. Total Inventory Value
 8. Exit

Enter Choice: 1
Item Name: Arduino Uno R3
Category: Microcontrollers
Initial Quantity: 25
Unit Price: 650
Reorder Level (default 10): 5

✓ Item added with ID 1

Enter Choice: 3
Item ID: 1
Quantity to sell: 22

✓ Sale recorded! Remaining quantity: 3

Enter Choice: 6

⚠ 1 item(s) at or below reorder level:
  [1] Arduino Uno R3 - Current: 3, Reorder Level: 5

Enter Choice: 3
Item ID: 1
Quantity to sell: 100

✗ InsufficientStockError: Only 3 units of 'Arduino Uno R3' available, requested 100
```

## Screenshots

> See `/Images/Screenshots/project06_*.png`:
> - `project06_menu.png`
> - `project06_add_item.png`
> - `project06_low_stock_flag.png`
> - `project06_insufficient_stock_error.png`
> - `project06_total_value.png`

## Learning Outcomes

- Built proactive alerting logic (low stock report), not just passive
  CRUD — a small but meaningful step toward thinking like a real product
  feature, not just a database wrapper
- Maintained a full audit log (stock_log table) of every quantity
  change, useful for later analysis even though I don't have a
  reporting UI for it yet
- Practiced aggregate SQL queries for business metrics (total inventory
  value via SUM(quantity * unit_price))

## Future Enhancements

- [ ] Supplier tracking and automatic reorder request generation
- [ ] Barcode/SKU lookup support
- [ ] Sales trend visualization over time using stock_log history
- [ ] Multi-location/warehouse stock tracking
