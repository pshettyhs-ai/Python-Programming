# =============================================================================
# password_manager.py
# Project : 08 - Password Manager
# Author  : Pavan Shetty H S
# Date    : September 2024
# =============================================================================
#
# Notes from Pavan:
# This is the project I was most nervous about getting wrong. Storing
# passwords, even for a personal learning project, made me actually
# research proper encryption instead of just base64-encoding things and
# calling it "secure" (which I embarrassingly considered for about five
# minutes before realizing base64 is ENCODING, not ENCRYPTION -- totally
# reversible by anyone, not remotely secure). Used the 'cryptography'
# library's Fernet symmetric encryption instead, which is actually
# designed for this purpose.
# =============================================================================

import sqlite3
import os
import string
import secrets
from cryptography.fernet import Fernet

DB_PATH = os.path.join(os.path.dirname(__file__), "vault.db")
KEY_PATH = os.path.join(os.path.dirname(__file__), "secret.key")


class PasswordManagerError(Exception):
    pass

class EntryNotFoundError(PasswordManagerError):
    pass


def load_or_create_key():
    """Generates a new encryption key on first run, reuses it afterward.
    IMPORTANT lesson I learned: this key file must be kept safe and
    PRIVATE. Anyone with this key can decrypt all stored passwords.
    For a real production tool, this absolutely should NOT live in the
    same folder as the database, and definitely shouldn't be committed
    to git. Noting clearly here for anyone reading this as a learning
    reference: never commit secret.key to version control."""
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)
    return key


