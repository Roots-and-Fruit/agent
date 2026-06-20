---
name: rf-wordpress-ops
description: Operate rootsandfruit.com MCP-first. Use when managing WordPress content, block posts, drafts, previews, plugin smoke tests, or site ops — mentions rootsandfruit.com, execute-ability, blocks-mutate, public preview, or Breeze cache.
---

# R&F WordPress ops

**Predictability:** every site task follows classify → **ability** (or **escape hatch**) → **legwork** → site post-steps.

Authoritative routing: `agent/AGENTS.md` and `agent/agent_docs/mcp-routing.md`. Do not restate full ability tables here.

## 1. Classify the task

| Signal | Path |
|--------|------|
| Block body, patterns, Gutenberg tree | `rootsandfruit/blocks-*` |
| Title or excerpt only | `rootsandfruit/update-post` |
| Listed `rootsandfruit/*` workflow | `mcp-adapter-execute-ability` |
| No ability (cache purge, …) | **escape hatch** — WP REST |

**Block posts:** never push body HTML through `update-post`.

**Done when:** path is named (ability id or REST route) before any write.

## 2. Credential profile

| Profile | Use for |
|---------|---------|
| Content agent (`.env` default) | Posts, blocks, preview, drafts |
| Admin Application Password | `snippets-*`, `plugin-update-safe` |

Discover may list abilities the user cannot execute — execution fails at `permission_callback`.

**Done when:** profile matches the chosen ability's permission basis.

## 3. Execute

1. Block edits: `blocks-get-page` before mutate/update/insert.
2. `blocks-insert` / static block updates: include **`innerHTML`** with attributes or GK rejects the save.
3. Prefer **drafts** for E2E on production; ask before writes to published content.
4. No delete abilities — do not trash/delete via MCP.

**Done when:** MCP response received or REST response for escape hatch.

## 4. Legwork

From `agent/` in PowerShell when MCP wiring or deploy changed:

```powershell
.\tools\scripts\test-wordpress-mcp-http.ps1 -ExpectRfAbilities -ExpectBlocks
.\tools\scripts\audit-mcp-abilities.ps1 -ExpectBlocks
```

After plugin PHP edits in `abilities/`:

```powershell
php -l ..\abilities\<touched-file>.php
```

**Done when:** relevant commands exit 0, or manual E2E steps are documented with observable results.

## 5. Site post-steps

- **Breeze:** after author or byline-affecting meta, purge cache before sharing **logged-out** public preview URLs.
- **Preview:** `enable-public-preview` → test incognito.
- **Article publish:** full draft → blocks → preview flow → `/rf-article-publish` skill.
- **Catalog:** run audit after deploys — do not hardcode ability lists in chat.

**Done when:** post-steps applied or explicitly N/A for the task.

## Anti-patterns

- Second `@gravitykit/block-mcp` Node MCP — block work stays on `rootsandfruit/blocks-*`.
- Claiming verified without script output or named manual checks.
- Generic block-plugin scaffolding — use upstream `wp-block-development` only when building new blocks in code, not for content ops.
