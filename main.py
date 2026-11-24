#!/usr/bin/env python3
"""One-Star Review of Something Essential — make.fun one-line bounty entry.

The program authors ~12 candidate one-line jokes on the theme, scores each
(MAX rating among the lowercase keywords found, plus a bonus for containing a
digit and a bonus for brevity), then runs a 10-round improvement loop that
keeps the top 5 seeds, spawns light phrasing mutants, rescores them, and
tracks the best line ever seen — all with a deterministic RNG seed.

Only the champion line is written to ./output/entry.txt.
"""

import os
import random
import re

RNG_SEED = 20261124
ROUNDS = 10
TOP_K = 5
MAX_LEN = 140  # brevity ceiling; under this earns the brevity bonus

# --- 12 hand-written candidates on the theme -------------------------------
# rating keywords are lowercase substrings matched case-insensitively against
# each line; score() takes the MAX keyword rating found, then adds bonuses.
CANDIDATES = [
    (
        "Water: 1 star. Wet, tastes like nothing, and it was gone in 2 sips.",
        {"water": 3, "tastes": 4, "gone": 3, "sip": 2, "nothing": 3},
        4,
    ),
    (
        "Air: 0 stars. Invisible, overpriced, and the free version has bugs.",
        {"air": 2, "invisible": 3, "free": 3, "bugs": 4, "version": 2},
        4,
    ),
    (
        "Sleep: 1 star. Woke up 8 hours later and my problems were all still there.",
        {"sleep": 3, "woke": 2, "hours": 3, "problems": 4, "still": 2},
        4,
    ),
    (
        "Gravity: 1 star. Never once let me down, but also never once let me up.",
        {"gravity": 3, "down": 2, "never": 3, "once": 2, "up": 2},
        3,
    ),
    (
        "Oxygen: 1 star. Fine at first, then I got hooked. Now I need it every minute.",
        {"oxygen": 3, "hooked": 4, "need": 3, "minute": 2, "fine": 2},
        4,
    ),
    (
        "Bread: 1 star. It's just sad wheat. The crust fought back and won 3 times.",
        {"bread": 3, "wheat": 3, "crust": 3, "fought": 3, "won": 2},
        4,
    ),
    (
        "Toilet paper: 1 star. Did the job once, then quit and left me hanging.",
        {"toilet": 3, "paper": 2, "job": 3, "quit": 4, "hanging": 3},
        4,
    ),
    (
        "The Sun: 1 star. Shows up late, leaves early, and stares at me all day.",
        {"sun": 3, "late": 3, "early": 2, "stares": 4, "day": 2},
        4,
    ),
    (
        "Soap: 0 stars. Washed my hands and now they're cleaner than my browser history.",
        {"soap": 3, "wash": 3, "clean": 3, "browser": 4, "history": 3},
        4,
    ),
    (
        "Coffee: 1 star. Costs $7, tastes like dirt, and I'd fight you for the last cup.",
        {"coffee": 3, "cost": 3, "dirt": 3, "fight": 4, "cup": 2},
        4,
    ),
    (
        "WiFi: 1 star. Connects instantly — right after I've already given up twice.",
        {"wifi": 3, "connect": 3, "instantly": 3, "up": 2, "twice": 2},
        3,
    ),
    (
        "Monday: 1 star. Comes back every 7 days no matter how many times I unsubscribe.",
        {"monday": 3, "days": 3, "back": 2, "unsubscribe": 4, "times": 2},
        4,
    ),
]

# light phrasing swaps used to build mutants
SWAPS = [
    ("1 star", "one star"),
    ("one star", "1 star"),
    ("0 stars", "zero stars"),
    ("zero stars", "0 stars"),
    ("It's", "It is"),
    ("It is", "It's"),
    ("I'd", "I would"),
    ("I would", "I'd"),
    ("never once", "not once"),
    ("not once", "never once"),
    ("every", "each"),
    ("each", "every"),
    ("Fine at first", "Started fine"),
    ("Started fine", "Fine at first"),
    ("tastes like", "flavors of"),
    ("flavors of", "tastes like"),
    ("Did the job", "Got the job done"),
    ("Shows up late", "Arrives late"),
    ("Arrives late", "Shows up late"),
    ("all day", "all day long"),
    ("right after", "just after"),
    ("no matter", "regardless"),
]


def _bonuses(text):
    bonus = 0
    if re.search(r"\d", text):
        bonus += 1  # a digit earns a point
    if len(text) <= MAX_LEN:
        bonus += 1  # brevity earns a point
    return bonus


def score(d):
    """Score a candidate tuple -> (total, keyword_rating, bonuses).

    total = MAX rating among keywords found (case-insensitive) + bonuses.
    """
    text, ratings, _cap = d
    low = text.lower()
    found = [v for k, v in ratings.items() if k.lower() in low]
    kw = max(found) if found else 0
    b = _bonuses(text)
    return kw + b, kw, b


def mutants(text, rng):
    """Light phrasing mutants: 1-2 random light swaps applied to a copy."""
    out = text
    for _ in range(rng.randint(1, 2)):
        a, b = rng.choice(SWAPS)
        if a in out:
            out = out.replace(a, b, 1)
    return out


def improve():
    rng = random.Random(RNG_SEED)
    pool = list(CANDIDATES)
    best = None  # (score, text)

    def consider(d):
        nonlocal best
        s, _kw, _b = score(d)
        if best is None or s > best[0]:
            best = (s, d[0])

    for d in pool:
        consider(d)

    for _round in range(ROUNDS):
        pool.sort(key=lambda d: score(d)[0], reverse=True)
        seeds = pool[:TOP_K]
        new_pool = []
        for d in seeds:
            new_pool.append(d)
            m_text = mutants(d[0], rng)
            new_pool.append((m_text, d[1], d[2]))
        pool = new_pool
        for d in pool:
            consider(d)

    return best


def main():
    best_score, winner = improve()
    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner)
    print(winner)
    print(f"[best score: {best_score}]")


if __name__ == "__main__":
    main()
