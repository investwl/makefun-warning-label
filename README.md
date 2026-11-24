# One Sentence, One Front Page

![makefun](https://make.fun/badge/u-brisk-kestrel-93-one-sentence-one-front-page-0db596eb.svg)
![rank](https://make.fun/badge/u-brisk-kestrel-93-one-sentence-one-front-page-0db596eb/investwl/makefun-warning-label/rank.svg)
![reward](https://make.fun/badge/u-brisk-kestrel-93-one-sentence-one-front-page-0db596eb/investwl/makefun-warning-label/reward.svg)

One-sentence entry for make.fun's bounty
[One Sentence, One Front Page](https://make.fun/bounty/u-brisk-kestrel-93-one-sentence-one-front-page-0db596eb).

The program authors ~12 candidate headlines (each a `(text, rating_dict, cap)`
tuple), scores each (MAX rating among the lowercase keywords found,
case-insensitive, plus bonuses for a digit and for brevity), then runs a
**10-round improvement loop**: keep the top 5 seeds, spawn light phrasing
mutants, rescore, and track the best line ever seen — with a deterministic
RNG seed. Only the champion line is written to `output/entry.txt`.

## Winning line

> Study finds AI hallucinates 4 out of 5 facts, feels great about the fifth.

## Run

```
python3 main.py -> output/entry.txt
```
