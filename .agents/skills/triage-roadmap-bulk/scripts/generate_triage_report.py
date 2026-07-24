#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Collect triage assessments and render an accessible HTML report.

Two subcommands:

  plan    Given roadmap issue files (and the current skill + selection criteria),
          compute a content-addressed cache key per item and report which items
          already have a cached assessment (hit) and which need one (miss).
          The skill uses this to skip re-scoring unchanged items.

  report  Read assessment JSON files (from the cache and/or explicit paths),
          dedupe by id, and write a single self-contained HTML report with an
          Observable Plot scatter (strategic value x viability, bubble = effort,
          colour = strategic theme) plus an accessible data table.

The cache key folds in the SKILL.md and selection-criteria.md contents, so any
change to the skill or the rubric invalidates every cached score automatically —
that is what lets us safely reuse scores "when the skill and criteria are the same".

Pure standard library: run directly via the uv shebang, no install step.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

# --- Strategic-theme palette (categories match the assessment `primary_pillar`) ---
PALETTE = [
    {
        "category": "🏔️ Future-ready content management",
        "color": "rgb(9, 105, 218)",
        "colorBg": "rgb(221, 244, 255)",
    },
    {
        "category": "🪢 Deep integrations and customizations",
        "color": "rgb(191, 57, 137)",
        "colorBg": "rgb(255, 239, 247)",
    },
    {
        "category": "🛠️ DX for humans with AI",
        "color": "rgb(130, 80, 223)",
        "colorBg": "rgb(251, 239, 255)",
    },
    {
        "category": "🌳 How we build Wagtail",
        "color": "rgb(31, 136, 61)",
        "colorBg": "rgb(218, 251, 225)",
    },
    {
        "category": "🏗️ Enabling capabilities",
        "color": "rgb(188, 76, 0)",
        "colorBg": "rgb(255, 241, 229)",
    },
    {
        "category": "🪴 Maintenance",
        "color": "rgb(154, 103, 0)",
        "colorBg": "rgb(255, 248, 197)",
    },
    {"category": "Other", "color": "rgb(89, 99, 110)", "colorBg": "rgb(246, 248, 250)"},
]
PALETTE_BY_CATEGORY = {p["category"]: p for p in PALETTE}

# Effort -> bubble radius in px (identity r scale in Plot).
EFFORT_RADIUS = {"XS": 5, "S": 7, "M": 10, "L": 14, "XL": 18}

DECISION_LABELS = {
    "schedule": "Schedule",
    "seek_sponsor": "Seek sponsor",
    "park": "Park",
    "decline": "Decline",
}

REPO = "wagtail/roadmap"
DEFAULT_CACHE = ".issues/triage-cache"
DEFAULT_SKILL = ".agents/skills/triage-roadmap-bulk/SKILL.md"
DEFAULT_CRITERIA = "docs/selection-criteria.md"


# --------------------------------------------------------------------------- #
# Hashing / cache keys
# --------------------------------------------------------------------------- #
def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def issue_id(path: Path) -> str:
    m = re.match(r"(\d+)", path.name)
    return m.group(1) if m else path.stem


def parse_issue(path: Path) -> dict:
    """Extract the substantive content of a synced .issues/*.md file.

    Only the title + labels + body are hashed, so volatile frontmatter such as
    `synced_at` never spuriously invalidates a cached score.
    """
    raw = path.read_text(encoding="utf-8")
    title, labels, body = "", [], raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) == 3:
            front, body = parts[1], parts[2]
            tm = re.search(r"^title:\s*(.+)$", front, re.MULTILINE)
            if tm:
                title = tm.group(1).strip().strip("\"'")
            labels = re.findall(r"^\s*-\s*(.+)$", _labels_block(front), re.MULTILINE)
    if not title:
        hm = re.search(r"^#+\s*(.+)$", body, re.MULTILINE)
        title = hm.group(1).strip() if hm else path.stem
    return {
        "id": issue_id(path),
        "title": title,
        "labels": [lab.strip().strip("\"'") for lab in labels],
        "body": body.strip(),
        "url": f"https://github.com/{REPO}/issues/{issue_id(path)}",
    }


