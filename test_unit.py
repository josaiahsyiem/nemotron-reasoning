"""Quick tests for the unit solver."""

from vcd.solvers.unit import UnitSolver

s = UnitSolver()

# exact match
assert s.verify("16.65", "16.65") is True

# extra decimal places are fine
assert s.verify("16.650", "16.65") is True

# stray unit is stripped
assert s.verify("16.65 m", "16.65") is True

# tiny rounding difference is accepted
assert s.verify("16.64", "16.65") is True

# clearly wrong number fails
assert s.verify("20.0", "16.65") is False

# no prediction fails
assert s.verify(None, "16.65") is False

print("All unit solver tests passed!")
