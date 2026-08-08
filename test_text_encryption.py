"""Quick tests for the text encryption solver."""

from vcd.solvers.text_encryption import TextEncryptionSolver

s = TextEncryptionSolver()

# exact match
assert s.verify("cat imagines book", "cat imagines book") is True

# case and messy spacing ignored
assert s.verify("Cat  Imagines   Book", "cat imagines book") is True

# wrong words fail
assert s.verify("dog imagines book", "cat imagines book") is False

# no prediction fails
assert s.verify(None, "cat imagines book") is False

print("All text encryption solver tests passed!")
