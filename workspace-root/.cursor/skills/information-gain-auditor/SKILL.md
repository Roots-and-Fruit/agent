---
name: information-gain-auditor
description: Produce ig-audit.html and ig-audit.json for rootsandfruit.com articles in plain language. User invokes with /information-gain-auditor after voiceprint-audit and user draft review.
disable-model-invocation: true
---

# R&F information gain auditor

**Predictability:** every audit lands as `content/articles/<slug>/ig-audit.html` + matching `ig-audit.json`, styled from the example explainer.

Read section contract: [REFERENCE.md](REFERENCE.md). Canonical styles: `content/articles/example-explainer/ig-audit.html`.

## When to use

- After user reviews post-`/voiceprint-audit` `draft.md` (draft-article mode)
- Before `/rf-article-publish`
- Reviewing a live rootsandfruit.com URL (live-page mode)

## Procedure

### 1. Collect inputs

1. Mode: `draft-article` or `live-page-plain-language`.
2. Slug folder: `content/articles/<keyword-slug>/`.
3. Draft mode: `brief.html`, `draft.md`, artifact root `content/keyword-intel/output/<slug>/`.
4. Optional: `--refresh-serp` when keyword-intel artifacts are stale (>30 days).
5. Page job in one sentence.

**Done when:** mode and paths confirmed.

### 2. Load contracts

Read [REFERENCE.md](REFERENCE.md). Copy `<!DOCTYPE html>` through `</style>` from `content/articles/example-explainer/ig-audit.html`.

**Done when:** canonical audit `<head>` ready.

### 3. Score

**Draft-article:** run from `agent/` (corpus first, then audit):

```powershell
python content/keyword-intel/scripts/build_serp_corpus.py --artifact-root content/keyword-intel/output/<slug>/
python content/keyword-intel/scripts/ig_audit.py --brief content/articles/<slug>/brief.html --draft content/articles/<slug>/draft.md --artifact-root content/keyword-intel/output/<slug>/
```

Map script categories to plain-language scorecard labels per REFERENCE.md. Read `serp_delta.json` for actionable fixes (novel claims, baseline gaps).

**Corpus refresh:** re-run `build_serp_corpus.py` when keyword-intel artifacts are stale (>30 days) or user sets `--refresh-serp` (omit `--skip-fetch`).

**Live-page:** score 6 rows × 0–2 from observed evidence only.

**Done when:** `ig-audit.json` + `serp_delta.json` exist; script exit 0; `scoring_mode` is `brief-draft+serp-corpus` (not degraded).

### 4. Write HTML

Render scorecard, What's working, What's hurting, Do this next. Link to `brief.html` in note-card.

Badge thresholds (draft-article): ≥10 publish-ready · 8–9 revise-once · <8 no-publish

**Done when:** `ig-audit.html` exists with aligned scores.

### 5. Publish handoff

If publish-ready (or user override): next step is `/rf-article-publish` in **preview** mode — not live publish.

**Done when:** response states total score, badge, **`ig_why_summary.one_liner`** (why this score), top fix priorities if any, and publish handoff if applicable.

## Pointers (do not duplicate)

- Legwork: `content/keyword-intel/scripts/ig_audit.py`
- Publish: `/rf-article-publish`
- DataforSEO supplement: [rf-keyword-research/references/dataforseo.md](../rf-keyword-research/references/dataforseo.md)

## Anti-patterns

- Running before voiceprint-audit / user draft review in pipeline
- Scoring from vibe when script output exists
- Mismatched HTML and JSON scores
- Jumping to `publish-post` from this skill
