# Soft-Imóveis Desktop — Executável de Referência V0.2

## Identificação

- Produto: Soft-Imóveis Desktop
- Versão: 0.2.0
- Linguagem: Python
- UI: PySide6
- Packaging: PyInstaller
- Formato: `onedir`
- Executável: `SoftImoveis.exe`
- Tipo: Development Build
- Assinatura Authenticode: NotSigned

## Objetivo

Este arquivo é um snapshot de referência do executável correspondente à V0.2.

Ele é mantido para:

- histórico;
- comparação;
- QA;
- regressão visual;
- referência de build;
- auditoria.

## Importante

> Este executável é uma DEVELOPMENT BUILD não assinada e pode ser bloqueado pelo Smart App Control do Windows 11.

Não há orientação para desabilitar mecanismos de segurança.

## Execução em desenvolvimento

O fluxo oficial de desenvolvimento permanece:

```powershell
.\run-dev.ps1
```

ou comando Python equivalente do projeto.

## Distribuição

> Este arquivo não deve ser tratado como release pública ou instalador de produção.

A futura distribuição deverá passar por:

```text
PyInstaller
→ Authenticode
→ Timestamp
→ Verification
→ Smoke Test
→ Release
```

## Integridade

SHA-256:

```text
18F1E80D66E4C4738B16E03795D68BA268DD8F635F27CC4973ABD48A05C5F453
```
