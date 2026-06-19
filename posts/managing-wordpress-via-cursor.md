# Managing WordPress via Cursor

A summary of the Roots & Fruit approach to operating a WordPress site through Cursor agents, based on the `rootsandfruit-abilities` plugin implementation.

## Architecture

- **Cursor** talks to the site through an **MCP server** (`@automattic/mcp-wordpress-remote`), configured in the client repo via `.cursor/mcp.json` and `.env` (URL + Application Password).
- **WordPress MCP Adapter** exposes core and third-party abilities as MCP tools; the custom **`rootsandfruit-abilities`** plugin adds a curated, R&F-specific tool surface on top of WordPress **6.9+ Abilities API**.
- **Plugin source lives in the sibling `abilities/` repo** ([Roots-and-Fruit/abilities](https://github.com/Roots-and-Fruit/abilities)); production is a deploy via Git Updater, not ad-hoc edits on the server. Cursor ops live in the **`agent/`** repo.

## Security model

- Use a **dedicated WordPress user** (e.g. “Cursor Agent”) with a **custom role** — content caps only: read, edit/publish posts, uploads; **no delete, no `manage_options`, no plugin/theme caps** (recommended).
- Each ability has a **`permission_callback`** aligned to real WordPress capabilities (`edit_posts`, `unfiltered_html`, `update_plugins`, etc.).
- **High-risk operations are split by credential**: content agent for posts; **admin Application Password** for snippets (`unfiltered_html`) and plugin updates (`update_plugins`).
- **No delete abilities** are registered — agents can create, edit, and publish, but not trash/delete via MCP.

## What agents can do (ability modules)

- **Health:** `rootsandfruit/ping` — confirms plugin version and MCP wiring.
- **Content:** list, get, create draft, update, publish — structured JSON in/out with shared schemas and error shapes.
- **Preview** (when Public Post Preview is active): enable preview link, read preview URL — replaces old mu-plugin hacks.
- **Snippets** (when FluentSnippets is active): list/get/create/update/activate/deactivate/**verify** — wraps FluentSnippets with guardrails (draft-by-default, `rf-ability` tag, name validation).
- **Plugin updates** (when WP Rollback is active): **`plugin-update-safe`** — one composite workflow: baseline version → update from wordpress.org → homepage smoke test → auto-rollback on failure.

## Design patterns

- **Server-side guardrails, not prompt hope:** validation, permissions, and workflows live in PHP; Cursor doesn’t get raw REST or arbitrary admin access.
- **Composite abilities for risky work:** plugin updates are one orchestrated tool, not a chain of low-level REST calls the agent has to get right.
- **Conditional registration:** abilities appear only when their dependency plugin is active (PPP, FluentSnippets, WP Rollback) — keeps discover honest and avoids dead tools.
- **Extensibility without redeploying the main plugin:** new agent abilities can be registered from **FluentSnippets** using `rf_register_agent_ability()` and a template snippet, then activated through the same MCP surface.
- **Cursor Skills vs WordPress abilities:** skills are **client-side** playbooks in the repo; abilities are **server-side** tools with schemas and enforcement — skills tell the agent *how*; abilities define *what’s allowed*.

## Client repo as the ops layer

- **`.env`** holds MCP URL and credentials (never committed).
- **Verification scripts** gate every environment:
  - `test-wordpress-mcp-http.ps1 -ExpectRfAbilities` — transport + R&F abilities present
  - `audit-mcp-abilities.ps1` — MCP discover matches REST ability catalog
- **Living plan** (`.cursor/plans/rf-abilities-plugin.md`) tracks phased rollout: scaffold → modules → local gates → production deploy → live audit.

## Deploy and test workflow

- **Develop locally** (e.g. WordPress Studio), sync plugin, point `.env` at local URL, run audit/smoke scripts.
- **Ship to production** by deploying the same plugin folder; activate; re-run audit/smoke against production `.env`.
- **Evidence-based sign-off:** each phase needs script output or explicit E2E (create draft → preview → publish), not “looks fine in the UI.”
- **Destructive ops on prod are intentional gaps:** full plugin update + rollback E2E is reserved for controlled admin-cred tests, not the default content agent.

## What this approach optimizes for

- **Repeatable agent operations** on a real marketing site without giving Cursor admin keys.
- **Auditability** — named abilities, schemas, and scripts you can re-run after every deploy.
- **Safe escalation path** — content automation by default; snippets and plugin maintenance via admin creds or composite tools with rollback.
- **Coexistence with other MCP tools** — MCP Adapter still exposes other plugins’ abilities; R&F adds a bounded, tested subset on top.

## Practical caveats from live testing

- Abilities may **still appear in MCP discover** for users who can’t execute them — execution fails at permission check; document which MCP user to use for which task.
- **Role caps on production must match intent** (e.g. if the agent user has `update_plugins`, it can run `plugin-update-safe`).
- **Host constraints matter** — plugin updates need outbound access to wordpress.org; local Studio may fail updates even when prod works.
- **Two MCP profiles** (agent vs admin) is the cleanest pattern when you need both content and maintenance from Cursor.

## Related paths

| Path | Role |
|------|------|
| `../abilities/` | Plugin source (separate git repo) |
| `docs/wordpress-plugins.md` | Server dependencies, roles, verification commands |
| `.cursor/mcp.json` | Cursor MCP bridge config |
| `.env.example` | MCP credential placeholders |
| `.cursor/plans/rf-abilities-plugin.md` | Implementation status and phase gates |
