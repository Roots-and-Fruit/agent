# Deploy AI crawler robots.txt FluentSnippet via MCP (requires admin Application Password).
# Usage (from agent/):
#   $env:ROOTSANDFRUIT_MCP_USERNAME = 'admin-user'
#   $env:ROOTSANDFRUIT_MCP_PASSWORD = 'xxxx xxxx xxxx'
#   .\tools\scripts\deploy-robots-ai-crawlers-snippet.ps1
#
# Or paste templates/fluent-snippet-robots-ai-crawlers.php into FluentSnippets wp-admin.

param(
    [switch]$ActivateOnly,
    [string] $FileName
)

$ErrorActionPreference = 'Stop'
$agentRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$templateFile = Join-Path $agentRoot 'templates\fluent-snippet-robots-ai-crawlers.php'

function Invoke-RfAbility {
    param([string] $Ability, [hashtable] $Params)
    $json = $Params | ConvertTo-Json -Depth 20 -Compress
    & (Join-Path $PSScriptRoot 'invoke-mcp-ability.ps1') -AbilityName $Ability -ParametersJson $json
}

function Get-SnippetCodeFromTemplate {
    $raw = [System.IO.File]::ReadAllText($templateFile, [System.Text.Encoding]::UTF8)
  $raw = $raw -replace '^\s*<\?php\s*', ''
  $idx = $raw.IndexOf('add_action(')
    if ($idx -lt 0) { throw "Template missing add_action block: $templateFile" }
    return $raw.Substring($idx).TrimEnd()
}

if ($ActivateOnly) {
    if (-not $FileName) { Write-Error 'Pass -FileName for -ActivateOnly' }
    Write-Host (Invoke-RfAbility 'rootsandfruit/snippets-activate' @{ file_name = $FileName })
    exit 0
}

$code = Get-SnippetCodeFromTemplate
Write-Host 'Creating draft snippet...'
$createOut = Invoke-RfAbility 'rootsandfruit/snippets-create' @{
    name        = 'RF robots.txt AI crawler rules'
    description = 'Append explicit allow/disallow rules for named AI crawlers (training blocked, retrieval allowed).'
    tags        = 'rf-ability, robots, agent-readiness'
    group       = 'Roots & Fruit — site'
    code        = $code
}
Write-Host $createOut

if ($createOut -match 'Permission denied') {
    Write-Host ''
    Write-Host 'Content-agent MCP user cannot manage snippets.'
    Write-Host 'Either set admin ROOTSANDFRUIT_MCP_* in .env temporarily, or paste:'
    Write-Host "  $templateFile"
    Write-Host 'into FluentSnippets wp-admin (PHP, run everywhere, tag rf-ability).'
    exit 1
}

$fileName = $null
if ($createOut -match '"file_name"\s*:\s*"([^"]+)"') { $fileName = $Matches[1] }
if (-not $fileName) { Write-Error 'Could not parse file_name from create response.' }

Write-Host "Activating $fileName ..."
Write-Host (Invoke-RfAbility 'rootsandfruit/snippets-activate' @{ file_name = $fileName })

Write-Host 'Verifying snippet runtime...'
Write-Host (Invoke-RfAbility 'rootsandfruit/snippets-verify' @{ file_name = $fileName })

Write-Host ''
Write-Host 'Fetch robots.txt to confirm AI rules:'
Write-Host '  curl.exe -sL https://rootsandfruit.com/robots.txt'
