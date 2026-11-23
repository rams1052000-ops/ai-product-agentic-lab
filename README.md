# AI Product & Agentic AI Lab

Hands-on AI product experiments showing how I move from customer problem and
product requirements to working prototypes, evaluation evidence, governance,
and iteration decisions.

## Portfolio focus

- AI product strategy and requirements
- LLM product and workflow design
- Human-in-the-loop decisions and governance
- Evaluation datasets, failure analysis, and LLM-judge alignment
- Technical fluency through working prototypes
- Clear separation between probabilistic AI behavior and deterministic logic

## Featured project

### Customer Empathy Analysis AI

A local AI workflow that converts unstructured customer feedback into structured
product signals for Product Managers. The working MVP uses Qwen 3.5 through
Ollama, Flask, Python, and SQLite. The next product version is defined through a
PRD and validated through a Reforge-style evaluation framework.

| Portfolio evidence | Artifact |
| --- | --- |
| Product narrative and decisions | [Case study](projects/customer-empathy-analysis/CASE_STUDY.md) |
| Product requirements | [PRD V2](projects/customer-empathy-analysis/docs/%23%20Customer%20Empathy%20Analysis%20AI%20%E2%80%94%20PRD%20V2.md) |
| Working implementation | [Prototype and setup](projects/customer-empathy-analysis/README.md) |
| Technical design | [Architecture](projects/customer-empathy-analysis/docs/TECHNICAL_ARCHITECTURE.md) |
| AI-quality measurement | [Evaluation rubric](projects/customer-empathy-analysis/evals/eval-rubric-v1.md) |
| Dataset design | [O1 User Input Grid](projects/customer-empathy-analysis/evals/o1-user-input-grid.md) |
| Failure analysis | [Known failures](projects/customer-empathy-analysis/evals/failure%20analysi.md) |
| Executable evaluator | [O1 LLM judge](projects/customer-empathy-analysis/evals/o1_evaluator.py) |
| Tests | [Automated test suite](projects/customer-empathy-analysis/tests) |

[Read the full project documentation in Notion](https://app.notion.com/p/Customer-Empathy-Analysis-AI-3db93493be8d80dda570fd3f3d96abf4)

## Repository structure

```text
ai-product-agentic-lab/
├── README.md
└── projects/
    └── customer-empathy-analysis/
        ├── CASE_STUDY.md       # Product story, decisions, tradeoffs, evidence
        ├── README.md           # Prototype setup and current status
        ├── docs/               # PRD and technical architecture
        ├── evals/              # Rubric, datasets, traces, judges
        ├── tests/              # Automated checks
        ├── templates/          # Flask UI
        ├── static/             # UI styles
        └── *.py                # Application and deterministic logic
```

## How to review this portfolio

For a product-management review, start with the case study and PRD, then examine
the evaluation artifacts to see how product quality is defined and measured.
The implementation and architecture demonstrate technical depth; they are
supporting evidence rather than the primary story.

## Status and disclosure

This repository contains portfolio experiments built with local or synthetic
test inputs. Proposed V2 capabilities are labeled separately from implemented
MVP behavior. Evaluation results are reported only after they are run; planned
metrics and targets are not presented as measured outcomes.
