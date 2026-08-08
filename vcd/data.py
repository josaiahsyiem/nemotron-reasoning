"""Load the competition puzzles as a pandas table, with type attached.

train.csv has: id, prompt, answer  (no type column).
This adds a 'type' column using the detector, so the rest of the
project always works with typed puzzles.
"""

import pandas as pd

from vcd.detect import detect_type


def load_puzzles(csv_path: str = "train.csv") -> pd.DataFrame:
    """Read the puzzle CSV and return it with a detected 'type' column."""
    df = pd.read_csv(csv_path)

    # sanity check: fail loudly if the columns aren't what we expect
    expected = {"id", "prompt", "answer"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"train.csv is missing columns: {missing}")

    # add the type column by running the detector on each prompt
    df["type"] = df["prompt"].apply(detect_type)

    return df
