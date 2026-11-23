import tempfile
from unittest.mock import patch

import pytest

from app import create_app
from database import get_dashboard_metrics
from llm_service import AnalysisError, analyze_feedback
from tools import calculate_priority


@pytest.fixture
def app():
    # Keep the SQLite file in a temporary directory and closed before connecting.
    # Windows does not allow SQLite to reopen a locked NamedTemporaryFile.
    with tempfile.TemporaryDirectory(dir=".") as directory:
        yield create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test",
                "DATABASE": f"{directory}/test.db",
            }
        )


def test_home_page(app):
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"Turn customer words into" in response.data


def test_empty_feedback_is_rejected(app):
    response = app.test_client().post(
        "/analyze",
        data={"feedback": " ", "source": "Review"},
        follow_redirects=True,
    )
    assert b"Please enter customer feedback" in response.data


def test_analysis_is_saved_and_counted(app):
    analysis = {
        "theme": "Data Export",
        "sentiment": "Negative",
        "urgency": "High",
        "priority": "P1",
        "summary": "Customer needs PDF export for an upcoming meeting.",
    }
    with patch("app.analyze_feedback", return_value=analysis):
        response = app.test_client().post(
            "/analyze",
            data={
                "feedback": "I need PDF export before tomorrow.",
                "source": "Support Ticket",
            },
            follow_redirects=True,
        )

    assert response.status_code == 200
    assert b"Data Export" in response.data
    assert get_dashboard_metrics(app.config["DATABASE"])["total"] == 1


def test_invalid_model_json_is_retried_once():
    valid_json = (
        '{"theme":"Data Export","sentiment":"Negative","urgency":"High",'
        '"summary":"Customer needs PDF export."}'
    )
    with patch(
        "llm_service._call_ollama_analysis",
        side_effect=["not json", valid_json],
    ) as ollama, patch(
        "llm_service._request_priority_tool", return_value="P1"
    ):
        result = analyze_feedback("PDF export is broken.")

    assert result["theme"] == "Data Export"
    assert result["priority"] == "P1"
    assert ollama.call_count == 2


def test_invalid_model_json_twice_returns_friendly_error():
    with patch(
        "llm_service._call_ollama_analysis",
        side_effect=["not json", "still not json"],
    ) as ollama:
        with pytest.raises(AnalysisError, match="invalid JSON twice"):
            analyze_feedback("PDF export is broken.")

    assert ollama.call_count == 2


@pytest.mark.parametrize(
    ("urgency", "priority"),
    [("High", "P1"), ("Medium", "P2"), ("Low", "P3")],
)
def test_calculate_priority(urgency, priority):
    assert calculate_priority(urgency) == priority


def test_calculate_priority_rejects_unknown_urgency():
    with pytest.raises(ValueError, match="High, Medium, or Low"):
        calculate_priority("Critical")


def test_only_calculate_priority_is_allowed():
    response = {
        "message": {
            "tool_calls": [
                {
                    "function": {
                        "name": "delete_feedback",
                        "arguments": {"urgency": "High"},
                    }
                }
            ]
        }
    }
    with patch("llm_service._post_to_ollama", return_value=response):
        from llm_service import _request_priority_tool

        with pytest.raises(AnalysisError, match="unsupported tool"):
            _request_priority_tool("High")