class PasswordManager:
    def __init__(self, db_path=DB_PATH):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.fernet = Fernet(load_or_create_key())
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vault (
                entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                encrypted_password BLOB NOT NULL
            )
        """)
        self.connection.commit()

    def add_entry(self, website, username, password):
        encrypted = self.fernet.encrypt(password.encode())
        self.cursor.execute(
            "INSERT INTO vault (website, username, encrypted_password) VALUES (?, ?, ?)",
            (website, username, encrypted)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_password(self, entry_id):
        self.cursor.execute("SELECT * FROM vault WHERE entry_id = ?", (entry_id,))
        row = self.cursor.fetchone()
        if not row:
            raise EntryNotFoundError(f"Entry {entry_id} not found")
        decrypted = self.fernet.decrypt(row[3]).decode()
        return {"website": row[1], "username": row[2], "password": decrypted}

    def view_all_entries(self):
        """Returns entries WITHOUT decrypting passwords, for a safe listing view."""
        self.cursor.execute("SELECT entry_id, website, username FROM vault")
        return self.cursor.fetchall()

    def delete_entry(self, entry_id):
        self.cursor.execute("DELETE FROM vault WHERE entry_id = ?", (entry_id,))
        self.connection.commit()
        if self.cursor.rowcount == 0:
            raise EntryNotFoundError(f"Entry {entry_id} not found")

    def search(self, keyword):
        self.cursor.execute(
            "SELECT entry_id, website, username FROM vault WHERE website LIKE ?",
            (f"%{keyword}%",)
        )
        return self.cursor.fetchall()

    @staticmethod
    def generate_password(length=16, use_symbols=True):
        """Generates a cryptographically secure random password.
        Used 'secrets' module, NOT 'random' -- learned this distinction
        the hard way while researching this project. 'random' is
        predictable enough to be exploitable for security purposes
        (it's a Mersenne Twister PRNG, not cryptographically secure).
        'secrets' is specifically designed for security-sensitive
        random generation."""
        characters = string.ascii_letters + string.digits
        if use_symbols:
            characters += "!@#$%^&*()-_=+"
        return ''.join(secrets.choice(characters) for _ in range(length))

    @staticmethod
    def check_password_strength(password):
        """Simple strength checker based on common criteria."""
        score = 0
        feedback = []

        if len(password) >= 12:
            score += 1
        else:
            feedback.append("Use at least 12 characters")

        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Add uppercase letters")

        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Add lowercase letters")

        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Add numbers")

        if any(c in string.punctuation for c in password):
            score += 1
        else:
            feedback.append("Add special characters")

        strength_levels = {0: "Very Weak", 1: "Weak", 2: "Fair", 3: "Good", 4: "Strong", 5: "Very Strong"}
        return strength_levels[score], feedback

    def close(self):
        self.connection.close()


def print_menu():
    print("\n" + "=" * 42)
    print("          PASSWORD MANAGER")
    print("          Encrypted Vault")
    print("=" * 42)
    print(" 1. Add New Entry")
    print(" 2. View Password")
    print(" 3. View All Entries (no passwords shown)")
    print(" 4. Search")
    print(" 5. Generate Strong Password")
    print(" 6. Check Password Strength")
    print(" 7. Delete Entry")
    print(" 8. Exit")


def main():
    pm = PasswordManager()
    print("\n🔒 Vault unlocked. All passwords are encrypted at rest.")

    while True:
        print_menu()
        choice = input("\nEnter Choice: ").strip()
        try:
            if choice == "1":
                website = input("Website: ")
                username = input("Username: ")
                use_generated = input("Generate a strong password? (y/n): ").lower()
                if use_generated == "y":
                    password = pm.generate_password()
                    print(f"  Generated password: {password}")
                else:
                    password = input("Password: ")
                entry_id = pm.add_entry(website, username, password)
                print(f"\n✓ Entry saved with ID {entry_id} (password encrypted)")

            elif choice == "2":
                entry_id = int(input("Entry ID: "))
                entry = pm.get_password(entry_id)
                print(f"\n  Website : {entry['website']}")
                print(f"  Username: {entry['username']}")
                print(f"  Password: {entry['password']}")

            elif choice == "3":
                entries = pm.view_all_entries()
                print(f"\n  {'ID':5}{'Website':25}{'Username':20}")
                print("  " + "-" * 50)
                for e in entries:
                    print(f"  {e[0]:<5}{e[1]:<25}{e[2]:<20}")

            elif choice == "4":
                keyword = input("Search website: ")
                results = pm.search(keyword)
                print(f"\nFound {len(results)} match(es):")
                for r in results:
                    print(f"  [{r[0]}] {r[1]} - {r[2]}")

            elif choice == "5":
                length = int(input("Password length (default 16): ") or 16)
                password = pm.generate_password(length)
                strength, _ = pm.check_password_strength(password)
                print(f"\n  Generated: {password}")
                print(f"  Strength : {strength}")

            elif choice == "6":
                password = input("Enter password to check: ")
                strength, feedback = pm.check_password_strength(password)
                print(f"\n  Strength: {strength}")
                if feedback:
                    print("  Suggestions:")
                    for f in feedback:
                        print(f"    - {f}")

            elif choice == "7":
                entry_id = int(input("Entry ID to delete: "))
                pm.delete_entry(entry_id)
                print(f"\n✓ Entry {entry_id} deleted")

            elif choice == "8":
                print("\n🔒 Vault locked. Goodbye!")
                pm.close()
                break
            else:
                print("✗ Invalid choice.")
        except PasswordManagerError as e:
            print(f"\n✗ {type(e).__name__}: {e}")
        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")


if __name__ == "__main__":
    main()

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 password_manager.py
# =============================================================================
#
#
# 🔒 Vault unlocked. All passwords are encrypted at rest.
#
# ==========================================
#           PASSWORD MANAGER
#           Encrypted Vault
# ==========================================
#  1. Add New Entry
#  2. View Password
#  3. View All Entries (no passwords shown)
#  4. Search
#  5. Generate Strong Password
#  6. Check Password Strength
#  7. Delete Entry
#  8. Exit
#
# Enter Choice: Website: Username: Generate a strong password? (y/n):   Generated password: _91ZAy-4yM5vp3a+
#
# ✓ Entry saved with ID 1 (password encrypted)
#
# ==========================================
#           PASSWORD MANAGER
#           Encrypted Vault
# ==========================================
#  1. Add New Entry
#  2. View Password
#  3. View All Entries (no passwords shown)
#  4. Search
#  5. Generate Strong Password
#  6. Check Password Strength
#  7. Delete Entry
#  8. Exit
#
# Enter Choice: Website: Username: Generate a strong password? (y/n): Password: 
# ✓ Entry saved with ID 2 (password encrypted)
#
# ==========================================
#           PASSWORD MANAGER
#           Encrypted Vault
# ==========================================
#  1. Add New Entry
#  2. View Password
#  3. View All Entries (no passwords shown)
#  4. Search
#  5. Generate Strong Password
#  6. Check Password Strength
#  7. Delete Entry
#  8. Exit
#
# Enter Choice: 
#   ID   Website                  Username            
#   --------------------------------------------------
#   1    github.com               pavanshetty         
#   2    gmail.com                pavan@gmail.com     
#
# ==========================================
#           PASSWORD MANAGER
#           Encrypted Vault
# ==========================================
#  1. Add New Entry
#  2. View Password
#  3. View All Entries (no passwords shown)
#  4. Search
#  5. Generate Strong Password
#  6. Check Password Strength
#  7. Delete Entry
#  8. Exit
#
# Enter Choice: Entry ID: 
#   Website : github.com
#   Username: pavanshetty
#   Password: _91ZAy-4yM5vp3a+
#
# ==========================================
#           PASSWORD MANAGER
#           Encrypted Vault
# ==========================================
#  1. Add New Entry
#  2. View Password
#  3. View All Entries (no passwords shown)
#  4. Search
#  5. Generate Strong Password
#  6. Check Password Strength
#  7. Delete Entry
#  8. Exit
#
# Enter Choice: Search website: 
# Found 1 match(es):
#   [1] github.com - pavanshetty
#
# ==========================================
#           PASSWORD MANAGER
#           Encrypted Vault
# ==========================================
#  1. Add New Entry
#  2. View Password
#  3. View All Entries (no passwords shown)
#  4. Search
#  5. Generate Strong Password
#  6. Check Password Strength
#  7. Delete Entry
#  8. Exit
#
# Enter Choice: Password length (default 16): 
#   Generated: xHr^tzASKftPLNuP
#   Strength : Strong
#
# ==========================================
#           PASSWORD MANAGER
#           Encrypted Vault
# ==========================================
#  1. Add New Entry
#  2. View Password
#  3. View All Entries (no passwords shown)
#  4. Search
#  5. Generate Strong Password
#  6. Check Password Strength
#  7. Delete Entry
#  8. Exit
#
# Enter Choice: Enter password to check: 
#   Strength: Fair
#   Suggestions:
#     - Use at least 12 characters
#     - Add uppercase letters
#     - Add special characters
#
# ==========================================
#           PASSWORD MANAGER
#           Encrypted Vault
# ==========================================
#  1. Add New Entry
#  2. View Password
#  3. View All Entries (no passwords shown)
#  4. Search
#  5. Generate Strong Password
#  6. Check Password Strength
#  7. Delete Entry
#  8. Exit
#
# Enter Choice: Entry ID to delete: 
# ✓ Entry 2 deleted
#
# ==========================================
#           PASSWORD MANAGER
#           Encrypted Vault
# ==========================================
#  1. Add New Entry
#  2. View Password
#  3. View All Entries (no passwords shown)
#  4. Search
#  5. Generate Strong Password
#  6. Check Password Strength
#  7. Delete Entry
#  8. Exit
#
# Enter Choice: 
#   ID   Website                  Username            
#   --------------------------------------------------
#   1    github.com               pavanshetty         
#
# ==========================================
#           PASSWORD MANAGER
#           Encrypted Vault
# ==========================================
#  1. Add New Entry
#  2. View Password
#  3. View All Entries (no passwords shown)
#  4. Search
#  5. Generate Strong Password
#  6. Check Password Strength
#  7. Delete Entry
#  8. Exit
#
# Enter Choice: 
# 🔒 Vault locked. Goodbye!
#
# =============================================================================

