"""Shared helper for solvers whose answers are numbers.

Used by both unit conversion and gravitational constant: compare two
values as numbers within a small tolerance.
"""

import re


def to_number(text: str):
    """Pull the first number out of a string, or return None."""
    if text is None:
        return None
    match = re.search(r"-?\d+\.?\d*", str(text))
    if match is None:
        return None
    return float(match.group())


def numbers_match(predicted: str, answer: str) -> bool:
    """True if predicted is within tolerance of answer (0.05 abs or 0.5% rel)."""
    p = to_number(predicted)
    a = to_number(answer)
    if p is None or a is None:
        return False
    return abs(p - a) <= max(0.05, abs(a) * 0.005)
