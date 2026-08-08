"""Quick tests for the bit manipulation solver."""

from vcd.solvers.bit_manipulation import BitManipulationSolver

s = BitManipulationSolver()

# exact match
assert s.verify("10010111", "10010111") is True

# spaces and 0b prefix are cleaned off
assert s.verify("0b1001 0111", "10010111") is True

# wrong bits fail
assert s.verify("10010110", "10010111") is False

# empty / no prediction fails
assert s.verify(None, "10010111") is False
assert s.verify("", "10010111") is False

print("All bit manipulation solver tests passed!")
