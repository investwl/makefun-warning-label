#!/usr/bin/env python3
"""One Line of Earned Pride — generate, score, mutate, keep the champion line.

Entry for make.fun's bounty 'One Line of Earned Pride'.
Run: python3 main.py  ->  output/entry.txt
"""

import os
import re
import random

SEED = 20261124
ROUNDS = 10
KEEP = 5
OUT_DIR = "output"
OUT_FILE = os.path.join(OUT_DIR, "entry.txt")

# Each candidate: (text, {lowercase_keyword: score if found}, cap)
# `cap` is the max a line can ever score, so a short zinger can't be outrun
# by a paragraph that merely happens to contain every keyword.
CANDIDATES = [
    ("I didn't fail — I found 40 ways it doesn't work.", {"found": 3, "fail": 2, "proud": 4}, 12),
    ("Still standing. Mostly out of spite, but standing.", {"standing": 3, "proud": 4, "spite": 2}, 11),
    ("Earned it the hard way: on purpose, twice.", {"earned": 4, "hard": 2, "proud": 3}, 11),
    ("Zero shortcuts, one scar, fully worth it.", {"scar": 3, "worth": 3, "proud": 4}, 11),
    ("The plan survived. I did not stay the same.", {"plan": 2, "proud": 4, "survived": 3}, 11),
    ("It works. Don't ask what it cost me.", {"works": 3, "cost": 2, "proud": 4}, 10),
    ("Proud of the mess I made on purpose.", {"mess": 2, "proud": 5, "earned": 3}, 11),
    ("Blood, sweat, and one very smug commit.", {"smug": 3, "proud": 4, "earned": 2}, 11),
    ("Wore the badge. Earning it took longer.", {"badge": 3, "earned": 4, "proud": 4}, 11),
    ("I built it, broke it, built it better.", {"built": 3, "better": 2, "proud": 4}, 11),
    ("Nobody clapped, so I clapped for myself.", {"clapped": 3, "proud": 4, "earned": 3}, 11),
    ("Earned pride: 100% self-supplied.", {"pride": 4, "earned": 4, "proud": 4}, 12),
    ("Not lucky. Just stubborn for a very long time.", {"stubborn": 3, "proud": 4, "earned": 2}, 11),
]


def score(text, rating, cap):
    """Max rating among keywords present (case-insensitive) + digit + brevity."""
    low = text.lower()
    base = 0
    for kw, val in rating.items():
        if kw in low:
            base = max(base, val)
    s = base
    if re.search(r"\d", text):
        s += 2  # a concrete number reads as a specific, earned detail
    words = len(text.split())
    if words <= 7:
        s += 3  # brevity bonus: punchy line
    elif words <= 9:
        s += 1
    return min(s, cap)


def mutate(text, rng):
    """Light phrasing mutants — same joke, slightly different clothes."""
    m = rng.choice([
        lambda t: t.replace("I didn't", "I never"),
        lambda t: t.replace("It works", "And it works"),
        lambda t: t.replace(" — ", ", "),
        lambda t: t.replace("Proud", "Proud,"),
        lambda t: t.replace("very ", "really "),
        lambda t: t.replace("one ", "a single "),
        lambda t: t.rstrip(".") + " Indeed.",
        lambda t: t.rstrip(".") + ".",
        lambda t: t,
        lambda t: t,
    ])
    out = m(text).strip()
    if not out.endswith((".", "!", "?")):
        out += "."
    return out


def run():
    rng = random.Random(SEED)
    pool = [(t, r, c, score(t, r, c)) for t, r, c in CANDIDATES]
    best = max(pool, key=lambda x: x[3])

    for rnd in range(1, ROUNDS + 1):
        pool.sort(key=lambda x: x[3], reverse=True)
        seeds = pool[:KEEP]
        kids = [(mutate(t, rng), r, c, 0) for t, r, c, _ in seeds]
        kids = [(t, r, c, score(t, r, c)) for t, r, c, _ in kids]
        pool = seeds + kids
        round_best = max(pool, key=lambda x: x[3])
        if round_best[3] > best[3]:
            best = round_best
        print(f"round {rnd:2d}: best={best[3]} ({best[0]})")

    return best


def main():
    best = run()
    os.makedirs(OUT_DIR, exist_ok=True)
    line = best[0]
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(line + "\n")
    print("\nWINNER:", line)
    print("score:", best[3])


if __name__ == "__main__":
    main()
