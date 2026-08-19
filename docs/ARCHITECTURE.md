# Arquitetura

## Objetivo

Criar uma aplicação desktop Python/PySide6 modular, testável e preparada para evolução gradual sem acoplar a interface ao legado ou a um banco definitivo.

## Camadas

```text
UI
Application
Domain
Infrastructure
Persistence
Integrations
```

## Responsabilidades

- `src/ui`: shell desktop, páginas, dialogs, widgets, modelos Qt e QSS.
- `src/application`: DTOs, navegação, serviços de tela e dados demonstrativos.
- `src/domain`: entidades, repository protocols e serviços de domínio.
- `src/infrastructure`: implementação in-memory atual e futuras integrações/persistência.
- `src/core`: configuração, paths, logging, exceções, busca e formatters.

## Dependências

O fluxo permitido é descendente:

```text
UI -> Application -> Domain -> Repository Protocol -> Infrastructure
```

Widgets não executam SQL e não contêm regra financeira. Cálculos desconhecidos ficam atrás de `ChargeCalculationService`.

## Estado

`AppState` mantém sessão mock e rota atual. Futuramente poderá receber usuário, empresa, permissões e configurações sem virar variável global ampla.

## Persistência

Esta fase usa `InMemoryRepository`. A direção futura preferencial é API Python/FastAPI com PostgreSQL, sem acoplar PySide6 diretamente ao banco.

## Integrações

`BankingProvider`, `BoletoIssuer`, `RemittanceService` e `ReturnFileService` são apenas contratos preparatórios. Nenhuma integração real foi implementada.

