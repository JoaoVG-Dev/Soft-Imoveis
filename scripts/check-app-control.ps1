$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Write-Host "Soft-Imoveis Smart App Control diagnostic"
Write-Host "Modo: somente leitura"

$ciTool = Get-Command CiTool -ErrorAction SilentlyContinue
if (-not $ciTool) {
    Write-Host "CiTool nao encontrado neste ambiente."
    exit 1
}

$output = & $ciTool.Source --list-policies 2>&1
$exitCode = $LASTEXITCODE
$output | ForEach-Object { Write-Host $_ }

$text = ($output -join "`n")
if ($exitCode -ne 0 -or $text -match "0x80070005" -or $text -match "Ocorreu um erro") {
    Write-Host ""
    Write-Host "[INFO] CiTool nao retornou a lista de politicas para este processo."
    Write-Host "[INFO] Diagnostico preservado em docs\WINDOWS_APP_CONTROL.md quando a leitura direta nao estiver disponivel."
    Write-Host "Nenhuma politica foi alterada."
    exit 2
}

$hasPolicy = $text -match "VerifiedAndReputableDesktop"
$isApplied = $false
if ($hasPolicy) {
    $policyIndex = $text.IndexOf("VerifiedAndReputableDesktop")
    $window = $text.Substring($policyIndex, [Math]::Min(800, $text.Length - $policyIndex))
    $isApplied = $window -match "Currently Applied:\s*true"
}

Write-Host ""
if ($hasPolicy -and $isApplied) {
    Write-Host "[INFO] VerifiedAndReputableDesktop esta aplicado."
} elseif ($hasPolicy) {
    Write-Host "[INFO] VerifiedAndReputableDesktop foi encontrado, mas nao aparece como aplicado no bloco analisado."
} else {
    Write-Host "[INFO] VerifiedAndReputableDesktop nao foi encontrado na saida do CiTool."
}
Write-Host "Nenhuma politica foi alterada."
