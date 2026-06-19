import path from "node:path";
import process from "node:process";

const input = JSON.parse(await readStdin());
const filePath = normalizePath(String(input.file_path ?? ""));

const isAbilitiesPhp =
  filePath.includes(`${path.sep}abilities${path.sep}`) && filePath.endsWith(".php");

if (!isAbilitiesPhp) {
  process.stdout.write("{}");
  process.exit(0);
}

const rel = filePath.includes(`${path.sep}abilities${path.sep}`)
  ? filePath.split(`${path.sep}abilities${path.sep}`).pop()
  : path.basename(filePath);

process.stdout.write(
  JSON.stringify({
    additional_context: [
      "R&F plugin file edited:",
      `abilities/${rel}`,
      "Legwork: run `php -l` on touched PHP from agent/ (`php -l ..\\abilities\\...`).",
      "If ability registration or MCP surface changed: run test-wordpress-mcp-http.ps1 and audit-mcp-abilities.ps1.",
      "Release: abilities/GITHUB.md (tag + zip — git push alone does not update prod).",
    ].join("\n"),
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
