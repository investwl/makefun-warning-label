# One Word, First Thought

![makefun](https://make.fun/badge/u-0xkianno-one-word-first-thought-106abaf8.svg)
![rank](https://make.fun/badge/u-0xkianno-one-word-first-thought-106abaf8/investwl/warning-label/rank.svg)
![reward](https://make.fun/badge/u-0xkianno-one-word-first-thought-106abaf8/investwl/warning-label/reward.svg)

Entry for [make.fun's bounty](https://make.fun/bounty/u-0xkianno-one-word-first-thought-106abaf8): **One Word, First Thought**.

Deliverable: exactly one word. The program generates ~12 candidate one-word
reactions, scores them on several comedy axes (max rating among found keywords,
plus bonuses for a digit and for brevity), and runs a **10-round improvement
loop** that keeps the top 5 seeds, spawns light phrasing mutants, rescores,
and tracks the best line ever seen — with a deterministic RNG seed. Only the
champion word is written out.

Run: `python3 main.py` -> `output/entry.txt`
