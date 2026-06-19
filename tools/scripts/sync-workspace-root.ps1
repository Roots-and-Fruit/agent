# Sync workspace-root template to parent .cursor/ and generate boot rule from AGENT-BOOT.md
# Run from agent/: .\tools\scripts\sync-workspace-root.ps1

param(
    [switch]$AgentOnly
)

$ErrorActionPreference = "Stop"
$agentRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$workspaceRoot = Split-Path -Parent $agentRoot
$templateRoot = Join-Path $agentRoot "workspace-root"
$bootSource = Join-Path $agentRoot "AGENT-BOOT.md"
$ruleTemplate = Join-Path $templateRoot ".cursor\rules\00-rf-boot.mdc"

if (-not (Test-Path $bootSource)) {
    Write-Error "Missing boot source: $bootSource"
}

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$bootBody = [System.IO.File]::ReadAllText($bootSource, $utf8NoBom).TrimEnd()
$ruleContent = @"
---
description: Roots & Fruit workspace boot - layout, MCP-first ops, verification gates
alwaysApply: true
---

$bootBody
"@

New-Item -ItemType Directory -Force -Path (Split-Path $ruleTemplate) | Out-Null
[System.IO.File]::WriteAllText($ruleTemplate, $ruleContent, $utf8NoBom)
Write-Host "Generated $ruleTemplate from AGENT-BOOT.md"

function Sync-Tree {
    param([string]$Src, [string]$Dest, [string]$Label)
    if (-not (Test-Path $Src)) {
        Write-Warning "Skip missing: $Src"
        return
    }
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    Copy-Item -Path "$Src\*" -Destination $Dest -Recurse -Force
    Write-Host "Synced $Label -> $Dest"
}

if ($AgentOnly) {
    Sync-Tree (Join-Path $templateRoot ".cursor\rules") (Join-Path $agentRoot ".cursor\rules") "boot rule"
    Sync-Tree (Join-Path $templateRoot ".cursor\hooks") (Join-Path $agentRoot ".cursor\hooks") "hooks"
    Copy-Item (Join-Path $templateRoot ".cursor\hooks.json") (Join-Path $agentRoot ".cursor\hooks.json") -Force
    Write-Host "Agent-only sync done."
    exit 0
}

Copy-Item (Join-Path $templateRoot "AGENTS.md") (Join-Path $workspaceRoot "AGENTS.md") -Force
Write-Host "Synced AGENTS.md -> workspace root"

Sync-Tree (Join-Path $templateRoot ".cursor\hooks") (Join-Path $workspaceRoot ".cursor\hooks") "hooks"
Sync-Tree (Join-Path $templateRoot ".cursor\rules") (Join-Path $workspaceRoot ".cursor\rules") "boot rule"
Sync-Tree (Join-Path $templateRoot ".cursor\skills") (Join-Path $workspaceRoot ".cursor\skills") "skills"

foreach ($file in @("hooks.json", "mcp.json")) {
    $src = Join-Path $templateRoot ".cursor\$file"
    if (Test-Path $src) {
        Copy-Item $src (Join-Path $workspaceRoot ".cursor\$file") -Force
        Write-Host "Synced .cursor\$file"
    }
}

foreach ($file in @(".cursorignore", ".cursorindexingignore")) {
    $src = Join-Path $templateRoot $file
    if (Test-Path $src) {
        Copy-Item $src (Join-Path $workspaceRoot $file) -Force
        Write-Host "Synced $file"
    }
}

# Keep agent/.cursor/hooks aligned with template (no duplicate always-on rule in agent/)
Sync-Tree (Join-Path $templateRoot ".cursor\hooks") (Join-Path $agentRoot ".cursor\hooks") "hooks to agent"
Copy-Item (Join-Path $templateRoot ".cursor\hooks.json") (Join-Path $agentRoot ".cursor\hooks.json") -Force

$agentRule = Join-Path $agentRoot ".cursor\rules\00-rf-boot.mdc"
if (Test-Path $agentRule) {
    Remove-Item $agentRule -Force
    Write-Host "Removed duplicate agent/.cursor/rules/00-rf-boot.mdc (use workspace root or -AgentOnly)"
}

Write-Host "Done. Reload Cursor window to pick up hooks/rules/MCP changes."
