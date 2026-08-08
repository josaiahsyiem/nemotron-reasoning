"""Solver for equation transformation puzzles.

The hardest type — each puzzle defines its own substitution rule via 3-4
examples using symbols (#]+\\# = "!) or pseudo-digits (82/15 = 8241).
Answers are short exact strings.

Key structural insight: the MIDDLE character of each 5-char input is an
"operator" that determines which transformation applies. Examples sharing
the target's operator reveal the specific rule. augment_prompt focuses the
model on those examples instead of averaging across all of them.

verify stays strict (every character significant); no full solver — this
type is genuinely underdetermined, so we guide the model rather than crack it.
"""

import re


def _trim(text):
    if text is None:
        return ""
    s = str(text).strip()
    for q in ('"', "'", "`"):
        if len(s) >= 2 and s[0] == q and s[-1] == q:
            s = s[1:-1].strip()
            break
    return s


def _parse(prompt):
    """Return (examples, target) where examples is list of (input, output)."""
    examples = []
    target = ""
    for line in prompt.splitlines():
        if "=" in line and "determine" not in line.lower():
            parts = line.split("=", 1)
            left = parts[0].strip().strip("`")
            right = parts[1].strip().strip("`")
            if left and right:
                examples.append((left, right))
    m = re.search(r"result for:\s*(.+)", prompt)
    if m:
        target = m.group(1).strip().strip("`")
    return examples, target


class EquationSolver:
    type_name = "equation_transformation"

    def verify(self, predicted, answer):
        if predicted is None:
            return False
        return _trim(predicted) == _trim(answer)

    def augment_prompt(self, prompt):
        """Focus the model on same-operator examples via a structural hint."""
        examples, target = _parse(prompt)
        if not target or len(target) < 3:
            return prompt

        target_op = target[len(target) // 2]  # middle char = operator

        # find examples that share the target's operator
        same_op = [
            (inp, out) for inp, out in examples
            if len(inp) >= 3 and inp[len(inp) // 2] == target_op
        ]

        hint = (
            "\n\nHINT: The middle character of each input is an OPERATOR that "
            "decides the transformation rule. Different operators follow "
            f"different rules. The target's operator is '{target_op}'. "
        )
        if same_op:
            pairs = "; ".join(f"{i} -> {o}" for i, o in same_op)
            hint += (
                f"Focus ONLY on the examples with the same operator '{target_op}': "
                f"{pairs}. Find the exact rule those follow and apply it to the "
                "target. Ignore examples with other operators."
            )
        else:
            hint += (
                "No example shares this exact operator, so infer the rule from "
                "the closest patterns. "
            )
        hint += " Give the result in \\boxed{}."
        return prompt + hint
