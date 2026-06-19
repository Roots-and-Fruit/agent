# Sibling workspace root files

When `agent/` and `abilities/` live under a shared parent folder (e.g. `rootsandfruit-as-client/`), copy these files **up one level** to that parent:

```
rootsandfruit-as-client/
├── .cursor/mcp.json          ← from workspace-root/.cursor/mcp.json
├── .cursor/skills/           ← from workspace-root/.cursor/skills/ (project skills)
├── .cursorignore             ← from workspace-root/.cursorignore
├── .cursorindexingignore     ← from workspace-root/.cursorindexingignore
├── rootsandfruit.code-workspace
├── agent/
└── abilities/
```

Cursor only loads `.cursor/mcp.json` and discovers `.cursor/skills/` from the **folder you opened**. Nested `agent/.cursor/skills/` and `abilities/.cursor/skills/` auto-scope to those folders.

Copy skills to the parent for repo-wide ops skills; upstream WordPress skills live under `abilities/.cursor/skills/` (see `agent/agent_docs/cursor-context-stack.md`).

**GROOT paths:** `groot` and `groot-mapper` MCP entries point at `c:/Users/reach/GROOT`. Edit or remove them if you clone without the GROOT monorepo.

**WordPress MCP:** loads credentials from `agent/.env`.