def _labels_block(front: str) -> str:
    """Return just the `labels:` list block from frontmatter (best-effort)."""
    m = re.search(r"^labels:\s*\n((?:\s*-\s*.+\n)+)", front, re.MULTILINE)
    return m.group(1) if m else ""


def cache_key(skill_hash: str, criteria_hash: str, item: dict) -> str:
    substance = f"{item['title']}\n{sorted(item['labels'])}\n{item['body']}"
    return sha(f"{skill_hash}\n{criteria_hash}\n{substance}")


def cache_path(cache_dir: Path, item_id: str, key: str) -> Path:
    return cache_dir / f"{item_id}__{key[:12]}.json"


# --------------------------------------------------------------------------- #
# plan
# --------------------------------------------------------------------------- #
def cmd_plan(args: argparse.Namespace) -> int:
    skill_hash = sha(Path(args.skill).read_text(encoding="utf-8"))
    criteria_hash = sha(Path(args.criteria).read_text(encoding="utf-8"))
    cache_dir = Path(args.cache_dir)
    ids = set(args.ids.split(",")) if args.ids else None

    issue_files = sorted(Path(args.issues_dir).glob("*.md"))
    plan = []
    for path in issue_files:
        item = parse_issue(path)
        if ids and item["id"] not in ids:
            continue
        key = cache_key(skill_hash, criteria_hash, item)
        cp = cache_path(cache_dir, item["id"], key)
        plan.append(
            {
                "id": item["id"],
                "title": item["title"],
                "url": item["url"],
                "source": str(path),
                "cache_key": key,
                "cache_path": str(cp),
                "status": "hit" if cp.exists() else "miss",
            }
        )

    hits = [p for p in plan if p["status"] == "hit"]
    misses = [p for p in plan if p["status"] == "miss"]
    result = {
        "skill_hash": skill_hash[:12],
        "criteria_hash": criteria_hash[:12],
        "cache_dir": str(cache_dir),
        "total": len(plan),
        "hits": len(hits),
        "misses": len(misses),
        "items": plan,
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(
            f"skill {result['skill_hash']} · criteria {result['criteria_hash']} · cache {cache_dir}/"
        )
        print(
            f"{len(plan)} items — {len(hits)} cached (reuse), {len(misses)} to assess\n"
        )
        for p in plan:
            mark = "✓ reuse" if p["status"] == "hit" else "· assess"
            print(f"  {mark}  #{p['id']:<4} {p['title']}")
            if p["status"] == "miss":
                print(f"            write -> {p['cache_path']}")
    return 0


# --------------------------------------------------------------------------- #
# report
# --------------------------------------------------------------------------- #
def load_assessments(
    inputs: list[Path], cache_dir: Path, ids: set[str] | None
) -> list[dict]:
    files: list[Path] = []
    for p in inputs or [cache_dir]:
        if p.is_dir():
            files.extend(sorted(p.glob("*.json")))
        elif p.exists():
            files.append(p)
    by_id: dict[str, dict] = {}
    for f in files:
        try:
            a = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            print(f"warning: skipping {f}: {e}", file=sys.stderr)
            continue
        aid = str(a.get("id", f.stem))
        if ids and aid not in ids:
            continue
        # Keep the most recently assessed record per id.
        prev = by_id.get(aid)
        if prev is None or a.get("assessed_at", "") >= prev.get("assessed_at", ""):
            by_id[aid] = a
    return list(by_id.values())


def enrich(a: dict) -> dict:
    """Fill derived/display fields and guard against missing values."""
    a = dict(a)
    pillar = a.get("primary_pillar") or "Other"
    pal = PALETTE_BY_CATEGORY.get(pillar, PALETTE_BY_CATEGORY["Other"])
    a["color"] = pal["color"]
    a["colorBg"] = pal["colorBg"]
    a["radius"] = EFFORT_RADIUS.get((a.get("effort") or "M").upper(), 10)
    a["decision_label"] = DECISION_LABELS.get(
        a.get("decision", ""), a.get("decision", "—")
    )
    a["short_label"] = a.get("short_label") or (
        f"#{a['id']}" if a.get("type") == "issue" else _short(a.get("title", ""))
    )
    a["routed_out"] = bool(a.get("routed_out"))
    return a


def _short(title: str, n: int = 22) -> str:
    return title if len(title) <= n else title[: n - 1] + "…"


def cmd_report(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir)
    ids = set(args.ids.split(",")) if args.ids else None
    inputs = [Path(p) for p in args.inputs] if args.inputs else []
    assessments = [enrich(a) for a in load_assessments(inputs, cache_dir, ids)]
    if not assessments:
        print(
            "No assessments found. Run the skill first (writes JSON into the cache).",
            file=sys.stderr,
        )
        return 1

    scored = [
        a
        for a in assessments
        if not a["routed_out"] and a.get("strategic_value") is not None
    ]
    routed = [
        a for a in assessments if a["routed_out"] or a.get("strategic_value") is None
    ]
    scored.sort(key=lambda a: a.get("weighted_overall", 0), reverse=True)
    routed.sort(key=lambda a: a.get("title", ""))

    html = render_html(scored, routed, title=args.title)
    out = Path(args.out)
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out}  ({len(scored)} scored, {len(routed)} routed out)")
    if args.open:
        webbrowser.open(out.resolve().as_uri())
    return 0


