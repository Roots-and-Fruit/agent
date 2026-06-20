# DataforSEO MCP — keyword research reference

Used by `/rf-keyword-research` in **full mode**. Discover live tool names via the `dataforseo` MCP server in Cursor — tool lists change with package version.

Credentials: `DATAFORSEO_USERNAME` and `DATAFORSEO_PASSWORD` in [`agent/.env`](../../../../.env). MCP launcher: [`tools/scripts/run-dataforseo-mcp.mjs`](../../../../tools/scripts/run-dataforseo-mcp.mjs).

## Required calls (full mode)

Before writing artifacts, gather:

1. **Primary keyword metrics** — volume, difficulty, intent signals if available.
2. **SERP top results** — at least 5 organic URLs for primary keyword (US or target location).
3. **Related keywords** — 3–10 secondaries or fanout variants.

Map results into repo artifacts — never leave research only in chat.

## Artifact mapping

| Artifact field | Data source |
|----------------|-------------|
| `manifest.json` → `primary_keyword`, `generated_at`, `mode: "full"` | User input + timestamp |
| `scored/top_n.json` → `primary`, `secondaries`, `top_results[]` | SERP + keyword tools |
| `reports/baseline-delta.md` → Baseline | Topics covered in top results |
| `reports/baseline-delta.md` → Delta | Gaps vs top results |
| `reports/baseline-delta.md` → Friction | Reader blockers from SERP patterns |
| `reports/baseline-delta.md` → Information gain opportunity | One evidence-backed paragraph |

## Typical MCP tool patterns

Tool names vary by `dataforseo-mcp-server` version. Look for descriptors containing:

- **SERP** / **organic** / **google** — top ranking URLs and snippets
- **keyword** / **search volume** / **difficulty** — primary and related terms
- **related keywords** / **suggestions** — secondaries

If exact tool names differ, use MCP discover output and record which tools were called in `manifest.json` under `dataforseo_tools_used`.

## Degraded mode

Only when user explicitly approves:

- Set `manifest.json` → `"mode": "degraded"`
- Label **Fanout Research Summary** honestly in downstream brief
- Do not fabricate URLs or rankings

## Stale data (auditor refresh)

Re-run corpus build when keyword-intel artifacts are older than 30 days or before re-auditing a draft:

```powershell
python content/keyword-intel/scripts/build_serp_corpus.py --artifact-root content/keyword-intel/output/<slug>/
python content/keyword-intel/scripts/ig_audit.py --brief content/articles/<slug>/brief.html --draft content/articles/<slug>/draft.md --artifact-root content/keyword-intel/output/<slug>/
```

## SERP baseline corpus (IG audit prerequisite)

| Step | DataForSEO endpoint | Artifact |
|------|---------------------|----------|
| Top 10 + AI Overview | `serp/google/organic/live/advanced` | `serp/serp_raw.json`, `serp/ai_overview.md` |
| Page bodies | `on_page/content_parsing/live` | `serp/pages/*.md`, `serp/corpus.md` |
| Audit delta | `ig_audit.py` (deterministic) | `articles/<slug>/serp_delta.json` |

Script: [`content/keyword-intel/scripts/build_serp_corpus.py`](../../../../content/keyword-intel/scripts/build_serp_corpus.py). Uses `DATAFORSEO_*` from `agent/.env` (same credentials as MCP).
