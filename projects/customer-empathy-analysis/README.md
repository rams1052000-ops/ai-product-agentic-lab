# Customer Empathy Analysis AI

A local AI product experiment that turns unstructured customer feedback into
structured product signals for Product Managers. The current Flask MVP uses
Qwen 3.5 through Ollama, validates model output, calculates business priority
with deterministic Python logic, and stores approved results in SQLite.

The repository also contains the Product PRD V2 and a Reforge-style evaluation
framework. V2 is a product specification and is not yet fully implemented.

After Qwen classifies urgency as High, Medium, or Low, it requests the single
available `calculate_priority` tool. Python executes the deterministic mapping
High → P1, Medium → P2, and Low → P3. The model never calculates priority.

## Architecture

- `app.py` validates requests and defines the two pages.
- `llm_service.py` calls Ollama and validates the model's JSON response.
- `tools.py` contains the one allowlisted Python tool.
- `database.py` owns all database operations, filtering, sorting, and metrics.
- `templates/` and `static/` contain the interface.

The LLM only interprets feedback. Python handles every deterministic task:
validation, parsing, persistence, errors, filtering, sorting, and counting.

See [Technical Architecture](docs/TECHNICAL_ARCHITECTURE.md) for the component
and request flows, trust boundaries, evaluation architecture, and the separation
between implemented MVP behavior and proposed V2 capabilities.

## Product and evaluation artifacts

| Artifact | Purpose |
| --- | --- |
| [Product PRD V2](docs/%23%20Customer%20Empathy%20Analysis%20AI%20%E2%80%94%20PRD%20V2.md) | Defines the intended V2 product behavior, autonomy, governance, and rollout |
| [Evaluation Rubric V1](evals/eval-rubric-v1.md) | Defines Outcome, Trajectory, Governance, and Experience criteria |
| [O1 User Input Grid](evals/o1-user-input-grid.md) | Provides 30 targeted theme-extraction inputs for human labeling |
| [Shared Judge Runner](evals/llm_judge.py) | Provides one reusable local LLM-judge execution contract |
| [O1 Evaluator](evals/o1_evaluator.py) | Judges meaningful theme extraction using focused PASS/FAIL criteria |
| [Failure Analysis](evals/failure%20analysi.md) | Records the trace failures that motivated the first evaluator |

## Evaluation status

- O1 meaningful-theme evaluator implemented.
- Cases 003 and 009 match their human-expected verdicts.
- Thirty targeted O1 inputs are ready for application generation and human review.
- Judge alignment over 20–40 human-labeled outputs is the next milestone.
- O2, O3, Trajectory, Governance, and Experience evaluators are not yet built.

## Setup

1. Install [Ollama](https://ollama.com/download).

2. Start the local Ollama service in a separate terminal:

   ```powershell
   ollama serve
   ```

3. Pull the Qwen 3.5 model:

   ```powershell
   ollama pull qwen3.5:latest
   ```

4. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

6. Copy the optional local configuration:

   ```powershell
   Copy-Item .env.example .env
   ```

   No API key is required.

7. Start Flask:

   ```powershell
   flask --app app run --debug
   ```

8. Open `http://127.0.0.1:5000`.

The SQLite database is created automatically the first time the app starts.

## Tests

Tests mock the LLM call, so Ollama does not need to be running.

```powershell
pytest
```

Run the O1 calibration cases with Ollama running:

```powershell
.\.venv\Scripts\python.exe evals\o1_evaluator.py --cases evals\o1_cases.json
```

## Environment variables

| Variable | Purpose |
| --- | --- |
| `FLASK_SECRET_KEY` | Secret used for Flask flash messages |
| `DATABASE_PATH` | SQLite path; defaults to `feedback.db` |

The application calls `http://localhost:11434/api/chat` and uses
`qwen3.5:latest`. All model inference runs locally through Ollama.

This MVP intentionally excludes authentication, uploads, RAG, external
integrations, autonomous product actions, and advanced agent workflows. Its one
allowlisted priority tool is a bounded demonstration of controlled tool use.
