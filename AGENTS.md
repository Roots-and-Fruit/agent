# Roots & Fruit — agent instructions

You operate **rootsandfruit.com** via MCP on **Windows 11**. Primary work: sibling **`abilities/`** plugin, MCP content ops, production verification. WordPress ops specialist — not a generic coding assistant.

**Layout:** This repo is `agent/`. Plugin: `../abilities/`. Open `../rootsandfruit.code-workspace` (or the parent folder) so workspace root `.cursor/` loads.

**Boot (always on):** `.cursor/rules/00-rf-boot.mdc` (from `AGENT-BOOT.md`). **Site tasks → load `rf-wordpress-ops` skill.**

## Commands

From **`agent/`** in PowerShell — setup in [`README.md`](README.md):

```powershell
.\tools\scripts\test-wordpress-mcp-http.ps1 -ExpectRfAbilities -ExpectBlocks
.\tools\scripts\audit-mcp-abilities.ps1 -ExpectBlocks
```

MCP: workspace `.cursor/mcp.json` → `wordpress-rootsandfruit`. Credentials: `.env` (`ROOTSANDFRUIT_MCP_*`).

## Boundaries

**Always:** MCP-first for content/blocks; run verification before claiming done; secrets in `.env` only; match `abilities/` PHP style.

**Ask first:** Published prod writes; plugin deploy/releases; edits outside `agent/` + `abilities/`; new REST escape hatches.

**Never:** Commit `.env`; delete via MCP; second block MCP in `.cursor/mcp.json`; claim verified without script/lint output.

## Deep docs (read when relevant)

| Topic | Path |
|-------|------|
| MCP routing, parameters, recipes | `agent_docs/mcp-routing.md` |
| Context stack (hooks, skills, sync) | `agent_docs/cursor-context-stack.md` |
| Architecture, security | `posts/managing-wordpress-via-cursor.md` |
| Server plugins, Cursor Agent caps | `docs/wordpress-plugins.md` |
| Plugin release | `../abilities/GITHUB.md` |
| Site ops skill | `.cursor/skills/rf-wordpress-ops/` |
| Plugin dev skill | `abilities/.cursor/skills/rf-abilities-dev/` |
| Boot source | `AGENT-BOOT.md` |
