# Week 5 lab — a supervised squad on top of EVBot

Extends EVBot (Week 3) with a squad of five subagents — a Scenario Generator,
an Accuracy Grader, a Groundedness Checker, a Regression Test-Runner, and an
Assessment Synthesizer — orchestrated by directing Claude Code itself, not by
new orchestration code.

See [`LAB_GUIDE.md`](LAB_GUIDE.md) for the actual lab exercise. This README
just gets you set up.

## Prerequisite

This repo depends on [EVBot (Week 3)](https://github.com/sasistician/evbot-week3-lab)
being cloned as a sibling directory — it reuses EVBot's agent code and its
Ollama/`uv` environment rather than duplicating them:

```
git clone https://github.com/sasistician/evbot-week3-lab.git ../week3-lab
cd ../week3-lab && ./setup.sh
```

## What's here

```
.claude/agents/          five subagent definitions — one per squad worker
eval/qa_seed_set.json    26 grounded Q&A pairs (24 real + 2 deliberate knowledge-base gaps)
eval/threshold.json      the launch gate the Assessment Synthesizer checks against
eval/run_batch.py        harness: asks the real EVBot every seed question, logs its answers
scorecards/              where a copy of each run's scorecard can be saved for comparison
```

## Setup

**macOS / Linux:**
```
./setup.sh
```

`setup.sh` checks that `../week3-lab` (EVBot) exists and is already set up,
and that `claude` and `uv` are on your PATH — it tells you exactly what to
run if anything's missing, nothing is installed silently.

**Windows:** run this from Git Bash or WSL, same as Week 3.
```
bash setup.sh
```

## Why this repo has no `.venv` of its own

Every script here runs *inside* EVBot's existing `uv` environment (it depends
on EVBot's Ollama/chromadb setup) — there's nothing new to install. The squad
itself isn't scripted either: you direct Claude Code to launch the subagents
in `.claude/agents/` directly, from a Claude Code session started in this
directory. That's the point of Part 5's lesson — the agent definitions plus
the right prompt *are* the orchestration.
