# =============================================================================
# calculator.py
# Project : 01 - Scientific Calculator Application
# Author  : Pavan Shetty H S
# Date    : August 2024
# =============================================================================
#
# Notes from Pavan:
# My very first "real" project after finishing the basics modules. Started
# as a simple 4-operation calculator, then I kept adding features
# (power, sqrt, log, trig, history) over a weekend because I got into a
# flow state. This is genuinely the project that made me feel like I was
# "building something" instead of just doing exercises.
# =============================================================================

import math

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self._log(f"{a} + {b} = {result}")
        return result

    def subtract(self, a, b):
        result = a - b
        self._log(f"{a} - {b} = {result}")
        return result

    def multiply(self, a, b):
        result = a * b
        self._log(f"{a} * {b} = {result}")
        return result

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = a / b
        self._log(f"{a} / {b} = {result}")
        return result

    def modulus(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot perform modulus by zero")
        result = a % b
        self._log(f"{a} % {b} = {result}")
        return result

    def power(self, a, b):
        result = a ** b
        self._log(f"{a} ^ {b} = {result}")
        return result

    def square_root(self, a):
        if a < 0:
            raise ValueError("Cannot compute square root of a negative number")
        result = math.sqrt(a)
        self._log(f"sqrt({a}) = {result}")
        return result

    def logarithm(self, a, base=10):
        if a <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")
        result = math.log(a, base)
        self._log(f"log_{base}({a}) = {result}")
        return result

    def sine(self, degrees):
        result = math.sin(math.radians(degrees))
        self._log(f"sin({degrees}°) = {result:.4f}")
        return result

    def cosine(self, degrees):
        result = math.cos(math.radians(degrees))
        self._log(f"cos({degrees}°) = {result:.4f}")
        return result

    def tangent(self, degrees):
        result = math.tan(math.radians(degrees))
        self._log(f"tan({degrees}°) = {result:.4f}")
        return result

    def _log(self, entry):
        self.history.append(entry)

    def show_history(self):
        if not self.history:
            print("  No calculations yet.")
            return
        for i, entry in enumerate(self.history, 1):
            print(f"  {i}. {entry}")


def print_menu():
    print("\n" + "=" * 40)
    print("     PYTHON SCIENTIFIC CALCULATOR")
    print("=" * 40)
    print(" 1. Addition          6. Power")
    print(" 2. Subtraction       7. Square Root")
    print(" 3. Multiplication    8. Logarithm")
    print(" 4. Division          9. Trigonometry")
    print(" 5. Modulus          10. History")
    print("                     11. Exit")
    print("=" * 40)


def main():
    calc = Calculator()
    print("Welcome to Pavan's Scientific Calculator!")

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                print(f"------------------------------------\nResult: {a} + {b} = {calc.add(a, b)}\n------------------------------------")
            elif choice == "2":
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                print(f"------------------------------------\nResult: {a} - {b} = {calc.subtract(a, b)}\n------------------------------------")
            elif choice == "3":
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                print(f"------------------------------------\nResult: {a} * {b} = {calc.multiply(a, b)}\n------------------------------------")
            elif choice == "4":
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                print(f"------------------------------------\nResult: {a} / {b} = {calc.divide(a, b)}\n------------------------------------")
            elif choice == "5":
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                print(f"------------------------------------\nResult: {a} % {b} = {calc.modulus(a, b)}\n------------------------------------")
            elif choice == "6":
                a = float(input("Enter base: "))
                b = float(input("Enter exponent: "))
                print(f"------------------------------------\nResult: {a} ^ {b} = {calc.power(a, b)}\n------------------------------------")
            elif choice == "7":
                a = float(input("Enter number: "))
                print(f"------------------------------------\nResult: sqrt({a}) = {calc.square_root(a):.4f}\n------------------------------------")
            elif choice == "8":
                a = float(input("Enter number: "))
                base = float(input("Enter base (default 10): ") or 10)
                print(f"------------------------------------\nResult: log = {calc.logarithm(a, base):.4f}\n------------------------------------")
            elif choice == "9":
                print("  a. sin   b. cos   c. tan")
                trig_choice = input("  Choose: ").strip().lower()
                deg = float(input("Enter angle in degrees: "))
                if trig_choice == "a":
                    print(f"Result: sin({deg}°) = {calc.sine(deg):.4f}")
                elif trig_choice == "b":
                    print(f"Result: cos({deg}°) = {calc.cosine(deg):.4f}")
                elif trig_choice == "c":
                    print(f"Result: tan({deg}°) = {calc.tangent(deg):.4f}")
                else:
                    print("Invalid trig choice")
            elif choice == "10":
                print("\n----- CALCULATION HISTORY -----")
                calc.show_history()
            elif choice == "11":
                print("\nThank you for using Pavan's Calculator! Goodbye.")
                break
            else:
                print("Invalid choice. Please select 1-11.")

        except ZeroDivisionError as e:
            print(f"  Error: {e}")
        except ValueError as e:
            print(f"  Error: {e}")
        except Exception as e:
            print(f"  Unexpected error: {e}")


if __name__ == "__main__":
    main()

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 calculator.py
# =============================================================================
#
# Welcome to Pavan's Scientific Calculator!
#
# ========================================
#      PYTHON SCIENTIFIC CALCULATOR
# ========================================
#  1. Addition          6. Power
#  2. Subtraction       7. Square Root
#  3. Multiplication    8. Logarithm
#  4. Division          9. Trigonometry
#  5. Modulus          10. History
#                      11. Exit
# ========================================
# Enter choice: Enter first number: Enter second number: ------------------------------------
# Result: 15.0 + 27.0 = 42.0
# ------------------------------------
#
# ========================================
#      PYTHON SCIENTIFIC CALCULATOR
# ========================================
#  1. Addition          6. Power
#  2. Subtraction       7. Square Root
#  3. Multiplication    8. Logarithm
#  4. Division          9. Trigonometry
#  5. Modulus          10. History
#                      11. Exit
# ========================================
# Enter choice: Enter base: Enter exponent: ------------------------------------
# Result: 2.0 ^ 8.0 = 256.0
# ------------------------------------
#
# ========================================
#      PYTHON SCIENTIFIC CALCULATOR
# ========================================
#  1. Addition          6. Power
#  2. Subtraction       7. Square Root
#  3. Multiplication    8. Logarithm
#  4. Division          9. Trigonometry
#  5. Modulus          10. History
#                      11. Exit
# ========================================
# Enter choice: Enter number: ------------------------------------
# Result: sqrt(16.0) = 4.0000
# ------------------------------------
#
# ========================================
#      PYTHON SCIENTIFIC CALCULATOR
# ========================================
#  1. Addition          6. Power
#  2. Subtraction       7. Square Root
#  3. Multiplication    8. Logarithm
#  4. Division          9. Trigonometry
#  5. Modulus          10. History
#                      11. Exit
# ========================================
# Enter choice:   a. sin   b. cos   c. tan
#   Choose: Enter angle in degrees: Result: sin(30.0°) = 0.5000
#
# ========================================
#      PYTHON SCIENTIFIC CALCULATOR
# ========================================
#  1. Addition          6. Power
#  2. Subtraction       7. Square Root
#  3. Multiplication    8. Logarithm
#  4. Division          9. Trigonometry
#  5. Modulus          10. History
#                      11. Exit
# ========================================
# Enter choice: 
# ----- CALCULATION HISTORY -----
#   1. 15.0 + 27.0 = 42.0
#   2. 2.0 ^ 8.0 = 256.0
#   3. sqrt(16.0) = 4.0
#   4. sin(30.0°) = 0.5000
#
# ========================================
#      PYTHON SCIENTIFIC CALCULATOR
# ========================================
#  1. Addition          6. Power
#  2. Subtraction       7. Square Root
#  3. Multiplication    8. Logarithm
#  4. Division          9. Trigonometry
#  5. Modulus          10. History
#                      11. Exit
# ========================================
# Enter choice: 
# Thank you for using Pavan's Calculator! Goodbye.
#
# =============================================================================

