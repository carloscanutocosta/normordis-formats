# Exemplo — liquidação de IRS gerada automaticamente

Pacote `.ndfpkg` descomprimido, com um documento **gerado por sistema
determinístico, sem autor humano material**. Demonstra, num só artefacto, as
quatro alterações estruturais introduzidas em 2026-08-13.

```bash
python3 tools/validate.py --package specs/ndf/examples/liquidacao-irs-automatica
```

## O que este exemplo demonstra

### 1. Proveniência de sistema (§2.14)

`proveniencia_sistema` tem **duas entradas** — motor de cálculo e emissor de
notificações — ordenadas cronologicamente por `gerado_em`. A ordem é normativa
(§2.14.3): JCS preserva a ordem dos arrays, logo entra no `payload_hash`.

A primeira entrada traz `regra_ref`, apontando para as tabelas de retenção
aplicadas. É uma referência externa com hash, não uma cópia: o NDF identifica
a regra, não a incorpora.

### 2. Imputação jurídica (§2.15)

Não há autor humano, mas há responsável. `imputacao` identifica o órgão que
responde pelo ato e o título ao abrigo do qual o pratica — aqui, `delegacao`,
com `fundamento.publicacao_ref` a identificar o despacho publicado em Diário
da República. É a menção que o CPA (art. 151.º, n.º 1, al. a)) torna
obrigatória e que o CPPT (art. 36.º, n.º 2) exige na notificação.

Repare-se na separação entre três coisas que costumam ser confundidas:

| Campo | Valor neste exemplo | Papel |
|---|---|---|
| `metadados.entidade_produtora` | Autoridade Tributária e Aduaneira | pessoa coletiva, para efeitos arquivísticos |
| `imputacao[].imputado` | Diretor de Serviços do IRS | órgão que responde juridicamente |
| `proveniencia_sistema[].sistema` | Sistema de Liquidação de IRS 2026.4.17 | o que produziu o conteúdo |

### 3. Invariante de origem (§2.2.1)

`participantes` está **legitimamente ausente** — ninguém escreveu este
documento. O invariante é satisfeito por `proveniencia_sistema`, e nenhum
autor humano é fabricado para o cumprir.

### 4. Tipo documental por namespace de entidade (§2.9.5)

`tipo_documento_ref` é `ext.at.liquidacao-irs@2026.1` — um tipo de domínio,
definido e mantido pela entidade produtora, **fora do registo canónico**. O
registo NORMORDIS reserva-se a formas documentais transversais; manter
centralmente `liquidacao-irs`, `liquidacao-iva`, `liquidacao-imi` e as
notificações correspondentes, para cada organismo, produziria um número
indeterminado de tipos impossível de manter (ADR-014).

O que torna isto seguro é o schema viajar no pacote, em
`schemas/ext.at.liquidacao-irs.schema.json`. Um verificador independente —
em qualquer linguagem — valida `documento` sem acesso a registo nenhum.

Para confirmar que a resolução é real e não silenciosa, remova esse ficheiro
e volte a validar: o pacote passa a ser rejeitado (`NDF-PKG-007`).

## Notas

- `nivel_assinatura` é `"nenhuma"`: uma liquidação automática não é assinada
  com CAdES. Isso **não** a torna não imputável — ver §2.15.4.
- O NDT incluído reutiliza um layout genérico, com identidade própria
  (`liquidacao-irs@2026.1`). Serve para o pacote ser autocontido e validável;
  não pretende representar o grafismo real de uma liquidação.
- Valores, números de liquidação, NIF e referências de despacho são
  fictícios.
