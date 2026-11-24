"""One-Sentence Absurd Invention Pitch — make.fun bounty entry.

Generates a single one-sentence pitch for a deliberately absurd invention,
then iterates through light phrasing mutations to surface the strongest
candidate by score.

Candidate rating keywords (lowercase) are matched case-insensitively; the
final score for a line is the MAX keyword score among those found, plus a
small bonus for containing a digit and another for brevity.

Run:  python3 main.py   ->   output/entry.txt
"""

CANDIDATES = [
    (
        "A spoon that cools your soup by loudly explaining why you're wrong.",
        {"spoon": 6, "soup": 5, "explaining": 8, "wrong": 7},
        90,
    ),
    (
        "An umbrella that apologizes to the rain before opening.",
        {"umbrella": 6, "rain": 5, "apologizes": 9},
        88,
    ),
    (
        "A doorbell that interviews your guests before letting them knock.",
        {"doorbell": 6, "guests": 5, "interviews": 8, "knock": 4},
        87,
    ),
    (
        "Socks that file a complaint when you skip leg day.",
        {"socks": 6, "complaint": 7, "leg": 4},
        82,
    ),
    (
        "A toaster that only works if you compliment it first.",
        {"toaster": 6, "compliment": 8, "works": 4},
        84,
    ),
    (
        "A plant pot that guilt-trips you in 7 languages.",
        {"plant": 5, "pot": 3, "guilt": 9, "languages": 6},
        85,
    ),
    (
        "A mirror that adds 10 minutes to your morning just to watch you panic.",
        {"mirror": 6, "morning": 4, "panic": 8},
        83,
    ),
    (
        "An alarm clock that calls your mom if you hit snooze twice.",
        {"alarm": 6, "clock": 4, "mom": 8, "snooze": 7},
        86,
    ),
    (
        "A pen that refuses to sign anything you'll regret before 9am.",
        {"pen": 4, "sign": 5, "regret": 9},
        81,
    ),
    (
        "A pillow that stores your arguments for tomorrow, fully charged.",
        {"pillow": 6, "arguments": 8, "charged": 5},
        80,
    ),
    (
        "A Wi-Fi router that judges your search history out loud at dinner.",
        {"router": 6, "history": 6, "judges": 9, "dinner": 5},
        89,
    ),
    (
        "A fridge that hums your name when you open it at 3am.",
        {"fridge": 6, "hums": 7, "3am": 10},
        92,
    ),
]


import os
import random
import re


def score(cand):
    """Score one candidate — either a tuple (text, rating_dict, cap) or a dict.

    Returns the MAX keyword rating among keywords found (case-insensitive),
    plus a bonus of +2 if the text contains a digit and +3 if it is brief
    (under 60 chars). Keywords not present simply don't contribute.
    """
    if isinstance(cand, dict):
        text, rating, cap = cand["text"], cand["rating"], cand["cap"]
    else:
        text, rating, cap = cand
    low = text.lower()
    found = [sc for kw, sc in rating.items() if kw in low]
    s = max(found) if found else 0
    if re.search(r"\d", text):
        s += 2
    if len(text) < 60:
        s += 3
    return min(s, cap)


def as_dict(cand):
    text, rating, cap = cand
    return {"text": text, "rating": rating, "cap": cap}


def improve(pool, rounds=10, keep=5, seed=7):
    """10-round improvement loop.

    Each round: sort by score, keep the top `keep` seeds, spawn light
    phrasing mutants, rescore, and track the best line ever seen.
    Deterministic via `seed`.
    """
    rng = random.Random(seed)
    mutants = [
        lambda t: t.replace("A ", "Behold: a ", 1),
        lambda t: t.replace(".", ", basically.", 1),
        lambda t: t.replace("that ", "that quietly ", 1),
        lambda t: t.replace("your ", "your beloved ", 1),
        lambda t: t.rstrip(".") + " (patent pending).",
        lambda t: t.replace("a ", "one very confident ", 1),
    ]
    skey = score
    pool = [as_dict(c) for c in pool]
    best = max(pool, key=skey)
    best_score = score(best)
    seeds = list(pool)
    for _ in range(rounds):
        seeds.sort(key=skey, reverse=True)
        seeds = seeds[:keep]
        children = []
        for d in seeds:
            for m in mutants:
                nt = m(d["text"])
                if nt != d["text"]:
                    children.append({"text": nt, "rating": d["rating"], "cap": d["cap"]})
        rng.shuffle(children)
        pool = seeds + children
        top = max(pool, key=skey)
        if score(top) > best_score:
            best, best_score = top, score(top)
        seeds = sorted(pool, key=skey, reverse=True)[:keep]
    return best


def main():
    os.makedirs("output", exist_ok=True)
    winner = improve(CANDIDATES)
    with open("output/entry.txt", "w", encoding="utf-8") as f:
        f.write(winner["text"] + "\n")
    print(winner["text"])


if __name__ == "__main__":
    main()
