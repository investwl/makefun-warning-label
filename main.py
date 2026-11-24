"""make.fun bounty: 'Make the Judge Fall in Love in One Line'.

Authors ~12 candidate one-line pickup lines (each a
``(text, rating_dict, cap)`` tuple), scores them, runs an improvement loop,
and writes ONLY the winning line to ``output/entry.txt``.

The scoring logic and the 10-round improvement loop are added in a second
pass; this first pass just lays down the docstring, the candidate pool and a
``main()`` stub.
"""

# ---------------------------------------------------------------------------
# Candidate pool: ~12 one-line pickup lines.
# Each entry is (text, rating_dict, cap) where rating_dict maps lowercase
# keywords -> score and cap is the maximum achievable score for that line.
# ---------------------------------------------------------------------------
CANDIDATES = [
    (
        "Are you a git conflict? Because I can't resolve anything without you.",
        {"conflict": 8, "resolve": 6, "git": 4, "without you": 10},
        10,
    ),
    (
        "I'd never ghost you — I only haunt the ones who left me on read.",
        {"ghost": 7, "haunt": 5, "read": 4},
        7,
    ),
    (
        "You must be a stack overflow, because you just overflowed my stack.",
        {"stack": 6, "overflow": 8, "you": 3},
        8,
    ),
    (
        "Roses are #FF0000, violets are #0000FF, my heart throws a 200 only for you.",
        {"roses": 7, "violets": 6, "heart": 9, "200": 8},
        9,
    ),
    (
        "I asked the RNG for a soulmate and it returned your user ID.",
        {"rng": 6, "soulmate": 9, "returned": 4},
        9,
    ),
    (
        "Are you a semicolon? Because without you my heart won't compile.",
        {"semicolon": 8, "compile": 7, "without you": 10},
        10,
    ),
    (
        "You're the only dependency I'd never pin — I want every version of you.",
        {"dependency": 7, "pin": 5, "version": 6},
        7,
    ),
    (
        "My love for you is O(1): no matter how big the world gets, it's constant.",
        {"o(1)": 8, "constant": 7, "big": 4},
        8,
    ),
    (
        "I'd branch off main just to merge into you.",
        {"branch": 7, "main": 5, "merge": 8},
        8,
    ),
    (
        "Forget fallbacks — you're the only endpoint I'll ever hit.",
        {"fallback": 6, "endpoint": 8, "hit": 5},
        8,
    ),
    (
        "You had me at 'hello world', but you sealed it at 'sudo'.",
        {"hello world": 8, "sudo": 7, "sealed": 5},
        8,
    ),
    (
        "If loving you is a bug, I'm not filing the ticket.",
        {"bug": 8, "ticket": 6, "loving": 9},
        9,
    ),
]


import os
import random
import re

RNG_SEED = 20261124
ROUNDS = 10
SEEDS_KEPT = 5
BREVITY_BONUS = 2
BREVITY_MAX_LEN = 60
DIGIT_BONUS = 1


def score(d):
    """Score one candidate dict {'text','rating','cap'}.

    MAX rating among the lowercase keywords found (case-insensitive) in the
    text, plus a bonus for containing a digit and a brevity bonus. Capped at
    the candidate's ``cap``.
    """
    text = d["text"].lower()
    ratings = [s for kw, s in d["rating"].items() if kw.lower() in text]
    base = max(ratings) if ratings else 0
    s = base
    if re.search(r"\d", d["text"]):
        s += DIGIT_BONUS
    if len(d["text"]) <= BREVITY_MAX_LEN:
        s += BREVITY_BONUS
    return min(s, d["cap"])


def mutate(text, rng):
    """Spawn a light phrasing mutant of ``text`` (deterministic via rng)."""
    swaps = [
        ("you're", "you are"),
        ("you are", "you're"),
        ("I'd", "I would"),
        ("I would", "I'd"),
        ("my heart", "this heart"),
        ("won't", "will never"),
        ("only", "just"),
        ("never", "not once"),
    ]
    idx = rng.randrange(len(swaps))
    a, b = swaps[idx]
    if a in text:
        return text.replace(a, b, 1)
    return text.rstrip(".") + ", honestly."


def improve():
    """10-round loop: sort by score, keep top 5 seeds, make mutants,
    rescore, track the best line ever seen. Deterministic RNG seed."""
    rng = random.Random(RNG_SEED)
    pool = [
        {"text": t, "rating": r, "cap": c} for t, r, c in CANDIDATES
    ]
    best = None
    for _ in range(ROUNDS):
        for d in pool:
            d["score"] = score(d)
        pool.sort(key=lambda d: d["score"], reverse=True)
        if best is None or pool[0]["score"] > best["score"]:
            best = pool[0]
        seeds = pool[:SEEDS_KEPT]
        mutants = []
        for d in seeds:
            m = dict(d)
            m["text"] = mutate(d["text"], rng)
            m["score"] = score(m)
            mutants.append(m)
        pool = seeds + mutants
    return best


def main():
    best = improve()
    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "entry.txt"), "w") as f:
        f.write(best["text"] + "\n")
    print(best["text"])


if __name__ == "__main__":
    main()
