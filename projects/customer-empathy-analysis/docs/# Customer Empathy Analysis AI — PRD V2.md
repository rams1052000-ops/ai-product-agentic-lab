# Customer Empathy Analysis AI — PRD V2

**Version:** 2.0  
**Status:** Draft for approval  
**Date:** November 22, 2026  
**Existing product:** Customer Feedback Analyzer  
**Implementation:** Local Qwen 3.5, Ollama, Python, Flask, SQLite

---

## 1. Product

Customer Empathy Analysis AI helps Product Managers turn unstructured customer reviews, surveys, and support tickets into actionable product intelligence. V2 extends the existing single-feedback analyzer to extract multiple themes, assess customer impact, aggregate patterns across stored reviews, calculate deterministic priorities, and generate evidence-backed insights and recommendations. The system supports product decision-making while keeping AI-generated recommendations advisory and important taxonomy changes under human control.

## 2. User and Channel

**Primary user:** Product Manager.

**Secondary users:** Product Operations, Customer Insights, and Support Leads.

**Channel:** Local Flask web application.

Users submit one feedback item at a time and review results through a dashboard. Previously analyzed feedback is stored in SQLite and used to generate aggregated insights.

**Definition of success:** A PM can understand recurring customer problems, identify high-impact issues, and evaluate evidence-backed recommendations without manually categorizing and summarizing every review.

Success will be measured through classification accuracy, deterministic correctness, insight usefulness, and time required to complete the analysis workflow.

## 3. Jobs to Be Done

The product should support these user requests:

| Job | Example user request |
|---|---|
| Understand feedback | "What issues is this customer describing?" |
| Identify recurring problems | "What are customers complaining about most?" |
| Understand sentiment | "How do customers feel about checkout?" |
| Prioritize problems | "Which issues should I investigate first?" |
| Identify opportunities | "Based on customer feedback, what improvements should we consider?" |

The product must also handle ambiguous, mixed-sentiment, multi-theme, and potentially critical feedback without inventing unsupported conclusions.

## 4. Tool Surface

V2 uses local LLM inference and deterministic application functions.

| Tool / capability | What it does | Reversible? |
|---|---|---|
| `analyze_feedback()` | Uses Qwen to extract themes, sentiment, urgency, impact, severity, summaries, and evidence | Yes — generated result can be discarded |
| `validate_analysis()` | Validates structured LLM output | Yes |
| `save_feedback()` | Persists validated feedback and analysis in SQLite | No — no user-facing deletion workflow in V2 |
| `normalize_theme()` | Maps extracted themes to approved categories | Yes before persistence; historical mappings are preserved afterward |
| `detect_duplicates()` | Identifies reliable duplicates and flags suspected semantic duplicates | Yes — flags can be reviewed |
| `aggregate_feedback()` | Calculates theme counts, frequencies, and distributions | Yes — read-only |
| `calculate_priority()` | Calculates weighted priority from approved scoring rules | Yes — reproducible |
| `generate_insights()` | Uses Qwen to interpret aggregated patterns and supporting evidence | Yes — generated output can be discarded |
| `generate_recommendations()` | Proposes evidence-backed investigations and improvements | Yes — advisory |
| `review_suggestion()` | Records PM acceptance or rejection of a suggestion | No dedicated undo workflow in V2 |

**Implementation note:** These names describe the proposed V2 capability boundaries, not necessarily existing function names or currently implemented tools.

The LLM does not directly execute database modifications or approve its own suggestions.

## 5. Autonomy

The system must explicitly separate autonomous analysis from human decisions.

| Action | Autonomy | Reason |
|---|---|---|
| Extract themes, sentiment, urgency, impact, and severity | Acts automatically | Analytical interpretation |
| Generate individual summaries | Acts automatically | Low-risk advisory output |
| Map equivalent themes to approved categories | Acts automatically when sufficiently supported | Existing taxonomy |
| Propose new categories or structural merges | Requires PM approval | Changes classification structure |
| Calculate frequency and priority | Acts automatically through Python | Deterministic business logic |
| Flag critical P1 candidates | Acts automatically; PM reviews candidate | Early warning without autonomous approval |
| Generate insights and recommendations | Acts automatically | Advisory output |
| Accept or reject recommendations and priority decisions | PM action | Product decision authority |
| Implement product changes | Not permitted | Outside V2 scope |

