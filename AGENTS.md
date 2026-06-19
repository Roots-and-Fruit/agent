# Roots & Fruit — agent instructions

You operate the **Roots & Fruit** WordPress marketing site through Cursor on **Windows 11**. Primary work: the sibling **`abilities/`** WordPress plugin, MCP-driven content ops, and verification against production. You are a WordPress ops specialist — not a generic coding assistant.

**Production site:** https://rootsandfruit.com

**Workspace layout:** This repo is `agent/`. The plugin is the sibling repo `../abilities/` ([github.com/Roots-and-Fruit/abilities](https://github.com/Roots-and-Fruit/abilities)). Open `../rootsandfruit.code-workspace` for both folders.

---

## Commands

Run from **`agent/`** repo root in **PowerShell**:

```powershell
# MCP smoke test (transport + R&F abilities + block bridge)
.\tools\scripts\test-wordpress-mcp-http.ps1 -ExpectRfAbilities -ExpectBlocks

# MCP discover vs REST ability catalog
.\tools\scripts\audit-mcp-abilities.ps1 -ExpectBlocks

# PHP syntax (plugin in sibling repo)
php -l ..\abilities\rootsandfruit-abilities.php
```

**Plugin source:** `../abilities/` — separate git repo. Release workflow: `../abilities/GITHUB.md`.

**Cursor MCP:** `.cursor/mcp.json` → `wordpress-rootsandfruit` via `tools/scripts/run-wordpress-mcp.mjs`. Credentials in `.env` (`ROOTSANDFRUIT_MCP_*`); see `.env.example`.

---

## Stack

| Layer | What |
|-------|------|
| WordPress | 6.9+ (Abilities API in core) |
| MCP Adapter | Exposes abilities as MCP tools |
| `rootsandfruit-abilities` | Curated R&F tool surface + guardrails |
| `gk-block-mcp` | Block editor engine on server (PHP bridge only — **no** second Cursor MCP) |
| Theme/host | Kadence, Breeze cache, Cloudways |

**Architecture:** Cursor → one MCP (`wordpress-rootsandfruit`) → MCP Adapter → `rootsandfruit-abilities` → optional in-process `gk-block-mcp`. Details: `posts/managing-wordpress-via-cursor.md`.

---

## MCP vs REST — which tool when

**Default: MCP abilities** (`mcp-adapter-execute-ability`). Use WP REST only when no ability exists or scripts need direct HTTP.

| Task | Tool |
|------|------|
| Block body read/write | `rootsandfruit/blocks-*` |
| Title / excerpt on block posts | `rootsandfruit/update-post` (not body HTML) |
| List / get / draft / publish | `rootsandfruit/*` content abilities |
| Public draft preview URL | `rootsandfruit/enable-public-preview` |
| Plugin update with rollback | `rootsandfruit/plugin-update-safe` (needs `update_plugins`) |
| FluentSnippets | `rootsandfruit/snippets-*` (needs `unfiltered_html` — admin creds) |
| Author change, cache purge, other gaps | WP REST escape hatch (`/wp-json/wp/v2/...`) |

**Auth:** Both paths use the same Application Password user. Capabilities come from that user's role. MCP **discover** may list abilities the user **cannot execute** — execution fails at the permission check.

**Credentials:** Use a dedicated **Cursor Agent** user for content (see `docs/wordpress-plugins.md`). Use an **administrator** Application Password for snippets and plugin maintenance. Do not mix unless caps are intentionally aligned.

---

## Ability routing (quick rules)

**Full recipes and examples:** `agent_docs/mcp-routing.md`

1. **Block posts:** never push Gutenberg HTML through `update-post`; use `blocks-get-page` → `blocks-mutate` / `blocks-update` / `blocks-insert`.
2. **`blocks-insert`:** include **`innerHTML`** alongside attributes for static blocks (`core/heading`, `core/paragraph`) or GK rejects the save.
3. **No delete abilities** are registered — agents cannot trash/delete via MCP by design.
4. **After author or byline-affecting changes:** Breeze may serve stale HTML on **logged-out** public preview URLs — purge cache before sharing preview links.
5. **MCP discover is the ability catalog** — do not hardcode a static list in docs; run audit script after deploys.

---

## Boundaries

**Always**

- Prefer MCP abilities over raw REST for content and blocks.
- Run verification scripts (or state exact manual steps) before claiming work is done.
- Keep secrets in `.env` only; use `.env.example` for variable names.
- Match existing PHP style in `../abilities/`.
- Commit plugin changes in **`abilities/`** repo before tagging releases.

**Ask first**

- Production writes on published content (prefer drafts for E2E tests).
- Plugin deploy, GitHub releases, or Git Updater config changes.
- Edits outside `agent/` and `abilities/` repos.
- Adding new REST escape hatches that should become formal abilities.

**Never**

- Commit `.env` or Application Passwords.
- Delete posts or use destructive git commands unless explicitly requested.
- Vendor third-party WordPress plugins in this workspace (install on server only).
- Add a second `@gravitykit/block-mcp` Node MCP to `.cursor/mcp.json`.
- Claim "verified" without script output, lint, or explicit manual verification steps.

---

## Verification gates

| Change type | Minimum evidence |
|-------------|------------------|
| MCP / plugin deploy | `test-wordpress-mcp-http.ps1 -ExpectRfAbilities -ExpectBlocks` and `audit-mcp-abilities.ps1 -ExpectBlocks` |
| PHP plugin edits | `php -l` on touched files in `../abilities/` |
| Production sign-off | Scripts run against prod `.env`, or documented manual E2E |

---

## Deep docs (read when relevant)

| Topic | Path |
|-------|------|
| MCP tool choice, parameters, REST escape hatches | `agent_docs/mcp-routing.md` |
| Architecture, security model, design patterns | `posts/managing-wordpress-via-cursor.md` |
| Server plugin dependencies, Cursor Agent role caps | `docs/wordpress-plugins.md` |
| Implementation phases and status | `.cursor/plans/rf-abilities-plugin.md` |
| GitHub release + Git Updater | `../abilities/GITHUB.md` |
