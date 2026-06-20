---
name: grill-info-gain
description: Interview the user to lock 1-3 defensible information-gain deltas using keyword-intel artifacts. User invokes with /grill-info-gain after rf-keyword-research and before content-brief.
disable-model-invocation: true
---

# R&F grill info gain

**Predictability:** at most 10 single questions, then a paste-ready `Info Gain Handoff` block for `/content-brief`.

## When to use

- After `/rf-keyword-research` produced artifacts
- Before `/content-brief` when delta commitments need explicit user sign-off

## Procedure

### 1. Collect inputs

1. Primary keyword and slug (`content/articles/<keyword-slug>/`).
2. Artifact root: `content/keyword-intel/output/<keyword-slug>/`.
3. Success intent: `traffic`, `leads`, or `commercial`.
4. Publish target URL on rootsandfruit.com (if known).
5. Strictness: default (ship after ≤10 questions) or strict (optional continuation only if user asks).

**Done when:** slug and artifact root are confirmed; missing inputs requested before Question 1.

### 2. Read artifacts

In order: `manifest.json`, `scored/top_n.json`, `reports/baseline-delta.md`; `raw/*.json` only for tie-breaks.

If artifacts missing, stale, or contradictory, state degraded status and ask whether to continue.

**Done when:** baseline and delta evidence summarized internally before interviewing.

### 3. Interview (max 10 questions)

One question per turn. Fixed progression (stop early when sufficient):

1. Baseline reality check
2. Gap selection from report evidence
3. Differentiation test
4. Proof design per delta
5. Feasibility this cycle
6. Intent alignment
7. Reader friction
8. Competitive response
9. Prioritization (must-have vs nice-to-have)
10. Final commitment lock (1–3 deltas)

Each turn format:

- `Question <n>/10: <single question>`
- `Why this matters: <one sentence>`
- `Recommended answer pattern: <concrete structure>`

**Done when:** 1–3 deltas have topic, required artifact, proof claim, success proxy, and brief injection point — or Question 10 triggers insufficient-info handling.

### 4. Emit handoff

```md
## Info Gain Handoff

### Chosen Deltas (max 3)
- Delta 1: <short title>
- Delta 2: <short title>
- Delta 3: <short title or omit>

### Delta Artifact Commitments
- Topic: <topic>
  - Required artifact: <artifact to create/include>
  - Proof claim: <claim this artifact supports>
  - Success proxy: <observable indicator>
  - Brief injection point: <Page Structure § in content-brief>

### Rejected Ideas
- <idea> — rejected because <reason>

### Open Risks
- <risk and mitigation>
```

If Question 10 reached with insufficient signal, add `### Insufficient Information Notice` per template in prior audits, then stop and ask about optional continuation.

**Done when:** complete handoff block is in chat and ready to paste into brief workflow.

## Pointers (do not duplicate)

- Upstream: `/rf-keyword-research`
- Downstream: `/content-brief` → `content/articles/<slug>/brief.html`

## Anti-patterns

- Inventing SERP or competitor evidence
- Compound multi-part questions in one turn
- Proceeding to brief output without handoff block
- More than 10 questions
