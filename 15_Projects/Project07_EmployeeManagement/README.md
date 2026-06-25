# 👔 Project 7: Employee Management System

**Author:** Pavan Shetty H S
**Built:** September 2024

---

## Project Overview

An employee database supporting different employee TYPES (Developer,
Manager, Intern) each with different bonus calculation rules, backed by
SQLite, with CSV export capability. This is the project where I
deliberately put Abstraction (Module 9) to a real test — `Employee` is
an abstract base class, and every subclass MUST implement
`calculate_bonus()`.

**A genuine bug story:** while developing this, I forgot to implement
`calculate_bonus()` in an early draft of the `Manager` class. Python
refused to let me even INSTANTIATE the class —
`TypeError: Can't instantiate abstract class Manager with abstract
method calculate_bonus` — catching my mistake immediately at object
creation time instead of failing later when bonus calculation actually
got called somewhere deep in the program. This is the cleanest real-world
demonstration I've had of why abstraction matters beyond being an
academic OOP concept.

## Features

- Three employee types with distinct bonus calculation logic:
  - Developer: 10% of base salary
  - Manager: 15% of base salary + Rs.1000 per team member
  - Intern: no bonus
- Add, view, update salary, and delete employee records
- View all employees with total compensation calculated on the fly
- Export complete employee data (including computed bonus/total) to CSV

## Folder Structure

```
Project07_EmployeeManagement/
├── employee_management.py
├── employees.db
├── README.md
└── requirements.txt
```

## Class Diagram

```
┌──────────────────────────────┐
│      <<abstract>> Employee         │
├──────────────────────────────┤
│ # emp_id, name, department,         │
│   base_salary                        │
├──────────────────────────────┤
│ + total_compensation()                │
│ + calculate_bonus() *abstract*         │
│ + role() *abstract*                     │
└─────────────┬────────────────┘
              │
     ┌────────┼─────────┐
     │        │           │
┌────▼───┐┌───▼────┐ ┌────▼───┐
│Developer││ Manager │ │ Intern  │
├────────┤├────────┤ ├────────┤
│+calc_   ││+team_size│ │+calc_   │
│ bonus()  ││+calc_     │ │ bonus()  │
│+role()   ││ bonus()    │ │+role()   │
│          ││+role()      │ │          │
└────────┘└────────┘ └────────┘

┌──────────────────────────────┐
│       EmployeeDatabase             │
├──────────────────────────────┤
│ + add_employee(employee)            │
│ + get_employee(emp_id)               │
│ + view_all()                          │
│ + update_salary(emp_id, salary)        │
│ + delete_employee(emp_id)               │
│ + export_to_csv(filepath)                │
│ - _row_to_object(row)                      │
└──────────────────────────────┘
```

## Algorithm

**Reconstructing Objects from Database Rows:**
1. SQLite only stores flat data (no native object types)
2. `_row_to_object()` reads the `role` column and reconstructs the
   correct Python subclass (Developer/Manager/Intern) from raw row data
3. This lets polymorphism work correctly even after round-tripping
   through the database — calling `.calculate_bonus()` on a
   reconstructed object still dispatches to the right subclass method

## Requirements

```
# No external packages required -- uses sqlite3, csv, abc (all built-in)
```

## Installation Steps

```bash
cd 15_Projects/Project07_EmployeeManagement
python employee_management.py
```

## Sample Inputs & Outputs

```
==========================================
      EMPLOYEE MANAGEMENT SYSTEM
==========================================
 1. Add Employee
 2. View Employee
 3. View All Employees
 4. Update Salary
 5. Delete Employee
 6. Export to CSV
 7. Exit

Enter Choice: 1
Role (Developer/Manager/Intern): Manager
Employee ID: 501
Name: Pavan Shetty H S
Department: Engineering
Base Salary: 65000
Team Size: 6

✓ Manager Pavan Shetty H S added with Total Compensation: Rs.80,750.00

Enter Choice: 1
Role (Developer/Manager/Intern): Developer
Employee ID: 502
Name: Rahul Kumar
Department: Engineering
Base Salary: 58000

✓ Developer Rahul Kumar added with Total Compensation: Rs.63,800.00

Enter Choice: 3

  ID   Name              Role        Dept        Total Comp
  ------------------------------------------------------------
  501  Pavan Shetty H S  Manager     Engineering Rs.80,750.00
  502  Rahul Kumar       Developer   Engineering Rs.63,800.00

Enter Choice: 6
Export filename (e.g. employees.csv): team_export.csv

✓ Exported to team_export.csv
```

## Screenshots

> See `/Images/Screenshots/project07_*.png`:
> - `project07_menu.png`
> - `project07_add_manager.png`
> - `project07_view_all.png`
> - `project07_csv_export.png`
> - `project07_abstract_class_error.png` — shows the TypeError when
>   abstract methods aren't implemented (captured during development,
>   kept as documentation of the bug)

## Learning Outcomes

- Real-world proof that abstract base classes catch incomplete
  implementations at instantiation time, not at call time — directly
  experienced this as a genuine bug during development, not just read
  about it
- Practiced reconstructing polymorphic objects from flat database rows
  (`_row_to_object`) — a pattern that wasn't obvious to me until I hit
  the need for it directly
- CSV export combining stored data (base_salary) with computed data
  (bonus, total) in the same row

## Future Enhancements

- [ ] Add a Senior Developer tier with different bonus tiers based on
      years of experience
- [ ] Department-wise compensation reports
- [ ] Performance rating integration affecting bonus multiplier
