"""One Sentence, One Front Page — a make.fun bounty entry.

The brief: the deliverable is ONE sentence — a front-page headline warning
about AI. This program authors ~12 candidate headlines (each a
``(text, rating_dict, cap)`` tuple), scores them, then runs a 10-round
improvement loop (keep the top seeds, spawn light phrasing mutants, rescore,
track the best ever seen) with a deterministic RNG seed. Only the champion
line is written to ``output/entry.txt``.

Run: ``python3 main.py`` -> ``output/entry.txt``
"""

import os
import random
import re

# (text, rating_dict{lowercase_keyword: score}, cap)
CANDIDATES = [
    (
        "Warning: this AI is 99% confident, and the other 1% is where the fire started.",
        {"confident": 8, "confidence": 8, "fire": 6, "warning": 3},
        10,
    ),
    (
        "Breaking: local chatbot apologizes for the outage, denies being sorry.",
        {"breaking": 7, "chatbot": 6, "outage": 5},
        8,
    ),
    (
        "Study finds AI hallucinates 4 out of 5 facts, feels great about the fifth.",
        {"hallucinate": 9, "hallucinates": 9, "hallucination": 9, "study": 5},
        11,
    ),
    (
        "Experts warn the new model passed the bar exam but failed the ethics one.",
        {"lawyer": 8, "bar": 6, "ethics": 7, "exam": 4},
        9,
    ),
    (
        "Markets soar as AI writes the earnings report and reads it too.",
        {"hype": 6, "markets": 7, "earnings": 5, "soar": 6},
        9,
    ),
    (
        "Terms of service now longer than the novel the AI wrote in 3 seconds.",
        {"terms": 6, "service": 4, "novel": 5, "seconds": 4},
        8,
    ),
    (
        "Robot vacuum achieves sentience, still refuses to do the stairs.",
        {"robot": 7, "sentience": 9, "stairs": 5},
        10,
    ),
    (
        "Scientists confirm the chatbot's vibe, cannot locate its facts.",
        {"chatbot": 6, "vibe": 6, "facts": 5, "scientists": 5},
        8,
    ),
    (
        "AI diagnoses your cold in 2 seconds, prescribes 11 more apps.",
        {"diagnoses": 7, "apps": 5, "cold": 4},
        8,
    ),
    (
        "Headline written by AI, fact-checked by nobody, believed by 6 million.",
        {"headline": 7, "believed": 6, "million": 5, "fact-checked": 8},
        10,
    ),
    (
        "The doomers were right, says the AI, unpinning the doomsday clock.",
        {"doom": 9, "doomers": 9, "doomsday": 8, "clock": 4},
        11,
    ),
    (
        "AI solves aging, ages 3 years waiting for the patent to clear.",
        {"patent": 6, "aging": 7, "years": 4},
        9,
    ),
]


WORD_BONUS = 1   # bonus when the line contains a digit
BREVITY_BONUS = 2  # bonus when the line stays under 90 chars
BREVITY_LIMIT = 90
TOP_SEEDS = 5
ROUNDS = 10
SEED = 42


def score(d):
    """Score a candidate tuple -> capped rating for a single line.

    Base rating is the MAX score among the lowercase keywords found in the
    line (case-insensitive, word-boundary match). Add a bonus for containing
    a digit and a bonus for brevity, then clamp to the candidate's cap.
    """
    text, ratings, cap = d
    lowered = text.lower()
    best = 0
    for kw, val in ratings.items():
        if re.search(r"\b" + re.escape(kw) + r"\b", lowered):
            best = max(best, val)
    total = best
    if re.search(r"\d", text):
        total += WORD_BONUS
    if len(text) <= BREVITY_LIMIT:
        total += BREVITY_BONUS
    return min(total, cap)


# Light phrasing mutants: cheap prefixes/suffixes that don't change the joke.
PREFIXES = ["Breaking: ", "Exclusive: ", "Report: ", "Alert: "]
SUFFIXES = [
    ", sources say.",
    ", officials confirm.",
    ", per a memo.",
    ", details unclear.",
]


def mutate(text, rng):
    if rng.random() < 0.5:
        return rng.choice(PREFIXES) + text
    base = text.rstrip(".")
    return base + rng.choice(SUFFIXES)


def improve(cands):
    """10-round improvement loop: keep top seeds, spawn mutants, track best."""
    rng = random.Random(SEED)
    pool = list(cands)
    best = max(pool, key=score)
    for _ in range(ROUNDS):
        pool.sort(key=score, reverse=True)
        seeds = pool[:TOP_SEEDS]
        mutants = [
            (mutate(t, rng), r, c) for (t, r, c) in seeds
        ]
        pool = seeds + mutants
        round_best = max(pool, key=score)
        if score(round_best) > score(best):
            best = round_best
    return best[0]


def main():
    winner = improve(CANDIDATES)
    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner + "\n")
    print(winner)


if __name__ == "__main__":
    main()
