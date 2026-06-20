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
