---
name: draft-roadmap-rfc
description: Write a draft RFC for roadmap updates to Wagtail
license: MIT
metadata:
  audience: maintainers
  # Hide the skill from discovery: https://github.com/vercel-labs/skills#optional-fields
  internal: true
  disable-model-invocation: true
---

## Overview

Draft a new "Public roadmap updates" RFC, following the structure of past RFCs in the [`wagtail/rfcs`](https://github.com/wagtail/rfcs) repository (label: [`roadmap`](https://github.com/wagtail/rfcs/pulls?q=is%3Apr+label%3Aroadmap)). The output is a new Markdown file in the root of the [`wagtail/roadmap`](https://github.com/wagtail/roadmap) repository that follows [`docs/rfc-template.md`](../../../docs/rfc-template.md), populated from the previous RFC, the corresponding Wagtail release notes, and the current state of roadmap issues / project board.

## Methodology

### Goals

- Produce a draft RFC that mirrors the structure and tone of past roadmap RFCs.
- Pull factual content (issues, sizes, milestones, statuses) from the canonical sources rather than inventing it.
- Use the [roadmap style guide](../../../docs/style-guide.md): conversational-instructional, link-rich, comfortable hedging.
- Leave parts of the document marked `TBC` when the input data does not support a confident draft, rather than guessing.

### Guardrails

- Never invent issue numbers, sizes, milestones, or release dates — fetch them.
- Always link to roadmap issues by their full URL (e.g. `https://github.com/wagtail/roadmap/issues/116`).
- Don't rephrase existing roadmap item summaries — copy them as-is from the issue body unless the user asks otherwise.
- Don't propose anything for sections marked `TBC` (next+1, Future, items to close, items that didn't make the cut). The user will fill those in.
- Don't open a PR or push commits. The skill ends with a file on disk for the user to review.

### Inputs

To detect from the context or request from the user if unclear:

- **Author name** for the RFC frontmatter. Default: read `git config user.name`.
- **RFC date** in `YYYY-MM-DD` for the `Created` / `Last Modified` fields. Default: today.
- **Previous roadmap RFC**. Default: most recent merged or open PR with the `roadmap` label in `wagtail/rfcs`. Resolve to its raw `text/NNN-roadmap-updates.md` file on the `main` branch (or the PR head ref if not yet merged).
- **New RFC number**. Default: `latest wagtail/roadmap PR / issue number + 1`. The user may have already created an empty `rfc-NNN.md` placeholder in the repo root — prefer that filename if present.
- **Output file path**. Default: `rfc-<NNN>.md` in the repo root. Reuse an empty placeholder if it exists.

### Reference data sources

Always fetch the latest data from these sources rather than relying on local caches.

- Previous RFC raw Markdown: `https://raw.githubusercontent.com/wagtail/rfcs/refs/heads/main/text/<NNN>-roadmap-updates.md`
- Wagtail release notes (Markdown view): `https://docs.wagtail.org/en/latest/releases/<X.Y>.html.md`
- Wagtail release schedule: <https://github.com/wagtail/wagtail/wiki/Release-schedule>
- Roadmap repo issues: `https://github.com/wagtail/roadmap/issues` and the corresponding milestones.
- Roadmap GitHub Project (for the `Size` custom field): <https://github.com/orgs/wagtail/projects/16> ("Wagtail public roadmap").

If present, project-local data already synced via the [`gh-issue-sync`](../../../.issues) skill is the fastest source for issue titles, milestones, labels, and bodies:

- `.issues/open/*.md` and `.issues/closed/*.md` — synced issues with frontmatter (`title`, `labels`, `milestone`, `projects`, `state`).
- `.issues/.sync/milestones.json` — full list of milestones with state and due dates.

The local issue files do **not** include the project's `Size` custom field, so that has to come from `gh project item-list 16 --owner wagtail`.

### Reporting

