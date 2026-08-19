$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $Root "scripts\pipeline-common.ps1")

Write-Host "Soft-Imoveis SIGNED RELEASE"
Write-Host "Gerando build de desenvolvimento como base da release..."
& (Join-Path $Root "build.ps1")

$Python = Resolve-ProjectPython -Root $Root
$Artifacts = Assert-OnedirBuild -Root $Root
$Config = Get-SigningConfig

try {
    Assert-SigningConfig -Config $Config
} catch {
    Write-Host ""
    Write-Host "RELEASE CANCELADA"
    Write-Host ""
    Write-Host "Nenhum certificado de assinatura de codigo confiavel foi configurado."
    Write-Host "A build de desenvolvimento foi gerada normalmente."
    Write-Host "Configure as credenciais de Code Signing para produzir uma release distribuivel."
    Write-Host "Detalhe: $($_.Exception.Message)"
    exit 2
}

$SignTool = Find-SignTool
Write-Host "[OK] SignTool: $SignTool"
Write-Host "Assinando SoftImoveis.exe com Authenticode e timestamp..."
Invoke-CodeSigning -FilePath $Artifacts.Executable -Config $Config -SignTool $SignTool

$Signature = Get-FileSignatureInfo -Path $Artifacts.Executable
Write-Host "[INFO] Authenticode: $($Signature.Status)"
if ($Signature.Status -ne "Valid") {
    Write-Host "RELEASE FAILED"
    throw "Assinatura invalida apos SignTool: $($Signature.Status)"
}

$TestResult = [PSCustomObject]@{
    Status  = "OK"
    Summary = "executado em build.ps1"
}
$MetadataPath = Write-BuildMetadata -Root $Root -Python $Python -BuildType "Release" -Signature $Signature
$ReportPath = Write-BuildReport -Root $Root -BuildType "Release" -TestResult $TestResult -Signature $Signature -Executable $Artifacts.Executable -MetadataPath $MetadataPath -ReleaseReady:$true

Write-Host "Executando smoke test do EXE assinado..."
Invoke-ExecutableSmokeTest -Executable $Artifacts.Executable
Write-Host "[OK] Smoke test do EXE assinado"

& (Join-Path $Root "scripts\audit-signatures.ps1")

Write-Host "[OK] Relatorio: $ReportPath"
Write-Host "SIGNED RELEASE CONCLUIDA"
