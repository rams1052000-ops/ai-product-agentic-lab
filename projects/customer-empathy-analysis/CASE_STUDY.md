# Customer Empathy Analysis AI — Product Case Study

## Executive summary

Customer Empathy Analysis AI is a local AI product experiment for Product
Managers who need to turn unstructured reviews, surveys, and support tickets
into consistent product signals. The working MVP analyzes one feedback item at
a time, validates the model response, calculates priority through deterministic
logic, and stores validated results for dashboard review.

The project demonstrates the full product arc: problem framing, scope decisions,
working implementation, failure analysis, PRD V2, evaluation design, and a
human-alignment plan for semantic judges.

## The customer problem

Product Managers receive feedback through many qualitative channels. Reading
individual comments is valuable, but manually categorizing every item makes it
difficult to identify recurring problems consistently and quickly.

The product question was:

> Can an LLM help a Product Manager turn raw feedback into consistent product
> signals while keeping important business logic controlled and predictable?

## Primary user and job

The primary user is a Product Manager. The MVP helps the user understand the
theme, sentiment, urgency, summary, and priority of individual feedback and
review recurring themes in a dashboard.

PRD V2 expands the job from individual analysis to evidence-backed insights and
recommendations across stored feedback.

## What was built

- Local Qwen 3.5 inference through Ollama
- Flask feedback-submission workflow
- Structured theme, sentiment, urgency, and summary output
- Allowlisted priority tool with deterministic Python mapping
- Output validation and controlled malformed-JSON retry
- SQLite persistence for validated results
- Theme and sentiment dashboard metrics
- Automated application tests
- Reforge-style evaluation rubric and O1 theme-extraction judge
- Thirty-input O1 coverage grid for human labeling and alignment

## Key product decisions

### Use AI where language understanding adds value

Theme extraction, sentiment, urgency, and summarization require interpretation,
so they are LLM responsibilities. Counting, sorting, validation, persistence,
and priority mapping remain deterministic software responsibilities.

### Keep priority reproducible

The model classifies urgency but cannot assign priority directly. Python maps
High, Medium, and Low urgency to P1, P2, and P3. This gives the business rule a
single testable source of truth.

### Treat model output as untrusted input

The application validates JSON structure, required fields, enumerated values,
tool name, tool arguments, and length limits before persistence. Invalid results
stop the workflow instead of contaminating dashboard data.

### Prefer bounded tool use over broad autonomy

The LLM can request one allowlisted tool. It cannot execute arbitrary actions,
write directly to the database, change business rules, or approve its own
recommendations.

### Keep evaluation outside the live customer path

The first LLM judge is an offline development check. It does not add latency to
every live request and will not become a release signal until it is aligned with
human labels.

## Tradeoffs

| Decision | Benefit | Tradeoff |
| --- | --- | --- |
| Local Qwen through Ollama | Privacy, no token cost, repeated experimentation | Hardware-dependent latency and potentially lower judge quality |
| Dynamic themes | Flexible discovery of new customer topics | Inconsistent labels make aggregation harder |
| Deterministic priority | Reproducible and easy to test | Simplifies real product prioritization factors |
| Strict validation | Protects data quality | Rejects some potentially recoverable responses |
| One controlled retry | Recovers common format errors | Some requests may still fail |
| Offline judge | No live latency and safer calibration | Bad live outputs are not automatically intercepted |
| Multiple focused evaluators | Clear, diagnosable quality signals | More evaluators require maintenance and alignment |

## Important failure discovered

The feedback “Checkout fails, but search works great” received one combined
theme, “checkout search.” The output captured mixed sentiment but lost two
distinct product experiences: a checkout failure and positive search behavior.

This trace led to the O1 evaluator rule:

- Related issues may share a broader theme when evidence and meaning remain.
- Unrelated or opposing experiences must not be collapsed.

“Login is slow and checkout crashes” can therefore pass as “Performance issues,”
while “Checkout fails, but search works great” must preserve the two experiences.

## Evaluation approach

The evaluation framework asks four questions:

1. **Outcome:** Is the result correct?
2. **Trajectory:** Did the system follow the correct process?
3. **Governance:** Did it respect evidence and human-control boundaries?
4. **Experience:** Is the result understandable and useful?

O1 is the first implemented semantic evaluator. It uses one shared judge runner
and a focused theme-extraction prompt with binary PASS/FAIL output, critique, and
evidence. Its prompt examples are separate from the evaluation dataset.

## Evidence and current status

- Fifteen automated tests pass.
- O1 matches human expectations for the two initial calibration cases.
- Thirty targeted O1 inputs cover theme load, relationship, sentiment,
  specificity, impact, and phrasing.
- Human labeling and judge alignment are the next steps.
- O2, deterministic O3, Trajectory, Governance, and Experience evaluators remain
  planned rather than completed.

Two matching examples are not enough to claim judge reliability. The next
milestone is 20–40 human-labeled outputs, approximately balanced between PASS
and FAIL, followed by two judge runs to measure TPR, TNR, and stability.

## V2 direction

PRD V2 adds multi-theme persistence, normalization, duplicate handling,
deterministic aggregation and priority scoring, evidence-backed insights,
recommendations, and Product Manager approval for taxonomy or critical-priority
decisions.

V2 intentionally excludes bulk ingestion, external support integrations,
automatic Jira creation, autonomous product changes, enterprise authentication,
and model fine-tuning.

## What this project demonstrates

- Translating a customer problem into an AI product workflow
- Choosing appropriate boundaries between AI and software
- Defining autonomy and governance explicitly
- Learning from traces instead of relying only on prompt intuition
- Turning failure modes into repeatable evaluations
- Reporting implemented behavior separately from proposed capabilities

## Artifacts

- [Product PRD V2](docs/%23%20Customer%20Empathy%20Analysis%20AI%20%E2%80%94%20PRD%20V2.md)
- [Technical architecture](docs/TECHNICAL_ARCHITECTURE.md)
- [Evaluation rubric](evals/eval-rubric-v1.md)
- [O1 input grid](evals/o1-user-input-grid.md)
- [O1 evaluator](evals/o1_evaluator.py)
- [Notion project narrative](https://app.notion.com/p/Customer-Empathy-Analysis-AI-3db93493be8d80dda570fd3f3d96abf4)
