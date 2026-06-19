# Cursor context stack — Roots & Fruit

How AI context layers fit together for operating rootsandfruit.com. **Do not duplicate** routing tables here — see pointers below.

## Layers

| Layer | Role | Location |
|-------|------|----------|
| **Boot (always on)** | Layout, MCP-first, legwork, boundaries | `.cursor/rules/00-rf-boot.mdc` (generated from `agent/AGENT-BOOT.md`) |
| **Session hook** | `RF_PROJECT_DIR` / `RF_AGENT_DIR` env only | `.cursor/hooks/session-boot.mjs` → `sessionStart` |
| **Guardrail hooks** | MCP reminders, PHP edit legwork | `.cursor/hooks/mcp-guard.mjs`, `after-php-edit.mjs` |
| **@Docs** | WordPress reference (API shapes, security, blocks) | Cursor Settings → Indexing & Docs |
| **Skills** | Procedures and scoped expertise | `.cursor/skills/` (workspace root) + nested `.cursor/skills/` |
| **Index (auto-loaded)** | Pointers, boundaries, deep-docs table | `agent/AGENTS.md`, parent `AGENTS.md` |
| **Site truth (on demand)** | MCP routing, parameters, recipes | `agent/agent_docs/mcp-routing.md` |
| **Abilities** | Server execution + permissions | WordPress MCP → `rootsandfruit/*` |
| **Legwork** | Verification gates | `agent/tools/scripts/*.ps1`, `php -l` |

**Cursor injects `AGENTS.md` from each workspace folder automatically** — keep `agent/AGENTS.md` short (index only). Do not restate boot or routing tables there.

**Multi-root workspace:** boot rule lives at **workspace root** `.cursor/rules/` only. Do not add `alwaysApply` boot under `agent/.cursor/rules/` — Cursor loads both and duplicates tokens.

Sync template → parent: `.\tools\scripts\sync-workspace-root.ps1` from `agent/`.

## Hooks (`.cursor/hooks.json`)

| Hook | Script | Purpose |
|------|--------|---------|
| `sessionStart` | `session-boot.mjs` | Set `RF_PROJECT_DIR`, `RF_AGENT_DIR` (no boot text — rule carries boot) |
| `beforeMCPExecution` | `mcp-guard.mjs` | MCP-first reminders on WordPress tool calls |
| `afterFileEdit` | `after-php-edit.mjs` | `php -l` + audit reminder after `abilities/**/*.php` edits |

Requires **Node** on PATH. Verify in Cursor **Settings → Hooks** or Hooks output channel after reload.

**Cloud agents:** hooks may not run — **`alwaysApply` `00-rf-boot.mdc` is the guaranteed boot layer.** Event hooks (`mcp-guard`, `after-php-edit`) may also be absent; follow boot legwork gates manually.

## Indexed @Docs (add in Cursor Settings)

Keep your existing three, and add if missing:

| Name | URL |
|------|-----|
| WordPress Abilities API | https://developer.wordpress.org/apis/abilities-api/ |
| WordPress REST API | https://developer.wordpress.org/rest-api/ |
| WordPress Common APIs | https://developer.wordpress.org/apis/ |
| Block Editor Handbook | https://developer.wordpress.org/block-editor/ |

Cursor has no repo file for @Docs — add these manually under **Settings → Indexing & Docs → Add Doc**.

## Project skills map

| Skill | Path | When it loads |
|-------|------|----------------|
| `write-a-skill` | `.cursor/skills/write-a-skill/` | User invokes `/write-a-skill` |
| `rf-wordpress-ops` | `.cursor/skills/rf-wordpress-ops/` | Site ops, content, blocks, MCP (model-invoked) |
| `rf-abilities-dev` | `abilities/.cursor/skills/rf-abilities-dev/` | Plugin work under `abilities/` (auto-scoped) |
| `wp-abilities-api` | `abilities/.cursor/skills/` | Abilities API PHP/REST (auto-scoped to `abilities/`) |
| `wp-abilities-verify` | `abilities/.cursor/skills/` | Verify registrations (auto-scoped) |
| `wp-abilities-audit` | `abilities/.cursor/skills/` | REST → abilities audit (auto-scoped) |
| `wp-plugin-development` | `abilities/.cursor/skills/` | Plugin patterns (auto-scoped) |
| `wp-rest-api` | `agent/.cursor/skills/` | REST escape hatches (auto-scoped to `agent/`) |

### Refresh upstream WordPress skills

From workspace root:

```powershell
npx skills add WordPress/agent-skills --skill wp-abilities-api wp-abilities-verify wp-abilities-audit wp-plugin-development wp-rest-api
```

Then re-copy from `.agents/skills/` into the scoped paths above (or run `agent/tools/scripts/sync-wordpress-skills.ps1`).

### Sync workspace-root to parent

From `agent/`:

```powershell
.\tools\scripts\sync-workspace-root.ps1
```

Regenerates `00-rf-boot.mdc` from `AGENT-BOOT.md` and copies hooks, rules, skills, `mcp.json`, and parent `AGENTS.md`.

## Authoring new skills

Invoke **`/write-a-skill`** before creating or editing any skill.
