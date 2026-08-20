# ADR-021: Componentes binários declarados nos bytes assinados

**Estado**: Aceite
**Data**: 2026-08-20
**Decisores**: carloscanutocosta

---

## Contexto

Um documento capturado (ADR-020) tem o seu conteúdo num ou mais ficheiros
binários: o PDF/A emitido pelo produtor, o original recebido de terceiro, os
anexos de apoio, o material de validação de assinaturas externas. O formato tem
de saber **que componentes constituem aquele documento**, com que papel, que
tipo MIME, que dimensão e que hash.

A questão é onde essa declaração vive. O desenho preliminar propôs
sucessivamente dois lugares: um campo `payload_ref` no **envelope**, e depois
`components[]`/`resources[]` no **`manifest.json`**.

## Decisão

Os componentes são declarados em **`documento`**, através do schema do tipo
documental — nunca no envelope, nunca no manifesto.

```json
{
  "documento": {
    "componentes": [
      {
        "id": "principal",
        "papel": "original",
        "media_type": "application/pdf",
        "sha256": "sha256:…",
        "tamanho": 352991,
        "nome_original": "parecer.pdf"
      }
    ]
  }
}
```

Uma entrada de componente **NÃO DEVE** conter referência de armazenamento: nem
URI, nem bucket, nem nome de adapter, nem qualquer identificador que dependa da
infraestrutura que custodia o objeto hoje.

O `manifest.json` **não muda**.

## Alternativas consideradas

### `payload_ref` no envelope

A assinatura CAdES é *detached* sobre os `payload_bytes`, que são os bytes JCS
do NDF-core e apenas esses (SPEC §5.2, passos 1 e 4). O envelope **contém** a
assinatura; não é coberto por ela. Um campo de componentes no envelope seria um
campo não assinado.

### `components[]` no `manifest.json`

Falha pela mesma razão, e ainda por uma segunda: SPEC §8.3 declara que o
manifesto é inventário físico do pacote e **NÃO DEVE duplicar informação
documental do NDF-core**. Papel, identidade e tipo de um componente são
informação documental.

### Primitiva nova no NDF-core

Falha o passo 2 do teste de admissão ([`ROADMAP.md`](../../ROADMAP.md)): o que
cabe em `documento` via schema do tipo tem aí o seu lugar.

## Justificação da decisão

**Num documento capturado, o binário é o documento.** Se o seu `sha256` viver
apenas no manifesto, substituir o ficheiro e regerar o manifesto produz um
pacote que passa em toda a validação existente — a assinatura continua válida,
porque assina outra coisa. A promessa de preservação ficaria sem fundamento
criptográfico.

Declarado em `documento`, o hash entra nos `payload_bytes`, é canonicalizado por
JCS e fica coberto pela assinatura e pelo timestamp de arquivo. O conteúdo não
está dentro dos bytes assinados, mas fica **amarrado a eles pelo hash**. É isto
que torna as duas vias de ADR-020 equivalentes em prova.

**O manifesto não precisa de mudar** porque já faz o seu trabalho. A composição
do pacote exige que todo o ficheiro presente esteja inventariado com hash
correto, e o vetor `PKG-NEG-002` rejeita ficheiros não inventariados. A
integridade física de um binário em `original/` já está coberta. O que faltava
era a declaração documental — e essa é matéria de `documento`.

A junta verificável nova, e única, é a **coerência entre
`documento.componentes[].sha256` e `manifest.inventario`**.

**Quanto à referência de armazenamento:** um formato aberto que transporte
`"storage": "minio://…"` amarra o documento à infraestrutura que o custodia
hoje, e contradiz a razão de ser de uma especificação disponibilizada em CC0
para que qualquer fornecedor a implemente. O formato sabe o quê, qual o papel,
qual o tipo MIME, qual a dimensão e qual o hash; onde o objeto reside é decisão
de implementação do repositório, e o hash é chave suficiente para o resolver.

## Consequências

**Positivas**: a preservação de um documento capturado passa a ter o mesmo
fundamento criptográfico que a de um documento nativo; o manifesto mantém-se
como inventário físico puro, sem sobreposição de responsabilidades; a separação
entre formato e infraestrutura fica preservada.

**Negativas / mitigações**: a informação de componente aparece em dois sítios —
declaração em `documento`, presença física no inventário. Não é duplicação de
responsabilidade (uma é documental e assinada, a outra é física e do pacote),
mas exige um requisito de coerência entre as duas, sem o qual poderiam
divergir. Esse requisito é `NDF-PKG-010`, com vetor negativo próprio.

## Referências

- SPEC.md §5.2 (pipeline de finalização), §8.1 (composição), §8.3 (garantias do pacote)
- [`tools/validate.py`](../../tools/validate.py) — verificação de inventário fechado
- `conformance/package/` — `PKG-NEG-002`
- [`docs/design/NDFPKG-CAPTURA-E-INGESTAO.md`](../design/NDFPKG-CAPTURA-E-INGESTAO.md) §4
- ADR-020 (um formato, duas realidades)
