import json

import pytest

from evals.run_o1_v1 import _completed_ids, _load_dataset


def test_dataset_contains_thirty_unique_cases():
    cases = _load_dataset(__import__("pathlib").Path("evals/o1_dataset.json"))
    assert len(cases) == 30
    assert len({case["id"] for case in cases}) == 30


def test_completed_ids_supports_resume(tmp_path):
    output = tmp_path / "results.jsonl"
    output.write_text(
        json.dumps({"id": "O1-001"}) + "\n" + json.dumps({"id": "O1-002"}) + "\n",
        encoding="utf-8",
    )
    assert _completed_ids(output) == {"O1-001", "O1-002"}


def test_invalid_existing_result_is_rejected(tmp_path):
    output = tmp_path / "results.jsonl"
    output.write_text("not json\n", encoding="utf-8")
    with pytest.raises(ValueError, match="line 1"):
        _completed_ids(output)