- After writing the file, summarize what was filled in vs. left as `TBC`, and link to the inputs used (previous RFC URL, release notes URL, project URL).
- Flag any roadmap issues that were skipped (e.g. closed but not in last release, missing size, ambiguous milestone) so the user can decide what to do.
- Don't invent a title — keep it `RFC <NNN>: Public roadmap updates` to match the series.

## Steps

### 1. Determine versions and the previous RFC

- [ ] Identify the previous roadmap RFC. Run:

  ```bash
  gh pr list --repo wagtail/rfcs --label roadmap --state all --limit 5 \
    --json number,title,state,headRefName,mergedAt,url
  ```

  Pick the most recent one (highest RFC number / most recent `mergedAt`).

- [ ] Fetch its raw Markdown from `https://raw.githubusercontent.com/wagtail/rfcs/refs/heads/main/text/<NNN>-roadmap-updates.md`. If that 404s (PR not merged yet), fall back to the PR head: `https://raw.githubusercontent.com/wagtail/rfcs/<headRefName>/text/<NNN>-roadmap-updates.md`.
- [ ] Extract from the previous RFC:
  - The "next release" version (e.g. `v7.4`) → this becomes the **previous release** in the new RFC.
  - The "next+1" version (e.g. `v7.5*`) → this becomes the **next release** in the new RFC.
  - The list of items in "Roadmap for the next release" — use these as the rows of the **previous release** status table.
