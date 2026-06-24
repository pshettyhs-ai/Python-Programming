# =============================================================================
# Loops.py
# Author  : Pavan Shetty H S
# Date    : January 2024
# Topic   : for loop, while loop, range(), nested loops
# =============================================================================
#
# Notes from Pavan:
# range() confused me initially. range(5) gives 0,1,2,3,4 — NOT including 5.
# Classic off-by-one trap, especially coming from C's "for(i=0; i<=5; i++)"
# style where I'd consciously decide the boundary. Here it's baked into the
# function so I had to retrain my brain.
#
# =============================================================================

print("=" * 50)
print("       LOOPS DEMO")
print("=" * 50)

# ---------------------
# Basic for loop with range()
# ---------------------
print("\n[1] range(5) -- prints 0 to 4, NOT 0 to 5")
for i in range(5):
    print(f"  i = {i}")

print("\n[2] range(1, 6) -- start, stop (exclusive)")
for i in range(1, 6):
    print(f"  i = {i}")

print("\n[3] range(0, 10, 2) -- start, stop, step")
for i in range(0, 10, 2):
    print(f"  i = {i}")

print("\n[4] range(10, 0, -1) -- counting down")
for i in range(10, 0, -1):
    print(f"  i = {i}", end=" ")
print()

# ---------------------
# for loop over collections
# ---------------------
print("\n[5] for loop over a list")
skills = ["Python", "C", "Embedded C", "Arduino"]
for skill in skills:
    print(f"  Skill: {skill}")

print("\n[6] enumerate() -- get index AND value together")
for index, skill in enumerate(skills):
    print(f"  [{index}] {skill}")

print("\n[7] for loop over a dictionary")
student = {"name": "Pavan", "branch": "ECE", "cgpa": 8.5}
for key, value in student.items():
    print(f"  {key}: {value}")

# ---------------------
# while loop
# ---------------------
print("\n[8] while loop -- countdown")
count = 5
while count > 0:
    print(f"  Countdown: {count}")
    count -= 1
print("  Liftoff!")

# ---------------------
# while True with break (common pattern for menus)
# ---------------------
print("\n[9] while True with break -- simulating a menu loop")
attempts = 0
while True:
    attempts += 1
    # Simulating user input for demo purposes
    simulated_input = attempts  # pretend user entered their attempt number
    print(f"  Attempt #{attempts}")
    if attempts >= 3:
        print("  Max attempts reached, breaking out.")
        break

# ---------------------
# Nested loops -- multiplication table
# ---------------------
print("\n[10] Nested loops -- multiplication table (1-5)")
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:4}", end="")
    print()  # newline after each row

# ---------------------
# else clause on loops (Python-specific feature!)
# ---------------------
# This confused me a LOT initially. The else block runs if the loop
# completes WITHOUT hitting a break.
print("\n[11] for-else -- runs else only if loop completes without break")

numbers = [2, 4, 6, 8, 10]
search_for = 7

for num in numbers:
    if num == search_for:
        print(f"  Found {search_for}!")
        break
else:
    print(f"  {search_for} not found in list (else block executed)")

print("\n" + "=" * 50)

# =============================================================================
# PROGRAM OUTPUT
# Run with: python3 Loops.py
# =============================================================================
#
# ==================================================
#        LOOPS DEMO
# ==================================================
#
# [1] range(5) -- prints 0 to 4, NOT 0 to 5
#   i = 0
#   i = 1
#   i = 2
#   i = 3
#   i = 4
#
# [2] range(1, 6) -- start, stop (exclusive)
#   i = 1
#   i = 2
#   i = 3
#   i = 4
#   i = 5
#
# [3] range(0, 10, 2) -- start, stop, step
#   i = 0
#   i = 2
#   i = 4
#   i = 6
#   i = 8
#
# [4] range(10, 0, -1) -- counting down
#   i = 10   i = 9   i = 8   i = 7   i = 6   i = 5   i = 4   i = 3   i = 2   i = 1 
#
# [5] for loop over a list
#   Skill: Python
#   Skill: C
#   Skill: Embedded C
#   Skill: Arduino
#
# [6] enumerate() -- get index AND value together
#   [0] Python
#   [1] C
#   [2] Embedded C
#   [3] Arduino
#
# [7] for loop over a dictionary
#   name: Pavan
#   branch: ECE
#   cgpa: 8.5
#
# [8] while loop -- countdown
#   Countdown: 5
#   Countdown: 4
#   Countdown: 3
#   Countdown: 2
#   Countdown: 1
#   Liftoff!
#
# [9] while True with break -- simulating a menu loop
#   Attempt #1
#   Attempt #2
#   Attempt #3
#   Max attempts reached, breaking out.
#
# [10] Nested loops -- multiplication table (1-5)
#    1   2   3   4   5
#    2   4   6   8  10
#    3   6   9  12  15
#    4   8  12  16  20
#    5  10  15  20  25
#
# [11] for-else -- runs else only if loop completes without break
#   7 not found in list (else block executed)
#
# ==================================================
#
# =============================================================================

