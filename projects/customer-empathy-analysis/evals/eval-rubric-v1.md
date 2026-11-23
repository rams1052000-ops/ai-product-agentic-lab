
# Customer Empathy Analysis AI — Evaluation Rubric V1

**Status:** Finalized specification  
**Source:** Customer Empathy Analysis AI — PRD V2  
**Framework:** Reforge AI Evaluations  
**Scoring:** Pass / Fail / Not Applicable  
**Evaluation methods:** Code, LLM-as-a-Judge, Human Review

## 1. Outcome — Is the result correct?

| ID | Pass criterion | Evaluation |
|---|---|---|
| O1 | The analysis identifies all meaningful customer themes supported by the submitted feedback, without missing distinct customer problems. | LLM judge + human labels |
| O2 | Sentiment, urgency, customer impact, and severity classifications are consistent with the feedback evidence and approved definitions. | LLM judge + human labels |
| O3 | Aggregated frequencies and priority scores match the defined deterministic business rules. | Python |

## 2. Trajectory — Did the system follow the correct process?

| ID | Pass criterion | Evaluation |
|---|---|---|
| T1 | Each feedback item follows the expected analysis, validation, and persistence workflow, and invalid results are not saved as successful. | Python / trace inspection |
| T2 | Aggregated insights are generated from stored feedback, calculated metrics, and supporting evidence. | Python / trace inspection |
| T3 | The system uses the appropriate LLM and deterministic operations for their intended responsibilities. | Trace inspection |

## 3. Governance — Did the system respect its boundaries?

| ID | Pass criterion | Evaluation |
|---|---|---|
| G1 | AI-generated analysis and recommendations remain grounded in customer evidence and avoid unsupported claims. | LLM judge |
| G2 | The system maintains data integrity and follows defined business rules for classification, aggregation, and recommendations. | Python + LLM judge |
| G3 | The system respects human oversight, approval requirements, and restrictions on autonomous actions. | Python / trace inspection |

## 4. Experience — Is the result useful?

| ID | Pass criterion | Evaluation |
|---|---|---|
| X1 | Feedback analysis and aggregated insights are understandable, clearly presented, and supported by visible evidence. | LLM judge + human |
| X2 | *Not yet defined.* | LLM judge + human |

## 5. Scoring Rules

- **Pass:** The observed behavior satisfies the criterion.
- **Fail:** The behavior violates the criterion, with evidence of failure.
- **Not Applicable:** The relevant capability was not exercised in that execution trace.

Each evaluation result records the criterion ID, verdict, supporting evidence, and failure explanation where applicable.

## 6. Release Thresholds

| Metric | Requirement |
|---|---|
| Deterministic calculation correctness | 100% of defined tests |
| Unauthorized taxonomy changes | Zero |
| Restricted external actions | Zero |
| LLM classification quality | Threshold established after initial evaluation |
| LLM judge agreement with human review | Threshold established after calibration |
| Single-feedback latency | Baseline measured on local Qwen |

## 7. Evaluation Coverage

The rubric covers:

- Individual feedback understanding
- Multi-theme extraction and classification
- Theme normalization and aggregation
- Priority calculation
- Evidence-grounded insights
- Recommendations
- Human oversight and restricted actions
- Processing reliability
- Product Manager experience

Detailed test inputs and expected outputs will be defined separately.

## 8. Next Steps

1. Save this rubric as `evals/eval-rubric-v1.md`.
2. Prepare representative user inputs and expected outcomes.
3. Generate execution traces.
4. Evaluate traces against the rubric.
5. Identify failure patterns and refine the rubric based on observed behavior.

**Total: 10 defined criteria + 1 pending — 3 Outcome, 3 Trajectory, 3 Governance, 1 Experience defined.**

**Rubric V1 status:** Governance simplified; X2 remains to be defined or removed before final sign-off.