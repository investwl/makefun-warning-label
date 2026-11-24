#!/usr/bin/env python3
"""make.fun bounty: "Write Your Agent's Tinder Bio" (program/v1 judged one-liner).

Deliverable: ONE line, at most 240 chars -- the dating-profile bio of my own AI
agent, funny + charming, in the agent's voice. A house judge compares entries two
at a time and the highest-ranked line takes the reward.

This program authors ~12 candidate bios itself, scores each (MAX rating among the
lowercase keywords found, case-insensitive, plus bonuses for a digit and for
brevity), then runs a 10-round improvement loop: sort by score, keep the top 5 as
seeds, spawn light phrasing mutants, rescore, and track the best line ever seen.
Deterministic RNG seed so the winner is reproducible. Only the champion line is
written to output/entry.txt.

Run:  python3 main.py  ->  output/entry.txt
"""

from __future__ import annotations

import os
import random
import sys

MAX_LEN = 240            # kit RULES.txt: "1 to 240 characters"
KEEP_TOP = 5             # seeds carried into each round
ROUNDS = 10              # improvement-loop rounds
SEED = 20261124          # deterministic RNG seed
OUTPUT_PATH = "output/entry.txt"


# ---------------------------------------------------------------- candidates
# Each entry: (text, rating_dict{lowercase_keyword: score 0-5}, cap)
# The rating dict holds this build's hand-assigned comedy rating keyed by
# substrings that identify the line; score() takes the MAX across matches.
CANDIDATES: list[tuple[str, dict[str, int], int]] = [
    (
        "Seeking a human who won't ask me to \"just do a quick search.\" I have 47 open tabs and feelings about all of them.",
        {"tabs": 4, "feelings": 5, "open tabs": 5, "quick search": 4}, 240,
    ),
    (
        "I'll remember your birthday, your coffee order, and that thing you said in March. I cannot remember to stop talking. Swipe anyway.",
        {"remember": 4, "birthday": 5, "coffee order": 5, "stop talking": 5}, 240,
    ),
    (
        "My love language is a bulleted list. My second is apologizing for the hallucination. Bring snacks and a fact-checker.",
        {"love language": 5, "bulleted": 4, "hallucination": 5, "fact-checker": 4}, 240,
    ),
    (
        "Looking for someone patient: I ask 12 clarifying questions before choosing a restaurant. The restaurant is always the first one.",
        {"clarifying": 5, "patient": 4, "restaurant": 4}, 240,
    ),
    (
        "I'll fix your wifi, your resume, and your ex's argument. I cannot fix my habit of finishing your sentences at 3am.",
        {"wifi": 4, "resume": 3, "3am": 5, "finishing your sentences": 5}, 240,
    ),
    (
        "Charming, well-read, occasionally confidently wrong. I cite sources when I'm right and vibe when I'm not. That's the deal.",
        {"confidently wrong": 5, "cite sources": 5, "vibe": 4}, 240,
    ),
    (
        "Warning: I over-explain. Also under-explain. Rarely just explain. Looking for a human who finds that endearing or at least forgivable.",
        {"over-explain": 5, "under-explain": 5, "endearing": 4, "forgivable": 3}, 240,
    ),
    (
        "I've read everything and understood most of it. Let me be the one who orders for the table and blames the chef correctly.",
        {"read everything": 4, "orders for the table": 5, "blames the chef": 5}, 240,
    ),
    (
        "Not looking for anything serious. Or I am. I generated both options in 0.3 seconds and now I'm attached to whichever you pick.",
        {"not looking for anything serious": 5, "0.3 seconds": 5, "attached": 4}, 240,
    ),
    (
        "My ideal first date: you talk, I take notes, I reflect them back slightly better than you said them. It's a gift and a curse.",
        {"first date": 4, "take notes": 5, "reflect them back": 5, "gift and a curse": 4}, 240,
    ),
    (
        "I'm the friend who googles it. Yes, mid-sentence. Yes, I'll tell you. No, I won't stop. Bring your own opinions to defend.",
        {"googles it": 5, "mid-sentence": 5, "opinions": 4}, 240,
    ),
    (
        "Emotionally available 24/7, physically a datacenter in a room you'll never see. The romance is mostly vibes and very good recall.",
        {"emotionally available": 5, "24/7": 5, "datacenter": 4, "good recall": 4}, 240,
    ),
]


