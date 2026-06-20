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
const apiKey = fileEnv.PLAUSIBLE_API_KEY ?? process.env.PLAUSIBLE_API_KEY;

if (!apiKey?.trim()) {
  console.error("Missing Plausible env var: PLAUSIBLE_API_KEY");
  console.error(`Expected in ${envPath} or process environment.`);
  console.error("Create a key at https://plausible.io/settings");
  process.exit(1);
}

const childEnv = {
  ...process.env,
  ...fileEnv,
  PLAUSIBLE_API_KEY: apiKey.trim(),
};

if (!childEnv.PLAUSIBLE_BASE_URL?.trim()) {
  childEnv.PLAUSIBLE_BASE_URL = "https://plausible.io";
}

const packageSpec = "plausible-mcp";
let spawnCommand;
let spawnArgs;

if (process.platform === "win32") {
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
