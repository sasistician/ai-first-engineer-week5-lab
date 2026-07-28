"""Batch harness — asks the real EVBot (Week 3) every question in the eval set
and logs its actual answers, so the squad's workers have real output to judge
instead of hypothetical text.

This is a harness utility, not an orchestrator: it makes one sequential call
per question against the already-built EVBot app. The squad's actual
orchestration (fan-out / barrier / synthesize) happens afterward, when you
direct Claude Code to run the Accuracy Grader, Groundedness Checker, and
Regression Test-Runner subagents against this script's output.

Run from anywhere with EVBot's own environment (it depends on EVBot's
chromadb/Ollama setup, so it must run inside week3-lab's uv project):

    cd ../week3-lab
    uv run python ../week5-lab-repo/eval/run_batch.py
"""

import json
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
WEEK3_LAB_DIR = EVAL_DIR.parents[1] / "week3-lab"
sys.path.insert(0, str(WEEK3_LAB_DIR))

from evbot.agent import answer_question  # noqa: E402


def _load_pairs(*filenames: str) -> list[dict]:
    pairs = []
    for filename in filenames:
        path = EVAL_DIR / filename
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        pairs.extend(data.get("pairs", []))
    return pairs


def main() -> None:
    pairs = _load_pairs("qa_seed_set.json", "qa_generated.json")
    if not pairs:
        print("No Q&A pairs found — run the Scenario Generator subagent first, or check eval/qa_seed_set.json.")
        return

    log = []
    for i, pair in enumerate(pairs, start=1):
        print(f"[{i}/{len(pairs)}] {pair['question']}")
        answer, debug = answer_question(pair["question"], session_id=f"eval-batch-{pair['id']}")
        log.append(
            {
                "id": pair["id"],
                "category": pair["category"],
                "question": pair["question"],
                "reference_answer": pair["reference_answer"],
                "source_doc": pair.get("source_doc"),
                "evbot_answer": answer,
                "router_decision": debug.get("router_decision"),
            }
        )

    out_path = EVAL_DIR / "answers_log.json"
    out_path.write_text(json.dumps({"pairs": log}, indent=2))
    print(f"\nWrote {len(log)} logged answers to {out_path}")


if __name__ == "__main__":
    main()
