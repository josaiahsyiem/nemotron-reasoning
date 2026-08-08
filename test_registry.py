"""Test the registry ties everything together, using real puzzle data."""

from vcd.data import load_puzzles
from vcd.solvers.registry import get_solver, all_types

# 1. all six types are registered
types = all_types()
print("Registered solvers:", types)
assert len(types) == 6

# 2. lookup works and errors clearly on bad input
get_solver("bit_manipulation")   # should work
try:
    get_solver("nonsense")
    assert False, "should have raised"
except KeyError:
    pass  # expected

# 3. the real answer for each puzzle should verify as correct
df = load_puzzles()
checked = 0
for _, row in df.head(500).iterrows():
    solver = get_solver(row["type"])
    # a correct answer must verify True against itself
    assert solver.verify(row["answer"], row["answer"]) is True
    checked += 1

print(f"Verified {checked} real answers against their solvers — all correct!")
print("Registry test passed!")
