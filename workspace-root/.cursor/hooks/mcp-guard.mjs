import process from "node:process";

const input = JSON.parse(await readStdin());
const toolName = String(input.tool_name ?? "");
const toolInputRaw = input.tool_input;
const toolInput =
  typeof toolInputRaw === "string"
    ? safeParse(toolInputRaw)
    : toolInputRaw && typeof toolInputRaw === "object"
      ? toolInputRaw
      : {};

const isWordPressMcp =
  /wordpress|rootsandfruit|mcp-adapter|execute-ability|discover-abilities/i.test(
    `${toolName} ${JSON.stringify(input.command ?? "")} ${JSON.stringify(input.url ?? "")}`
  );

const allow = { permission: "allow" };

if (!isWordPressMcp) {
  process.stdout.write(JSON.stringify(allow));
  process.exit(0);
}

const abilityName = String(
  toolInput.ability_name ?? toolInput.name ?? toolInput.tool ?? ""
);

let agent_message =
  "R&F MCP: prefer rootsandfruit/* abilities over WP REST. Block body → blocks-* only; title/excerpt → update-post.";

if (/execute-ability/i.test(toolName) && abilityName) {
  if (/^rootsandfruit\/blocks-/.test(abilityName)) {
    agent_message +=
      " blocks-insert/update: include innerHTML for static core blocks.";
  }
  if (/update-post/i.test(abilityName)) {
    agent_message += " Do not send block body HTML through update-post.";
  }
}

process.stdout.write(
  JSON.stringify({
    permission: "allow",
    agent_message,
  })
);

function safeParse(value) {
  try {
    return JSON.parse(value);
  } catch {
    return {};
  }
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
