# Soft-Imóveis Desktop

Fundação funcional do novo executável de gestão imobiliária da Soft-Imóveis, refinada visualmente na V0.2.

## Quick Start

```powershell
cd "C:\Users\DevJo\Documents\GitHub\Soft-Imoveis"

python -m venv .venv

.\.venv\Scripts\python.exe -m pip install -r requirements.txt

.\run-dev.ps1
```

O repositório oficial acima é a fonte canônica do projeto. Desenvolvimento, testes, documentação e builds devem ser feitos a partir dele.

## Visão Geral

Aplicação desktop Windows em Python 3.12+ com PySide6/Qt Widgets, QSS centralizado, dados mockados e arquitetura preparada para banco, API, integrações bancárias e migração futura do sistema legado.

O objetivo desta fase é entregar um programa navegável e testável, não uma cópia visual do ADMINISTRARE at immobilis.

## Stack

- Python 3.12+
- PySide6 / Qt Widgets
- QSS
- pytest
- PyInstaller

## Pré-Requisitos

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Se o Python do projeto estiver em outro local, informe o executável explicitamente:

```powershell
$env:SOFTIMOVEIS_PYTHON = "C:\caminho\para\python.exe"
```

Não versione `.venv`, certificados, senhas, tokens, PFX ou segredos de CI.

## Desenvolvimento

```powershell
.\run-dev.ps1
```

O fluxo oficial de desenvolvimento executa a aplicação via Python. Ele não depende de executar o EXE não assinado, portanto continua utilizável em máquinas com Smart App Control ativo.

Também é possível executar smoke test sem manter a janela aberta:

```powershell
.\run-dev.ps1 -SmokeTest
```

## Testes

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Build Local

```powershell
.\build.ps1
```

O build local é uma **Development Build**:

```text
Python -> Tests -> PyInstaller -> Dev Build
```

Ele usa PyInstaller em modo `onedir` por estabilidade e melhor diagnóstico de assets Qt. O script valida Python, dependências, testes, artefatos produzidos, Authenticode e metadata, mas não executa automaticamente um EXE `NotSigned`.

Resultado esperado:

```text
dist/
└── SoftImoveis/
    └── SoftImoveis.exe
```

Uma build local não assinada pode ser bloqueada pelo Windows 11 Smart App Control / Device Guard. Isso não é bug da aplicação.

## Release

```powershell
.\release.ps1
```

O pipeline de release é separado da build local:

```text
Python -> Tests -> PyInstaller -> Authenticode -> Timestamp -> Verification -> Smoke Test -> Release
```

Uma release destinada à distribuição deve utilizar assinatura Authenticode confiável. Sem certificado configurado, `release.ps1` cancela com mensagem clara depois de gerar a build de desenvolvimento.

Variáveis de ambiente aceitas pelo pipeline:

```text
SOFTIMOVEIS_SIGN_ENABLED=1
SOFTIMOVEIS_CERT_THUMBPRINT=<thumbprint no certificate store>
SOFTIMOVEIS_TIMESTAMP_URL=<RFC3161 timestamp URL>
SOFTIMOVEIS_SIGNTOOL_PATH=<caminho opcional para signtool.exe>
SOFTIMOVEIS_PFX_PATH=<caminho opcional para .pfx>
SOFTIMOVEIS_PFX_PASSWORD=<senha fornecida por secret/env, nunca versionada>
```

Prefira certificate store ou segredo de CI. Não coloque senha, token, PFX ou API key no repositório.

Auditoria de assinaturas:

```powershell
.\scripts\audit-signatures.ps1
```

Diagnóstico somente leitura do App Control:

```powershell
.\scripts\check-app-control.ps1
```

## Estrutura

```text
src/
├── app/              bootstrap, estado e roteamento
├── core/             configuração, paths, logging, formatters e busca
├── domain/           entidades, repositories e services de domínio
├── application/      DTOs, navegação e dados demonstrativos
├── infrastructure/   repositórios in-memory e pontos futuros
├── ui/               shell, páginas, widgets, dialogs, models e QSS
└── assets/           ícones SVG e futura tipografia
scripts/              pipeline, assinatura e auditoria de distribuição
```

## Arquitetura

Fluxo previsto:

```text
UI
↓
Application Service / Use Case
↓
Domain Service
↓
Repository Protocol
↓
Infrastructure
```

A UI não executa SQL nem conhece persistência definitiva. Regras financeiras desconhecidas permanecem atrás de protocols/services.

## Design System

Tokens de cor, tipografia e métricas estão em `src/ui/styles/tokens.py`; o QSS é gerado em `src/ui/styles/stylesheet.py`.

Observação de auditoria V0.2: os arquivos `Documentação V1.dc.html` e `Soft-Imóveis Site v1.dc.html` foram lidos como fontes oficiais de identidade visual. Tokens, sidebar, tabelas, métricas, filtros e formulários foram refinados para seguir esse sistema.

## Dados Mockados

Todos os dados são fictícios e marcados conceitualmente como `DEMO DATA`. Não há dados reais da imobiliária nem gravação em legado.

## Limitações

- Sem banco definitivo.
- Sem autenticação real.
- Sem regras reais de multa, juros, correção, baixas ou repasses.
- Sem integração bancária, CNAB, remessa ou retorno.
- Sem migração do Immobilis.

## Próximos Passos

1. Importar os arquivos oficiais da fonte Archivo.
2. Fazer reunião de descoberta operacional.
3. Mapear banco/arquivos do legado apenas em modo leitura.
4. Validar regras de cobrança, boleto, baixa e repasse.
5. Definir API futura e persistência.
