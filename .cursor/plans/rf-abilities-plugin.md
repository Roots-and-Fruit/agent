# R&F Abilities Plugin — Living Status

**Implementation reference:** Cursor plan `r&f_abilities_plugin_af171379.plan.md` (do not edit that file).

**Plugin source:** `../abilities/` (sibling repo)

## Plan status

| Phase | Name | Status | Date |
|-------|------|--------|------|
| 0 | Scaffold + plan artifact | PASS | 2026-06-19 |
| 1 | Core framework + site/ping | PASS (repo gates) | 2026-06-19 |
| 2 | Preview module | PASS (repo gates) | 2026-06-19 |
| 3 | Content module | PASS (repo gates) | 2026-06-19 |
| 4 | Audit + client tooling | PASS (repo gates) | 2026-06-19 |
| 5 | Local manual testing | IN PROGRESS | 2026-06-19 |
| 6 | Live deploy + confirmation | AWAITING DEPLOY | |

**Overall:** IN PROGRESS — local MCP gates pass after ability-name fix; PPP plugin needed for preview E2E

---

## Global rules

- No made-to-pass tests; evidence required per gate.
- Two-strike failure protocol: one fix attempt, then BLOCKED + user handoff.

---

## Phase handoffs

### Phase 0 handoff
- **Status:** PASS
- **Summary:** Created plugin skeleton, readme, tools/wordpress/README.md, living status doc.
- **Evidence:** `php -l` all PHP files exit 0; plan file exists.
- **Next phase:** 1 — entry criteria met.

### Phase 1 handoff
- **Status:** PASS (repo); gates 1.3–1.7 require local WP deploy
- **Summary:** Registry, Definition builder, Permissions, Schemas, Annotations, Errors, Health module with `rootsandfruit/ping`.
- **Evidence:** `php -l` exit 0; `bin/validate-definition-builder.php` exit 0 (wrong prefix + empty description throw; valid build passes).
- **Next phase:** 2 — entry criteria met.

### Phase 2 handoff
- **Status:** PASS (repo)
- **Summary:** Preview module (`enable-public-preview`, `get-public-preview-url`); mu-plugin marked deprecated.
- **Evidence:** Code review + PHP syntax; PPP integration via `DS_Public_Post_Preview`.
- **Next phase:** 3 — entry criteria met.

### Phase 3 handoff
- **Status:** PASS (repo)
- **Summary:** Content module — list, get, create-draft, update-post, publish-post (separate ability).
- **Evidence:** PHP syntax; no delete abilities registered.
- **Next phase:** 4 — entry criteria met.

### Phase 4 handoff
- **Status:** PASS (repo)
- **Summary:** `audit-mcp-abilities.ps1`; smoke test `-ExpectRfAbilities`; deprecated enable script.
- **Evidence:** Base smoke test exit 0 against production (MCP transport OK); audit exit 1 as expected pre-deploy (no rootsandfruit/* yet).
- **Next phase:** 5 — requires plugin deploy to local/staging WP.

---

### Phase 5 handoff (2026-06-19, rfaiblueprint.wp.local)
- **Status:** PARTIAL PASS — automated gates OK; preview E2E blocked on local
- **Root cause fixed:** WordPress allows only `namespace/name` (one slash). Old names like `rootsandfruit/site/ping` silently failed registration. Renamed to `rootsandfruit/ping`, etc. Builder now validates the pattern.
- **Evidence:**
  - `test-wordpress-mcp-http.ps1 -ExpectRfAbilities` — exit 0 (8 abilities, ping 1.0.0)
  - `audit-mcp-abilities.ps1` with local URL — exit 0 (8 in MCP discover, get-ability-info OK)
  - E2E `rootsandfruit/create-draft` — post ID 7 created
  - `rootsandfruit/enable-public-preview` — fails: Public Post Preview plugin not active on local
- **Deploy note:** Synced fix to `C:\Users\reach\Studio\wpcoreai\wp-content\plugins\rootsandfruit-abilities`
- **Remaining checklist:** Abilities Explorer UI confirm, install/activate PPP for preview E2E, incognito preview, publish path, negative control

---

## Phase 5 — Your checklist (local/staging)

Deploy `../abilities/` to `wp-content/plugins/rootsandfruit-abilities/` and point `agent/.env` at local/staging.

1. [x] Activate plugin — no fatals (categories + 8 MCP abilities register)
2. [ ] Abilities Explorer — 8 `rootsandfruit/*` abilities visible
3. [x] `audit-mcp-abilities.ps1` against local URL — exit 0
4. [x] `test-wordpress-mcp-http.ps1 -ExpectRfAbilities` against local — exit 0
5. [ ] Cursor MCP reload — discover lists all 8
6. [ ] E2E: create draft → enable public preview → incognito URL works (**needs Public Post Preview plugin on local**)
7. [ ] Publish test draft; verify front-end; trash manually
8. [ ] Negative: agent cannot execute `ws-form/form-delete` via MCP

**Sign-off:** Reply “local/staging OK for live deploy” to proceed to Phase 6.

---

## Phase 6 — Live deploy (after Phase 5 sign-off)

1. Deploy plugin to production `wp-content/plugins/rootsandfruit-abilities/`
2. Activate; do not deploy deprecated mu-plugin
3. Run audit + smoke with `-ExpectRfAbilities` against production `.env`
4. Live E2E test draft + public preview; trash in admin
5. Confirm regression: non-RF MCP abilities count ≥ 7

**Sign-off:** Reply “live OK” to mark plan COMPLETE.

---

## Pre-deploy verification evidence (2026-06-19)

```
php -l: all plugin PHP files — OK
validate-definition-builder.php — exit 0
test-wordpress-mcp-http.ps1 — exit 0 (transport + 7 third-party MCP abilities)
audit-mcp-abilities.ps1 — exit 1 (expected: no rootsandfruit/* until deploy)
```
