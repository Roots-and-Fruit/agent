---
name: rf-article-publish
description: Convert approved draft.md to Gutenberg blocks on rootsandfruit.com, set author, enable public preview, publish on explicit approval. User invokes with /rf-article-publish.
disable-model-invocation: true
---

# R&F article publish

**Predictability:** approved local draft → MCP draft post with blocks → author set → public preview URL → STOP → publish only on explicit user OK.

Block mapping rules: [REFERENCE.md](REFERENCE.md). WordPress routing: [`agent_docs/mcp-routing.md`](../../../agent_docs/mcp-routing.md).

## When to use

- After `/information-gain-auditor` (or user override)
- Resuming preview or publish for an existing slug
- Block edits on an existing draft post (mutate path)

## Procedure

### 1. Collect inputs

1. Slug: `content/articles/<keyword-slug>/`.
2. `brief.html`, `draft.md`, `ig-audit.json`.
3. **Author:** default **`1`** (site founder on rootsandfruit.com). Override only when the user specifies another login or ID.
4. Mode: `preview` (default) or `publish` (only after prior preview + explicit user approval).

**Done when:** paths confirmed; use author `1` unless overridden in chat.

### 2. Gate

- `brief.html` pre-publish score ≥8, or user override logged in chat.
- `ig-audit.json` recommendation `publish-ready` (or `revise-once` with user override), or user override logged.

**Done when:** gate passed or override documented.

### 3. Map draft to blocks

Read [REFERENCE.md](REFERENCE.md). Site block defaults: [`content/block-defaults.json`](../../../content/block-defaults.json).

**One command (preferred):**

```powershell
python tools/scripts/publish-article-preview.py content/articles/<slug>/
```

Runs: `draft-md-to-blocks.py` → `blocks-create-page` → author **1** → public preview → writes `preview.json`. Python only — no npm.

Manual steps only if debugging — see REFERENCE.md.

**Done when:** `preview.json` exists with `preview_url`.

### 4. Create or update WordPress draft

**New post (preferred):** one-shot via Python (UTF-8 safe):

```powershell
python tools/scripts/invoke-mcp-ability.py rootsandfruit/blocks-create-page content/articles/<slug>/blocks-payload.json
```

Payload comes from `draft-md-to-blocks.py`. Do **not** pipe large JSON through PowerShell `Get-Content` without `-Encoding UTF8`.

**Existing post_id:** prefer a fresh `blocks-create-page` when block tree is corrupted; otherwise `repair-blocks-payload.py` (uses ref-based replace for lists/tables).

**Done when:** MCP returns `post_id`.

### 5. Verify blocks

`rootsandfruit/blocks-get-page` — confirm block count and heading structure match draft sections.

**Done when:** tree matches intent or fixes applied.

### 6. Set author

`rootsandfruit/set-post-author` with `post_id` and `author` (default **`1`**).

If ability unavailable (pre-deploy): REST escape hatch per mcp-routing.md — document in chat.

**Done when:** author matches requested user; note Breeze purge reminder from ability response.

### 7. Public preview

`rootsandfruit/enable-public-preview` with `post_id`.

Return to user: `post_id`, `preview_url`, `edit_url` (also in `preview.json`).

**STOP** — do not call `publish-post` in preview mode.

**Done when:** `preview_url` shared; user reminded to test logged-out/incognito and purge Breeze if byline stale.

### 7b. Convert code blocks (human — before publish approval)

MCP inserts **`core/code`**. Code Block Pro styling is applied in the editor, not via MCP.

1. Open **`edit_url`** from `preview.json` (or `wp-admin/post.php?post={id}&action=edit`).
2. Focus each code block → block toolbar → **Convert to Code Pro**.
3. **Save** the draft (Shiki + site defaults run on save).
4. Re-check **`preview_url`** logged out if you care about front-end code styling.

Skip if plain `core/code` is acceptable for this article.

**Done when:** user confirms convert step done or skipped.

### 8. Publish (explicit approval only)

When user explicitly approves after preview review:

`rootsandfruit/publish-post` with `post_id`.

**Done when:** post status `publish` confirmed via `get-post`; live URL returned.

## Pointers (do not duplicate)

- Orchestrator: `/rf-article-pipeline`
- Generic site ops: `/rf-wordpress-ops` (non-article tasks)

## Anti-patterns

- `publish-post` before preview STOP
- Body HTML via `update-post`
- Blocks without `innerHTML` on static blocks
- Skipping Breeze purge note after author change
