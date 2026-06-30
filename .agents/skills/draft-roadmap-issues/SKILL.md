---
name: draft-roadmap-issues
description: Convert an approved roadmap RFC into create/update/close operations for wagtail/roadmap issues
license: MIT
metadata:
  audience: maintainers
  # Hide the skill from discovery: https://github.com/vercel-labs/skills#optional-fields
  internal: true
  disable-model-invocation: true
---

## Overview

Convert an approved "Public roadmap updates" RFC into local issue files under [`.issues/`](../../../.issues), ready to review and push with [`gh-issue-sync`](https://github.com/mitsuhiko/gh-issue-sync).

Counterpart to [`draft-roadmap-rfc`](../draft-roadmap-rfc/SKILL.md): that skill writes an RFC from current roadmap data; this one applies an RFC back to the roadmap.

Read first:

- [CONTRIBUTING](../../../docs/CONTRIBUTING.md) — lifecycle, review process, maintainer metadata requirements
- [item template](../../../docs/item-template.md)
- [style guide](../../../docs/style-guide.md)
- [RFC template](../../../docs/rfc-template.md) — RFC section layout
- [`gh-issue-sync` skill](~/.agents/skills/gh-issue-sync/SKILL.md) — commands and file format

## Methodology

### Goals

- Determine which milestones and issues to **create**, **update**, **close**, or **reschedule** from the RFC.
- Create or update release milestones (with `due_on`) before assigning issues.
- Draft issue content per the item template and style guide.
- Set labels ([`.github/labels.json`](../../../.github/labels.json)), milestone, and project membership via issue frontmatter; set project custom fields on [Wagtail public roadmap](https://github.com/orgs/wagtail/projects/16) after push.
- Flag ambiguous items as `TBC` rather than guessing.

### Guardrails

- Never invent issue numbers, labels, sizes, or milestones — fetch them (see [`draft-roadmap-rfc`](../draft-roadmap-rfc/SKILL.md) reference data sources).
- Don't rephrase existing roadmap item summaries unless the RFC explicitly proposes new wording.
- Don't close issues unless the RFC's "Proposed roadmap items to close" section names them.
- Don't create issues for "Items that didn't make the cut" unless the user asks.
- Don't push to GitHub. End with local files, `gh-issue-sync push --dry-run` output, and a report.

### Inputs

Detect from context or ask the user:

- **Roadmap RFC** — local `rfc-<NNN>.md`, or latest merged `roadmap`-labelled PR in `wagtail/rfcs` (raw: `https://raw.githubusercontent.com/wagtail/rfcs/refs/heads/main/text/<NNN>-roadmap-updates.md`; fall back to PR head if unmerged).
- **Target sections** — default: all release sections in the RFC. Skip "Items that didn't make the cut".

### Reference data

Same sources as [`draft-roadmap-rfc`](../draft-roadmap-rfc/SKILL.md): `.issues/open/` and `.issues/closed/`, `.issues/.sync/milestones.json`, `gh project item-list 16 --owner wagtail`.

Local issue files do **not** include project custom fields (`Size`, `Status`, `Start date`, `Target date`). Fetch current values from the project; set changes with `gh project field-list` / `gh project item-edit` after push. See [CONTRIBUTING](../../../docs/CONTRIBUTING.md) for how milestone, Status, and Start date relate.

### Reporting

- RFC URL used.
- Milestone create / update operations (title, `due_on`, and whether already applied or pending user approval).
- Operations table: create / update / close / reschedule / no change — with issue number (or `T…` temp ID), title, milestone, size, strategic theme, labels.
- Items left `TBC` and why.
- Post-push project field commands still needed.
- Reminder to update [wagtail.org/roadmap](https://wagtail.org/roadmap/) ([CONTRIBUTING](../../../docs/CONTRIBUTING.md)).

## Steps

### 1. Sync local issues

Follow `gh-issue-sync` skill (report if uninstalled):

```bash
gh-issue-sync init --owner wagtail --repo roadmap   # if needed
gh-issue-sync pull --all
```

### 2. Ensure milestones exist

From the RFC version number and release section headings (step 3 parses items in full), list required milestone titles (`vX.Y` per section; `Future` should already exist).

Compare against `.issues/.sync/milestones.json` or:

```bash
gh api repos/wagtail/roadmap/milestones --jq '.[] | select(.state=="open") | {number, title, due_on}'
```

Derive each release milestone's `due_on` from the RFC section date and the [release schedule](https://github.com/wagtail/wagtail/wiki/Release-schedule). Wagtail ships in Feb / May / Aug / Nov.

**Create** missing milestones before drafting issues (so `due_on` is set correctly):

```bash
gh api repos/wagtail/roadmap/milestones -f title='v7.5' -f due_on='2026-08-03T00:00:00Z'
```

**Update** existing milestones when the RFC date differs from `due_on`:

```bash
gh api -X PATCH repos/wagtail/roadmap/milestones/<number> -f due_on='2026-08-03T00:00:00Z'
```

`gh-issue-sync push` can create a milestone from issue frontmatter, but without a due date — prefer explicit creation above.

After creating or updating milestones, refresh local cache:

```bash
gh-issue-sync pull --all
```

Include milestone commands in the report. Do not run create/update commands unless the user asks (same as issue push).

### 3. Parse RFC → operations list

Read the RFC against [`docs/rfc-template.md`](../../../docs/rfc-template.md) section layout. For each `###` item under release sections, classify:

| RFC pattern                                              | Operation                                                             |
| -------------------------------------------------------- | --------------------------------------------------------------------- |
| `### [Title](…/issues/N)`                                | **Update** / **Reschedule** `#N`                                      |
| `### Title` (no link)                                    | **Create** (match title against `.issues/` first — may already exist) |
| Rename / move instructions on a linked item              | **Update** title / **Reschedule** milestone                           |
| `## Proposed roadmap items to close`                     | **Close**                                                             |
| Previous-release row: Done + "follow-ups on the roadmap" | Flag — follow-up is usually a separate RFC item                       |

Extract per item: title, `Size:` from RFC (or `TBC`), `Strategic theme:` from RFC (or `TBC`), target milestone from the section (`vX.Y` or `Future`), body content below the heading.

Cross-check release dates with `.issues/.sync/milestones.json` and the [release schedule](https://github.com/wagtail/wagtail/wiki/Release-schedule).

Diff against synced local files; skip items that already match.

### 4. Draft issue files

Structure and tone: [`docs/item-template.md`](../../../docs/item-template.md), [`docs/style-guide.md`](../../../docs/style-guide.md). Labels: [`.github/labels.json`](../../../.github/labels.json) only.

Frontmatter mapping (see [`gh-issue-sync` skill](~/.agents/skills/gh-issue-sync/SKILL.md)):

| Item template     | Issue frontmatter | Set on project after push |
| ----------------- | ----------------- | ------------------------- |
| `title`           | `title`           | —                         |
| `labels`          | `labels`          | —                         |
| `strategic_theme` | —                 | `Strategic theme`         |
| `release`         | `milestone`       | `Status`                  |
| `size`            | —                 | `Size`                    |

Always set `projects: [Wagtail public roadmap]`. Derive `Status`, `Start date`, and `Target date` from milestone metadata per [CONTRIBUTING](../../../docs/CONTRIBUTING.md).

**Creates** — `gh-issue-sync new "Title" --edit` or write `.issues/open/T…-slug.md` (temp ID prefix required).

**Updates** — edit `.issues/open/<N>-*.md`; patch only what the RFC changes.

**Closes** — `gh-issue-sync close <N> --reason completed|not_planned`.

**Comments on push** — `.issues/open/<N>.comment.md` ([`gh-issue-sync` skill](~/.agents/skills/gh-issue-sync/SKILL.md)).

Review with `gh-issue-sync status`, `gh-issue-sync diff <N>`, `gh-issue-sync push --dry-run`. Do not push unless the user asks.

### 5. Plan project field updates

After push, new items appear on [project 16](https://github.com/orgs/wagtail/projects/16). Look up item and field IDs at runtime:

```bash
gh project item-list 16 --owner wagtail --format json --limit 300
gh project field-list 16 --owner wagtail --format json
gh project item-edit --id <item-id> --project-id <project-id> --field-id <field-id> ...
```

One field per `item-edit` invocation. Plan commands in the report; run after push when real issue numbers exist.

### 6. Report

List milestone commands, created/edited file paths, the operations table, dry-run output, pending project field commands, and suggested next steps: milestones → review → push → project fields → verify board → update wagtail.org.
