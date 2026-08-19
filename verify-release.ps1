$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $Root "scripts\pipeline-common.ps1")

$Artifacts = Assert-OnedirBuild -Root $Root
$Signature = Get-FileSignatureInfo -Path $Artifacts.Executable

Write-Host "Soft-Imoveis RELEASE VERIFY"
Write-Host "Executable: $($Artifacts.Executable)"
Write-Host "Authenticode: $($Signature.Status)"

if ($Signature.Status -ne "Valid") {
    Write-Host "RELEASE VERIFY FAILED"
    Write-Host "A release so pode ser verificada quando SoftImoveis.exe estiver com Authenticode Status == Valid."
    exit 2
}

& (Join-Path $Root "scripts\audit-signatures.ps1")
Invoke-ExecutableSmokeTest -Executable $Artifacts.Executable
Write-Host "RELEASE VERIFY OK"
