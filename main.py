"""One Sentence, One Journey — make.fun bounty entry.

Author: investwl
Repo: https://github.com/investwl/warning-label
Bounty: https://make.fun/bounty/u-gudril-cool-one-sentence-one-journey-410686ca

Deliverable: a single sentence. The program drafts ~12 candidate
jokes, scores them against a keyword rubric plus bonuses, runs a
deterministic 10-round improvement loop (top-5 seeds, light phrasing
mutants, best-ever tracking), and writes only the winner to
./output/entry.txt.
"""

import os
import random

# Each candidate is (text, rating_dict{lowercase_keyword: score}, cap).
# cap = hard ceiling on the final score for this candidate.
CANDIDATES = [
    (
        "I planned one sentence, one journey, but the sentence took a detour "
        "and never came back.",
        {"journey": 3, "detour": 4, "sentence": 2},
        90,
    ),
    (
        "One sentence, one journey: step one was packing my punctuation.",
        {"journey": 3, "step": 2, "punctuation": 4},
        88,
    ),
    (
        "My one-sentence journey began with a comma and ended in a full stop, "
        "which is exactly how I feel.",
        {"journey": 3, "comma": 3, "full stop": 4},
        90,
    ),
    (
        "I set out on a one-sentence journey and immediately got lost in the "
        "footnotes.",
        {"journey": 3, "lost": 3, "footnotes": 4},
        85,
    ),
    (
        "One sentence, one journey — the journey was fine, the sentence never "
        "found its verb.",
        {"journey": 3, "verb": 4, "sentence": 2},
        88,
    ),
    (
        "I packed light for my one-sentence journey: just one word and a lot "
        "of hope.",
        {"journey": 3, "word": 3, "hope": 2},
        82,
    ),
    (
        "My one-sentence journey was going great until the semicolon showed up "
        "and made it two sentences.",
        {"journey": 3, "semicolon": 4, "two": 2},
        90,
    ),
    (
        "One sentence, one journey: I took the scenic route and forgot the "
        "punchline at home.",
        {"journey": 3, "punchline": 4, "scenic": 3},
        88,
    ),
    (
        "I left for a one-sentence journey with a capital letter and came back "
        "with a lowercase one.",
        {"journey": 3, "capital": 3, "lowercase": 4},
        85,
    ),
    (
        "One sentence, one journey — shortest trip ever, the sentence ran out "
        "of words after three.",
        {"journey": 3, "shortest": 3, "words": 2},
        84,
    ),
    (
        "My one-sentence journey was delayed because the sentence missed its "
        "connecting clause.",
        {"journey": 3, "delayed": 3, "clause": 4},
        88,
    ),
    (
        "One sentence, one journey: I travelled so far the sentence needed a "
        "passport.",
        {"journey": 3, "far": 2, "passport": 4},
        86,
    ),
]


# Light phrasing mutants applied to seeds to breed the next generation.
MUTANTS = [
    ("One sentence, one journey — ", "One sentence, one journey: "),
    ("One sentence, one journey: ", "One sentence, one journey — "),
    ("I ", "So I "),
    ("My ", "This "),
    ("just ", ""),
    ("really ", ""),
    ("actually ", ""),
    ("immediately ", "right away "),
    ("exactly ", "pretty much "),
    ("never ", "just never "),
    (" took", " went and took"),
    (" got lost", " got completely lost"),
]


def score(d):
    """Score a candidate dict {text, rating, cap} -> int.

    Base = MAX rating among keywords actually found in the text
    (case-insensitive substring). Plus +6 for containing any digit,
    plus a brevity bonus (+4 if <= 12 words, +2 if <= 18 words).
    Result is clamped to the candidate's cap.
    """
    text = d["text"].lower()
    ratings = [s for kw, s in d["rating"].items() if kw in text]
    base = max(ratings) if ratings else 0
    total = base
    if any(ch.isdigit() for ch in d["text"]):
        total += 6
    words = len(d["text"].split())
    if words <= 12:
        total += 4
    elif words <= 18:
        total += 2
    return min(total, d["cap"])


def improve(cands):
    """Run the deterministic 10-round improvement loop.

    Each round: sort by score desc, keep the top 5 as seeds, spawn
    light phrasing mutants of each seed, rescore everything, and track
    the best (score, text) ever seen. Deterministic via fixed seed.
    Returns the best-ever (score, text).
    """
    rng = random.Random(42)

    def as_dicts(texts):
        out = []
        for t in texts:
            for cd in cands:
                if cd["text"] == t:
                    out.append({"text": t, "rating": cd["rating"],
                                "cap": cd["cap"]})
                    break
            else:
                out.append({"text": t, "rating": {}, "cap": 100})
        return out

    texts = [cd["text"] for cd in cands]
    pool = as_dicts(texts)
    best = max(pool, key=score)

    for _ in range(10):
        pool.sort(key=score, reverse=True)
        seeds = pool[:5]
        # Track best ever seen before mutating.
        if pool:
            top = max(pool, key=score)
            if score(top) > score(best):
                best = top
        mutants = []
        for s in seeds:
            for old, new in MUTANTS:
                if old in s["text"]:
                    mutants.append({"text": s["text"].replace(old, new, 1),
                                    "rating": s["rating"], "cap": s["cap"]})
        # A couple of random light trims to keep the pool diverse.
        for s in seeds:
            words = s["text"].split()
            if len(words) > 8:
                mutants.append({"text": " ".join(words[:-1]),
                                "rating": s["rating"], "cap": s["cap"]})
        pool = seeds + mutants
        if mutants:
            rng.choice(mutants)  # consume RNG deterministically

    for s in pool:
        if score(s) > score(best):
            best = s
    return score(best), best["text"]


def main():
    """Score all candidates, improve, and write only the winner."""
    dicts = [{"text": t, "rating": r, "cap": c} for t, r, c in CANDIDATES]
    _, winner = improve(dicts)
    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner if winner.endswith(("\n",)) else winner + "\n")


if __name__ == "__main__":
    main()
