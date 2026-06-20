# Verify parent and agent mcp.json match workspace-root template (path-adjusted).
# Run from agent/: .\tools\scripts\test-mcp-config.ps1

$ErrorActionPreference = 'Stop'
$agentRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$workspaceRoot = Split-Path -Parent $agentRoot
$templatePath = Join-Path $agentRoot 'workspace-root\.cursor\mcp.json'
$parentPath = Join-Path $workspaceRoot '.cursor\mcp.json'
$agentPath = Join-Path $agentRoot '.cursor\mcp.json'

function Read-Json([string] $Path) {
    if (-not (Test-Path $Path)) {
        return $null
    }
    return Get-Content $Path -Raw -Encoding UTF8 | ConvertFrom-Json
}

function Get-ServerNames($mcp) {
    if (-not $mcp -or -not $mcp.mcpServers) {
        return @()
    }
    $mcp.mcpServers.PSObject.Properties.Name | Sort-Object
}

$template = Read-Json $templatePath
$parent = Read-Json $parentPath
$agent = Read-Json $agentPath
$fail = 0

if (-not $template) {
    Write-Host "FAIL  Missing template: $templatePath"
    exit 1
}

$expectedAgentJson = (Get-Content $templatePath -Raw -Encoding UTF8).Replace(
    '${workspaceFolder}/agent/tools/scripts/',
    '${workspaceFolder}/tools/scripts/'
)

function Normalize([string] $Json) {
  return ($Json -replace "`r`n", "`n").Trim()
}

$templateRaw = Normalize (Get-Content $templatePath -Raw -Encoding UTF8)
$parentRaw = if (Test-Path $parentPath) { Normalize (Get-Content $parentPath -Raw -Encoding UTF8) } else { '' }
$agentRaw = if (Test-Path $agentPath) { Normalize (Get-Content $agentPath -Raw -Encoding UTF8) } else { '' }
$expectedAgentRaw = Normalize $expectedAgentJson

Write-Host "MCP config parity"
Write-Host "  Template: $templatePath"
Write-Host "  Parent:   $parentPath"
Write-Host "  Agent:    $agentPath"
Write-Host ""

if ($parentRaw -eq $templateRaw) {
    Write-Host 'OK    Parent mcp.json matches template'
} else {
    Write-Host 'FAIL  Parent mcp.json differs from template — run sync-workspace-root.ps1'
    $fail++
}

if ($agentRaw -eq $expectedAgentRaw) {
    Write-Host 'OK    agent/.cursor/mcp.json matches template (path-adjusted)'
} else {
    Write-Host 'FAIL  agent/.cursor/mcp.json differs from template — run sync-workspace-root.ps1'
    $fail++
}

$templateNames = Get-ServerNames $template
$parentNames = Get-ServerNames $parent
$agentNames = Get-ServerNames $agent

Write-Host ''
Write-Host "Servers in template: $($templateNames -join ', ')"
Write-Host "Servers in parent:   $($parentNames -join ', ')"
Write-Host "Servers in agent:    $($agentNames -join ', ')"

$missingParent = $templateNames | Where-Object { $_ -notin $parentNames }
$missingAgent = $templateNames | Where-Object { $_ -notin $agentNames }

if ($missingParent) {
    Write-Host "FAIL  Parent missing: $($missingParent -join ', ')"
    $fail++
}
if ($missingAgent) {
    Write-Host "FAIL  Agent missing: $($missingAgent -join ', ')"
    $fail++
}

Write-Host ''
if ($fail -gt 0) {
    Write-Host "$fail check(s) failed. Edit workspace-root/.cursor/mcp.json then sync."
    exit 1
}

Write-Host 'All MCP config checks passed. Reload Cursor after sync.'
