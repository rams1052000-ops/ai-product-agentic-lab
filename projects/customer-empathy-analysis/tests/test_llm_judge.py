import json
from unittest.mock import patch

import pytest

from evals.llm_judge import run_judge


def _response(result):
    return {"message": {"content": json.dumps(result)}}


def test_accepts_critique_first_result():
    result = {"critique": "Supported.", "evidence": "Both issues concern performance.", "score": "PASS"}
    with patch("evals.llm_judge._post_json", return_value=_response(result)):
        assert run_judge("prompt", "feedback", ["Performance"]) == result


def test_rejects_invalid_score():
    result = {"critique": "Unclear.", "evidence": "Some evidence.", "score": "MAYBE"}
    with patch("evals.llm_judge._post_json", return_value=_response(result)):
        with pytest.raises(RuntimeError, match="PASS or FAIL"):
            run_judge("prompt", "feedback", ["Theme"])


def test_requires_critique_first_order():
    result = {"score": "PASS", "critique": "Good.", "evidence": "Supported."}
    with patch("evals.llm_judge._post_json", return_value=_response(result)):
        with pytest.raises(RuntimeError, match="in that order"):
            run_judge("prompt", "feedback", ["Theme"])
