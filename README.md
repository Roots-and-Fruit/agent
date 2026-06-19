# Roots & Fruit — Cursor agent

Cursor project for operating [rootsandfruit.com](https://rootsandfruit.com) via MCP. Pair with the sibling **`abilities/`** WordPress plugin repo.

**Start here:** [`AGENTS.md`](AGENTS.md) · **MCP routing:** [`agent_docs/mcp-routing.md`](agent_docs/mcp-routing.md)

---

## Workspace layout

Clone into a shared parent folder:

```
rootsandfruit-as-client/
├── agent/          ← this repo
└── abilities/      ← git clone https://github.com/Roots-and-Fruit/abilities.git
```

Open **`rootsandfruit.code-workspace`** in Cursor for both folders (expects `../abilities` sibling). If you use the parent folder layout, open **`../rootsandfruit.code-workspace`** instead.

---

## Setup

1. **Clone abilities** (sibling folder):

   ```powershell
   cd ..
   git clone https://github.com/Roots-and-Fruit/abilities.git abilities
   ```

2. **Sibling parent folder:** If you open `rootsandfruit-as-client/` (parent of `agent/` + `abilities/`), sync workspace-root to the parent:

   ```powershell
   .\tools\scripts\sync-workspace-root.ps1
   ```

   Generates `00-rf-boot.mdc` from `AGENT-BOOT.md` and copies hooks, rules, skills, and `mcp.json` to the parent. Stack map: [`agent_docs/cursor-context-stack.md`](agent_docs/cursor-context-stack.md).

3. **Configure credentials:**

   ```powershell
   copy .env.example .env
   # Edit .env — ROOTSANDFRUIT_MCP_URL, USERNAME, PASSWORD (Application Password)
   ```

3. **Reload MCP** in Cursor (Settings → MCP → wordpress-rootsandfruit).

4. **Verify:**

   ```powershell
   .\tools\scripts\test-wordpress-mcp-http.ps1 -ExpectRfAbilities -ExpectBlocks
   .\tools\scripts\audit-mcp-abilities.ps1 -ExpectBlocks
   ```

---

## Commands

Run from **`agent/`** root in PowerShell:

| Command | Purpose |
|---------|---------|
| `.\tools\scripts\test-wordpress-mcp-http.ps1 -ExpectRfAbilities -ExpectBlocks` | MCP transport + R&F + block abilities |
| `.\tools\scripts\audit-mcp-abilities.ps1 -ExpectBlocks` | MCP discover vs REST catalog |
| `php -l ..\abilities\rootsandfruit-abilities.php` | PHP syntax (from workspace; plugin in sibling repo) |

Plugin releases: see `../abilities/GITHUB.md`.

WordPress server plugins (not in this repo): [`docs/wordpress-plugins.md`](docs/wordpress-plugins.md).

---

## Publish to GitHub

This folder is the **`Roots-and-Fruit/agent`** repo (or your chosen name). The **`abilities/`** sibling stays in its own repo — do not merge plugin source into `agent/`.

```powershell
git init
git add .
git commit -m "Initial agent workspace for Roots & Fruit Cursor MCP ops."
git remote add origin https://github.com/Roots-and-Fruit/agent.git
git push -u origin main
```

---