# Cursor context stack — Roots & Fruit



How AI context layers fit together for operating rootsandfruit.com. **Do not duplicate** routing tables here — see pointers below.



## Layers



| Layer | Role | Location |

|-------|------|----------|

| **Boot (always on)** | Layout, MCP-first, legwork, boundaries | `.cursor/rules/00-rf-boot.mdc` (generated from `agent/AGENT-BOOT.md`) |

| **MCP layout (always on)** | Dual `mcp.json`; template + sync | `.cursor/rules/01-mcp-workspace-layout.mdc` + `agent/.cursor/rules/` copy |

| **Session hook** | `RF_PROJECT_DIR`, `RF_AGENT_DIR`, `RF_WORKSPACE_OPEN_MODE`, `RF_MCP_CONFIG_ACTIVE` | `.cursor/hooks/session-boot.mjs` → `sessionStart` |

| **Guardrail hooks** | MCP reminders, PHP + mcp.json edit legwork | `mcp-guard.mjs`, `after-php-edit.mjs`, `after-mcp-json-edit.mjs` |

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

| `sessionStart` | `session-boot.mjs` | Set `RF_PROJECT_DIR`, `RF_AGENT_DIR`, `RF_WORKSPACE_OPEN_MODE`, `RF_MCP_CONFIG_ACTIVE` |

| `beforeMCPExecution` | `mcp-guard.mjs` | MCP-first reminders on WordPress tool calls |

| `afterFileEdit` | `after-php-edit.mjs` | `php -l` + audit reminder after `abilities/**/*.php` edits |

| `afterFileEdit` | `after-mcp-json-edit.mjs` | Remind template + sync when any `mcp.json` is edited |



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



## MCP servers



| Server | Use | Credentials |

|--------|-----|-------------|

| `wordpress-rootsandfruit` | Site ops, blocks, publish | `ROOTSANDFRUIT_MCP_*` in `agent/.env` |

| `dataforseo` | Article keyword/SERP research | `DATAFORSEO_*` in `agent/.env` |

| `plausible` | Traffic, conversions, realtime visitors | `PLAUSIBLE_API_KEY` in `agent/.env` |

| `searchconsole` | GSC queries, indexing, URL inspection | Google ADC (`gcloud` login on this machine) |



Launchers: `run-wordpress-mcp.mjs`, `run-dataforseo-mcp.mjs`, `run-plausible-mcp.mjs`, `run-searchconsole-mcp.mjs`. Routing: `agent/agent_docs/analytics-mcp.md`.

**Config source of truth:** `agent/workspace-root/.cursor/mcp.json` only — sync generates parent and `agent/.cursor/mcp.json`. See `agent/agent_docs/mcp-workspace-layout.md`. Parity: `.\tools\scripts\test-mcp-config.ps1`.



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



### Article pipeline skills (`agent/.cursor/skills/`)



User-invoked only (`disable-model-invocation: true`). Orchestrator: **`/rf-article-pipeline`**. Layout: [`content/README.md`](../content/README.md).



| Skill | When |

|-------|------|

| `rf-article-pipeline` | Full workflow map + STOP gates + `--from` resume |

| `voiceprint` | Once / voice refresh |

| `rf-keyword-research` | DataforSEO → `keyword-intel/output/<slug>/` |

| `grill-info-gain` | Info Gain Handoff |

| `content-brief` | `brief.html` (voiceprint required) |

| `article-writer` | `draft.md` |

| `voiceprint-audit` | Auto-revise draft before user review |

| `information-gain-auditor` | `ig-audit.html` + JSON (before publish) |

| `rf-article-publish` | blocks → author → preview → publish on OK |



Legwork: `python content/keyword-intel/scripts/ig_audit.py …` from `agent/`.



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

