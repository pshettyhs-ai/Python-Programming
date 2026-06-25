# 📚 Project 4: Library Management System

**Author:** Pavan Shetty H S
**Built:** August 2024

---

## Project Overview

A library system managing books, members, and book loans with due dates
and overdue fine calculation. My first project with genuinely related
multi-table data — books, members, and loans all connected via foreign
keys doing real work, not just declared for show.

## Features

- Add books with multiple copy tracking (total vs available)
- Add members
- Search books by title or author (partial match)
- Issue books with automatic 14-day due date calculation
- Return books with automatic overdue fine calculation (Rs.5/day late)
- View all currently overdue books across all members
- View complete book catalog with availability

## Folder Structure

```
Project04_LibraryManagement/
├── library_management.py
├── library.db
├── README.md
└── requirements.txt
```

## Flowchart

```
   Issue Book Flow:
   ┌─────────┐
   │ Start    │
   └────┬────┘
        │
  ┌─────▼──────┐
  │ Book exists? │── No ──► Error: BookNotFoundError
  └─────┬──────┘
        │ Yes
  ┌─────▼──────────┐
  │ Copies available?│── No ──► Error: BookNotAvailableError
  └─────┬──────────┘
        │ Yes
  ┌─────▼──────┐
  │Member exists?│── No ──► Error: MemberNotFoundError
  └─────┬──────┘
        │ Yes
  ┌─────▼──────────────┐
  │ Create loan record    │
  │ Decrement available    │
  │ Set due_date = +14 days │
  └─────┬──────────────┘
        │
   ┌────▼────┐
   │   End    │
   └─────────┘
```

## Class Diagram

```
┌───────────────────────────────┐
│             Library                │
├───────────────────────────────┤
│ - connection, cursor                │
├───────────────────────────────┤
│ + add_book(...)                      │
│ + add_member(...)                     │
│ + search_books(keyword)               │
│ + issue_book(book_id, member_id)       │
│ + return_book(loan_id)                 │
│ + overdue_books()                       │
│ + view_all_books()                      │
└───────────────────────────────┘

Exception Hierarchy:
  LibraryError (base)
  ├── BookNotAvailableError
  ├── BookNotFoundError
  └── MemberNotFoundError

Tables: books ──< loans >── members  (many-to-many via loans)
```

## Algorithm

**Return Book with Fine Calculation:**
1. Look up the loan record by loan_id
2. Verify it hasn't already been returned
3. Set return_date to today, increment book's available_copies
4. Compare today's date against due_date
5. If overdue: calculate days late × Rs.5, return fine message
6. If on time: return confirmation with no fine

## Requirements

```
# No external packages required -- uses sqlite3, datetime (both built-in)
```

## Installation Steps

```bash
cd 15_Projects/Project04_LibraryManagement
python library_management.py
```

## Sample Inputs & Outputs

```
==========================================
       LIBRARY MANAGEMENT SYSTEM
==========================================
 1. Add Book
 2. Add Member
 3. Search Books
 4. Issue Book
 5. Return Book
 6. View Overdue Books
 7. View All Books
 8. Exit

Enter Choice: 1
Title: Clean Code
Author: Robert C. Martin
ISBN: 9780132350884
Number of copies: 2

✓ Book added with ID 1

Enter Choice: 2
Member Name: Pavan Shetty H S
Email: pavan@example.com

✓ Member added with ID 1

Enter Choice: 4
Book ID: 1
Member ID: 1

✓ Book issued! Due date: 2024-08-29

Enter Choice: 4
Book ID: 1
Member ID: 1

(Issuing the SAME book a second time before the first copy's return,
 with only 1 copy left available, succeeds since 2 copies exist)

✓ Book issued! Due date: 2024-08-29

Enter Choice: 5
Loan ID: 1

✓ Returned on time. No fine.
```

## Screenshots

> See `/Images/Screenshots/project04_*.png`:
> - `project04_menu.png`
> - `project04_add_book.png`
> - `project04_issue_book.png`
> - `project04_overdue.png`
> - `project04_return_with_fine.png`

## Learning Outcomes

- First real multi-table relational design with meaningful foreign keys
- Practiced JOIN queries to combine loan, book, and member data for the
  overdue report (direct application of Module 11's AdvancedQueries.py)
- Date arithmetic using `datetime.timedelta` for due date calculation
- Designed a custom exception hierarchy specific to library domain logic

## Future Enhancements

- [ ] Reservation queue for books that are fully checked out
- [ ] Email reminders for upcoming due dates (connects to Module 12)
- [ ] Genre/category classification and filtering
- [ ] Member borrowing history view
