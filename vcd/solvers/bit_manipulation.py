"""Solver for bit manipulation puzzles (e.g. 00110100 -> 10010111).

Answers are 8-bit binary strings. Models sometimes add spaces, a "0b"
prefix, or quotes, so we strip those out before comparing.

This is the VERIFY half only. The hint half (augment_prompt), which analyses
each output bit as a boolean function of the input bits, comes as a later step.
"""

import re


def _clean_bits(text: str) -> str:
    """Keep only 0s and 1s. Strips a leading 0b prefix first so its 0
    isn't mistaken for a data bit."""
    if text is None:
        return ""
    s = str(text).strip().lower()
    s = s.replace("0b", "")          # drop binary prefix before filtering
    return re.sub(r"[^01]", "", s)


class BitManipulationSolver:
    type_name = "bit_manipulation"

    def verify(self, predicted: str, answer: str) -> bool:
        """True if the predicted bits exactly match the answer bits."""
        p = _clean_bits(predicted)
        a = _clean_bits(answer)
        if not p or not a:
            return False
        return p == a
