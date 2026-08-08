"""Run the type detector across train.csv and report the counts."""

import csv
from collections import Counter

from vcd.detect import detect_type

counts = Counter()
unknown_examples = []

with open("train.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        t = detect_type(row["prompt"])
        counts[t] += 1
        # stash a few unknowns so we can read them
        if t == "unknown" and len(unknown_examples) < 5:
            unknown_examples.append(row["prompt"][:200])

print("Type counts:")
for type_name, n in counts.most_common():
    print(f"  {type_name:28s} {n}")

print(f"\nTotal puzzles: {sum(counts.values())}")

if unknown_examples:
    print(f"\n--- {counts['unknown']} unknown; first few starts: ---")
    for ex in unknown_examples:
        print("•", ex.replace("\n", " "), "\n")
