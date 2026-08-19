$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Resolve-ProjectPython {
    param([Parameter(Mandatory = $true)][string]$Root)

    $candidates = New-Object System.Collections.Generic.List[string]
    if ($env:SOFTIMOVEIS_PYTHON) {
        $candidates.Add($env:SOFTIMOVEIS_PYTHON)
    }

    $candidates.Add((Join-Path $Root ".venv\Scripts\python.exe"))
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand) {
        $candidates.Add($pythonCommand.Source)
    }

    foreach ($candidate in $candidates) {
        if ($candidate -and (Test-Path $candidate)) {
            return (Resolve-Path $candidate).Path
        }
    }

    throw "Python nao encontrado. Crie .venv, defina SOFTIMOVEIS_PYTHON ou instale Python 3.12+."
}

function Assert-PythonVersion {
    param([Parameter(Mandatory = $true)][string]$Python)

    $output = & $Python -c "import sys; print(sys.version.split()[0]); raise SystemExit(0 if sys.version_info >= (3, 12) else 1)" 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python 3.12+ requerido. Saida: $output"
    }
    return [string]$output
}

function Get-PythonPackageVersions {
    param([Parameter(Mandatory = $true)][string]$Python)

    $script = @"
import PyInstaller
import PySide6
import pytest
print(PySide6.__version__)
print(PyInstaller.__version__)
print(pytest.__version__)
"@
    $output = & $Python -c $script 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Dependencias nao encontradas. Saida: $output"
    }
    return [PSCustomObject]@{
        PySide6     = [string]$output[0]
        PyInstaller = [string]$output[1]
        Pytest      = [string]$output[2]
    }
}

function Get-ApplicationInfo {
    param([Parameter(Mandatory = $true)][string]$Python)

    $script = "import json; from src.core.constants import APP_NAME, APP_VERSION; print(json.dumps({'name': APP_NAME, 'version': APP_VERSION}, ensure_ascii=True))"
    $output = & $Python -c $script 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Nao foi possivel ler APP_NAME/APP_VERSION. Saida: $output"
    }
    $app = ([string]$output).Trim() | ConvertFrom-Json
    return [PSCustomObject]@{
        Name    = [string]$app.name
        Version = [string]$app.version
    }
}

function Invoke-ProjectTests {
    param([Parameter(Mandatory = $true)][string]$Python)

    $output = & $Python -m pytest 2>&1
    $exitCode = $LASTEXITCODE
    $output | ForEach-Object { Write-Host $_ }
    if ($exitCode -ne 0) {
        throw "pytest falhou com exit code $exitCode."
    }

    $summary = ($output | Select-String -Pattern "\d+\s+passed.*" | Select-Object -Last 1).Line
    if (-not $summary) {
        $summary = "pytest concluido"
    }

    return [PSCustomObject]@{
        Status  = "OK"
        Summary = [string]$summary
    }
}

function Remove-ProjectPath {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$RelativePath,
        [switch]$Recurse
    )

    $rootFull = [System.IO.Path]::GetFullPath($Root).TrimEnd("\")
    $targetFull = [System.IO.Path]::GetFullPath((Join-Path $Root $RelativePath))
    $rootPrefix = "$rootFull\"
    if (-not $targetFull.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Recusa ao remover caminho fora do projeto: $targetFull"
    }

    if (Test-Path $targetFull) {
        if ($Recurse) {
            Remove-Item -LiteralPath $targetFull -Recurse -Force
        } else {
            Remove-Item -LiteralPath $targetFull -Force
        }
    }
}

function Clear-BuildOutputs {
    param([Parameter(Mandatory = $true)][string]$Root)

    Remove-ProjectPath -Root $Root -RelativePath "build" -Recurse
    Remove-ProjectPath -Root $Root -RelativePath "dist" -Recurse
    Remove-ProjectPath -Root $Root -RelativePath "SoftImoveis.spec"
}

function Invoke-PyInstallerBuild {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$Python
    )

    $assets = Join-Path $Root "src\assets"
    $main = Join-Path $Root "src\main.py"
    & $Python -m PyInstaller `
        --noconfirm `
        --clean `
        --windowed `
        --name SoftImoveis `
        --add-data "$assets;src\assets" `
        --distpath (Join-Path $Root "dist") `
        --workpath (Join-Path $Root "build") `
        $main

    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller falhou com exit code $LASTEXITCODE."
    }
}

function Get-ExecutablePath {
    param([Parameter(Mandatory = $true)][string]$Root)
    return (Join-Path $Root "dist\SoftImoveis\SoftImoveis.exe")
}

