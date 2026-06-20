# Baseline / Delta Report — cursor-wp-mcp-abilities

Primary keyword: **wordpress mcp server** (210/mo US, KD 22, LOW competition)  
Secondary: **wordpress abilities api** (70/mo, rising trend)  
Data: DataforSEO SERP + keyword overview, 2026-06-19

## Baseline (table stakes in top results)

- Define MCP and why WordPress sites expose tools to AI agents
- Point to official **MCP Adapter** + **Abilities API** (developer.wordpress.org, GitHub)
- Install/configure a generic MCP plugin or remote server (Automattic wordpress-mcp, @automattic/mcp-wordpress-remote)
- Claude Desktop or Cursor **Settings → MCP** wiring (JSON config, Application Passwords)
- Listicles of “best WordPress MCP servers” without production guardrails
- Video walkthroughs: connect AI to WordPress in ~5 minutes (no least-privilege model)

## Delta (gaps R&F can win)

1. **Curated abilities vs raw REST** — competitors expose broad MCP/REST; few document a **custom `rootsandfruit/*` ability surface** with permission callbacks and no delete paths
2. **Single MCP + in-process blocks** — avoid second Node block MCP; `blocks-*` via plugin bridge (GravityKit Block MCP in PHP)
3. **Agent ops pipeline** — keyword research → brief → draft → audit → **blocks-create-page** + **set-post-author** + public preview (end-to-end on a live site)
4. **Production guardrails** — draft-first, ask before publish, Breeze cache after byline, verification scripts (`test-wordpress-mcp-http.ps1`)

## Friction

- Readers confuse **WordPress.com MCP** docs with **self-hosted** Cloudways/Kadence stacks
- Multiple MCP servers (WordPress remote + block MCP + DataforSEO) without a routing story
- Fear of AI “taking over” production (Reddit threads) — need explicit draft/preview gates
- Abilities API is new (6.9+); developers don’t know **abilities vs REST escape hatches**

## Information gain opportunity

Publish a **self-hosted, operator-focused** walkthrough: Cursor → one `wordpress-rootsandfruit` MCP → MCP Adapter → custom Abilities plugin → block insert with `innerHTML` → public preview → explicit publish. Show real ability names and what intentionally **is not** exposed (delete, cache purge). This is more specific than GitHub READMEs or listicles and matches how rootsandfruit.com actually ships content.
