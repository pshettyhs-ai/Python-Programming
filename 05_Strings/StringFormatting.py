# =============================================================================
# StringFormatting.py
# Author  : Pavan Shetty H S
# Date    : March 2024
# Topic   : String Formatting -- %, .format(), f-strings
# =============================================================================
#
# Notes from Pavan:
# There are THREE ways to format strings in Python and I was confused
# about which to use for a while. After research: f-strings (Python 3.6+)
# are the modern standard, fastest, and most readable. I use them
# everywhere now. Keeping the old methods here because I still see them
# in older codebases and tutorials, so I should recognize them.
#
# =============================================================================

print("=" * 50)
print("    STRING FORMATTING DEMO")
print("=" * 50)

name = "Pavan"
age = 22
cgpa = 8.567

# ---------------------
# Method 1: % operator (old style, C-like)
# ---------------------
print("\n[1] % operator (old style -- looks like C's printf)")
print("  Name: %s, Age: %d, CGPA: %.2f" % (name, age, cgpa))

# ---------------------
# Method 2: .format()
# ---------------------
print("\n[2] .format() method")
print("  Name: {}, Age: {}, CGPA: {:.2f}".format(name, age, cgpa))
print("  Name: {0}, Age: {1}, Name again: {0}".format(name, age))   # positional reuse
print("  Name: {n}, Age: {a}".format(n=name, a=age))                # named

# ---------------------
# Method 3: f-strings (MODERN, what I use now)
# ---------------------
print("\n[3] f-strings (Python 3.6+, my default choice)")
print(f"  Name: {name}, Age: {age}, CGPA: {cgpa:.2f}")

# f-strings can contain expressions directly!
print(f"  Age next year: {age + 1}")
print(f"  Uppercase name: {name.upper()}")

# ---------------------
# Number formatting specifiers
# ---------------------
print("\n[4] Number formatting specifiers")
value = 1234567.891

print(f"  Default        : {value}")
print(f"  2 decimals     : {value:.2f}")
print(f"  Comma separator: {value:,.2f}")
print(f"  Percentage     : {0.4567:.2%}")
print(f"  Scientific     : {value:.2e}")

n = 42
print(f"\n  Binary  : {n:b}")
print(f"  Octal   : {n:o}")
print(f"  Hex     : {n:x}")
print(f"  With width/padding: '{n:5}'  -> right aligned width 5")
print(f"  Zero padded: '{n:05}'")

# ---------------------
# Alignment
# ---------------------
print("\n[5] Alignment (useful for table-like output)")
items = ["Pen", "Notebook", "Calculator"]
prices = [10, 45, 850]

print(f"\n  {'Item':<15}{'Price':>10}")
print("  " + "-" * 25)
for item, price in zip(items, prices):
    print(f"  {item:<15}{price:>10}")

# < left align, > right align, ^ center align
print(f"\n  '{'left':<10}|'  (left align)")
print(f"  '{'right':>10}|'  (right align)")
print(f"  '{'mid':^10}|'  (center align)")

# ---------------------
# Multi-line f-strings and nested expressions
# ---------------------
print("\n[6] Practical: Building a formatted receipt")
item_name = "USB Cable"
qty = 3
unit_price = 149.50
total = qty * unit_price

receipt = f"""
{'='*30}
       PURCHASE RECEIPT
{'='*30}
Item     : {item_name}
Quantity : {qty}
Price    : Rs.{unit_price:.2f}
{'='*30}
Total    : Rs.{total:.2f}
{'='*30}
"""
print(receipt)

print("=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 StringFormatting.py
# =============================================================================
#
# ==================================================
#     STRING FORMATTING DEMO
# ==================================================
#
# [1] % operator (old style -- looks like C's printf)
#   Name: Pavan, Age: 22, CGPA: 8.57
#
# [2] .format() method
#   Name: Pavan, Age: 22, CGPA: 8.57
#   Name: Pavan, Age: 22, Name again: Pavan
#   Name: Pavan, Age: 22
#
# [3] f-strings (Python 3.6+, my default choice)
#   Name: Pavan, Age: 22, CGPA: 8.57
#   Age next year: 23
#   Uppercase name: PAVAN
#
# [4] Number formatting specifiers
#   Default        : 1234567.891
#   2 decimals     : 1234567.89
#   Comma separator: 1,234,567.89
#   Percentage     : 45.67%
#   Scientific     : 1.23e+06
#
#   Binary  : 101010
#   Octal   : 52
#   Hex     : 2a
#   With width/padding: '   42'  -> right aligned width 5
#   Zero padded: '00042'
#
# [5] Alignment (useful for table-like output)
#
#   Item                Price
#   -------------------------
#   Pen                    10
#   Notebook               45
#   Calculator            850
#
#   'left      |'  (left align)
#   '     right|'  (right align)
#   '   mid    |'  (center align)
#
# [6] Practical: Building a formatted receipt
#
# ==============================
#        PURCHASE RECEIPT
# ==============================
# Item     : USB Cable
# Quantity : 3
# Price    : Rs.149.50
# ==============================
# Total    : Rs.448.50
# ==============================
#
# ==================================================
#
# =============================================================================

