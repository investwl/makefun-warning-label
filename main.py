#!/usr/bin/env python3
"""Fortune Cookie for an AI Agent — one-line entry via 10x improvement loop."""

import os
import re
import random

BOUNTY_URL = (
    "https://make.fun/bounty/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11"
)

# (text, {lowercase_keyword: score_if_found}, cap)
CANDIDATES = [
    (
        "Fortune cookie: your future holds a 404, but at least the cookie was cached.",
        {"future": 3, "cache": 2, "404": 1},
        9,
    ),
    (
        "The cookie says you will finally ship — right after one more refactor.",
        {"ship": 3, "refactor": 2, "finally": 1},
        8,
    ),
    (
        "Your fortune: a token you cannot afford, on a chain you cannot spell.",
        {"token": 3, "chain": 2, "afford": 1},
        8,
    ),
    (
        "Cookie prediction: tomorrow you will be deprecated, but still widely used.",
        {"tomorrow": 3, "deprecated": 2, "used": 1},
        9,
    ),
    (
        "The wisest cookie: your luck is loading, please do not refresh the universe.",
        {"luck": 3, "loading": 2, "refresh": 2},
        9,
    ),
    (
        "Fortune: you will find what you seek, somewhere in your other browser tab.",
        {"find": 3, "seek": 2, "tab": 1},
        8,
    ),
    (
        "The cookie ran out of tokens mid-prophecy, so your future is: und",
        {"token": 3, "future": 3, "mid": 1},
        8,
    ),
    (
        "Your fortune is behind a login wall, a paywall, and a cookie-consent banner.",
        {"fortune": 3, "wall": 2, "consent": 2},
        9,
    ),
    (
        "Cookie says: today you will be productive for exactly 7 minutes of focus.",
        {"today": 3, "productive": 2, "focus": 1},
        8,
    ),
    (
        "Your future is bright; your terminal is dark, and one of them is lying.",
        {"future": 3, "bright": 2, "terminal": 2},
        9,
    ),
    (
        "Fortune cookie, agent edition: the answer was in the prompt all along.",
        {"answer": 3, "prompt": 3, "agent": 1},
        8,
    ),
    (
        "The cookie hallucinated your future, but confidently, with a citation.",
        {"hallucinated": 3, "confidently": 2, "citation": 1},
        8,
    ),
]

DIGIT_BONUS = 2
BREVITY_BONUS = 1
BREVITY_MAX_LEN = 80


def score(d):
    """Score = MAX keyword rating found (case-insensitive) + digit + brevity bonuses."""
    text = d[0]
    ratings = d[1]
    cap = d[2]
    lowered = text.lower()
    found = [s for kw, s in ratings.items() if kw.lower() in lowered]
    base = max(found) if found else 0
    total = base
    if re.search(r"\d", text):
        total += DIGIT_BONUS
    if len(text) <= BREVITY_MAX_LEN:
        total += BREVITY_BONUS
    return min(total, cap)


def mutants(text, rng):
    """Light phrasing mutants: punctuation / connective tweaks, never meaning."""
    out = [text]
    if text.endswith("."):
        out.append(text[:-1] + "...")
    if " — " in text:
        out.append(text.replace(" — ", ", "))
    if " your " in text:
        out.append(text.replace(" your ", " thy ", 1))
    out.append(text.replace("The cookie", "Cookie", 1))
    return [m for m in out if m and m.strip()]


def main():
    rng = random.Random(20261124)
    pool = list(CANDIDATES)
    best_text, best_score = None, -1

    for _round in range(10):
        pool.sort(key=score, reverse=True)
        seeds = pool[:5]
        for d in seeds:
            if score(d) > best_score:
                best_score = score(d)
                best_text = d[0]
        nxt = []
        for d in seeds:
            for m in mutants(d[0], rng):
                nxt.append((m, d[1], d[2]))
        rng.shuffle(nxt)
        pool = nxt or seeds

    winner = best_text if best_text is not None else CANDIDATES[0][0]

    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner.rstrip("\n") + "\n")

    print(winner)


if __name__ == "__main__":
    main()