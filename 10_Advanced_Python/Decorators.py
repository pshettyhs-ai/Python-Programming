# =============================================================================
# Decorators.py
# Author  : Pavan Shetty H S
# Date    : June 2024
# Topic   : Function Decorators
# =============================================================================
#
# Notes from Pavan:
# Decorators broke my brain for about 3 days. The @ syntax looked like
# magic until I understood it's literally just "pass my function into
# another function, and replace the original name with whatever comes
# back." Once I manually wrote out the equivalent without @ syntax,
# it clicked properly.
# =============================================================================

import time
import functools

print("=" * 50)
print("    DECORATORS DEMO")
print("=" * 50)

# ---------------------
# Understanding decorators -- the manual way first
# ---------------------
print("\n[1] What @decorator REALLY means (no magic, just function wrapping)")

def my_decorator(func):
    def wrapper():
        print("  Before the function runs")
        func()
        print("  After the function runs")
    return wrapper

def say_hello():
    print("  Hello!")

# The @ syntax is just sugar for this:
decorated = my_decorator(say_hello)
decorated()

print("\n  Now using @ syntax (does the EXACT same thing):")

@my_decorator
def say_hi():
    print("  Hi!")

say_hi()   # this is actually calling wrapper(), which calls the original

# ---------------------
# Decorators with arguments -- needed *args, **kwargs to make generic
# ---------------------
print("\n[2] Decorator that works with ANY function signature")

def log_call(func):
    @functools.wraps(func)   # preserves original function's name/docstring
    def wrapper(*args, **kwargs):
        print(f"  Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} returned {result}")
        return result
    return wrapper

@log_call
def add(a, b):
    return a + b

@log_call
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

add(5, 3)
greet("Pavan", greeting="Welcome")

# ---------------------
# Why functools.wraps matters -- the bug I hit without it
# ---------------------
print("\n[3] Why functools.wraps matters")

def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper   # NOTE: no functools.wraps here

@bad_decorator
def my_function():
    """This is my function's docstring."""
    pass

print(f"  Without functools.wraps, my_function.__name__ = '{my_function.__name__}'")
print("  ^ Shows 'wrapper' instead of 'my_function' -- broke my debugging once")
print("  because stack traces showed 'wrapper' everywhere instead of real names!")

# ---------------------
# Practical decorator: Timing function execution
# ---------------------
print("\n[4] Practical: Timing decorator")

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"  {func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    total = sum(i**2 for i in range(1000000))
    return total

slow_function()

# ---------------------
# Practical decorator: Retry on failure (used this in WebScraping.py later)
# ---------------------
print("\n[5] Practical: Retry decorator")

def retry(max_attempts=3):
    """Decorator FACTORY -- takes arguments and returns the actual decorator.
    This nested structure confused me until I realized: @retry(3) first
    CALLS retry(3) which returns a decorator, THEN that decorator gets
    applied to the function."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"  Attempt {attempts} failed: {e}")
                    if attempts == max_attempts:
                        print(f"  All {max_attempts} attempts failed, giving up")
                        raise
            return None
        return wrapper
    return decorator

attempt_counter = {"count": 0}

@retry(max_attempts=3)
def unreliable_function():
    attempt_counter["count"] += 1
    if attempt_counter["count"] < 3:
        raise ConnectionError("Simulated network failure")
    return "Success!"

result = unreliable_function()
print(f"  Final result: {result}")

# ---------------------
# Stacking multiple decorators
# ---------------------
print("\n[6] Stacking multiple decorators (order matters!)")

@timer
@log_call
def compute(n):
    return sum(range(n))

print("  Decorators apply BOTTOM-UP: log_call wraps compute first,")
print("  then timer wraps THAT result. So timer's print statements")
print("  surround log_call's print statements:")
compute(100)

# ---------------------
# Built-in decorators I use constantly
# ---------------------
print("\n[7] Built-in decorators (@staticmethod, @classmethod, @property)")
print("  Covered these in detail in the OOP module (Encapsulation.py,")
print("  Constructors.py) -- @property for controlled attribute access,")
print("  @classmethod for alternative constructors, @staticmethod for")
print("  utility methods that don't need self or cls at all.")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Decorators.py
# =============================================================================
#
# ==================================================
#     DECORATORS DEMO
# ==================================================
#
# [1] What @decorator REALLY means (no magic, just function wrapping)
#   Before the function runs
#   Hello!
#   After the function runs
#
#   Now using @ syntax (does the EXACT same thing):
#   Before the function runs
#   Hi!
#   After the function runs
#
# [2] Decorator that works with ANY function signature
#   Calling add with args=(5, 3), kwargs={}
#   add returned 8
#   Calling greet with args=('Pavan',), kwargs={'greeting': 'Welcome'}
#   greet returned Welcome, Pavan!
#
# [3] Why functools.wraps matters
#   Without functools.wraps, my_function.__name__ = 'wrapper'
#   ^ Shows 'wrapper' instead of 'my_function' -- broke my debugging once
#   because stack traces showed 'wrapper' everywhere instead of real names!
#
# [4] Practical: Timing decorator
#   slow_function took 0.053548 seconds
#
# [5] Practical: Retry decorator
#   Attempt 1 failed: Simulated network failure
#   Attempt 2 failed: Simulated network failure
#   Final result: Success!
#
# [6] Stacking multiple decorators (order matters!)
#   Decorators apply BOTTOM-UP: log_call wraps compute first,
#   then timer wraps THAT result. So timer's print statements
#   surround log_call's print statements:
#   Calling compute with args=(100,), kwargs={}
#   compute returned 4950
#   compute took 0.000012 seconds
#
# [7] Built-in decorators (@staticmethod, @classmethod, @property)
#   Covered these in detail in the OOP module (Encapsulation.py,
#   Constructors.py) -- @property for controlled attribute access,
#   @classmethod for alternative constructors, @staticmethod for
#   utility methods that don't need self or cls at all.
#
# ==================================================
#
# =============================================================================

