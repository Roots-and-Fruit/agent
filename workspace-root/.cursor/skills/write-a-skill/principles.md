# Skill authoring principles

Condensed reference for [`SKILL.md`](SKILL.md). Vocabulary adapted from [mattpocock/writing-great-skills](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md).

## Root virtue: predictability

A skill wrangles **predictability** out of a stochastic agent — same *process* every run, not the same output.

## Invocation axis

| Mode | Frontmatter | Who fires it | Cost |
|------|-------------|--------------|------|
| **User-invoked** | `disable-model-invocation: true` | Human types `/skill-name` only | Zero context load; human must remember it |
| **Model-invoked** | omit `disable-model-invocation` | Agent auto-selects from description | Description loaded every turn |

**Default for this repo:** user-invoked unless the agent must reach the skill without being told.

Model-invoked descriptions: front-load the **leading word**, one trigger per **branch**, no identity prose duplicated from the body.

## Information hierarchy

1. **Steps** — ordered actions in `SKILL.md`; each ends with a **completion criterion** (checkable, exhaustive where it matters).
2. **In-skill reference** — rules consulted during a step; co-locate related material under one heading.
3. **Disclosed reference** — sibling `.md` in the skill folder, reached by a **context pointer** only when a branch needs it.

**Progressive disclosure:** inline what every branch needs; push branch-specific material behind a pointer.

## Single source of truth

Each meaning lives in one authoritative place.

| Content | Authoritative home in R&F workspace |
|---------|-------------------------------------|
| MCP routing, credentials, site quirks | `AGENTS.md`, `agent_docs/mcp-routing.md` |
| Plugin architecture | `posts/managing-wordpress-via-cursor.md`, `abilities/` code |
| How to write skills | `write-a-skill` skill (this tree) |
| Generic WordPress API facts | @Docs or upstream agent-skills — **pointer**, not copy |

Skills **point** at repo docs; they do not restate them.

## Leading words (R&F)

Reuse these across skills, descriptions, and `AGENTS.md` so invocation stays aligned:

| Word | Meaning here |
|------|----------------|
| **ability** | Server-side MCP tool registered in WordPress (`rootsandfruit/*`) |
| **skill** | Client-side playbook in `.cursor/skills/` |
| **legwork** | Verification the agent runs (scripts, `php -l`, audit) — not "ask the user if it looks fine" |
| **escape hatch** | WP REST when no ability exists |
| **predictability** | Same procedure every run |

## Failure modes (diagnose before shipping)

| Mode | Symptom | Fix |
|------|---------|-----|
| **Premature completion** | Agent skips verification or half-applies steps | Sharpen completion criterion; split sequence if agent rushes |
| **Duplication** | Same rule in skill + `AGENTS.md` | Delete from skill; add pointer |
| **No-op** | Line restates default agent behaviour | Delete the sentence |
| **Sprawl** | SKILL.md > ~500 lines | Disclose reference; split by branch or invocation |
| **Sediment** | Stale steps after workflow changed | Prune or update completion criteria |

## Ops vs coding skills

Both use the same craft. The difference is **completion criteria** and **pointers**:

- **Ops skills** — end on script output or explicit manual E2E; point at MCP ability names; warn on credential profile (content vs admin).
- **Coding skills** — end on `php -l`, tests, or lint; use `paths` to scope to `abilities/**/*.php` when plugin-specific.

Generic "scaffold a block plugin" guidance belongs in upstream WordPress agent-skills, not R&F ops skills — link or install, don't duplicate.
