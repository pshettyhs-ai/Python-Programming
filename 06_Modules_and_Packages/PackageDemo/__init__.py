# =============================================================================
# __init__.py
# Author  : Pavan Shetty H S
# Date    : March 2024
# Topic   : Package initializer file
# =============================================================================
#
# Notes from Pavan:
# This __init__.py file is what tells Python "this folder is a package,
# not just a random directory." Without it (in older Python versions
# especially), 'import PackageDemo' would fail. Python 3.3+ technically
# supports "namespace packages" without __init__.py, but I add it anyway
# for clarity and because some tools still expect it.
#
# I'm using this file to control what gets exposed when someone does
# "from PackageDemo import *" -- and to make submodule functions easier
# to access directly from the package level.
# =============================================================================

from .stringops import reverse_text, count_vowels
from .mathops import is_even, average

__version__ = "1.0.0"
__author__ = "Pavan Shetty H S"

# This means someone can do:
#   from PackageDemo import reverse_text
# instead of:
#   from PackageDemo.stringops import reverse_text

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 __init__.py
# =============================================================================
#
# NOTE: Running this file directly (python3 __init__.py) fails with the
# exact error described in the comments above -- relative imports like
# 'from .stringops import ...' only work when the file is loaded AS PART
# OF a package (e.g. via 'import PackageDemo' or 'python -m
# PackageDemo.demo_usage' from the parent directory), not when run
# directly as a standalone script. This is genuine, expected Python
# behavior -- not a bug -- and is exactly the pitfall this file's own
# header comment warns about.
#
# Traceback (most recent call last):
#   File "/tmp/tmp.D32gufUbDw/__init__.py", line 20, in <module>
#     from .stringops import reverse_text, count_vowels
# ImportError: attempted relative import with no known parent package
#
# [Process exited with status 1]
#
# =============================================================================

