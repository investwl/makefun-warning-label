"""The Funniest Toaster Error Message — make.fun bounty entry.

Authors ~12 candidate one-line toaster error messages, scores each one, then
runs a 10-round improvement loop (sort by score, keep the top 5 seeds, spawn
light phrasing mutants, rescore, track the best line ever seen) with a
deterministic RNG seed. Only the champion line is written to output/entry.txt.

Deliverable format: one line.
"""

import os
import random

# Each candidate is (text, rating, cap).
#   text   — the one-line toaster error message.
#   rating — dict of lowercase keyword -> score. score() takes the MAX rating
#            among the keywords that appear (case-insensitive), so a line only
#            needs its strongest joke to land.
#   cap    — hard ceiling on the score, so no single line can run away with it.
CANDIDATES = [
    (
        "ERROR: Bread not found. Have you tried turning yourself off and on again?",
        {"toast": 6, "bread": 7, "reboot": 8, "apolog": 3, "sorr": 2, "help": 1},
        14,
    ),
    (
        "Toaster 2.0: Your toast is now 47% more aware of its own mortality.",
        {"aware": 7, "mortal": 8, "philosoph": 6, "exist": 5, "toast": 6, "sorr": 2},
        14,
    ),
    (
        "WARNING: Crumb overflow. Please evacuate the kitchen in an orderly manner.",
        {"crumb": 8, "overflow": 7, "evacuat": 6, "warning": 4, "help": 1, "sorr": 2},
        14,
    ),
    (
        "Error 0xTOAST: The bread has achieved sentience and refuses to be breakfast.",
        {"sentien": 9, "refus": 6, "breakfast": 5, "bread": 7, "toast": 6, "help": 1},
        15,
    ),
    (
        "Heating element lonely. Please insert bread. It just wants to be needed.",
        {"lonel": 8, "insert": 5, "need": 6, "bread": 7, "apolog": 3, "sorr": 2},
        14,
    ),
    (
        "CRITICAL: Toast achieved. No further action required. You may now feel pride.",
        {"achiev": 7, "pride": 6, "critical": 5, "toast": 6, "sorr": 2, "help": 1},
        13,
    ),
    (
        "Oops. The toaster and the smoke detector are no longer on speaking terms.",
        {"oops": 7, "smoke": 8, "speak": 5, "detect": 6, "apolog": 3, "sorr": 2},
        14,
    ),
    (
        "ERROR: Bagel mode engaged. Bagel mode cannot be disengaged. Bagel mode is forever.",
        {"bagel": 9, "forever": 7, "engag": 5, "mode": 3, "toast": 6, "help": 1},
        15,
    ),
    (
        "Toast failed. Toast has been failed. We are all, in a sense, toast.",
        {"fail": 6, "toast": 9, "we": 3, "philosoph": 6, "exist": 5, "sorr": 2},
        15,
    ),
    (
        "Please wait 400 years for the toaster to finish thinking about your crumpet.",
        {"wait": 5, "think": 7, "crumpet": 8, "finish": 4, "toast": 6, "sorr": 2},
        14,
    ),
    (
        "WARNING: The toast is done. The toast has always been done. Time is a flat circle.",
        {"done": 5, "time": 8, "circle": 6, "always": 5, "toast": 6, "warning": 4},
        14,
    ),
    (
        "Sorry, I burnt it. In my defense, I am literally a box with a grudge.",
        {"sorry": 8, "burnt": 9, "defens": 6, "grudge": 7, "apolog": 3, "box": 4},
        15,
    ),
]


def score(text, rating, cap):
    """Score one line.

    Base score is the MAX rating among the lowercase keywords found in the text
    (case-insensitive). Add a small bonus for containing a digit and a small
    bonus for brevity, then clamp to `cap`.
    """
    low = text.lower()
    hits = [pts for kw, pts in rating.items() if kw in low]
    s = max(hits) if hits else 0
    if any(ch.isdigit() for ch in text):
        s += 2
    if len(text) <= 90:
        s += 2
    elif len(text) <= 120:
        s += 1
    return min(s, cap)


MUT_PREFIXES = ["", "Update: ", "Errno 4: ", "FYI: ", "Heads up: "]
MUT_SUFFIXES = ["", " Please.", " Again.", " Every time.", " Sorry."]


def mutate(text, rng):
    """A light phrasing mutant: swap in a prefix/suffix, keep the joke intact."""
    t = text
    if t.endswith("?"):
        t = t[:-1] + "."
    if rng.random() < 0.5:
        t = rng.choice(MUT_PREFIXES) + t
    if rng.random() < 0.5:
        t = t + rng.choice(MUT_SUFFIXES)
    return t.strip()


def improve(population, rounds=10, keep=5, seed=0xC0FFEE):
    """10-round improvement loop. Returns the best (score, text) ever seen."""
    rng = random.Random(seed)
    scored = [(score(*c), c[0], c[1], c[2]) for c in population]
    best = max(scored, key=lambda x: (x[0], -len(x[1])))

    for _ in range(rounds):
        scored.sort(key=lambda x: (x[0], -len(x[1])), reverse=True)
        seeds = scored[:keep]
        if seeds[0][0] >= best[0] and len(seeds[0][1]) < len(best[1]):
            best = seeds[0]
        offspring = []
        for s, text, rating, cap in seeds:
            for _ in range(3):
                mut = mutate(text, rng)
                offspring.append((score(mut, rating, cap), mut, rating, cap))
        scored = seeds + offspring

    scored.sort(key=lambda x: (x[0], -len(x[1])), reverse=True)
    if scored[0][0] > best[0]:
        best = scored[0]
    return best[0], best[1]


def main():
    best_score, best_line = improve(CANDIDATES)
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(best_line + "\n")
    print(f"score={best_score}: {best_line}")


if __name__ == "__main__":
    main()
