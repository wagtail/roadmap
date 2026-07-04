# Wagtail roadmap triage & scoring methodology: DRAFT

🚧 Experimental! A consistent, lightweight way to assess proposed roadmap items against the [Wagtail product strategy](./product-strategy.md), producing both a qualitative assessment and a single weighted score, plus coordinates for visual comparison across items.

Scope: applies to substantial roadmap proposals and as needed to one-off enhancements. Not intended for bug fixes or small maintenance tasks.

---

## Stage 0: Classification

Before scoring, classify the item. Only **pillar work** and **enablers** go through the full scoring matrix.

| Category                  | Definition                                                                                    | Route                                                        |
| ------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Pillar work**           | Advances one or more strategy pillars                                                         | Full scoring matrix                                          |
| **Enabling capabilities** | Cross-cutting, unblocks work across pillars (docs architecture, QA automation, design system) | Full scoring matrix, with the enabler variant of Criterion 1 |
| **Maintenance**           | Required hygiene: security patches, dependency upgrades, deprecations, compatibility          | Will be considered ad-hoc, no scoring                        |
| **Management system**     | Changes to processes, metrics, governance                                                     | Not a roadmap item; handled through core team processes      |

Note: Classification correctness is essential so we know how much of our work genuinely contributes to our strategy.

## Gates (hard blocks)

All gates must pass before scoring. A blocked item is either declined, redirected, or returned for revision.

**G1. AI guiding principles alignment**: Mark each principle **Pass / N/A / Violation**. Any violation blocks.

| Principle                      | What 'good' looks like                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------- |
| 1. No AI dependency in core    | Feature can be delivered via a package, or discretionary AI adoption from our users |
| 2. Responsible approach to AI  | Strong alignment with ethical, environmental, transparency, or privacy commitments  |
| 3. Model and provider agnostic | Supports a wide range of model sizes / capabilities. Standards-based approach       |
| 4. Only the right AI           | AI applied with tangible value over a non-AI approach                               |
| 5. Human in the loop           | Preserves user agency. Reviewable quality outputs                                   |

**G2. Ecosystem placement**: Does this belong in core, or in a package? Package territory is ok if it requires a new core API or integration point, or if the goal is to have an official 'blessed' package.

**G3. Maintainability floor**: Is the ongoing maintenance burden bounded and understood?

## Scoring matrix

Score each criterion 1–5 using the guidance. Multiply by weight. Sum for the overall score out of 5.

### 1. Strategic fit: 25%

**Pillar work:** score the item against _each_ of the four pillars, then take the **MAX** as the criterion score. Record the per-pillar scores: they feed the roadmap alignment metric and pillar-balance review.

| Score | Guidance (per pillar)                           |
| ----- | ----------------------------------------------- |
| 5     | Directly delivers a named element of the pillar |
| 4     | Clearly advances the pillar's stated direction  |
| 3     | Plausibly connected, with explanation           |
| 2     | Weak or indirect connection                     |
| 1     | No identifiable connection                      |

**Enabler variant:** score breadth of unblocking instead.

| Score | Guidance (enablers)                                   |
| ----- | ----------------------------------------------------- |
| 5     | Materially unblocks or accelerates work in 3+ pillars |
| 4     | Unblocks/accelerates 2 pillars                        |
| 3     | Unblocks 1 pillar significantly                       |
| 2     | Marginal acceleration                                 |
| 1     | No identifiable strategic leverage                    |

### 2. Differentiator reinforcement: 15%

Does the item strengthen the cross-cutting differentiators that we pursue: accessibility, security, sustainability, responsible AI, SEO.

| Score | Guidance                                                                                   |
| ----- | ------------------------------------------------------------------------------------------ |
| 5     | Materially advances a differentiator beyond current standards (like WCAG/ATAG, WSG, OWASP) |
| 4     | Clear improvement to at least one differentiator                                           |
| 3     | Neutral, with differentiators consciously preserved                                        |
| 2     | Neutral, differentiator impact unexamined                                                  |
| 1     | Regresses a differentiator                                                                 |

### 3. User demand & adoption impact: 15%

Evidence of demand from target sectors (government/public sector, nonprofits, higher education, GLAM, agencies, in-house engineering teams) and impact on adoption decisions.

| Score | Guidance                                                                                                    |
| ----- | ----------------------------------------------------------------------------------------------------------- |
| 5     | Documented demand from multiple target-sector organisations or agencies; addresses a known adoption blocker |
| 4     | Clear demand signals from at least one target sector                                                        |
| 3     | Plausible demand; anecdotal evidence                                                                        |
| 2     | Assumed demand; no evidence gathered                                                                        |
| 1     | No identifiable user demand                                                                                 |

### 4. Sponsorship appeal: 15%

Could this attract a feature sponsor, or is it already funded?

| Score | Guidance                                                                                       |
| ----- | ---------------------------------------------------------------------------------------------- |
| 5     | Sponsor already committed or in active discussion                                              |
| 4     | Named plausible sponsor(s); the item maps to a need an identifiable organisation would pay for |
| 3     | Generic sponsorship potential; the kind of item that has attracted sponsors before             |
| 2     | Hard to attribute value to a single sponsor; would need pooled/collective funding              |
| 1     | No plausible route to sponsorship; core team capacity only                                     |

### 5. Deliverability: 15%

Scope clarity, low dependency risk.

| Score | Guidance                                                          |
| ----- | ----------------------------------------------------------------- |
| 5     | Well-scoped; no blocking dependencies                             |
| 4     | Scoped with minor open questions                                  |
| 3     | Direction clear but scope needs definition                        |
| 2     | Vague scope or significant unresolved dependencies                |
| 1     | Open-ended; no plausible path to delivery with available capacity |

### 6. Maintenance burden: 15%

Long-term cost to the core team after delivery. High score = low burden.

| Score | Guidance                                                 |
| ----- | -------------------------------------------------------- |
| 5     | Reduces net burden (automation, consolidation, deletion) |
| 4     | Negligible ongoing burden                                |
| 3     | Moderate, bounded burden                                 |
| 2     | Significant ongoing burden                               |
| 1     | Unbounded burden or new perpetual surface area           |

### Overall

**Overall weighted score = Σ (score × weight), out of 5.**

Weights sum to 100%: 25 + 15 + 15 + 15 + 15 + 15.

## Stage 3: Qualitative summary

Alongside the numbers, each assessment records:

- **One-paragraph rationale**: why this item, why now, in strategy language
- **Pillar attribution**: primary pillar (or "enabler"), for the alignment metric and visual identity (emoji/color)
- **AI principles record**: the Pass/N/A/Violation marks from G1 (these become responsible-AI proof points for marketing)
- **Key assumption to test**: the single thing most likely to change the score
- **Decision**: schedule / seek sponsor / park / decline, with review date if parked
