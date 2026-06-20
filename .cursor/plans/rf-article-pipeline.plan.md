---
name: R&F Article Pipeline
overview: "Close the article workflow gaps: orchestrated multi-skill pipeline, DataforSEO-backed keyword research, required voiceprint in brief, post-writer voiceprint audit, IG auditor before publish, explicit draft-to-blocks publish skill, and set-post-author ability."
todos:
  - id: save-plan-artifact
    content: Write agent/.cursor/plans/rf-article-pipeline.plan.md (Cursor YAML frontmatter + todos)
    status: completed
  - id: orchestrator-skill
    content: Create rf-article-pipeline/SKILL.md with stages, STOP gates, --from resume, MCP deps
    status: completed
  - id: voiceprint-audit-skill
    content: Create voiceprint-audit/SKILL.md — post-writer revise draft.md before user review
    status: completed
  - id: rf-article-publish-skill
    content: Create rf-article-publish/SKILL.md + REFERENCE.md — draft→blocks, preview STOP, publish gate
    status: completed
  - id: update-content-skills
    content: Update content-brief (voiceprint required), article-writer, information-gain-auditor, rf-keyword-research
    status: completed
  - id: dataforseo-wire
    content: Add dataforseo.md reference; wire MCP in rf-keyword-research; move credentials to .env in mcp.json
    status: completed
  - id: set-post-author-ability
    content: Add rootsandfruit/set-post-author in abilities plugin; update mcp-routing.md; release + legwork
    status: completed
  - id: docs-sync
    content: Update content/README.md, AGENTS.md, cursor-context-stack.md, rf-wordpress-ops pointers
    status: completed
isProject: false
---

# R&F Article Pipeline — Gap Closure Plan

**Canonical artifact:** this file. **Orchestrator:** `/rf-article-pipeline`.

See [`content/README.md`](../../content/README.md) for live pipeline order and STOP gates.

**Deploy note:** `rootsandfruit/set-post-author` requires abilities plugin release before production publish step.
