---
url: https://github.com/Automattic/wordpress-mcp
title: "GitHub - Automattic/wordpress-mcp: ..."
status_code: 200
parse_mode: ok
---

# Automattic/wordpress-mcp
## Folders and files
| Name | Name | Last commit message | Last commit date |
|---|
| Latest commit History 228 Commits 228 Commits |
### Transport Protocols
| Protocol | Endpoint | Format | Authentication | Use Case |
|---|
| STDIO | /wp/v2/wpmcp | WordPress-style | JWT + App Passwords | Legacy compatibility |
| Streamable | /wp/v2/wpmcp/streamable | JSON-RPC 2.0 | JWT only | Modern AI clients |
#### Claude Desktop Configuration using mcp-wordpress-remote proxy

Claude Desktop Configuration using [mcp-wordpress-remote](https://github.com/Automattic/mcp-wordpress-remote) proxy

Add to your Claude Desktop claude_desktop_config.json :
### Available MCP Methods
| Method | Description | Transport Support |
|---|
| initialize | Initialize MCP session | Both |
| tools/list | List available tools | Both |
| tools/call | Execute a tool | Both |
| resources/list | List available resources | Both |
| resources/read | Read resource content | Both |
| prompts/list | List available prompts | Both |
| prompts/get | Get prompt template | Both |
#### Available Tools
| Tool Name | Description | Type |
|---|
| list_api_functions | Discover all available WordPress REST API endpoints | Read |
| get_function_details | Get detailed metadata for specific endpoint/method | Read |
| run_api_function | Execute any REST API function with CRUD operations | Action |
## Releases 18

Releases 18
## Packages 0

Packages 0
## Contributors

[Contributors](https://github.com/Automattic/wordpress-mcp/graphs/contributors)
## Repository files navigation

This repository will be deprecated as the [mcp-adapter](https://github.com/wordpress/mcp-adapter) AI Building Block for WordPress continues releasing stable versions.

The shift aligns with two important developments:

The [Abilities API](https://github.com/WordPress/abilities-api) is moving into WordPress Core as of version 6.9.

mcp-adapter is now stable and will become the canonical plugin and Composer package for MCP integration in WordPress.

We encourage all users to migrate to mcp-adapter. Future work, including new features and fixes, will happen there. This repository will remain available in archived form for historical reference.
# WordPress MCP

A comprehensive WordPress plugin that implements the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) to expose WordPress functionality through standardized interfaces. This plugin enables AI models and applications to interact with WordPress sites securely using multiple transport protocols and enterprise-grade authentication.
## Features

Dual Transport Protocols : STDIO and HTTP-based (Streamable) transports

JWT Authentication : Secure token-based authentication with management UI

Admin Interface : React-based token management and settings dashboard

AI-Friendly APIs : JSON-RPC 2.0 compliant endpoints for AI integration

Extensible Architecture : Custom tools, resources, and prompts support

WordPress Feature API : Adapter for standardized WordPress functionality

Experimental REST API CRUD Tools : Generic tools for any WordPress REST API endpoint

Comprehensive Testing : 200+ test cases covering all protocols and authentication

High Performance : Optimized routing and caching mechanisms

Enterprise Security : Multi-layer authentication and audit logging
## Architecture

The plugin implements a dual transport architecture:
### Quick Install

Download wordpress-mcp.zip from [releases](https://github.com/Automattic/wordpress-mcp/releases/)

Upload to /wp-content/plugins/wordpress-mcp directory

Activate through WordPress admin 'Plugins' menu

Navigate to Settings > WordPress MCP to configure
### JWT Token Generation

Go to Settings > WordPress MCP > Authentication Tokens

Select token duration (1-24 hours)

Click "Generate New Token"

Copy the token for use in your MCP client
#### VS Code MCP Extension (Direct Streamable Transport)

Add to your VS Code MCP settings:
### With MCP Clients

This plugin works seamlessly with MCP-compatible clients in two ways:

Via Proxy:

[mcp-wordpress-remote](https://github.com/Automattic/mcp-wordpress-remote) - Official MCP client with enhanced features

Claude Desktop with proxy configuration for full WordPress and WooCommerce support

Any MCP client using the STDIO transport protocol

Direct Streamable Transport:

VS Code MCP Extension connecting directly to /wp/v2/wpmcp/streamable

Custom HTTP-based MCP implementations using JSON-RPC 2.0

Any client supporting HTTP transport with JWT authentication

The streamable transport provides a direct JSON-RPC 2.0 compliant endpoint, while the proxy offers additional features like WooCommerce integration, enhanced logging, and compatibility with legacy authentication methods.
### Experimental REST API CRUD Tools

EXPERIMENTAL FEATURE : This functionality is experimental and may change or be removed in future versions.

When enabled via Settings > WordPress MCP > Enable REST API CRUD Tools, the plugin provides three powerful generic tools that can interact with any WordPress REST API endpoint:
#### Usage Workflow

Discovery : Use list_api_functions to see all available endpoints

Inspection : Use get_function_details to understand required parameters

Execution : Use run_api_function to perform CRUD operations
#### Security & Permissions

User Capabilities : All operations respect current user permissions

: Individual CRUD operations can be disabled in settings:

Enable Create Tools (POST operations)

Enable Update Tools (PATCH/PUT operations)

Enable Delete Tools (DELETE operations)

Automatic Filtering : Excludes sensitive endpoints (JWT auth, oembed, autosaves, revisions)
#### Benefits

Universal Access : Works with any WordPress REST API endpoint, including custom post types and third-party plugins

AI-Friendly : Provides discovery and introspection capabilities for AI agents

Standards Compliant : Uses standard HTTP methods (GET, POST, PATCH, DELETE)

Permission Safe : Inherits WordPress user capabilities and respects endpoint permissions
### Adding Custom Tools

You can extend the MCP functionality by adding custom tools through your own plugins or themes. Create a new tool class in your plugin or theme:
### Adding Custom Resources

You can extend the MCP functionality by adding custom resources through your own plugins or themes. Create a new resource class in your plugin or theme:
### Testing

Run the comprehensive test suite:
### Best Practices

Token Management : Use shortest expiration time needed (1-24 hours)

User Permissions : Tokens inherit user capabilities

Secure Storage : Never commit tokens to repositories

Regular Cleanup : Revoke unused tokens promptly

Access Control : Streamable transport requires admin privileges

CRUD Operations : Only enable create/update/delete tools when necessary

Experimental Features : Use REST API CRUD tools with caution in production environments
### Security Features

JWT signature validation

Token expiration and revocation

User capability inheritance

Secure secret key generation

Audit logging for security events

Protection against malformed requests
## Testing Coverage

The plugin includes extensive testing:

Transport Testing : Both STDIO and Streamable protocols

Authentication Testing : JWT generation, validation, and revocation

Integration Testing : Cross-transport comparison

Security Testing : Edge cases and malformed requests

Performance Testing : Load and stress testing

View detailed testing documentation in [tests/README.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/tests/README.md).
### Plugin Settings

Access via Settings > WordPress MCP :

Enable/Disable MCP : Toggle plugin functionality

Transport Configuration : Configure STDIO/Streamable transports

Feature Toggles : Enable/disable specific tools and resources

CRUD Operation Controls : Granular control over create, update, and delete operations

Experimental Features : Enable REST API CRUD Tools (experimental functionality)

Authentication Settings : JWT token management
#### CRUD Operation Settings

The plugin provides granular control over CRUD operations:

Enable Create Tools : Allow POST operations via MCP tools

Enable Update Tools : Allow PATCH/PUT operations via MCP tools

Enable Delete Tools : ⚠️ Allow DELETE operations via MCP tools (use with caution)

Enable REST API CRUD Tools : 🧪 Enable experimental generic REST API access tools

Security Note : Delete operations can permanently remove data. Only enable delete tools if you trust all users with MCP access.
## Contributing

We welcome contributions! Please see our [Contributing Guidelines](https://github.com/Automattic/wordpress-mcp/blob/trunk/CONTRIBUTING.md).
### Development Setup

Clone the repository

Run composer install for PHP dependencies

Run npm install for JavaScript dependencies

Set up WordPress test environment

Run tests with vendor/bin/phpunit
## Documentation

Documentation Overview : [docs/README.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/docs/README.md)

Client Setup Guide : [docs/client-setup.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/docs/client-setup.md)

AI Integration Guide : [docs/for-ai.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/docs/for-ai.md)

Registered Tools : [docs/registered-tools.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/docs/registered-tools.md)

Registered Resources : [docs/registered-resources.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/docs/registered-resources.md)

Registered Prompts : [docs/registered-prompts.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/docs/registered-prompts.md)

Register MCP Tools : [docs/register-mcp-tools.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/docs/register-mcp-tools.md)

Register MCP Prompts : [docs/register-mcp-prompt.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/docs/register-mcp-prompt.md)

Register MCP Resources : [docs/register-mcp-resources.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/docs/register-mcp-resources.md)

Troubleshooting Guide : [docs/troubleshooting.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/docs/troubleshooting.md)

Testing Guide : [tests/README.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/tests/README.md)
## Support

For support and questions:

Documentation : [docs/README.md](https://github.com/Automattic/wordpress-mcp/blob/trunk/docs/README.md)

Bug Reports : [GitHub Issues](https://github.com/Automattic/wordpress-mcp/issues)

Discussions : [GitHub Discussions](https://github.com/Automattic/wordpress-mcp/discussions)

Contact : Reach out to the maintainers
## License

This project is licensed under the [GPL v2 or later](https://github.com/Automattic/wordpress-mcp/blob/trunk/LICENSE).
## WordPress MCP

Built with ❤️ by [Automattic](https://automattic.com/) for the WordPress and AI communities.
## About

WordPress MCP — This repository will be deprecated as stable releases of mcp-adapter become available. Please use [https://github.com/WordPress/mcp-adapter](https://github.com/WordPress/mcp-adapter) for ongoing development and support.
### Uh oh!

There was an error while loading. Please reload this page.
### Uh oh!

There was an error while loading. Please reload this page.
### Uh oh!

There was an error while loading. Please reload this page.
### Uh oh!

There was an error while loading. Please reload this page.
## Languages

PHP 88.5%

JavaScript 9.1%

CSS 1.2%

Shell 1.2%
