# 📒 Module 06 — Modules and Packages: My Notes

**Started:** Mar 25, 2024
**Finished:** Apr 1, 2024
**Time spent:** ~9 hours

---

## What I learned this module

This module changed how I structure my code entirely. Before this, every
exercise was a single standalone .py file. Now I understand how to split
logic across files and folders properly, which became essential once my
projects (starting Module 15) grew beyond a couple hundred lines.

### Key realizations

1. **A module is just a .py file. A package is a folder with `__init__.py`.**
   I overcomplicated this in my head before actually trying it. No special
   "module declaration" syntax needed, unlike C's separate header/source
   files with their own compilation units.

2. **`if __name__ == "__main__":` is genuinely important, not just
   boilerplate I copy-pasted without understanding.** When a file is run
   directly, `__name__` is `"__main__"`. When it's imported, `__name__`
   becomes the module's actual name. This lets me write test/demo code
   that runs when I execute the file directly but stays silent when
   someone else imports my functions. Before understanding this, I had a
   module where importing it would trigger a bunch of print statements
   meant only for my own testing — embarrassing bug to discover.

3. **Relative imports inside packages are genuinely tricky to get right.**
   I hit `ImportError: attempted relative import with no known parent
   package` repeatedly when trying to run `demo_usage.py` directly with
   `python demo_usage.py` from inside the PackageDemo folder. The fix:
   run it as a module from the PARENT directory using
   `python -m PackageDemo.demo_usage`. This "run as module vs run as
   script" distinction is something I wish someone had explained to me
   up front instead of me discovering it through 30 minutes of error
   messages.

4. **`__init__.py` can selectively expose functions from submodules.**
   By writing `from .stringops import reverse_text` inside `__init__.py`,
   users of my package can do `from PackageDemo import reverse_text`
   instead of the longer `from PackageDemo.stringops import reverse_text`.
   Small thing but makes package APIs feel cleaner.

5. **`pip` and PyPI is how third-party packages work**, separate from the
   modules/packages I write myself. I installed my first external package
   (`requests`) this week just to see how `pip install` works, even
   though I won't really use it until Module 12.

---

## Mistakes & Debugging Log

| Issue | What happened | How I fixed it |
|---|---|---|
| ImportError on relative import | Ran demo_usage.py directly as a script | Ran with `python -m PackageDemo.demo_usage` from parent dir instead |
| Module-level print statements firing on import | Forgot `if __name__ == "__main__":` guard | Wrapped test/demo code in the guard |
| ModuleNotFoundError | Tried importing a module not in the same directory or PYTHONPATH | Either moved file or adjusted working directory |
| Circular import confusion | Two modules tried importing from each other | Restructured so shared logic lives in a third, lower-level module |

---

## Lessons learned after this module

- Keep modules focused — one module shouldn't do everything (learned this
  from trying to cram math AND string operations into a single file
  before splitting them into stringops.py and mathops.py)
- Always guard demo/test code with `if __name__ == "__main__":`
- Understand the difference between running a file as a script vs as a
  module — this distinction actually matters for imports
- `__init__.py` is a good place to define a clean public API for a package

Next up: File Handling — finally going to make programs that persist data
between runs instead of losing everything when the script ends.
