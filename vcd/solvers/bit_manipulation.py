"""Solver for bit-manipulation puzzles (8-bit input -> 8-bit output).

Learns each output bit as a boolean function of the input bits by searching
a library of candidate functions (constants, single bits, NOT, XOR/AND/OR of
pairs, majority and XOR of triples) against the examples.

If all 8 bits are pinned down, the puzzle is solved fully in Python.
Otherwise generate_trace() emits the bits it DID find as a strong hint and
leaves the rest for the model.
"""

import re
from itertools import combinations


def _to_bits(s):
    return [int(c) for c in str(s).strip() if c in "01"]


def _from_bits(b):
    return "".join(map(str, b))


def _clean_bits(text):
    if text is None:
        return ""
    s = str(text).strip().lower().replace("0b", "")
    return re.sub(r"[^01]", "", s)


def _candidates(n_in=8):
    """Yield (name, fn) boolean-function candidates over the input bits."""
    yield ("0", lambda x: 0)
    yield ("1", lambda x: 1)
    for i in range(n_in):
        yield (f"in[{i}]", lambda x, i=i: x[i])
        yield (f"NOT in[{i}]", lambda x, i=i: 1 - x[i])
    for i, j in combinations(range(n_in), 2):
        yield (f"in[{i}]^in[{j}]", lambda x, i=i, j=j: x[i] ^ x[j])
        yield (f"in[{i}]&in[{j}]", lambda x, i=i, j=j: x[i] & x[j])
        yield (f"in[{i}]|in[{j}]", lambda x, i=i, j=j: x[i] | x[j])
        yield (f"NOT(in[{i}]^in[{j}])", lambda x, i=i, j=j: 1 - (x[i] ^ x[j]))
    for i, j, k in combinations(range(n_in), 3):
        yield (f"maj({i},{j},{k})", lambda x, i=i, j=j, k=k: 1 if (x[i] + x[j] + x[k]) >= 2 else 0)
        yield (f"in[{i}]^in[{j}]^in[{k}]", lambda x, i=i, j=j, k=k: x[i] ^ x[j] ^ x[k])


def _parse_examples(prompt):
    """Pull (input, output) bit-string pairs from the prompt."""
    pairs = []
    for line in prompt.splitlines():
        m = re.search(r"([01]{8})\s*->\s*([01]{8})", line)
        if m:
            pairs.append((m.group(1), m.group(2)))
    return pairs


def _find_target(prompt):
    m = re.search(
        r"determine the output for:\s*([01]{8})", prompt, re.IGNORECASE)
    return m.group(1) if m else ""


def _solve_bits(examples):
    """Return list of (name, fn) per output bit; (None, None) where unsolved."""
    ins = [_to_bits(i) for i, o in examples]
    outs = [_to_bits(o) for i, o in examples]
    funcs = []
    for ob in range(8):
        col = [outs[e][ob] for e in range(len(ins))]
        found = (None, None)
        for name, fn in _candidates():
            if all(fn(ins[e]) == col[e] for e in range(len(ins))):
                found = (name, fn)
                break
        funcs.append(found)
    return funcs


class BitManipulationSolver:
    type_name = "bit_manipulation"

    def verify(self, predicted, answer):
        p, a = _clean_bits(predicted), _clean_bits(answer)
        if not p or not a:
            return False
        return p == a

    def solve(self, prompt):
        """Return (answer_or_None, funcs). answer is set only if all 8 solved."""
        examples = _parse_examples(prompt)
        target = _find_target(prompt)
        funcs = _solve_bits(examples)
        if any(fn is None for _, fn in funcs) or not target:
            return None, funcs
        tin = _to_bits(target)
        return _from_bits([fn(tin) for _, fn in funcs]), funcs

    def generate_trace(self, prompt):
        """Worked-example trace. Full answer if solvable, else partial hint."""
        answer, funcs = self.solve(prompt)
        lines = [f"out[{i}] = {name if name else '(unknown, infer from examples)'}"
                 for i, (name, _) in enumerate(funcs)]
        rule = "; ".join(lines)
        if answer:
            trace = (
                f"Analyzing each output bit as a function of the input bits: {rule}. "
                f"Applying these to the target input gives \\boxed{{{answer}}}."
            )
            return trace, answer
        # partial: hand over what we found
        trace = (
            f"Analyzing each output bit: {rule}. "
            f"Use the identified bit functions and infer the unknown bits from "
            f"the examples, then output the 8-bit result in \\boxed{{}}."
        )
        return trace, None
