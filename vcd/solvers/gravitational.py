"""Solver for gravitational constant puzzles (falling distance).

Answers are plain decimal numbers, so we reuse the shared numeric check.
"""

from vcd.solvers.numeric import numbers_match


class GravitationalSolver:
    type_name = "gravitational_constant"

    def verify(self, predicted: str, answer: str) -> bool:
        return numbers_match(predicted, answer)
