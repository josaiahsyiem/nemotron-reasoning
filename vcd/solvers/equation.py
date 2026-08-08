"""Solver for equation transformation puzzles.

These are the hardest type: each puzzle defines its own substitution rule
via 3-4 examples, using symbols (#]+\\# = "!) or pseudo-digits (82/15 = 8241).
Answers are short exact strings like "\\:", "@&", or "6644".

This is the VERIFY half only, and on purpose it stays strict: unlike the
word puzzles we do NOT lowercase or touch internal characters, because in a
symbol puzzle every character is significant. We only trim outer whitespace
and any surrounding quotes the model might wrap the answer in.

The hard part -- a real solver that cracks each puzzle's rule -- is deferred
to a later, separate effort (see project notes).
"""


def _trim(text: str) -> str:
    """Strip outer whitespace and a single layer of surrounding quotes."""
    if text is None:
        return ""
    s = str(text).strip()
    # remove one layer of wrapping quotes if present
    for q in ('"', "'", "`"):
        if len(s) >= 2 and s[0] == q and s[-1] == q:
            s = s[1:-1].strip()
            break
    return s


class EquationSolver:
    type_name = "equation_transformation"

    def verify(self, predicted: str, answer: str) -> bool:
        """Strict exact match after trimming outer whitespace/quotes only."""
        if predicted is None:
            return False
        return _trim(predicted) == _trim(answer)