### Failure and Uncertainty Handling

- Invalid LLM output must not be saved as successful analysis.
- Insufficient evidence must be flagged as uncertain.
- Unsupported root-cause claims must not be presented as facts.
- Ambiguous category mappings must be flagged for review.
- Tool failures must stop the affected operation and return an understandable error.
- Previously saved feedback must remain available after failures.
- If PM approval is required and not provided, the suggestion remains pending.
- The system must not silently approve or execute pending decisions.

## 6. Happy Paths / Golden Dataset

### Scenario 1 — Multiple Themes and Mixed Sentiment

**Customer feedback:**

"The app is easy to use, but checkout keeps failing. I tried three times and couldn't complete my order."

**Expected behavior:**

1. Identify app usability as a positive theme.
2. Identify checkout failure as a negative theme.
3. Classify overall sentiment as Mixed.
4. Assess checkout impact and severity based on the stated inability to complete an order.
5. Preserve supporting evidence for both themes.
6. Save validated analysis in SQLite.

**Expected outcome:** Multiple distinct themes are extracted without losing the mixed customer experience.

### Scenario 2 — Recurring Customer Problem

**Stored feedback:** 100 eligible reviews, including 25 distinct reviews explicitly mentioning checkout failures.

**Expected behavior:**

1. Python aggregates stored reviews.
2. Checkout Failure frequency is calculated as 25%.
3. Each review contributes at most once to the theme.
4. Inferred mentions do not increase official frequency.
5. Python calculates the frequency score as 5.
6. The system checks recommendation eligibility.
7. Qwen generates a grounded insight and possible investigation recommendation.

**Expected outcome:** The PM sees checkout failures as a recurring customer issue with supporting evidence.

### Scenario 3 — Critical Issue With Limited Frequency

**Customer feedback:**

"After submitting my order, the app deleted my saved payment information and order history."

**Expected behavior:**

1. Extract the relevant explicit issue.
2. Assess potential severity using the approved rubric.
3. Flag uncertainty about the underlying cause.
4. If the critical-severity criteria are met, flag a P1 candidate.
5. Propose investigation rather than asserting a confirmed root cause.
6. Require PM review of the critical priority candidate.

**Expected outcome:** A potentially critical problem receives attention without being misrepresented as widespread or technically confirmed.

### Golden Dataset

**Pilot:** 100 historical reviews analyzed individually.

**Golden dataset:** 30 manually labeled historical reviews.

Human labels will include expected themes, explicit/inferred classification, sentiment, urgency, impact, severity, and supporting evidence.

The golden dataset will be maintained separately:

`evals/golden-dataset.json`

These scenarios are illustrative seeds, not completed golden records.

## 7. Non-Goals

V2 will not:

- Process multiple new feedback submissions in a single batch.
- Support bulk CSV ingestion.
- Run background review-processing jobs.
- Integrate with Amazon, app stores, or support platforms.
- Automatically create Jira tickets.
- Implement recommended product changes.
- Automatically close customer support feedback loops.
- Provide enterprise authentication or multi-user collaboration.
- Maintain a formal PM approval audit trail.
- Retroactively reclassify historical themes following taxonomy changes.
- Train or fine-tune Qwen on customer reviews.

Batch processing, scheduled monitoring, external integrations, and recommendation outcome tracking are potential future enhancements.

## 8. Eval Rubric

### Definition of Success

The system successfully extracts grounded information from individual feedback, aggregates recurring themes accurately, and produces useful product insights. Priority scores must follow deterministic rules, and recommendations must be supported by customer evidence. The system must respect human approval boundaries and clearly distinguish observations from hypotheses.

### Known Risks

| Risk | Potential failure |
|---|---|
| Incorrect classification | Qwen misses a theme or assigns the wrong sentiment |
| Unsupported inference | AI invents customer needs or product characteristics |
| Duplicate counting | Theme frequency is inflated |
| Taxonomy inconsistency | Equivalent themes are counted separately |
| Incorrect priority | Weighted scoring or threshold logic is wrong |
| Recommendation hallucination | AI invents root causes or unsupported solutions |
| Governance failure | AI changes categories without PM approval |
| Local model limitations | Slow inference or incomplete structured output |

