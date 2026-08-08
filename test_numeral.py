"""Quick tests for the numeral solver."""

from vcd.solvers.numeral import NumeralSolver

s = NumeralSolver()

# should pass — exact match
assert s.verify("XXXVIII", "XXXVIII") is True

# should pass — case and spaces ignored
assert s.verify("  xxxviii  ", "XXXVIII") is True

# should fail — wrong answer
assert s.verify("XXXIX", "XXXVIII") is False

# should fail — no prediction
assert s.verify(None, "XXXVIII") is False

print("All numeral solver tests passed!")
