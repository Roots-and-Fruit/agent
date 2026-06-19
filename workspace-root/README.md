# Sibling workspace root files

When `agent/` and `abilities/` live under a shared parent folder (e.g. `rootsandfruit-as-client/`), sync these files **up one level** to that parent:

```
rootsandfruit-as-client/
├── AGENTS.md                 ← from workspace-root/AGENTS.md
├── .cursor/mcp.json          ← from workspace-root/.cursor/mcp.json
├── .cursor/hooks.json        ← from workspace-root/.cursor/hooks.json
├── .cursor/hooks/            ← from workspace-root/.cursor/hooks/
├── .cursor/rules/            ← 00-rf-boot.mdc generated from agent/AGENT-BOOT.md
├── .cursor/skills/           ← rf-* + write-a-skill
├── .cursorignore             ← from workspace-root/.cursorignore
├── .cursorindexingignore     ← from workspace-root/.cursorindexingignore
├── rootsandfruit.code-workspace
├── agent/                    ← AGENT-BOOT.md is boot source; no always-on rule in agent/.cursor/rules/
└── abilities/
```

Cursor loads `.cursor/mcp.json`, **rules**, **hooks**, and **skills** from the **folder you opened**. Boot rule belongs at **workspace root only** (multi-root loads `agent/.cursor/rules/` too and duplicates tokens).

**Boot source:** edit `agent/AGENT-BOOT.md`, then sync. **`00-rf-boot.mdc`** is generated — do not edit by hand.

**WordPress MCP:** loads credentials from `agent/.env`.

## Sync (from `agent/`)

```powershell
.\tools\scripts\sync-workspace-root.ps1
```

Regenerates `workspace-root/.cursor/rules/00-rf-boot.mdc`, copies to parent `.cursor/`, parent `AGENTS.md`, and aligns `agent/.cursor/hooks/`. Removes duplicate `agent/.cursor/rules/00-rf-boot.mdc` if present.

**Agent folder only** (no parent workspace): `.\tools\scripts\sync-workspace-root.ps1 -AgentOnly` copies generated boot rule + hooks into `agent/.cursor/`.

See `agent/agent_docs/cursor-context-stack.md` for the full stack map.