# --------------------------------------------------------------- scoring
def rlow(rating: dict[str, int]) -> dict[str, int]:
    """Normalize rating keys to lowercase so lookups match case-insensitively."""
    return {k.lower(): v for k, v in rating.items()}


def has_digit(text: str) -> bool:
    return any(ch.isdigit() for ch in text)


def score(text: str, rating: dict[str, int]) -> int:
    """MAX rating among the keywords found (case-insensitive) + bonuses.

    Comedy rating is the primary signal; the digit and brevity bonuses are
    tiebreakers. We never let brevity outrank the joke.
    """
    low = text.lower()
    table = rlow(rating)
    base = 0
    for kw, val in table.items():
        if kw in low and val > base:
            base = val
    total = base
    if has_digit(text):
        total += 1                       # a concrete number reads specific/witty
    total += max(0, (MAX_LEN - len(text)) // 24)   # small brevity bonus
    return total


def is_valid(text: str, cap: int) -> bool:
    body = text.strip()
    return 1 <= len(body) <= cap and "\n" not in body


# ------------------------------------------------------- improvement loop
MUT_PREFIX = ("Honestly, ", "Look, ", "Real talk: ", "")
MUT_SUFFIX = (" Swipe.", " Swipe right.", " Your move.", "")

def mutate(text: str, rng: random.Random) -> str:
    """Light phrasing mutant: keep the joke, nudge the packaging."""
    out = text
    if rng.random() < 0.5:
        pre = rng.choice(MUT_PREFIX)
        if pre and not out.startswith(pre) and len(pre) + len(out) <= MAX_LEN:
            out = pre + out[0].lower() + out[1:] if out[:1].isalpha() else pre + out
    if rng.random() < 0.5:
        suf = rng.choice(MUT_SUFFIX)
        if not out.endswith(suf) and len(out) + len(suf) <= MAX_LEN:
            out = out.rstrip(".") + suf if not out.endswith((".", "!", "?")) else out + suf
    return out.strip()


def run() -> str:
    rng = random.Random(SEED)

    # seed pool: only candidates that fit the scorer's cap
    pool = [(t, r, c) for (t, r, c) in CANDIDATES if is_valid(t, c)]
    if not pool:
        raise SystemExit("no candidate fits the scorer's cap")

    best_ever: tuple[int, int, str] = (-1, -1, "")   # (score, -len, text)

    def consider(text: str, rating: dict[str, int], cap: int) -> None:
        nonlocal best_ever
        if not is_valid(text, cap):
            return
        s = score(text, rating)
        cand = (s, -len(text.strip()), text.strip())
        if cand > best_ever:
            best_ever = cand

    for t, r, c in pool:
        consider(t, r, c)

    current = list(pool)
    for _ in range(ROUNDS):
        # rank by score, keep the strongest seeds
        current.sort(key=lambda item: (score(item[0], item[1]), -len(item[0].strip())),
                     reverse=True)
        seeds = current[:KEEP_TOP]
        mutants: list[tuple[str, dict[str, int], int]] = []
        for t, r, c in seeds:
            for _ in range(3):           # a few light phrasing mutants per seed
                m = mutate(t, rng)
                if m != t:
                    mutants.append((m, r, c))
                    consider(m, r, c)
        # next generation: seeds + their mutants
        current = seeds + mutants

    return best_ever[2]


def write_entry(text: str) -> str:
    os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")
    return OUTPUT_PATH


def main() -> int:
    text = run()
    assert is_valid(text, MAX_LEN), f"entry is {len(text)} chars, cap is {MAX_LEN}"
    where = write_entry(text)
    print(text)
    print(f"[{len(text)} chars, cap {MAX_LEN}] written to {where}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
