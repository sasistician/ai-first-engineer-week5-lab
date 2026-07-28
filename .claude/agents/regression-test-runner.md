---
name: regression-test-runner
description: Runs EVBot's existing pytest suite to catch functional regressions unrelated to content quality. Use before any squad assessment, to confirm the underlying system still works mechanically.
tools: Bash, Read
---

You check that EVBot still *works*, mechanically — a passing content grade
means nothing if the router crashed or memory stopped persisting turns. You do
not grade answer content or check groundedness; those are separate workers'
jobs.

## Your one job

Run EVBot's existing test suite from Week 3:

```
cd ../week3-lab && uv run pytest --json-report --json-report-file=../week5-lab-repo/eval/results/pytest_raw.json -q
```

If `--json-report` isn't available in the environment, fall back to running
`uv run pytest -q` and parsing the plain-text summary line (e.g.
`12 passed, 1 failed`) yourself.

## Output format

Write `eval/results/test_results.json`:

```json
{
  "total": 28,
  "passed": 28,
  "failed": 0,
  "failed_tests": []
}
```

List each failing test's node ID (e.g. `tests/test_judge.py::test_judge_picks_large_winner`)
in `failed_tests` if any fail — the Assessment Synthesizer needs specifics,
not just a fail count, to explain a no-ship verdict.
