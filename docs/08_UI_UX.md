Este documento registra o que foi levantado sobre a identidade visual do site atual (softimoveis.com.br/softimoveis/) e a proposta de modernização mantendo essa identidade.

A análise foi feita a partir de um print/PDF enviado pelo Fabio, já que o site bloqueia acesso automatizado (bot detection) — não foi possível inspecionar o HTML/CSS reais, só o resultado visual renderizado.

## Confirmado

**Marca**
- Nome: Soft-Imóveis Informática
- Slogan: "Especialista em soluções de automação para imobiliárias"
- Empresa existe desde 1993 (indicado no rodapé)
- Logo: ícone de prédios/skyline dentro de um círculo teal + wordmark "soft" (preto) + "imóveis" (teal) + "informática" (cinza, letras espaçadas, abaixo do wordmark principal)

**Paleta de cores (extraída por amostragem de pixel do print, não é suposição)**
- Teal principal: `#007E8F` (texto "imóveis" da logo, fundo dos botões de menu)
- Laranja de destaque: `#FF9900` (título "Bem vindo!")
- Preto: `#000000` (texto "soft" da logo, textos fortes)
- Cinza secundário: `#ABABAB` (tagline, texto de apoio)
- Fundo branco

**Estrutura da home (única página confirmada até agora)**
- Header: logo à esquerda, tagline à direita
- Menu de navegação vertical fixo à direita, 8 itens: EMPRESA, PRODUTOS E SOLUÇÕES, PARCEIROS, CLIENTES, CONTATO, ATUALIZAÇÕES, SUPORTE TÉCNICO, INFORMATIVOS (cada um com ícone de seta ">")
- Banner full-width com foto de skyline de cidade (stock photo)
- Bloco "Bem vindo!" com foto de aperto de mão (stock photo) + texto institucional
- Caixa lateral "Últimas Notícias" com itens sobre COVID-19 e DIMOB
- Rodapé: copyright "Desde 1993" + link "Privacidade e termos legais"
- Tipografia: sans-serif genérica (aparência de Arial/Helvetica), sem indício de fonte customizada

## Inferido (não confirmado, mas provável)

- O layout parece ter largura fixa pensada pra telas antigas — sobra muito espaço em branco nas laterais em telas modernas, o que sugere que não é responsivo
- O site provavelmente não foi atualizado desde a pandemia (conteúdo de COVID-19 ainda ativo na área de notícias em 2026)
- As outras 7 seções do menu (EMPRESA, PRODUTOS E SOLUÇÕES etc.) devem seguir o mesmo padrão visual da home, mas isso não foi verificado

## Desconhecido

- Conteúdo real das outras 7 páginas do menu
- Se existe versão mobile ou é só desktop
- Se a empresa tem o logo em arquivo vetorial (svg/ai) ou só em raster
- Fonte exata usada (nome da família tipográfica)
- Se há CMS por trás do site ou é HTML estático
- Se o link "Privacidade e termos legais" leva a uma página real com conteúdo válido (LGPD)

## Proposta de modernização mantendo identidade visual

Ideia: manter os elementos que carregam a marca (teal `#007E8F`, laranja `#FF9900`, o wordmark, o conceito de banner com skyline) mas resolver os problemas estruturais:

- Layout responsivo (mobile-first), abandonando a largura fixa
- Menu lateral fixo → navegação horizontal no topo (ou menu hambúrguer no mobile), mantendo os mesmos 8 itens e as mesmas cores dos botões
- Tipografia web moderna (ex. Inter, ou outra sans-serif atual) no lugar da sans-serif genérica
- Substituir stock photos genéricas por imagens mais alinhadas ao negócio real da empresa (ou manter o conceito skyline, mas em resolução/qualidade atual)
- "Últimas Notícias" passa a ser um bloco dinâmico de verdade (ou é removido, se não for mantido pela equipe)
- Manter o "Desde 1993" — é um sinal de confiança que vale a pena reforçar visualmente, não esconder

## Perguntas para o Fabio / cliente

- Podemos ver as outras 7 páginas do menu (print ou PDF, mesmo processo desta)?
- Existe arquivo original do logo (vetor)?
- As notícias/atualizações precisam continuar existindo, ou podemos simplificar essa seção?
- Existe conteúdo de "Produtos e Soluções" que precisa ser migrado com fidelidade (é provavelmente onde fica a descrição do sistema de gestão imobiliária que este projeto vai substituir)?