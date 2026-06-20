---
url: https://github.com/wordpress/mcp-adapter
title: "WordPress/mcp-adapter: An MCP ..."
status_code: 200
parse_mode: ok
---

# WordPress/mcp-adapter
## Folders and files
| Name | Name | Last commit message | Last commit date |
|---|
| Latest commit History 105 Commits 105 Commits |
## Releases 5

Releases 5
## Packages 0

Packages 0
## Contributors

[Contributors](https://github.com/WordPress/mcp-adapter/graphs/contributors)
## Repository files navigation

Code of conduct

GPL-2.0 license
# MCP Adapter

Part of the [AI Building Blocks for WordPress initiative](https://make.wordpress.org/ai/2025/07/17/ai-building-blocks)

The official WordPress package for MCP integration that exposes WordPress abilities as [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) tools, resources, and prompts for AI agents.
## Overview

This adapter bridges WordPress's Abilities API with the [MCP specification](https://modelcontextprotocol.io/specification/2025-11-25/), providing a standardized way for AI agents to interact with WordPress functionality. It includes HTTP and STDIO transport support, comprehensive error handling, and an extensible architecture for custom integrations.
### Core Functionality

Ability-to-MCP Conversion : Automatically converts WordPress abilities into MCP tools, resources, and prompts

Multi-Server Management : Create and manage multiple MCP servers with unique configurations

HTTP Transport : Unified transport implementing [MCP 2025-11-25 specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) for HTTP-based communication

STDIO Transport : Process-based communication via standard input/output for local development and CLI integration

Custom Transport Support : Implement McpTransportInterface to create specialized communication protocols

Multi-Transport Configuration : Configure servers with multiple transport methods simultaneously

Built-in Error Handler : Default WordPress-compatible error logging included

Custom Error Handlers : Implement McpErrorHandlerInterface for custom logging, monitoring, or notification
systems

Server-specific Handlers : Different error handling strategies per MCP server

Built-in Observability : Default zero-overhead metrics tracking with configurable handlers

Custom Observability Handlers : Implement McpObservabilityHandlerInterface for integration with monitoring
systems

Validation : Built-in validation for tools, resources, and prompts with extensible validation rules

Permission Control : Granular permission checking for all exposed functionality with configurable [transport permissions](https://github.com/WordPress/mcp-adapter/blob/trunk/docs/guides/transport-permissions.md)
### MCP Component Support

[Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools.md) : Convert WordPress abilities into executable MCP tools for AI agent interactions

[Resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources.md) : Expose WordPress data as MCP resources for contextual information access

[Prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts.md) : Transform abilities into structured MCP prompts for AI guidance and templates

Server Discovery : Automatic registration and discovery of MCP servers following MCP protocol standards

Built-in Abilities : Core WordPress abilities for system introspection and ability management

CLI Integration : WP-CLI commands supporting STDIO transport as defined in MCP specification
## Architecture

For a full breakdown of the component structure, see the [Architecture Overview](https://github.com/WordPress/mcp-adapter/blob/trunk/docs/architecture/overview.md).
## Dependencies

PHP : >= 7.4

WordPress : >= 6.9

[php-mcp-schema](https://github.com/WordPress/php-mcp-schema) ( ^0.1.0 ): Typed DTOs for MCP protocol types — installed automatically via Composer
### As a WordPress Plugin (Recommended)

MCP Adapter is designed to be installed as a WordPress plugin. To install you should download the latest stable release from the [GitHub Releases page](https://github.com/WordPress/mcp-adapter/releases/latest) and install it like any other WordPress plugin.
### As a Composer Library (for plugin developers)

Plugin developers may wish to install MCP Adapter as a Composer dependency to integrate MCP functionality into their own plugins.
#### Using Jetpack Autoloader (Highly Recommended)

When multiple plugins use the MCP Adapter, it's highly recommended to use the [Jetpack Autoloader](https://github.com/Automattic/jetpack-autoloader) to prevent version conflicts. The Jetpack Autoloader ensures that only the latest version of shared packages is loaded, eliminating conflicts when different plugins use different versions of the same dependency.

Then load it in your main plugin file instead of the standard Composer autoloader:
### Using MCP Adapter in Your Plugin

Check availability and initialize on plugins_loaded so all plugins are available before the adapter starts:
## Basic Usage

The MCP Adapter automatically creates a default server that exposes registered WordPress abilities through a layered architecture. This provides immediate MCP functionality without requiring manual server configuration.

How it works:

WordPress abilities registered via wp_register_ability() with the meta.mcp.public flag set to true are discoverable and executable on the default server via its built-in adapter tools

On the default server, public abilities are accessed through mcp-adapter/discover-abilities, mcp-adapter/get-ability-info, and mcp-adapter/execute-ability rather than being auto-registered individually in tools/list

Alternatively, abilities can be explicitly listed when creating a custom MCP server ; in that case, they can be exposed directly as MCP tools, resources, or prompts without requiring the meta.mcp.public flag

The default server supports both HTTP and STDIO transports and supports multiple MCP protocol versions

Built-in error handling and observability are included

Access via HTTP: /wp-json/mcp/mcp-adapter-default-server

Access via STDIO: wp mcp-adapter serve --server=mcp-adapter-default-server

For detailed information about creating WordPress abilities, see the [Abilities API developer documentation](https://developer.wordpress.org/news/2025/11/introducing-the-wordpress-abilities-api/).
### Connecting to MCP Servers

The MCP Adapter supports multiple connection methods. Here are examples for connecting with MCP clients:
#### STDIO Transport (Local Development)

For local development and testing, you can interact directly with MCP servers using WP-CLI commands:
#### MCP Client Configuration

Configure MCP clients (Claude Desktop, Claude Code, VS Code, Cursor, etc.) to connect to your WordPress MCP servers.

The [@automattic/mcp-wordpress-remote](https://www.npmjs.com/package/@automattic/mcp-wordpress-remote) proxy runs locally and translates STDIO-based MCP communication from AI clients into HTTP REST API calls that WordPress understands. Authentication uses [WordPress Application Passwords](https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/).
### Creating Custom MCP Servers

For advanced use cases, you can create custom MCP servers with specific configurations:
### Custom Transport Implementation

The MCP Adapter includes production-ready HTTP transports. For specialized requirements like custom authentication, message queues, or enterprise integrations, you can create custom transport protocols.

See the [Custom Transports Guide](https://github.com/WordPress/mcp-adapter/blob/trunk/docs/guides/custom-transports.md) for detailed implementation instructions.
### Custom Transport Permissions

The MCP Adapter supports custom authentication logic through transport permission callbacks. Instead of the default is_user_logged_in() check, you can implement custom authentication for your MCP servers.

See the [Transport Permissions Guide](https://github.com/WordPress/mcp-adapter/blob/trunk/docs/guides/transport-permissions.md) for detailed authentication patterns.
### Custom Error Handler

The MCP Adapter includes a default WordPress-compatible error handler, but you can implement custom error handling to integrate with existing logging systems, monitoring tools, or meet specific requirements.

See the [Error Handling Guide](https://github.com/WordPress/mcp-adapter/blob/trunk/docs/guides/error-handling.md) for detailed implementation instructions.
### Custom Observability Handler

The MCP Adapter includes built-in observability for tracking metrics and events. You can implement custom observability handlers to integrate with monitoring systems, analytics platforms, or performance tracking tools.

See the [Observability Guide](https://github.com/WordPress/mcp-adapter/blob/trunk/docs/guides/observability.md) for detailed metrics tracking and custom handler implementation.
## Migration

[Migration Guide: v0.5.0](https://github.com/WordPress/mcp-adapter/blob/trunk/docs/migration/v0.5.0.md) — Breaking changes and upgrade instructions

[Migration Guide: v0.3.0](https://github.com/WordPress/mcp-adapter/blob/trunk/docs/migration/v0.3.0.md) — Transport, observability, and hook name changes
## About

An MCP adapter that bridges the Abilities API to the Model Context Protocol, enabling MCP clients to discover and invoke WordPress plugin, theme, and core abilities programmatically.
### Uh oh!

There was an error while loading. Please reload this page.
### Uh oh!

There was an error while loading. Please reload this page.
### Uh oh!

There was an error while loading. Please reload this page.
### Uh oh!

There was an error while loading. Please reload this page.
## Languages

PHP 100.0%
