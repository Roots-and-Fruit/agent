# Invoke one WordPress MCP ability via JSON-RPC (loads agent/.env).
param(
    [Parameter(Mandatory = $true)][string] $AbilityName,
    [string] $ParametersJson,
    [string] $ParametersFile,
    [string] $EnvFile
)

if (-not $ParametersJson -and -not $ParametersFile) {
    Write-Error "Provide -ParametersJson or -ParametersFile (UTF-8 JSON)."
    exit 1
}
if ($ParametersFile) {
    $ParametersJson = [System.IO.File]::ReadAllText((Resolve-Path $ParametersFile), [System.Text.Encoding]::UTF8)
}

$agentRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (-not $EnvFile) { $EnvFile = Join-Path $agentRoot '.env' }

Get-Content $EnvFile | ForEach-Object {
    if ($_ -match '^\s*([^#=]+)=(.*)$') {
        Set-Item -Path "Env:$($matches[1].Trim())" -Value $matches[2].Trim().Trim('"').Trim("'")
    }
}

$Url = $env:ROOTSANDFRUIT_MCP_URL
$Username = $env:ROOTSANDFRUIT_MCP_USERNAME
$Password = $env:ROOTSANDFRUIT_MCP_PASSWORD
$b64 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${Username}:${Password}"))
$headers = @{ Authorization = "Basic $b64"; Accept = 'application/json' }

function Send-Mcp([string] $Body, [hashtable] $Extra = @{}) {
    $h = $headers.Clone()
    foreach ($k in $Extra.Keys) { $h[$k] = $Extra[$k] }
    return Invoke-WebRequest -Uri $Url -Method Post -Headers $h `
        -ContentType 'application/json; charset=utf-8' `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($Body)) -UseBasicParsing
}

$initBody = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"invoke-mcp-ability","version":"1.0.0"}}}'
$r1 = Send-Mcp $initBody
$sessionId = $r1.Headers['Mcp-Session-Id']

$params = $ParametersJson | ConvertFrom-Json
$execArgs = (@{ ability_name = $AbilityName; parameters = $params } | ConvertTo-Json -Depth 100 -Compress)
$execBody = '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"mcp-adapter-execute-ability","arguments":' + $execArgs + '}}'
$r2 = Send-Mcp $execBody @{ 'Mcp-Session-Id' = $sessionId }
($r2.Content | ConvertFrom-Json).result.content[0].text
