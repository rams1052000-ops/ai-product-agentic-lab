"""O1 judge: meaningful theme extraction. Motivated by trace 003."""

import argparse
import json
import sys
from pathlib import Path

try:
    from .llm_judge import DEFAULT_MODEL, DEFAULT_URL, run_judge
except ImportError:  # Direct execution: python evals/o1_evaluator.py
    from llm_judge import DEFAULT_MODEL, DEFAULT_URL, run_judge

O1_JUDGE_PROMPT = """
You are evaluating theme extraction for a customer-feedback analysis.

## Evaluation criterion
A good output identifies the meaningful customer themes supported by the
feedback while preserving each distinct customer experience.

## Scoring
PASS when every meaningful experience is represented, every theme is supported,
and the themes preserve the feedback's meaning. Related issues may be grouped
under one accurate broader theme.

FAIL when a meaningful experience is missed, a theme is unsupported, meaning is
changed, or unrelated experiences are collapsed so their separate meaning is
lost. Opposite sentiments about different product areas are distinct.

Judge theme extraction only. Do not judge taxonomy normalization, wording style,
urgency, priority, or whether the application supports multiple stored themes.

## Examples
### Example 1 — PASS
Input: "Audio stutters and videos keep buffering."
Output: ["Media performance"]
Result: {"critique":"The broader theme preserves both related playback problems.","evidence":"Audio stuttering and video buffering are both media-performance failures.","score":"PASS"}

### Example 2 — FAIL: meaningful experience missed
Input: "Notifications arrive late, although dark mode is excellent."
Output: ["Notification delays"]
Result: {"critique":"The output misses the distinct positive experience with dark mode.","evidence":"The feedback supports notification delays and positive dark-mode usability.","score":"FAIL"}

### Example 3 — FAIL: unsupported theme
Input: "PDF export works perfectly."
Output: ["Data loss"]
Result: {"critique":"The theme is unsupported and reverses the feedback's meaning.","evidence":"The feedback reports successful export and says nothing about lost data.","score":"FAIL"}

Now evaluate the input and output supplied by the user. Decide only from that
evidence. Write the critique before committing to the score.

Return only JSON in this exact order and shape:
{
  "critique": "one short sentence explaining why the output passes or fails",
  "evidence": "a short comparison of the feedback to the generated themes",
  "score": "PASS" or "FAIL"
}
""".strip()


def evaluate_o1(feedback, themes, *, model=DEFAULT_MODEL, url=DEFAULT_URL):
    if isinstance(themes, str):
        themes = [themes]
    if not feedback.strip() or not themes or not all(str(theme).strip() for theme in themes):
        raise ValueError("feedback and at least one non-empty generated theme are required")
    return run_judge(O1_JUDGE_PROMPT, feedback, themes, model=model, url=url)


def _load_cases(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data if isinstance(data, list) else [data]


def main():
    parser = argparse.ArgumentParser(description="Evaluate theme extraction against O1")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--cases", help="JSON file containing one case or a list of cases")
    source.add_argument("--feedback", help="customer feedback to evaluate")
    parser.add_argument("--theme", action="append", help="generated theme; repeat for multiple themes")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()
    if args.feedback and not args.theme:
        parser.error("--feedback requires at least one --theme")
    cases = _load_cases(args.cases) if args.cases else [{"id": "input", "feedback": args.feedback, "themes": args.theme}]
    exit_code = 0
    for case in cases:
        try:
            result = evaluate_o1(case["feedback"], case["themes"], model=args.model, url=args.url)
            output = {"id": case.get("id"), "criterion": "O1", **result}
            expected = case.get("expected_verdict")
            if expected is not None:
                output["expected_verdict"] = expected
                output["matches_expected"] = result["score"] == expected
                exit_code |= int(not output["matches_expected"])
            print(json.dumps(output, ensure_ascii=False))
        except (KeyError, TypeError, ValueError, RuntimeError) as exc:
            print(json.dumps({"id": case.get("id"), "criterion": "O1", "error": str(exc)}))
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
