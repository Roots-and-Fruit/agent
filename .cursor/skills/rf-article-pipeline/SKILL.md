---
name: rf-article-pipeline
description: Orchestrate the rootsandfruit.com article pipeline from keyword research through MCP draft preview. User invokes with /rf-article-pipeline or resumes with --from.
disable-model-invocation: true
---

# R&F article pipeline

**Predictability:** same stage order, STOP gates, and artifact paths for every article slug under `content/articles/<keyword-slug>/`.

Do not duplicate child skill procedures — invoke each skill in order.

## When to use

- Starting a new rootsandfruit.com article end-to-end
- Resuming after a human review gate (`--from brief|writer|audit|publish`)

## Required MCP servers

| Server | Use |
|--------|-----|
| `wordpress-rootsandfruit` | Draft, blocks, author, preview, publish |
| `dataforseo` | Keyword/SERP research (`/rf-keyword-research` full mode) |

Credentials: [`agent/.env`](../../../.env) — `ROOTSANDFRUIT_MCP_*`, `DATAFORSEO_*`.

## Inputs

1. Primary keyword and slug (`<keyword-slug>`).
2. Success intent: `traffic`, `leads`, or `commercial`.
3. Target URL on rootsandfruit.com (if known).
4. Author for publish: user login or ID (for `/rf-article-publish`).
5. Resume flag (optional): `--from <stage>` — see table below.

**Done when:** slug and intent confirmed.

## Stage map

| # | Skill | Output | STOP gate |
|---|-------|--------|-----------|
| 0 | `/voiceprint` | `.cursor/skills/voiceprint/artifacts/*.md` | Once per voice refresh — skip if artifact exists |
| 1 | `/rf-keyword-research` | `content/keyword-intel/output/<slug>/` (+ `serp/corpus.md`) | — |
| 2 | `/grill-info-gain` | Info Gain Handoff block | — |
| 3 | `/content-brief` | `content/articles/<slug>/brief.html` | **STOP** — user reviews/tweaks brief |
| 4 | `/article-writer` | `content/articles/<slug>/draft.md` | — |
| 5 | `/voiceprint-audit` | revised `draft.md` + `excerpt.txt` + `key-takeaways.txt` | **STOP** — user reviews draft, excerpt, takeaways |
| 6 | `/information-gain-auditor` | `ig-audit.html` + `ig-audit.json` + `serp_delta.json` | — |
| 7 | `/rf-article-publish` | WP draft + `preview_url` | **STOP** — user reviews public preview |
| 8 | `/rf-article-publish` (approve) | `publish-post` on explicit OK | Live only after user says publish |

## Resume (`--from`)

| `--from` | Start at skill | Requires on disk |
|----------|----------------|------------------|
| `research` | `/rf-keyword-research` | slug only |
| `grill` | `/grill-info-gain` | keyword-intel artifacts |
| `brief` | `/content-brief` | keyword-intel + handoff (or user deltas) |
| `writer` | `/article-writer` | approved `brief.html` |
| `voice` | `/voiceprint-audit` | `draft.md` from writer |
| `audit` | `/information-gain-auditor` | `draft.md` after voiceprint-audit |
| `publish` | `/rf-article-publish` | `draft.md` + passing `ig-audit.json` |

**Done when:** correct resume stage identified and prior artifacts verified.

## Procedure

### 1. Preflight

Confirm voiceprint artifact exists or run `/voiceprint` first.

Confirm MCP servers available (WordPress ping; DataforSEO for full research).

**Done when:** voiceprint path known; MCP status OK or degraded mode agreed.

### 2. Run stages in order

Invoke each skill with slug and paths from the stage map. Stop at every **STOP gate** until user confirms continue.

After brief STOP: user may edit `brief.html` in place or re-run `/content-brief`.

After draft STOP: user may edit `draft.md` in place or re-run `/article-writer` then `/voiceprint-audit`.

After preview STOP: user requests block edits via `/rf-article-publish` or approves publish.

**Done when:** current stage complete per child skill **Done when** criteria.

### 3. Close

When publish completes, record `post_id` and live URL in chat. Remind: Breeze purge if author/byline changed before sharing logged-out URLs.

**Done when:** draft preview delivered or post published per user instruction.

## Pointers (do not duplicate)

- Layout: [`content/README.md`](../../../content/README.md)
- Plan: [`agent/.cursor/plans/rf-article-pipeline.plan.md`](../../plans/rf-article-pipeline.plan.md)
- WordPress routing: [`agent_docs/mcp-routing.md`](../../../agent_docs/mcp-routing.md)

## Anti-patterns

- Skipping `/rf-keyword-research` before grill without degraded approval
- Publishing without preview STOP
- Calling `publish-post` before explicit user approval
- Inlining full brief/writer procedures in this skill
