# =============================================================================
# library_management.py
# Project : 04 - Library Management System
# Author  : Pavan Shetty H S
# Date    : August 2024
# =============================================================================
#
# Notes from Pavan:
# Built this right after the Bank Management project, so I reused a lot
# of structural patterns (custom exceptions, SQLite class wrapper) that
# were still fresh in my head. New challenge here: tracking BOTH books
# AND members AND the relationship between them (who has what checked
# out, due dates). This is my first project with genuinely related
# multi-table data and real foreign keys doing meaningful work.
# =============================================================================

import sqlite3
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "library.db")


class LibraryError(Exception):
    pass

class BookNotAvailableError(LibraryError):
    pass

class BookNotFoundError(LibraryError):
    pass

class MemberNotFoundError(LibraryError):
    pass


class Library:
    def __init__(self, db_path=DB_PATH):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                total_copies INTEGER DEFAULT 1,
                available_copies INTEGER DEFAULT 1
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (member_id) REFERENCES members(member_id)
            )
        """)
        self.connection.commit()

    def add_book(self, title, author, isbn, copies=1):
        self.cursor.execute(
            "INSERT INTO books (title, author, isbn, total_copies, available_copies) VALUES (?, ?, ?, ?, ?)",
            (title, author, isbn, copies, copies)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def add_member(self, name, email):
        self.cursor.execute(
            "INSERT INTO members (name, email) VALUES (?, ?)", (name, email)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def search_books(self, keyword):
        self.cursor.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        )
        return self.cursor.fetchall()

    def issue_book(self, book_id, member_id, loan_days=14):
        self.cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        book = self.cursor.fetchone()
        if not book:
            raise BookNotFoundError(f"Book ID {book_id} not found")
        if book[5] <= 0:   # available_copies
            raise BookNotAvailableError(f"'{book[1]}' has no available copies")

        self.cursor.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
        if not self.cursor.fetchone():
            raise MemberNotFoundError(f"Member ID {member_id} not found")

        issue_date = datetime.date.today()
        due_date = issue_date + datetime.timedelta(days=loan_days)

        self.cursor.execute(
            "INSERT INTO loans (book_id, member_id, issue_date, due_date) VALUES (?, ?, ?, ?)",
            (book_id, member_id, str(issue_date), str(due_date))
        )
        self.cursor.execute(
            "UPDATE books SET available_copies = available_copies - 1 WHERE book_id = ?",
            (book_id,)
        )
        self.connection.commit()
        return str(due_date)

    def return_book(self, loan_id):
        self.cursor.execute("SELECT * FROM loans WHERE loan_id = ?", (loan_id,))
        loan = self.cursor.fetchone()
        if not loan:
            raise LibraryError(f"Loan ID {loan_id} not found")
        if loan[5]:   # already has a return_date
            raise LibraryError("This book has already been returned")

        return_date = str(datetime.date.today())
        self.cursor.execute(
            "UPDATE loans SET return_date = ? WHERE loan_id = ?", (return_date, loan_id)
        )
        self.cursor.execute(
            "UPDATE books SET available_copies = available_copies + 1 WHERE book_id = ?",
            (loan[1],)
        )
        self.connection.commit()

        # Check for overdue fine (Rs.5 per day late)
        due = datetime.date.fromisoformat(loan[4])
        today = datetime.date.today()
        if today > due:
            days_late = (today - due).days
            fine = days_late * 5
            return f"Returned {days_late} days late. Fine: Rs.{fine}"
        return "Returned on time. No fine."

    def overdue_books(self):
        today = str(datetime.date.today())
        self.cursor.execute("""
            SELECT loans.loan_id, books.title, members.name, loans.due_date
            FROM loans
            JOIN books ON loans.book_id = books.book_id
            JOIN members ON loans.member_id = members.member_id
            WHERE loans.return_date IS NULL AND loans.due_date < ?
        """, (today,))
        return self.cursor.fetchall()

    def view_all_books(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()


def print_menu():
    print("\n" + "=" * 42)
    print("       LIBRARY MANAGEMENT SYSTEM")
    print("=" * 42)
    print(" 1. Add Book")
    print(" 2. Add Member")
    print(" 3. Search Books")
    print(" 4. Issue Book")
    print(" 5. Return Book")
    print(" 6. View Overdue Books")
    print(" 7. View All Books")
    print(" 8. Exit")


def main():
    lib = Library()
    while True:
        print_menu()
        choice = input("\nEnter Choice: ").strip()
        try:
            if choice == "1":
                title = input("Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")
                copies = int(input("Number of copies: ") or 1)
                book_id = lib.add_book(title, author, isbn, copies)
                print(f"\n✓ Book added with ID {book_id}")

            elif choice == "2":
                name = input("Member Name: ")
                email = input("Email: ")
                member_id = lib.add_member(name, email)
                print(f"\n✓ Member added with ID {member_id}")

            elif choice == "3":
                keyword = input("Search keyword (title/author): ")
                results = lib.search_books(keyword)
                print(f"\nFound {len(results)} result(s):")
                for b in results:
                    print(f"  [{b[0]}] {b[1]} by {b[2]} -- Available: {b[5]}/{b[4]}")

            elif choice == "4":
                book_id = int(input("Book ID: "))
                member_id = int(input("Member ID: "))
                due_date = lib.issue_book(book_id, member_id)
                print(f"\n✓ Book issued! Due date: {due_date}")

            elif choice == "5":
                loan_id = int(input("Loan ID: "))
                result = lib.return_book(loan_id)
                print(f"\n✓ {result}")

            elif choice == "6":
                overdue = lib.overdue_books()
                if overdue:
                    print(f"\n{len(overdue)} overdue book(s):")
                    for o in overdue:
                        print(f"  Loan {o[0]}: '{o[1]}' borrowed by {o[2]} (due {o[3]})")
                else:
                    print("\n  No overdue books!")

            elif choice == "7":
                books = lib.view_all_books()
                print(f"\n  {'ID':5}{'Title':25}{'Author':20}{'Available':10}")
                for b in books:
                    print(f"  {b[0]:<5}{b[1]:<25}{b[2]:<20}{b[5]}/{b[4]}")

            elif choice == "8":
                print("\nThank you for using the Library System!")
                lib.close()
                break
            else:
                print("✗ Invalid choice.")
        except LibraryError as e:
            print(f"\n✗ {type(e).__name__}: {e}")
        except (ValueError, sqlite3.IntegrityError) as e:
            print(f"\n✗ Input error: {e}")


if __name__ == "__main__":
    main()

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 library_management.py
# =============================================================================
#
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: Title: Author: ISBN: Number of copies: 
# ✓ Book added with ID 1
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: Title: Author: ISBN: Number of copies: 
# ✓ Book added with ID 2
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: Member Name: Email: 
# ✓ Member added with ID 1
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: Member Name: Email: 
# ✓ Member added with ID 2
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: 
#   ID   Title                    Author              Available 
#   1    The C++ Programming LanguageBjarne Stroustrup   3/3
#   2    Clean Code               Robert C. Martin    4/4
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: Book ID: Member ID: 
# ✓ Book issued! Due date: 2026-07-05
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: Book ID: Member ID: 
# ✓ Book issued! Due date: 2026-07-05
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: Search keyword (title/author): 
# Found 1 result(s):
#   [2] Clean Code by Robert C. Martin -- Available: 3/4
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: 
#   No overdue books!
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: Loan ID: 
# ✓ Returned on time. No fine.
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: 
#   No overdue books!
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: 
#   ID   Title                    Author              Available 
#   1    The C++ Programming LanguageBjarne Stroustrup   3/3
#   2    Clean Code               Robert C. Martin    3/4
#
# ==========================================
#        LIBRARY MANAGEMENT SYSTEM
# ==========================================
#  1. Add Book
#  2. Add Member
#  3. Search Books
#  4. Issue Book
#  5. Return Book
#  6. View Overdue Books
#  7. View All Books
#  8. Exit
#
# Enter Choice: 
# Thank you for using the Library System!
#
# =============================================================================

