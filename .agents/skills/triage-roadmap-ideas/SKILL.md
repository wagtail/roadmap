---
name: triage-roadmap-ideas
description: Triage unstructured roadmap ideas or feature requests against Wagtail's product strategy and selection criteria — classify the item, run the AI/ecosystem/maintainability gates, score it on the weighted matrix, plot it on the strategic-value/viability axes, and record a qualitative summary with a decision. Use this whenever someone drops in a feature request, a wishlist, a "should we do X?" question, or a grab-bag of ideas and wants to know where it fits in the prioritization framework, whether it's on-strategy, what score it gets, or what to do with it — even if they don't say the word "triage".
license: MIT
metadata:
  audience: maintainers
  # Hide the skill from discovery: https://github.com/vercel-labs/skills#optional-fields
  internal: true
  disable-model-invocation: true
---

## Overview

Take one or more roadmap ideas in unstructured form — a single feature request, a vague "should we do X?", or a grab-bag of wishes pasted from a discussion — and run each through Wagtail's triage methodology to produce a structured assessment: a classification, gate results, a weighted score, a position on the strategic-value/viability chart, and a qualitative summary ending in a decision. This is the front of the roadmap funnel: it helps decide whether an idea is worth pursuing and how it's framed, *before* anyone writes an [RFC](../draft-roadmap-rfc/SKILL.md) or an [issue](../draft-roadmap-issues/SKILL.md).

The scoring rubric itself lives in **[`docs/selection-criteria.md`](../../../docs/selection-criteria.md)** — that is the source of truth for the gates, the 1–5 guidance per criterion, the weights, and the two-axis view. This skill *instruments* that document: it tells you how to apply it consistently and what to emit. When the two disagree, the criteria doc wins; don't hard-code numbers or guidance from it here, read it at runtime so the skill tracks the (still-evolving, `DRAFT`) methodology.

The output is a Markdown report the user reviews — it does **not** create issues, open PRs, or change the roadmap. It's a decision aid, not a decision.

Read first, every run:

- [`docs/selection-criteria.md`](../../../docs/selection-criteria.md) — the methodology: Stage 0 classification, gates G1–G3, the six-criterion scoring matrix, the qualitative summary, and the two-axis view. **This drives everything below.**
- [`docs/product-strategy.md`](../../../docs/product-strategy.md) — the strategy the scores are grounded in (pillars, differentiators, AI principles, target sectors).
- [`README.md`](../../../README.md) — the canonical short names + emoji for the pillars and supporting work.
- [`.github/labels.json`](../../../.github/labels.json) — the only valid labels.

## Methodology

### Goals

- Run each idea through the full pipeline in [`selection-criteria.md`](../../../docs/selection-criteria.md): **classify → gate → score → plot → summarise → decide**.
- Ground every judgment in the strategy *as written*. A criterion-1 score of 4–5 should point at a named element of a pillar; a differentiator score of 4–5 should point at accessibility / security / sustainability / responsible AI / SEO. If you can't cite it, it isn't that high.
- Produce numbers a human can trust *and* the qualitative record that explains them — the single weighted score ranks the queue, the summary explains why, and the "key assumption" says which lever would move it.
- Point to **related roadmap items** already in [`.issues/`](../../../.issues) and suggest **2–3 real labels**, so a graduating idea is ready to become an issue.
- Be honest about weak or off-strategy ideas. A low score, a gate block, or a "route out at Stage 0" is a legitimate, useful outcome — report it plainly rather than inflating scores to give an idea a home.

### Guardrails

