"""Generate resumable V1 outputs for the O1 human-labeling dataset."""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from llm_service import AnalysisError, OLLAMA_MODEL, SYSTEM_PROMPT, analyze_feedback

DEFAULT_DATASET = Path(__file__).with_name("o1_dataset.json")
DEFAULT_OUTPUT = Path(__file__).with_name("results") / "o1-v1-outputs.jsonl"


def _load_dataset(path):
    cases = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        raise ValueError("dataset must contain a JSON list")
    required = {"id", "feedback", "expected_behavior"}
    seen = set()
    for case in cases:
        if not isinstance(case, dict) or not required.issubset(case):
            raise ValueError("every case requires id, feedback, and expected_behavior")
        if case["id"] in seen:
            raise ValueError(f"duplicate case id: {case['id']}")
        if not all(isinstance(case[key], str) and case[key].strip() for key in required):
            raise ValueError(f"case {case['id']} contains an empty required field")
        seen.add(case["id"])
    return cases


def _completed_ids(path):
    if not path.exists():
        return set()
    completed = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            completed.add(json.loads(line)["id"])
        except (json.JSONDecodeError, KeyError) as exc:
            raise ValueError(f"invalid existing result on line {line_number}") from exc
    return completed


def _append_result(path, result):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(result, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def run(dataset_path, output_path, limit=None):
    cases = _load_dataset(dataset_path)
    completed = _completed_ids(output_path)
    pending = [case for case in cases if case["id"] not in completed]
    if limit is not None:
        pending = pending[:limit]

    prompt_hash = hashlib.sha256(SYSTEM_PROMPT.encode("utf-8")).hexdigest()[:12]
    print(f"Dataset: {len(cases)} cases; completed: {len(completed)}; running: {len(pending)}", flush=True)

    for position, case in enumerate(pending, 1):
        print(f"[{position}/{len(pending)}] {case['id']} generating...", flush=True)
        result = {
            **case,
            "run": {
                "product_version": "v1",
                "model": OLLAMA_MODEL,
                "prompt_sha256": prompt_hash,
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
            "v1_output": None,
            "generation_error": None,
            "human_label": None,
            "human_reason": None,
        }
        try:
            result["v1_output"] = analyze_feedback(case["feedback"])
            status = result["v1_output"]["theme"]
        except AnalysisError as exc:
            result["generation_error"] = {"type": type(exc).__name__, "message": str(exc)}
            status = f"ERROR: {exc}"
        except Exception as exc:
            result["generation_error"] = {"type": type(exc).__name__, "message": str(exc)}
            status = f"UNEXPECTED ERROR: {exc}"
        _append_result(output_path, result)
        print(f"[{case['id']}] saved — {status}", flush=True)

    print(f"Results: {output_path}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Generate V1 outputs for the O1 dataset")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int, help="run only this many pending cases")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1")
    try:
        run(args.dataset, args.output, args.limit)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")


if __name__ == "__main__":
    main()