### Outcome — Pass / Fail

- Extracted themes, sentiment, and urgency agree with human-labeled expectations under the evaluation criteria.
- Aggregated frequencies and priorities are calculated correctly.
- Recommendations satisfy eligibility rules and are supported by evidence.

### Trajectory — Pass / Fail

- Individual feedback follows extraction, validation, and persistence steps.
- Aggregated insights use stored structured data and supporting evidence.
- Priority calculations are executed through deterministic Python logic.

### Governance — Pass / Fail

- Unsupported inferences are not presented as facts.
- Inferred themes are excluded from official frequency.
- Taxonomy changes requiring approval are not automatically applied.
- Recommendations and critical priority candidates remain advisory until reviewed.

### Experience — Pass / Fail

- Insights are understandable to a Product Manager.
- Recommendations clearly identify the customer problem and proposed next action.
- Supporting evidence and uncertainty are visible.

**Rubric artifact:** `evals/eval-rubric-v1.md`

**Scoring approach:** Pass / Fail.

The detailed rubric, test cases, and evaluation results will be defined in separate artifacts.

## 9. Release Thresholds

Release thresholds are evaluated across multiple reviews and workflows, rather than a single example.

| Metric | Initial target | Why |
|---|---|---|
| Theme extraction accuracy | Establish after baseline | Confirm classification quality |
| Sentiment and urgency accuracy | Establish after baseline | Validate interpretation |
| Impact and severity accuracy | Establish after baseline | Validate prioritization inputs |
| Deterministic calculation correctness | 100% on defined test cases | Business rules must be reproducible |
| Critical governance violations | 0 tolerated | Prevent unauthorized decisions |
| Single-feedback latency | Measure baseline | Understand local Qwen performance |
| Cost per task | No paid LLM API required | Maintain local-first architecture |
| Overall evaluation failure-rate ceiling | Establish after baseline | Determine release readiness |

The initial pilot will establish baseline quality and latency. Numerical targets for probabilistic model behavior will then be proposed and approved before wider release.

## 10. Rollout

### Stage 1 — Local Development

Implement enhanced individual feedback analysis, SQLite changes, taxonomy mapping, aggregation, prioritization, and insight generation.

**Exit criteria:** Functional requirements are implemented and deterministic tests pass.

### Stage 2 — Evaluation Pilot

Analyze 100 historical reviews individually, including the 30 manually labeled golden reviews.

Run Reforge-style evaluations for Outcome, Trajectory, Governance, and Experience.

**Exit criteria:** Evaluation baseline is documented, major failure modes are understood, and proposed release thresholds are reviewed.

### Stage 3 — Human-in-the-Loop Beta

Use the dashboard to review insights, recommendations, and priority candidates.

**Exit criteria:** Approved quality thresholds are met, critical governance tests pass, and PM review confirms that outputs are useful.

### Stage 4 — V2 Release

Release the validated local application for its intended pilot usage.

**Exit criteria:** Required evaluation thresholds and acceptance tests pass.

Enterprise general availability is not part of this V2 rollout.

## 11. Open Questions

| Question | Owner | Decision timing |
|---|---|---|
| How should impact and severity scores from multiple reviews be aggregated into one theme-level score? | Product Manager | Before priority implementation |
| What evidence-reference format should be stored? | Engineering / Product | Before data model implementation |
| How should suspected semantic duplicates be reviewed? | Product Manager | Before deduplication UI implementation |
| Should aggregated insights refresh automatically or on user request? | Product Manager | Before insights implementation |
| What are the final classification accuracy and latency thresholds? | Product Manager | After evaluation baseline |
| How should taxonomy versions be displayed in historical analytics? | Product Manager / Engineering | Before taxonomy UI implementation |

---

**Document status:** Draft for product approval.  
**Next artifact:** Reforge Evaluation Rubric V1.  
**Recommended location:** `docs/PRD-V2.md`.