"""Quick tests for the gravitational solver + confirm unit still works."""

from vcd.solvers.gravitational import GravitationalSolver
from vcd.solvers.unit import UnitSolver

g = GravitationalSolver()
assert g.verify("154.62", "154.62") is True
assert g.verify("154.60", "154.62") is True      # rounding ok
assert g.verify("150.0", "154.62") is False      # wrong
assert g.verify(None, "154.62") is False

u = UnitSolver()
assert u.verify("16.65 m", "16.65") is True       # still works after refactor

print("All gravitational + unit solver tests passed!")
