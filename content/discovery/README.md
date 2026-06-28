# Agent discovery files (canonical)

Local source of truth for document-root files served at:

- https://rootsandfruit.com/robots.txt
- https://rootsandfruit.com/llms.txt
- https://rootsandfruit.com/llms-full.txt

## Sync to production (after abilities plugin 1.6.0+ deploy)

1. Edit files here in Cursor.
2. MCP `rootsandfruit/get-robots-llms-txt` — capture `sha256`.
3. MCP `rootsandfruit/update-robots-llms-txt` with full `content`, `expected_sha256`, `purge_breeze: true`.
4. Use **administrator** Application Password (`update_robots_llms_txt` cap).

See `agent/agent_docs/mcp-routing.md` recipe §6 and `abilities/readme.txt`.
