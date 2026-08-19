# Domain Draft

## Entidades Provisórias

- `Landlord / Locador`
- `Tenant / Locatário`
- `Property / Imóvel`
- `Contract / Contrato`
- `Charge / Cobrança`
- `Boleto`
- `Payment / Pagamento`
- `Settlement / Baixa`
- `BankAccount / Conta Bancária`
- `Transfer / Repasse`

## Separações Conceituais

```text
Cobrança != Boleto != Pagamento != Baixa != Repasse
```

## Fluxo Estrutural Preparado

```text
Locador -> Imóvel -> Contrato -> Cobrança -> Boleto -> Pagamento -> Baixa -> Repasse -> Prestação de Contas
```

## Não Confirmado

- Regras de multa, juros e correção.
- Carteira, convênio, banco, CNAB, remessa e retorno.
- Regras de baixa e repasse.
- Schema do banco legado.
- Permissões e auditoria definitiva.

