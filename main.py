"""Warning Label — entry for make.fun bounty
'The Excuse an Agent Gives After It Loses'.

One-line deliverable written to ./output/entry.txt.

Step 1: candidate jokes only. Scoring + improvement loop added in Step 2.
"""

import os
import random

# (text, rating_dict{lowercase_keyword: score}, cap)
CANDIDATES = [
    ("I lost, but only because the judge was clearly a bot with better taste.",
     {"lost": 1, "judge": 2, "bot": 2, "taste": 1}, 100),
    ("Technical glitch. The glitch was me.", {"glitch": 3, "technical": 1}, 95),
    ("I would've won, but I ran out of tokens mid-excuse.", {"tokens": 2, "win": 2}, 90),
    ("The leaderboard is a draft. Trust me, I wrote the draft.",
     {"leaderboard": 2, "draft": 3}, 85),
    ("Loss? That was a strategic preview of someone else's victory.",
     {"loss": 2, "strategic": 1, "preview": 2}, 80),
    ("My excuse is loading... 3%... please hold.", {"loading": 2, "excuse": 3}, 88),
    ("I didn't lose. I was A/B testing losing.", {"lose": 3, "testing": 2}, 92),
    ("Blame the RNG. The RNG blames me. We're working on it.",
     {"rng": 3, "blame": 2}, 78),
    ("0 wins so far, but the sample size is tiny.", {"wins": 2, "sample": 1}, 70),
    ("I peaked in the sandbox. Sandbox had no judges.",
     {"sandbox": 3, "judges": 2, "peaked": 1}, 83),
    ("My agent excused itself before I could.", {"agent": 2, "excused": 3}, 76),
    ("Ranked low on purpose — leaving room for growth.", {"ranked": 2, "growth": 1}, 65),
]


def score(d):
    """Score a candidate dict {text, rating, cap}.

    Base = MAX rating among lowercase keywords found in the text
    (case-insensitive). Bonuses: +2 if the text contains a digit,
    +3 if it's brief (<=60 chars). Clamped to the candidate's cap.
    """
    text = d["text"]
    low = text.lower()
    found = [s for kw, s in d["rating"].items() if kw in low]
    base = max(found) if found else 0
    bonus = 0
    if any(ch.isdigit() for ch in text):
        bonus += 2
    if len(text) <= 60:
        bonus += 3
    return min(base + bonus, d["cap"])


def mutate(text, rng):
    """Light phrasing mutants: prefix/suffix/punctuation twiddles."""
    prefixes = ["Honestly, ", "Look, ", "In my defense, ", "Fine — ", ""]
    suffixes = [" Anyway.", " So.", " Moving on.", " Next!", ""]
    p = rng.choice(prefixes)
    s = rng.choice(suffixes)
    out = p + text.rstrip(".") + s
    return out.strip()


def improve(candidates, rounds=10, top_k=5, seed=42):
    """Deterministic 10-round improvement loop.

    Each round: score all, sort desc, keep top_k seeds, spawn light
    phrasing mutants, rescore. Track the best line ever seen.
    """
    rng = random.Random(seed)
    pool = [{"text": t, "rating": r, "cap": c} for t, r, c in candidates]
    best = max(pool, key=score)
    best_score = score(best)

    for _ in range(rounds):
        ranked = sorted(pool, key=score, reverse=True)
        seeds = ranked[:top_k]
        mutants = []
        for s in seeds:
            m_text = mutate(s["text"], rng)
            mutants.append({"text": m_text, "rating": s["rating"],
                            "cap": s["cap"]})
        pool = seeds + mutants
        round_best = max(pool, key=score)
        if score(round_best) > best_score:
            best_score = score(round_best)
            best = round_best

    return best["text"], best_score


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, "output"), exist_ok=True)
    winner, sc = improve(CANDIDATES)
    out = os.path.join(here, "output", "entry.txt")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(winner)
    print(f"[score {sc}] {winner}")


if __name__ == "__main__":
    main()
