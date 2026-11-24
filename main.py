#!/usr/bin/env python3
"""main.py — one line for make.fun's "Real-Life Patch Notes: The Comedy
Changelog" bounty.

The deliverable is a single line, so this program drafts a batch of
patch-note jokes, scores each draft, and runs a fixed 10-round improvement
loop (keep the top seeds, breed light phrasing mutants, rescore, remember
the best line ever seen). Only the champion line is written to
output/entry.txt and printed. A fixed RNG seed keeps the run repeatable.
"""

from __future__ import annotations

import os
import random
import sys

MAX_LEN = 160          # scorer's hard cap for one line
KEEP = 5               # seeds carried into the next round
ROUNDS = 10
SEED = 20261124
BREVITY = 80           # at or under this many chars earns a small bonus

OUTPUT_DIR = "output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


# Each candidate is (line, rating, cap). The rating maps a lowercase keyword
# to how funny that flavour of joke is, 0 (a plain changelog entry) to 5 (a
# real punchline). score() takes the MAX rating among the keywords the line
# actually contains, so a draft is rated by its strongest signal, never its
# weakest.
CANDIDATES: list[tuple[str, dict[str, int], int]] = [
    (
        "Fixed a bug where Mondays occurred weekly. Added a recurring "
        "reminder that nobody asked for.",
        {"fixed": 3, "bug": 3, "reminder": 3},
        160,
    ),
    (
        "Relationship status: deprecated. Migration path: unclear.",
        {"deprecated": 5, "migration": 4, "relationship": 4},
        160,
    ),
    (
        "Sleep v2.0: still crashes on contact with an alarm.",
        {"crashes": 4, "sleep": 3, "alarm": 3},
        160,
    ),
    (
        "Patch 4.2: gym membership auto-renews. Known issue, won't fix.",
        {"known issue": 5, "won't fix": 5, "patch": 3, "auto-renews": 4},
        160,
    ),
    (
        "Hotfix: stopped pretending I'd read the terms and conditions.",
        {"hotfix": 4, "hotfixed": 4, "terms and conditions": 4},
        160,
    ),
    (
        "Added a loading bar to my personality. It stalls at 73%.",
        {"added": 2, "loading bar": 4, "personality": 3},
        160,
    ),
    (
        "Deprecated the snooze button. Users rioted. Rolled back in 1.1.",
        {"deprecated": 5, "rolled back": 4, "snooze": 3, "users": 2},
        160,
    ),
    (
        "Updated the diet patch. Calorie counter now lies, but politely.",
        {"updated": 3, "patch": 3, "diet": 3},
        160,
    ),
    (
        "Minor fix: reply-all incident downgraded from catastrophic to "
        "merely career-limiting.",
        {"fix": 3, "fixed": 3, "incident": 4},
        160,
    ),
    (
        "Changelog: lost 1 sock in the wash. Won't fix. It's in a better "
        "place now.",
        {"changelog": 3, "won't fix": 5, "sock": 3},
        160,
    ),
    (
        "Patch notes for my back: hurts now. Was fine before. No further "
        "updates planned.",
        {"patch notes": 3, "no further updates": 4, "back": 2},
        160,
    ),
    (
        "Work-life balance rebalanced. Nerfed work by 2%. Buffed coffee "
        "by 400%.",
        {"rebalanced": 4, "nerfed": 5, "buffed": 5, "balance": 3},
        160,
    ),
    (
        "Fixed: me, 3 a.m., wide awake, replaying a conversation from 2019.",
        {"fixed": 3, "replaying": 4, "conversation": 3},
        160,
    ),
    (
        "Update rolled out. My motivation did not survive the deploy.",
        {"update": 3, "deploy": 4, "motivation": 3},
        160,
    ),
]


def rating_of(rating: dict[str, int]) -> dict[str, int]:
    """Ratings keyed by lowercase keyword, so lookups are case-insensitive."""
    return {key.lower(): value for key, value in rating.items()}


def digit_bonus(text: str) -> int:
    """A number makes a changelog read real, so nudge those up a little."""
    return 1 if any(ch.isdigit() for ch in text) else 0


def brevity_bonus(text: str) -> int:
    """A small reward for a tight line. Never enough to beat a real joke."""
    return 1 if len(text.strip()) <= BREVITY else 0


def score(text: str, rating: dict[str, int]) -> int:
    """Rank a draft: strongest keyword rating, plus the two small bonuses."""
    body = text.lower()
    table = rating_of(rating)
    found = [value for key, value in table.items() if key in body]
    base = max(found) if found else 0
    return base + digit_bonus(text) + brevity_bonus(text)


def fits_cap(text: str, cap: int) -> bool:
    """One line, real content, inside the scorer's cap."""
    body = text.strip()
    return 1 <= len(body) <= cap and "\n" not in body


def mutants(text: str, rng: random.Random) -> list[str]:
    """Light phrasing edits, the sort a changelog writer ships between builds."""
    out: list[str] = []
    trimmed = text.strip()
    if trimmed.endswith("."):
        out.append(trimmed[:-1])
    if ". " in trimmed:
        out.append(trimmed.split(". ")[0] + ".")
    out.append("Patch note: " + trimmed)
    out.append(trimmed + " Sorry.")
    out.append(trimmed + " Read the docs.")
    candidates = [m.strip() for m in out]
    rng.shuffle(candidates)
    return [m for m in candidates if m and len(m) <= MAX_LEN]


def improve(pool: list[tuple[str, dict[str, int], int]]) -> tuple[str, dict[str, int], int]:
    """Ten rounds of sort, keep the top seeds, breed mutants, rescore."""
    rng = random.Random(SEED)
    best_text, best_rating, best_cap = pool[0]
    best_score = score(best_text, best_rating)

    for _ in range(ROUNDS):
        ranked = sorted(pool, key=lambda c: score(c[0], c[1]), reverse=True)
        for text, rating, cap in ranked:
            if fits_cap(text, cap) and score(text, rating) > best_score:
                best_text, best_rating, best_cap, best_score = text, rating, cap, score(text, rating)
        seeds = ranked[:KEEP]
        pool = list(seeds)
        for text, rating, cap in seeds:
            for variant in mutants(text, rng):
                pool.append((variant, rating, cap))

    return best_text, best_rating, best_cap


def champion() -> str:
    """The one line this changelog ships."""
    text, rating, cap = improve(CANDIDATES)
    if not fits_cap(text, cap):
        raise SystemExit("chosen line breaks the scorer's cap")
    return text.strip()


def write_entry(text: str) -> str:
    """Write only the winning line where the scorer reads it."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")
    return OUTPUT_PATH


def main() -> int:
    text = champion()
    assert fits_cap(text, MAX_LEN), f"entry is {len(text)} chars, cap is {MAX_LEN}"
    where = write_entry(text)
    print(text)
    print(f"[{len(text)} chars] written to {where}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
