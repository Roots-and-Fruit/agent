---
name: voiceprint
description: Build a reusable Roots & Fruit writing voice profile from samples and emit a voice contract for article-writer. User invokes with /voiceprint once or on voice refresh.
disable-model-invocation: true
---

# R&F voiceprint

**Predictability:** one auditable voice artifact at `.cursor/skills/voiceprint/artifacts/YYYY-MM-DD-<profile>-voiceprint.md` that `article-writer` can load every run.

## When to use

- First-time setup for rootsandfruit.com article voice
- Refresh after tone drift or new content registers (technical, pastoral, etc.)
- **Not** part of the per-article pipeline unless voice direction changed

## Procedure

### 1. Setup

Collect: profile name (slug-safe), use case (`blog/articles` default), collection mode (`interactive` or `provided samples`), target audience if known, strictness (`balanced` or `strict anti-AI`).

Confirm output path: `.cursor/skills/voiceprint/artifacts/YYYY-MM-DD-<profile>-voiceprint.md`.

**Done when:** profile name, use case, and output path are confirmed.

### 2. Writing samples (required)

Collect at least 5 samples across registers: casual, explanatory, enthusiastic, critical, opinionated. Prefer **rootsandfruit.com published posts** or user-approved drafts. Never infer voice from unrelated repo files.

Ask up to 2 follow-ups if register range is weak.

**Done when:** five labeled samples are recorded in the artifact.

### 3. Style calibration (required)

Collect concise answers for: sentence structure, punctuation, rhythm, **pacing (deliberate vs rushed)**, transitions (**section bridges required**), formality, specificity, personal voice (**`I` founder-first; no fake-team `we`**), opening/hook preference, **hand-holding level for explainers**.

**Done when:** Style Preferences section is populated.

### 4. Pattern rejection (required)

Capture AI-generic phrases, forced structures, **section jumps without bridges**, emoji/formatting boundaries, and freeform bans.

**Done when:** Rejected Patterns section lists enforceable bans with alternatives.

### 5. Voice synthesis (required)

Produce Voice Contract with: 3–5 core characteristics, rhythm/punctuation profiles, **Transition and Hand-Holding Profile**, 3–5 signature moves (include **section bridge** move), banned phrases with alternatives, opening/closing rules, blog format rules, 3–4 before/after rewrites, narrative-first guidance (bullets only when clarity demands it).

**Done when:** Voice Contract and Article Format Rules sections are complete.

### 6. Validation loop (required)

Write one test paragraph for the stated audience. Score Voice Match Check (0–2 each): tone, rhythm, wording, anti-pattern compliance, clarity. Total out of 10.

If score `< 7`, revise contract once and retest.

**Done when:** Validation Result shows numeric score and residual risks.

### 7. Writer handoff

Append paste-ready block:

```md
## Voiceprint Handoff
- Profile: <name> (solo founder if applicable)
- Core voice: <3-5 bullets — include first-person POV, deliberate pace, hand-holding>
- Signature moves: <3-5 bullets — include section bridges and walkthrough language>
- Hard bans: <phrases/patterns — include section jumps, fake-team we>
- Article format rules: <opening, rhythm, transitions, section bridges, closing>
- Validation score: <0-10>
- Residual risks: <if any>
```

**Done when:** artifact file exists with all 8 required sections and Handoff block.

## Pointers (do not duplicate)

- Draft step: `/article-writer` reads latest artifact from `.cursor/skills/voiceprint/artifacts/`
- If no artifact exists, `article-writer` proceeds with explicit voice-drift warning

## Anti-patterns

- Claiming voice traits without sample evidence or user confirmation
- Copying competitor phrasing into voice rules
- Overfitting one emotional register
