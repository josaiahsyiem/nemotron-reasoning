"""Solver for numeral conversion puzzles (e.g. 38 -> XXXVIII).

Verifying is simple: does the predicted Roman numeral match the answer,
ignoring case and surrounding whitespace?
"""


class NumeralSolver:
    type_name = "numeral_conversion"

    def verify(self, predicted: str, answer: str) -> bool:
        """Return True if the predicted numeral matches the answer."""
        if predicted is None:
            return False
        return predicted.strip().upper() == answer.strip().upper()
