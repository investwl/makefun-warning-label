#!/usr/bin/env python3
"""Two Lines of Morning Light — a make.fun entry generator.

The bounty asks for a single two-line micro poem about light and morning,
at most 120 characters, written as the whole entry. A judge model reads the
poems two at a time and picks the more beautiful one, weighing whether the
poem is really about light and morning, whether its two lines turn on one
image of light arriving, the freshness and exactness of the language, how it
sounds read aloud, and whether it leaves something unsaid.

This module authors a pool of candidate two-liners, scores each one, then
improves the pool over several rounds. The champion line is written to
``output/entry.txt``.

This file currently only defines the candidate pool and a stub; the scoring
logic and the improvement loop are added below.
"""

import os
import random

# (text, rating_dict{lowercase_keyword: score}, cap)
# The rating dict holds the scores for each lowercase keyword that could
# appear in the line; the scoring function takes the MAX among the keywords
# actually found (case-insensitive) and adds small bonuses.
CANDIDATES = [
    (
        "Morning leaned in and left its light on the sill.\nI forgot to lock the window.",
        {"sill": 6, "window": 5, "morning": 4, "light": 4, "forgot": 3},
        90,
    ),
    (
        "The curtain let one thin blade of morning through.\nIt fell across the bed like a held breath.",
        {"curtain": 5, "blade": 6, "morning": 4, "light": 3, "breath": 4},
        90,
    ),
    (
        "Morning light arrived before I did,\nunlocked the room and said nothing.",
        {"morning": 4, "light": 4, "unlocked": 5, "room": 3, "nothing": 4},
        90,
    ),
    (
        "First light found the kettle and made it shine.\nThe day began without asking me.",
        {"first": 5, "light": 4, "kettle": 5, "shine": 4, "morning": 2},
        90,
    ),
    (
        "A coin of morning light slid under the door.\nNobody came to claim it.",
        {"coin": 6, "morning": 4, "light": 4, "door": 5, "claim": 3},
        90,
    ),
    (
        "The window held the morning light like a page.\nI read it once and did not turn it.",
        {"window": 5, "morning": 4, "light": 4, "page": 5, "read": 3},
        90,
    ),
    (
        "Morning came in on the dust and stood there,\nquiet as a key on the floor.",
        {"morning": 4, "dust": 5, "quiet": 5, "key": 6, "floor": 4},
        90,
    ),
    (
        "Light spilled through the glass and cut the room in half.\nHalf of it was morning, half was mine.",
        {"light": 4, "glass": 5, "room": 3, "half": 4, "morning": 3},
        90,
    ),
    (
        "One bar of morning light crossed the floorboards.\nThe house held still to let it pass.",
        {"bar": 5, "morning": 4, "light": 4, "floorboards": 5, "still": 4},
        90,
    ),
    (
        "Morning put its light on the doorstep\nand left before I could say thank you.",
        {"morning": 4, "light": 4, "doorstep": 6, "left": 3, "thank": 2},
        90,
    ),
    (
        "The lamp was off but the room was lit.\nMorning had been there first.",
        {"lamp": 5, "off": 4, "room": 3, "lit": 6, "morning": 4},
        90,
    ),
    (
        "A thin light found the edge of the bed.\nMorning, arriving, asked for nothing.",
        {"thin": 4, "light": 4, "edge": 5, "bed": 4, "morning": 4, "nothing": 4},
        90,
    ),
]


def score(d):
    """Score one candidate dict.

    Returns the MAX rating among the rating keywords found (case-insensitive)
    in the text, plus a small bonus if the line contains a digit and a bonus
    for brevity (shorter is better for a micro poem, up to the cap).
    """
    text = d["text"]
    low = text.lower()
    found = [s for kw, s in d["rating"].items() if kw.lower() in low]
    base = max(found) if found else 0
    bonus = 0
    if any(ch.isdigit() for ch in text):
        bonus += 1
    cap = d.get("cap", 120)
    if len(text) <= cap:
        bonus += max(0, (cap - len(text))) / float(cap)
    return base + bonus


SEED = 7
ROUNDS = 10
KEEP = 5


def mutate(text, rng):
    """Make a light phrasing mutant of a two-line poem."""
    lines = text.split("\n")
    kind = rng.randrange(5)
    if kind == 0 and "Morning" in lines[0]:
        lines[0] = lines[0].replace("Morning", "Dawn", 1)
    elif kind == 1 and " light" in text.lower():
        lines[rng.randrange(len(lines))] = lines[rng.randrange(len(lines))].replace(
            "light", "glow", 1
        )
    elif kind == 2:
        lines[0] = lines[0].replace("the ", "that ", 1)
    elif kind == 3:
        lines[-1] = lines[-1].rstrip(".")
    else:
        lines[0] = lines[0].replace("I ", "i ", 1)
    return "\n".join(lines)


def improve(pool, seed=SEED, rounds=ROUNDS, keep=KEEP):
    """10-round improvement loop.

    Each round: sort by score, keep the top ``keep`` seeds, spawn light
    phrasing mutants, rescore everything, and track the best line ever seen.
    Deterministic via the RNG seed.
    """
    rng = random.Random(seed)
    best = None
    best_score = float("-inf")

    def consider(d):
        nonlocal best, best_score
        s = score(d)
        if s > best_score:
            best_score, best = s, d["text"]
        return s, d

    for _ in range(rounds):
        scored = sorted(pool, key=lambda d: score(d), reverse=True)
        for s, d in ((score(d), d) for d in scored):
            consider(d)
        seeds = [d["text"] for d in scored[:keep]]
        pool = [{"text": t, "rating": CANDIDATES[0][1], "cap": 120} for t in seeds]
        mutants = [mutate(t, rng) for t in seeds]
        pool += [
            {"text": m, "rating": CANDIDATES[0][1], "cap": 120} for m in mutants
        ]
    return best, best_score


def main():
    os.makedirs("output", exist_ok=True)
    pool = [{"text": t, "rating": r, "cap": c} for t, r, c in CANDIDATES]
    best, _ = improve(pool)
    line = best.strip()
    with open(os.path.join("output", "entry.txt"), "w", encoding="utf-8") as f:
        f.write(line)
    print(line)


if __name__ == "__main__":
    main()
