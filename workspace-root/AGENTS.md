# Roots & Fruit — Cursor workspace

Multi-repo workspace for operating [rootsandfruit.com](https://rootsandfruit.com) with Cursor agents.

```
rootsandfruit-as-client/
├── agent/       ← MCP ops, scripts, AGENT-BOOT.md (boot source)
├── abilities/   ← WordPress plugin (github.com/Roots-and-Fruit/abilities)
└── .cursor/     ← MCP, skills, rules, hooks (when parent folder is open)
```

## Start here

| Need | Path |
|------|------|
| **Boot (always on)** | `.cursor/rules/00-rf-boot.mdc` (from `agent/AGENT-BOOT.md`) |
| **Agent index** | `agent/AGENTS.md` |
| **MCP routing & recipes** | `agent/agent_docs/mcp-routing.md` |
| **Context stack** (skills, @Docs, sync) | `agent/agent_docs/cursor-context-stack.md` |

Open **`rootsandfruit.code-workspace`** or this parent folder. Sync from `agent/`: `.\tools\scripts\sync-workspace-root.ps1` — see `agent/workspace-root/README.md`.

## Non-negotiables

- **MCP abilities first** — not raw REST for content/blocks
- **Verification scripts** — done means script output, not "looks fine"
- **Secrets** in `agent/.env` only — never commit
- **Plugin deploy** — GitHub release + Git Updater, not git push alone
