# Run a WordPress MCP Server in Cursor With Curated Abilities

I kept hitting the same wall with WordPress MCP tutorials: “connect Claude to your site in five minutes.” That line gets you a working demo. It does not get you a production workflow you would trust on a live blog—and when you are the only person running the site, that gap matters.

I run [rootsandfruit.com](https://rootsandfruit.com/) as a one-person shop: self-hosted WordPress on Cloudways, Kadence, Breeze cache. I connect Cursor through **one** MCP server. I call **curated** `rootsandfruit/*` abilities instead of opening the whole REST surface to an agent. And I do not publish until I have read a public preview myself.

So in this article I am going to walk you through the stack I actually use—not a theoretical setup. Take what fits your site. Leave what does not.

## Why generic MCP tutorials left me wanting more

When I searched “wordpress mcp server,” most results fell into three buckets: MCP explainers, links to Automattic’s [wordpress-mcp](https://github.com/Automattic/wordpress-mcp) repo, and listicles of MCP servers. All of that is useful for a first connection. Once you are already publishing, though, it gets thin—because almost none of it talks about what an agent *should not* be able to do.

That is the part I had to learn the hard way. Here are the four gaps that kept showing up for me:

- **Least privilege.** Broad MCP plugins expose a lot of tools. I wanted agents to help with content—not wander the whole install.
- **Block editor reality.** Dumping HTML into `post_content` via REST breaks Gutenberg structure. Body edits need block-aware tools.
- **Publish gates.** A preview URL is not the live URL. I needed an explicit approve step, plus a plan for byline and cache.
- **Self-hosted vs hosted.** WordPress.com MCP docs do not map cleanly to my Cloudways stack. Follow the wrong guide and you lose an afternoon.

Once I named those gaps, the design choice got clearer. I stopped treating MCP as a magic pipe to “the whole site.” I started building a narrow, reviewed surface instead—and that decision shapes everything below.

## MCP, Abilities API, and MCP Adapter (plain language)

Before we get into my architecture, it helps to align on three terms. They show up in every official doc, and I found it easier to move fast once I had a plain-language read on each one.

**Model Context Protocol (MCP)** is how Cursor (or Claude Desktop) talks to external tools. On WordPress, those tools are things like “create a draft,” “insert a paragraph block,” or “enable a public preview link.” Think of MCP as the wire between your editor and your site.

WordPress 6.9+ adds the **[Abilities API](https://developer.wordpress.org/apis/abilities-api/)**. That is where *you* register named abilities in PHP—with schemas, permission callbacks, and execute handlers. Your site decides what exists. A generic client does not get to guess.

From there, the **[MCP Adapter](https://github.com/wordpress/mcp-adapter)** ([announcement](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)) exposes those registered abilities to MCP clients. Cursor sees them as tools. WordPress still enforces capabilities on every call. That last point is important: MCP does not bypass WordPress permissions, and I would not want it to.

On my site, the chain looks like this:

1. **My abilities plugin** ([Roots-and-Fruit/abilities](https://github.com/Roots-and-Fruit/abilities)) registers `rootsandfruit/*` abilities.
2. **MCP Adapter** (separate plugin) bridges them to MCP.
3. **Cursor** connects with one entry in `.cursor/mcp.json`, authenticated via Application Password.

You still need WordPress 6.9+, both plugins active, and a user with the right capabilities. With that foundation in place, the next question is how many MCP servers you actually need—which is where a lot of setups get messy.

## Architecture: one Cursor MCP to rootsandfruit.com

Early on I asked myself a simple question: how many MCP servers should Cursor talk to for one WordPress site? My answer today is **one**: `wordpress-rootsandfruit`. No second Node process for blocks.

Here is the flow I settled on:

```
Cursor IDE
    │
    ▼  MCP (Application Password)
wordpress-rootsandfruit
    │
    ▼
MCP Adapter plugin
    │
    ▼
rootsandfruit-abilities plugin  ──►  rootsandfruit/* abilities
    │
    └──►  GK Block MCP (in-process PHP)  ──►  blocks-* abilities
```

I did consider adding `@gravitykit/block-mcp` as a second Cursor MCP. In the end I skipped it. Block operations already run in-process through my plugin’s bridge to GravityKit Block MCP. A second server would duplicate config, split routing (“REST here, Node MCP there”), and make agent instructions harder to keep safe.

So I kept one server, one routing doc, and one workflow I can explain in a single blog post. From there I split responsibilities on purpose: block work goes through `rootsandfruit/blocks-*`; title and excerpt go through `rootsandfruit/update-post`. I enforce that split in my agent rules.

That routing split only makes sense once you know *which* abilities exist—which brings us to the curated list I actually expose.

## Curated `rootsandfruit/*` abilities (what I expose—and what I don’t)

Generic MCP setups often mirror large parts of the REST API. I took the opposite approach: a **small, reviewed set** of abilities with explicit permission checks on each one.

The live list grows as I ship plugin releases. After every deploy I run `audit-mcp-abilities.ps1` or MCP discover to confirm what Cursor actually sees—because the doc you write and the tools Cursor discovers should match.

| Module | Abilities | Permission basis | How I use them |
|--------|-----------|------------------|----------------|
| Health | `ping` | read | Smoke test; confirms plugin version and block bridge |
| Content | `list-posts`, `get-post`, `create-draft`, `update-post`, `publish-post`, `set-post-author` | `edit_posts` / `edit_post` / `publish_posts` / `edit_others_posts` | Shell drafts, title/excerpt, byline, publish |
| Preview | `enable-public-preview`, `get-public-preview-url` | `edit_post` | Shareable preview before go-live |
| Blocks | `blocks-get-page`, `blocks-update`, `blocks-mutate`, `blocks-insert`, `blocks-create-page`, `blocks-list-patterns` | `edit_post` | All post **body** edits |
| Snippets | `snippets-list`, … | `unfiltered_html` | Admin-only; separate credential profile |
| Plugins | `plugin-update-safe` | `update_plugins` | Admin-only updates |

The table shows what I *do* expose. The omissions matter just as much.

**What I deliberately left out:** post delete, trash, cache purge. Agents cannot remove content through my MCP surface. Breeze cache clears stay manual—I purge after byline changes so logged-out preview matches what I expect.

**REST escape hatches** still exist for gaps I have not codified in the plugin yet. For day-to-day content I stick to `rootsandfruit/*`—especially `blocks-*` for body and `set-post-author` for bylines (v1.5.1+).

When an agent call comes in, I route it with a simple rule of thumb: block markup → `blocks-*`; title, excerpt, or status → `update-post` / `publish-post`; byline → `set-post-author`. That rule saves me from the most common mistake in this stack—which is trying to push body HTML through the wrong ability.

## Self-hosted vs WordPress.com MCP

Even with the right abilities registered, I still see people follow the wrong setup guide—and that usually traces back to hosted vs self-hosted confusion.

WordPress.com documents MCP in a **hosted** context. My site is **self-hosted**: my plugins, my Application Passwords, my Cloudways server, my cache layer. Same vocabulary on the page, different moving parts behind it.

If you are on Cloudways, Kadence, or a similar stack, follow Abilities API + MCP Adapter + your own abilities plugin—not a WordPress.com-only setup guide. The mental model is the same (MCP tools → WordPress). The install paths, credentials, and cache behavior are not.

I see the mismatch in forums all the time: “I connected MCP but my blocks are wrong” or “preview works logged-in only.” In most cases it is the wrong doc path, a missing block bridge, or skipping public preview entirely. Once you are on the right path for self-hosted, the next friction point is usually *how* body content gets written—which is where Gutenberg rules kick in.

## Block body rules: `innerHTML`, not HTML via `update-post`

Gutenberg stores posts as block comments and structured JSON—not a single HTML blob. That is why **`rootsandfruit/update-post` is for title, excerpt, and status—not body HTML.** If you try to shove the article body through `update-post`, you are fighting the editor instead of working with it.

Body work on my site flows through block abilities instead:

- **`blocks-create-page`** — draft shell when I am starting from markdown.
- **`blocks-get-page`** — read the block tree before I mutate anything.
- **`blocks-insert`** — add blocks; for static blocks like `core/heading` and `core/paragraph`, include **`innerHTML`** or you get empty paragraphs on save.
- **`blocks-mutate`** — targeted edits when I know block IDs.

Blank paragraphs after an agent run? Nine times out of ten someone skipped `innerHTML`. That is why I verify with `blocks-get-page` after every insert—it is a quick sanity check before I move on to preview.

Getting blocks right is only half the publish story, though. The other half is the human gate between draft and live.

## Draft → author → public preview → publish gate

Here is how I think about the handoff: agents edit **drafts**; I approve **publish**; preview is the checkpoint between those two.

This is the checklist I run on rootsandfruit.com before anything goes live:

1. **`blocks-create-page`** (or `create-draft` + block insert) — draft shell with block body.
2. **`blocks-get-page`** — verify structure; confirm headings and paragraphs in block JSON.
3. **`set-post-author`** — assign the WordPress user that should appear on the byline.
4. **Purge Breeze cache** — manual, after byline change, so logged-out preview is trustworthy.
5. **`enable-public-preview`** — tokenized URL I can share without handing out wp-admin.
6. **STOP** — I read the preview URL; voice, links, and information-gain commitments have to clear the bar.
7. **`publish-post`** — only when I explicitly say go.

Step 6 is the one I treat as non-negotiable. A public preview URL is **not** the live permalink. I treat preview as the last read-through, not shipping.

Before I run any of that, I start with **`ping`** and expect `block_mcp_active: true` when the block bridge is live. If that fails, I fix the bridge first—there is no point building a draft on a broken path.

## Verify your setup, then ship a draft

If you wire Cursor MCP the way I describe here, I would start with proof—not faith. Here is the sequence I use:

1. Run **`rootsandfruit/ping`** via MCP and confirm plugin version (1.5.1+ if you need `set-post-author`).
2. From your agent repo, run smoke scripts against production discover:
   ```powershell
   .\tools\scripts\test-wordpress-mcp-http.ps1 -ExpectRfAbilities -ExpectBlocks
   .\tools\scripts\audit-mcp-abilities.ps1 -ExpectBlocks
   ```
3. Ship your first piece as **draft + preview**, not straight to publish.

Plugin source and ability registrations: [github.com/Roots-and-Fruit/abilities](https://github.com/Roots-and-Fruit/abilities). Official references: [MCP Adapter](https://github.com/wordpress/mcp-adapter), [Abilities API](https://developer.wordpress.org/apis/abilities-api/).

If you are building a similar stack, start narrow—one MCP server, a short ability list, preview before publish. That is how I keep a solo operation moving without pretending I have a platform team behind me. Get the first draft live in preview, read it like a reader would, and iterate from there.

---

## Draft QA Summary

| Gate | Result | Notes |
|------|--------|-------|
| Delta Preservation | Pass | §3 architecture diagram; §4 abilities table + no-delete; §7 publish checklist |
| Voice Fidelity | Pass | First-person founder; slower pace; explicit section bridges |
| Structure | Pass | Matches brief Page Structure §1–§8 |
| Evidence Safety | Pass | Ability names from mcp-routing.md; no fabricated stats; external links are real |

**Brief IG score:** 9/10 (inherited)  
**Writer self-check:** all three delta artifacts present; transitions tee up next section (gaps → terms → architecture → abilities → hosting → blocks → publish → verify).

---

## Voiceprint Audit

- Voice Match Check: 10/10
- Revised in place: yes (pacing + transition hand-holding pass)
- Residual voice risks: §4 table stays list-heavy (brief-required artifact); watch length if combined with “deep” draft depth later