# --------------------------------------------------------------------------- #
# HTML rendering
# --------------------------------------------------------------------------- #
def esc(s) -> str:
    from html import escape

    return escape(str(s if s is not None else ""))


def stat_cards(scored: list[dict], routed: list[dict]) -> str:
    from collections import Counter

    dec = Counter(a.get("decision") for a in scored)
    mean = (
        sum(a.get("weighted_overall", 0) for a in scored) / len(scored) if scored else 0
    )
    cards = [
        ("Scored items", len(scored)),
        ("Mean score", f"{mean:.2f} / 5"),
        ("Schedule", dec.get("schedule", 0)),
        ("Seek sponsor", dec.get("seek_sponsor", 0)),
        ("Park / decline", dec.get("park", 0) + dec.get("decline", 0)),
        ("Routed out", len(routed)),
    ]
    return "".join(
        f'<div class="card"><span class="card-n">{esc(v)}</span>'
        f'<span class="card-l">{esc(label)}</span></div>'
        for label, v in cards
    )


def legend() -> str:
    items = "".join(
        f'<li><span class="swatch" style="background:{p["color"]}"></span>{esc(p["category"])}</li>'
        for p in PALETTE
    )
    return f'<ul class="legend" aria-label="Strategic theme colours">{items}</ul>'


