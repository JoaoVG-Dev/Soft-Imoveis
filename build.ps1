$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $Root "scripts\pipeline-common.ps1")

Write-Host "Soft-Imoveis DEV BUILD"
Write-Host "Root: $Root"

Write-Host "Validando Python..."
$Python = Resolve-ProjectPython -Root $Root
$PythonVersion = Assert-PythonVersion -Python $Python
Write-Host "[OK] Python: $PythonVersion ($Python)"

Write-Host "Validando dependencias..."
$Versions = Get-PythonPackageVersions -Python $Python
Write-Host "[OK] PySide6: $($Versions.PySide6)"
Write-Host "[OK] PyInstaller: $($Versions.PyInstaller)"
Write-Host "[OK] pytest: $($Versions.Pytest)"

Write-Host "Executando testes..."
$TestResult = Invoke-ProjectTests -Python $Python
Write-Host "[OK] Testes: $($TestResult.Summary)"

Write-Host "Limpando builds anteriores..."
Clear-BuildOutputs -Root $Root

Write-Host "Gerando executavel com PyInstaller onedir/windowed..."
Invoke-PyInstallerBuild -Root $Root -Python $Python
Write-Host "[OK] PyInstaller concluido"

Write-Host "Validando artefatos produzidos..."
$Artifacts = Assert-OnedirBuild -Root $Root
Write-Host "[OK] SoftImoveis.exe gerado: $($Artifacts.Executable)"
Write-Host "[OK] Assets: $($Artifacts.Assets)"
Write-Host "[OK] Qt platform plugin: $($Artifacts.QtPlatform)"

Write-Host "Consultando assinatura Authenticode..."
$Signature = Get-FileSignatureInfo -Path $Artifacts.Executable
Write-Host "[INFO] Authenticode: $($Signature.Status)"
if ($Signature.Status -ne "Valid") {
    Write-Host "[INFO] Release assinada: nao disponivel"
    Write-Host "[INFO] Execucao direta do EXE pode ser bloqueada pelo Smart App Control"
}

$MetadataPath = Write-BuildMetadata -Root $Root -Python $Python -BuildType "Development" -Signature $Signature
$ReportPath = Write-BuildReport -Root $Root -BuildType "Development" -TestResult $TestResult -Signature $Signature -Executable $Artifacts.Executable -MetadataPath $MetadataPath -ReleaseReady:$false

Write-Host "[OK] Metadata: $MetadataPath"
Write-Host "[OK] Relatorio: $ReportPath"
Write-Host "DEV BUILD CONCLUIDO"
