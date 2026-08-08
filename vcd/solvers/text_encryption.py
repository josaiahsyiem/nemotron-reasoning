"""Solver for text encryption puzzles (substitution cipher).

Cracks the cipher fully in Python:
  1. Build the letter-substitution key from the example pairs
  2. Decode the target word by word
  3. Fill single-letter gaps using the harvested vocabulary
  4. Leave genuinely-ambiguous words as '?' for the model to finish

generate_trace() produces a worked-example reasoning trace ending in
\\boxed{answer} — used as training data so the model learns the method.
"""

import re

_VOCAB = set()


def set_vocab(vocab):
    """Provide the word list used to fill cipher gaps."""
    global _VOCAB
    _VOCAB = set(w.lower() for w in vocab)


def _normalize(text):
    if text is None:
        return ""
    return " ".join(text.lower().split())


def _parse_examples(prompt):
    pairs = []
    for line in prompt.splitlines():
        if "->" in line:
            left, right = line.split("->", 1)
            c, p = left.strip(), right.strip()
            if c and p and "decrypt" not in c.lower():
                pairs.append((c, p))
    return pairs


def _build_key(pairs):
    key = {}
    for cipher, plain in pairs:
        cw, pw = cipher.split(), plain.split()
        if len(cw) != len(pw):
            continue
        for cwd, pwd in zip(cw, pw):
            if len(cwd) != len(pwd):
                continue
            for c, p in zip(cwd, pwd):
                key[c] = p
    return key


def _find_target(prompt):
    m = re.search(r"decrypt the following text:\s*(.+)", prompt, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def _decode_word(cword, key):
    return "".join(key.get(c, "?") for c in cword)


def _fill(pattern):
    """Resolve a '?'-containing pattern to a unique vocab word, or leave it.
    Returns (result, how, candidates)."""
    if "?" not in pattern:
        return pattern, "direct", []
    rx = re.compile("^" + pattern.replace("?", ".") + "$")
    matches = [w for w in _VOCAB if rx.match(w)]
    if len(matches) == 1:
        return matches[0], "unique", matches
    return pattern, "ambiguous", matches


class TextEncryptionSolver:
    type_name = "text_encryption"

    def verify(self, predicted, answer):
        if predicted is None:
            return False
        return _normalize(predicted) == _normalize(answer)

    def crack(self, prompt):
        """Return (decoded_string, key, steps) — the full solve."""
        pairs = _parse_examples(prompt)
        target = _find_target(prompt)
        key = _build_key(pairs)

        words, steps = [], []
        for cw in target.split():
            raw = _decode_word(cw, key)
            filled, how, cands = _fill(raw)
            words.append(filled)
            if how == "direct":
                steps.append(f"'{cw}' -> '{filled}'")
            elif how == "unique":
                steps.append(
                    f"'{cw}' -> '{raw}' -> '{filled}' (only fitting word)")
            else:
                opts = " or ".join(cands) if cands else "unknown"
                steps.append(
                    f"'{cw}' -> '{raw}' (candidates: {opts}; pick by context)")
        return " ".join(words), key, steps

    def generate_trace(self, prompt):
        """Produce a worked-example reasoning trace for training data."""
        decoded, key, steps = self.crack(prompt)
        key_str = ", ".join(f"{c}->{p}" for c, p in sorted(key.items()))
        trace = (
            f"This is a letter-substitution cipher. From the examples, "
            f"the letter mapping is: {key_str}. "
            f"Decoding the target word by word: " + "; ".join(steps) + ". "
            f"Therefore the answer is \\boxed{{{decoded}}}."
        )
        return trace, decoded
