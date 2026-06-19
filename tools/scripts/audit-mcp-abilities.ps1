# Compare MCP discover, REST abilities list, and rootsandfruit/* cross-checks.
# Usage:
#   .\tools\scripts\audit-mcp-abilities.ps1
#   .\tools\scripts\audit-mcp-abilities.ps1 -ExpectBlocks
#
# Loads ROOTSANDFRUIT_MCP_* from agent/.env.

param(
    [switch] $ExpectBlocks,
    [string] $EnvFile
)

$agentRoot = if ($PSScriptRoot) {
    Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
} else {
    (Get-Location).Path
}

if (-not $EnvFile) {
    $EnvFile = Join-Path $agentRoot '.env'
}

function Import-DotEnv {
    param([string] $Path)
    if (-not (Test-Path $Path)) { return }
    Get-Content $Path | ForEach-Object {
        if ($_ -match '^\s*([^#=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"').Trim("'")
            Set-Item -Path "Env:$name" -Value $value
        }
    }
}

Import-DotEnv -Path $EnvFile

$url = $env:ROOTSANDFRUIT_MCP_URL
$username = $env:ROOTSANDFRUIT_MCP_USERNAME
$password = $env:ROOTSANDFRUIT_MCP_PASSWORD
$siteRoot = ($url -replace '/wp-json/.*$', '')

if (-not $url -or -not $username -or -not $password) {
    Write-Error "Missing ROOTSANDFRUIT_MCP_* in $EnvFile"
    exit 1
}

$pair = "${username}:${password}"
$b64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
$headers = @{
    Authorization = "Basic $b64"
    Accept        = 'application/json'
}

function Invoke-Mcp {
    param([string] $JsonBody, [string] $SessionId, [string] $McpUrl)
    $h = $headers.Clone()
    if ($SessionId) { $h['Mcp-Session-Id'] = $SessionId }
    return Invoke-WebRequest -Uri $McpUrl -Method Post -Headers $h `
        -ContentType 'application/json; charset=utf-8' `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($JsonBody)) -UseBasicParsing
}

Write-Host "=== MCP initialize ===" -ForegroundColor Cyan
$initBody = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"audit-mcp-abilities","version":"1.0.0"}}}'
$r1 = Invoke-Mcp -JsonBody $initBody -SessionId $null -McpUrl $url
$sessionId = $r1.Headers['Mcp-Session-Id']
if (-not $sessionId) {
    Write-Host "FAIL: no Mcp-Session-Id" -ForegroundColor Red
    exit 1
}

Write-Host "=== MCP discover-abilities ===" -ForegroundColor Cyan
$discBody = '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"mcp-adapter-discover-abilities","arguments":{}}}'
$r2 = Invoke-Mcp -JsonBody $discBody -SessionId $sessionId -McpUrl $url
$discJson = ($r2.Content | ConvertFrom-Json)
$mcpAbilities = @(($discJson.result.content[0].text | ConvertFrom-Json).abilities | ForEach-Object { $_.name })
$mcpSet = [System.Collections.Generic.HashSet[string]]::new([string[]]$mcpAbilities)

Write-Host "MCP discover count: $($mcpAbilities.Count)"

Write-Host "`n=== REST abilities list ===" -ForegroundColor Cyan
$restNames = @()
try {
    $rest = Invoke-RestMethod -Uri "$siteRoot/wp-json/wp-abilities/v1/abilities?per_page=100" -Headers $headers
    $restNames = @($rest | ForEach-Object { $_.name })
    Write-Host "REST list count: $($restNames.Count)"
} catch {
    Write-Host "REST list failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

$restSet = [System.Collections.Generic.HashSet[string]]::new([string[]]$restNames)

Write-Host "`n=== Catalog comparison note ===" -ForegroundColor Cyan
Write-Host "Abilities Explorer (admin UI) shows ALL registered abilities."
Write-Host "MCP discover shows only meta.mcp.public=true abilities for the authenticated user context."
Write-Host "REST list shows only meta.show_in_rest=true abilities."
Write-Host "Count mismatches between the three are expected unless every ability opts into all flags."

Write-Host "`n=== rootsandfruit/* in MCP discover ===" -ForegroundColor Cyan
$rfMcp = @($mcpAbilities | Where-Object { $_ -like 'rootsandfruit/*' })
if ($rfMcp.Count -eq 0) {
    Write-Host "FAIL: no rootsandfruit/* abilities in MCP discover. Deploy and activate rootsandfruit-abilities plugin." -ForegroundColor Red
    exit 1
}
$rfMcp | ForEach-Object { Write-Host "  $_" }

if ($ExpectBlocks) {
    Write-Host "`n=== Block MCP abilities gate ===" -ForegroundColor Cyan
    $requiredBlocks = @(
        'rootsandfruit/blocks-get-page',
        'rootsandfruit/blocks-update',
        'rootsandfruit/blocks-mutate',
        'rootsandfruit/blocks-insert',
        'rootsandfruit/blocks-create-page',
        'rootsandfruit/blocks-list-patterns'
    )
    $blockFailed = $false
    foreach ($name in $requiredBlocks) {
        if ($mcpSet.Contains($name)) {
            Write-Host "OK   $name"
        } else {
            Write-Host "FAIL $name missing (gk-block-mcp inactive?)" -ForegroundColor Red
            $blockFailed = $true
        }
    }
    if ($blockFailed) { exit 1 }
}

Write-Host "`n=== get-ability-info cross-check ===" -ForegroundColor Cyan
$infoFailed = $false
foreach ($name in $rfMcp) {
    $argsJson = (@{ ability_name = $name } | ConvertTo-Json -Compress)
    $body = '{"jsonrpc":"2.0","id":10,"method":"tools/call","params":{"name":"mcp-adapter-get-ability-info","arguments":' + $argsJson + '}}'
    $r = Invoke-Mcp -JsonBody $body -SessionId $sessionId -McpUrl $url
    $j = $r.Content | ConvertFrom-Json
    $txt = $j.result.content[0].text
    if ($txt -match 'not exposed via MCP') {
        Write-Host "FAIL info: $name => $txt" -ForegroundColor Red
        $infoFailed = $true
    } else {
        Write-Host "OK   info: $name"
    }
}

Write-Host "`n=== Summary table (union of MCP + REST names) ===" -ForegroundColor Cyan
$union = [System.Collections.Generic.HashSet[string]]::new()
foreach ($n in $mcpAbilities) { [void]$union.Add($n) }
foreach ($n in $restNames) { [void]$union.Add($n) }

$rows = foreach ($n in ($union | Sort-Object)) {
    $prefix = if ($n -match '^([^/]+)/') { $matches[1] } else { '?' }
    [PSCustomObject]@{
        name             = $n
        in_mcp_discover  = $mcpSet.Contains($n)
        in_rest_list     = $restSet.Contains($n)
        provider_prefix  = $prefix
    }
}
$rows | Format-Table -AutoSize

if ($infoFailed) { exit 1 }

Write-Host "Audit passed." -ForegroundColor Green
exit 0
