# Failure Analysis — Customer Empathy AI

## Failure 001 — Multi-Theme Extraction

**Test ID:** 003  
**Rubric criterion:** O1 — Theme Extraction  
**Failure code:** `INCOMPLETE_THEME_EXTRACTION`

**Customer input:**  
"Checkout fails, but search works great."

**Expected behavior:**
- Checkout failure — Negative
- Search functionality — Positive

**Actual behavior:**
- Overall sentiment: Mixed
- One combined theme: "checkout search"

**Evaluation:**
- O1 Theme extraction: FAIL
- O2 Sentiment: PASS

**Root cause:** Not yet determined.

**V2 implication:** Support multiple themes and per-theme sentiment within a single feedback item.

## Test 009 — Related Issues Grouped


**Input:** "Login is slow and checkout crashes."

**Expected:** Related issues may be grouped under a broader theme.

**Actual:** Performance issues.

**Rubric:** O1 — Theme Extraction

**Result:** PASS

**Failure code:** None

**Reason:** The broader theme is acceptable for this test.

## Capability Gap — Theme Normalization

**Test ID:** 010  
**Code:** `MISSING_THEME_NORMALIZATION`

**Observation:** V1 generates a theme independently for each feedback item without checking previously classified themes.

**Expected V2 behavior:** Match new feedback themes to existing equivalent categories when appropriate, avoiding duplicate categories.

**Evaluation:** Theme extraction PASS; normalization NOT IMPLEMENTED in V1.

**V2 implication:** Introduce semantic theme normalization using existing categories.

**Status:** Known V1 capability gap; not counted as a V1 evaluation failure.

