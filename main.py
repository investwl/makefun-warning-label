"""Six Words, One Story — make.fun bounty entry (investwl/makefun-warning-label).

A tiny program that authors ~12 candidate six-word micro-stories, scores them,
and improves them over several rounds before writing the single winning line
to ``output/entry.txt``.

Deliverable format: exactly SIX WORDS.

Candidates are ``(text, rating_dict, cap)`` tuples where ``rating_dict`` maps
lowercase keyword -> score; the score of a line is the MAX rating among the
keywords it contains (case-insensitive), plus bonuses for containing a digit
and for being brief, clamped to ``cap``.
"""

import os
import random

# (text, {lowercase_keyword: score}, cap)
CANDIDATES = [
    ("Rebooted my life. Forgot to save.", {"reboot": 9, "save": 8, "forgot": 7, "life": 6}, 12),
    ("Sold the house. Kept the Wi-Fi password.", {"sold": 8, "kept": 6, "house": 7, "wifi": 9}, 12),
    ("Six words left. This one counts.", {"six": 9, "left": 6, "counts": 8, "words": 7}, 12),
    ("Woke up famous. Alarm was dreaming.", {"woke": 7, "famous": 9, "alarm": 8, "dreaming": 7}, 12),
    ("Deleted the app. It deleted back.", {"deleted": 9, "app": 7, "back": 6}, 12),
    ("Won the lottery. Lost the ticket.", {"won": 9, "lost": 9, "lottery": 8, "ticket": 8}, 12),
    ("Trained the model. It trained me.", {"trained": 9, "model": 8, "me": 6}, 12),
    ("Fixed the bug. Created two worse.", {"fixed": 9, "bug": 9, "created": 7, "worse": 8}, 12),
    ("She said yes. To the other guy.", {"said": 7, "yes": 9, "other": 6, "guy": 6}, 12),
    ("Emergency landing. Pilot was learning.", {"emergency": 9, "landing": 8, "pilot": 8, "learning": 7}, 12),
    ("Graduated today. Diploma was blank.", {"graduated": 9, "diploma": 9, "blank": 8, "today": 6}, 12),
    ("Ran the marathon. Wrong city though.", {"ran": 7, "marathon": 9, "wrong": 8, "city": 6}, 12),
]


BREVITY_BONUS = 2      # award if the line is 5 words or fewer
DIGIT_BONUS = 1        # award if the line contains any digit
SEEDS = 5              # top seeds kept each round
ROUNDS = 10
SEED = 42
FILLERS = ["still", "then", "now", "so", "yet", "again", "truly", "somehow"]


def score(d):
    """Score a candidate tuple -> int.

    MAX rating among the lowercase keywords found (case-insensitive), plus a
    bonus for containing a digit and a bonus for brevity, clamped to ``cap``.
    """
    text, ratings, cap = d
    low = text.lower()
    ratings_hit = [v for k, v in ratings.items() if k in low]
    base = max(ratings_hit) if ratings_hit else 0
    s = base
    if any(ch.isdigit() for ch in text):
        s += DIGIT_BONUS
    if len(text.split()) <= 5:
        s += BREVITY_BONUS
    return min(s, cap)


def _mutate(text, rng):
    """Light phrasing mutants that preserve the six-word format."""
    words = text.split()
    kind = rng.randrange(4)
    if kind == 0:  # soften the punch with a filler
        words[-1] = rng.choice(FILLERS) + " " + words[-1]
        return " ".join(words[:6])
    if kind == 1:  # swap a mid word for a filler
        i = rng.randrange(1, len(words) - 1)
        words[i] = rng.choice(FILLERS)
        return " ".join(words[:6])
    if kind == 2:  # re-punctuate
        return text.replace(".", ",", 1)
    # uppercase the lead for punch
    words[0] = words[0].upper()
    return " ".join(words[:6])


def main():
    rng = random.Random(SEED)
    os.makedirs("output", exist_ok=True)

    pool = list(CANDIDATES)
    best = max(pool, key=score)
    best_score = score(best)

    for _ in range(ROUNDS):
        pool.sort(key=score, reverse=True)
        seeds = pool[:SEEDS]
        mutants = [(_mutate(t, rng), r, c) for t, r, c in seeds]
        pool = seeds + mutants
        for d in pool:
            if score(d) > best_score:
                best, best_score = d, score(d)

    line = " ".join(best[0].split()[:6])
    with open(os.path.join("output", "entry.txt"), "w") as f:
        f.write(line)
    print(line)


if __name__ == "__main__":
    main()
