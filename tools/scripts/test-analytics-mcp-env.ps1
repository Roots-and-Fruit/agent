# Preflight for Plausible + Search Console MCP launchers (reads agent/.env only).
# Run from agent/: .\tools\scripts\test-analytics-mcp-env.ps1

param([string] $EnvFile)

$ErrorActionPreference = 'Stop'
$agentRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (-not $EnvFile) { $EnvFile = Join-Path $agentRoot '.env' }

$fail = 0

function Test-EnvVar {
    param([string] $Name, [hashtable] $Vars)
    if ($Vars.ContainsKey($Name) -and $Vars[$Name].Trim()) {
        Write-Host "OK  $Name is set"
    } else {
        Write-Host "FAIL  $Name is missing in $EnvFile"
        $script:fail++
    }
}

$vars = @{}
if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -match '^\s*([^#=]+)=(.*)$') {
            $vars[$matches[1].Trim()] = $matches[2].Trim().Trim('"').Trim("'")
        }
    }
} else {
    Write-Host "FAIL  Missing $EnvFile (copy from .env.example)"
    exit 1
}

Write-Host "Plausible MCP"
Test-EnvVar 'PLAUSIBLE_API_KEY' $vars
if ($vars['PLAUSIBLE_SITE_ID']) {
    Write-Host "OK  PLAUSIBLE_SITE_ID=$($vars['PLAUSIBLE_SITE_ID'])"
} else {
    Write-Host "WARN PLAUSIBLE_SITE_ID not set (agents should pass rootsandfruit.com per query)"
}

Write-Host ""
Write-Host "Search Console MCP"
$adc = Join-Path $env:APPDATA 'gcloud\application_default_credentials.json'
if (Test-Path $adc) {
    Write-Host "OK  Google ADC file exists"
} else {
    Write-Host "FAIL  Google ADC not found at $adc"
    Write-Host "      Run: .\tools\scripts\setup-searchconsole-adc.ps1 -ProjectId YOUR_GCP_PROJECT_ID"
    $fail++
}

if ($vars['GSC_SITE_URL']) {
    Write-Host "OK  GSC_SITE_URL=$($vars['GSC_SITE_URL'])"
} else {
    Write-Host "WARN GSC_SITE_URL not set (use https://rootsandfruit.com/ in tool calls)"
}

Write-Host ""
if ($fail -gt 0) {
    Write-Host "Fix $fail issue(s), reload Cursor MCP, then test in chat."
    exit 1
}

Write-Host "Preflight passed. Reload Cursor and enable plausible + searchconsole MCP servers."
