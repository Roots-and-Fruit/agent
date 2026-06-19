---
name: write-a-skill
description: Mandatory gate before creating or editing any Cursor skill in this repo. Invoke with /write-a-skill.
disable-model-invocation: true
---

# Write a skill

**Predictability gate:** do not create or edit any skill under `.cursor/skills/` until this procedure completes. Applies to ops runbooks and coding skills alike.

Vocabulary and failure-mode reference: [principles.md](principles.md). Scaffold: [template.md](template.md).

## 1. Intake

Collect from the user (or infer from thread):

| Field | Question |
|-------|----------|
| Purpose | What **predictability** does this skill guarantee? |
| Branches | Distinct paths (ops vs plugin dev vs block content)? |
| Invocation | User-invoked (default) or model-invoked? |
| Location | Sibling layout (parent open): `.cursor/skills/<name>/` at workspace root. Agent-only: `agent/.cursor/skills/<name>/`. See [Cursor skills docs](https://cursor.com/docs/context/skills) — nested `agent/.cursor/skills/` is scoped to `agent/` files only. |
| Authority | What already exists in `AGENTS.md` / `agent_docs/` that must stay the single source of truth? |

**Done when:** purpose, invocation mode, and authoritative doc pointers are stated in chat before drafting.

## 2. Design

1. **Name** — kebab-case, ≤64 chars, matches folder name; prefer an R&F **leading word** (`ability`, `legwork`, `escape hatch`) in the name or first heading when it fits.
2. **Invocation**
   - **User-invoked** (`disable-model-invocation: true`) — runbooks, deploy gates, meta authoring. Zero context load.
   - **Model-invoked** — only when the agent must auto-apply without `/skill-name`; pay context load; write a tight description (one trigger per branch).
3. **Scope** — model-invoked plugin skills: set `paths` to `abilities/**/*.php` (or narrower) so ops chat does not pull block-scaffold guidance.
4. **Single source of truth** — list repo docs this skill will **pointer-link**, not copy.

**Done when:** name, invocation choice, `paths` (if any), and pointer list are agreed.

## 3. Draft structure

Choose content type per [principles.md](principles.md):

- **Steps** for procedures (deploy, audit, author ability, install upstream skill pack).
- **Reference** for checklists and rules; disclose branch-specific detail to a sibling file.

Use [template.md](template.md). Rules:

- Each step ends with **Done when:** — checkable and, for verification steps, exhaustive (`script exit 0`, not "looks good").
- Ops skills: completion criteria cite concrete scripts (`test-wordpress-mcp-http.ps1`, `audit-mcp-abilities.ps1`, `php -l`).
- Coding skills: completion criteria cite touched files and lint/test commands.
- **Co-locate** related rules under one heading.
- Push optional depth to `references/` or one sibling `.md` — one hop from `SKILL.md` only.

**Done when:** draft exists on disk at `.cursor/skills/<name>/SKILL.md` (workspace root when parent folder is open).

## 4. Prune pass

Sentence-by-sentence:

1. **Relevance** — does it bear on this skill's branches?
2. **No-op** — would the agent behave the same without this line? Delete the whole sentence.
3. **Duplication** — already in `AGENTS.md`, upstream WordPress agent-skills, or @Docs? Replace with a pointer.
4. **Sprawl** — body >500 lines? Split by branch or disclose reference.

**Done when:** every remaining line changes behaviour or anchors a leading word.

## 5. Integrate

1. If the skill supersedes prose in `AGENTS.md`, **trim AGENTS.md** to a pointer — never maintain two copies.
2. Add one line to `AGENTS.md` § Deep docs table only if the skill is a long-lived entry point.
3. Do not commit unless the user asks.

**Done when:** no duplicated routing/security rules between skill and `AGENTS.md`.

## 6. Verify

- [ ] `name` matches folder name; frontmatter valid YAML
- [ ] Invocation mode intentional (`disable-model-invocation` set or deliberately omitted)
- [ ] Every step has a **Done when:** criterion
- [ ] Ops skills distinguish **ability** (MCP) vs **escape hatch** (REST) where relevant
- [ ] No secrets, no `.env` values, no Application Password placeholders beyond variable names
- [ ] File references ≤ one hop from `SKILL.md`

**Done when:** checklist complete and user has the skill path to test with `/skill-name`.

## Anti-patterns for R&F skills

- Restating MCP routing tables — link `agent_docs/mcp-routing.md`.
- Teaching generic block plugin scaffolding in an ops skill — install/link [WordPress/agent-skills](https://github.com/WordPress/agent-skills) instead.
- Model-invoked skills with vague descriptions ("helps with WordPress") — causes wrong auto-invocation during content ops.
- Completion criteria that allow **premature completion** ("verify the change") without naming the script or observable.
