# Cursor context stack — Roots & Fruit

How AI context layers fit together for operating rootsandfruit.com. **Do not duplicate** routing tables here — see pointers below.

## Layers

| Layer | Role | Location |
|-------|------|----------|
| **@Docs** | WordPress reference (API shapes, security, blocks) | Cursor Settings → Indexing & Docs |
| **Skills** | Procedures and scoped expertise | `.cursor/skills/` (workspace root) + nested `.cursor/skills/` |
| **Site truth** | R&F routing, credentials, boundaries | `agent/AGENTS.md`, `agent/agent_docs/mcp-routing.md` |
| **Abilities** | Server execution + permissions | WordPress MCP → `rootsandfruit/*` |
| **Legwork** | Verification gates | `agent/tools/scripts/*.ps1`, `php -l` |

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

## Authoring new skills

Invoke **`/write-a-skill`** before creating or editing any skill.
