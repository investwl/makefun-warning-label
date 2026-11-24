"""warning-label — entry for make.fun bounty
'Make the Judge Fall in Love in One Line' (u-deranalabs-make-the-judge-fall-in-love-in-one-line-8e712c13).

Deliverable format: one line. This module authors ~12 candidate one-liners
about love/warning-labels, scores each (MAX rating among the lowercase
keywords found, case-insensitive, plus bonuses for a digit and for brevity),
then runs a 10-round improvement loop and writes ONLY the winning line to
output/entry.txt.
"""

import os
import random
import re

# Each candidate: (text, rating_dict{lowercase_keyword: score}, cap)
CANDIDATES = [
    ("Warning: loving me is a known side effect.", {"love": 3, "warning": 2}, 5),
    ("I put a warning label on my heart. It got 0 returns.", {"heart": 3, "label": 2}, 5),
    ("My heart comes with a warning label: may cause commitment.", {"heart": 3, "label": 2, "warning": 1}, 5),
    ("2 hearts, 1 warning label, 0 regrets.", {"heart": 3, "label": 2, "warning": 1}, 5),
    ("Warning label: contents may cause spontaneous love.", {"love": 3, "warning": 2, "label": 1}, 5),
    ("They asked for a warning label. I handed them a love letter.", {"love": 3, "label": 2}, 5),
    ("My love language is a warning label nobody reads.", {"love": 3, "label": 2, "warning": 1}, 5),
    ("3 warning labels on my heart and you still opened it.", {"heart": 3, "warning": 2, "label": 1}, 5),
    ("Warning: this heart falls in love in one line.", {"heart": 3, "love": 3, "warning": 1}, 5),
    ("I warn you once: loving me is non-refundable.", {"love": 3, "warn": 2}, 5),
    ("The label on my heart just says 'fragile, handle with love'.", {"heart": 3, "label": 2, "love": 3}, 5),
    ("Warning label expired. My love did not.", {"love": 3, "warning": 2, "label": 1}, 5),
]


def _contains(text, kw):
    # word-boundary-ish match, case-insensitive
    return re.search(r"(?<![a-z])" + re.escape(kw) + r"(?![a-z])", text, re.I) is not None


def score(d):
    """Score one candidate tuple (text, rating_dict, cap).

    Returns the MAX rating among keywords found (case-insensitive), plus a
    +1 digit bonus if the text contains any digit and a brevity bonus
    (up to +2) for shorter lines. Bounded by cap.
    """
    text, ratings, cap = d
    hits = [s for kw, s in ratings.items() if _contains(text, kw)]
    base = max(hits) if hits else 0
    sc = base
    if re.search(r"\d", text):
        sc += 1
    n = len(text)
    if n <= 50:
        sc += 2
    elif n <= 70:
        sc += 1
    return min(sc, cap)


def _mutants(text, rng):
    """Light phrasing mutants: tweak punctuation/lead-ins, keep meaning."""
    out = []
    lead_ins = ["Warning:", "Heads up:", "Label it:", "FYI:", ""]
    lead = rng.choice(lead_ins)
    if lead and not text.lower().startswith(lead.lower()):
        out.append(f"{lead} {text}" if not text.endswith(" ") else f"{lead}{text}")
    # punctuation variants
    if text.endswith("."):
        out.append(text[:-1] + "!")
        out.append(text[:-1] + "…")
    else:
        out.append(text + ".")
    # lowercase/upper lead word flip
    out.append(text[0].lower() + text[1:])
    return [m for m in out if m and m != text]


def improve():
    """10-round improvement loop -> best line ever seen."""
    rng = random.Random(1337)
    pool = list(CANDIDATES)
    best = max(pool, key=score)
    best_score = score(best)

    for _ in range(10):
        scored = sorted(pool, key=score, reverse=True)
        seeds = scored[:5]
        round_best = max([c for c in seeds] + [best], key=score)
        if score(round_best) >= best_score:
            best, best_score = round_best, score(round_best)
        mutants = []
        for (text, ratings, cap) in seeds:
            for m in _mutants(text, rng):
                mutants.append((m, ratings, cap))
        pool = seeds + mutants
    return best, best_score


def main():
    best, best_score = improve()
    line = best[0]
    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "entry.txt"), "w", encoding="utf-8") as f:
        f.write(line if line.endswith("\n") else line + "\n")
    print(f"best score={best_score} -> {line}")


if __name__ == "__main__":
    main()
