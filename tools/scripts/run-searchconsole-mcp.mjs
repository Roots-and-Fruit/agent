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

function adcCredentialsPath() {
  if (process.platform === "win32") {
    const appData = process.env.APPDATA;
    if (!appData) {
      return null;
    }
    return path.join(appData, "gcloud", "application_default_credentials.json");
  }
  const home = process.env.HOME;
  if (!home) {
    return null;
  }
  return path.join(home, ".config", "gcloud", "application_default_credentials.json");
}

const adcPath = adcCredentialsPath();
if (!adcPath || !fs.existsSync(adcPath)) {
  console.error("Google Application Default Credentials not found.");
  console.error("One-time setup (PowerShell — quote scopes):");
  console.error(`  gcloud config set project YOUR_GCP_PROJECT_ID`);
  console.error(
    '  gcloud auth application-default login --scopes="https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform"'
  );
  console.error("  gcloud auth application-default set-quota-project YOUR_GCP_PROJECT_ID");
  console.error("Or: .\\tools\\scripts\\setup-searchconsole-adc.ps1 -ProjectId YOUR_GCP_PROJECT_ID");
  process.exit(1);
}

const fileEnv = parseEnvFile(envPath);
const childEnv = {
  ...process.env,
  ...fileEnv,
};

const packageSpec = "@vmandic/searchconsole-mcp";
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
