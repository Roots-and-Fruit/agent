# Skill template

Copy into `.cursor/skills/<name>/SKILL.md` at the **workspace root** (sibling layout). When only `agent/` is opened, use `agent/.cursor/skills/<name>/` instead.

```markdown
---
name: <kebab-case-name>
description: <Third person. WHAT + WHEN branches. Only if model-invoked — omit rich triggers if user-invoked.>
disable-model-invocation: true
paths:
  - <optional/glob/**> 
---

# <Human title>

<One sentence: what predictability this skill guarantees.>

## When to use

- <Branch A trigger>
- <Branch B trigger>

## Procedure

### 1. <Step name>

<Actions.>

**Done when:** <Checkable completion criterion.>

### 2. <Step name>

<Actions.>

**Done when:** <Checkable completion criterion.>

## Pointers (do not duplicate)

- <Repo doc or upstream skill — single source of truth>

## Anti-patterns

- <Skill-specific mistakes>
```

## Frontmatter cheatsheet

| Field | Required | Notes |
|-------|----------|-------|
| `name` | yes | Lowercase, hyphens; matches folder name |
| `description` | yes | Human summary if user-invoked; trigger-rich if model-invoked |
| `disable-model-invocation` | default `true` | Set `true` unless agent must auto-invoke |
| `paths` | no | Glob list; scopes model-invoked skills to matching files |
