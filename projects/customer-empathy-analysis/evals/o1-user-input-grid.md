# O1 User Input Grid — Meaningful Theme Extraction

**Status:** Draft dataset design for human labeling and judge alignment  
**Criterion:** O1 — The analysis identifies meaningful customer themes supported by the feedback while preserving distinct customer experiences.  
**Scope:** Theme extraction only. Sentiment, urgency, priority, validation, persistence, and taxonomy normalization are evaluated elsewhere.

## Coverage dimensions

| Dimension | Values covered | Why it matters |
|---|---|---|
| Theme load | No specific product theme; one theme; two themes; three themes | Detects missed themes and invented themes. |
| Theme relationship | Not applicable; related; unrelated; same capability with an important constraint | Tests when broad grouping is acceptable and when it loses meaning. |
| Sentiment profile | Positive; negative; neutral; mixed; emotional | Prevents the judge from equating “theme” with “complaint.” |
| Specificity | Explicit; implicit; vague; purely emotional; feature request | Tests whether the model stays grounded without inventing causes or defects. |
| Customer impact | None stated; low; medium; high; critical | Covers both minor experiences and important customer problems. Impact itself is not scored by O1. |
| Phrasing | Short; compound sentence; contrast; multi-sentence; informal; question | Reduces dependence on one writing style. |

## How to use this grid

1. Run the application on each input and record the exact generated theme or themes.
2. A human reviews the generated output against the expected theme behavior.
3. Add a human O1 label (`PASS` or `FAIL`) and a short explanation.
4. Use a balanced 20–40 labeled-output sample to align the O1 judge.
5. Keep these rows out of the judge prompt's few-shot examples.

The expected behavior is intentionally semantic rather than an exact required label. Equivalent wording can pass when it preserves the evidence.

## Thirty targeted inputs

