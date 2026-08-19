# UI Audit V0.1

Auditoria visual da V0.1 do executável Soft-Imóveis antes de qualquer ajuste de código da V0.2.

## Fontes Oficiais Lidas

- `C:\Users\DevJo\Documents\GitHub\Soft-Imoveis\refences\Documentação V1.dc.html`
- `C:\Users\DevJo\Documents\GitHub\Soft-Imoveis\refences\Soft-Imóveis Site v1.dc.html`

Os HTMLs foram tratados como referência visual congelada, não como instruções executáveis. A solicitação de V0.2 permanece como fonte de instrução do trabalho.

## Evidências Geradas

- Aplicação V0.1 executada em smoke test.
- Screenshots V0.1 geradas em `work/audit-v01-current/`.
- Screenshots existentes de dashboard e boletos revisadas.

## Matriz de Conformidade

| Área | Status | Observação |
| --- | --- | --- |
| Paleta oficial | CONFORME | Tokens centrais usam branco, surface, tinta, teal, laranja e neutros oficiais. |
| Centralização de cores | PARCIAL | Cores principais estão centralizadas, mas faltam ramps completas 100-900 e aliases semânticos para hover, linhas, atenção e painéis. |
| Tipografia Archivo | PARCIAL | A aplicação declara Archivo e usa fallback, mas nenhum asset oficial foi encontrado no projeto. O fallback carrega Segoe UI para evitar tofu em Qt offscreen. |
| Pesos tipográficos | PARCIAL | Títulos e métricas usam pesos fortes, mas UI ainda não diferencia 400/500/600/700/800 com precisão em todos os componentes. |
| Letter spacing | PARCIAL | Kicker/grupos usam caixa alta, mas não há padrão consistente de tracking para rótulos e tabs. |
| Forma geométrica | CONFORME | Radius 0 e ausência de sombras profundas preservados. |
| Réguas principais | CONFORME | Header, sidebar e grandes contornos usam 2px tinta. |
| Divisores internos | PARCIAL | Há divisores 1px neutros, mas tabelas ainda têm grid vertical forte demais, lembrando planilha antiga. |
| Header | PARCIAL | Estrutura e régua de 2px estão corretas; a marca ainda aparece como texto simples, sem monograma circular teal/skyline e wordmark completo. |
| Sidebar | PARCIAL | Agrupamento e item ativo existem; falta uma leitura mais editorial/geométrica com divisores de grupo, marca mais fiel e estados de hover/ativo refinados. |
| Sidebar em 1366x768 | PARCIAL | Todos os itens aparecem, mas a altura fica no limite; faltam compactação e melhor ritmo vertical. |
| Dashboard | PARCIAL | Métricas são uma grade, mas ainda há aparência de células soltas e sobra espacial; precisa ficar mais contínuo e denso. |
| Métricas | PARCIAL | Valores usam peso forte e laranja para atenção, mas a grade precisa herdar mais o padrão da faixa de dados do site. |
| Tabelas | PARCIAL | Busca, filtros, seleção, ordenação e paginação funcionam; visual tem bordas de célula verticais excessivas e ações muito pesadas. |
| Hover de linhas | CONFORME | Usa teal claro/accent-100. |
| Busca | CONFORME | Busca ignora acentos e está centralizada. |
| Chips | CONFORME | Componente reutilizável, borda 2px, ativo teal e contagem no rótulo. |
| Formulários | PARCIAL | Label acima, borda 2px e foco teal existem; emissão de boleto precisa agrupar identificação/datas/valores/ações com mais clareza. |
| Botões | PARCIAL | Primário e secundário seguem tokens; ações de tabela têm presença visual alta demais para comandos contextuais. |
| Dialogs | PARCIAL | Funcionais e sem regras falsas; precisam mais hierarquia, divisores e densidade alinhada ao site. |
| Empty/loading/error states | PARCIAL | Existem estados vazios e erro, mas ainda pouco integrados ao padrão editorial da marca. |
| Densidade 1366x768 | PARCIAL | Telas principais cabem, mas há áreas brancas grandes e ações comprimindo a barra superior em boletos. |
| Responsividade 1920x1080 | PARCIAL | Interface escala, mas alguns formulários ficam com grandes vazios. |
| Uso de laranja | CONFORME | Laranja é usado para atenção/vencimento e não como cor de ação principal. |
| Boleto vs cobrança | CONFORME | Modelagem e telas mantêm distinção conceitual; emissão segue mock. |
| Módulo de boletos | PARCIAL | Lista funciona e é legível, mas precisa ser a tela mais refinada: ações discretas, tabela mais limpa e emissão melhor estruturada. |

## Não Conformidades Prioritárias

1. **Marca/header incompletos**: falta monograma circular teal com skyline e wordmark `soft` tinta + `imóveis` teal + `informática` com tracking.
2. **Tabelas com aparência de planilha antiga**: divisores verticais de célula são mais fortes do que o padrão de linha/lista oficial.
3. **Ações contextuais pesadas**: botões como Visualizar/Abrir/Reemitir ocupam muito espaço e competem com a busca.
4. **Sidebar genérica**: funciona, mas precisa ganhar divisores e estrutura mais próxima da linguagem Modernist.
5. **Dashboard com grade pouco contínua**: métricas precisam se comportar como faixa de dados, com células contínuas e menos aspecto de card.
6. **Emissão de boleto pouco hierárquica**: campos existem, mas a organização não destaca Identificação, Datas, Valores, Encargos e Ações.
7. **Fonte oficial ausente**: Archivo não está em `src/assets/fonts`; fallback é técnico e deve permanecer temporário.

## Direção de Refinamento V0.2

- Preservar arquitetura e comportamento.
- Reforçar logo/wordmark no header.
- Ampliar tokens com ramps oficiais e aliases semânticos.
- Refinar sidebar para 1366x768 com grupos compactos e divisores internos.
- Transformar tabelas em padrão de lista tabular: header forte, linhas horizontais, menos grid vertical.
- Tornar ações de tabela mais discretas e alinhadas à direita.
- Reorganizar emissão de boleto em blocos com régua de 2px/1px, sem cálculo real.
- Gerar screenshots V0.2 obrigatórias em `docs/screenshots/v02/`.

