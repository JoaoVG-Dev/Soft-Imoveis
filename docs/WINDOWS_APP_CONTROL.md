# Windows App Control

Este documento registra o diagnóstico confirmado para o executável da V0.2. Não é bug da aplicação Python/PySide6 e não deve ser tratado com alteração de UI, arquitetura ou regras de negócio.

## Diagnóstico Confirmado

Policy:

```text
VerifiedAndReputableDesktop
```

Policy ID:

```text
0283ac0f-fff1-49ae-ada1-8a933130cad6
```

Currently Applied:

```text
true
```

SoftImoveis.exe:

```text
Authenticode Status: NotSigned
```

Code Integrity Event:

```text
Microsoft-Windows-CodeIntegrity/Operational
Event ID: 3077
```

Resultado:

```text
SoftImoveis.exe
    -> não possui assinatura Authenticode
    -> Smart App Control / VerifiedAndReputableDesktop
    -> bloqueio antes da inicialização
```

## Decisão De Engenharia

O projeto separa:

```text
Development Build
Python -> Tests -> PyInstaller -> Dev Build
```

de:

```text
Signed Release
Python -> Tests -> PyInstaller -> Authenticode -> Timestamp -> Verification -> Smoke Test -> Release
```

`build.ps1` produz uma build local válida mesmo quando `SoftImoveis.exe` estiver `NotSigned`. Essa build pode ser bloqueada pelo Smart App Control se executada diretamente.

`release.ps1` exige certificado confiável, timestamp e `Get-AuthenticodeSignature` com `Status == Valid` antes de continuar para smoke test.

## Desenvolvimento

Enquanto não houver assinatura confiável, o fluxo oficial de desenvolvimento é:

```powershell
.\run-dev.ps1
```

Smoke test sem abrir a janela permanentemente:

```powershell
.\run-dev.ps1 -SmokeTest
```

## Release

Variáveis de ambiente suportadas:

```text
SOFTIMOVEIS_SIGN_ENABLED
SOFTIMOVEIS_CERT_THUMBPRINT
SOFTIMOVEIS_TIMESTAMP_URL
SOFTIMOVEIS_SIGNTOOL_PATH
SOFTIMOVEIS_PFX_PATH
SOFTIMOVEIS_PFX_PASSWORD
```

Nenhum segredo deve ser versionado ou impresso em log. A senha de PFX, quando usada, deve vir de variável de ambiente ou secret de CI.

## Auditoria

Auditar binários do onedir:

```powershell
.\scripts\audit-signatures.ps1
```

Verificar política aplicada em modo somente leitura:

```powershell
.\scripts\check-app-control.ps1
```

Os scripts deste projeto não desativam Smart App Control, Device Guard, WDAC, AppLocker, Defender nem qualquer política do Windows.
