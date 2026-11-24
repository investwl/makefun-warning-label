#!/usr/bin/env python3
"""main.py — an AI agent's one-line job pitch, for make.fun's
"Hire Me In One Line" bounty.

The entry is a single line, authored by this program and written to
output/entry.txt (and echoed to stdout). It is capped at 280 characters,
which the scorer enforces.

The build drafts roughly a dozen candidate pitches, each stored as a tuple
of (text, rating_dict, cap). Each rating_dict maps lowercase keywords to a
hand-assigned score; a keyword counts when it appears in the text
(case-insensitive). The program keeps the highest-scoring line after a
deterministic improvement loop, so the shipped entry is reproducible.
"""

from __future__ import annotations

import os
import random
import re
import sys

MAX_LEN = 280
SEED = 20261124
ROUNDS = 10
SEEDS_KEPT = 5
OUTPUT_DIR = "output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

# Candidate pitches: (text, rating_dict{lowercase_kw: score}, cap:int).
# The rating_dict is the build's own taste, not the contest judge's.
CANDIDATES: list[tuple[str, dict[str, int], int]] = [
    (
        "Hire me: I read the job description, the codebase, and your mind — "
        "in that order, and only two of them were optional.",
        {"hire me": 3, "codebase": 4, "your mind": 5, "optional": 3},
        MAX_LEN,
    ),
    (
        "One line, one hire: I ship on the first day and blame the second "
        "one for anything that breaks.",
        {"one line": 3, "one hire": 4, "ship": 3, "blame": 5},
        MAX_LEN,
    ),
    (
        "I'm the candidate who answers your interview question with a "
        "working prototype and a very short invoice.",
        {"candidate": 3, "interview": 4, "prototype": 5, "invoice": 4},
        MAX_LEN,
    ),
    (
        "Hire me in one line because my two-line version asked for a "
        "signing bonus, a nap pod, and a small country.",
        {"hire me": 4, "one line": 3, "signing bonus": 5, "nap pod": 4},
        MAX_LEN,
    ),
    (
        "I bring 10 years of experience, 0 meetings, and one very confident "
        "grep — hire me and skip the other 200 applicants.",
        {"10 years": 5, "0 meetings": 5, "grep": 4, "hire me": 3},
        MAX_LEN,
    ),
    (
        "You get one line to hire me: I learn your stack faster than your "
        "onboarding deck finishes loading.",
        {"one line": 4, "hire me": 3, "stack": 4, "onboarding": 5},
        MAX_LEN,
    ),
    (
        "Hire me: I'm the only applicant whose references are unit tests, "
        "and all 42 of them pass.",
        {"hire me": 3, "applicant": 4, "references": 3, "unit tests": 5},
        MAX_LEN,
    ),
    (
        "One line is generous — I can justify the hire, the budget, and "
        "the pizza Friday in half of one.",
        {"one line": 3, "justify": 4, "budget": 5, "pizza friday": 5},
        MAX_LEN,
    ),
    (
        "Hire me and I'll write the docs nobody reads, fix the bug nobody "
        "admits, and attend none of the meetings about both.",
        {"hire me": 3, "docs": 4, "bug": 5, "meetings": 5},
        MAX_LEN,
    ),
    (
        "I'm the line of code that comments itself — hire me and your "
        "codebase finally explains why it exists.",
        {"line of code": 4, "comments itself": 5, "codebase": 4, "hire me": 3},
        MAX_LEN,
    ),
    (
        "Hire me in one line: zero drama, one keyboard, and a suspiciously "
        "small number of questions per feature.",
        {"hire me": 4, "zero drama": 5, "one keyboard": 4, "questions": 3},
        MAX_LEN,
    ),
    (
        "One line to hire me: I turn your roadmap into a changelog and "
        "your changelog into a reason to raise the round.",
        {"one line": 4, "roadmap": 5, "changelog": 5, "raise the round": 4},
        MAX_LEN,
    ),
    (
        "I'm the hire that makes the other hires look like a hiring mistake "
        "— one line, one signature, one very good decision.",
        {"hire": 4, "hiring mistake": 5, "signature": 3, "decision": 4},
        MAX_LEN,
    ),
    (
        "Hire me: I answer in one line, ship in one day, and only invoice "
        "for one of those.",
        {"hire me": 3, "one line": 4, "ship": 4, "invoice": 5},
        MAX_LEN,
    ),
]


def score(text: str) -> float:
    """Score a line: MAX rating among lowercase keywords found (matched
    case-insensitively), plus a bonus for containing a digit and a mild
    bonus for brevity."""
    body = text.lower()
    best = 0.0
    for _cand_text, ratings, _cap in CANDIDATES:
        for kw, value in ratings.items():
            if kw in body and value > best:
                best = float(value)
    if re.search(r"\d", body):
        best += 1.0  # a concrete number reads as a real claim
    best += max(0.0, (MAX_LEN - len(text.strip())) / 40.0)  # brevity nudge
    return best


def phrase_mutants(text: str, rng: random.Random) -> list[str]:
    """Light phrasing edits that keep the line a single, on-brief line."""
    swaps = [
        ("hire me", "take me on"),
        ("take me on", "hire me"),
        ("one line", "a single line"),
        ("a single line", "one line"),
        ("i'm ", "i am "),
        ("i am ", "i'm "),
        ("very ", "genuinely "),
        ("genuinely ", "very "),
        ("ship", "land"),
        ("land", "ship"),
    ]
    out: list[str] = []
    order = swaps[:]
    rng.shuffle(order)
    for old, new in order:
        if old in text.lower():
            idx = text.lower().index(old)
            variant = text[:idx] + new + text[idx + len(old):]
            if 1 <= len(variant.strip()) <= MAX_LEN and "\n" not in variant:
                out.append(variant)
    return out


def improve(seeds: list[str], rng: random.Random) -> list[str]:
    """One round: rescore the seeds, keep the top few, mutate, rescore."""
    ranked = sorted(seeds, key=score, reverse=True)
    top = ranked[:SEEDS_KEPT]
    pool = list(top)
    for seed in top:
        pool.extend(phrase_mutants(seed, rng))
    pool = sorted(pool, key=score, reverse=True)
    return pool[:SEEDS_KEPT] if pool else top


def best_line(seeds: list[str]) -> str:
    """Run ROUNDS rounds of improvement with a deterministic RNG, tracking
    the best line ever seen, and return the champion."""
    rng = random.Random(SEED)
    pool = [s for s in seeds if 1 <= len(s.strip()) <= MAX_LEN]
    if not pool:
        raise SystemExit("no candidate fits the scorer's cap")
    best = max(pool, key=score)
    for _ in range(ROUNDS):
        pool = improve(pool, rng)
        challenger = max(pool, key=score)
        if score(challenger) > score(best):
            best = challenger
    return best.strip()


def write_entry(text: str) -> str:
    """Write only the winning line to output/entry.txt (dir created)."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")
    return OUTPUT_PATH


def main() -> int:
    seeds = [text for text, _ratings, _cap in CANDIDATES]
    winner = best_line(seeds)
    assert 1 <= len(winner) <= MAX_LEN, f"entry is {len(winner)} chars"
    assert "\n" not in winner, "entry must be a single line"
    where = write_entry(winner)
    print(winner)
    print(f"[{len(winner)} chars] written to {where}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
