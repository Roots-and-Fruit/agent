# DEPRECATED — superseded by rootsandfruit-abilities plugin.
# Use MCP ability: rootsandfruit/preview/enable-public-preview
# Or run: .\tools\scripts\audit-mcp-abilities.ps1

Write-Error @"
enable-public-post-preview.ps1 is deprecated.

Enable public preview via the Roots & Fruit Abilities plugin:
  ability: rootsandfruit/preview/enable-public-preview
  parameters: { post_id: <id> }

Deploy: tools/wordpress/rootsandfruit-abilities/ -> wp-content/plugins/
"@

exit 1
