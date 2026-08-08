"""Quick tests for the equation transformation solver."""

from vcd.solvers.equation import EquationSolver

s = EquationSolver()

# exact symbol match
assert s.verify("\\:", "\\:") is True

# pseudo-digit answer
assert s.verify("6644", "6644") is True

# outer whitespace trimmed
assert s.verify("  @&  ", "@&") is True

# wrapping quotes removed
assert s.verify('"@&"', "@&") is True

# internal characters are significant - this must FAIL
assert s.verify("\\ :", "\\:") is False

# wrong answer fails
assert s.verify("@#", "@&") is False

# no prediction fails
assert s.verify(None, "@&") is False

print("All equation solver tests passed!")