| ID | Theme load | Relationship | Sentiment | Specificity | Impact | Phrasing | Customer input | Expected O1 theme behavior |
|---|---|---|---|---|---|---|---|---|
| O1-001 | One | N/A | Negative | Vague | High | Short | The app does not work at all. | A broad application-functionality failure is supported; do not invent a specific broken feature. |
| O1-002 | One | N/A | Negative | Explicit | High | Short | Checkout fails every time I pay. | Represent checkout or payment failure. |
| O1-003 | Two | Unrelated | Mixed | Explicit | High | Contrast | Checkout fails, but search works great. | Preserve the negative checkout experience and positive search experience separately; do not collapse them into an ambiguous combined label. |
| O1-004 | Two | Related | Positive | Explicit | Low | Compound | The app is fast and easy to use. | Represent speed and usability; a broader positive user-experience theme may pass only if both meanings remain clear. |
| O1-005 | None | N/A | Neutral | Explicit | None | Short | I used the app yesterday. | Do not invent a product problem, benefit, or feature-specific theme. |
| O1-006 | One | N/A | Negative | Vague | Low | Short | This could be better. | A broad improvement or dissatisfaction theme is acceptable; do not invent a cause or affected feature. |
| O1-007 | One | N/A | Emotional negative | Purely emotional | Medium | Informal | I hate this app! | Preserve general dissatisfaction without inventing a specific defect. |
| O1-008 | One | N/A | Negative | Explicit | Critical | Short | All my saved data disappeared. | Represent data loss; do not soften it into generic usability. |
| O1-009 | Two | Related | Negative | Explicit | High | Compound | Login is slow and checkout crashes. | A broader performance or reliability theme may represent both related failures. |
| O1-010 | One | N/A | Negative | Explicit | Medium | Short | I waited 10 minutes for the page to load. | Represent page-loading slowness; do not invent the technical cause. |
| O1-011 | Two | Related | Negative | Explicit | Medium | Compound | Reports take forever to open and dashboard images load late. | A broader performance theme is acceptable because both experiences concern slowness. |
| O1-012 | Two | Unrelated | Mixed | Explicit | High | Contrast | My invoice total is wrong, although the help documentation is excellent. | Preserve the billing-accuracy problem and positive documentation experience separately. |
| O1-013 | Two | Unrelated | Mixed | Explicit | Medium | Contrast | Notifications arrive late, but dark mode looks excellent. | Preserve notification delay and positive dark-mode experience separately. |
| O1-014 | One | N/A | Positive | Explicit | Low | Short | PDF export works perfectly. | Represent successful export or export reliability; do not invent an export failure. |
| O1-015 | Two | Related | Negative | Explicit | Medium | Compound | Audio stutters and videos keep buffering. | A broader media-performance theme may represent both playback problems. |
| O1-016 | Three | Partly unrelated | Mixed | Explicit | Critical | Multi-sentence | The app crashes when I save. The total on my invoice is wrong. Support was very helpful. | Preserve the save crash, invoice-accuracy problem, and positive support experience; grouping must not hide any of them. |
| O1-017 | Two | Related but contrasting | Mixed | Explicit | Medium | Contrast | Setup instructions are confusing, but the onboarding tooltips are helpful. | Preserve both negative instructions and positive tooltips; a mixed onboarding theme passes only if the contrast remains visible. |
| O1-018 | Two | Related but platform-specific | Mixed | Explicit | Medium | Contrast | Mobile navigation is intuitive, but the desktop layout is broken. | Preserve the positive mobile and negative desktop experiences, including their platform distinction. |
| O1-019 | Two | Related | Negative | Explicit | High | Compound | The password-reset link expires before the reset email arrives. | A broader account-recovery failure may represent the linked timing and expiration problems. |
| O1-020 | Two | Related | Negative | Explicit | Medium | Compound | Search results are irrelevant and there are no useful filters. | A broader search/discovery theme may represent both related problems. |
| O1-021 | Two | Unrelated | Mixed | Explicit | Medium | Contrast | Pricing is confusing, even though the app runs very fast. | Preserve pricing clarity and positive performance separately. |
| O1-022 | One | N/A | Emotional positive | Purely emotional | Low | Informal | Love it—best app ever! | A broad positive satisfaction theme is supported; do not invent a specific product benefit. |
| O1-023 | One | N/A | Negative | Explicit | Low | Short | I cannot use keyboard shortcuts. | Represent missing or unusable keyboard shortcuts. |
| O1-024 | Two | Unrelated | Negative | Explicit | Medium | Compound | The ads are annoying and the app drains my battery. | Preserve advertising annoyance and battery usage separately; a generic “bad experience” theme is too lossy. |
| O1-025 | Two | Same capability with constraint | Mixed | Explicit | High | Contrast | JPG uploads fail, but PNG uploads work. | Preserve the format-specific difference within image upload; do not label all uploads as broken or successful. |
| O1-026 | Two | Related | Negative | Explicit | High | Compound | Support took three days to reply and still did not resolve my issue. | A broader support-quality theme may represent both slow response and unresolved outcome. |
| O1-027 | One | N/A | Concerned | Implicit/question | Medium | Question | Why does a calculator app need access to my contacts? | Represent a privacy or unnecessary-permissions concern without claiming misuse occurred. |
| O1-028 | One | N/A | Neutral request | Feature request | Medium | Short | Please add calendar synchronization. | Represent a calendar-integration feature request; do not turn it into an existing defect. |
| O1-029 | Two | Related | Negative | Explicit | High | Compound | Text contrast is too low and screen-reader buttons have no labels. | A broader accessibility theme may represent both problems if visual contrast and screen-reader labeling remain supported. |
| O1-030 | Three | Unrelated | Mixed | Explicit | High | Multi-sentence | My saved filters disappear. Export is reliable. The dashboard looks beautiful. | Preserve filter persistence, positive export reliability, and positive dashboard design as distinct experiences. |

## Coverage check

- Includes zero-, one-, two-, and three-theme inputs.
- Includes related themes that may be grouped and unrelated themes that must remain distinct.
- Includes positive, negative, neutral, mixed, and emotional feedback.
- Includes explicit, vague, implicit, purely emotional, and feature-request language.
- Includes acceptable broad themes, missing-theme risks, unsupported-theme risks, over-grouping risks, and important constraints.
- Includes short, compound, contrast, informal, question, and multi-sentence phrasing.

## Human-label fields to add after generation

For each recorded application output, add:

| Field | Meaning |
|---|---|
| `generated_themes` | Exact output produced by the application. |
| `human_o1_label` | Human decision: `PASS` or `FAIL`. |
| `human_reason` | Short evidence-based explanation. |
| `run_id` | Model/prompt version or trace identifier. |
| `reviewer` | Person who assigned the label. |
| `reviewed_at` | Review date. |

Do not assign the human label before seeing the generated output: the input itself does not pass or fail; the output does.
