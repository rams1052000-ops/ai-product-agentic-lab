import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from tools import calculate_priority

VALID_SENTIMENTS = {"Positive", "Neutral", "Negative", "Mixed"}
VALID_URGENCIES = {"Low", "Medium", "High"}
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen3.5:latest"
ALLOWED_TOOL = "calculate_priority"

SYSTEM_PROMPT = """
Analyze the customer feedback below.

Return only valid JSON with exactly this structure:
{
  "theme": "",
  "sentiment": "",
  "urgency": "",
  "summary": ""
}

Rules:
- theme: a short, reusable product theme (2-4 words)
- sentiment: exactly Positive, Neutral, Negative, or Mixed
- urgency: exactly High, Medium, or Low
- summary: one concise sentence, no more than 25 words
- judge urgency from customer impact and time sensitivity
- do not invent facts
- do not include markdown, commentary, or reasoning outside the JSON
""".strip()


class AnalysisError(Exception):
    """A safe, user-facing error produced by the analysis boundary."""


def _validate_analysis(data):
    required = {"theme", "sentiment", "urgency", "summary"}
    if not isinstance(data, dict) or not required.issubset(data):
        raise AnalysisError("The AI returned an incomplete analysis. Try again.")

    cleaned = {
        key: str(data[key]).strip()
        for key in ("theme", "sentiment", "urgency", "summary")
    }
    if not all(cleaned.values()):
        raise AnalysisError("The AI returned an incomplete analysis. Try again.")
    if cleaned["sentiment"] not in VALID_SENTIMENTS:
        raise AnalysisError("The AI returned an invalid sentiment. Try again.")
    if cleaned["urgency"] not in VALID_URGENCIES:
        raise AnalysisError("The AI returned an invalid urgency. Try again.")
    if len(cleaned["theme"]) > 60 or len(cleaned["summary"]) > 240:
        raise AnalysisError("The AI response was too long. Try again.")

    return cleaned


def _post_to_ollama(payload):
    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise AnalysisError(
            "Ollama is unavailable. Make sure Ollama is running and try again."
        ) from exc
    except (json.JSONDecodeError, TypeError) as exc:
        raise AnalysisError(
            "Ollama returned an unexpected response. Please try again."
        ) from exc


def _call_ollama_analysis(feedback):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": feedback},
        ],
        "format": "json",
        "stream": False,
        "think": False,
        "options": {"temperature": 0},
    }
    try:
        return _post_to_ollama(payload)["message"]["content"]
    except (KeyError, TypeError) as exc:
        raise AnalysisError(
            "Ollama returned an unexpected response. Please try again."
        ) from exc



def _request_priority_tool(urgency):
    tool_definition = {
        "type": "function",
        "function": {
            "name": ALLOWED_TOOL,
            "description": (
                "Convert an urgency classification into a business priority. "
                "You must call this tool and must not calculate priority yourself."
            ),
            "parameters": {
                "type": "object",
                "required": ["urgency"],
                "properties": {
                    "urgency": {
                        "type": "string",
                        "enum": ["High", "Medium", "Low"],
                    }
                },
            },
        },
    }
    result = _post_to_ollama(
        {
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Request the provided calculate_priority tool exactly "
                        "once. Do not calculate or state a priority yourself."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"The feedback urgency was classified as {urgency}. "
                        "Request the tool now."
                    ),
                },
            ],
            "tools": [tool_definition],
            "stream": False,
            "think": False,
            "options": {"temperature": 0},
        }
    )

    try:
        tool_calls = result["message"]["tool_calls"]
        if len(tool_calls) != 1:
            raise AnalysisError(
                "The AI did not request the priority tool correctly. Try again."
            )
        function = tool_calls[0]["function"]
        if function["name"] != ALLOWED_TOOL:
            raise AnalysisError("The AI requested an unsupported tool.")
        arguments = function["arguments"]
        if set(arguments) != {"urgency"} or arguments["urgency"] != urgency:
            raise AnalysisError(
                "The AI requested the priority tool with invalid input."
            )
        return calculate_priority(arguments["urgency"])
    except AnalysisError:
        raise
    except (KeyError, TypeError) as exc:
        raise AnalysisError(
            "The AI did not request the priority tool correctly. Try again."
        ) from exc


def analyze_feedback(feedback):
    # Retry exactly once when the model output itself is not valid JSON.
    for attempt in range(2):
        content = _call_ollama_analysis(feedback)
        try:
            analysis = _validate_analysis(json.loads(content))
            analysis["priority"] = _request_priority_tool(analysis["urgency"])
            return analysis
        except json.JSONDecodeError:
            if attempt == 1:
                raise AnalysisError(
                    "The local AI returned invalid JSON twice. Please try again."
                )

    raise AnalysisError("The local AI could not analyze this feedback.")
