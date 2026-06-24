# =============================================================================
# UserInput.py
# Author  : Pavan Shetty H S
# Date    : January 2024
# Topic   : Taking Input from User
# =============================================================================
#
# Notes from Pavan:
# input() always returns a string. ALWAYS. This bit me hard in week 1 —
# I tried to add two "numbers" entered by the user and got string
# concatenation instead of addition. "5" + "3" gave me "53", not 8.
# Took me a solid 15 minutes of confused printing to figure out why.
# Lesson: always typecast input() when you need numbers.
#
# =============================================================================

print("=" * 50)
print("       USER INPUT DEMO")
print("=" * 50)

# ---------------------
# Basic input — always returns string
# ---------------------
name = input("Enter your name: ")
print(f"Hello, {name}! Welcome.")
print(f"Type of input: {type(name)}")

# ---------------------
# The classic mistake I made
# ---------------------
print("\n--- The bug that confused me in week 1 ---")
num1 = input("Enter first number: ")
num2 = input("Enter second number: ")
print(f"Without casting: {num1} + {num2} = {num1 + num2}  <-- WRONG! (string concat)")
print(f"With casting   : {num1} + {num2} = {int(num1) + int(num2)}  <-- correct")

# ---------------------
# Correct way — typecast immediately
# ---------------------
age = int(input("\nEnter your age: "))
height = float(input("Enter your height in meters: "))

print(f"\nIn 10 years, you'll be {age + 10} years old.")
print(f"Your height in cm: {height * 100}")

# ---------------------
# Taking multiple inputs in one line
# ---------------------
print("\n--- Multiple inputs in one line ---")
data = input("Enter name, age, branch (comma-separated): ")
parts = data.split(",")
print(f"Parsed parts: {parts}")
print(f"Name: {parts[0].strip()}")

# ---------------------
# Taking multiple numbers using split + map
# ---------------------
print("\n--- Multiple numbers using map() ---")
nums_input = input("Enter 3 numbers separated by space: ")
a, b, c = map(int, nums_input.split())
print(f"Sum = {a + b + c}")

# ---------------------
# Input validation example
# ---------------------
print("\n--- Input Validation ---")
while True:
    choice = input("Enter a number between 1-5: ")
    if choice.isdigit() and 1 <= int(choice) <= 5:
        print(f"Valid choice: {choice}")
        break
    else:
        print("Invalid input. Try again.")
        break  # Removed in real loop scenario - here just for demo, would loop in practice

print("\n" + "=" * 50)

# =============================================================================
# Sample Run:
# Enter your name: Pavan
# Hello, Pavan! Welcome.
# Type of input: <class 'str'>
#
# Enter first number: 5
# Enter second number: 3
# Without casting: 5 + 3 = 53  <-- WRONG! (string concat)
# With casting   : 5 + 3 = 8  <-- correct
# =============================================================================

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 UserInput.py
# =============================================================================
#
# ==================================================
#        USER INPUT DEMO
# ==================================================
# Enter your name: Hello, Pavan! Welcome.
# Type of input: <class 'str'>
#
# --- The bug that confused me in week 1 ---
# Enter first number: Enter second number: Without casting: 5 + 3 = 53  <-- WRONG! (string concat)
# With casting   : 5 + 3 = 8  <-- correct
#
# Enter your age: Enter your height in meters: 
# In 10 years, you'll be 31 years old.
# Your height in cm: 175.0
#
# --- Multiple inputs in one line ---
# Enter name, age, branch (comma-separated): Parsed parts: ['Pavan', ' 21', ' CSE']
# Name: Pavan
#
# --- Multiple numbers using map() ---
# Enter 3 numbers separated by space: Sum = 60
#
# --- Input Validation ---
# Enter a number between 1-5: Valid choice: 3
#
# ==================================================
#
# =============================================================================

