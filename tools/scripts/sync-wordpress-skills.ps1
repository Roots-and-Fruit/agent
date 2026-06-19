# Sync WordPress/agent-skills into scoped .cursor/skills/ folders
# Run from agent/ after: npx skills add WordPress/agent-skills --skill ...

$ErrorActionPreference = "Stop"
$agentRoot = Split-Path -Parent $PSScriptRoot
$workspaceRoot = Split-Path -Parent $agentRoot
$staging = Join-Path $workspaceRoot ".agents\skills"

if (-not (Test-Path $staging)) {
    Write-Error "Missing $staging — run npx skills add WordPress/agent-skills first (from workspace root)."
}

$abilitySkills = @(
    "wp-abilities-api",
    "wp-abilities-verify",
    "wp-abilities-audit",
    "wp-plugin-development"
)

foreach ($name in $abilitySkills) {
    $src = Join-Path $staging $name
    $dest = Join-Path $workspaceRoot "abilities\.cursor\skills\$name"
    if (-not (Test-Path $src)) { Write-Warning "Skip missing skill: $name"; continue }
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Copy-Item -Path "$src\*" -Destination $dest -Recurse -Force
    Write-Host "Synced $name -> abilities/.cursor/skills/"
}

$restSrc = Join-Path $staging "wp-rest-api"
$restDest = Join-Path $agentRoot ".cursor\skills\wp-rest-api"
if (Test-Path $restSrc) {
    New-Item -ItemType Directory -Force -Path $restDest | Out-Null
    Copy-Item -Path "$restSrc\*" -Destination $restDest -Recurse -Force
    Write-Host "Synced wp-rest-api -> agent/.cursor/skills/"
}

Write-Host "Done. Remove staging with: Remove-Item -Recurse -Force '$staging' parent .agents if desired."
