"""One-Line Laugh Sprint — make.fun bounty u-daring-gecko-25-one-line-laugh-sprint-cda708b2.

The deliverable is ONE original funny line (1-200 chars) on everyday life.
This program authors ~12 candidate one-liners as (text, rating, cap) tuples,
scores them, then runs a 10-round improvement loop that keeps the strongest
seeds and breeds light phrasing mutants, tracking the best line ever seen.
Only the champion line is written to output/entry.txt, with a deterministic
RNG seed so the run is reproducible.

Scoring (added in a second pass): the MAX rating among the candidate's own
lowercase keywords found in the text (case-insensitive), plus a bonus for a
digit and a bonus for brevity.
"""

from __future__ import annotations

import os
import random
import re

MAX_LEN = 200
OUTPUT_DIR = "output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

DIGIT_BONUS = 1
BREVITY_BONUS = 2
BREVITY_CEILING = 90
SEED = 20261124
ROUNDS = 10
TOP_K = 5

# ~12 candidate one-liners on everyday life. Each is
# (text, rating_dict{lowercase_keyword: score}, cap).
# rating_dict keys are substrings identifying a strength of that line; the
# scorer takes the MAX rating among the keys found (case-insensitive), never
# the first match, so a line is rated at its strongest signal.
CANDIDATES: list[tuple[str, dict[str, int], int]] = [
    (
        "My smart fridge sent a push notification to remind me the milk expired. "
        "It has never once reminded me to actually drink it.",
        {"fridge": 4, "smart": 3, "notification": 2},
        MAX_LEN,
    ),
    (
        "I finally reached inbox zero. Then I remembered that was just Tuesday's "
        "tab, and there are six more tabs of unread.",
        {"inbox": 3, "zero": 4, "email": 2, "unread": 3},
        MAX_LEN,
    ),
    (
        "My washing machine has 14 settings and I have used one for a decade. "
        "The other 13 are just there to judge me quietly.",
        {"washing": 4, "settings": 3, "laundry": 4, "machine": 2},
        MAX_LEN,
    ),
    (
        "Set 8 alarms for one 7 a.m. meeting. Slept through all 8 and woke up "
        "to a text asking if I was still joining.",
        {"alarm": 5, "meeting": 3, "7": 2, "slept": 3},
        MAX_LEN,
    ),
    (
        "The gym sent me a 'we miss you' email. I have never been so accurately "
        "called out by a machine that also wants my card number.",
        {"gym": 5, "email": 2, "card": 2, "machine": 2},
        MAX_LEN,
    ),
    (
        "Told my plant I'd water it tomorrow 6 days running. It dropped a leaf "
        "today like a passive-aggressive note.",
        {"plant": 5, "water": 3, "leaf": 4, "watering": 3},
        MAX_LEN,
    ),
    (
        "My phone battery hit 3% and I sprinted for a charger faster than I have "
        "run for any bus in my whole adult life.",
        {"battery": 5, "charger": 4, "phone": 3, "3%": 2},
        MAX_LEN,
    ),
    (
        "Ordered the 'quick 10-minute recipe'. It had 23 steps and I'm still "
        "chopping something at minute 40.",
        {"recipe": 5, "cooking": 4, "chopping": 3, "10-minute": 2},
        MAX_LEN,
    ),
    (
        "Replied 'no worries if not!' to a message that absolutely required a "
        "yes or no. Now I wait, forever, in politeness limbo.",
        {"message": 3, "text": 2, "limbo": 4, "polite": 3},
        MAX_LEN,
    ),
    (
        "Firmware update at 2% battery. The laptop chose violence and now I "
        "own a very expensive black rectangle.",
        {"firmware": 5, "update": 3, "laptop": 4, "battery": 2},
        MAX_LEN,
    ),
    (
        "Group chat asked who's free this weekend. Eleven people said 'maybe' "
        "and somehow that meant nobody, again.",
        {"group": 3, "chat": 3, "weekend": 4, "maybe": 5},
        MAX_LEN,
    ),
    (
        "Put the laundry in the dryer. The dryer has been 'almost done' for an "
        "hour, exactly like every estimate I've ever given.",
        {"dryer": 5, "laundry": 3, "estimate": 4, "done": 2},
        MAX_LEN,
    ),
]


def score(text: str, rating: dict[str, int]) -> int:
    """Rate a line by its strongest keyword, plus digit and brevity bonuses.

    The rating dict keys are lowercased; the query text is lowercased too so the
    match is case-insensitive. MAX over all matching keys (never the first hit),
    so a line is scored at its strongest signal, not its weakest.
    """
    rlow = {k.lower(): v for k, v in rating.items()}
    low = text.lower()
    base = max((v for k, v in rlow.items() if k in low), default=0)
    digit = DIGIT_BONUS if re.search(r"\d", text) else 0
    brevity = BREVITY_BONUS if len(text.strip()) <= BREVITY_CEILING else 0
    return base + digit + brevity


def valid(text: str) -> bool:
    body = text.strip()
    return 1 <= len(body) <= MAX_LEN and "\n" not in body


def mutate(text: str, rng: random.Random) -> str:
    """A light phrasing nudge — the joke stays, the wording shifts."""
    swaps = [
        ("My ", "Our "),
        ("my ", "your "),
        ("I ", "I still "),
        ("So ", ""),
        ("Honestly, ", ""),
        ("Basically, ", ""),
        ("somehow ", "somehow, "),
        ("again.", "yet again."),
        ("forever.", "for a while yet."),
        ("quietly.", "in silence."),
        ("still", "already"),
        ("today", "right now"),
    ]
    pool = [s for s in swaps if s[0] in text]
    if not pool:
        return text
    src, dst = rng.choice(pool)
    return text.replace(src, dst, 1)


def run_loop() -> str:
    """Sort seeds, keep the top 5, breed + rescore mutants for 10 rounds."""
    rng = random.Random(SEED)

    def rated():
        return [(t, r, score(t, r)) for t, r, _ in CANDIDATES if valid(t)]

    pool = sorted(rated(), key=lambda x: x[2], reverse=True)
    best_text, best_rating, best_score = pool[0]

    for _ in range(ROUNDS):
        seeds = pool[:TOP_K]
        mutants = []
        for text, rating, _ in seeds:
            for _ in range(2):
                m = mutate(text, rng)
                if valid(m):
                    mutants.append((m, rating, score(m, rating)))
        pool = sorted(seeds + mutants, key=lambda x: x[2], reverse=True)
        top = pool[0]
        if top[2] > best_score:
            best_text, best_rating, best_score = top

    return best_text.strip()


def main() -> int:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    line = run_loop()
    assert valid(line), f"entry is {len(line.strip())} chars, cap is {MAX_LEN}"
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