function Assert-OnedirBuild {
    param([Parameter(Mandatory = $true)][string]$Root)

    $exe = Get-ExecutablePath -Root $Root
    $internal = Join-Path $Root "dist\SoftImoveis\_internal"
    $assets = Join-Path $internal "src\assets"
    $icons = Join-Path $assets "icons"
    $qwindows = Join-Path $internal "PySide6\plugins\platforms\qwindows.dll"

    foreach ($path in @($exe, $internal, $assets, $icons, $qwindows)) {
        if (-not (Test-Path $path)) {
            throw "Artefato esperado nao encontrado: $path"
        }
    }

    return [PSCustomObject]@{
        Executable = $exe
        Internal   = $internal
        Assets     = $assets
        Icons      = $icons
        QtPlatform = $qwindows
    }
}

function Get-FileSignatureInfo {
    param([Parameter(Mandatory = $true)][string]$Path)

    try {
        $signature = Get-AuthenticodeSignature -FilePath $Path -ErrorAction Stop
        $status = [string]$signature.Status
        $statusMessage = [string]$signature.StatusMessage
        $subject = ""
        $issuer = ""
        if ($signature.SignerCertificate) {
            $subject = [string]$signature.SignerCertificate.Subject
            $issuer = [string]$signature.SignerCertificate.Issuer
        }
        return [PSCustomObject]@{
            Path          = $Path
            FileName      = Split-Path -Leaf $Path
            Extension     = [System.IO.Path]::GetExtension($Path).TrimStart(".").ToUpperInvariant()
            Status        = $status
            StatusMessage = $statusMessage
            Publisher     = $subject
            Issuer        = $issuer
            IsValid       = ($status -eq "Valid")
            IsSigned      = ($status -ne "NotSigned")
        }
    } catch {
        return [PSCustomObject]@{
            Path          = $Path
            FileName      = Split-Path -Leaf $Path
            Extension     = [System.IO.Path]::GetExtension($Path).TrimStart(".").ToUpperInvariant()
            Status        = "UnknownError"
            StatusMessage = $_.Exception.Message
            Publisher     = ""
            Issuer        = ""
            IsValid       = $false
            IsSigned      = $false
        }
    }
}

function Get-SigningConfig {
    $enabledValues = @("1", "true", "yes", "on")
    $enabled = $false
    if ($env:SOFTIMOVEIS_SIGN_ENABLED) {
        $enabled = $enabledValues -contains $env:SOFTIMOVEIS_SIGN_ENABLED.ToLowerInvariant()
    }

    return [PSCustomObject]@{
        Enabled        = $enabled
        Thumbprint     = $env:SOFTIMOVEIS_CERT_THUMBPRINT
        TimestampUrl   = $env:SOFTIMOVEIS_TIMESTAMP_URL
        PfxPath        = $env:SOFTIMOVEIS_PFX_PATH
        HasPfxPassword = [bool]$env:SOFTIMOVEIS_PFX_PASSWORD
        SignToolPath   = $env:SOFTIMOVEIS_SIGNTOOL_PATH
    }
}

function Assert-SigningConfig {
    param([Parameter(Mandatory = $true)]$Config)

    if (-not $Config.Enabled) {
        throw "Nenhum certificado de assinatura de codigo confiavel foi configurado. Defina SOFTIMOVEIS_SIGN_ENABLED=1 e configure certificate store ou PFX via variaveis de ambiente."
    }
    if (-not $Config.TimestampUrl) {
        throw "SOFTIMOVEIS_TIMESTAMP_URL e obrigatorio para release assinada."
    }
    if ($Config.Thumbprint -and $Config.PfxPath) {
        throw "Configure apenas SOFTIMOVEIS_CERT_THUMBPRINT ou SOFTIMOVEIS_PFX_PATH, nao ambos."
    }
    if (-not $Config.Thumbprint -and -not $Config.PfxPath) {
        throw "Configure SOFTIMOVEIS_CERT_THUMBPRINT ou SOFTIMOVEIS_PFX_PATH."
    }
    if ($Config.PfxPath -and -not (Test-Path $Config.PfxPath)) {
        throw "SOFTIMOVEIS_PFX_PATH nao encontrado."
    }
}