- [ ] Compute the new RFC's "next release" version: increment the minor of the previous "next release" by 1. So if the previous RFC's next release was `v7.4`, the new RFC's next release is `v7.5`.
- [ ] Confirm the release month/year using `.issues/.sync/milestones.json` (`due_on`) and the Wagtail [release schedule](https://github.com/wagtail/wagtail/wiki/Release-schedule). Wagtail ships in Feb / May / Aug / Nov. Format as `Month YYYY` (e.g. `August 2026`).
- [ ] Decide the new RFC number. Default: `previous RFC number + 2`. If the user has already created an empty `rfc-<NNN>.md` placeholder, use that number.

### 2. Pull the previous release's release notes

- [ ] Fetch the official release notes for the version that just shipped, from `https://docs.wagtail.org/en/latest/releases/<X.Y>.html.md`. (Use `latest` even after release; the release notes stay reachable.) If the page 404s, try `https://docs.wagtail.org/en/stable/releases/<X.Y>.html.md`.
- [ ] Skim the "What's new" headings and bug-fix list. For each item that was on the previous RFC's "next release" list:
  - If a matching feature heading appears in the release notes → status `Done`.
  - If only partial work appears (or only a related issue is referenced) → status `Partial` and add a brief note.
  - If the item does not appear at all → status `TBC` (do not assume "deferred"; the user will resolve it).

  These statuses go in the new RFC's "Roadmap for the previous release" table. Per the user's instructions, when in doubt prefer `TBC` over guessing.

### 3. Build the "Roadmap for the previous release" table

For each roadmap item that had milestone equal to the previous "next release" version (e.g. `v7.4`):

- [ ] Find the local file in `.issues/open/` or `.issues/closed/` whose frontmatter has `milestone: vX.Y`. Cross-check against the previous RFC's list of items so nothing is missed.
- [ ] Build a Markdown table with columns: `Roadmap item`, `Status`, `Notes`. Example row:

  ```markdown
  | [Customizable page explorer](https://github.com/wagtail/roadmap/issues/102) | Done | Follow-ups outside the roadmap |
  ```

  - Title is the issue title from frontmatter.
  - Issue link is `https://github.com/wagtail/roadmap/issues/<N>` where `<N>` is the leading number in the filename.
  - Status: prefer `TBC` unless the release notes give a clear signal (see step 2).
  - Notes: leave empty for `TBC` rows. For confidently `Done` rows, mirror the wording style of past RFCs ("Follow-ups outside the roadmap", "UX follow-ups on the roadmap", etc.) only if accurate.

### 4. Build the "Roadmap for the next release" sections

For each roadmap item with milestone equal to the new "next release" version (e.g. `v7.5`):

- [ ] List the local issue files via:

  ```bash
  rg -l "^milestone: vX\.Y$" .issues/open/
  ```

  (or read frontmatter directly from `.issues/open/*.md`).

- [ ] Get sizes from the GitHub project. Run once and reuse:

  ```bash
  gh project item-list 16 --owner wagtail --format json --limit 200 > /tmp/wagtail-roadmap-project.json
  ```

  Then for each issue, find the matching item by `content.number` and read the `Size` custom field (single-select, values `XS`/`S`/`M`/`L`/`XL`). If `Size` is missing, write `Size: TBC`.

- [ ] Also read the `Strategic theme` custom field for each item. If it is missing, write `Strategic theme: TBC`.
- [ ] For each item, write a section like:

  ```markdown
  ### [<Issue title>](https://github.com/wagtail/roadmap/issues/<N>)

  Size: <XS|S|M|L|XL|TBC>, Strategic theme: one of the options from the README.

  <Summary paragraph copied from the issue body — the lead paragraph above the first `##` heading.>
  ```

  Heading rules:
  - Items that already have a roadmap issue → heading is a link to the issue (mirrors `rfc-template.md`).
  - Items not yet tracked as a roadmap issue (rare for this skill, since we drive off issues) → plain heading, no link.

- [ ] Order items the same way they appear in the GitHub Project's roadmap view, or — if that is unclear — by issue number ascending. Don't sort by size.

### 5. Fill in the remaining sections as `TBC`

Per the user's instructions, the following sections are left for the user to refine. Don't generate content for them.

- [ ] `## Roadmap for the next+1 release` — body: `TBC`.
- [ ] `## Roadmap for "Future" releases` — body: `TBC`.
- [ ] `## Proposed roadmap items to close` — body: `TBC`.
- [ ] `## Items that didn't make the cut` — body: `TBC`.

Keep each heading from the template intact so the user can fill in directly without restructuring.

### 6. Assemble the document

- [ ] Use the template at [`docs/rfc-template.md`](../../../docs/rfc-template.md) as the structural baseline. Don't keep template HTML comments in the final draft.
- [ ] Frontmatter / header:

  ```markdown
  # RFC <NNN>: Public roadmap updates

  - RFC: <NNN>
  - Author: <author>
  - Created: <YYYY-MM-DD>
  - Last Modified: <YYYY-MM-DD>
  ```

- [ ] Abstract: copy the standard abstract used in `rfc-template.md` verbatim. It links to past RFCs and the release schedule.
- [ ] Version number section: phrase as `Provisional version number: v<X.Y> (minor release), in <Month YYYY> based on discussions to date.` Use `LTS` after the version only if the milestone metadata or release schedule says so; otherwise drop it.
- [ ] Roadmap for the previous release: the table from step 3, preceded by the line `Here is the status of roadmap items for the latest release, v<X.Y> (<Month YYYY>):`.
- [ ] Roadmap for the next release: the heading line `Proposed roadmap items for v<X.Y> (<Month YYYY>).`, followed by the per-item sections from step 4.
- [ ] Subsequent `TBC` sections from step 5.

### 7. Write the file and report

- [ ] Save to `rfc-<NNN>.md` in the repo root (overwrite if the user already created an empty placeholder).
- [ ] Lint the file by reading it back: every roadmap issue link should resolve to `https://github.com/wagtail/roadmap/issues/<N>`, and every section from the template should be present.
- [ ] Report to the user:
  - The path of the new file.
  - The previous RFC URL used as input.
  - The release notes URL used as input.
  - The list of items pulled into the "previous release" table (with their inferred status) and the "next release" sections (with their sizes and strategic themes).
  - Anything that was left as `TBC` and why.
  - Suggested next steps: review statuses, fill in the four `TBC` sections, then open a PR against `wagtail/rfcs` with the file renamed to `text/<NNN>-roadmap-updates.md`.
