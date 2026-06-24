# =============================================================================
# Arguments.py
# Author  : Pavan Shetty H S
# Date    : February 2024
# Topic   : Positional, Keyword, Default, *args, **kwargs in depth
# =============================================================================
#
# Notes from Pavan:
# This file exists because Functions.py covered the basics but I kept
# getting confused about the ORDER rules when mixing different argument
# types. So I made a dedicated file just to nail this down.
#
# Order must be: positional -> *args -> keyword/default -> **kwargs
#
# =============================================================================

print("=" * 50)
print("   ARGUMENTS DEEP DIVE")
print("=" * 50)

# ---------------------
# Positional arguments -- order matters
# ---------------------
print("\n[1] Positional arguments (order matters)")

def describe_pet(animal, name):
    print(f"  {name} is a {animal}")

describe_pet("dog", "Tommy")        # correct order
describe_pet("Tommy", "dog")        # WRONG order -- still runs but wrong meaning!
print("  ^ Notice: no error, just wrong logic. This is dangerous!")

# ---------------------
# Keyword arguments -- order doesn't matter
# ---------------------
print("\n[2] Keyword arguments (order doesn't matter)")
describe_pet(name="Tommy", animal="dog")   # explicit, order-independent
describe_pet(animal="cat", name="Whiskers")

# ---------------------
# Default arguments -- must come after non-default ones
# ---------------------
print("\n[3] Default arguments")

def create_profile(name, age, country="India"):
    print(f"  {name}, {age} years old, from {country}")

create_profile("Pavan", 22)                  # uses default country
create_profile("John", 30, "USA")             # overrides default

# This would be a SyntaxError (non-default arg after default arg):
# def bad_function(name, age=20, branch):  # ERROR!

# ---------------------
# *args -- arbitrary positional arguments
# ---------------------
print("\n[4] *args in depth")

def calculate_total(*prices):
    """Accepts any number of price arguments."""
    print(f"  Received args as tuple: {prices}")
    return sum(prices)

print(f"  Total of (100, 250, 75): {calculate_total(100, 250, 75)}")
print(f"  Total of (50,): {calculate_total(50)}")

# Unpacking a list into *args using *
price_list = [10, 20, 30, 40]
print(f"  Unpacking a list with *: {calculate_total(*price_list)}")

# ---------------------
# **kwargs -- arbitrary keyword arguments
# ---------------------
print("\n[5] **kwargs in depth")

def build_user(**details):
    """Accepts any number of named arguments."""
    print(f"  Received kwargs as dict: {details}")
    for k, v in details.items():
        print(f"    {k} = {v}")

build_user(name="Pavan", role="Engineer", city="Mangalore")

# Unpacking a dict into **kwargs using **
user_data = {"name": "Sneha", "role": "Developer", "city": "Bangalore"}
print("  Unpacking a dict with **:")
build_user(**user_data)

# ---------------------
# Correct ordering when combining all types
# ---------------------
print("\n[6] Combining everything (correct order)")

def master_function(a, b, *args, c=10, **kwargs):
    """
    Order rule (I had to write this 3 times to remember it):
    1. Positional args (a, b)
    2. *args (collects extra positional)
    3. Keyword/default args (c=10)
    4. **kwargs (collects extra keyword)
    """
    print(f"  a={a}, b={b}")
    print(f"  args={args}")
    print(f"  c={c}")
    print(f"  kwargs={kwargs}")

master_function(1, 2, 3, 4, 5, c=99, extra1="x", extra2="y")

# ---------------------
# Keyword-only arguments (using * as separator)
# ---------------------
print("\n[7] Forcing keyword-only arguments")

def connect(host, port, *, timeout=30, retries=3):
    """Everything after the bare * MUST be passed as keyword argument.
    Learned this pattern from the 'requests' library source code."""
    print(f"  Connecting to {host}:{port} (timeout={timeout}, retries={retries})")

connect("localhost", 8080, timeout=60)
# connect("localhost", 8080, 60)  # This would raise TypeError!

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Arguments.py
# =============================================================================
#
# ==================================================
#    ARGUMENTS DEEP DIVE
# ==================================================
#
# [1] Positional arguments (order matters)
#   Tommy is a dog
#   dog is a Tommy
#   ^ Notice: no error, just wrong logic. This is dangerous!
#
# [2] Keyword arguments (order doesn't matter)
#   Tommy is a dog
#   Whiskers is a cat
#
# [3] Default arguments
#   Pavan, 22 years old, from India
#   John, 30 years old, from USA
#
# [4] *args in depth
#   Received args as tuple: (100, 250, 75)
#   Total of (100, 250, 75): 425
#   Received args as tuple: (50,)
#   Total of (50,): 50
#   Received args as tuple: (10, 20, 30, 40)
#   Unpacking a list with *: 100
#
# [5] **kwargs in depth
#   Received kwargs as dict: {'name': 'Pavan', 'role': 'Engineer', 'city': 'Mangalore'}
#     name = Pavan
#     role = Engineer
#     city = Mangalore
#   Unpacking a dict with **:
#   Received kwargs as dict: {'name': 'Sneha', 'role': 'Developer', 'city': 'Bangalore'}
#     name = Sneha
#     role = Developer
#     city = Bangalore
#
# [6] Combining everything (correct order)
#   a=1, b=2
#   args=(3, 4, 5)
#   c=99
#   kwargs={'extra1': 'x', 'extra2': 'y'}
#
# [7] Forcing keyword-only arguments
#   Connecting to localhost:8080 (timeout=60, retries=3)
#
# ==================================================
#
# =============================================================================

