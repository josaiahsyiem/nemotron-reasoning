"""Solver for unit conversion puzzles (e.g. 25.09 m -> 16.65).

Answers are plain decimal numbers, checked with the shared numeric helper.
"""

from vcd.solvers.numeric import numbers_match


class UnitSolver:
    type_name = "unit_conversion"

    def verify(self, predicted: str, answer: str) -> bool:
        return numbers_match(predicted, answer)
