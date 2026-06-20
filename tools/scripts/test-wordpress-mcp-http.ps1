# Smoke-test WordPress MCP Adapter HTTP transport and REST auth.
# Usage:
#   .\tools\scripts\test-wordpress-mcp-http.ps1
#   .\tools\scripts\test-wordpress-mcp-http.ps1 -ExpectRfAbilities -ExpectBlocks
#
# Loads ROOTSANDFRUIT_MCP_* from agent/.env when not passed as parameters.

param(
    [string] $Url,
    [string] $Username,
    [string] $ApplicationPassword,
    [switch] $ExpectRfAbilities,
    [switch] $ExpectBlocks,
    [switch] $RequirePreview,
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

if (-not $Url) { $Url = $env:ROOTSANDFRUIT_MCP_URL }
if (-not $Username) { $Username = $env:ROOTSANDFRUIT_MCP_USERNAME }
if (-not $ApplicationPassword) { $ApplicationPassword = $env:ROOTSANDFRUIT_MCP_PASSWORD }

if (-not $Url -or -not $Username -or -not $ApplicationPassword) {
    Write-Error "Set -Url, -Username, -ApplicationPassword or ROOTSANDFRUIT_MCP_* in $EnvFile."
    exit 1
}

$siteRoot = ($Url -replace '/wp-json/.*$', '')
$failed = $false
$pair = "${Username}:${ApplicationPassword}"
$b64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
$headers = @{
    Authorization = "Basic $b64"
    Accept        = "application/json"
}

function Send-Mcp {
    param(
        [string] $JsonBody,
        [hashtable] $ExtraHeaders = @{}
    )
    $h = $headers.Clone()
    foreach ($k in $ExtraHeaders.Keys) { $h[$k] = $ExtraHeaders[$k] }
    return Invoke-WebRequest -Uri $Url -Method Post -Headers $h `
        -ContentType 'application/json; charset=utf-8' `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($JsonBody)) `
        -UseBasicParsing
}

Write-Host "=== REST: /wp/v2/users/me ===" -ForegroundColor Cyan
try {
    $me = Invoke-RestMethod -Uri "$siteRoot/wp-json/wp/v2/users/me?context=edit" -Headers $headers -Method Get
    Write-Host "OK  id=$($me.id)  name=$($me.name)  roles=$($me.roles -join ', ')"
} catch {
    Write-Host "FAIL  $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) { Write-Host $_.ErrorDetails.Message }
    $failed = $true
}

Write-Host "`n=== MCP: initialize ===" -ForegroundColor Cyan
$initBody = @'
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"rootsandfruit-smoke-test","version":"1.0.0"}}}
'@

try {
    $r1 = Send-Mcp -JsonBody $initBody
} catch {
    Write-Host "FAIL  $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = [IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
        Write-Host $reader.ReadToEnd()
    }
    exit 1
}

$sessionId = $r1.Headers['Mcp-Session-Id']
if (-not $sessionId) {
    Write-Host "FAIL  No Mcp-Session-Id header on initialize response." -ForegroundColor Red
    Write-Host $r1.Content
    exit 1
}

Write-Host "OK  session=$sessionId"

Write-Host "`n=== MCP: tools/list ===" -ForegroundColor Cyan
$listBody = '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
try {
    $r2 = Send-Mcp -JsonBody $listBody -ExtraHeaders @{ 'Mcp-Session-Id' = $sessionId }
    Write-Host "OK  status=$($r2.StatusCode)"
    $list = $r2.Content | ConvertFrom-Json
    $tools = @($list.result.tools)
    Write-Host "Tools ($($tools.Count)):"
    foreach ($tool in $tools) {
        Write-Host "  - $($tool.name)"
    }
} catch {
    Write-Host "FAIL  $($_.Exception.Message)" -ForegroundColor Red
    $failed = $true
}

Write-Host "`n=== MCP: discover-abilities ===" -ForegroundColor Cyan
$discBody = '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"mcp-adapter-discover-abilities","arguments":{}}}'
$mcpAbilityNames = @()
try {
    $r3 = Send-Mcp -JsonBody $discBody -ExtraHeaders @{ 'Mcp-Session-Id' = $sessionId }
    $disc = $r3.Content | ConvertFrom-Json
    $text = $disc.result.content[0].text
    $abilities = ($text | ConvertFrom-Json).abilities
    $mcpAbilityNames = @($abilities | ForEach-Object { $_.name })
    Write-Host "OK  abilities=$($mcpAbilityNames.Count)"
    foreach ($ability in $abilities) {
        Write-Host "  - $($ability.name)"
    }
} catch {
    Write-Host "FAIL  $($_.Exception.Message)" -ForegroundColor Red
    $failed = $true
}

if ($ExpectRfAbilities) {
    Write-Host "`n=== R&F abilities gate ===" -ForegroundColor Cyan
    $required = @(
        'rootsandfruit/ping',
        'rootsandfruit/enable-public-preview',
        'rootsandfruit/get-public-preview-url',
        'rootsandfruit/list-posts',
        'rootsandfruit/get-post',
        'rootsandfruit/create-draft',
        'rootsandfruit/update-post',
        'rootsandfruit/set-post-author',
        'rootsandfruit/publish-post'
    )
    if ($RequirePreview) {
        # Preview abilities already in $required
    }
    foreach ($req in $required) {
        if ($mcpAbilityNames -contains $req) {
            Write-Host "OK   discover: $req"
        } else {
            Write-Host "FAIL discover: $req missing" -ForegroundColor Red
            $failed = $true
        }
    }

    Write-Host "`n=== MCP: execute rootsandfruit/ping ===" -ForegroundColor Cyan
    try {
        $execArgs = (@{ ability_name = 'rootsandfruit/ping'; parameters = @{} } | ConvertTo-Json -Compress)
        $execBody = '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"mcp-adapter-execute-ability","arguments":' + $execArgs + '}}'
        $r4 = Send-Mcp -JsonBody $execBody -ExtraHeaders @{ 'Mcp-Session-Id' = $sessionId }
        $exec = $r4.Content | ConvertFrom-Json
        $payload = $exec.result.content[0].text | ConvertFrom-Json
        if ($payload.success -eq $true -and $payload.data.ok -eq $true -and $payload.data.plugin_version) {
            Write-Host "OK  ping version=$($payload.data.plugin_version) block_mcp_active=$($payload.data.block_mcp_active)"
        } else {
            Write-Host "FAIL ping execute: $($exec.result.content[0].text)" -ForegroundColor Red
            $failed = $true
        }
    } catch {
        Write-Host "FAIL ping execute: $($_.Exception.Message)" -ForegroundColor Red
        $failed = $true
    }
}

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
    foreach ($name in $requiredBlocks) {
        if ($mcpAbilityNames -contains $name) {
            Write-Host "OK   $name"
        } else {
            Write-Host "FAIL $name missing (gk-block-mcp inactive?)" -ForegroundColor Red
            $failed = $true
        }
    }
}

if ($failed) {
    Write-Host "`nSmoke test completed with failures." -ForegroundColor Red
    exit 1
}

Write-Host "`nSmoke test passed." -ForegroundColor Green
exit 0
