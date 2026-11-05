#Requires -Version 5.1
<#
.SYNOPSIS
  Verify nephroctor.sk / .eu path-preserving redirects after WebSupport panel aliasing.
.DESCRIPTION
  Expects HTTP 301 to the canonical .com legal document (path preserved).
  Upstream OpenResty HTTP redirect still yields 302 to https://nephroctor.com (path drop).
  PowerShell 5.1 compatible. No secrets.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

$cases = @(
    @{ Url = 'https://nephroctor.sk/privacy'; ExpectStatus = 301; ExpectLocationContains = '/legal/ochrana-osobnych-udajov.html' }
    @{ Url = 'https://nephroctor.eu/terms';   ExpectStatus = 301; ExpectLocationContains = '/legal/podmienky-pouzivania.html' }
    @{ Url = 'https://nephroctor.sk/cookies'; ExpectStatus = 301; ExpectLocationContains = '/legal/cookies.html' }
    @{ Url = 'https://nephroctor.eu/legal';   ExpectStatus = 301; ExpectLocationContains = '/legal/pravne-informacie.html' }
    @{ Url = 'https://nephroctor.com/privacy'; ExpectStatus = 301; ExpectLocationContains = '/legal/ochrana-osobnych-udajov.html' }
)

$fail = 0
foreach ($c in $cases) {
    $tmp = [System.IO.Path]::GetTempFileName()
    try {
        $code = & curl.exe -s -D $tmp -o NUL -A $ua --connect-timeout 10 --max-time 20 -w '%{http_code}' $c.Url
        if ($LASTEXITCODE -ne 0 -and [string]::IsNullOrWhiteSpace($code)) { $code = '000' }
        $headers = Get-Content -LiteralPath $tmp -ErrorAction SilentlyContinue
        $location = ($headers | Where-Object { $_ -match '^(?i)location:\s*(.+)$' } | Select-Object -First 1)
        if ($location -match '^(?i)location:\s*(.+)$') { $location = $Matches[1].Trim() } else { $location = '' }

        $okStatus = ($code -as [string]) -eq ([string]$c.ExpectStatus)
        $okLoc = $location -like ('*' + $c.ExpectLocationContains + '*')
        $verdict = if ($okStatus -and $okLoc) { 'OK' } else { 'FAIL' }
        if ($verdict -eq 'FAIL') { $fail++ }

        Write-Host ("{0,-42} {1} -> {2}  [{3}]" -f $c.Url, $code, $location, $verdict)

        if (-not $okStatus -and $code -eq '302' -and $location -match '^https://nephroctor\.com/?$') {
            Write-Host '  hint: still OpenResty HTTP redirect (path drop). Switch panel to domain alias.' -ForegroundColor Yellow
        }
    }
    finally {
        Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
    }
}

if ($fail -gt 0) {
    Write-Host ("Result: {0} case(s) failed. Panel alias still required for .sk/.eu." -f $fail) -ForegroundColor Yellow
    exit 1
}
Write-Host 'Result: all alias redirects OK.' -ForegroundColor Green
exit 0
