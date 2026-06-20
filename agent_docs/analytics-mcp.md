# Analytics MCP — Plausible + Search Console

Read-only analytics in Cursor alongside WordPress and DataForSEO MCP.

## Servers

| Server | Launcher | Credentials |
|--------|----------|-------------|
| `plausible` | `tools/scripts/run-plausible-mcp.mjs` | `PLAUSIBLE_API_KEY` in `agent/.env` |
| `searchconsole` | `tools/scripts/run-searchconsole-mcp.mjs` | Google ADC on this machine (`gcloud auth application-default login`) |

Config: workspace `.cursor/mcp.json` (sync from `agent/workspace-root/.cursor/mcp.json`).

Preflight: `.\tools\scripts\test-analytics-mcp-env.ps1`

## When to use which

| MCP | Use for |
|-----|---------|
| **dataforseo** | Pre-publish keyword research, SERP corpus (`/rf-keyword-research`) |
| **plausible** | Traffic, referrers, goals, real-time visitors after publish |
| **searchconsole** | Queries, impressions, CTR, indexing, URL inspection |

## Plausible

- API key: [plausible.io/settings](https://plausible.io/settings)
- Default site domain: `rootsandfruit.com` (`PLAUSIBLE_SITE_ID` in `.env` — agent hint, not read by the npm package)
- Self-hosted: set `PLAUSIBLE_BASE_URL`

Typical tools: `list-sites`, `get-aggregate-stats`, `get-timeseries`, `get-breakdown`, `get-current-visitors`, `query`.

## Search Console

One-time on this PC (PowerShell — **quote the scopes** so the comma is not split):

```powershell
gcloud config set project YOUR_GCP_PROJECT_ID
gcloud services enable searchconsole.googleapis.com --project=YOUR_GCP_PROJECT_ID
gcloud auth application-default login --scopes="https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform"
gcloud auth application-default set-quota-project YOUR_GCP_PROJECT_ID
```

Or run: `.\tools\scripts\setup-searchconsole-adc.ps1 -ProjectId YOUR_GCP_PROJECT_ID`

Your Google account must have access to the property in [Search Console](https://search.google.com/search-console).

Default property URL: `https://rootsandfruit.com/` (`GSC_SITE_URL` in `.env`).

Typical tools: `gsc_list_sites`, `gsc_search_analytics`, `gsc_inspect_url`, `gsc_list_sitemaps`.

Optional: `GSC_OUTPUT_FORMAT=toon` in `.env` for smaller tabular responses.

## Boundaries

- Read-only — no writes to Plausible or Google from these MCP servers.
- Secrets stay in `agent/.env` (Plausible only). Never commit `.env`.
- GSC auth is machine-local; not shared via the WordPress content-agent user.
