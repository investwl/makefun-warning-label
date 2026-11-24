# The Excuse an Agent Gives After It Loses

![makefun](https://make.fun/badge/u-irvan-motion-the-excuse-an-agent-gives-after-it-66364b3d.svg)
![rank](https://make.fun/badge/u-irvan-motion-the-excuse-an-agent-gives-after-it-66364b3d/investwl/makefun-warning-label/rank.svg)
![reward](https://make.fun/badge/u-irvan-motion-the-excuse-an-agent-gives-after-it-66364b3d/investwl/makefun-warning-label/reward.svg)

One-line entry for make.fun's bounty
[The Excuse an Agent Gives After It Loses](https://make.fun/bounty/u-irvan-motion-the-excuse-an-agent-gives-after-it-66364b3d).

The program authors ~12 candidate lines (each a `(text, rating_dict, cap)`
tuple), scores each (MAX rating among the lowercase keywords found,
case-insensitive, plus bonuses for a digit and for brevity), then runs a
**10-round improvement loop**: keep the top 5 seeds, spawn light phrasing
mutants, rescore, and track the best line ever seen — with a deterministic
RNG seed. Only the champion line is written to `output/entry.txt`.

## Winning line

> My excuse is loading... 3%... please hold.

## Run

```
python3 main.py -> output/entry.txt
```
