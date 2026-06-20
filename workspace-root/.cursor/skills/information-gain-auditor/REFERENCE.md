# IG Audit HTML — Reference Contract

Canonical example: `content/articles/example-explainer/ig-audit.html`  
JSON companion: `content/articles/example-explainer/ig-audit.json`

## HTML shell (mandatory)

Every audit **must** be self-contained HTML with R&F doc styles embedded. Steps:

1. Read `content/articles/example-explainer/ig-audit.html`.
2. Copy `<!DOCTYPE html>` through `</style>` unchanged (fonts, CSS variables, all class rules).
3. Change only `<title>` and `<body>` content.
4. Write to `content/articles/<keyword-slug>/ig-audit.html`.
5. Write matching `ig-audit.json` in the same folder.

**Never:** output markdown as the audit; swap fonts/colors; use external stylesheets; omit the score-grid CSS.

Legacy `ig-audit.md` may be a one-line stub: `Canonical audit: [ig-audit.html](ig-audit.html)`.

---

## Tone and language

- **Audience:** stakeholder or writer — not SEO jargon.
- **Scorecard labels:** plain questions (“Does the draft explain the next step clearly?”), not category codes.
- **Score notes:** one short italic sentence under each score — what you observed, not theory.
- **Verdict:** direct (“Revise first”, “Publish-ready”); one paragraph what's strong, one line what to fix.
- **What's hurting:** numbered `h3` findings with tables/lists where helpful; assume a stated **page job**.
- **Do this next:** ordered checklist; first 3 items are **blockers** when audit score &lt; 10.
- Avoid: “information gain”, “delta fidelity”, “SERP novelty” in HTML body (OK in JSON `scores` keys).

---

## Document flow (required order)

1. **`<header class="doc-header">`**
   - `doc-kicker`: `Plain-Language Audit` (clay uppercase)
   - `h1`: `{Page name} — What to Fix` (or “Publish Readiness” for draft mode)
   - `meta-grid` rows: Page · Page job · Date · Compared to

2. **Scorecard** (`section`, `h2`: Scorecard)
   - Intro paragraph: explain 0–2 scale and **page job** lens
   - `ul.score-grid` with 6× `li.score-{0|1|2}`
   - Each card: `span.label`, `span.value` (e.g. `1/2`), `p.score-note`
   - Final `li.verdict-total`: `verdict-score`, `badge`, `verdict-body`

3. **Why this score** (`section`, `h2`: Why this score)
   - Lead: `ig_why_summary.one_liner` from JSON (required when present)
   - `h3`: What page-one already covers — `page_one_contrast` (truncate for HTML)
   - `h3`: What wins on information gain — `ul` of `wins_vs_serp[]` title + body
   - Optional `h3`: Sample novel claims — `notable_novel_claims`
   - `div.note-card`: `caveats` bullets

4. **What's working** (`keep-list`)
   - Lead: “Do not delete these…”
   - `ul.keep-list` with checkmark pseudo-elements

4. **What's hurting**
   - Lead: restate page-job assumption
   - Numbered `h3` subfindings; use `table-wrap` + `stat-line` where useful

5. **Do this next**
   - `ol.checklist` — items 1–3 `li.blocker` + `span.blocker-tag` Blocker + `span.sub` when score &lt; 10
   - `p.checklist-divider`: “Then tighten the rest…”
   - `ol.checklist.continue` (counter continues from 3) when needed
   - `div.note-card`: link to `brief.html`; re-audit target score; mention `/rf-wordpress-ops` when publish-ready

6. **`p.footer-note`**: `Roots & Fruit Audit · {date}`

---

## Score colors (CSS classes)

| Score | Class | Meaning |
|-------|--------|---------|
| 0 | `score-0` | Missing / weak (clay) |
| 1 | `score-1` | Partial (amber) |
| 2 | `score-2` | Solid (olive) |

Verdict row: `verdict-total` with clay-soft background; badge clay for revise, olive for publish-ready.

---

## Draft-article mode: script → HTML mapping

Run from `agent/`:

```powershell
python content/keyword-intel/scripts/ig_audit.py --brief content/articles/<slug>/brief.html --draft content/articles/<slug>/draft.md --artifact-root content/keyword-intel/output/<slug>/
```

When `--brief` is `brief.html`, JSON defaults to `ig-audit.json` in the same folder; render `ig-audit.html` from JSON via this skill.

Map `ig_audit.py` categories to scorecard **labels** (rewrite as plain questions):

| Script category | Example scorecard label |
|-----------------|-------------------------|
| Delta Fidelity | Does the draft deliver what the brief promised? |
| Artifact Realization | Are required proof blocks present and usable? |
| Baseline Coverage | Does the draft cover table-stakes topics page-one already explains? |
| SERP Novelty | Does the draft add claims absent from the SERP baseline corpus? |
| Intent Fit | Does the draft fit the primary keyword intent (navigational / informational)? |
| Risk Honesty | Are limits, caveats, and scope stated plainly? |

**Prerequisite:** build SERP corpus before audit (DataForSEO):

```powershell
python content/keyword-intel/scripts/build_serp_corpus.py --artifact-root content/keyword-intel/output/<slug>/
python content/keyword-intel/scripts/ig_audit.py --brief content/articles/<slug>/brief.html --draft content/articles/<slug>/draft.md --artifact-root content/keyword-intel/output/<slug>/
```

When `--brief` is `brief.html`, JSON defaults to `ig-audit.json` in the same folder; companion `serp_delta.json` lists novel claims and fixes. Render `ig-audit.html` from JSON via this skill.

Use script total for `verdict-score` and recommendation for `badge` text. Include `scoring_mode: brief-draft+serp-corpus` in JSON note-card when corpus-backed.

**Optional refresh:** `--refresh-serp` on corpus builder when artifacts are stale (>30 days).

---

## Live-page mode: scorecard rows

Tailor all 6 rows to the **page job**. Blog explainer example:

1. Does the intro state the page job in plain language?
2. Are baseline topics easy to scan?
3. Does the article include at least one distinctive proof block?
4. Are claims honest about scope and limits?
5. Can the reader take a clear next step?
6. Are internal links relevant to rootsandfruit.com readers?

For other page types, rewrite rows but keep six 0–2 questions aligned to that job.

---

## JSON schema (minimum)

```json
{
  "audit_mode": "draft-article | live-page-plain-language",
  "page_intent": "short-key",
  "page_intent_note": "one sentence",
  "target_url": "",
  "date": "YYYY-MM-DD",
  "compared_against": "",
  "recommendation": "publish-ready | revise-once | revise-first | no-publish",
  "recommendation_plain": "",
  "total_score": 0,
  "max_score": 12,
  "scores": { },
  "keep_these": [],
  "fix_first": [],
  "blockers": [],
  "next_steps": [],
  "rewrite_target_score": 10
}
```

HTML and JSON scores must match.

---

## Checklist HTML pattern

```html
<li class="blocker">
  <strong>Action headline.</strong><span class="blocker-tag">Blocker</span>
  <span class="sub">Concrete sub-instruction for writer/dev.</span>
</li>
```

Non-blockers omit `blocker` class and tag.

---

## Links

- Same folder: `brief.html`, optional mock HTML
- Live rootsandfruit.com URL in meta row when applicable
