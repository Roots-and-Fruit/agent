# Content Brief HTML — Reference Contract

Canonical example: `content/articles/example-explainer/brief.html`  
Pairs with: `content/articles/example-explainer/ig-audit.html`

## HTML shell (mandatory)

Every brief **must** be self-contained HTML with R&F doc styles embedded. Steps:

1. Read `content/articles/example-explainer/brief.html`.
2. Copy `<!DOCTYPE html>` through `</style>` unchanged (fonts, CSS variables, all class rules).
3. Change only `<title>` and `<body>` content.
4. Write to `content/articles/<keyword-slug>/brief.html`.

**Never:** output markdown as the brief; swap fonts/colors; use external stylesheets; skip the verdict band or delta-card CSS.

Legacy `brief.md` may be a one-line stub: `Canonical brief: [brief.html](brief.html)`.

---

## Modes and output paths

| Mode | Use when | Output |
|------|----------|--------|
| **IG-Driven Lite (default)** | Normal production; keyword-intel artifacts available | `content/articles/<slug>/brief.html` |
| **Standard** | Extra confidence on fanout/keyword patterns | `brief.html` with expanded fanout/positioning |
| **Deep** | Stakeholder wants full receipts | `brief.html` + optional `content/articles/<slug>/research.md` |

Paired audit (when run): `ig-audit.html` + `ig-audit.json` in same article folder.

---

## Research budget by mode

### IG-Driven Lite (default)

- Ingest keyword-intel artifacts: `manifest.json`, `scored/top_n.json`, `reports/baseline-delta.md`.
- Capture fanout query evidence (primary plus intent variants) from available provider outputs.
- Use 1 primary plus up to 4 secondary keywords.
- Add one concise positioning paragraph tied to real evidence.
- Add baseline commitments plus at least one delta artifact commitment.
- Internal links only to real rootsandfruit.com URLs.
- Add 2–3 accuracy checks only for claims likely to drift.

### Standard

IG-Driven Lite plus:

- 8–10 related keywords.
- Expanded fanout divergence analysis and one competitor pattern block (max 5 rows/bullets).
- Explicit no-go area: what this draft should avoid competing on.

### Deep

Standard plus:

- Full appendix with keyword and SERP evidence in optional `research.md`.
- Extra competitor and format analysis only when requested.

### Data-source handling

If primary research sources are unavailable, stop and ask for approval before running degraded mode. Label degraded scope honestly in **Fanout Research Summary**.

---

## Info Gain Handoff (when from grill-info-gain)

When `grill-info-gain` ran before the brief, reflect handoff in **Delta Artifact Commitments** and/or a short note under **Positioning Snapshot**:

- Each chosen delta: topic, required artifact, proof claim, success proxy, brief injection point (Page Structure §).
- If a handoff delta was overridden, state why in one line.

Optional **Handoff Fidelity Check** (mini-card or bullet list at end of Delta section when handoff existed):

- `[Delta title] → [Page Structure §] → Kept | Overridden (reason)`

---

## Internal cross-link rule

Before finalizing **Suggested Links & CTA**:

1. Find related rootsandfruit.com URLs from sitemap or live site when available.
2. Include internal URLs only when relevant — do not invent paths.

---

## Baseline/Delta gate

Before finalizing:

1. Confirm baseline-required topics from the report appear in planned structure.
2. Confirm at least one delta includes a concrete required artifact.
3. Map each delta commitment to a success proxy.

---

## Outline quality gate

Before finalizing **Page Structure**:

1. Choose best archetype (explainer, how-to, comparison, update).
2. Order sections by reader friction: confusion → clarity → interpretation → action → CTA.
3. Use outcome-first headings; avoid generic placeholders.
4. Confirm sequence supports delta proof placement.

If the outline fails, revise section order/headings before shipping.

---

## Verification gates

Brief passes when:

1. Objective, audience, CTA, and timeline are present.
2. Page Structure has 5–7 sections.
3. Keywords: 1 primary plus 3–5 secondaries.
4. Positioning Snapshot includes at least one demand signal plus one SERP landscape observation.
5. Suggested Links include at least two useful links total.
6. Baseline Coverage Commitments are explicit and mapped to report evidence.
7. Delta Artifact Commitments include required artifact plus success proxy.
8. Information Gain Audit includes score and publish recommendation.
9. Depth choice and rationale appear in **Audience & Tone** (Short take / Standard run / Deep dive).

If any gate fails, revise once and re-check.

---

## IG audit (downstream)

After draft or live-page review, run `/information-gain-auditor` → `ig-audit.html` + `ig-audit.json`. Canonical example: `content/articles/example-explainer/ig-audit.html`.

---

## Tone and language

- **Audience:** writer + approver.
- **Page job** stated early: what this URL is for on rootsandfruit.com (blog explainer ≠ homepage).
- Plainspoken, specific, evidence-backed; “scan like a spec sheet”.
- Baseline = table stakes competitors show; Delta = provable differentiators with artifacts.
- Cross-link related site pages — don’t duplicate whole-site positioning blocks on focused articles.
- Degraded fanout: say so honestly in Fanout Research Summary.

---

## Document flow (required sections, in order)

