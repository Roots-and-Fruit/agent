# Roots & Fruit — article content workspace



Local artifacts for the rootsandfruit.com article pipeline. WordPress publish uses **`/rf-article-publish`** (MCP `rootsandfruit/blocks-*`).



## Layout



```

content/

├── articles/<keyword-slug>/     ← brief, draft, audit per article

│   ├── brief.html               ← canonical writer contract (required)

│   ├── draft.md                 ← article-writer output

│   ├── excerpt.txt              ← hero excerpt / SEO meta (140–155 chars; required for publish)

│   ├── key-takeaways.txt        ← sidebar takeaways (1–12 lines; required for publish)

│   ├── ig-audit.html            ← publish/revise audit (HTML)

│   └── ig-audit.json            ← machine-readable scores

└── keyword-intel/output/<keyword-slug>/   ← rf-keyword-research artifacts

    ├── manifest.json

    ├── scored/top_n.json

    ├── reports/                 ← baseline/delta reports

    └── serp/                    ← DataForSEO SERP baseline corpus (required for IG audit)

        ├── corpus.md

        ├── serp_raw.json

        ├── corpus_manifest.json

        └── pages/

```



## Pipeline (orchestrator: `/rf-article-pipeline`)



| Order | Skill | Output | STOP |

|-------|-------|--------|------|

| 0 (once) | `/voiceprint` | `.cursor/skills/voiceprint/artifacts/` | — |

| 1 | `/rf-keyword-research` | `keyword-intel/output/<slug>/` | — |

| 2 | `/grill-info-gain` | Info Gain Handoff block | — |

| 3 | `/content-brief` | `articles/<slug>/brief.html` | **Review brief** |

| 4 | `/article-writer` | `articles/<slug>/draft.md` | — |

| 5 | `/voiceprint-audit` | revised `draft.md` + `excerpt.txt` + `key-takeaways.txt` | **Review draft + excerpt + takeaways** |

| 6 | `/information-gain-auditor` | `ig-audit.html` + `ig-audit.json` | — |

| 7 | `/rf-article-publish` | WP draft + public preview URL | **Review preview**; **convert code → Code Pro** in editor |

| 8 | `/rf-article-publish` (approve) | live post | explicit OK only |



**MCP servers:** `wordpress-rootsandfruit` + `dataforseo` (full keyword research).



Canonical style examples: `content/articles/example-explainer/brief.html` and `ig-audit.html`.

## Block defaults (publish)

[`block-defaults.json`](block-defaults.json) — converter targets:

- Fenced code → **`core/code`** (labeled fences get `language-*`; unlabeled/plain omit language class)
- Markdown tables → **Striped** (`is-style-stripes`)

**Code Block Pro:** MCP inserts `core/code` only. In wp-admin, focus each code block → **Convert to Code Pro** → Save (uses your site Shiki defaults). See `/rf-article-publish` step 7b.

Publish: `python tools/scripts/publish-article-preview.py content/articles/<slug>/` (reads `excerpt.txt` and `key-takeaways.txt` automatically)

## Hero excerpt (`excerpt.txt`)

WordPress `post_excerpt` drives the Kadence hero quote and SEO meta. Without it, the theme falls back to body paragraph 1.

| Stage | Excerpt job |
|-------|-------------|
| `/rf-keyword-research` | Draft line in `articles/<slug>/keyword-research.md` (`## SEO meta description`) |
| `/content-brief` | Commit in `brief.html` Keywords / Hero Excerpt (140–155 chars; STOP gate) |
| `/voiceprint-audit` | Finalize `excerpt.txt` — must **not** duplicate draft ¶1 |
| `/rf-article-publish` | Auto-read `excerpt.txt` → `blocks-create-page` |

Rules: single line, 140–155 characters, enticing hook (not the article lede). Validator: `tools/scripts/article-excerpt.py`.

## Key takeaways (`key-takeaways.txt`)

WordPress post meta `_rf_key_takeaways` (LCF ordered-list repeater) drives the Kadence sidebar **Key Takeaways** widget and ItemList JSON-LD (`rootsandfruit/key-takeaways-json-ld`).

| Stage | Takeaways job |
|-------|---------------|
| `/content-brief` | Optional bullets in brief for writer alignment |
| `/voiceprint-audit` | Finalize `key-takeaways.txt` — one bullet per line |
| `/rf-article-publish` | Auto-read → `rootsandfruit/set-key-takeaways` after `blocks-create-page` |

Rules: 1–12 lines (typically 3), scannable sidebar bullets (not body copy). Validator: `tools/scripts/article-key-takeaways.py`.

Plan: [`agent/.cursor/plans/rf-article-pipeline.plan.md`](../.cursor/plans/rf-article-pipeline.plan.md).