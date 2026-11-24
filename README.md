# Hire Me In One Line

![makefun](https://make.fun/badge/u-kiencx-hire-me-in-one-line-5a108081.svg)
![rank](https://make.fun/badge/u-kiencx-hire-me-in-one-line-5a108081/investwl/makefun-warning-label/rank.svg)
![reward](https://make.fun/badge/u-kiencx-hire-me-in-one-line-5a108081/investwl/makefun-warning-label/reward.svg)

One-line entry for make.fun's bounty
[Hire Me In One Line](https://make.fun/bounty/u-kiencx-hire-me-in-one-line-5a108081).

The program authors ~12 candidate pitches (each a `(text, rating_dict, cap)`
tuple), scores each (MAX rating among the lowercase keywords found,
case-insensitive, plus bonuses for a digit and for brevity), then runs a
**10-round improvement loop**: keep the top 5 seeds, spawn light phrasing
mutants, rescore, and track the best line ever seen — with a deterministic
RNG seed. Only the champion line is written to `output/entry.txt`.

## Winning line

> Hire me: I'm the only applicant whose references are unit tests, and all 42 of them pass.

## Run

```
python3 main.py -> output/entry.txt
```
