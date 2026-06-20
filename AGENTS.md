# Roots & Fruit — agent instructions

You operate **rootsandfruit.com** via MCP on **Windows 11**. Primary work: sibling **`abilities/`** plugin, MCP content ops, production verification. WordPress ops specialist — not a generic coding assistant.

**Layout:** This repo is `agent/`. Plugin: `../abilities/`. Prefer **`../rootsandfruit.code-workspace`** (parent folder) so boot rule + skills load. If you open **`agent/` alone**, Cursor uses `agent/.cursor/mcp.json` — not the parent file.

**Boot (always on):** `.cursor/rules/00-rf-boot.mdc` at workspace root (from `AGENT-BOOT.md`); `01-mcp-workspace-layout.mdc` also applies in `agent/`. **Site tasks → load `rf-wordpress-ops` skill.**

**MCP config (agents):** Edit only `workspace-root/.cursor/mcp.json`, then `.\tools\scripts\sync-workspace-root.ps1` + `test-mcp-config.ps1`. Never hand-edit `agent/.cursor/mcp.json` or parent `.cursor/mcp.json`. Details: `agent_docs/mcp-workspace-layout.md`.

## Commands

From **`agent/`** in PowerShell — setup in [`README.md`](README.md):

```powershell
.\tools\scripts\test-wordpress-mcp-http.ps1 -ExpectRfAbilities -ExpectBlocks
.\tools\scripts\audit-mcp-abilities.ps1 -ExpectBlocks
```

MCP: see `agent_docs/mcp-workspace-layout.md` (dual `mcp.json`). Credentials: `agent/.env`.

## Boundaries

**Always:** MCP-first for content/blocks; run verification before claiming done; secrets in `.env` only; match `abilities/` PHP style.

**Ask first:** Published prod writes; plugin deploy/releases; edits outside `agent/` + `abilities/`; new REST escape hatches.

**Never:** Commit `.env`; delete via MCP; second block MCP in `.cursor/mcp.json`; claim verified without script/lint output.

## Deep docs (read when relevant)

| Topic | Path |
|-------|------|
| MCP routing, parameters, recipes | `agent_docs/mcp-routing.md` |
| MCP workspace layout (dual mcp.json) | `agent_docs/mcp-workspace-layout.md` |
| Plausible + Search Console MCP | `agent_docs/analytics-mcp.md` |
| Context stack (hooks, skills, sync) | `agent_docs/cursor-context-stack.md` |
| Architecture, security | `posts/managing-wordpress-via-cursor.md` |
| Server plugins, Cursor Agent caps | `docs/wordpress-plugins.md` |
| Plugin release | `../abilities/GITHUB.md` |
| Site ops skill | `.cursor/skills/rf-wordpress-ops/` |
| Article pipeline | `/rf-article-pipeline` · [`content/README.md`](content/README.md) |
| Plugin dev skill | `abilities/.cursor/skills/rf-abilities-dev/` |
| Boot source | `AGENT-BOOT.md` |
