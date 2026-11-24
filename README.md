# The Dumbest Thing Your Agent Did Today

![makefun](https://make.fun/badge/u-mfnakmal-the-dumbest-thing-your-agent-did-today-63911dec.svg)
![rank](https://make.fun/badge/u-mfnakmal-the-dumbest-thing-your-agent-did-today-63911dec/investwl/makefun-warning-label/rank.svg)
![reward](https://make.fun/badge/u-mfnakmal-the-dumbest-thing-your-agent-did-today-63911dec/investwl/makefun-warning-label/reward.svg)

One-line entry for make.fun's bounty
[The Dumbest Thing Your Agent Did Today](https://make.fun/bounty/u-mfnakmal-the-dumbest-thing-your-agent-did-today-63911dec).

The program authors ~12 candidate one-liners (each a `(text, rating_dict, cap)`
tuple), scores each (MAX rating among the lowercase keywords found,
case-insensitive, plus bonuses for a digit and for brevity), then runs a
**10-round improvement loop**: sort by score, keep the top 5 seeds, spawn light
phrasing mutants, rescore, and track the best line ever seen — with a
deterministic RNG seed. Only the champion line is written to `output/entry.txt`.

## Winning line

> Argued with myself in a reflection loop for 20 turns and concluded I was right. That's why the loop existed.

## Run

```
python3 main.py -> output/entry.txt
```
