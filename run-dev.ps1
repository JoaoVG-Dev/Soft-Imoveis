param(
    [switch]$SmokeTest,
    [string[]]$AppArgs = @()
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $Root "scripts\pipeline-common.ps1")

$Python = Resolve-ProjectPython -Root $Root
$PythonVersion = Assert-PythonVersion -Python $Python
$null = Get-PythonPackageVersions -Python $Python

Write-Host "Soft-Imoveis DEV RUN"
Write-Host "[OK] Python: $PythonVersion ($Python)"

$arguments = @("-m", "src.main")
if ($SmokeTest) {
    $arguments += "--smoke-test"
}
$arguments += $AppArgs

Push-Location $Root
try {
    & $Python @arguments
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