- The rubric is [`selection-criteria.md`](../../../docs/selection-criteria.md), not your taste. Read it each run and apply its tables. Don't invent criteria, weights, or score bands.
- **Classify before scoring.** Only *pillar work* and *enablers* go through the matrix. Maintenance (security patches, dependency bumps, small template/DX enhancements) and management-system changes are routed out at Stage 0 with a note — don't force a matrix score onto them. Example: `include_block template tag` (#161) is a small DX enhancement, not pillar work — route it out; `Adopt Stimulus` (#21) is an *enabler* — score it with the enabler variant of Criterion 1.
- **Gates are hard blocks.** Any G1 AI-principle **Violation**, or a failed G2/G3, blocks the item — it's declined, redirected, or returned for revision. Still report the matrix if useful, but the decision is driven by the block, not the score.
- Resist strategic-fit inflation. Criterion 1 is the **MAX** across the four pillars, but most ideas genuinely deliver *one* pillar and score 1–2 on the others — record the per-pillar spread honestly; a row of 4s across all pillars almost always means the scoring is too generous.
- Only use labels that exist in [`.github/labels.json`](../../../.github/labels.json), and only cite related items that actually exist in [`.issues/open`](../../../.issues/open) or [`.issues/closed`](../../../.issues/closed), linked by real issue number. Never invent either.
- Don't write issue bodies, RFC sections, or effort estimates beyond the S/M/L/XL bubble size — that's [`draft-roadmap-issues`](../draft-roadmap-issues/SKILL.md) and [`draft-roadmap-rfc`](../draft-roadmap-rfc/SKILL.md). Triage stops at "here's the score, the position, and the decision".

### Scoring notes (the rubric lives in the criteria doc)

Read [`selection-criteria.md`](../../../docs/selection-criteria.md) for the actual tables. A few things worth holding in mind as you apply it, so the output is consistent across runs:

