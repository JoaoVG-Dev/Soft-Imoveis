# Legacy Notes

## Confirmado pelo briefing

- Sistema atual identificado: `ADMINISTRARE at immobilis`.
- Aplicação desktop Windows.
- Rotinas de administração de imóveis, locadores, locatários, contratos, cobranças, boletos, recebimentos, baixas, repasses e relatórios.
- Instalação semelhante a `C:\Immobilis\`.
- Uso aparente de arquivos em servidor de rede semelhante a `\\LOCAR-SERVER\C\Immobilis\`.

## Hipóteses

- Arquitetura antiga baseada em arquivos compartilhados.
- Existência de tabelas/arquivos relacionados a boleto, baixa e fluxo financeiro.
- Necessidade futura de leitura legado -> transformação -> validação -> novo banco.

## Restrições

- Nenhum arquivo do Immobilis deve ser modificado.
- Nenhum script desta fase grava em produção.
- Migração não foi implementada.

