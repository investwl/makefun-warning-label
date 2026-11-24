"""One Line of Wonder — make.fun bounty entry (investwl/makefun-warning-label).

A single line of text, at most 200 characters, written to make a reader feel
wonder: a small concrete thing made strange, a gap that keeps opening after the
line ends. No grand abstraction, no wasted word.

Program shape:
  * ~12 candidate lines, each a ``(text, rating_dict, cap)`` tuple where
    ``rating_dict`` maps lowercase keywords to a score.
  * A stub scoring hook (filled in on the second pass).
"""

# Each candidate: (text, {lowercase_keyword: score}, cap)
CANDIDATES = [
    (
        "The moon is a hole in the night, and the stars are the light leaking through it.",
        {"moon": 3, "hole": 4, "leak": 4, "night": 1},
        12,
    ),
    (
        "Somewhere a door you never opened is still holding its breath for you.",
        {"door": 3, "breath": 4, "holding": 2, "you": 1},
        12,
    ),
    (
        "Every map is a lie that agreed to be useful.",
        {"map": 3, "lie": 4, "useful": 2},
        11,
    ),
    (
        "The ocean has been rehearsing the same wave for four billion years and still flubs the ending.",
        {"ocean": 3, "wave": 3, "billion": 5, "ending": 3},
        13,
    ),
    (
        "There are 8 billion people and not one of them has ever seen your exact face fall asleep.",
        {"8": 4, "billion": 5, "face": 3, "asleep": 3},
        13,
    ),
    (
        "Rain is just the sky returning what it borrowed.",
        {"rain": 3, "borrowed": 4, "sky": 2},
        11,
    ),
    (
        "Your shadow has walked every step with you and never once asked where you were going.",
        {"shadow": 4, "walked": 2, "never": 2, "going": 1},
        12,
    ),
    (
        "Light left that star before there was a word for leaving.",
        {"light": 3, "star": 3, "leaving": 4, "word": 2},
        12,
    ),
    (
        "A seed splits itself open to find out it was wrong about being small.",
        {"seed": 3, "splits": 3, "small": 3, "wrong": 3},
        12,
    ),
    (
        "The 3 a.m. sky is the only room big enough to hold a thought that won't fit in the morning.",
        {"3": 4, "sky": 3, "thought": 3, "morning": 2},
        13,
    ),
    (
        "Snow is the sky reading itself aloud, one flake at a time, and forgetting by noon.",
        {"snow": 3, "flake": 4, "forgetting": 4, "noon": 2},
        13,
    ),
    (
        "You are the only animal that looks up and wonders what's looking back.",
        {"look": 3, "wonders": 5, "looking": 4, "back": 1},
        13,
    ),
]


BREVITY_BONUS_MAX = 6   # chars under the 200-char cap that earns full brevity bonus
DIGIT_BONUS = 3
ROUNDS = 10
SEEDS_KEPT = 5
RNG_SEED = 20261124


def score(d):
    """Score a candidate line.

    Returns the MAX rating among the lowercase keywords found in the text
    (case-insensitive), plus a bonus if the line contains a digit and a bonus
    for brevity. The result is clamped to the candidate's ``cap``.
    """
    text, ratings, cap = d
    low = text.lower()
    found = [s for kw, s in ratings.items() if kw.lower() in low]
    base = max(found) if found else 0
    total = base
    if any(ch.isdigit() for ch in text):
        total += DIGIT_BONUS
    under = 200 - len(text)
    total += min(under, BREVITY_BONUS_MAX)
    return min(total, cap)


def _mutate(text, rng):
    """Spawn a light phrasing mutant of ``text`` (deterministic given rng)."""
    swaps = [
        ("wonders", "wonders aloud"),
        ("never once", "not once"),
        ("four billion", "4 billion"),
        ("and still", "— and still"),
        ("what it borrowed", "everything it borrowed"),
        ("looking back", "looking back down"),
    ]
    cands = [t for t in swaps if t[0] in text]
    if not cands:
        return text
    a, b = cands[rng.randrange(len(cands))]
    return text.replace(a, b, 1)


def improve(pool, rounds=ROUNDS):
    """Run the improvement loop; return the best line ever seen."""
    import random

    rng = random.Random(RNG_SEED)
    pool = list(pool)
    best = max(pool, key=score)
    best_line = best[0]

    for _ in range(rounds):
        ranked = sorted(pool, key=score, reverse=True)
        seeds = ranked[:SEEDS_KEPT]
        mutants = [(_mutate(t, rng), r, c) for (t, r, c) in seeds]
        pool = seeds + mutants
        for d in pool:
            if score(d) > score(best):
                best = d
                best_line = d[0]
    return best_line


def main():
    import os

    winner = improve(CANDIDATES)
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(winner)
    print(winner)


if __name__ == "__main__":
    main()
