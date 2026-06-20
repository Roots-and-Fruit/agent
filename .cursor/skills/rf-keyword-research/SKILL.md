---
name: rf-keyword-research
description: Run keyword and SERP research for a rootsandfruit.com article slug and write keyword-intel artifacts. User invokes with /rf-keyword-research before grill-info-gain.
disable-model-invocation: true
---

# R&F keyword research

**Predictability:** every new article slug gets the same artifact layout under `content/keyword-intel/output/<slug>/` before grill or brief work.

Authoritative layout: [`content/README.md`](../../../content/README.md). DataforSEO wiring: [references/dataforseo.md](references/dataforseo.md).

## When to use

- Starting a new article for rootsandfruit.com
- Upstream step before `/grill-info-gain` and `/content-brief`
- Refreshing stale SERP evidence for an existing slug

## Procedure

### 1. Collect inputs

1. Primary keyword and slug-safe folder name (`<keyword-slug>`).
2. Success intent: `traffic`, `leads`, or `commercial`.
3. Target URL on rootsandfruit.com (if known).
4. Research mode: `full` (DataforSEO MCP required) or `degraded` (user-approved notes only).

**Done when:** slug, keyword, and mode are confirmed.

### 2. Prepare artifact root

Create `content/keyword-intel/output/<keyword-slug>/` with:

- `manifest.json` — slug, primary keyword, timestamps, mode, file pointers
- `scored/top_n.json` — primary, secondaries, top-result summaries
- `reports/baseline-delta.md` — Baseline, Delta, Friction, Information Gain sections

Use `content/keyword-intel/output/example-explainer/` as structural reference.

**Done when:** folder exists and `manifest.json` lists artifact paths.

### 3. Gather evidence

**Full mode:** call **DataforSEO MCP** per [references/dataforseo.md](references/dataforseo.md). Record `dataforseo_tools_used` in `manifest.json`. Never invent SERP URLs, rankings, or competitor quotes.

**Degraded mode:** only after user approves; set `"mode": "degraded"` in manifest; label scope honestly in report.

**Done when:** `top_n.json` and `baseline-delta.md` reflect real or explicitly degraded evidence.

### 4. Summarize for downstream skills

Ensure the report includes:

- **Baseline** — table-stakes topics competitors cover
- **Delta** — gaps this article could win
- **Friction** — reader decision blockers
- **Information gain opportunity** — one paragraph tied to evidence

**Done when:** `grill-info-gain` can read `manifest.json`, `scored/top_n.json`, and the report without missing required sections.

### 5. Build SERP baseline corpus (full mode)

From `agent/`:

```powershell
python content/keyword-intel/scripts/build_serp_corpus.py --artifact-root content/keyword-intel/output/<keyword-slug>/
```

Writes `serp/corpus.md`, `serp/serp_raw.json`, `serp/pages/*.md`, and `serp/corpus_manifest.json` via DataForSEO SERP + On-Page APIs. Required before `/information-gain-auditor`.

**Done when:** `serp/corpus.md` exists and `manifest.json` lists serp artifact paths.

## Pointers (do not duplicate)

- Pipeline: `/rf-article-pipeline`
- Next step: `/grill-info-gain`
- MCP credentials: `DATAFORSEO_*` in [`agent/.env`](../../../.env)

## Anti-patterns

- Full mode without DataforSEO MCP calls
- Skipping artifacts and jumping straight to brief.html
- Fabricating SERP data
- Writing research only in chat with no files on disk
