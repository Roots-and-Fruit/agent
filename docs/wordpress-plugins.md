# WordPress plugins — server dependencies

This workspace does **not** vendor third-party plugins. Install them on WordPress (Git Updater, wp-admin, or Composer on server). Plugin **source you maintain** lives in the sibling repo **`../abilities/`**.

## rootsandfruit-abilities (our plugin)

**Source (dev):** `../abilities/` (sibling git repo)

**GitHub:** [github.com/Roots-and-Fruit/abilities](https://github.com/Roots-and-Fruit/abilities)

**Deploy to:** `wp-content/plugins/rootsandfruit-abilities/` on your WordPress site.



### Dependencies



- WordPress **6.9+** (Abilities API in core)

- **MCP Adapter** plugin (active)

- **Public Post Preview** plugin (preview abilities register only when active)

- **Block MCP by GravityKit** (`gk-block-mcp`) for block editor abilities

- **FluentSnippets** (`easy-code-manager`) for snippet management abilities

- **WP Rollback** for `rootsandfruit/plugin-update-safe`



### Block editor bridge (gk-block-mcp active)



Block abilities register on the **same MCP Adapter** surface — no second Cursor MCP server.



| Ability | Use |
|---------|-----|
| `rootsandfruit/blocks-get-page` | Read structured block tree |
| `rootsandfruit/blocks-update` | Update one block by ref or flat_index |
| `rootsandfruit/blocks-mutate` | Structural ops (insert-child, replace-block, move, …) |
| `rootsandfruit/blocks-insert` | Insert blocks at a position |
| `rootsandfruit/blocks-create-page` | Create post/page with blocks array |
| `rootsandfruit/blocks-list-patterns` | List block patterns |

Use `rootsandfruit/update-post` for **title/excerpt only** on block posts; use `blocks-*` for body edits.



### Safe plugin updates (WP Rollback active)



Requires `update_plugins` — use an administrator Application Password, not the content agent role.



Composite ability `rootsandfruit/plugin-update-safe`: capture version → update from WordPress.org → homepage smoke test → auto-rollback via WP Rollback step runner on failure.



WordPress.org outbound access is required on the host for updates to succeed.



### FluentSnippets custom abilities



Snippet MCP abilities register only when FluentSnippets is active. They wrap

`FluentSnippets\App\Helpers\Helper` with guardrails (`rf-ability` tag, draft-by-default,

`rootsandfruit/*` name validation).



Template: `../abilities/templates/rf-ability-snippet.example.php`



Register helpers (v1.2.0+): `rf_register_agent_ability()`, `rf_register_agent_abilities()` inside

`wp_abilities_api_init`. Shared category `rootsandfruit-custom` is registered by the plugin.



Requires `unfiltered_html` — use an administrator Application Password, not the agent role.



### robots.txt / llms.txt (document root)



Requires custom capability `update_robots_llms_txt` (granted to Administrator on plugin activate/upgrade).



| Ability | Use |
|---------|-----|
| `rootsandfruit/get-robots-llms-txt` | Read `robots.txt`, `llms.txt`, or `llms-full.txt` (`file`: `robots` \| `llms` \| `llms-full`) |
| `rootsandfruit/update-robots-llms-txt` | Replace file body; requires `expected_sha256` from get; update-only (no create/delete) |

Canonical local copies: `agent/content/discovery/`. Use administrator Application Password for writes.

Kill switch: `define( 'RF_ROBOTS_LLMS_TXT_WRITABLE', false );` in `wp-config.php`.



### Cursor Agent role



Use a dedicated user with a custom role. Recommended capabilities:



- `read`, `edit_posts`, `publish_posts`, `upload_files`

- `edit_published_posts`, `edit_others_posts` (if agents edit existing posts/pages)

- Do **not** grant `delete_*`, `manage_options`, `update_robots_llms_txt`, or plugin/theme caps



### Verification (from `agent/` repo root)



```powershell
.\tools\scripts\test-wordpress-mcp-http.ps1 -ExpectRfAbilities -ExpectBlocks
.\tools\scripts\audit-mcp-abilities.ps1 -ExpectBlocks
```



### GitHub / Git Updater



Plugin headers target [Roots-and-Fruit/abilities](https://github.com/Roots-and-Fruit/abilities). See `../abilities/GITHUB.md` for release zip layout.



### Deprecated



- `docs/deprecated/rootsandfruit-agent-public-preview.php` — replaced by preview abilities in the plugin.

