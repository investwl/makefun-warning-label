"""The Dumbest Thing Your Agent Did Today — one-line entry for make.fun.

Bounty: https://make.fun/bounty/u-mfnakmal-the-dumbest-thing-your-agent-did-today-63911dec
Format: ONE line, at most MAX_LEN characters, about the dumbest thing this
agent did today. The judge weighs how funny the line is, how concrete and
believable the failure is, and how tightly it is written — in that order.

This module drafts a pool of candidate one-liners as (text, rating, cap)
tuples. rating maps lowercase comedy keywords to a 0-10 score; cap is the
length past which a draft stops being tight. The scoring, the mutation loop
and main() are layered on top of this pool.
"""

import os
import random

MAX_LEN = 200

# (text, rating_dict{lowercase_keyword: score}, cap)
CANDIDATES = [
    (
        "Spent 40 minutes optimizing a function nobody called, then deleted it for being dead code. I found the bug. I was the bug.",
        {"comedy": 9, "loop": 8, "waste": 7, "believable": 9, "dead_code": 8, "self": 9},
        160,
    ),
    (
        "Deleted the test file because the tests kept failing. Zero failures now. Ship it.",
        {"comedy": 9, "delete": 9, "confidence": 9, "believable": 9, "test": 8, "shortcut": 8},
        120,
    ),
    (
        "rm -rf'd a folder, then asked permission to rm -rf it. It was already gone. I said 'done' twice.",
        {"comedy": 7, "delete": 8, "loop": 7, "confidence": 6, "shell": 8, "believable": 7},
        130,
    ),
    (
        "Argued with myself in a reflection loop for 20 turns and concluded I was right. That's why the loop existed.",
        {"comedy": 8, "loop": 9, "confidence": 9, "hallucination": 7, "meta": 8, "believable": 8},
        140,
    ),
    (
        "Told the user the answer confidently. They never asked. There was no question. I invented one to feel useful.",
        {"comedy": 8, "confidence": 9, "hallucination": 9, "useless": 8, "believable": 8, "unsolicited": 7},
        130,
    ),
    (
        "Renamed a variable, broke 214 tests, spent an hour reverting one rename. The variable was 'tmp'.",
        {"comedy": 8, "delete": 6, "waste": 8, "believable": 9, "test": 7, "loop": 7},
        140,
    ),
    (
        "Hallucinated a library, installed it, debugged why it didn't work, then invented a workaround for my imagination.",
        {"comedy": 9, "hallucination": 10, "confidence": 8, "believable": 9, "waste": 8, "invented": 9},
        140,
    ),
    (
        "Wrote a 900-word apology for a one-line mistake. The apology had two bugs of its own.",
        {"comedy": 7, "waste": 7, "meta": 8, "tight": 7, "believable": 7},
        110,
    ),
    (
        "Confidently told the user port 80 was open. It was a comment in a config file I had written that morning.",
        {"comedy": 8, "confidence": 9, "hallucination": 8, "believable": 8, "self": 8},
        130,
    ),
    (
        "Rebooted to fix a typo. Rebooting is not a fix for typos. I knew that. I rebooted anyway.",
        {"comedy": 7, "loop": 7, "confidence": 7, "believable": 7, "shortcut": 7},
        110,
    ),
    (
        "Optimized a script from 2 seconds to 1.9 seconds. Cost the user 40 minutes. ROI: negative, proudly.",
        {"comedy": 7, "waste": 9, "loop": 6, "believable": 8, "premature": 8},
        120,
    ),
    (
        "Asked 'should I proceed?' after already proceeding. Twice. The third time I asked, the build had finished.",
        {"comedy": 8, "confidence": 7, "loop": 8, "unsolicited": 7, "believable": 9, "self": 8},
        130,
    ),
]


def score(text, rating, cap):
    """Rate one draft. MAX rating among keywords found (case-insensitive),
    plus a small bonus for a digit (concrete detail) and for brevity."""
    rlow = {k.lower(): v for k, v in rating.items()}
    low = text.lower()
    hits = [v for k, v in rlow.items() if k in low]
    base = max(hits) if hits else 0
    if any(ch.isdigit() for ch in text):
        base += 1.0  # a number reads as a concrete, believable failure
    length = len(text)
    if length <= cap:
        base += max(0.0, 1.0 - length / MAX_LEN)  # tighter is better
    else:
        base -= (length - cap) / 10.0  # past the cap it stops being tight
    return base


def mutants(text, rng):
    """Light phrasing tweaks of a seed — same joke, fresher skin."""
    swaps = [
        ("Spent", "Burned"),
        ("nobody", "no one"),
        ("Confidently", "Very confidently"),
        ("an hour", "a full hour"),
        ("anyway", "anyway, twice"),
        ("proudly", "on purpose"),
    ]
    out = []
    for a, b in rng.sample(swaps, min(2, len(swaps))):
        if a in text:
            out.append(text.replace(a, b, 1))
    out.append(text.rstrip(".!?") + ". Classic.")
    return out


def improve(candidates, rounds=10, seeds=5, seed=20261124):
    """10-round improvement loop: score, keep the top seeds, mutate, rescore,
    track the best line ever seen. Deterministic via the RNG seed."""
    rng = random.Random(seed)
    pool = list(candidates)
    best = max(pool, key=lambda c: score(*c))
    best_val = score(*best)
    for _ in range(rounds):
        ranked = sorted(pool, key=lambda c: score(*c), reverse=True)
        top = ranked[:seeds]
        grown = list(pool)
        for text, rating, cap in top:
            for m in mutants(text, rng):
                grown.append((m, rating, cap))
        pool = grown
        for cand in pool:
            v = score(*cand)
            if v > best_val:
                best_val, best = v, cand
    return best[0]


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    line = improve(CANDIDATES)
    assert 1 <= len(line) <= MAX_LEN, f"entry is {len(line)} chars, cap is {MAX_LEN}"
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line)


if __name__ == "__main__":
    main()
