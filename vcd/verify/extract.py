"""Pull the final answer out of a model's response.

The model puts its answer inside \\boxed{...}. This finds the LAST such box
(in case the format is mentioned earlier) and returns what's inside it,
handling nested braces correctly.
"""

_BOXED = r"\boxed{"


def extract_boxed(text: str):
    """Return the content of the last \\boxed{...}, or None if there isn't one."""
    if not text:
        return None

    start = text.rfind(_BOXED)
    if start == -1:
        return None

    i = start + len(_BOXED)
    depth = 1
    out = []
    while i < len(text) and depth > 0:
        ch = text[i]
        if ch == "{":
            depth += 1
            out.append(ch)
        elif ch == "}":
            depth -= 1
            if depth > 0:
                out.append(ch)
        else:
            out.append(ch)
        i += 1

    if depth != 0:      # unfinished \boxed{ with no closing brace
        return None
    return "".join(out).strip()
