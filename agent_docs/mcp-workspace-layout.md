# MCP workspace layout — dual `mcp.json`

**Problem this solves:** Cursor loads MCP config from the **folder you opened**, not from “the project” abstractly. Editing the wrong `mcp.json` makes new servers invisible in Settings.

## Folder layout

```
website/                          ← parent workspace root (open this OR rootsandfruit.code-workspace)
├── .cursor/
│   ├── mcp.json                  ← Cursor reads when parent / multi-root workspace is open
│   ├── rules/00-rf-boot.mdc
│   └── skills/
├── agent/                        ← agent repo (often opened alone in Cursor)
│   ├── .cursor/
│   │   ├── mcp.json              ← Cursor reads when agent/ folder is open
│   │   └── rules/01-mcp-workspace-layout.mdc
│   ├── .env                      ← all MCP secrets (never commit)
│   └── workspace-root/           ← **single source of truth** for parent .cursor/*
│       └── .cursor/mcp.json
└── abilities/
```

## Path convention

| Open mode | `${workspaceFolder}` | Launcher path in `mcp.json` |
|-----------|----------------------|-----------------------------|
| Parent or `rootsandfruit.code-workspace` | `website/` | `${workspaceFolder}/agent/tools/scripts/run-*.mjs` |
| `agent/` folder only | `website/agent/` | `${workspaceFolder}/tools/scripts/run-*.mjs` |

Same scripts, different prefix. **`sync-workspace-root.ps1` generates both files** from one template.

## Rules for humans and agents

1. **Edit only** `agent/workspace-root/.cursor/mcp.json` when adding/removing MCP servers.
2. **Run** `.\tools\scripts\sync-workspace-root.ps1` from `agent/`.
3. **Reload Cursor** after sync.
4. **Never** edit `website/.cursor/mcp.json` or `agent/.cursor/mcp.json` by hand — they are outputs.
5. **Verify** with `.\tools\scripts\test-mcp-config.ps1`.
6. **Global** `~/.cursor/mcp.json` is separate (user-wide). Project servers belong in the template above.

## Session env (hooks)

`session-boot.mjs` sets:

| Variable | Meaning |
|----------|---------|
| `RF_PROJECT_DIR` | Cursor project directory |
| `RF_AGENT_DIR` | Path to `agent/` (repo root for scripts) |
| `RF_WORKSPACE_OPEN_MODE` | `parent-or-workspace` or `agent-only` |
| `RF_MCP_CONFIG_ACTIVE` | Which `mcp.json` Cursor should be using this session |

## Recommended open mode

Prefer **`rootsandfruit.code-workspace`** from the parent folder — boot rule, skills, hooks, and parent `mcp.json` load together. Opening `agent/` alone still works if sync kept `agent/.cursor/mcp.json` current.

## Related

- Sync: `agent/tools/scripts/sync-workspace-root.ps1`
- Stack map: `agent/agent_docs/cursor-context-stack.md`
- Analytics MCP: `agent/agent_docs/analytics-mcp.md`
