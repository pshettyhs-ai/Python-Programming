# 🧮 Project 1: Scientific Calculator Application

**Author:** Pavan Shetty H S
**Built:** August 2024 (weekend project, ~6 hours total across 2 sessions)

---

## Project Overview

My very first "real" project after finishing the foundational modules
(Basics through Functions). What started as a simple 4-operation
calculator grew into a scientific calculator with trigonometry,
logarithms, and a calculation history feature, because I got into a flow
state one Saturday and kept adding capabilities. This is the project
that made Python feel like a tool for BUILDING things rather than just a
language for exercises.

## Features

- Basic arithmetic: addition, subtraction, multiplication, division, modulus
- Power and square root calculations
- Logarithm with custom base support
- Trigonometric functions (sin, cos, tan) with degree input
- Calculation history tracking
- Robust error handling (division by zero, negative square roots, etc.)
- Clean menu-driven CLI interface

## Folder Structure

```
Project01_Calculator/
├── calculator.py       # Main application
├── README.md            # This file
└── requirements.txt      # No external dependencies (uses math module only)
```

## Flowchart

```
        ┌─────────────┐
        │ Start        │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │ Show Menu    │◄────────────────┐
        └──────┬──────┘                  │
               │                          │
        ┌──────▼──────┐                  │
        │ Get Choice   │                  │
        └──────┬──────┘                  │
               │                          │
       ┌───────▼────────┐                │
       │ Choice == Exit? │── No ──────────┘
       └───────┬─────────┘
               │ Yes
        ┌──────▼──────┐
        │   End        │
        └─────────────┘
```

## Class Diagram

```
┌────────────────────────────┐
│         Calculator           │
├────────────────────────────┤
│ - history: list               │
├────────────────────────────┤
│ + add(a, b)                   │
│ + subtract(a, b)               │
│ + multiply(a, b)               │
│ + divide(a, b)                 │
│ + modulus(a, b)                │
│ + power(a, b)                  │
│ + square_root(a)               │
│ + logarithm(a, base)           │
│ + sine(degrees)                │
│ + cosine(degrees)              │
│ + tangent(degrees)             │
│ + show_history()               │
│ - _log(entry)                   │
└────────────────────────────┘
```

## Algorithm

1. Display menu with all available operations
2. Read user's menu choice
3. Based on choice, prompt for required inputs (1 or 2 numbers)
4. Call corresponding Calculator method, wrapped in try/except
5. Log the operation to history
6. Display result
7. Loop back to menu until user chooses Exit

## Requirements

```
# No external packages required -- uses Python's built-in math module
```

## Installation Steps

```bash
# No installation needed beyond Python 3.x itself
cd 15_Projects/Project01_Calculator
python calculator.py
```

## Execution Guide

```bash
python calculator.py
```

Then follow the on-screen menu prompts.

## Sample Inputs & Outputs

```
========================================
     PYTHON SCIENTIFIC CALCULATOR
========================================
 1. Addition          6. Power
 2. Subtraction       7. Square Root
 3. Multiplication    8. Logarithm
 4. Division          9. Trigonometry
 5. Modulus          10. History
                     11. Exit
========================================
Enter choice: 1
Enter first number: 25.5
Enter second number: 14.3
------------------------------------
Result: 25.5 + 14.3 = 39.8
------------------------------------

Enter choice: 7
Enter number: 144
------------------------------------
Result: sqrt(144) = 12.0000
------------------------------------

Enter choice: 4
Enter first number: 10
Enter second number: 0
  Error: Cannot divide by zero

Enter choice: 10
----- CALCULATION HISTORY -----
  1. 25.5 + 14.3 = 39.8
  2. sqrt(144) = 12.0
```

## Screenshots

> See `/Images/Screenshots/project01_*.png` for terminal screenshots:
> - `project01_menu.png` — main menu display
> - `project01_addition.png` — successful addition operation
> - `project01_division_error.png` — division by zero error handling
> - `project01_trig.png` — trigonometric calculation
> - `project01_history.png` — calculation history view

## Learning Outcomes

- First hands-on application of functions and basic exception handling
  in a complete, runnable program
- Understanding menu-driven CLI design patterns
- Practiced input validation and graceful error messages instead of
  letting the program crash on bad input
- Learned to separate LOGIC (the Calculator class) from PRESENTATION
  (the menu loop) — this separation became a recurring design pattern
  in every later project

## Future Enhancements

- [ ] Add support for chained expressions (e.g., "5 + 3 * 2")
- [ ] Save/load history to a file between sessions
- [ ] Add a GUI version using tkinter
- [ ] Support for complex number operations
