# 🔐 Project 8: Password Manager

**Author:** Pavan Shetty H S
**Built:** September 2024

---

## Project Overview

An encrypted password vault with strong password generation and strength
checking. This is the project I was most nervous about getting wrong.
Storing passwords, even for a personal learning project, pushed me to
actually research proper encryption instead of taking a shortcut.

**Honest confession:** I genuinely considered base64-encoding passwords
and calling it "secure" for about five minutes before realizing base64
is ENCODING, not ENCRYPTION — trivially and intentionally reversible by
anyone, not remotely secure for sensitive data. Switched to the
`cryptography` library's Fernet symmetric encryption, which is actually
designed for this purpose, generates a proper encryption key, and
produces genuinely unreadable ciphertext without that key.

**Important security note documented directly in the code:** the
generated `secret.key` file must be kept private and should never be
committed to version control — anyone with that key can decrypt every
stored password. This repo includes the code, not a real key or real
vault data.

## Features

- AES-based encryption (via Fernet) for all stored passwords
- Add new entries (website, username, password) with optional auto-generation
- View individual decrypted passwords by entry ID
- View all entries WITHOUT exposing passwords (safe listing mode)
- Search entries by website
- Cryptographically secure password generation (using `secrets`, not
  `random` — an important distinction I researched specifically for
  this project)
- Password strength checker with actionable feedback
- Delete entries

## Folder Structure

```
Project08_PasswordManager/
├── password_manager.py
├── vault.db          # encrypted entries (created on first run)
├── secret.key          # encryption key (NEVER commit this in real use)
├── README.md
└── requirements.txt
```

## Algorithm

**Encryption Flow (Add Entry):**
1. Generate or load a persistent Fernet encryption key
2. Encode password string to bytes
3. Encrypt bytes using Fernet (AES 128 in CBC mode + HMAC for integrity)
4. Store ciphertext (BLOB) in SQLite — never store plaintext

**Decryption Flow (View Password):**
1. Look up the entry's encrypted_password BLOB
2. Decrypt using the same Fernet key
3. Decode bytes back to a readable string
4. Display only when explicitly requested by entry ID (never in the
   "view all" listing)

**Secure Password Generation:**
1. Build a character pool (letters, digits, optionally symbols)
2. Use `secrets.choice()` (cryptographically secure) for each character
   — NOT `random.choice()`, which uses a predictable PRNG unsuitable
   for security purposes

## Requirements

```
cryptography==41.0.3
```

## Installation Steps

```bash
cd 15_Projects/Project08_PasswordManager
pip install -r requirements.txt
python password_manager.py
```

## Execution Guide

```bash
python password_manager.py
```

## Sample Inputs & Outputs

```
==========================================
          PASSWORD MANAGER
          Encrypted Vault
==========================================

🔒 Vault unlocked. All passwords are encrypted at rest.

 1. Add New Entry
 2. View Password
 3. View All Entries (no passwords shown)
 4. Search
 5. Generate Strong Password
 6. Check Password Strength
 7. Delete Entry
 8. Exit

Enter Choice: 1
Website: github.com
Username: pavanshettyhs
Generate a strong password? (y/n): y
  Generated password: xK9#mP2$vL8nQ4@z

✓ Entry saved with ID 1 (password encrypted)

Enter Choice: 3

  ID   Website                  Username
  --------------------------------------------------
  1    github.com               pavanshettyhs

Enter Choice: 2
Entry ID: 1

  Website : github.com
  Username: pavanshettyhs
  Password: xK9#mP2$vL8nQ4@z

Enter Choice: 6
Enter password to check: password123

  Strength: Fair
  Suggestions:
    - Use at least 12 characters
    - Add uppercase letters
    - Add special characters
```

## Screenshots

> See `/Images/Screenshots/project08_*.png`:
> - `project08_menu.png`
> - `project08_add_entry.png`
> - `project08_view_all_safe.png` — shows passwords are hidden in list view
> - `project08_decrypt_view.png` — explicit single-entry decryption
> - `project08_strength_check.png`

## Learning Outcomes

- Real, practical lesson in the difference between ENCODING (reversible
  by design, not secure) and ENCRYPTION (requires a key, actually secure)
- Learned to use `secrets` instead of `random` for any
  security-sensitive randomness — a distinction I hadn't previously
  known mattered
- Practiced separating "safe to display" data (website, username) from
  "sensitive, opt-in only" data (decrypted password) at the application
  level, not just relying on database access control
- Documented a real security practice (never commit secret.key) directly
  in code comments, not just as an afterthought

## Future Enhancements

- [ ] Master password requirement to unlock the vault itself
- [ ] Auto-clear clipboard after copying a password
- [ ] Password expiry reminders
- [ ] Breach-check integration (checking against known leaked password lists)
