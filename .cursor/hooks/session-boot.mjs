import fs from "node:fs";
import path from "node:path";

const projectDir = process.env.CURSOR_PROJECT_DIR ?? process.cwd();
const parentAgentScripts = path.join(
  projectDir,
  "agent",
  "tools",
  "scripts",
  "run-wordpress-mcp.mjs"
);
const agentOnlyScripts = path.join(
  projectDir,
  "tools",
  "scripts",
  "run-wordpress-mcp.mjs"
);

let agentDir = projectDir;
let openMode = "unknown";
let mcpConfigActive = path.join(projectDir, ".cursor", "mcp.json");

if (fs.existsSync(parentAgentScripts)) {
  openMode = "parent-or-workspace";
  agentDir = path.join(projectDir, "agent");
  mcpConfigActive = path.join(projectDir, ".cursor", "mcp.json");
} else if (fs.existsSync(agentOnlyScripts)) {
  openMode = "agent-only";
  agentDir = projectDir;
  mcpConfigActive = path.join(projectDir, ".cursor", "mcp.json");
}

process.stdout.write(
  JSON.stringify({
    env: {
      RF_PROJECT_DIR: projectDir,
      RF_AGENT_DIR: agentDir,
      RF_WORKSPACE_OPEN_MODE: openMode,
      RF_MCP_CONFIG_ACTIVE: mcpConfigActive,
    },
  })
);