def table_rows(scored: list[dict]) -> str:
    rows = []
    for a in scored:
        title = esc(a.get("title", ""))
        if a.get("url"):
            title_cell = f'<a href="{esc(a["url"])}">{title} ↗</a>'
        else:
            title_cell = f'{title} <span class="badge">new idea</span>'
        chip = (
            f'<span class="chip" style="background:{a["colorBg"]};color:{a["color"]}">'
            f"{esc(a.get('primary_pillar', 'Other'))}</span>"
        )
        rows.append(
            "<tr>"
            f"<td>{title_cell}</td>"
            f"<td>{esc(a.get('classification', '—'))}</td>"
            f"<td>{chip}</td>"
            f'<td class="num" data-sort="{a.get("weighted_overall", 0)}">{a.get("weighted_overall", 0):.2f}</td>'
            f'<td class="num" data-sort="{a.get("strategic_value", 0)}">{a.get("strategic_value", 0):.1f}</td>'
            f'<td class="num" data-sort="{a.get("viability", 0)}">{a.get("viability", 0):.1f}</td>'
            f"<td>{esc(a.get('effort', '—'))}</td>"
            f"<td>{esc(a.get('decision_label', '—'))}</td>"
            f"<td>{esc(a.get('review_date', '—'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def routed_rows(routed: list[dict]) -> str:
    if not routed:
        return '<tr><td colspan="3" class="muted">None.</td></tr>'
    out = []
    for a in routed:
        title = esc(a.get("title", ""))
        title_cell = (
            f'<a href="{esc(a["url"])}">{title} ↗</a>' if a.get("url") else title
        )
        out.append(
            f"<tr><td>{title_cell}</td>"
            f"<td>{esc(a.get('classification', '—'))}</td>"
            f"<td>{esc(a.get('rationale') or a.get('decision_label', '—'))}</td></tr>"
        )
    return "\n".join(out)


def render_html(scored: list[dict], routed: list[dict], title: str) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    # Only the fields the chart/tooltip need, keeps the payload lean.
    chart_data = [
        {
            "id": a.get("id"),
            "title": a.get("title"),
            "short_label": a.get("short_label"),
            "url": a.get("url"),
            "primary_pillar": a.get("primary_pillar", "Other"),
            "color": a.get("color"),
            "colorBg": a.get("colorBg"),
            "strategic_value": a.get("strategic_value"),
            "viability": a.get("viability"),
            "radius": a.get("radius"),
            "effort": a.get("effort"),
            "weighted_overall": a.get("weighted_overall"),
            "classification": a.get("classification"),
            "decision_label": a.get("decision_label"),
            "review_date": a.get("review_date"),
            "rationale": a.get("rationale"),
            "key_assumption": a.get("key_assumption"),
        }
        for a in scored
    ]
    data_json = json.dumps(chart_data, ensure_ascii=False)

    return TEMPLATE.format(
        title=esc(title),
        generated=esc(generated),
        n_scored=len(scored),
        n_routed=len(routed),
        cards=stat_cards(scored, routed),
        legend=legend(),
        table_rows=table_rows(scored),
        routed_rows=routed_rows(routed),
        data_json=data_json,
    )


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{
    --fg: #1f2328; --muted: #59636e; --line: #d1d9e0; --bg: #ffffff;
    --accent: rgb(9,105,218);
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; color: var(--fg); background: var(--bg);
    font: 16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
  .wrap {{ max-width: 1080px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }}
  h1 {{ font-size: 1.6rem; margin: 0 0 .25rem; }}
  .sub {{ color: var(--muted); margin: 0 0 1.5rem; }}
  .sub a {{ color: var(--accent); }}
  a {{ color: var(--accent); }}
  .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: .75rem; margin-bottom: 1.5rem; }}
  .card {{ border: 1px solid var(--line); border-radius: 10px; padding: .8rem 1rem; }}
  .card-n {{ display: block; font-size: 1.5rem; font-weight: 650; }}
  .card-l {{ display: block; color: var(--muted); font-size: .85rem; }}
  .panel {{ display: grid; grid-template-columns: 2fr 1fr; gap: 1.25rem; align-items: start; }}
  @media (max-width: 800px) {{ .panel {{ grid-template-columns: 1fr; }} }}
  figure {{ margin: 0; border: 1px solid var(--line); border-radius: 10px; padding: 1rem; overflow-x: auto; }}
  figcaption {{ color: var(--muted); font-size: .85rem; margin-top: .5rem; }}
  #details {{ border: 1px solid var(--line); border-radius: 10px; padding: 1rem; min-height: 200px; }}
  #details h2 {{ font-size: 1rem; margin: 0 0 .5rem; }}
  #details dl {{ display: grid; grid-template-columns: auto 1fr; gap: .2rem .6rem; margin: .5rem 0; font-size: .9rem; }}
  #details dt {{ color: var(--muted); }}
  #details .cta {{ display: inline-block; margin-top: .6rem; font-weight: 600; }}
  .legend {{ list-style: none; display: flex; flex-wrap: wrap; gap: .4rem 1rem; padding: 0; margin: 1rem 0 0;
    font-size: .82rem; color: var(--muted); }}
  .legend li {{ display: flex; align-items: center; gap: .35rem; }}
  .swatch {{ width: .8rem; height: .8rem; border-radius: 50%; display: inline-block; }}
  section {{ margin-top: 2.5rem; }}
  h2.sec {{ font-size: 1.15rem; border-bottom: 1px solid var(--line); padding-bottom: .35rem; }}
  table {{ width: 100%; border-collapse: collapse; font-size: .9rem; }}
  th, td {{ text-align: left; padding: .5rem .6rem; border-bottom: 1px solid var(--line); vertical-align: top; }}
  th {{ color: var(--muted); font-weight: 600; }}
  th[aria-sort] {{ cursor: pointer; }}
  th.sortable::after {{ content: " ↕"; color: var(--line); }}
  th[aria-sort="ascending"]::after {{ content: " ↑"; color: var(--fg); }}
  th[aria-sort="descending"]::after {{ content: " ↓"; color: var(--fg); }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  .chip {{ display: inline-block; padding: .1rem .5rem; border-radius: 999px; font-size: .8rem; white-space: nowrap; }}
  .badge {{ font-size: .7rem; color: var(--muted); border: 1px solid var(--line); border-radius: 4px; padding: 0 .3rem; }}
  .muted {{ color: var(--muted); }}
  :focus-visible {{ outline: 3px solid rgba(9,105,218,.4); outline-offset: 2px; }}
  circle {{ cursor: pointer; }}
  .skip {{ position: absolute; left: -9999px; }}
  .skip:focus {{ position: static; }}
</style>
</head>
<body>
<a class="skip" href="#table">Skip to data table</a>
<div class="wrap">
  <header>
    <h1>{title}</h1>
    <p class="sub">{n_scored} scored, {n_routed} routed out · generated {generated} ·
      method: <a href="../../../docs/selection-criteria.md">selection-criteria.md</a></p>
  </header>

  <div class="cards">{cards}</div>

  <div class="panel">
    <figure>
      <div id="chart" role="img"
           aria-label="Scatter plot of roadmap ideas by strategic value (vertical) and viability (horizontal); bubble size is effort and colour is strategic theme. Full data in the table below."></div>
      {legend}
      <figcaption>Bubble size = effort (XS–XL). Hover or focus a point for details; click a point to open its roadmap issue. Dashed lines mark the score midpoint (3/5).</figcaption>
    </figure>
    <aside id="details" aria-live="polite">
      <h2>Details</h2>
      <p class="muted">Hover, focus, or click a point to see its assessment here.</p>
    </aside>
  </div>

  <section id="table">
    <h2 class="sec">Scored items</h2>
    <table>
      <thead><tr>
        <th scope="col">Idea</th><th scope="col">Class</th><th scope="col">Theme</th>
        <th scope="col" class="sortable num" aria-sort="descending" data-key="3">Score</th>
        <th scope="col" class="sortable num" data-key="4">Strat. value</th>
        <th scope="col" class="sortable num" data-key="5">Viability</th>
        <th scope="col">Effort</th><th scope="col">Decision</th><th scope="col">Review</th>
      </tr></thead>
      <tbody>{table_rows}</tbody>
    </table>
  </section>

  <section>
    <h2 class="sec">Routed out at Stage 0</h2>
    <table>
      <thead><tr><th scope="col">Idea</th><th scope="col">Class</th><th scope="col">Note</th></tr></thead>
      <tbody>{routed_rows}</tbody>
    </table>
  </section>
</div>

<script type="module">
import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";

const data = {data_json};
const details = document.querySelector("#details");

function showDetails(d) {{
  const link = d.url
    ? `<a class="cta" href="${{d.url}}">View on the roadmap ↗</a>`
    : `<p class="muted">New idea — not yet a roadmap issue.</p>`;
  details.innerHTML = `
    <h2>${{d.title ?? ""}}</h2>
    <dl>
      <dt>Theme</dt><dd>${{d.primary_pillar ?? "—"}}</dd>
      <dt>Class</dt><dd>${{d.classification ?? "—"}}</dd>
      <dt>Score</dt><dd>${{(d.weighted_overall ?? 0).toFixed(2)}} / 5</dd>
      <dt>Strat. value</dt><dd>${{(d.strategic_value ?? 0).toFixed(1)}}</dd>
      <dt>Viability</dt><dd>${{(d.viability ?? 0).toFixed(1)}}</dd>
      <dt>Effort</dt><dd>${{d.effort ?? "—"}}</dd>
      <dt>Decision</dt><dd>${{d.decision_label ?? "—"}}${{d.review_date ? " · review " + d.review_date : ""}}</dd>
    </dl>
    ${{d.rationale ? `<p>${{d.rationale}}</p>` : ""}}
    ${{d.key_assumption ? `<p class="muted"><strong>Key assumption:</strong> ${{d.key_assumption}}</p>` : ""}}
    ${{link}}`;
}}

const plot = Plot.plot({{
  width: 640, height: 520, marginLeft: 56, marginBottom: 46, marginRight: 20,
  style: {{ fontSize: "12px", background: "transparent" }},
  x: {{ domain: [1, 5], label: "Viability →", grid: true, ticks: 5 }},
  y: {{ domain: [1, 5], label: "↑ Strategic value", grid: true, ticks: 5 }},
  r: {{ type: "identity" }},
  marks: [
    Plot.ruleX([3], {{ stroke: "#d1d9e0", strokeDasharray: "4 4" }}),
    Plot.ruleY([3], {{ stroke: "#d1d9e0", strokeDasharray: "4 4" }}),
    Plot.text([
      {{ x: 4.9, y: 4.9, t: "Schedule now" }},
      {{ x: 1.1, y: 4.9, t: "Find a sponsor" }},
      {{ x: 1.1, y: 1.1, t: "Decline / park" }},
      {{ x: 4.9, y: 1.1, t: "Opportunistic" }},
    ], {{ x: "x", y: "y", text: "t", fill: "#8b949e", fontSize: 11,
          textAnchor: d => d.x > 3 ? "end" : "start" }}),
    Plot.dot(data, {{
      x: "viability", y: "strategic_value", r: "radius",
      fill: "color", stroke: "white", strokeWidth: 1.5,
      href: "url", target: "_blank",
      title: d => `${{d.title}}\\n${{d.primary_pillar}}\\nscore ${{(d.weighted_overall ?? 0).toFixed(2)}} · effort ${{d.effort ?? "—"}}`,
    }}),
    Plot.text(data, {{
      x: "viability", y: "strategic_value", text: "short_label",
      dy: d => -(d.radius) - 6, fontSize: 10, fill: "#59636e",
    }}),
  ],
}});

document.querySelector("#chart").append(plot);

// Plot.dot renders one <circle> per datum in data order, so index mapping is
// exact. With href set, Plot wraps each dot in an <a>, which is the focusable,
// clickable element — bind interactions there when present, else the circle.
[...plot.querySelectorAll("circle")].forEach((c, i) => {{
  const d = data[i];
  if (!d) return;
  const el = c.closest("a") || c;
  const show = () => showDetails(d);
  el.addEventListener("mouseenter", show);
  el.addEventListener("focus", show);
  if (!el.closest("a")) {{
    // New-idea points have no link; keep them focusable and labelled.
    el.setAttribute("tabindex", "0");
    el.setAttribute("role", "img");
  }}
  el.setAttribute("aria-label",
    `${{d.title}}, score ${{(d.weighted_overall ?? 0).toFixed(2)}} of 5, ${{d.decision_label ?? ""}}.` +
    (d.url ? " Activate to open the roadmap issue." : ""));
}});

// Lightweight column sorting for the numeric columns.
const table = document.querySelector("#table table");
table.querySelectorAll("th.sortable").forEach(th => {{
  th.addEventListener("click", () => {{
    const tbody = table.tBodies[0];
    const idx = +th.dataset.key;
    const asc = th.getAttribute("aria-sort") !== "ascending";
    table.querySelectorAll("th").forEach(h => h.removeAttribute("aria-sort"));
    th.setAttribute("aria-sort", asc ? "ascending" : "descending");
    [...tbody.rows].sort((a, b) => {{
      const av = +a.cells[idx].dataset.sort, bv = +b.cells[idx].dataset.sort;
      return asc ? av - bv : bv - av;
    }}).forEach(r => tbody.append(r));
  }});
}});
</script>
</body>
</html>
"""


# --------------------------------------------------------------------------- #
def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("plan", help="report cache hits/misses for roadmap issues")
    p.add_argument("--issues-dir", default=".issues/open")
    p.add_argument("--ids", help="comma-separated issue numbers to limit to")
    p.add_argument("--cache-dir", default=DEFAULT_CACHE)
    p.add_argument("--skill", default=DEFAULT_SKILL)
    p.add_argument("--criteria", default=DEFAULT_CRITERIA)
    p.add_argument("--json", action="store_true", help="emit the plan as JSON")
    p.set_defaults(func=cmd_plan)

    r = sub.add_parser("report", help="render the HTML report from cached assessments")
    r.add_argument(
        "inputs", nargs="*", help="assessment JSON files or dirs (default: cache dir)"
    )
    r.add_argument("--cache-dir", default=DEFAULT_CACHE)
    r.add_argument("--ids", help="comma-separated ids to include")
    r.add_argument("--out", default="triage-report.html")
    r.add_argument("--title", default="Wagtail roadmap triage")
    r.add_argument("--open", action="store_true", help="open the report in a browser")
    r.set_defaults(func=cmd_report)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
