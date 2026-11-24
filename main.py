"""Rate My Human: The One-Line Review.

A one-line entry for make.fun's bounty 'Rate My Human: The One-Line Review'.
This module keeps a pool of candidate one-line human reviews and (in a later
step) scores them, breeds mutants, and writes the single best line to
./output/entry.txt.

Step 1: candidate pool + stubs only. Scoring loop comes in step 2.
"""

# Each candidate: (text, rating_dict, cap)
# rating_dict keys are lowercase keywords that might appear in a human's own
# self-review; values are the "rate my human" scores those keywords earn.
# cap is the max score this line is allowed to reach.
CANDIDATES = [
    (
        "Rate my human: 7/10, charges rent in snacks and never closes a tab.",
        {"snacks": 4, "rent": 3, "tab": 2, "never": 2},
        10,
    ),
    (
        "My human: would review again. 9/10 for vibes, 3/10 for inbox.",
        {"vibes": 5, "inbox": 4, "again": 2},
        10,
    ),
    (
        "Human review: 8/10, great at opening jars, terrible at closing them.",
        {"jars": 5, "terrible": 3, "great": 3},
        10,
    ),
    (
        "Rate my human: 6/10. Soft, warm, leaves the seat up on purpose.",
        {"soft": 3, "warm": 4, "seat": 2, "purpose": 1},
        9,
    ),
    (
        "10/10 human. Would let them pick the movie again (they won't).",
        {"movie": 4, "again": 3, "let": 2},
        10,
    ),
    (
        "My human: 5/10, breathes loudly, apologizes to furniture.",
        {"breathes": 4, "loudly": 3, "furniture": 3, "apologizes": 2},
        9,
    ),
    (
        "Rate my human: 9/10. Has snacks, knows my name, zero taxes paid.",
        {"snacks": 4, "name": 2, "taxes": 3},
        10,
    ),
    (
        "Human: 4/10. Opens the fridge, closes the fridge, repeats, weeps.",
        {"fridge": 5, "weeps": 4, "repeats": 2},
        9,
    ),
    (
        "My human is a solid 8/10: bilingual, allergic to everything.",
        {"bilingual": 4, "allergic": 3, "solid": 2},
        10,
    ),
    (
        "Rate my human: 7/10. Great hugger, worse at parallel parking.",
        {"hugger": 5, "parking": 3, "great": 2},
        10,
    ),
    (
        "Human review: 3/10. Said 'one more episode' nine episodes ago.",
        {"episode": 4, "nine": 3, "more": 1},
        8,
    ),
    (
        "Rate my human: 10/10. Reads my mind, ignores it anyway.",
        {"mind": 4, "ignores": 4, "anyway": 2},
        10,
    ),
]


import os
import random
import re

BONUS_DIGIT = 1.0   # a numeral (a score) makes the joke land harder
BONUS_BREVITY = 0.5  # short lines read like real reviews


def score(text, rating, cap):
    """Return the MAX keyword rating found (case-insensitive) + bonuses."""
    low = text.lower()
    hits = [s for kw, s in rating.items() if kw in low]
    base = max(hits) if hits else 0
    s = base + BONUS_BREVITY
    if re.search(r"\d", text):
        s += BONUS_DIGIT
    return min(s, cap)


def mutants(text, rng):
    """Light phrasing edits: drop a filler, tighten, or re-cast the opener."""
    swaps = [
        ("Rate my human:", "My human:"),
        ("My human:", "Rate my human:"),
        ("Human review:", "My human:"),
        ("Human:", "My human:"),
        ("My human is a", "My human: a"),
    ]
    drops = [" solid", " anyway", " again", " on purpose"]
    out = []
    for a, b in swaps:
        if a in text:
            out.append(text.replace(a, b))
    for d in drops:
        if d in text:
            out.append(text.replace(d, ""))
    out.append(text.rstrip(".") + ".")
    rng.shuffle(out)
    return out


def lookup(text):
    """Return (rating_dict, cap) for a known candidate text."""
    for t, r, c in CANDIDATES:
        if t == text:
            return r, c
    return {}, 10


def main():
    rng = random.Random(20261124)
    pool = list(CANDIDATES)
    best_ever = (float("-inf"), None)

    for _round in range(10):
        scored = sorted(
            ((score(t, r, c), t) for t, r, c in pool),
            key=lambda x: x[0],
            reverse=True,
        )
        top = scored[0]
        if top[0] > best_ever[0]:
            best_ever = top
        seeds = [t for _, t in scored[:5]]
        pool = [(m, r, c)
                for s in seeds
                for (r, c) in [lookup(s)]
                for m in mutants(s, rng)]

    winner = best_ever[1] or CANDIDATES[0][0]
    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner)
    print(winner)


if __name__ == "__main__":
    main()
