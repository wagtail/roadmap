# Triage assessment JSON schema

Each triaged idea is stored as one JSON file in the cache (`.issues/triage-cache/<id>__<key>.json`). The report generator reads these; the fields below are what it consumes. Produce this per idea — it is the machine-readable form of the qualitative assessment the [`triage-roadmap-ideas`](../../triage-roadmap-ideas/SKILL.md) skill writes as prose.

| Field              | Type                                                           | Notes                                                                                                                                                          |
| ------------------ | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`               | string                                                         | Issue number for existing roadmap items (e.g. `"36"`); a short kebab slug for new ideas.                                                                       |
| `type`             | `"issue"` \| `"idea"`                                          | Existing roadmap item vs a new proposal.                                                                                                                       |
| `title`            | string                                                         | Short title.                                                                                                                                                   |
| `url`              | string \| null                                                 | `https://github.com/wagtail/roadmap/issues/<N>` for issues; `null` for new ideas. Drives the clickable point/link.                                             |
| `classification`   | `"pillar"` \| `"enabler"` \| `"maintenance"` \| `"management"` | Stage 0.                                                                                                                                                       |
| `routed_out`       | boolean                                                        | `true` for maintenance / management / small-enhancement items routed out at Stage 0. Routed-out items are listed in a table, not plotted.                      |
| `primary_pillar`   | string                                                         | **Must match a palette category exactly** (emoji + name), e.g. `"🏔️ Future-ready content management"`, `"🏗️ Enabling capabilities"`, `"Other"`. Drives colour. |
| `gates`            | object                                                         | Optional record: `{ "g1": "pass"\|"blocked", "g1_marks": {…}, "g2": "core"\|"package", "g3": "pass"\|"concern" }`.                                             |
| `scores`           | object                                                         | The six 1–5 criterion scores: `strategic_fit`, `differentiator`, `demand`, `sponsorship`, `deliverability`, `maintenance`.                                     |
| `per_pillar_fit`   | object                                                         | Optional: per-pillar strategic-fit scores, e.g. `{"🏔️": 4, "🪢": 2, ...}`.                                                                                     |
| `weighted_overall` | number                                                         | Σ(score × weight), out of 5. Ranks the table.                                                                                                                  |
| `strategic_value`  | number                                                         | **Y axis** = mean(strategic_fit, differentiator, demand).                                                                                                      |
| `viability`        | number                                                         | **X axis** = mean(sponsorship, deliverability, maintenance).                                                                                                   |
| `effort`           | `"XS"`\|`"S"`\|`"M"`\|`"L"`\|`"XL"`                            | Bubble size.                                                                                                                                                   |
| `decision`         | `"schedule"`\|`"seek_sponsor"`\|`"park"`\|`"decline"`          |                                                                                                                                                                |
| `review_date`      | string                                                         | `YYYY-MM-DD`.                                                                                                                                                  |
| `rationale`        | string                                                         | One-paragraph rationale (shown in the tooltip/details panel).                                                                                                  |
| `key_assumption`   | string                                                         | The single thing most likely to change the score.                                                                                                              |
| `related_items`    | array                                                          | Optional: `[{ "number": 19, "title": "…", "relation": "precursor" }]`.                                                                                         |
| `labels`           | array                                                          | 2–3 real labels from `.github/labels.json`.                                                                                                                    |
| `assessed_at`      | string                                                         | ISO timestamp; the report keeps the most recent record per `id`.                                                                                               |

Routed-out items may omit `scores`, `weighted_overall`, `strategic_value`, `viability`, `effort` — they still need `id`, `title`, `classification`, `routed_out: true`, `decision`, and a `rationale`.

## Minimal example (scored pillar item)

```json
{
  "id": "36",
  "type": "issue",
  "title": "Accessibility checker enhancements",
  "url": "https://github.com/wagtail/roadmap/issues/36",
  "classification": "pillar",
  "routed_out": false,
  "primary_pillar": "🏔️ Future-ready content management",
  "scores": {
    "strategic_fit": 4,
    "differentiator": 4,
    "demand": 4,
    "sponsorship": 3,
    "deliverability": 4,
    "maintenance": 4
  },
  "per_pillar_fit": { "🏔️": 4, "🪢": 2, "🛠️": 2, "🌳": 1 },
  "weighted_overall": 3.85,
  "strategic_value": 4.0,
  "viability": 3.7,
  "effort": "M",
  "decision": "schedule",
  "review_date": "2026-08-01",
  "rationale": "Accessibility is a named differentiator and a genuine adoption gate for core target sectors.",
  "key_assumption": "Whether the editor-integration stretch stays in scope or splits out.",
  "related_items": [
    {
      "number": 19,
      "title": "Built-in accessibility checker",
      "relation": "precursor"
    }
  ],
  "labels": ["accessibility", "UX"],
  "assessed_at": "2026-07-02T10:00:00Z"
}
```

## Example (routed-out item)

```json
{
  "id": "161",
  "type": "issue",
  "title": "include_block template tag",
  "url": "https://github.com/wagtail/roadmap/issues/161",
  "classification": "maintenance",
  "routed_out": true,
  "primary_pillar": "Other",
  "decision": "decline",
  "rationale": "Small, well-bounded template-tag DX enhancement — ship in the normal contribution flow, not a roadmap item.",
  "labels": ["DX"],
  "assessed_at": "2026-07-02T10:00:00Z"
}
```
