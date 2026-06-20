# SERP Baseline Corpus — wordpress mcp server
Generated: 2026-06-19

## Google AI Overview

A **WordPress MCP (Model Context Protocol) Server** `bridges AI assistants (like Claude, Cursor, and VS Code) with your WordPress website so you can manage content, posts, pages, and themes directly via natural language`.[](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/) [[1]](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)[[2]](https://mcpservers.org/servers/kungtekno/wp-mcp)By using the official [WordPress MCP Adapter](https://github.com/wordpress/mcp-adapter) developed under the official AI Building Blocks initiative, your site’s native capabilities are translated into standard MCP tools, resources, and prompts.[](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/) [[1]](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)[[2]](https://github.com/wordpress/mcp-adapter)
---

Core Features

- **Zero-Interface Admin** : Create, read, update, or delete posts and pages entirely via your AI client without logging into `wp-admin`.[](https://www.reddit.com/r/mcp/comments/1sbcwx7/i_built_a_wordpress_mcp_server_and_its_changed/) [[1]](https://www.reddit.com/r/mcp/comments/1sbcwx7/i_built_a_wordpress_mcp_server_and_its_changed/)[[2]](https://mcpservers.org/servers/kungtekno/wp-mcp)[[3]](https://instawp.com/wordpress-mcp/)[[4]](https://instawp.com/best-wordpress-mcp-servers-compared/)[[5]](https://instawp.com/wordpress-mcp-server/)
- **Media Operations** : Upload and manage media assets asynchronously using AI automation.[](https://mcpservers.org/servers/kungtekno/wp-mcp) [[1]](https://mcpservers.org/servers/kungtekno/wp-mcp)
- **System Introspection** : Inspect active plugins, switch themes, and perform diagnostic health checks using the official WordPress Abilities API.[](https://wordpress.org/plugins/royal-mcp/) [[1]](https://wordpress.org/plugins/royal-mcp/)[[2]](https://mcpservers.org/servers/kungtekno/wp-mcp)
- **Granular Security** : Leverages scoped WordPress **Application Passwords** , restricting the AI agent strictly to the user role permissions you assign.[](https://make.wordpress.org/ai/2025/07/17/mcp-adapter/) [[1]](https://make.wordpress.org/ai/2025/07/17/mcp-adapter/)[[2]](https://bionicwp.com/wordpress-mcp)


---

Popular Server Implementations If you are choosing an implementation for your workspace, consider these distinct solutions:

- **Official WordPress MCP Adapter** : Built by Automattic/WordPress contributors. It acts as a core bridge translating WordPress capabilities into standardized MCP primitives. Requires the companion proxy package `@automattic/mcp-wordpress-remote` to connect local apps via STDIO.[](https://github.com/Automattic/wordpress-mcp) [[1]](https://github.com/Automattic/wordpress-mcp)[[2]](https://www.youtube.com/watch?v=GRJYGLTpQLQ)[[3]](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)[[4]](https://developer.woocommerce.com/docs/features/mcp/)[[5]](https://github.com/Automattic/mcp-wordpress-remote)
- **[Royal MCP Plugin](https://wordpress.org/plugins/royal-mcp/)** : A security-first, production-ready solution available directly in the plugin directory. It features pre-configured OAuth 2.0, API key authentication, per-IP rate limiting, and 67 built-in tools that natively support core systems alongside popular plugins like WooCommerce, Advanced Custom Fields (ACF), and Elementor.[](https://wordpress.org/plugins/royal-mcp/) [[1]](https://wordpress.org/plugins/royal-mcp/)
- **[AI Engine Plugin](https://wordpress.org/plugins/ai-engine/)** : A popular third-party plugin by Jordi Meow that natively integrates an MCP bridge, allowing complete creation of site structure, posts, tags, and AI-generated imagery through continuous prompt interactions.[](https://www.reddit.com/r/Wordpress/comments/1kbdrji/claude_takes_over_wordpress_with_mcp/) [[1]](https://www.reddit.com/r/Wordpress/comments/1kbdrji/claude_takes_over_wordpress_with_mcp/)


---

Quick Setup Blueprint Connecting an AI client like Claude Desktop to your local or remote WordPress environment relies on standard JSON configurations.[](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/) [[1]](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)1. Generate Your Credentials

1. Log into your WordPress site dashboard.
2. Navigate to **Users** → **Profile**.
3. Scroll to **Application Passwords** , type a name (e.g., `Claude-MCP` ), and click **Add New**.
4. Copy the generated 24-character password string.[](https://github.com/deus-h/claudeus-wp-mcp) [[1]](https://github.com/deus-h/claudeus-wp-mcp)[[2]](https://www.cloudways.com/blog/manage-multiple-wordpress-sites/)

2. Configure Your AI Client Add the server configuration block to your application's settings file (e.g., `claude_desktop_config.json` for Claude Desktop or `mcp.json` for Cursor) using the Automattic proxy engine:[](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/) [[1]](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)[[2]](https://developer.wordpress.org/plugins/wordpress-org/using-the-mcp-server/)json```
{
  "mcpServers": {
    "wordpress-mcp-server": {
      "command": "npx",
      "args": ["-y", "@automattic/mcp-wordpress-remote@^0.2"],
      "env": {
        "WP_API_URL": "https://your-site-domain.com",
        "WP_API_USERNAME": "your-admin-username",
        "WP_API_PASSWORD": "xxxx xxxx xxxx xxxx xxxx xxxx"
      }
    }
  }
}
``` 
*(Note: Replace `WP_API_URL`, `WP_API_USERNAME` , and `WP_API_PASSWORD` with your setup's specific credentials).* [](https://developer.wordpress.org/plugins/wordpress-org/using-the-mcp-server/) [[1]](https://developer.wordpress.org/plugins/wordpress-org/using-the-mcp-server/)[[2]](https://github.com/stefans71/wordpress-mcp-server)3. Initialize and Run Restart your AI tool. You will see a 🔨 hammer icon or server confirmation message indicating that your agent has successfully discovered your custom WordPress tools and is ready to accept site commands.[](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/) [[1]](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)[[2]](https://github.com/deus-h/claudeus-wp-mcp)

---

## Rank 1: GitHub - Automattic/wordpress-mcp: ...
Source: https://github.com/Automattic/wordpress-mcp

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

---

## Rank 2: From Abilities to AI Agents: Introducing the WordPress MCP ...
Source: https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/

# From Abilities to AI Agents: Introducing the WordPress MCP Adapter
### Leave a Reply

Leave a Reply

Your email address will not be published. Required fields are marked *

Comment *

Name *

Email *

Save my name, email, and website in this browser for the next time I comment.

Notify me of follow-up comments by email.

Notify me of new posts by email.
### Learn how to contribute

[Learn how to contribute](https://developer.wordpress.org/news/how-to-contribute/)

Share your knowledge with fellow WordPress developers.
### Review tips and guidelines

[Review tips and guidelines](https://developer.wordpress.org/news/tips-and-guidelines-for-writers/)

Everything you need to know about writing for the Blog.

The [Abilities API introduced in WordPress 6.9](https://make.wordpress.org/core/2025/11/10/abilities-api-in-wordpress-6-9/) makes it possible to register WordPress functionality that is standardized, discoverable, typed, and executable. It provides a solid foundation on which WordPress developers can build and extend across the WordPress ecosystem.

It’s also a major step in making WordPress ready for AI automation and workflows. With Abilities, WordPress is positioned to take advantage of any current and future developments in Generative AI.

One of the biggest of these recent developments is the [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro), or MCP.

With MCP, it’s possible to provide additional context to the models which power AI tools. Let’s say you were using an AI tool to help you draft a report of all sales on your WordPress powered ecommerce site. Imagine if it was possible to give the AI secure access to all your orders for the year. If WordPress supported MCP, it would be.

Fortunately, the Core AI team has already thought of this, with the release of the [MCP Adapter](https://make.wordpress.org/ai/2025/07/17/mcp-adapter/). This adapter implements the Model Context Protocol in the scope of a WordPress site and lets AI tools (like Claude Desktop, Claude Code, Cursor, and VS Code) discover and call WordPress Abilities directly.

So let’s dive into the MCP Adapter. In this post, you’ll learn:

How to install and use the MCP Adapter in your WordPress plugins.

How to expose existing abilities as MCP tools, with practical examples.

How to connect popular AI clients to your WordPress-enabled MCP sites, whether local development environments or publicly accessible installs, to interact with your custom MCP tools.

What security considerations you need to be aware of.

How to start experimenting with the MCP adapter right away.

Table of Contents

[Quick recap: Abilities as the foundation](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[A primer on MCP tools, resources, and prompts](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[Installing the MCP Adapter](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[Enabling Abilities for the MCP Adapter default server](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[Transport methods](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[Claude Desktop](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[Claude Code](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[VS Code](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[Using MCP tools](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[Configuring custom MCP Servers for your plugins](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[Adding an MCP server to List All URLs](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[Security and best practices](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)

[How to start experimenting today](https://developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/)
## Quick recap: Abilities as the foundation

If this is the first time you’re reading about WordPress Abilities, it might be worthwhile to read the Introducing the [WordPress Abilities API](https://developer.wordpress.org/news/2025/11/introducing-the-wordpress-abilities-api/) post. However, if you don’t have the time to read that, here’s a quick recap.

The Abilities API gives WordPress a first-class, cross-context functional API that standardizes how core and plugins expose what they can do.

You define an ability once with:

A unique name ( namespace/ability-name )

A typed input schema and output schema

A permission_callback that enforces capabilities

An execute_callback that performs the actual functionality

The functionality triggered in the execute_callback can be anything from fetching data, updating posts, running diagnostics, or any other discrete unit of work.

Once registered, that ability is discoverable and executable from PHP, JavaScript, and the REST API.

WordPress 6.9 ships with 3 default abilities:

core/get-site-info : Returns site information configured in WordPress. By default, returns all fields, or optionally a filtered subset.

core/get-user-info : Returns basic profile details for the current authenticated user to support personalization, auditing, and access-aware behavior.

core/get-environment-info : Returns core details about the site’s runtime context for diagnostics and compatibility (environment, PHP runtime, database server info, WordPress version).

While only a small set of Core Abilities, they provide a foundation you can use to test the MCP adapter.
## What is the WordPress MCP Adapter?

The WordPress MCP Adapter is an official package in the [AI Building Blocks for WordPress](https://make.wordpress.org/ai/2025/07/17/ai-building-blocks/) initiative. Its job is to adapt Abilities registered by the Abilities API into the [primitives](https://modelcontextprotocol.io/docs/learn/architecture) supported by the Model Context Protocol (MCP) so that AI agents can discover and execute site functionality as MCP tools and read WordPress data as MCP resources.

In practice, this means: if your code already registers abilities, you are one step away from letting an AI agent use them.
### A primer on MCP tools, resources, and prompts

The Model Context Protocol organizes interactions into three main primitives: tools, which are executable functions the AI calls to perform actions; resources, which are passive data sources (like files or database rows) the AI reads for context; and prompts, which are pre-configured templates to guide specific workflows.

With the MCP adapter, Abilities are generally exposed as tools because they represent executable logic—fetching data, updating posts, or running diagnostics. However, the adapter is flexible: if an Ability simply provides read-only data, such as a debug log or a static site configuration, it can also be configured as a resource, allowing the AI to ingest that information as background context without needing to actively “call” it.
## Installing the MCP Adapter

The quickest way to get started with the MCP Adapter is to download and install it as a plugin from the [Releases page of the GitHub repository](https://github.com/WordPress/mcp-adapter/releases).

Once the plugin is installed and activated, it will register a default MCP server named mcp-adapter-default-server, and three custom abilities.

These abilities are also automatically exposed as MCP tools:

These three tools offer AI agents a [layered approach](https://engineering.block.xyz/blog/build-mcp-tools-like-ogres-with-layers) to accessing WordPress Abilities. Agents can discover which Abilities are available, get ability information, and execute abilities.
## Enabling Abilities for the MCP Adapter default server

By default, Abilities are only available via the MCP Adapter default server if they are explicitly marked as public for MCP access. For this, you need to add a meta.mcp.public flag to the ability registration arguments when you register your ability with wp_register_ability().

In the case of any Core Abilities, you can hook into the wp_register_ability_args filter to update their registration arguments to include the meta.mcp.public flag.

With this in place, you can start connecting AI clients to your WordPress site via the MCP Adapter and start calling these core abilities via the default server’s MCP tools.
### Transport methods

To communicate with a WordPress site that’s enabled as an MCP server, there are [two transport mechanisms](https://modelcontextprotocol.io/docs/learn/architecture) : STDIO and HTTP. Which one you use is generally decided by where the WordPress site is located.

For local WordPress development environments, the most straightforward way to connect is using STDIO transport. The MCP Adapter makes this possible via [WP-CLI](https://wp-cli.org/), so you need to have WP-CLI installed locally.

For the STDIO transport, at minimum you need to configure the following to connect to your MCP enabled WordPress site:

the server name in this case is wordpress-mcp-server. This can be any name you choose.

the command is wp, which is the WP-CLI command-line tool

the args array includes:

--path pointing to your WordPress installation

mcp-adapter serve to start the MCP Adapter server

--server specifying the MCP server to use (in this case, the default server)

--user specifying the WordPress user to authenticate as (in this case the admin user)

For any publicly accessible WordPress installations, or if you don’t want to use STDIO, you can set up an HTTP connection using the [@automattic/mcp-wordpress-remote](https://www.npmjs.com/package/@automattic/mcp-wordpress-remote) remote proxy. This requires you to have [Node.js](https://nodejs.org/en) installed on your computer, and to set up authentication using either [WordPress application passwords](https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/) or a custom OAuth implementation.

If you’re using the HTTP transport, your minimum configuration should look like this:

the server name stays the same

the command is npx, which executes Node.js packages

-y to automatically agree to install the package

@automattic/mcp-wordpress-remote@latest to use the latest version of the remote MCP proxy package

the env object includes:

WP_API_URL pointing to the MCP endpoint on your WordPress site

WP_API_USERNAME specifying the WordPress user to authenticate as

WP_API_PASSWORD specifying the application password for the user

For local WordPress installations connecting via the HTTP remote proxy, the mcp-wordpress-remote package [includes some troubleshooting tips](https://github.com/Automattic/mcp-wordpress-remote/blob/trunk/Docs/troubleshooting.md) if you run into any issues connecting. Usually, these issues are related to having multiple versions of Node.js installed or issues related to local SSL certificates.
### App-specific configurations

Now let’s look at where to configure your MCP server in the most popular AI applications, Claude Desktop, VS Code, Cursor, and Claude Code.

Note: For all the examples below, I’m using a Studio site named ‘WordPress MCP’ located at /Users/jonathanbossenger/Studio/wordpress-mcp and browsable via [http://localhost:8885/](http://localhost:8885/), with an admin user named admin. Make sure to replace these values with your own WordPress site path and user.
#### Claude Desktop

Being an Anthropic product, Claude Desktop was one of the first apps with built-in support for MCP servers. To add MCP servers to Claude Desktop, navigate to the Developer tab ( Claude → Settings → Developer ). Under Local MCP servers click Edit config.

This will open a file browser to the location of the claude_desktop_config.json file, where you can add your MCP server configurations.

MCP Servers are added to this file in a mcpServers object.

Here’s what the configuration looks like for connecting via STDIO transport:

Here’s what the configuration looks like for connecting via HTTP transport:

Once you save the configuration file, you will have to restart Claude Desktop, as it only reads the MCP server configurations on startup.

You should now see your MCP server listed in the Developer tab under Local MCP servers. If you see the running status next to your server name, you’re ready to start using it in your conversations.
#### Cursor

In Cursor, navigate to the Settings tab ( Cursor → Settings → Cursor Settings ), then select the Tools and MCP section.

Click on Add Custom MCP button, which will open the mcp.json configuration file for Cursor.

The configuration for Cursor is the same as for Claude Desktop. Once you’ve added your MCP server configuration, save the file and navigate back to the Tools and MCP section in Cursor settings. You should see your MCP server listed there, and you can enable it for use in your coding sessions.
#### Claude Code

To add MCP servers to Claude Code, you can either add the mcpServers object with the relevant server configs to the.claude.json file in your home directory, or create a.mcp.json file in your project directory. Adding the MCP servers to the project directory allows you to have different MCP server configurations for different projects, whereas adding them to the home directory makes them available globally across all projects.

Either way, you can use the same configuration format as Cursor or Claude Desktop.
#### VS Code

Configuring VS Code to connect to an MCP server requires setting up a [JSON configuration file that describes the MCP server details](https://code.visualstudio.com/docs/copilot/customization/mcp-servers). This file is usually named mcp.json and should be placed in a.vscode directory inside your project workspace.

The only difference between configuring VS Code and Claude Desktop is that you define your MCP servers in a servers object not an mcpServers object. The rest of the configuration is the same.

Once you create this file in your project workspace, VS Code displays an MCP control toolbar, where you can start, stop and restart the MCP server.

When the server has started correctly, it will also show you how many tools are available for the AI to use, in this case, three.
## Using MCP tools

With your MCP server connected to your AI application of choice, you can now start using the MCP tools exposed by the MCP Adapter.

For example, in Claude Desktop, you can start a new conversation asking Claude to “Get the site info from my WordPress site”.

It will determine that there is an available MCP server and call the mcp-adapter-discover-abilities tool to see what abilities are available. It will then determine that the core/get-site-info Ability will fulfill the request, and call the mcp-adapter-execute-ability tool, passing it the core/get-site-info Ability name. This will return the site info data, and the application will “answer” with the site information.
## Configuring custom MCP Servers for your plugins

While the MCP Adapter default server should cover most requirements, you may want to create a custom MCP server for your plugin. This allows you to have more control over how your abilities are exposed as MCP tools.

Implementing this requires installing the MCP Adapter package via Composer, and creating and registering a custom MCP server.

From your plugin directory, run the composer require command:

Then, make sure to load Composer’s autoloader in your main plugin file:

If it’s possible that multiple plugins on a site might depend on the MCP Adapter or Abilities API, the official documentation [recommends using the Jetpack Autoloader](https://github.com/WordPress/mcp-adapter/blob/trunk/docs/getting-started/installation.md) to avoid version conflicts.

The next step is to initialize the MCP Adapter in your plugin:

Finally, you can create a custom MCP server by hooking into the mcp_adapter_init action. The action callback function receives the McpAdapter instance. The adapter’s create_server() method is used to define the custom server, with the desired configuration.

The important parameters to note here are:

The first parameter is the unique server identifier. This is used when starting the MCP server via WP-CLI.

The second and third parameters define the REST API namespace and route for the MCP server.

The fourth and fifth parameters are the server name and description, which are displayed in AI applications when listing available MCP servers.

The sixth parameter is the server version.

The tenth parameter is an array of ability names that you want to expose as MCP tools. You can list multiple abilities here.

The rest of the parameters define the transport methods, error handling, and observability handlers. In this example, you’re using the HTTP transport, error logging, and observability handlers from the core MCP Adapter package. However, it is possible to create your own custom handlers if you want to integrate with your own transport, logging or monitoring systems.
## Adding an MCP server to List All URLs

To show you an example of creating a custom MCP server, let’s take the [List All URLs plugin](https://github.com/wptrainingteam/list-all-urls) from the Abilities API post, and add a custom MCP server to it.

Before you do this, deactivate the MCP Adapter plugin if you have it activated.

Next, clone the List All URLs GitHub repository inside your WordPress plugins directory:

You’ll also need to switch to the branch that includes the Abilities API implementation:

The plugin already uses Composer for dependency management, so run composer install to install the required packages.

Next require the mcp-adapter package:

Now, open the main plugin file list-all-urls.php, and add the following code at the bottom of the file to initialize the MCP Adapter and create a custom MCP server:

Notice that you don’t need to enable the meta.mcp.public flag for the list-all-urls/urls ability, because you’re explicitly exposing it via the custom MCP server.

Now activate the List All URLs plugin from the WordPress admin dashboard.

Once the plugin is activated, update your AI application’s MCP server configuration to use the new custom MCP server.

Here’s an example of the updated VS Code configuration to include both the default MCP server and the new custom MCP server from the List All URLs plugin, both using STDIO transport:

It’s possible to have multiple MCP servers configured in the same AI application. This allows you to switch between different WordPress sites or plugins that expose different sets of abilities.

Whatever AI application you’re using, make sure to either restart the application, or start the MCP server in the application after updating the MCP server configuration. You should see the new MCP server listed and be able to use the list-all-urls/urls ability as an MCP tool. You can then ask the AI to “List all URLs on my WordPress site”, and it will call the list-all-urls-urls tool via the MCP Adapter.
## Security and best practices

Because MCP clients act as logged-in WordPress users, always treat them as part of your application surface area by following these best practices:

Use permission_callback carefully

Each ability should check the minimum capability needed ( manage_options, edit_posts, etc.).

Avoid __return_true for destructive operations such as deleting content.

Use dedicated users for MCP access

Especially in production, create a specific role/user with limited capabilities.

Do not expose powerful abilities to unaudited AI clients.

Prefer read-only abilities for public MCP endpoints

For HTTP transports exposed over the internet, focus on read-only diagnostics, reporting, and content access.

Implement custom authentication if needed

The default authentication uses application passwords, but you can implement OAuth or other methods for better security.

Monitor and log usage

Use custom error and observability handlers to integrate with your logging/monitoring stack.
## How to start experimenting today

If you want to get started experimenting with the MCP adapter, a minimal “hello AI” path for a WordPress developer only requires you to register an ability, require and initialize the MCP Adapter, and connect an MCP-aware AI client.

If you already have plugins using the Abilities API, the MCP Adapter turns them into AI-ready APIs with very little additional work.

As with any new technology, start small. Begin by exposing a few non-destructive, read-only abilities as MCP tools. Test them with local AI clients like Claude Desktop or Cursor. Gradually expand to more complex abilities and workflows as you gain confidence. Be prepared to hit roadblocks, and engage with the WordPress AI and developer communities for support and collaboration. The documentation for both the [Abilities API](https://developer.wordpress.org/apis/abilities/) and the [MCP Adapter](https://github.com/WordPress/mcp-adapter) are great resources to help you along the way.

This combination of Abilities and the MCP Adapter gives WordPress developers a powerful path to build AI-assisted admin tools, automation, and workflows for both clients and teams.

Props to @ greenshady and @ bph for reviewing this post.

Share the post:

Share on Mastodon (Opens in new window) Mastodon

Share on LinkedIn (Opens in new window) LinkedIn

Share on X (Opens in new window) X

Share on Bluesky (Opens in new window) Bluesky

Share on Reddit (Opens in new window) Reddit

Share on Tumblr (Opens in new window) Tumblr

Share on Telegram (Opens in new window) Telegram

Share on WhatsApp (Opens in new window) WhatsApp
## 7 responses to “From Abilities to AI Agents: Introducing the WordPress MCP Adapter”

The progression from MCP access to OAuth 2.1 to an official connector in just a few months is impressive. The read-only approach is smart for a first release – it builds trust before opening write access.

Curious about one thing: as the Abilities API and MCP Adapter mature on the self-hosted side (especially with the recent meta.mcp.public registration pattern), are there plans to align the WordPress.com connector tools with that same abilities framework? It would be powerful if plugin developers could register capabilities once and have them work across both WordPress.com’s connector and the self-hosted MCP Adapter.

The page builder ecosystem is where this gets really interesting > Gutenberg works great with standard REST, but the millions of sites running Divi, Elementor, and Bricks need their builder-specific data structures understood by AI tools too. Would love to see the connector evolve to support that.

That’s a great question.

What I do know is that the WordPress.com MCP tools are powered by the same Abilities API and MCP Adapter I discuss in this blog post. Essentially what you are asking for “plugin developers could register capabilities once and have them work across both WordPress.com’s connector and the self-hosted MCP Adapter” should theoretically be possible. For example if you install the AI Experiments plugin on a WordPress.com site, the Abilities are all present and available.

The main difference between the two options at the moment is authentication. WordPress.com does this via OAuth 2.1, which you might have read about here: [https://wordpress.com/blog/2026/01/22/connect-ai-agents-to-wordpress-oauth-2-1/](https://wordpress.com/blog/2026/01/22/connect-ai-agents-to-wordpress-oauth-2-1/). For self hosted sites there currently isn’t an available OAuth solution, so you’re reliant on JWT Tokens or Application Passwords.

I registered the skills in respira.press plugin and MCP as WordPress Abilities. Curious if it worked.

i don’t know if links are allowed but posting this as a separate comment in case it needs to be deleted – [https://respira.press](https://respira.press/)

Video tutorial please

Great to see this shipped — the Abilities API is one of the most underrated additions in 6.9.

We took the same foundation and built the browser-side complement: WebMCP Abilities bridges any registered WordPress Ability to Chrome’s new WebMCP standard (navigator.modelContext).

So the MCP Adapter handles CLI/API agents (Claude Desktop, Cursor), and our plugin handles browser-based agents visiting your site.

Same abilities, two transports. Register once with wp_register_ability(), both plugins pick it up automatically.

Already running in production on wppopupmaker.com — here’s Gemini 2.5 Flash calling the tools live: [https://youtu.be/7A34ZNz2bMM](https://youtu.be/7A34ZNz2bMM)

Curious if the core team has thought about how the Abilities API might evolve to support both transports natively — or if the adapter/bridge pattern is the intended long-term approach?

The last time I checked the adapter/bridge pattern is intended as the long term approach. The idea being that if MCP is replaced by something new/better tomorrow (which, with the way AI is rapidly evolving, could be a possiblity) it’s much easier to pivot existing Abilities to the new protocol.
## Subscribe to the Blog

Email Address

Join 1,885 other subscribers

---

## Rank 3: Claude takes over WordPress with MCP
Source: https://www.reddit.com/r/Wordpress/comments/1kbdrji/claude_takes_over_wordpress_with_mcp/

_[No extractable body text]_

---

## Rank 5: WordPress/mcp-adapter: An MCP ...
Source: https://github.com/wordpress/mcp-adapter

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

---

## Rank 7: WordPress MCP Server
Source: https://mcpservers.org/servers/kungtekno/wp-mcp

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

---

## Rank 9: 10 Best WordPress MCP Servers to Try in 2026
Source: https://responsive.menu/10-best-wordpress-mcp-servers/

# 10 Best WordPress MCP Servers to Try in 2026

Jan 15, 2026

The Model Context Protocol has transformed how developers and agencies manage WordPress. Instead of clicking through wp-admin or writing custom scripts, you can now execute real WordPress operations, creating posts, managing plugins, and moderating comments, through natural language conversations with AI assistants like Claude.

But choosing the right WordPress MCP server matters. Setup complexity, feature coverage, security models, and maintenance requirements vary significantly across implementations.

We’ve evaluated the best MCP server WordPress solutions available in 2026, analyzing each for real-world developer and agency use cases.
## What Makes a WordPress MCP Server a Better Option

Not all [WordPress MCP servers](https://instawp.com/wordpress-mcp/) deliver equal value. The difference between a frustrating setup experience and a productive AI workflow often comes down to how well the server handles real-world developer and agency needs.

When evaluating MCP for WordPress implementations, these traits separate the exceptional from the mediocre:

Setup Simplicity: Minutes to first command, not hours of configuration

Tool Coverage: Comprehensive WordPress operations out of the box—content, taxonomies, media, users, plugins, themes

Authentication Flexibility: Token-based access with role inheritance and expiration controls

Multi-Site Support: Manage multiple WordPress installations without duplicating configurations

Security Architecture: Scoped permissions, instant revocation, encrypted transport

Staging Compatibility: Safe testing environments before production deployment

Maintenance Burden: Automatic updates versus manual dependency management
## Best WordPress MCP Servers: 10 Options to Explore

The WordPress MCP ecosystem has matured rapidly, with solutions ranging from fully managed platforms to specialized open-source implementations. Whether you prioritize zero-configuration setup, enterprise security, e-commerce capabilities, or maximum customization, there’s a WordPress MCP server designed for your workflow. Here are the top options for developers and agencies in 2026.
### 1. InstaWP WordPress MCP Server

InstaWP, the [managed WordPress cloud](https://instawp.com/), offers a built-in [WordPress MCP Server](https://instawp.com/wordpress-mcp-server/) that eliminates infrastructure complexity by building MCP directly into its managed WordPress platform.

While other WordPress MCP solutions require Node.js installations, npm packages, and configuration files, InstaWP delivers one-click activation.

Enable MCP from your site dashboard, copy the generated URL, paste it into Claude Desktop, and done.

The WordPress MCP plugin installs automatically, tokens generate instantly, and built-in staging environments let you test AI workflows without risking production sites.

📺 Watch the setup: [Enable MCP on WordPress sites using InstaWP](https://youtu.be/N4GIewmL_u4)

For agencies managing multiple clients, the centralized dashboard provides visual token management, role-based permissions, and multi-site control from a single interface.

Learn more about InstaWP’s [WordPress MCP server](https://instawp.com/wordpress-mcp-server/) and see how you can use it without any setup hassle.
#### Technical Specifications

Set-up Time : Under 2 Minutes

Hosting Model : Fully managed cloud infrastructure

Authentication : Token-based with WordPress role inheritance

Tool Coverage: 38+ tools (content, taxonomies, media, users, plugins, themes)
#### Best For

Agencies managing multiple client WordPress sites

Developers wanting immediate productivity without DevOps overhead

Teams with mixed technical skill levels need visual management

Anyone prioritizing speed-to-value over deep customization
#### Why Use It

InstaWP removes every friction point from WordPress MCP adoption. Zero configuration, built-in staging safety, visual token management, and automatic updates mean you spend time using MCP; not setting it up or maintaining it.

Get Started: [Instawp.com](https://instawp.com/)
### 2. Official WordPress MCP Server

The [official WordPress MCP server](https://github.com/Automattic/wordpress-mcp) from Automattic represents the enterprise-grade, core-aligned implementation. Built by WordPress.com’s team, it uses a two-component architecture: a local proxy ( mcp-wordpress-remote ) handling protocol communication and a WordPress MCP plugin ( mcp-adapter ) exposing site capabilities.

This separation provides maximum security isolation. The implementation supports OAuth 2.1, JWT, and Application Passwords, integrating with WordPress’s upcoming Abilities API for long-term core compatibility. If your organization requires spec-compliant, Automattic-backed infrastructure, this is the definitive choice.
#### Technical Specifications

Hosting Model: Self-hosted (local proxy + WordPress plugin)

Authentication: OAuth 2.1, JWT, Application Passwords

Tool Coverage: Extensible via PHP hooks and Abilities API

Setup Time: 15-30 minutes
#### Best For

Enterprise deployments requiring maximum security compliance

Organizations with existing Automattic/WordPress.com infrastructure

Teams wanting alignment with WordPress core development direction

Developers with DevOps resources for initial configuration
#### Why Use It

When security and long-term WordPress core alignment matter most, Automattic’s official MCP WordPress server is the safest bet. Enterprise authentication, spec compliance, and active maintenance from core contributors provide unmatched reliability.

Repository: [github.com/Automattic/wordpress-mcp](https://github.com/Automattic/wordpress-mcp)
### 3. InstaWP MCP-WP

Separate from their managed platform, InstaWP maintains an [open-source WordPress MCP server](https://github.com/InstaWP/mcp-wp) that developers can self-host anywhere. Launch instantly via npx -y @instawp/mcp-wp —no cloning or global installations required.

The server uses unified tool architecture: instead of separate tools for posts, pages, and custom post types, intelligent tools like list_content and create_content work across all content types.

With 38+ pre-built tools covering content, taxonomies, media, users, comments, plugins, and themes, it offers more out-of-the-box coverage than most MCP server WordPress alternatives.
#### Technical Specifications

Hosting Model: Self-hosted (Node.js process)

Authentication: Application Passwords via environment variables

Tool Coverage: 38+ unified tools (content, taxonomies, media, users, plugins, themes)

Setup Time: 5-10 minutes
#### Best For

Developers wanting InstaWP’s tool design without managed hosting

Self-hosted WordPress installations requiring local MCP

Teams needing to customize or extend MCP tools

Local development and staging environments
#### Why Use It

Get InstaWP’s thoughtfully designed MCP for WordPress implementation on your own infrastructure. One-line launch, unified tool architecture, and TypeScript codebase make it ideal for developers who want quality without lock-in.

Repository: [github.com/InstaWP/mcp-wp](https://github.com/InstaWP/mcp-wp)
### 4. docdyhr/mcp-wordpress

The [docdyhr WordPress MCP server](https://github.com/docdyhr/mcp-wordpress) takes a maximalist approach with approximately 59 pre-built tools—one of the most comprehensive WordPress MCP server implementations available. If WordPress exposes functionality via REST API, this server likely supports it.

Multiple installation methods (npm, DXT extension, Docker) accommodate different deployment preferences.

Extensive documentation with examples for every tool makes it particularly accessible for developers learning MCP WordPress patterns. The DXT extension option simplifies installation for users unfamiliar with Node.js environments.
#### Technical Specifications

Hosting Model: Self-hosted (Node.js or Docker container)

Tool Coverage: ~59 tools (comprehensive REST API coverage)

Setup Time: 10-15 minutes

Authentication: Application Passwords
#### Best For

Developers wanting maximum WordPress REST API coverage

Teams preferring Docker-based deployment workflows

Users who value extensive, example-rich documentation

Projects requiring access to obscure WordPress endpoints
#### Why Use It

When you need comprehensive REST API coverage and don’t want to build custom tools, docdyhr’s 59-tool library has you covered. Multiple installation methods and thorough documentation lower the barrier for WordPress MCP adoption.

Repository: [github.com/docdyhr/mcp-wordpress](https://github.com/docdyhr/mcp-wordpress)
### 5. mcp-wp/ai-comm

The [mcp-wp/ai-command](https://github.com/mcp-wp/ai-command) takes a fundamentally different approach; instead of building another standalone server, it extends WP-CLI with MCP capabilities. For developers already using WP-CLI in their workflows, this MCP for WordPress solution feels native.

Execute WordPress operations through AI while leveraging WP-CLI’s battle-tested command structure. The integration means you get MCP’s conversational interface combined with WP-CLI’s comprehensive WordPress control, posts, users, plugins, themes, database operations, and everything else [WP-CLI](https://instawp.com/features/commands/) supports.

For agencies with existing WP-CLI automation scripts, this WordPress MCP server bridges AI capabilities into established workflows without replacing them.
#### Technical Specifications

Hosting Model: Self-hosted (WP-CLI extension)

Authentication: WP-CLI authentication (SSH, local, or remote)

Tool Coverage: Full WP-CLI command coverage (100+ commands across all WordPress operations)

Setup Time: 10-15 minutes
#### Best For

Developers with existing WP-CLI workflows and scripts

Teams comfortable with command-line WordPress management

Server administrators managing WordPress at the infrastructure level

Agencies wanting AI capabilities without abandoning WP-CLI expertise
#### Why Use It

Why learn a new tool when you can enhance one you already know? This WordPress MCP implementation brings AI to WP-CLI; leverage your existing command-line expertise while adding conversational control to established workflows.

Repository: [github.com/mcp-wp/ai-command](https://github.com/mcp-wp/ai-command)
### 6. WordPress-MCP

The [WordPress MCP](https://github.com/Utsav-Ladani/WordPress-MCP) by a developer, Utsav, server differentiates itself through block-native content generation. Unlike servers treating posts as simple text fields, this implementation understands [WordPress block editor](https://instawp.com/wordpress-classic-editor-vs-block-editor/) (Gutenberg) schemas. AI-generated content arrives as properly structured blocks, headings, paragraphs, lists, images, not raw HTML or plain text.

Launch via npx -y wordpress-mcp without installation. For content-heavy sites where block structure matters, this MCP WordPress plugin alternative delivers publication-ready formatting directly from AI prompts.
#### Technical Specifications

Hosting Model: Self-hosted (Node.js via npx)

Tool Coverage: 15+ tools (block-focused content creation and management)

Setup Time: 5-10 minutes

Authentication: Application Passwords
#### Best For

Content-heavy WordPress sites using Gutenberg editor

AI-powered blogging and content marketing tools

Agencies producing structured, formatted content at scale

Developers building content pipelines requiring block formatting
#### Why Use It

If your WordPress workflow depends on properly structured Gutenberg blocks, this WordPress MCP server delivers. AI-generated content arrives block-formatted and publication-ready; no manual restructuring required.

Repository: [github.com/Utsav-Ladani/WordPress-MCP](https://github.com/Utsav-Ladani/WordPress-MCP)
### 7. prathammanocha/wordpress-mcp-server

This [comprehensive WordPress MCP server](https://github.com/prathammanocha/wordpress-mcp-server) targets full-scale admin workflows, extending beyond basic content management. Its standout feature is the custom_request tool, enabling arbitrary REST API calls, chaining multiple operations, accessing custom endpoints, and building advanced automation sequences impossible with fixed tool sets.

The server supports both development and production use cases with automatic recompilation during development ( npm run dev ). For developers comfortable with WordPress internals who need flexibility beyond pre-defined tools, this MCP server WordPress implementation provides escape hatches.
#### Technical Specifications

Hosting Model: Self-hosted (Node.js with dev/production modes)

Tool Coverage: 30+ tools + custom_request for arbitrary REST API calls

Setup Time: 10-15 minutes

Authentication: Application Passwords
#### Best For

Developers building complex, multi-step automation sequences

Teams requiring arbitrary REST API access through MCP

Advanced users are comfortable with WordPress REST API internals

Projects integrating custom plugin endpoints
#### Why Use It

Pre-defined tools can’t cover every use case. The custom_request tool lets you call any WordPress REST endpoint through MCP, making this WordPress MCP implementation the most flexible for advanced workflows.

Repository: [github.com/prathammanocha/wordpress-mcp-server](https://github.com/prathammanocha/wordpress-mcp-server)
### 8. emzimmer/server-wp-mcp

The [emzimmer WordPress MCP server](https://github.com/emzimmer/server-wp-mcp) is architected specifically for multi-site management. Configure all your WordPress sites in a single JSON file with aliases, then address them naturally in prompts: “List posts on client-alpha” or “Create a page on staging-beta.”

Dynamic endpoint discovery automatically maps available [WordPress REST API](https://instawp.com/wordpress-rest-api/) endpoints for each connected site. For agencies juggling dozens of client installations, this MCP for WordPress approach centralizes control without requiring separate MCP configurations per site.
#### Technical Specifications

Hosting Model: Self-hosted (Node.js with JSON config)

Authentication: Application Passwords per site (stored in config file)

Tool Coverage: 20+ tools with automatic per-site endpoint discovery

Setup Time: 10-15 minutes
#### Best For

Agencies managing multiple client WordPress sites

Developers with many WordPress installations to control

Teams wanting centralized multi-site MCP management

Projects requiring cross-site operations and audits
#### Why Use It

Managing ten sites shouldn’t require ten MCP configurations. This WordPress MCP server centralizes multi-site control with alias-based addressing—one server, unlimited sites, natural language targeting.

Repository: [github.com/emzimmer/server-wp-mcp](https://github.com/emzimmer/server-wp-mcp)
### 9. wp-elementor-mcp

The [wp-elementor-mcp](https://github.com/worldpeaceworker/wp-elementor-mcp) is a modular Model Context Protocol (MCP) server specifically engineered for WordPress and Elementor.

Unlike general WordPress tools, this WordPress MCP server specializes in deep integration with the Elementor page builder, allowing AI assistants to manipulate sections, containers, and widgets directly.

It uses an intelligent configuration system to scale from 20 to 34 specialized tools based on the user’s technical requirements and license level.
#### Technical Specifications

Hosting Model: Self-Hosted / Local Bridge

Authentication: WordPress Application Passwords

Setup Time: 5-10 minutes

Tool Coverage: 30+ tools
#### Best For

Users who need to create or modify complex [Elementor](https://instawp.com/plugin/elementor/) layouts via natural language.

Teams looking for “Content Discovery” tools with visual Elementor status indicators.

Developers requiring granular control over Elementor data chunks and incremental widget updates.

Professionals managing high-performance sites who need specific tools for [cache](https://instawp.com/most-effective-wordpress-cache-plugins/) clearing and element reordering.
#### Why Use It

It doesn’t just edit text; it can create sections, columns, and flexbox containers from scratch. Users can choose between Essential, Standard, Advanced, or Full modes to avoid “tool bloat” in their AI interface.

Repository: [GitHub – worldpeaceworker/wp-elementor-mcp: MCP server for interacting with Elementor and WordPress through natural language](https://github.com/worldpeaceworker/wp-elementor-mcp)
### 10. stefans71/wordpress-mcp-server

The [stefans71 WordPress MCP server](https://github.com/stefans71/wordpress-mcp-server) provides a straightforward, no-frills implementation ideal for learning MCP patterns or lightweight deployments. It focuses on core content operations without the feature sprawl of larger implementations.

The clean, readable codebase makes it an excellent starting point for developers who want to understand WordPress MCP internals before committing to more complex solutions. Basic CRUD operations for posts work reliably out of the box, with clear extension points for adding custom functionality.
#### Technical Specifications

Hosting Model: Self-hosted (lightweight Node.js process)

Tool Coverage: 10+ tools (core content CRUD operations)

Setup Time: 5-10 minutes

Authentication: Application Passwords
#### Best For

Developers learning MCP patterns and WordPress integration

Lightweight deployments needing basic content operations

Teams wanting a simple foundation to customize

Hobbyists and learners exploring AI-WordPress connections
#### Why Use It

Sometimes simpler is better. This WordPress MCP implementation provides a clean, understandable codebase, perfect for learning MCP internals or deploying lightweight content automation without enterprise complexity.

Repository: [github.com/stefans71/wordpress-mcp-server](http://github.com/stefans71/wordpress-mcp-server)
### Choosing the Right WordPress MCP Server

For fastest time-to-value : InstaWP’s managed solution eliminates all setup friction.

For enterprise security: Automattic’s official implementation with OAuth 2.1.
## Final Say

The WordPress MCP ecosystem continues evolving rapidly. Whatever your requirements, managed simplicity, enterprise security, e-commerce specialization, or maximum flexibility, there’s a [WordPress MCP server](https://instawp.com/wordpress-mcp/) built for your workflow.

Ready to start?

Start building WordPress with [InstaWP](https://instawp.com/) today.

It offers the fastest path from zero to productive WordPress MCP integration, one click to enable, and under two minutes to your first AI-executed WordPress operation.
#### Popular Articles

[InstaWP’s WordPress Migration Tool: A Detailed Review](https://responsive.menu/instawp-wordpress-migration-tool-review/)

[What is a Full Site Editing Theme in WordPress?](https://responsive.menu/full-site-editing-theme-in-wordpress/)

[3.1.12 Released – Sub Menu Speed, Header Bar Logo Sizing and more](https://responsive.menu/3-1-12-released-sub-menu-speed-header-bar-logo-sizing/)

[Responsive.Menu Feb 2020 Update](https://responsive.menu/responsive-menu-feb-2020-update/)

[Improved Mega Menu Functionality](https://responsive.menu/improved-mega-menu-functionality/)

[Free Version 2.8.6 Released – Push animation bug fixes](https://responsive.menu/free-version-2-8-6-released-push-animation-bug-fixes/)

[How to Move the WordPress Navigation Menu?](https://responsive.menu/move-wordpress-navigation-menu/)

[Season’s Greetings from Responsive Menu!](https://responsive.menu/christmas-and-new-year-deal/)

[WordPress Mobile Menu: How to Set Up and Customize One (2026)](https://responsive.menu/wordpress-mobile-menu-how-to-set-up-and-customize-one-2026/)

[How to Create a Menu in WordPress (Beginner Guide 2026)](https://responsive.menu/how-to-create-a-menu-in-wordpress-beginner-guide-2026/)

---

## Rank 10: Using WordPress MCP as a Development Tool
Source: https://webdevstudios.com/2025/06/11/using-wordpress-mcp-as-a-development-tool/

# 
##### Development

[Development](https://webdevstudios.com/category/development/)
# Using WordPress MCP as a Development Tool

Over the past few days, I’ve been testing the WordPress MCP server. I’ve got it running now, and honestly, it’s one of those tools that, even if not many people are using it yet, can really make life easier for developers working with WordPress every day. In this post, I’ll walk you through what it is, how to install it, what it’s for, how to extend it, and I’ll leave the door open for a future topic: the Feature API.
## What’s an MCP?

MCP stands for “Model Context Protocol.” It’s a structured way to connect external tools or AI agents to a local or remote system. In simple terms, it enables outside clients to interact with WordPress in a standard and predictable manner, utilizing well-defined tools and resources.
## What’s the WordPress MCP?

Automattic released a plugin called wordpress-mcp that turns your WordPress site into an MCP-compatible interface. This plugin doesn’t do anything visible on its own, instead, it exposes a set of tools that can be called by an external runner.
## How to Install (Local Dev Setup Using WP-CLI and Git)

Assuming you already have a local WordPress environment, run this:

Once activated, go to Settings > MCP in wp-admin and enable the plugin.

Then, in the same environment, clone the remote client.

This client acts as the MAP (Model Action Protocol) server. It’s what listens for instructions from tools like Claude or Cursor and talks to your WordPress site through the MCP interface provided by the plugin.
## Using the Remote Client

The mcp-wordpress-remote client is what receives instructions from agents like Cursor and sends them to your WordPress MCP plugin. Think of it as the bridge between the agent and your local site.

⚠️ Important: The wordpress-mcp plugin does not operate on its own. It only exposes functionality when the remote client is running and connected.

Configuration details: [https://github.com/Automattic/mcp-wordpress-remote](https://github.com/Automattic/mcp-wordpress-remote)

✅ Heads-up: This project is still under active development — behavior, defaults, and setup requirements may change. Always check the latest documentation.
## What can we do with it?

Once everything is running, you can do things like:

Create draft posts

Fetch recent content

Query users

List comments

Basically, anything exposed as a tool by the MCP plugin can be triggered by an agent. It’s incredibly helpful when building integrations, testing flows, or speeding up repetitive tasks.

Here’s a more practical example: imagine you’re working on a feature that depends on listing or displaying posts. Instead of manually creating test content, you could ask your agent (via Cursor or Claude): “Create 10 draft posts titled ‘Test Feature Post #1–10’ with placeholder content.” It will immediately create those entries on your site via the MCP API.

Or say you’re building a new layout that depends on specific plugins. You could type: “Install the following plugins from the WordPress repo: Gutenberg, Query Monitor, and FakerPress.” This saves you time during setup, allowing you to focus on writing or debugging the actual feature logic.

You can even use it for debugging. For example, you could say: “Check the latest PHP debug log and summarize the issue.” Cursor will read the debug_log file from your local environment and give you a quick explanation or suggestion on how to fix it. It’s like having a dev assistant that not only runs commands, but helps you understand what’s going wrong. You’re not building mock data manually anymore — the agent handles it all via WordPress MCP.
## Adding Your Tools

You can extend the plugin by adding custom tools to the /includes/Tools/ directory. Each tool includes:

A name

An input schema

A PHP function that performs the operation

Just follow the structure of existing tools in the plugin. This gives you full control to expose any internal logic you need.

Here’s a minimal example of a custom tool class:

Once registered, this tool will be available through the MCP interface.
## Wrap-up

WordPress MCP is still in early development, but it’s already proving useful for local dev workflows and automation. If you’ve tried it or plan to, let us know how it goes.
### Share this:

Share on Facebook (Opens in new window) Facebook

Share on LinkedIn (Opens in new window) LinkedIn

Share on X (Opens in new window) X

Never miss important WordPress news ever again.

For the past few years, the C-Suite has been sold a massive promise regarding Artificial Intelligence: it will revolutionize your business. Yet, when enterprise leaders look at their actual operations, the reality often falls short. The Abilities API changes that. Why? Because it opens...

Starting a new enterprise WordPress project is exciting, but the planning and budgeting phases are not. Those can feel incredibly daunting. How do you accurately estimate costs? How do you avoid “scope creep”? And most importantly, how do you choose the right partner to...

It’s 2025, and WordPress is far from the simple blogging tool it once was. Today, it powers everything from personal portfolios to massive enterprise websites and shows no sign of slowing down. At WebDevStudios, we strive to have our finger on the pulse of...

[Contact Us](https://webdevstudios.com/contact/)

[Privacy Policy](https://webdevstudios.com/privacy-policy/)

[Website Strategy](https://webdevstudios.com/services/website-strategy/)

[WordPress Design](https://webdevstudios.com/services/design/)

[WordPress Development](https://webdevstudios.com/services/wordpress-development/)

[Performance & Security](https://webdevstudios.com/services/wordpress-performance-security/)

[Content Migrations](https://webdevstudios.com/services/data-migration/)

[Ongoing Website Development & Support](https://webdevstudios.com/services/ongoing-website-development-support/)

[About Us](https://webdevstudios.com/about/)

[Our Team](https://webdevstudios.com/about/team/)

[Company History](https://webdevstudios.com/about/history/)

[WordPress Books](https://webdevstudios.com/books/)

[WDS Gives Back](https://webdevstudios.com/about/how-wds-gives-back/)

[Custom Post Type UI Pro](https://pluginize.com/plugins/custom-post-type-ui-pro/)

[ThemeSwitcher Pro](https://themeswitcher.com/)

[WP Search w/ Algolia Pro](https://pluginize.com/plugins/wp-search-with-algolia-pro/)

[Link to Facebook Link to Facebook](https://facebook.com/webdevstudios)

[Link to Twitter Link to Twitter](https://twitter.com/webdevstudios)

[Link to Github Link to Github](https://github.com/webdevstudios)

[Link to Wordpress Link to Wordpress](https://profiles.wordpress.org/webdevstudios/)

[Link to Instagram Link to Instagram](https://www.instagram.com/webdevstudios/)

[Link to Retro Link to Retro](https://webdevstudios.com/retro-wds/)

[Link to RSS Feed Link to RSS](https://webdevstudios.com/feed/rss/)

[Website Strategy](https://webdevstudios.com/services/website-strategy/)

[Custom Design](https://webdevstudios.com/services/design/)

[Custom Development](https://webdevstudios.com/services/wordpress-development/)

[Performance & Security](https://webdevstudios.com/services/wordpress-performance-security/)

[Ongoing Support](https://webdevstudios.com/services/ongoing-website-development-support/)

[Content Migrations](https://webdevstudios.com/services/data-migration/)

[WordPress Website Audit](https://webdevstudios.com/services/wordpress-website-audit/)

[Consumer Packaged Goods](https://webdevstudios.com/solutions/consumer-packaged-goods/)

[Headless WordPress](https://webdevstudios.com/solutions/wordpress-headless-cms/)

[WordPress VIP](https://webdevstudios.com/solutions/wordpress-vip/)

[WordPress Books](https://webdevstudios.com/books/)

[WDS History](https://webdevstudios.com/about/history/)

[WDS Gives Back](https://webdevstudios.com/about/how-wds-gives-back/)

---

## Rank 11: WordPress MCP — Let AI Manage Your WordPress Site
Source: https://bionicwp.com/wordpress-mcp

# Your AI agent can now manage WordPress.

Connect Claude, Cursor, Cline, Continue, or any MCP-compatible AI directly to your WordPress site. Create posts, update WooCommerce products, moderate comments, install plugins, clear cache, and more — all from chat.

Update the homepage CTA

Create a WooCommerce coupon for 20% off

Install RankMath and activate it

Clear cache and check site health

Publish this markdown as a blog post

Plugin installed

rank-math/seo · v1.0.224

Product updated

SKU-2244 · price $49 → $39

Cache cleared

edge + object cache · 1.2s

SEO meta updated

/pricing · 142 chars

Page published

/wordpress-mcp · live
## What is WordPress MCP?

WordPress MCP gives AI agents secure, authenticated access to your WordPress site using the Model Context Protocol.

AI Agent

Claude · Cursor · Cline

MCP Adapter

Abilities API

WordPress Site

REST + capabilities
### Secure application passwords

Scoped, revokable credentials — never share wp-admin.
### One-click setup in BionicWP

Enable MCP for any site from your dashboard.
### WordPress 6.9+ support

Built on the official WordPress Abilities API.
### Remote AI management

Manage sites from anywhere your AI agent runs.
### Works with local AI clients

Claude Desktop, Cursor, Continue, Cline, and more.
### Capability-based access

Honors WordPress roles and custom permissions.
## What your AI can do

Real WordPress actions, grouped by what they touch.
### Posts & Pages

Create posts

Update pages

Delete content

Manage categories

Manage tags

Read/write custom fields
### WooCommerce

Create products

Update pricing

Manage stock

Create coupons

Update orders
### SEO

Yoast SEO support

RankMath support

Update SEO titles

Update meta descriptions

Manage focus keywords
### Site Management

Install plugins

Activate/deactivate plugins

View available updates

Clear cache

Site health checks

Update settings
### Users & Moderation

Create users

Update user roles

Moderate comments

Manage permissions
### Developer Features

ACF support

Custom MCP abilities

JSON schema support

Permission callbacks

WP_Error support

Extend via plugin

built-in abilities included

And fully extensible via the WordPress Abilities API.
## How it works

Three steps to give your AI real WordPress capabilities.
### Enable MCP

Flip the WordPress MCP toggle from your BionicWP dashboard. The MCP adapter plugin installs and configures itself.

mcp-adapter · installed · active
### Generate application password

Create a scoped application password from your WordPress profile — separate from wp-admin, revokable anytime.

Application Password

xxxx xxxx xxxx xxxx
### Connect your AI client

Paste the config into Claude, Cursor, Cline, Continue — or any MCP-compatible client.
### mcp-config.json

Claude Desktop

Claude Code

MCP-compatible agents
## Extend MCP with your own abilities.

Register custom tools with JSON schema input, execute callbacks, and capability checks. Plugin-friendly, secure by default.

WordPress Abilities API

Custom MCP tools

Secure execution callbacks

Plugin-friendly architecture

JSON schema definitions

Extensible system
## Built on WordPress's own security model.

No new attack surface. No shared admin passwords. Every action runs through the same capability checks WordPress already uses.
### Application passwords

Generated per AI client, never your wp-admin password.
### Revokable access

Kill any client's access in one click — no password reset required.
### No wp-admin sharing

Your real credentials never leave WordPress.
### Capability-based permissions

Honors current_user_can() — AI inherits user role.
### Local AI clients supported

Run Claude Desktop or Cursor locally — no third-party relay.
### Fine-grained access control

Permission callbacks per tool, per ability.
## Who it's for

From agencies running 50 sites to solo developers building custom workflows.
### Agencies

Manage dozens of WordPress sites through AI.
### Content Teams

Create and optimize content faster.
### Ecommerce

Update products, pricing, and inventory from chat.
### Developers

Build custom AI-powered workflows.
### Support Teams

Moderate comments, clear cache, check health instantly.
### Traditional WordPress workflow

Endless wp-admin clicks

Multiple dashboards

Manual repetitive work

Plugin hunting

Slow workflows
### AI-native WordPress workflow

Natural language control

Unified workflows

Instant actions

AI-assisted management

Faster execution
## Your WordPress site is now AI-native.

Enable WordPress MCP in one click and give your AI real capabilities.
### Start a conversation

We'll need a few details to get started.

Loading articles...

---

