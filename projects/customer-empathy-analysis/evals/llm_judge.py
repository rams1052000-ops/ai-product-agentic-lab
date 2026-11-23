"""Shared Ollama runner for focused LLM-as-a-Judge evaluators."""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "qwen3.5:latest"


def _post_json(url, payload):
    request = Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"Judge model is unavailable at {url}: {exc}") from exc


def run_judge(prompt, judge_input, candidate_output, *, model=DEFAULT_MODEL, url=DEFAULT_URL):
    """Run one focused judge and validate its critique-first binary result."""
    task = json.dumps({"input": judge_input, "output": candidate_output}, ensure_ascii=False)
    response = _post_json(url, {
        "model": model,
        "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": task}],
        "format": "json", "stream": False, "think": False,
        "options": {"temperature": 0},
    })
    try:
        result = json.loads(response["message"]["content"])
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Judge returned an invalid response") from exc
    if list(result) != ["critique", "evidence", "score"]:
        raise RuntimeError("Judge result must contain critique, evidence, then score in that order")
    if result["score"] not in {"PASS", "FAIL"}:
        raise RuntimeError("Judge score must be PASS or FAIL")
    if not all(isinstance(result[key], str) and result[key].strip() for key in ("critique", "evidence")):
        raise RuntimeError("Judge critique and evidence must be non-empty strings")
    return result
