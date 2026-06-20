# One-time Google Search Console ADC setup for Windows PowerShell.
# Usage: .\tools\scripts\setup-searchconsole-adc.ps1 -ProjectId ecstatic-motif-486422-f4

param(
    [Parameter(Mandatory = $true)]
    [string] $ProjectId
)

$ErrorActionPreference = 'Stop'
$scopes = 'https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform'

Write-Host "Setting gcloud project to $ProjectId ..."
gcloud config set project $ProjectId

Write-Host "Enabling Search Console API ..."
gcloud services enable searchconsole.googleapis.com --project=$ProjectId

Write-Host "Opening browser for Google login (read-only Search Console + required cloud-platform scope) ..."
gcloud auth application-default login --scopes=$scopes

Write-Host "Setting quota project ..."
gcloud auth application-default set-quota-project $ProjectId

Write-Host ""
Write-Host "Done. Run: .\tools\scripts\test-analytics-mcp-env.ps1"
Write-Host "Then reload Cursor and enable the searchconsole MCP server."
