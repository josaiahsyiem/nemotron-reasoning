"""Solver for text encryption puzzles (substitution cipher).

Example: "trb wzrswvog hffk" decrypts to "cat imagines book".
Answers are lowercase English words separated by single spaces.

verify: exact match, case/space-insensitive.
augment_prompt: builds the letter-substitution key from the example pairs,
    decodes what it can, and hands the model a near-complete answer to finish.
    Python does the mechanical decoding; the model fills letters the examples
    didn't cover, using English word knowledge.
"""

import re


def _normalize(text):
    if text is None:
        return ""
    return " ".join(text.lower().split())


def _parse_examples(prompt):
    """Pull (cipher, plain) pairs from the 'cipher -> plain' example lines."""
    pairs = []
    for line in prompt.splitlines():
        if "->" in line:
            left, right = line.split("->", 1)
            cipher = left.strip()
            plain = right.strip()
            # skip the 'Now, decrypt...' line and anything without real text
            if cipher and plain and "decrypt" not in cipher.lower():
                pairs.append((cipher, plain))
    return pairs


def _build_key(pairs):
    """Align example pairs letter-by-letter to build cipher->plain map."""
    key = {}
    for cipher, plain in pairs:
        cw, pw = cipher.split(), plain.split()
        if len(cw) != len(pw):
            continue
        for c_word, p_word in zip(cw, pw):
            if len(c_word) != len(p_word):
                continue
            for c_ch, p_ch in zip(c_word, p_word):
                key[c_ch] = p_ch
    return key


def _find_target(prompt):
    """Extract the phrase after 'Now, decrypt the following text:'."""
    m = re.search(r"decrypt the following text:\s*(.+)", prompt, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def _decode(text, key):
    """Apply key; unknown letters become '?'."""
    return "".join(" " if ch == " " else key.get(ch, "?") for ch in text)


class TextEncryptionSolver:
    type_name = "text_encryption"

    def verify(self, predicted, answer):
        if predicted is None:
            return False
        return _normalize(predicted) == _normalize(answer)

    def augment_prompt(self, prompt):
        """Add a decoded-cipher hint to help the model solve reliably."""
        pairs = _parse_examples(prompt)
        target = _find_target(prompt)
        if not pairs or not target:
            return prompt  # can't parse — leave prompt unchanged

        key = _build_key(pairs)
        partial = _decode(target, key)

        # format the letter key readably
        key_str = ", ".join(f"{c}->{p}" for c, p in sorted(key.items()))

        hint = (
            "\n\nThis is a letter-substitution cipher. The letters have already "
            "been decoded for you using the example mappings. "
            f"The decoded text is: '{partial}'\n"
            "The only unknowns are the '?' characters (letters not in the examples). "
            "The rest of the decoding is CORRECT and must NOT be changed. "
            "Keep every decoded letter exactly as shown, and replace ONLY each '?' "
            "with the single letter that makes a valid English word. "
            "For example, 'wi?ard' becomes 'wizard', '?oo?' becomes 'book'. "
            "Do not rewrite or re-guess whole words."
        )
        return prompt + hint