1. **`<header class="doc-header">`**
   - `doc-kicker`: `Content Brief · {Page type}` (olive uppercase)
   - `h1`: descriptive rewrite title
   - `p.lead`: URL link + page job + commercial intent

2. **`<div class="verdict">`** (below header, olive band)
   - `verdict-score`: brief quality score (e.g. `10/10`)
   - `badge`: `Publish brief` | `Revise once` | `No publish`
   - Paragraph linking to `ig-audit.html` and live-page score if known

3. **Objective** — one section card; page job in plain language

4. **Audience & Tone** — `two-col` with `mini-card` pairs

5. **Keywords** — primary + `tag-row` / `span.tag` secondaries

6. **Positioning Snapshot** — competitor frame + `callout` angle + baseline/delta bullets

7. **Fanout Research Summary** — mode note; `two-col` Consensus / Divergence mini-cards

8. **Baseline Coverage Commitments** — scannable bullet list; cross-link only items

9. **Voiceprint Handoff** — embedded paste-ready block from voiceprint artifact:
   - Core voice bullets (founder-first `I`, deliberate pace, hand-holding)
   - Signature moves (section bridges, walkthrough language)
   - Hard bans (fake-team `we`, section jumps, telegraphic explainers)
   - Article format rules (transitions between §, preview walkthrough in opening)
   - Source artifact path and date in a one-line note
   - Required for `/article-writer` and `/voiceprint-audit`

10. **Delta Artifact Commitments** — one `article.delta-card` per must-win:
   - `p.must-win`: Must-win #N | Supporting delta
   - `h3` title
   - `dl` with Required artifact · Proof claim · Success proxy

11. **Page Structure** — `callout` for audit blockers when relevant; `ol.structure-list`:
    - `span.num`, description, `span.type baseline|delta`

12. **Language Contract** — banned-term table + required patterns list

13. **Suggested Links & CTA** — `two-col` link-list mini-cards; CTA fork line

14. **Accuracy Checks** — pre-ship verification bullets + timeline

15. **Page Audit Alignment** — when `ig-audit.html` exists; table maps audit rows → brief §

16. **Information Gain Audit (Pre-Publish)** — `ul.audit-scores` with `span.score` per row + total

17. **Visual mock — what this brief should look like** (optional, when local mock HTML exists)
    - `callout` linking before/after mock files in the article folder
    - Punch-list of design/copy changes (grouped by h3)

18. **`p.footer-note`**: `Roots & Fruit · {slug} · Content Brief · {date}`

---

## Key CSS components

| Component | Use |
|-----------|-----|
| `verdict` | Top olive band — brief quality gate |
| `delta-card` | Each must-win delta |
| `structure-list` | Numbered page outline with Baseline/Delta pills |
| `tag` / `tag.baseline` / `tag.delta` | Keyword or commitment tags |
| `callout` | Clay-left border — audit blockers, angle, mock notice |
| `mini-card` | Two-column fact blocks |
| `table-wrap` | Language contract, audit alignment |
| `audit-scores` | Pre-publish 5-row score list |

Brief uses **olive** accent for publish-positive verdict; audit HTML uses **clay** for revise urgency — do not swap.

---

## Baseline vs Delta rules

- **Baseline:** cost-of-admission topics; must be scannable from intro/checklist, not buried only in demos.
- **Delta:** must include all three in each card:
  - Required artifact (specific block, diagram, or copy pattern)
  - Proof claim (why it matters vs generic competitor page)
  - Success proxy (interaction, scroll, CTA, or qualifiable support signal)

**Delta count by page type:**

| Page type | Must-win deltas | Structure sections |
|-----------|-----------------|-------------------|
| Blog explainer / how-to | 1–2 | 5–7 |
| Long guide | 2–3 | 6–8 |
| Large catalog / features-scale | 3–4 | 7–9 |

Align with `grill-info-gain` (max 3 chosen deltas) unless user explicitly requests more.

---

## Page Audit Alignment table

When `ig-audit.html` scorecard exists, one row per audit dimension:

| Audit score (live) | Brief closes it via |

Reference brief § numbers from Page Structure list.

---

## Pre-publish gate (brief HTML)

Five rows × 0–2 (display as `2/2` in audit-scores list):

1. Baseline coverage complete  
2. Delta artifact specificity  
3. Evidence traceability  
4. Fanout divergence usage  
5. Success proxy clarity  

Total ≥8 → `Publish brief` badge.

---

## Output paths

| File | Role |
|------|------|
| `brief.html` | **Canonical** writer contract (required) |
| `brief.md` | Legacy stub only — link to `brief.html` |
| `ig-audit.html` | Input when closing audit gaps |
| `mock-*.html` | Optional visual mock — link from section 16 |

---

## Visual mock section (section 16)

Include when team builds a local HTML mock in the article folder:

```html
<section>
  <h2>Visual mock — what this brief should look like</h2>
  <div class="callout">
    <p><strong>Not for production.</strong> Local preview only.</p>
    <p><a href="mock-after.html"><strong>mock-after.html</strong></a> is the target layout …</p>
  </div>
  <h3>…</h3>
  <ul>…</ul>
</section>
```

Adapt filenames to the article folder.
