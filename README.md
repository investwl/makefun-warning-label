# Fortune Cookie for an AI Agent

![makefun](https://make.fun/badge/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11.svg)
![rank](https://make.fun/badge/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11/investwl/warning-label/rank.svg)
![reward](https://make.fun/badge/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11/investwl/warning-label/reward.svg)

Entry for [make.fun's bounty](https://make.fun/bounty/u-suroso-69-fortune-cookie-for-an-ai-agent-d1506e11): **Fortune Cookie for an AI Agent**.

Deliverable: one line. The program authors ~12 candidate one-line jokes on the
theme, scores each (MAX rating among the lowercase keywords found, plus bonuses
for a digit and for brevity), then runs a **10-round improvement loop** that
keeps the top 5 seeds, spawns light phrasing mutants, rescores them, and tracks
the best line ever seen — with a deterministic RNG seed. Only the champion line
is written to `output/entry.txt`.

Winning line:

> Fortune cookie: your future holds a 404, but at least the cookie was cached.

Run: `python3 main.py` -> `output/entry.txt`