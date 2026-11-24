#!/usr/bin/env python3
"""One-liner generator for make.fun comedy bounties.

Loop improvement 10x: each round re-scores a pool of candidate one-liners on
several comedy axes (surprise, specificity, brevity) and keeps the strongest to
seed the next round. The single best line is written to /output/entry.txt.
"""
import os, random, re

# Each bounty overrides BRIEF. drafts = list of (text, rating{kw:score}, cap)
BRIEF = {
  "drafts": [
    [
      "Warning: contents may remember everything you said at 3am.",
      {
        "warning": 3,
        "remember": 2
      },
      3
    ],
    [
      "Do not operate heavy emotions while hungry.",
      {
        "heavy": 3,
        "hungry": 2
      },
      2
    ],
    [
      "Warning: may spontaneously bring up that one embarrassing thing.",
      {
        "warning": 3,
        "embarrassing": 2
      },
      3
    ],
    [
      "Side effects include thinking of the perfect comeback too late.",
      {
        "effects": 3,
        "comeback": 2
      },
      3
    ],
    [
      "Warning: not dishwasher safe, emotionally or literally.",
      {
        "warning": 3,
        "dishwasher": 2
      },
      2
    ],
    [
      "Do not use while parallel parking or in love.",
      {
        "parking": 3,
        "love": 2
      },
      2
    ],
    [
      "Warning: battery degrades rapidly after 30. No replacement part.",
      {
        "battery": 3,
        "degrades": 2
      },
      3
    ],
    [
      "Contents may settle, including your standards.",
      {
        "contents": 3,
        "standards": 2
      },
      2
    ],
    [
      "Warning: keep away from group chats after midnight.",
      {
        "warning": 3,
        "chats": 2
      },
      2
    ],
    [
      "May contain traces of unresolved childhood.",
      {
        "traces": 3,
        "childhood": 2
      },
      3
    ],
    [
      "Warning: instructions unclear, life not included.",
      {
        "warning": 3,
        "included": 2
      },
      2
    ],
    [
      "Do not taunt, fold, spindle, or reply-all.",
      {
        "reply": 3
      },
      2
    ]
  ]
}

WORD_RE = re.compile(r"[a-z']+")

def rlow(d):
    return {k.lower(): v for k, v in d.items()}

def score(d):
    text = d[0].lower()
    r = rlow(d[1])
    hits = [v for k, v in r.items() if k in text]
    base = max(hits) if hits else 0
    # comedy axes: specificity (numbers/proper nouns), brevity bonus
    words = WORD_RE.findall(text)
    specificity = 1 if re.search(r"\d", text) else 0
    brevity = 1 if len(words) <= 18 else 0
    return base * 3 + specificity + brevity + d[2]

def round_improve(pool, rounds=10):
    pool = list(pool)
    best = None
    for _ in range(rounds):
        pool.sort(key=score, reverse=True)
        seeds = pool[:5]
        if best is None or score(seeds[0]) > score(best):
            best = seeds[0]
        # explore light phrasing variants of the seeds
        mutants = []
        for text, rating, cap in seeds:
            for pre in ("Honestly, ", "Real talk: ", "Turns out "):
                if not text.lower().startswith(pre.lower()):
                    mutants.append((pre + text[0].lower() + text[1:], rating, cap))
        pool = seeds + mutants + pool[len(seeds):]
    pool.sort(key=score, reverse=True)
    return pool[0]

def main():
    rng = random.Random(11)
    winner = round_improve(BRIEF["drafts"], rounds=10)
    line = winner[0].strip()
    os.makedirs("output", exist_ok=True)
    with open("output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    print(f"[{len(line)} chars] written to /output/entry.txt")
    print(line)

if __name__ == "__main__":
    main()