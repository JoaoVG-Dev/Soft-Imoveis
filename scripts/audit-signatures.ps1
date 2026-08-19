param(
    [string]$DistPath = "",
    [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
. (Join-Path $ScriptDir "pipeline-common.ps1")

if (-not $DistPath) {
    $DistPath = Join-Path $Root "dist\SoftImoveis"
}
if (-not $OutputPath) {
    $OutputPath = Join-Path $Root "docs\SIGNING_AUDIT.md"
}

if (-not (Test-Path $DistPath)) {
    throw "Diretorio de distribuicao nao encontrado: $DistPath"
}

$distFull = [System.IO.Path]::GetFullPath($DistPath).TrimEnd("\")
$files = Get-ChildItem -LiteralPath $distFull -Recurse -File |
    Where-Object { @(".exe", ".dll", ".pyd") -contains $_.Extension.ToLowerInvariant() } |
    Sort-Object FullName

$items = foreach ($file in $files) {
    $signature = Get-FileSignatureInfo -Path $file.FullName
    $relative = $file.FullName.Substring($distFull.Length).TrimStart("\")
    $owner = if ($relative -eq "SoftImoveis.exe") { "Projeto Soft-Imoveis" } else { "Fornecedor/terceiro" }
    $note = if ($relative -eq "SoftImoveis.exe" -and $signature.Status -eq "NotSigned") {
        "Artefato proprio; assinar em release."
    } elseif ($signature.Status -eq "Valid") {
        "Assinatura valida do fornecedor."
    } elseif ($signature.Status -eq "NotSigned") {
        "Binario sem assinatura; avaliar origem antes de distribuicao."
    } else {
        "Revisar status Authenticode."
    }

    [PSCustomObject]@{
        File          = $relative
        Type          = $signature.Extension
        Signature     = $signature.Status
        Publisher     = $signature.Publisher
        StatusMessage = $signature.StatusMessage
        Owner         = $owner
        Note          = $note
    }
}

$items | Format-Table File, Type, Signature, Publisher -AutoSize

$summary = $items | Group-Object Signature | Sort-Object Name
$validCount = ($items | Where-Object { $_.Signature -eq "Valid" }).Count
$notSignedCount = ($items | Where-Object { $_.Signature -eq "NotSigned" }).Count

$lines = New-Object System.Collections.Generic.List[string]
$generatedAt = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
$lines.Add("# Signing Audit")
$lines.Add("")
$lines.Add("Generated: $generatedAt")
$lines.Add("")
$lines.Add("Distribution: ``$DistPath``")
$lines.Add("")
$lines.Add("## Summary")
$lines.Add("")
$lines.Add("- Total EXE/DLL/PYD: $($items.Count)")
$lines.Add("- Valid: $validCount")
$lines.Add("- NotSigned: $notSignedCount")
foreach ($group in $summary) {
    if ($group.Name -notin @("Valid", "NotSigned")) {
        $lines.Add("- $($group.Name): $($group.Count)")
    }
}
$lines.Add("")
$lines.Add("## Details")
$lines.Add("")
$lines.Add("| arquivo | tipo | assinatura | publisher | status | observacao |")
$lines.Add("|---|---|---|---|---|---|")
foreach ($item in $items) {
    $lines.Add("| $(ConvertTo-MarkdownCell $item.File) | $(ConvertTo-MarkdownCell $item.Type) | $(ConvertTo-MarkdownCell $item.Signature) | $(ConvertTo-MarkdownCell $item.Publisher) | $(ConvertTo-MarkdownCell $item.StatusMessage) | $(ConvertTo-MarkdownCell $item.Note) |")
}
$lines.Add("")
$lines.Add("## Notes")
$lines.Add("")
$lines.Add("- Este script e somente auditoria; ele nao assina, remove ou modifica binarios.")
$lines.Add("- ``SoftImoveis.exe`` e o artefato proprio do projeto e deve ser assinado no pipeline de release.")
$lines.Add("- Binarios de terceiros nao devem ser modificados automaticamente sem avaliacao da origem.")

$outputDirectory = Split-Path -Parent $OutputPath
if (-not (Test-Path $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory | Out-Null
}
$lines | Set-Content -LiteralPath $OutputPath -Encoding UTF8
Write-Host "[OK] Signing audit: $OutputPath"
