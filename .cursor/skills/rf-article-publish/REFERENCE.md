# Draft → Gutenberg blocks — Reference

Used by `/rf-article-publish`. Do not paste raw HTML via `update-post`.

## Mapping rules

Parse `draft.md` top to bottom:

| Markdown | Block | Required fields |
|----------|-------|-----------------|
| `# Title` | (post title only — not a block) | Set on `blocks-create-page` |
| `## Heading` | `core/heading` | `attributes: { content, level: 2 }`, `innerHTML: "<h2 class=\"wp-block-heading\">…</h2>"` |
| `### Subheading` | `core/heading` | `level: 3`, matching `innerHTML` |
| Paragraph text | `core/paragraph` | `attributes: { content }`, `innerHTML: "<p>…</p>"` |
| `- item` list | `core/list` | `ordered: false`, `values` in attributes; include serialized innerHTML |
| `1. item` list | `core/list` | `ordered: true` |
| Fenced code | **`core/code`** | `content` + `innerHTML`; add `language` + `language-*` class only for real langs (powershell, bash, …) |
| Markdown table | `core/table` | **`className: is-style-stripes`**; plain text in `head`/`body` attrs and cells |

Site defaults: [`content/block-defaults.json`](../../../content/block-defaults.json). Converter: `tools/scripts/draft-md-to-blocks.py`.

**Do not** emit `kevinbatdorf/code-block-pro` from the agent pipeline.

### Code Block Pro (editor convert)

After MCP creates the draft:

1. Open **`edit_url`** (`preview.json` or `wp-admin/post.php?post={id}&action=edit`).
2. Focus each **`core/code`** block → toolbar → **Convert to Code Pro**.
3. **Save** — CBP applies your site Shiki theme and defaults.
4. Re-check preview logged out before publish approval.

**Rule:** every static core block must include **`innerHTML`** matching attributes or GK validation fails.

## Preview pipeline (Python only)

```powershell
python tools/scripts/publish-article-preview.py content/articles/<slug>/
```

Steps: `draft-md-to-blocks.py` → `blocks-create-page` → `set-post-author` (default **1**) → `enable-public-preview` → `preview.json`.

**Encoding:** use `invoke-mcp-ability.py` for manual MCP calls (UTF-8 safe). Converter emits HTML entities in `innerHTML`.

## Ability sequence (preview)

1. `rootsandfruit/blocks-create-page` — create draft with blocks
2. `rootsandfruit/blocks-get-page` — verify
3. `rootsandfruit/set-post-author` — `{ post_id, author }`
4. `rootsandfruit/enable-public-preview` — `{ post_id }`
5. **STOP** — share `preview_url` and `edit_url`; user converts code blocks in editor (see below)
6. `rootsandfruit/publish-post` — only on explicit user approval (after convert + preview OK)

## Author parameter

**Default (rootsandfruit.com articles):** user ID **`1`**.

After author change: purge Breeze cache before trusting logged-out preview byline.

## Manual debug

```powershell
python tools/scripts/draft-md-to-blocks.py content/articles/<slug>/draft.md -o content/articles/<slug>/blocks-payload.json --slug <slug>
python tools/scripts/invoke-mcp-ability.py rootsandfruit/blocks-create-page content/articles/<slug>/blocks-payload.json
```

## Existing post edits

1. `blocks-get-page`
2. `blocks-mutate` or `blocks-insert` for section changes
3. Re-run preview enable if token expired

**blocks-update:** send `innerHTML` only for `core/list` and `core/table`.
