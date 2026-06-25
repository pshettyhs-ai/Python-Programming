# 💰 Project 5: Personal Expense Tracker

**Author:** Pavan Shetty H S
**Built:** August 2024

---

## Project Overview

A genuinely personal-use tool — I built this because I actually wanted to
track my own monthly spending as a student. Unlike Projects 2-4, I
deliberately kept this on a JSON file instead of rewriting it to SQLite,
since the dataset is small and personal and doesn't need complex
filtering/querying beyond what plain Python list comprehensions handle
fine. Good exercise in NOT over-engineering a simple tool.

## Features

- Add expenses with category, description, amount, and date
- View all expenses in a formatted table with running total
- Filter by category or by specific month
- Monthly summary with a visual bar-chart breakdown by category
- Delete individual expense entries
- Persists between runs via a JSON file

## Folder Structure

```
Project05_ExpenseTracker/
├── expense_tracker.py
├── expenses.json   # created on first run
├── README.md
└── requirements.txt
```

## Flowchart

```
   ┌─────────┐
   │  Start    │
   └────┬─────┘
        │
  ┌─────▼──────┐
  │ Load existing │
  │  expenses.json │
  └─────┬──────┘
        │
  ┌─────▼──────┐
  │  Show Menu    │◄───────────┐
  └─────┬──────┘                │
        │                        │
 ┌──────▼────────┐              │
 │Add/View/Filter/ │── loop ─────┘
 │Summary/Delete    │
 └──────┬────────┘
        │ Exit
   ┌────▼────┐
   │   End    │
   └─────────┘
```

## Class Diagram

```
┌───────────────────────────────┐
│         ExpenseTracker             │
├───────────────────────────────┤
│ - data_path: str                     │
│ - expenses: list[dict]                │
├───────────────────────────────┤
│ + add_expense(...)                     │
│ + delete_expense(id)                    │
│ + view_all()                              │
│ + filter_by_category(category)            │
│ + filter_by_month(year, month)             │
│ + total_spent(expenses)                     │
│ + category_breakdown(expenses)               │
│ + highest_expense()                           │
│ - _load()                                       │
│ - _save()                                        │
└───────────────────────────────┘
```

## Algorithm

**Monthly Summary Generation:**
1. Group all expenses by category using `defaultdict`
2. Sum amounts within each category
3. Calculate each category's percentage of total spending
4. Render a simple text-based bar chart proportional to percentage
5. Identify the single highest expense for visibility into big spends

## Requirements

```
# No external packages required for the core tracker
# (PDF export functionality, if added, would require reportlab -- see Module 12)
```

## Installation Steps

```bash
cd 15_Projects/Project05_ExpenseTracker
python expense_tracker.py
```

## Sample Inputs & Outputs

```
==========================================
       PERSONAL EXPENSE TRACKER
       Maintained by Pavan Shetty H S
==========================================
 1. Add Expense
 2. View All Expenses
 3. Filter by Category
 4. Filter by Month
 5. Monthly Summary
 6. Delete Expense
 7. Exit

Enter Choice: 1
Category (Food/Transport/Bills/Education/Other): Food
Description: Groceries
Amount: 2500

✓ Expense added: [1] Food - Rs.2500.00

Enter Choice: 1
Category (Food/Transport/Bills/Education/Other): Transport
Description: Bus pass
Amount: 800

✓ Expense added: [2] Transport - Rs.800.00

Enter Choice: 5

----- MONTHLY SUMMARY -----
  Food            Rs.   2500.00  ███████████████ 75.8%
  Transport       Rs.    800.00  ████ 24.2%

  Total Spending: Rs.3300.00
  Highest single expense: Groceries - Rs.2500.00
```

## Screenshots

> See `/Images/Screenshots/project05_*.png`:
> - `project05_menu.png`
> - `project05_add_expense.png`
> - `project05_view_all.png`
> - `project05_summary_chart.png`
> - `project05_delete.png`

## Learning Outcomes

- Practiced choosing the RIGHT persistence layer for the job — JSON was
  genuinely sufficient here, didn't force SQLite where it wasn't needed
- Used `collections.defaultdict` for clean category aggregation (same
  pattern explored in Module 4's Dictionaries.py)
- Built a simple ASCII bar-chart visualization without any charting
  library, just string multiplication and percentage math
- Reinforced that not every project needs the "more advanced" tool —
  matching tool to problem size is itself a skill

## Future Enhancements

- [ ] PDF monthly report export (Module 12 PDFAutomation.py skills)
- [ ] Email myself the report automatically (Module 12 EmailAutomation.py)
- [ ] Budget limits per category with overspending alerts
- [ ] Year-over-year comparison view
