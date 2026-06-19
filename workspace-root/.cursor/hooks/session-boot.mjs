import fs from "node:fs";
import path from "node:path";

const projectDir = process.env.CURSOR_PROJECT_DIR ?? process.cwd();
const agentDir = fs.existsSync(path.join(projectDir, "agent"))
  ? path.join(projectDir, "agent")
  : projectDir;

process.stdout.write(
  JSON.stringify({
    env: {
      RF_PROJECT_DIR: projectDir,
      RF_AGENT_DIR: agentDir,
    },
  })
);
