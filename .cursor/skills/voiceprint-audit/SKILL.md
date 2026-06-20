---
name: voiceprint-audit
description: Audit and revise draft.md against voiceprint before user review. User invokes with /voiceprint-audit after article-writer.
disable-model-invocation: true
---

# R&F voiceprint audit

**Predictability:** every draft gets one Voice Match Check and at most one in-place revision before the user sees it.

Runs **after** `/article-writer`, **before** the orchestrator draft STOP gate.

## When to use

- Immediately after `/article-writer` writes `draft.md`
- Re-run after manual draft edits if voice drift is suspected

## Procedure

### 1. Collect inputs

1. Draft path: `content/articles/<keyword-slug>/draft.md`.
2. Voiceprint source (in order):
   - **Voiceprint Handoff** section in `brief.html` (preferred)
   - Latest `.cursor/skills/voiceprint/artifacts/*.md`
3. Language Contract from `brief.html` (banned terms).

If no voiceprint source, stop and run `/voiceprint` or `/content-brief` first.

**Done when:** draft and voice rules loaded.

### 2. Voice Match Check

Score 0–2 each (max 10):

- tone fit (founder-first `I`, approachable, personable)
- rhythm & pacing (deliberate pace; hand-holding on new concepts; not telegraphic)
- transition fit (section bridges; tee-up openers/closers; no orphan H2s)
- wording & clarity (plain language; right depth for audience)
- anti-pattern compliance (hard bans + language contract)

**Done when:** numeric score computed.

### 3. Revise if needed

If total **< 7/10**: revise `draft.md` in place once — preserve delta commitments and section structure from brief.

If total **≥ 7/10**: no revision required.

**Done when:** draft meets threshold or one revision cycle completed.

### 4. Update QA block

Append or update in `draft.md`:

```md
## Voiceprint Audit
- Voice Match Check: <score>/10
- Revised in place: <yes|no>
- Residual voice risks: <if any>
```

**Done when:** `draft.md` on disk includes Voiceprint Audit section.

## Pointers (do not duplicate)

- Upstream: `/article-writer`
- Downstream: `/information-gain-auditor` (after user draft review in pipeline)
- Voice baseline: `/voiceprint`

## Anti-patterns

- Skipping audit and sending raw writer output to user review
- Revising more than once without user request
- Stripping delta content during voice fixes
