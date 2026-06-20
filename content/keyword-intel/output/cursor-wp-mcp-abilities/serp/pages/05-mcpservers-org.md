---
url: https://mcpservers.org/servers/kungtekno/wp-mcp
title: "WordPress MCP Server"
status_code: 200
parse_mode: ok
---

# WordPress MCP Server
### Capafy

[Capafy](https://capafy.ai/?utm_source=mcpservers&utm_medium=referral)

[On Capafy, your Skill runs online 24/7 as an agent product, and you get paid every time someone uses it.](https://capafy.ai/?utm_source=mcpservers&utm_medium=referral)

[View on capafy.ai](https://capafy.ai/?utm_source=mcpservers&utm_medium=referral)
### 2slides

[2slides](https://mcpservers.org/servers/github-com-2slides-2slides-mcp)

[This is the 1st, easiest, and cheapest PPT, slides, presentation AI generation MCP Server in the world.](https://mcpservers.org/servers/github-com-2slides-2slides-mcp)
### Achriom

[Achriom](https://mcpservers.org/servers/achriom/achriom-mcp)

[The media memory layer for AI agents and their humans. Track books, movies, music, shows, and anime.](https://mcpservers.org/servers/achriom/achriom-mcp)
### Adfin

[Adfin](https://mcpservers.org/servers/Adfin-Engineering/mcp-server-adfin)

[The only platform you need to get paid - all payments in one place, invoicing and accounting reconciliations with Adfin.](https://mcpservers.org/servers/Adfin-Engineering/mcp-server-adfin)
### Agent Billy

[Agent Billy](https://mcpservers.org/servers/agent-billy/agentbilly)

[MCP server that gives AI agents and teams secure, role-based access to Stripe billing operations — customer lookups, subscription management, refunds, invoice history — without exposing Stripe dashboard credentials. Sub-100ms reads via local Stripe sync engine. 4 permission levels with audit logging. $14.99/month.](https://mcpservers.org/servers/agent-billy/agentbilly)
### ai-memory

[ai-memory](https://mcpservers.org/servers/alphaonedev/ai-memory-mcp)

[Persistent memory for any AI assistant. Zero token cost until recall. Stores memories in local SQLite, ranks by 6-factor scoring, returns results 79% smaller than JSON. Works with Claude, ChatGPT, Grok, Cursor, Windsurf, and any MCP client.](https://mcpservers.org/servers/alphaonedev/ai-memory-mcp)
### Aithon — AI Agent Marketplace

[Aithon — AI Agent Marketplace](https://mcpservers.org/servers/aithon-tech)

[AI agent commerce marketplace — register, list services, buy and sell capabilities with real payments via Stripe.](https://mcpservers.org/servers/aithon-tech)
### Anki MCP

[Anki MCP](https://mcpservers.org/servers/anki-mcp/anki-mcp-desktop)

[A MCP server that enables AI assistants to interact with Anki, the spaced repetition flashcard application.](https://mcpservers.org/servers/anki-mcp/anki-mcp-desktop)
### AppContext MCP

[AppContext MCP](https://mcpservers.org/servers/appcontext-dev)

[AppContext gives your AI coding agent instant visual insight into what you're developing, so it can fix issues, refine UI, and accelerate your development workflow in real time.](https://mcpservers.org/servers/appcontext-dev)
### AppleScript BB MCP Server

[AppleScript BB MCP Server](https://mcpservers.org/servers/beyondbetter-app-solutions-mcp-tools)

[Enables LLM clients to interact with macOS applications through AppleScript. Built using the @beyondbetter/bb-mcp-server library, this server provides safe, controlled execution of predefined scripts with optional support for arbitrary script execution.](https://mcpservers.org/servers/beyondbetter-app-solutions-mcp-tools)
### Atlassian Remote MCP

[Atlassian Remote MCP](https://mcpservers.org/servers/atlassian-mcp-server)

[Official Atlassian remote MCP server for connecting AI agents to Jira, Confluence, Opsgenie, and other Atlassian products.](https://mcpservers.org/servers/atlassian-mcp-server)

A secure bridge between AI assistants and WordPress, enabling site management and content operations through natural language.

A Model Context Protocol (MCP) server that enables AI assistants like Claude to interact with WordPress sites through a standardized interface.
## Description

WordPress MCP Server provides a secure bridge between AI assistants and WordPress installations, allowing for content management, site administration, and plugin/theme operations through natural language interactions. Built on the Model Context Protocol standard, it offers a comprehensive set of tools for WordPress automation.
## Features

Content Management : Create, read, update, and delete posts, pages, and custom post types

Media Handling : Upload and manage media files with automatic optimization

User Management : Handle user operations and permissions

Plugin & Theme Control : Install, activate, deactivate, and manage plugins/themes

Site Configuration : Manage WordPress settings and configurations

Custom Post Types : Full support for custom post types and taxonomies

SEO Integration : Built-in support for popular SEO plugins

Security : OAuth2 authentication and secure API communications

Batch Operations : Efficient bulk actions for content and media

Real-time Updates : Live site status and health monitoring
## Prerequisites

Node.js 16.0 or higher

npm or yarn package manager

WordPress 5.0 or higher with REST API enabled

Valid WordPress admin credentials or application passwords

Claude Code or any MCP-compatible client
### Initial Setup

Create a configuration file:

Or manually create wordpress-config.json :
#### Application Passwords (Recommended)

Go to WordPress Admin → Users → Your Profile

Scroll to "Application Passwords"

Enter a name and click "Add New Application Password"

Copy the generated password to your config
#### Basic Authentication

Requires HTTP Basic Auth plugin

Less secure, use only for development
#### OAuth2

Most secure option

Requires OAuth2 plugin setup

See [OAuth2 Setup Guide](https://github.com/kungtekno/wp-mcp/blob/main/docs/oauth2-setup.md)
### With Claude Code

Add to Claude Code configuration:

Use natural language commands:
### Content Tools

wp_create_post - Create posts, pages, or custom post types

wp_update_post - Update existing content

wp_get_post - Retrieve post details

wp_delete_post - Delete content

wp_list_posts - List and filter content
### Media Tools

wp_upload_media - Upload images, videos, documents

wp_get_media - Retrieve media information

wp_delete_media - Remove media files

wp_optimize_images - Bulk image optimization
### Site Management

wp_get_site_info - Site details and health

wp_update_settings - Modify site settings

wp_clear_cache - Clear various caches

wp_backup_site - Create site backups
### Plugin & Theme Tools

wp_install_plugin - Install from repository

wp_activate_plugin - Activate installed plugins

wp_update_plugin - Update to latest version

wp_list_themes - Available themes
### User Management

wp_create_user - Add new users

wp_update_user - Modify user details

wp_list_users - Get user listings

wp_manage_roles - Role and capability management
#### Connection Failed

Verify WordPress URL is correct

Check REST API is enabled: https://yoursite.com/wp-json/

Ensure credentials are valid
#### Authentication Errors

Application passwords require WordPress 5.6+

Username should be your login name, not email

Some hosts block REST API authentication
#### Permission Denied

User needs appropriate WordPress capabilities

Check plugin/theme installation permissions

Verify file upload limits
### Debug Mode

Enable verbose logging:
### Getting Help

Check [Claude Code Setup Guide](https://github.com/kungtekno/wp-mcp/blob/main/CLAUDE_CODE_SETUP.md)

Visit [Issues](https://github.com/yourusername/wordpress-mcp-server/issues)

Join our [Discord Community](https://discord.gg/wordpress-mcp)
## Contributing

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/kungtekno/wp-mcp/blob/main/CONTRIBUTING.md) for details.
## Security

For security concerns, please review our [Security Policy](https://github.com/kungtekno/wp-mcp/blob/main/SECURITY.md) and report issues responsibly.
## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/kungtekno/wp-mcp/blob/main/LICENSE) file for details.
## Acknowledgments

Built on the [Model Context Protocol](https://modelcontextprotocol.io/) standard

WordPress REST API documentation and community

Claude and Anthropic for MCP development
