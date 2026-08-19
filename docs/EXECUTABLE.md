# Soft-Imóveis Desktop — Executável Windows

## 1. Visão Geral

O Soft-Imóveis Desktop é desenvolvido em:

```text
Python 3.12+
PySide6
Qt
```

e distribuído através de:

```text
PyInstaller
```

## 2. Fluxo

Build de desenvolvimento:

```text
Código Python
    ↓
pytest
    ↓
PyInstaller
    ↓
DEV BUILD
```

Release futura:

```text
Código Python
    ↓
pytest
    ↓
PyInstaller
    ↓
Authenticode
    ↓
Timestamp
    ↓
Verification
    ↓
Signed Release
```

## 3. Executável Atual

```text
Version: 0.2.0
Build Type: Development
Packaging: onedir
Authenticode: NotSigned
```

Build original:

```text
dist/SoftImoveis/SoftImoveis.exe
```

Snapshot histórico:

```text
references/executables/v0.2.0/SoftImoveis.exe
```

## 4. Desenvolvimento

O fluxo oficial de desenvolvimento permanece:

```powershell
.\run-dev.ps1
```

## 5. Build

```powershell
.\build.ps1
```

Esse processo:

- executa testes;
- gera DEV build;
- não exige assinatura;
- não precisa executar o EXE caso Smart App Control o bloqueie.

## 6. Release

```powershell
.\release.ps1
```

Requisitos:

- certificado de Code Signing confiável;
- SignTool;
- Authenticode;
- timestamp;
- assinatura válida;
- smoke test.

## 7. Smart App Control

Diagnóstico confirmado:

```text
Policy:
VerifiedAndReputableDesktop

Policy ID:
0283ac0f-fff1-49ae-ada1-8a933130cad6

Executable:
SoftImoveis.exe

Authenticode:
NotSigned

Code Integrity Event:
3077
```

Conclusão:

```text
O executável de desenvolvimento é bloqueado pelo
Smart App Control por não possuir confiança/assinatura
suficiente para a política aplicada.
```

Isso não é bug da aplicação.

## 8. Auditoria de Binários

Situação atual:

```text
67 binários auditados

53 Valid
14 NotSigned
```

Entre os `NotSigned` estão:

```text
SoftImoveis.exe
_bz2.pyd
_decimal.pyd
_hashlib.pyd
_lzma.pyd
_queue.pyd
_socket.pyd
_ssl.pyd
libcrypto-3-x64.dll
libssl-3-x64.dll
python3.dll
python312.dll
select.pyd
unicodedata.pyd
```

Status:

```text
PENDENTE DE VALIDAÇÃO DURANTE O PROCESSO DE SIGNED RELEASE
```

## 9. Integridade

SHA-256 do executável arquivado:

```text
18F1E80D66E4C4738B16E03795D68BA268DD8F635F27CC4973ABD48A05C5F453
```

## 10. Política de Arquivamento

```text
dist/
```

é artefato transitório de build.

```text
references/executables/
```

é acervo de snapshots selecionados/versionados.

Não arquivar toda build automaticamente. Somente versões explicitamente selecionadas devem ser preservadas.
