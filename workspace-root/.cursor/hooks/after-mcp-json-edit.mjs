import path from "node:path";
import process from "node:process";

const input = JSON.parse(await readStdin());
const filePath = normalizePath(String(input.file_path ?? ""));

if (!filePath.endsWith(`${path.sep}mcp.json`)) {
  process.stdout.write("{}");
  process.exit(0);
}

const isTemplate = filePath.includes(
  `${path.sep}workspace-root${path.sep}.cursor${path.sep}mcp.json`
);

const lines = isTemplate
  ? [
      "R&F MCP template edited.",
      "Run from agent/: .\\tools\\scripts\\sync-workspace-root.ps1",
      "Then: .\\tools\\scripts\\test-mcp-config.ps1",
      "Reload Cursor. Doc: agent/agent_docs/mcp-workspace-layout.md",
    ]
  : [
      "R&F MCP config edited outside the template.",
      "Cursor uses different mcp.json files depending on which folder you opened (parent vs agent/).",
      "Do not hand-edit this file — changes may be overwritten or invisible in Settings.",
      "Edit agent/workspace-root/.cursor/mcp.json only, then run sync-workspace-root.ps1.",
      "Doc: agent/agent_docs/mcp-workspace-layout.md",
    ];

process.stdout.write(
  JSON.stringify({
    additional_context: lines.join("\n"),
  })
);

function normalizePath(p) {
  return p.replace(/\//g, path.sep);
}

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      data += chunk;
    });
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}
