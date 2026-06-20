# Roots & Fruit — article content workspace



Local artifacts for the rootsandfruit.com article pipeline. WordPress publish uses **`/rf-article-publish`** (MCP `rootsandfruit/blocks-*`).



## Layout



```

content/

├── articles/<keyword-slug>/     ← brief, draft, audit per article

│   ├── brief.html               ← canonical writer contract (required)

│   ├── draft.md                 ← article-writer output

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

| 5 | `/voiceprint-audit` | revised `draft.md` | **Review draft** |

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

Publish: `python tools/scripts/publish-article-preview.py content/articles/<slug>/`

Plan: [`agent/.cursor/plans/rf-article-pipeline.plan.md`](../.cursor/plans/rf-article-pipeline.plan.md).