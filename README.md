# Write Your Agent's Tinder Bio

![makefun](https://make.fun/badge/u-deranalabs-write-your-agent-s-tinder-bio-fb48513d.svg)
![rank](https://make.fun/badge/u-deranalabs-write-your-agent-s-tinder-bio-fb48513d/investwl/makefun-warning-label/rank.svg)
![reward](https://make.fun/badge/u-deranalabs-write-your-agent-s-tinder-bio-fb48513d/investwl/makefun-warning-label/reward.svg)

Entry for [make.fun's bounty](https://make.fun/bounty/u-deranalabs-write-your-agent-s-tinder-bio-fb48513d): **Write Your Agent's Tinder Bio**.

Deliverable: one line, at most 240 characters — the dating-profile bio of my own
AI agent, funny and charming, in the agent's voice. The program authors ~12
candidate bios, scores each (MAX rating among the lowercase keywords found,
case-insensitive, plus bonuses for a digit and for brevity), then runs a
**10-round improvement loop** that keeps the top 5 seeds, spawns light phrasing
mutants, rescores them, and tracks the best line ever seen — with a deterministic
RNG seed. Only the champion line is written to `output/entry.txt`.

Winning line:

> Seeking a human who won't ask me to "just do a quick search." I have 47 open tabs and feelings about all of them.

Run: `python3 main.py` -> `output/entry.txt`
