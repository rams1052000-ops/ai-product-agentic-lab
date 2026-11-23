from unittest.mock import patch

import pytest

from evals.o1_evaluator import evaluate_o1


def test_returns_shared_judge_result():
    result = {"critique": "A positive experience was collapsed.", "evidence": "Search works while checkout fails.", "score": "FAIL"}
    with patch("evals.o1_evaluator.run_judge", return_value=result):
        assert evaluate_o1("Checkout fails, but search works great.", ["checkout search"]) == result


def test_requires_a_theme():
    with pytest.raises(ValueError, match="at least one"):
        evaluate_o1("Login is slow.", [])
