---
name: triage-roadmap-bulk
description: Triage Wagtail roadmap ideas in bulk — score many existing roadmap items and/or a batch of new ideas against the selection criteria, cache the scores, and generate an interactive HTML report with a strategic-value/viability scatter plot. Use this whenever someone wants to triage, score, or compare more than a handful of roadmap ideas at once, re-score the whole roadmap, produce a triage report or chart, or see where a batch of proposals lands on the prioritization framework — anything that calls for a portfolio view rather than a single write-up.
license: MIT
metadata:
  audience: maintainers
  # Hide the skill from discovery: https://github.com/vercel-labs/skills#optional-fields
  internal: true
  disable-model-invocation: true
---

## Overview

The bulk counterpart to [`triage-roadmap-ideas`](../triage-roadmap-ideas/SKILL.md). That skill assesses one idea (or a small grab-bag) and writes a prose Markdown report. This one runs the **same methodology across many items** — existing roadmap issues, a batch of new ideas, or both — and produces a **portfolio view**: a cached JSON assessment per item plus an interactive HTML report with a strategic-value/viability scatter plot.

Use it to re-score the whole open roadmap, compare a stack of new proposals against each other and the existing items, or refresh a triage chart after the strategy/criteria change.

The methodology is identical to the single-idea skill and lives in **[`docs/selection-criteria.md`](../../../docs/selection-criteria.md)** (classify → gate → score → plot → summarise → decide). Read it every run; don't re-derive the rubric here. The only difference in bulk mode is the _output_: each assessment is emitted as JSON (per [`references/assessment-schema.md`](references/assessment-schema.md)) so it can be cached, charted, and re-used, rather than as prose.

Read first, every run:

- [`docs/selection-criteria.md`](../../../docs/selection-criteria.md) — the methodology (drives every score).
- [`references/assessment-schema.md`](references/assessment-schema.md) — the JSON shape each assessment must take.
- [`docs/product-strategy.md`](../../../docs/product-strategy.md), [`README.md`](../../../README.md), [`.github/labels.json`](../../../.github/labels.json) — as for the single-idea skill (strategy, pillar emoji, valid labels).

## How caching works

Scoring dozens of items is expensive, so results are cached and reused. The cache lives in `.issues/triage-cache/` (git-ignored) as one JSON file per item, named `<id>__<key>.json`.

The `key` is a content hash folding together **the skill, the selection criteria, and the item's own content**. So a cached score is reused only while all three are unchanged — edit `selection-criteria.md` (e.g. reweight a criterion) or change an issue's body, and that item's cache entry no longer matches and it gets re-scored. Everything else is reused. This is why bulk re-runs are cheap: only what actually changed is re-assessed.

The report script computes these keys for you (`plan`), so you never hash anything by hand.

## Reporting script

[`scripts/generate_triage_report.py`](scripts/generate_triage_report.py) is a self-contained `uv` script (PEP 723 inline metadata, standard library only — no install). Two subcommands:

- **`plan`** — given the roadmap issue files, print which items already have a valid cached assessment (reuse) and which need one (assess), with the exact cache path to write each new one to.
- **`report`** — read the cached assessments and write the HTML report (Observable Plot scatter + accessible sortable table + routed-out list).

Run it via the shebang (`./scripts/generate_triage_report.py …`) or `uv run scripts/generate_triage_report.py …`.

### Guardrails

- Same as the single-idea skill: rubric is `selection-criteria.md`, classify before scoring, gates are hard blocks, resist strategic-fit inflation, only real labels ([`.github/labels.json`](../../../.github/labels.json)) and real issue numbers. See [`triage-roadmap-ideas`](../triage-roadmap-ideas/SKILL.md) for the detail — this skill inherits all of it.
- **Reuse the cache.** Always run `plan` first and only assess the misses. Don't re-score items the plan reports as cached — that's the whole point of the cache.
- `primary_pillar` in each JSON **must exactly match** a palette category (emoji + name) from the schema, or the point renders as "Other" grey. Copy the strings from [`README.md`](../../../README.md).
- Don't hand-edit files in `.issues/triage-cache/` except to write new assessments to the paths `plan` gives you. Don't commit the cache or the report.
- The script renders; it does not score. All judgment is yours, per the criteria doc.

## Steps

### 1. Scope the batch and gather inputs

- [ ] Read [`docs/selection-criteria.md`](../../../docs/selection-criteria.md) and [`references/assessment-schema.md`](references/assessment-schema.md), plus the strategy/labels as usual.
- [ ] Decide the set to triage:
  - **Existing roadmap items** — default `.issues/open/` (the live roadmap). Add `.issues/closed/` only if asked (e.g. a retrospective re-score).
  - **New ideas** — split any pasted batch/file into distinct ideas (one idea = one thing that could become one roadmap item), each with a short kebab `id`.

### 2. Plan against the cache

- [ ] For existing items, ask the script what's already scored:

  ```bash
  ./.agents/skills/triage-roadmap-bulk/scripts/generate_triage_report.py plan \
    --issues-dir .issues/open --json
  ```

  (Add `--ids 36,94,110` to limit to specific issues.) The output lists each item as `hit` (reuse) or `miss`, and gives the `cache_path` to write each miss to.

- [ ] New ideas have no cache history — treat them all as items to assess.

### 3. Assess the misses

For each `miss` item (and every new idea), run the full methodology from the criteria doc — classify, gate, score the six criteria, compute the two-axis coordinates, decide — exactly as the single-idea skill does. Then write the result as JSON matching [`references/assessment-schema.md`](references/assessment-schema.md):

- [ ] For existing items: write to the `cache_path` the plan gave you (`.issues/triage-cache/<id>__<key>.json`). Set `type: "issue"`, real `url`, `assessed_at` to now.
- [ ] For new ideas: write to `.issues/triage-cache/<slug>__new.json`. Set `type: "idea"`, `url: null`.
- [ ] Compute `strategic_value` = mean(strategic_fit, differentiator, demand) and `viability` = mean(sponsorship, deliverability, maintenance) — the script does not derive these.
- [ ] Set `primary_pillar` to the exact palette string. For routed-out items, set `routed_out: true` and omit the scores (they'll be listed, not plotted).
- [ ] Do the assessments in parallel where possible (they're independent), but keep each grounded in the criteria doc — don't batch-guess scores to save time.

### 4. Generate the report

- [ ] Build the HTML from the cache:

  ```bash
  ./.agents/skills/triage-roadmap-bulk/scripts/generate_triage_report.py report \
    --cache-dir ./issues/triage-cache --out triage-report.html --title "Wagtail roadmap triage — <date/scope>" --open
  ```

  Use `--ids` to scope the report to just this batch if the cache holds more than you want to show. `--open` launches a browser.

### 5. Report to the user

- [ ] Summarise: how many items scored vs reused from cache vs routed out; the top few by weighted score and their quadrant; anything blocked by a gate; and the report path. Point out that clicking a point (or its table row link) opens the roadmap issue on GitHub.
- [ ] Note next steps: strong high-viability items → flesh out via [`draft-roadmap-rfc`](../draft-roadmap-rfc/SKILL.md) / [`draft-roadmap-issues`](../draft-roadmap-issues/SKILL.md); high-value/low-viability → the lever from each item's key assumption.
