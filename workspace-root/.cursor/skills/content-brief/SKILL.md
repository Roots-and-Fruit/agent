---
name: content-brief
description: Generate a writer-ready HTML content brief for rootsandfruit.com at content/articles/slug/brief.html. User invokes with /content-brief after grill-info-gain.
disable-model-invocation: true
---

# R&F content brief

**Predictability:** every article slug gets `content/articles/<keyword-slug>/brief.html` with canonical R&F doc styles, embedded voiceprint handoff, and delta commitments.

Read section contract: [REFERENCE.md](REFERENCE.md). Canonical styles: `content/articles/example-explainer/brief.html`.

## When to use

- After `/grill-info-gain` (or with explicit delta commitments)
- Closing gaps flagged by `ig-audit.html` in the same article folder
- Translating keyword-intel into a writer-ready brief

## Procedure

### 1. Collect inputs

1. Primary keyword and slug → `content/articles/<keyword-slug>/`.
2. Mode: IG-Driven Lite (default), Standard, or Deep — see REFERENCE.md.
3. Artifact root: `content/keyword-intel/output/<keyword-slug>/`.
4. Page job and rootsandfruit.com target URL.
5. Success intent: traffic, leads, or commercial.
6. `Info Gain Handoff` from grill-info-gain when available.
7. **Voiceprint artifact (required):** latest `.cursor/skills/voiceprint/artifacts/*.md` — block if missing unless user logs explicit override in brief.
8. Prior `ig-audit.html` path when closing audit gaps.

**Done when:** slug, mode, voiceprint path (or override), and artifact root confirmed.

### 2. Load contracts

1. Read [REFERENCE.md](REFERENCE.md).
2. Copy `<!DOCTYPE html>` through `</style>` from `content/articles/example-explainer/brief.html` verbatim.
3. Ingest keyword-intel artifacts or mark Fanout Research Summary as degraded.
4. Extract **Voiceprint Handoff** block from voiceprint artifact for embedding.

**Done when:** canonical `<head>` loaded; voiceprint handoff ready to embed; evidence status known.

### 3. Build brief body

Populate REFERENCE section order including **Voiceprint Handoff** section. Separate baseline vs delta throughout. Use `delta-card` for each must-win (1–2 blog; up to 3–4 catalog pages).

Reflect grill handoff in Delta Artifact Commitments; add Handoff Fidelity Check when handoff existed.

**Done when:** all required sections for the chosen mode drafted.

### 4. Score pre-publish gate

Five rows × 0–2: baseline coverage, delta specificity, evidence traceability, fanout divergence, success proxy clarity.

- **≥8:** badge `Publish brief`
- **5–7:** revise once
- **<5:** do not ship

**Done when:** verdict band shows numeric score and matching badge.

### 5. Write output

Write **only** `content/articles/<keyword-slug>/brief.html`. Legacy `brief.md` → one-line stub linking to `brief.html`.

**Done when:** file exists on disk; response states publish recommendation and any degraded gaps.

## Pointers (do not duplicate)

- Pipeline: `/rf-article-pipeline`
- Downstream: `/article-writer` → `/voiceprint-audit` → user review → `/information-gain-auditor`
- Publish: `/rf-article-publish` after audit

## Anti-patterns

- Brief without voiceprint handoff (unless logged override)
- Shipping markdown as the brief deliverable
- Inventing fonts, colors, or layout
- Inventing internal rootsandfruit.com URLs
