# Design System

## Auditoria Visual

A V0.2 foi refinada a partir da auditoria em `docs/UI_AUDIT_V01.md`, usando como fonte de verdade visual:

- `C:\Users\DevJo\Documents\GitHub\Soft-Imoveis\refences\Documentação V1.dc.html`
- `C:\Users\DevJo\Documents\GitHub\Soft-Imoveis\refences\Soft-Imóveis Site v1.dc.html`

## Paleta

Tokens centralizados em `src/ui/styles/tokens.py`:

- Background `#FFFFFF`
- Surface `#F2F5F6`
- Text `#14181C`
- Teal principal `#007E8F`
- Teal hover `#006C7B`
- Teal texto `#005965`
- Teal claro `#E6F2F4`
- Teal escuro `#002E34`
- Orange `#FF9900`
- Orange escuro `#B56B00`
- Neutros `#E9EDED`, `#D4DADB`, `#B3BCBE`, `#8D9799`, `#6F7A7D`, `#555F61`, `#14181C`

## Tipografia

Fonte principal: Archivo. A aplicação tenta carregar `src/assets/fonts/*.ttf` e usa fallback do sistema quando não existir. Os assets oficiais Archivo não foram localizados no workspace nesta etapa e permanecem registrados em `docs/TODO_DISCOVERY.md`.

## Forma

- Raio 0.
- Divisor principal de 2px.
- Divisores internos de 1px.
- Sem glassmorphism, gradientes, sombras profundas ou cards arredondados.
- Tabelas densas com header separado, divisores neutros de 1px, sem grade vertical pesada e hover teal claro.

## Componentes

- Sidebar geométrica com grupos, divisores, marca Soft-Imóveis, item ativo em teal e hover teal claro.
- Grid de métricas como faixa contínua, sem cards flutuantes.
- `SearchableTable` com busca, filtros, ordenação, paginação, seleção, hover e empty state.
- `FilterChip` com estado ativo teal.
- `FormField` com label sempre visível, borda 2px e foco teal.
- Dialogs objetivos para detalhe e emissão mock de boleto, com seções formais e campos label-acima.

## Acessibilidade

Prioridade para 1366x768: labels visíveis, contraste alto, navegação por teclado nativa do Qt, botões com texto claro e tabelas com seleção de linha.
