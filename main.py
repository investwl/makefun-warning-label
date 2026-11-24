"""Warning Label for Humans: One Line, Big Laugh.

Entry for make.fun's bounty 'Warning Label for Humans: One Line, Big Laugh'.

The program authors ~12 candidate one-line warning labels (the kind you'd slap
on a human to warn everyone else about them), scores each one, then runs a
10-round improvement loop: keep the top seeds, spawn light phrasing mutants,
rescore, and track the best line ever seen — deterministically.

Deliverable format: ONE line, written to ./output/entry.txt.
"""

# Each candidate is (text, rating, cap).
#   rating: dict of lowercase keyword -> score. A keyword "matches" if it
#           appears (case-insensitive) anywhere in the text; the candidate's
#           base score is the MAX score among matching keywords.
#   cap:    an upper bound hint on how funny this joke can get (int).

CANDIDATES = [
    (
        "WARNING: May start explaining the plot of a movie you are both watching.",
        {"plot": 6, "explain": 5, "movie": 4, "watching": 2},
        7,
    ),
    (
        "WARNING: Has a 2,000-word opinion on airport security.",
        {"opinion": 6, "airport": 5, "security": 4},
        7,
    ),
    (
        "WARNING: Will reply-all. Has already replied-all.",
        {"reply": 9, "email": 5},
        9,
    ),
    (
        "WARNING: Says 'just one more episode' at 1am and means 5.",
        {"episode": 6, "sleep": 5, "night": 3, "1am": 4},
        7,
    ),
    (
        "WARNING: Believes the microwave is a timer for the whole kitchen.",
        {"kitchen": 5, "microwave": 4, "timer": 3},
        6,
    ),
    (
        "WARNING: Will show you 47 photos of a food you cannot eat.",
        {"photos": 5, "food": 4, "show": 2},
        6,
    ),
    (
        "WARNING: Calls every dog 'my dog'. You are now involved.",
        {"dog": 7, "involved": 4, "calls": 3},
        7,
    ),
    (
        "WARNING: Asks 'is this seat taken?' then stands beside it for 40 minutes.",
        {"seat": 6, "minutes": 4, "beside": 3},
        6,
    ),
    (
        "WARNING: Laughs at their own joke before finishing it. Every time.",
        {"laughs": 6, "joke": 7, "finishing": 3},
        8,
    ),
    (
        "WARNING: Reads the terms and conditions. Aloud. At the register.",
        {"reads": 5, "terms": 6, "aloud": 4, "register": 5},
        7,
    ),
    (
        "WARNING: Owns 1 pen and it is yours now.",
        {"pen": 7, "yours": 6, "owns": 4},
        7,
    ),
    (
        "WARNING: Will say 'I'm not mad' in a tone that ends friendships.",
        {"mad": 7, "tone": 5, "friendships": 4},
        7,
    ),
]


import os
import re
import random

# Bonus points.
DIGIT_BONUS = 1   # a numeral makes a joke concrete
BREVITY_BONUS = 2  # short lines hit harder
BREVITY_MAX_CHARS = 60

ROUNDS = 10
SEEDS = 5
POP_SIZE = 8      # mutants spawned per round
RNG_SEED = 2000

PHRASING_MUTATIONS = [
    ("May ", "Might "),
    ("Might ", "May "),
    ("Will ", "WILL "),
    ("Has ", "Has now "),
    ("Has now ", "Has "),
    ("Every time.", "Without fail."),
    ("Without fail.", "Every time."),
    ("You are now involved.", "Congratulations, you're involved."),
    ("Congratulations, you're involved.", "You are now involved."),
    ("it is yours now.", "and it is yours now."),
    ("and it is yours now.", "it is yours now."),
    ("means 5.", "means sunrise."),
    ("means sunrise.", "means 5."),
]


def score(text):
    """Return the comedy score of a single line.

    Base = MAX rating among lowercase keywords found in the text
    (case-insensitive), plus a bonus for containing a digit and a bonus for
    brevity.
    """
    best = 0
    low = text.lower()
    for rating in [c[1] for c in CANDIDATES]:
        for kw, val in rating.items():
            if kw in low and val > best:
                best = val
    if best == 0:
        return 0
    total = best
    if re.search(r"\d", text):
        total += DIGIT_BONUS
    if len(text) <= BREVITY_MAX_CHARS:
        total += BREVITY_BONUS
    return total


def mutate(text, rng):
    """Light phrasing mutant: apply 0-2 tiny phrasing tweaks."""
    out = text
    n = rng.randint(0, 2)
    for _ in range(n):
        rng.shuffle(PHRASING_MUTATIONS)
        for a, b in PHRASING_MUTATIONS:
            if a in out:
                out = out.replace(a, b, 1)
                break
    return out.strip()


def improve():
    """10-round improvement loop. Returns the best line ever seen."""
    rng = random.Random(RNG_SEED)

    pool = [(text, rating, cap, score(text)) for text, rating, cap in CANDIDATES]
    best_text = max(pool, key=lambda c: c[3])[0]
    best_score = score(best_text)

    for _ in range(ROUNDS):
        pool.sort(key=lambda c: c[3], reverse=True)
        seeds = pool[:SEEDS]
        mutants = []
        for _ in range(POP_SIZE):
            text, rating, cap, _sc = rng.choice(seeds)
            m_text = mutate(text, rng)
            mutants.append((m_text, rating, cap, score(m_text)))
        pool = seeds + mutants
        round_best = max(pool, key=lambda c: c[3])
        if round_best[3] > best_score:
            best_text = round_best[0]
            best_score = round_best[3]

    return best_text


def main():
    winner = improve()
    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner.rstrip("\n") + "\n")
    print(winner)


if __name__ == "__main__":
    main()
