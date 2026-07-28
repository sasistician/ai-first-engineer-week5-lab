# Week 5 Lab Guide — Orchestration: Build a Supervised Squad on EVBot

**Time budget:** ~35–40 min within the 90-min live session, plus ~5 min
pre-class setup (no new model downloads — this lab runs inside EVBot's
existing Ollama/`uv` environment).

**Prerequisite:** Today's deck covered orchestration patterns, guardrails, and
evaluation — including the fan-out/barrier/synthesize shape a squad of
subagents can run. This lab makes that pattern real: five subagent
definitions extend EVBot (Week 3) into a supervised system, directed
interactively through Claude Code — no new orchestration code, the durable
agent definitions plus the right prompt **are** the artifact.

This lab is deliberately **not** a rewrite of EVBot — this repo sits as a
sibling to `week3-lab/` and only adds new artifacts (subagent definitions,
an eval dataset, a threshold config). Your existing EVBot install keeps
working exactly as it did in Week 3.

**Note on this standalone copy:** this repo was cloned out of the course
monorepo, where it's called `week5-lab-repo`. It's the same content; every
path below assumes it's checked out next to `week3-lab/` as
`ai-first-engineer-week5-lab/` (the default folder name `git clone` gives
it) — adjust the paths if you renamed the folder.

---

## 1. Setup

1. Clone [EVBot (Week 3)](https://github.com/sasistician/evbot-week3-lab) as
   a sibling directory if you haven't already, then run this repo's
   onboarding script from inside it:

   macOS/Linux:
   ```
   ./setup.sh
   ```
   Windows: run this from [Git Bash](https://git-scm.com/download/win) or
   WSL, same as Week 3:
   ```
   bash setup.sh
   ```
2. `setup.sh` confirms `../week3-lab` is already set up, and that `claude`
   and `uv` are on your PATH — it prints the exact command to run if
   anything's missing.
3. Generate a real answers log to work against:
   ```
   cd ../week3-lab
   uv run python ../ai-first-engineer-week5-lab/eval/run_batch.py
   ```
   This asks the real, running EVBot every question in the seed eval set and
   logs its actual answers to `eval/answers_log.json` — the workers below
   grade what EVBot really said, not hypothetical text.

---

## 2. Quick-reference card

| Worker | Definition | Role |
|---|---|---|
| Scenario Generator | `.claude/agents/scenario-generator.md` | Expands the eval set with new grounded Q&A pairs |
| Accuracy Grader | `.claude/agents/accuracy-grader.md` | Scores EVBot's logged answers on Accuracy/Completeness/Clarity |
| Groundedness Checker | `.claude/agents/groundedness-checker.md` | Verifies every claim traces back to a real source doc |
| Regression Test-Runner | `.claude/agents/regression-test-runner.md` | Runs EVBot's existing pytest suite |
| Assessment Synthesizer | `.claude/agents/assessment-synthesizer.md` | Barrier step — combines the other three into one scorecard against `eval/threshold.json` |

---

## 3. The exercise

### Step 1 — Read the five subagent definitions

Open each file in `.claude/agents/`. They're short. Find, for each one: what
its one job is, what it reads, what it's explicitly told *not* to do.

**Checkpoint:** Name which two workers have the narrowest, most easily
confused jobs (hint: Accuracy vs. Groundedness), and in your own words, what
distinguishes them. If you can't tell them apart, re-read both files.

### Step 2 — Fan out three workers in parallel

In a Claude Code session started from inside this repo, ask it to run
the Accuracy Grader, Groundedness Checker, and Regression Test-Runner
subagents **at the same time**, phrased explicitly as independent parallel
work — for example:

*"Launch the accuracy-grader, groundedness-checker, and regression-test-runner
subagents in parallel — they don't depend on each other's output. Report back
when all three have written their result files."*

**Checkpoint:** Confirm all three result files exist:
`eval/results/accuracy_grades.json`, `eval/results/groundedness_report.json`,
`eval/results/test_results.json`. This is today's deck's fan-out step, run
for real.

### Step 3 — Synthesize the scorecard (the barrier)

Once all three files exist, ask Claude Code to launch the
`assessment-synthesizer` subagent:

*"Now launch the assessment-synthesizer subagent to combine all three worker
results into one scorecard."*

**Checkpoint:** Open `eval/results/scorecard.json`. Confirm it has a
`verdict` of `PASS` or `FAIL`, and that every threshold from
`eval/threshold.json` is accounted for in the computed numbers.

### Step 4 — Read the verdict like a gatekeeper would

If the verdict is `FAIL`, read `failed_thresholds` — it should name the
specific number that missed, not just say "failed."

**Checkpoint:** Explain out loud (or to a partner) what you'd have to fix
before this system could ship, based only on what the scorecard tells you —
not by re-reading EVBot's code.

### Step 5 — Grow the eval set

Ask Claude Code to launch the `scenario-generator` subagent to add 8-10 new
Q&A pairs grounded in `../week3-lab/data/ev_docs/`.

**Checkpoint:** Confirm `eval/qa_generated.json` now exists, that
`eval/qa_seed_set.json` is untouched, and spot-check two new pairs against
their cited `source_doc` — is the `reference_answer` actually supported by
that file?

### Step 6 — Self-audit against today's guardrail checklist

Open today's deck to the production-readiness checklist (Part 3). Go through
it against the squad you just ran, not a hypothetical one.

**Checkpoint:** Name one item on the checklist your squad's current design
would fail if this were a real production launch gate (for example: no
approval-gate step for a human to review a `FAIL` verdict before anyone acts
on it). You don't have to fix it — noticing it is the point.

---

## 4. Reflection prompts

1. The Assessment Synthesizer was explicitly told not to re-grade or
   re-check anything itself. Why does that restriction matter more here than
   it would for a single do-everything agent?
2. If the Scenario Generator and Accuracy Grader ran in the same context
   window instead of as separate subagents, what specific failure mode from
   today's deck (Part 1) becomes more likely?
3. Compare this squad's gate to the real story from today's deck — several
   hundred grounded Q&A pairs, hybrid LLM-judge-plus-human grading, no ship
   without clearing it. What's the smallest change that would make this
   lab's five-worker squad closer to that real bar?
4. Your capstone won't be about EV Q&A. Which of today's five roles maps
   cleanly onto your own project, and which one doesn't exist yet because
   your system's actual risk is different?

---

## 5. APPLY — your reps this week

- From today's deck, Part "Apply": run the production-readiness checklist
  against your own capstone idea, using the answers you drafted there.
- Using Claude Code with this squad available, direct it to lower
  `max_ungrounded_claim_rate` in `eval/threshold.json` to `0.0` and re-run
  Steps 2-3. Does the scorecard still pass? If not, is that a real problem
  with EVBot, or a threshold that's stricter than the system needs to be?
- Optional stretch: sketch (doesn't need to run) what your own capstone's
  worker roster would look like — which tasks are genuinely independent,
  what your gate's thresholds would check, and who or what plays the
  Synthesizer's role.

Bring your capstone worker roster to the showcase prep session.

---

## Look ahead

This is the last FRAME of the course. What's next is the capstone: combine
your Skill (Week 3), your MCP server (Week 4), and this week's orchestration,
guardrails, and evaluation pattern into one working system that solves a real
problem from your own job — then defend it live to earn "Claude Code
Builder."
