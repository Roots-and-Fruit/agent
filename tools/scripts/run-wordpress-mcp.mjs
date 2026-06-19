import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { spawn } from "node:child_process";

const clientRoot = path.resolve(import.meta.dirname, "..", "..");
const envPath = path.join(clientRoot, ".env");

function parseEnvFile(filePath) {
  const env = {};
  if (!fs.existsSync(filePath)) {
    return env;
  }

  for (const rawLine of fs.readFileSync(filePath, "utf8").split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) {
      continue;
    }
    const index = line.indexOf("=");
    if (index === -1) {
      continue;
    }
    const key = line.slice(0, index).trim();
    let value = line.slice(index + 1).trim();
    value = value.replace(/^['"]|['"]$/g, "");
    env[key] = value;
  }
  return env;
}

const fileEnv = parseEnvFile(envPath);
const url = fileEnv.ROOTSANDFRUIT_MCP_URL ?? process.env.ROOTSANDFRUIT_MCP_URL ?? process.env.WP_API_URL;
const username =
  fileEnv.ROOTSANDFRUIT_MCP_USERNAME ?? process.env.ROOTSANDFRUIT_MCP_USERNAME ?? process.env.WP_API_USERNAME;
const password =
  fileEnv.ROOTSANDFRUIT_MCP_PASSWORD ?? process.env.ROOTSANDFRUIT_MCP_PASSWORD ?? process.env.WP_API_PASSWORD;

const missing = [];
if (!url?.trim()) missing.push("ROOTSANDFRUIT_MCP_URL");
if (!username?.trim()) missing.push("ROOTSANDFRUIT_MCP_USERNAME");
if (!password?.trim()) missing.push("ROOTSANDFRUIT_MCP_PASSWORD");

if (missing.length > 0) {
  console.error(`Missing WordPress MCP env vars: ${missing.join(", ")}`);
  console.error(`Expected in ${envPath} or process environment.`);
  process.exit(1);
}

const childEnv = {
  ...process.env,
  ...fileEnv,
  WP_API_URL: url.trim(),
  WP_API_USERNAME: username.trim(),
  WP_API_PASSWORD: password.trim(),
  OAUTH_ENABLED: process.env.OAUTH_ENABLED ?? "false",
};

const packageSpec = "@automattic/mcp-wordpress-remote@latest";
let spawnCommand;
let spawnArgs;

if (process.platform === "win32") {
  // npx.cmd cannot be spawned with shell:false (EINVAL). cmd.exe breaks paths with "&".
  const nodeExe = process.execPath;
  const npxCli = path.join(path.dirname(nodeExe), "node_modules", "npm", "bin", "npx-cli.js");
  spawnCommand = nodeExe;
  spawnArgs = [npxCli, "-y", packageSpec];
} else {
  spawnCommand = "npx";
  spawnArgs = ["-y", packageSpec];
}

const child = spawn(spawnCommand, spawnArgs, {
  cwd: clientRoot,
  env: childEnv,
  stdio: "inherit",
  shell: false,
});

child.on("exit", (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
    return;
  }
  process.exit(code ?? 1);
});
