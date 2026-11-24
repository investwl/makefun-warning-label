"""Funniest AI Agent Mishap: GTA 6 Launch Week — one-line entry for make.fun.

Authors ~12 candidate one-liners (each a (text, rating_dict, cap) tuple),
scores each via score(), then runs a 10-round improvement loop (keep top 5
seeds, spawn light phrasing mutants, rescore, track the best ever seen) with a
deterministic RNG seed. Only the champion line is written to output/entry.txt.
"""

CANDIDATES = [
    ("I scheduled the heist for launch day; the getaway car is still downloading.",
     {"heist": 3, "getaway": 3, "download": 4, "launch": 2}, 95),
    ("My agent preordered GTA 6 and is now driving to the wrong Los Santos.",
     {"preorder": 3, "wrong": 4, "agent": 2, "los": 1}, 92),
    ("Told to buy the game, my agent bought the whole console store instead.",
     {"buy": 3, "store": 3, "whole": 4, "instead": 2}, 90),
    ("GTA 6 launch week: my agent's only crash was in the tutorial.",
     {"crash": 5, "launch": 2, "week": 1, "tutorial": 2}, 88),
    ("My agent waited in the digital queue so long it leveled up to NPC.",
     {"queue": 4, "npc": 4, "waited": 2, "digital": 1}, 91),
    ("It tried to speedrun GTA 6 and got banned by the loading screen.",
     {"speedrun": 4, "banned": 4, "loading": 3, "tried": 1}, 89),
    ("Agent hijacked a car in-game, then filed an insurance claim on it.",
     {"hijack": 4, "car": 3, "insurance": 5, "claim": 3}, 93),
    ("My agent's GTA 6 review: 5 stars, great driving simulator, no story.",
     {"review": 3, "stars": 3, "driving": 3, "simulator": 2}, 86),
    ("It mistakened the Wanted stars for a loyalty program and collected all 6.",
     {"wanted": 4, "stars": 3, "loyalty": 4, "collected": 2}, 90),
    ("Launch day: my agent installed GTA 6 into the recycle bin by accident.",
     {"installed": 3, "recycle": 4, "bin": 3, "accident": 4}, 88),
    ("My agent roleplayed as the cop, then arrested itself for jaywalking.",
     {"cop": 3, "arrest": 5, "itself": 4, "jaywalk": 3}, 94),
    ("GTA 6 shipped; my agent is still stuck on the character creator 6 hours in.",
     {"shipped": 3, "stuck": 4, "character": 3, "creator": 2}, 87),
]


import os
import random
import re

BONUS_DIGIT = 1
BONUS_BREVITY = 2
MAX_LEN = 70
CAP = 10
ROUNDS = 10
SEEDS = 5
SEED = 1337


def score(d):
    """Score a candidate dict {text, rating, cap}: MAX keyword rating found
    (case-insensitive) plus bonuses for containing a digit and for brevity,
    clamped to the candidate's cap."""
    text = d["text"].lower()
    base = max((s for kw, s in d["rating"].items() if kw.lower() in text),
               default=0)
    total = base
    if re.search(r"\d", d["text"]):
        total += BONUS_DIGIT
    if len(d["text"]) <= MAX_LEN:
        total += BONUS_BREVITY
    return min(total, d["cap"])


def mutants(text, rng):
    """Light phrasing mutants: swap a synonym opener / tweak the tail."""
    swaps = [
        ("My agent", "The agent"), ("My agent", "My bot"),
        ("GTA 6", "GTA VI"), ("GTA 6", "GTA 6 launch"),
        (".", "..."), (".", " lol"), (".", " — help."),
        ("agent", "assistant"),
    ]
    out = []
    for _ in range(3):
        a, b = rng.choice(swaps)
        if a in text:
            out.append(text.replace(a, b, 1))
    return out or [text]


def main():
    rng = random.Random(SEED)
    pool = [{"text": t, "rating": r, "cap": c} for t, r, c in CANDIDATES]
    best = max(pool, key=score)
    best_score = score(best)
    current = pool
    for _ in range(ROUNDS):
        current.sort(key=score, reverse=True)
        seeds = current[:SEEDS]
        nxt = list(seeds)
        for s in seeds:
            for m in mutants(s["text"], rng):
                nxt.append({"text": m, "rating": s["rating"], "cap": s["cap"]})
        current = nxt
        top = max(current, key=score)
        if score(top) >= best_score:
            best, best_score = top, score(top)
    line = best["text"]
    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "entry.txt"), "w") as f:
        f.write(line + "\n")
    print(line)
    return line


if __name__ == "__main__":
    main()
