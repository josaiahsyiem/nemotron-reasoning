"""Solver for text encryption puzzles (substitution cipher).

Example: "trb wzrswvog hffk" decrypts to "cat imagines book".
Answers are lowercase English words separated by single spaces.

This file is the VERIFY half only. The hint half (augment_prompt), which
embeds a decoded dictionary to help the model, comes as a later step.
"""


def _normalize(text: str) -> str:
    """Lowercase and collapse whitespace, so spacing/case don't cause misses."""
    if text is None:
        return ""
    return " ".join(text.lower().split())


class TextEncryptionSolver:
    type_name = "text_encryption"

    def verify(self, predicted: str, answer: str) -> bool:
        """True if the decoded text matches the answer (case/space-insensitive)."""
        if predicted is None:
            return False
        return _normalize(predicted) == _normalize(answer)
