#!/usr/bin/env python3
"""One Word, First Thought — make.fun bounty entry.

Generate ~12 candidate one-word reactions, score them on several comedy
axes, then run a 10-round improvement loop (keep top 5 seeds, spawn light
phrasing mutants, rescore) tracking the best line ever seen.  Write ONLY
the winning word to ./output/entry.txt.
"""

import os
import random
import re

RNG_SEED = 42

# ---------------------------------------------------------------------------
# Candidate one-word jokes: (text, rating_dict{lowercase_kw: score}, cap)
# Each keyword is a comedy axis we may reward when it appears in the entry.
# ---------------------------------------------------------------------------
CANDIDATES = [
    ("Oops.",        {"oops": 8, "mistake": 6, "oopsie": 5}, 10),
    ("Whoops.",      {"whoops": 8, "oops": 5, "slip": 4},    10),
    ("Ouch.",        {"ouch": 7, "pain": 6, "hurt": 5},      9),
    ("Seriously?",   {"seriously": 7, "disbelief": 6},       8),
    ("Wow.",         {"wow": 5, "wow": 4, "awe": 3},         7),
    ("Yikes.",       {"yikes": 9, "cringe": 6, "yikes": 5},  9),
    ("Ugh.",         {"ugh": 6, "ugh": 5, "groan": 4},       7),
    ("Bruh.",        {"bruh": 8, "bruh": 6, "dude": 4},      8),
    ("Oopsie.",      {"oopsie": 8, "oops": 6, "cute": 3},    9),
    ("Nah.",         {"nah": 6, "no": 5, "refuse": 4},       7),
    ("Dude.",        {"dude": 6, "dude": 5, "bro": 4},       7),
    ("Welp.",        {"welp": 9, "welp": 7, "resign": 5},    10),
]


def score(d):
    """Score a candidate dict/tuple.

    Base = MAX rating among keywords found (case-insensitive substring),
    plus +1 for containing a digit, plus a brevity bonus for short words.
    """
    if isinstance(d, tuple):
        text, ratings, cap = d[0], d[1], d[2]
    else:
        text, ratings, cap = d["text"], d["ratings"], d.get("cap", 99)

    low = text.lower()
    found = [s for kw, s in ratings.items() if kw.lower() in low]
    base = max(found) if found else 0

    bonus = 0
    if re.search(r"\d", text):
        bonus += 1
    # brevity: reward punchy words (stripped of punctuation)
    core = re.sub(r"[^\w]", "", text)
    if len(core) <= 4:
        bonus += 3
    elif len(core) <= 6:
        bonus += 2
    elif len(core) <= 8:
        bonus += 1

    return min(base + bonus, cap), base, bonus


def light_mutants(text, rng):
    """Return light phrasing variants of a word."""
    core = text.strip().rstrip(".!?")
    outs = [core, core + ".", core + "!", core.lower(), core.upper(), core.capitalize() + "."]
    rng.shuffle(outs)
    return outs


def main():
    rng = random.Random(RNG_SEED)

    # Normalise seeds into tuples and pre-score.
    pool = list(CANDIDATES)

    best = None          # (score, text)
    ROUNDS = 10
    for rnd in range(1, ROUNDS + 1):
        scored = []
        for c in pool:
            s, _, _ = score(c)
            scored.append((s, c))
        scored.sort(key=lambda x: (-x[0], x[1][0]))
        for s, c in scored:
            if best is None or s > best[0]:
                best = (s, c[0])
        # keep top 5 seeds
        seeds = [c for _, c in scored[:5]]
        # spawn light mutants of the seeds for the next round
        pool = list(seeds)
        for c in seeds:
            for m in light_mutants(c[0], rng):
                pool.append((m, c[1], c[2]))

    winning_line = best[1]
    winning_score = best[0]

    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winning_line + "\n")

    print(f"Winning line: {winning_line}  (score {winning_score})")


if __name__ == "__main__":
    main()