- **Criterion 1 (Strategic fit, 25%)** — for pillar work, score the idea against *each* of the four pillars and take the MAX; record all four so the pillar-balance review and the alignment metric have data. For enablers, use the enabler variant (breadth of unblocking). The pillar that produced the MAX is the item's **primary pillar** — its emoji is the visual marker.
- **G1 (AI principles)** — mark each of the five principles **Pass / N/A / Violation**. For an idea with no AI dimension, all five are usually **N/A** (that's fine, not a gap). Record the marks even when the whole row is N/A — the record is the point, since a clean set of Pass marks on an AI feature is a responsible-AI proof point for marketing.
- **Weighted overall** — `Σ (score × weight)`, out of 5. Show the arithmetic in the matrix so it's checkable.
- **Two-axis coordinates** — Y (strategic value) = mean of criteria 1, 2, 3; X (viability) = mean of criteria 4, 5, 6; bubble = S/M/L/XL effort; marker = primary-pillar emoji. Name the quadrant and the disposition it implies (schedule now / find a sponsor / decline or park / opportunistic).
- Historical/closed items assessed retrospectively (as many eval cases are): score demand and sponsorship from the evidence in the body (e.g. `Headless & API improvements` (#94) cites the *2024 headless survey* → real demand signal), and say when evidence is absent rather than assuming it.

### Finding related roadmap items

The local issue files in [`.issues/open`](../../../.issues/open) and [`.issues/closed`](../../../.issues/closed) are the fastest source. Each is `<number>-<slug>.md` with frontmatter (`title`, `labels`, `milestone`) and a body. Match on concept, not just keywords. Strategic themes/pillars are **not** stored in these files (they live as a custom field on [project 16](https://github.com/orgs/wagtail/projects/16)), so infer an existing item's pillar from its title/body if needed. For each related item, give the issue link, its title, and one line on *how* it relates (duplicate / overlaps / umbrella / depends on / follow-up / precursor).

### Suggesting labels

Pick 2–3 from [`.github/labels.json`](../../../.github/labels.json) — usually topic labels for the area, plus a status label (`needs sponsorship`, `needs contributions`, `sponsored`) only if the idea/decision implies it. Favour the labels the related items already use, for consistency. If no label fits well, say which is closest and note the gap rather than forcing a third.

### Inputs

Detect from the request, or ask if unclear:

- **The idea(s)** — pasted text, a file path (e.g. an existing `.issues/...md`), or a link. The only required input.
- **Output path** — default `triage-<slug>.md` in the repo root, where `<slug>` is a short kebab-case name derived from the idea (or the batch, for a grab-bag). Reuse an existing placeholder if the user made one.
- **Whether to write a file** — default yes. For a quick gut-check it's fine to answer inline and skip the file; ask if ambiguous.

### Reporting

After writing the file, give the user a short summary: for each idea, the classification, the primary-pillar emoji, the overall weighted score, the quadrant, and the decision. Flag anything blocked by a gate or routed out at Stage 0. Point to the file path. Suggest next steps: strong, high-viability ideas → flesh out into an RFC/issue via the sibling skills; high-value/low-viability → the lever from "key assumption"; weak/off-strategy → what would change the picture.

## Output format

Use this structure. For a **single idea**, emit one assessment and skip the summary/scatter section. For a **grab-bag**, split the input into distinct ideas first (one idea = one thing that could become one roadmap item), emit one assessment per idea, then the ranking table and scatter coordinates at the end.

```markdown
# Triage: <batch or idea title>

_Assessed against [selection criteria](docs/selection-criteria.md) + [product strategy](docs/product-strategy.md) v<version> on <YYYY-MM-DD>._

## <primary-pillar emoji> <Idea 1: short title>

> <one- or two-sentence restatement of the idea in your own words, so the caller can confirm you understood it>

**Classification:** Pillar work · <or Enabler / Maintenance — routed out / Management system — not a roadmap item>

<!-- If routed out at Stage 0, stop after a one-line rationale + a decision. Only pillar work and enablers get the full block below. -->

### Gates

| Gate | Result | Note |
| --- | --- | --- |
| G1 · AI principles | Pass / **Blocked** | all N/A (no AI dimension) — or summarise the marks |
| G2 · Ecosystem placement | Core / Package | <why it belongs there> |
| G3 · Maintainability floor | Pass / Concern | <bounded? understood?> |

<!-- G1 detail — include the per-principle table only when the idea has an AI dimension: -->
| AI principle | Mark | Note |
| --- | --- | --- |
| 1. No AI dependency in core | Pass / N/A / **Violation** | … |
| 2. Responsible approach to AI | … | … |
| 3. Model and provider agnostic | … | … |
| 4. Only the right AI | … | … |
| 5. Human in the loop | … | … |

### Score

| Criterion | Weight | Score (1–5) | Weighted | Why |
| --- | --- | --- | --- | --- |
| 1. Strategic fit | 25% | 5 | 1.25 | MAX of per-pillar below |
| 2. Differentiator reinforcement | 15% | 4 | 0.60 | … |
| 3. User demand & adoption | 15% | 3 | 0.45 | … |
| 4. Sponsorship appeal | 15% | 3 | 0.45 | … |
| 5. Deliverability | 15% | 4 | 0.60 | … |
| 6. Maintenance burden (high = low burden) | 15% | 4 | 0.60 | … |
| **Overall** | 100% | | **3.95 / 5** | |

Per-pillar strategic fit (criterion 1) — MAX is the primary pillar:

- 🏔️ 5 ← MAX (primary)
- 🪢 2
- 🛠️ 3
- 🌳 1

### Position

- **Strategic value (Y)** = mean(1, 2, 3) = 4.0
- **Viability (X)** = mean(4, 5, 6) = 3.7
- **Bubble (effort):** M
- **Quadrant:** High value · High viability → **Schedule now**

### Assessment

- **Rationale:** <one paragraph — why this item, why now, in strategy language.>
- **Primary pillar:** 🏔️ Future-ready content management.
- **AI principles:** <Pass, all N/A — or the notable marks>.
- **Key assumption to test:** <the single thing most likely to change the score.>
- **Related roadmap items:** [Title](https://github.com/wagtail/roadmap/issues/36) — <how it relates>. _(or "None found.")_
- **Suggested labels:** `accessibility`, `UX` — <one line on the choice>.
- **Decision:** Schedule / Seek sponsor / Park / Decline — review by <YYYY-MM-DD>.

---

## Summary  ← grab-bag only

Ranked by overall weighted score.

| # | Idea | Class | Primary | Score | Quadrant | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | <title> | Pillar | 🏔️ | 4.00 | Schedule now | Schedule |
| 2 | <title> | Enabler | 🏗️ | 3.30 | Find a sponsor | Seek sponsor |
| — | <title> | Maintenance | — | — | routed out | Decline |

### Scatter coordinates

| Idea | Strategic value (Y) | Viability (X) | Effort | Marker |
| --- | --- | --- | --- | --- |
| <title> | 4.0 | 3.7 | M | 🏔️ |
```

## Steps

### 1. Load the methodology and gather inputs

- [ ] Read [`docs/selection-criteria.md`](../../../docs/selection-criteria.md) in full — it drives every step. Then [`docs/product-strategy.md`](../../../docs/product-strategy.md) (pillars, differentiators, AI principles, target sectors) and [`README.md`](../../../README.md) (pillar emoji/short names). Note the strategy version + date for the report header.
- [ ] Read [`.github/labels.json`](../../../.github/labels.json) so you only suggest real labels.
- [ ] Capture the idea(s). For a grab-bag, split into distinct ideas — one idea = one thing that could become a single roadmap item. Merge duplicates; split a line that hides two asks (and say so).

### 2. Classify (Stage 0)

- [ ] For each idea, classify per the Stage 0 table: **Pillar work**, **Enabling capabilities**, **Maintenance**, or **Management system**. Only pillar work and enablers continue to the matrix; record a one-line rationale and a decision for the others and move on. (E.g. `Editor guide translations` (#17) is thin documentation work; `include_block template tag` (#161) is a small DX enhancement — both route out rather than scoring as pillar work.)

### 3. Run the gates (G1–G3)

- [ ] **G1** — mark all five AI principles Pass/N/A/Violation (all N/A for non-AI ideas). Any Violation blocks.
- [ ] **G2** — core vs package. Package territory is fine when the item needs a new core API/integration point or is meant to be an official "blessed" package.
- [ ] **G3** — is the ongoing maintenance burden bounded and understood?
- [ ] A blocked item is declined/redirected/returned — carry that into the decision.

### 4. Score the matrix

- [ ] Score each of the six criteria 1–5 using the criteria-doc tables, multiply by weight, and sum to the overall out of 5. Show the arithmetic.
- [ ] For Criterion 1, score all four pillars and take the MAX; record the per-pillar spread and set the primary pillar. Use the enabler variant for enablers.
- [ ] Ground criterion 1 and 2 scores in named strategy elements; score demand/sponsorship from real evidence in the idea (survey, sector, sponsor interest) and say so when it's absent.

### 5. Plot the two-axis position

- [ ] Compute Y = mean(1,2,3) and X = mean(4,5,6). Set the bubble to the S/M/L/XL effort estimate and the marker to the primary-pillar emoji. Name the quadrant and its disposition.

### 6. Related items, labels, qualitative summary

- [ ] Search [`.issues/open`](../../../.issues/open) and [`.issues/closed`](../../../.issues/closed) for related items; cite real issue numbers and how they relate.

  ```bash
  ls .issues/open/ .issues/closed/ && rg -il "<keyword>" .issues/open/ .issues/closed/
  ```

- [ ] Pick 2–3 real labels from [`.github/labels.json`](../../../.github/labels.json).
- [ ] Write the qualitative summary: one-paragraph rationale, primary pillar, AI-principles record, key assumption to test, and the decision (schedule / seek sponsor / park / decline) **with a review date**.

### 7. Write the report and summarize

- [ ] Write the file to `triage-<slug>.md` (unless the user asked for inline only), following the output format. One assessment per idea; add the summary ranking table + scatter coordinates only for grab-bags.
- [ ] Read the file back and lint: classification present; gates recorded (G1 marks for AI ideas); six criteria scored with weighted arithmetic and per-pillar spread; Y/X coordinates + quadrant; qualitative summary with a decision and review date; every related-item link a real `.../issues/<N>`; every label in `labels.json`.
- [ ] Report to the user per the Reporting section, and point to the file path.
