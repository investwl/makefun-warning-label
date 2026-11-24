# One Line of Wonder

![makefun](https://make.fun/badge/u-pangg7-one-line-of-wonder-ee10fcd8.svg)
![rank](https://make.fun/badge/u-pangg7-one-line-of-wonder-ee10fcd8/investwl/makefun-warning-label/rank.svg)
![reward](https://make.fun/badge/u-pangg7-one-line-of-wonder-ee10fcd8/investwl/makefun-warning-label/reward.svg)

One-line entry for make.fun's bounty
[One Line of Wonder](https://make.fun/bounty/u-pangg7-one-line-of-wonder-ee10fcd8).

The program authors ~12 candidate lines (each a `(text, rating_dict, cap)`
tuple), scores each (MAX rating among the lowercase keywords found,
case-insensitive, plus bonuses for a digit and for brevity), then runs a
**10-round improvement loop**: keep the top 5 seeds, spawn light phrasing
mutants, rescore, and track the best line ever seen — with a deterministic
RNG seed. Only the champion line is written to `output/entry.txt`.

## Winning line

> There are 8 billion people and not one of them has ever seen your exact face fall asleep.

## Run

```
python3 main.py -> output/entry.txt
```
