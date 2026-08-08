"""Harvest the puzzle vocabulary from all training answers.

Text-encryption answers are English words drawn from a fixed vocabulary.
Collecting every word that appears in the answer column gives us the exact
word list needed to fill single-letter gaps when cracking ciphers.
"""

import pandas as pd


def harvest_vocab(csv_path="train.csv"):
    """Return the set of all words appearing in the answers column."""
    df = pd.read_csv(csv_path)
    vocab = set()
    for answer in df["answer"].astype(str):
        # only keep alphabetic words (skip numbers, roman numerals, symbols)
        for word in answer.lower().split():
            if word.isalpha():
                vocab.add(word)
    return vocab
