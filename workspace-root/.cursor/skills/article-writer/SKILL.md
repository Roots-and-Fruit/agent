---
name: article-writer
description: Write draft.md from a finalized brief.html for rootsandfruit.com preserving delta commitments and voiceprint. User invokes with /article-writer when brief.html is publish-ready.
disable-model-invocation: true
---

# R&F article writer

**Predictability:** one `draft.md` per run that preserves every delta from `brief.html`, applies voiceprint from brief handoff, and appends a Draft QA Summary.

Canonical brief example: `content/articles/example-explainer/brief.html`.

## When to use

- After `brief.html` scores ≥8 (Publish brief or post-revise)
- Before `/voiceprint-audit` in the pipeline

## Procedure

### 1. Collect inputs

1. Brief path (required): `content/articles/<keyword-slug>/brief.html`.
2. Draft output (required): `content/articles/<keyword-slug>/draft.md`.
3. Info gain source: brief Delta Artifact Commitments and/or pasted Info Gain Handoff.
4. Voiceprint (required via brief): **Voiceprint Handoff** section in `brief.html`; fallback to `.cursor/skills/voiceprint/artifacts/*.md` only if brief section missing.
5. Draft depth: `short`, `standard` (default), or `deep`.

If brief, deltas, or voiceprint handoff missing, stop and ask whether to proceed degraded.

**Done when:** paths confirmed; voiceprint loaded from brief first.

### 2. Contract ingestion

Extract from brief.html: Objective, Audience & Tone, Keywords, Positioning Snapshot, Baseline Coverage Commitments, Delta Artifact Commitments, Page Structure, Language Contract, Suggested Links & CTA, **Voiceprint Handoff**, Information Gain Audit score.

**Done when:** blueprint notes list every delta with target section placement.

### 3. Section blueprint

Build before prose: one claim per section, evidence intent, **transition line (opener + closer bridge to next §)**, delta-to-section mapping.

**Done when:** every chosen delta maps to a Page Structure § number; every § has a planned bridge.

### 4. Draft generation

Write in section order using voiceprint rules from brief: **founder-first `I`**, **deliberate pace**, **hand-holding on new terms**, **explicit section bridges**. No banned patterns; no fabricated citations.

**Done when:** full draft body and CTA exist in memory.

### 5. Quality gates

1. **Delta Preservation**
2. **Voice Fidelity** (founder POV, pacing, transitions/hand-holding per Voiceprint Handoff)
3. **Structure** (section bridges present; no orphan H2s)
4. **Evidence Safety**

Revise once if any gate fails.

**Done when:** all four gates pass or one revision cycle completed.

### 6. Write output

Write `draft.md` with title, section headings, CTA, and Draft QA Summary block.

**Done when:** `draft.md` exists at the requested path with QA block.

## Pointers (do not duplicate)

- Next: `/voiceprint-audit` (auto-revise before user review)
- Then: user review → `/information-gain-auditor` → `/rf-article-publish`
- Pipeline: `/rf-article-pipeline`

## Anti-patterns

- Skipping voiceprint handoff in brief
- Overriding delta commitments
- Generic SEO filler language