function Find-SignTool {
    $candidates = New-Object System.Collections.Generic.List[string]
    if ($env:SOFTIMOVEIS_SIGNTOOL_PATH) {
        $candidates.Add($env:SOFTIMOVEIS_SIGNTOOL_PATH)
    }

    $command = Get-Command signtool.exe -ErrorAction SilentlyContinue
    if ($command) {
        $candidates.Add($command.Source)
    }

    $sdkRoots = @(
        (Join-Path ${env:ProgramFiles(x86)} "Windows Kits\10\bin"),
        (Join-Path $env:ProgramFiles "Windows Kits\10\bin")
    ) | Where-Object { $_ -and (Test-Path $_) }

    foreach ($sdkRoot in $sdkRoots) {
        Get-ChildItem -LiteralPath $sdkRoot -Recurse -Filter "signtool.exe" -ErrorAction SilentlyContinue |
            Where-Object { $_.FullName -match "\\(x64|arm64|x86)\\signtool\.exe$" } |
            Sort-Object FullName -Descending |
            ForEach-Object { $candidates.Add($_.FullName) }
    }

    foreach ($candidate in $candidates) {
        if ($candidate -and (Test-Path $candidate)) {
            return (Resolve-Path $candidate).Path
        }
    }

    throw "SignTool nao encontrado. Instale Windows SDK Signing Tools antes de gerar uma release assinada."
}

function Invoke-CodeSigning {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)]$Config,
        [Parameter(Mandatory = $true)][string]$SignTool
    )

    $arguments = @("sign", "/fd", "SHA256", "/td", "SHA256", "/tr", $Config.TimestampUrl)
    if ($Config.Thumbprint) {
        $arguments += @("/sha1", $Config.Thumbprint)
    } elseif ($Config.PfxPath) {
        $arguments += @("/f", $Config.PfxPath)
        if ($env:SOFTIMOVEIS_PFX_PASSWORD) {
            $arguments += @("/p", $env:SOFTIMOVEIS_PFX_PASSWORD)
        }
    }
    $arguments += $FilePath

    & $SignTool @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "SignTool falhou com exit code $LASTEXITCODE."
    }
}

function Write-BuildMetadata {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$Python,
        [Parameter(Mandatory = $true)][string]$BuildType,
        [Parameter(Mandatory = $true)]$Signature
    )

    $app = Get-ApplicationInfo -Python $Python
    $pythonVersion = Assert-PythonVersion -Python $Python
    $versions = Get-PythonPackageVersions -Python $Python
    $signed = if ($Signature.Status -eq "Valid") { "Yes" } else { "No" }
    $metadataPath = Join-Path $Root "dist\SoftImoveis\BUILD_METADATA.txt"

    $lines = @(
        $app.Name,
        "Version: $($app.Version)",
        "Build Date: $((Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"))",
        "Python Version: $pythonVersion",
        "PySide6 Version: $($versions.PySide6)",
        "PyInstaller Version: $($versions.PyInstaller)",
        "Build Type: $BuildType",
        "Signed: $signed",
        "Authenticode Status: $($Signature.Status)"
    )
    $lines | Set-Content -LiteralPath $metadataPath -Encoding UTF8
    return $metadataPath
}

function Write-BuildReport {
    param(
        [Parameter(Mandatory = $true)][string]$Root,
        [Parameter(Mandatory = $true)][string]$BuildType,
        [Parameter(Mandatory = $true)]$TestResult,
        [Parameter(Mandatory = $true)]$Signature,
        [Parameter(Mandatory = $true)][string]$Executable,
        [Parameter(Mandatory = $true)][string]$MetadataPath,
        [Parameter(Mandatory = $true)][bool]$ReleaseReady
    )

    $releaseText = if ($ReleaseReady) { "YES" } else { "NO" }
    $reportPath = Join-Path $Root "dist\SoftImoveis\BUILD_REPORT.txt"
    $lines = @(
        "Soft-Imoveis Build Report",
        "Generated ............... $((Get-Date).ToString("yyyy-MM-dd HH:mm:ss"))",
        "Build Type .............. $BuildType",
        "Build Status ............ OK",
        "Tests ................... OK ($($TestResult.Summary))",
        "PyInstaller ............. OK",
        "Executable .............. OK ($Executable)",
        "Authenticode ............ $($Signature.Status)",
        "Release Ready ........... $releaseText",
        "Metadata ................ $MetadataPath"
    )
    $lines | Set-Content -LiteralPath $reportPath -Encoding UTF8

    Write-Host ""
    $lines | ForEach-Object { Write-Host $_ }
    Write-Host ""
    return $reportPath
}

function Invoke-ExecutableSmokeTest {
    param([Parameter(Mandatory = $true)][string]$Executable)

    & $Executable --smoke-test
    if ($LASTEXITCODE -ne 0) {
        throw "Smoke test do EXE falhou com exit code $LASTEXITCODE."
    }
}

function ConvertTo-MarkdownCell {
    param([AllowNull()][object]$Value)
    if ($null -eq $Value) {
        return ""
    }
    return ([string]$Value).Replace("|", "\|").Replace("`r", " ").Replace("`n", " ")
}
