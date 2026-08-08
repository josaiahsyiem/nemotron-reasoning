"""Detect a puzzle's type from its prompt text.

The competition train.csv only has id, prompt, answer — no type column.
So we read the prompt wording to decide which of the six puzzle types it is.
If nothing matches, we return "unknown" so we can find missing wordings later.
"""


# Each type maps to a list of lowercase phrases that identify it.
# We check these in order; the first match wins.
TYPE_KEYWORDS = {
    "bit_manipulation": ["bit manipulation"],
    "text_encryption": ["encryption rules", "decrypt"],
    "numeral_conversion": ["numeral system"],
    "unit_conversion": ["unit conversion"],
    "gravitational_constant": ["gravitational", "gravity"],
    "equation_transformation": ["equation"],
}


def detect_type(prompt: str) -> str:
    """Return the puzzle type for a prompt, or 'unknown' if none matches."""
    text = prompt.lower()
    for type_name, keywords in TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return type_name
    return "unknown"