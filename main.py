"""One-Line Roast: The Gadget You Use Every Day.

Entry for make.fun bounty 'One-Line Roast: The Gadget You Use Every Day'
(https://make.fun/bounty/u-daring-gecko-25-one-line-roast-the-gadget-you-use-3d6aa610).

Deliverable: ONE line, written to ./output/entry.txt.

This module holds a pool of candidate roast one-liners, each tagged with a
rating dict keyed by lowercase quality keywords (score per keyword present)
and a hard character cap. A later step scores, mutates, and picks the best.
"""

import os
import random

# (text, rating_dict{lowercase_kw: score}, cap)
CANDIDATES = [
    ("Your phone's battery dies before your excuses do.",
     {"relatable": 3, "punchy": 2, "battery": 2}, 70),
    ("My laptop fans spin like they're cooling my bad decisions.",
     {"relatable": 3, "self-deprecating": 2, "punchy": 1}, 75),
    ("Earbuds: tiny witnesses to everything you lip-sync alone.",
     {"observational": 3, "dark": 2}, 70),
    ("Your phone knows you better, and it's not flattered.",
     {"punchy": 3, "clever": 2}, 60),
    ("The smart fridge judges your 2 a.m. snacks in silence.",
     {"observational": 3, "dark": 1, "clever": 1}, 70),
    ("My charger lives a better life than I do, always plugged in.",
     {"relatable": 2, "self-deprecating": 2, "clever": 1}, 75),
    ("Autocorrect turns my texts into confessions I never wrote.",
     {"relatable": 3, "punchy": 2}, 70),
    ("Your phone's screen time report is a cry for help, in pie chart.",
     {"dark": 3, "relatable": 2, "clever": 1}, 75),
    ("Headphones on: the universal sign for 'do not perceive me.'",
     {"relatable": 3, "observational": 2}, 70),
    ("My phone updates overnight and still wakes up broken.",
     {"relatable": 2, "punchy": 2}, 60),
    ("The gadget you use every day uses you right back.",
     {"clever": 3, "dark": 2, "punchy": 1}, 60),
    ("Your phone's camera roll is a museum of choices you can't undo.",
     {"dark": 3, "clever": 2}, 75),
]


def score(d):
    """Score a candidate dict {'text','rating','cap'}.

    MAX rating among quality keywords found in the text (case-insensitive),
    plus a bonus for containing a digit and a bonus for brevity.
    """
    text = d["text"].lower()
    best = 0
    for kw, pts in d["rating"].items():
        if kw.lower() in text:
            best = max(best, pts)
    val = best
    if any(ch.isdigit() for ch in text):
        val += 2
    if len(d["text"]) <= 55:
        val += 3
    return val


def mutate(text, rng):
    """Make a light phrasing mutant of a seed line."""
    swaps = [
        ("your", "ur"), ("you", "u"), ("is", "'s"),
        ("do not", "don't"), ("cannot", "can't"),
    ]
    t = text
    for a, b in rng.sample(swaps, len(swaps)):
        if a in t.lower():
            i = t.lower().index(a)
            t = t[:i] + b + t[i + len(a):]
            break
    return t.strip()


def run():
    """Improve the pool over 10 rounds; return the best line ever seen."""
    rng = random.Random(1337)
    pool = [{"text": t, "rating": r, "cap": c} for t, r, c in CANDIDATES]
    best = None
    for _ in range(10):
        scored = sorted(pool, key=score, reverse=True)
        for d in scored:
            if len(d["text"]) <= d["cap"] and (best is None or score(d) > score(best)):
                best = d
        seeds = scored[:5]
        pool = seeds + [
            {"text": mutate(s["text"], rng), "rating": s["rating"], "cap": s["cap"]}
            for s in seeds
        ]
    return best["text"]


def main():
    line = run()
    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "entry.txt"), "w") as f:
        f.write(line + "\n")
    print(line)


if __name__ == "__main__":
    main()
