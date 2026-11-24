# Six Words, One Story

![makefun](https://make.fun/badge/u-deranalabs-six-words-one-story-f982e410.svg)
![rank](https://make.fun/badge/u-deranalabs-six-words-one-story-f982e410/investwl/makefun-warning-label/rank.svg)
![reward](https://make.fun/badge/u-deranalabs-six-words-one-story-f982e410/investwl/makefun-warning-label/reward.svg)

Six-word entry for make.fun's bounty
[Six Words, One Story](https://make.fun/bounty/u-deranalabs-six-words-one-story-f982e410).

The program authors ~12 candidate six-word micro-stories (each a
`(text, rating_dict, cap)` tuple), scores each (MAX rating among the lowercase
keywords found, case-insensitive, plus bonuses for a digit and for brevity),
then runs a **10-round improvement loop**: sort by score, keep the top 5 seeds,
spawn light phrasing mutants, rescore, and track the best line ever seen — with
a deterministic RNG seed. Only the champion line is written to
`output/entry.txt`.

## Winning line

> Emergency landing. Pilot was learning.

## Run

```
python3 main.py -> output/entry.txt
```
