# Perfil `nl-na` — Países Baixos

**Estado:** documentado. Schema não publicado.
**Autoridade:** Nationaal Archief.
**Fontes verificadas em:** 2026-08-15.

---

## 1. Base jurídica primária

| Instrumento | Conteúdo relevante |
|---|---|
| **Archiefwet 1995** | Cada `zorgdrager` elabora `selectielijsten` que indicam, no mínimo, quais os documentos destinados a destruição. As listas ministeriais são formalmente aprovadas e publicadas na *Staatscourant*. |
| **Archiefbesluit 1995, art. 5** | Uma `selectielijst` contém *"een systematische opsomming van categorieën archiefbescheiden, waarin bij iedere categorie is aangegeven of de archiefbescheiden bewaard worden dan wel na welke termijn zij voor vernietiging in aanmerking komen"* — uma enumeração sistemática de categorias, indicando **para cada categoria** se os documentos são conservados ou após que prazo são elegíveis para destruição. Exige ainda uma exposição de motivos, incluindo os critérios pelos quais o `zorgdrager` pode excecionar documentos da destruição. |

Sem `selectielijst` formalmente aprovada, um organismo público **não pode**
proceder à destruição nem à transferência.

## 2. Modelo arquivístico

```
selectielijst (aprovada e publicada)
   │
   ├── categoria
   │      ├── waardering: blijvend te bewaren  → conservação permanente
   │      └── waardering: te vernietigen + bewaartermijn
   │
   └── critérios de exceção (hotspots)
```

O artigo 5 mapeia quase 1:1 para a estrutura do NDF: enumeração de categorias,
com prazo e destino por categoria. É, dos cinco regimes analisados, o mais
próximo da forma do bloco `avaliacao`.

## 3. Mapeamento NDF

| NDF | Países Baixos |
|---|---|
| `perfil` | `nl-na` |
| `classificacao_ref` | categoria da `selectielijst` |
| `instrumento_ref` | `selectielijst` formalmente aprovada, com referência da publicação em *Staatscourant* |
| `prazo_conservacao` | bewaartermijn |
| `forma_contagem` | facto desencadeador fixado na lista |
| `destino_final` | `conservacao_permanente` ← *blijvend te bewaren*; `eliminacao` ← *te vernietigen* |
| `autoridade_avaliacao` | apenas quando a apreciação seja diferida |

**Hotspots.** Documentação que a lista tornaria eliminável pode ser excecionada
para conservação, ao abrigo dos critérios previstos no art. 5. No NDF isto não
exige mecanismo novo: o documento declara o destino efetivamente aplicável e
identifica em `instrumento_ref` a decisão que o determina. A rastreabilidade
vem de o instrumento ser nomeado, não de o NDF modelar a exceção.

**Valores de `waardering` sem correspondência direta.** O vocabulário MDTO do
Nationaal Archief inclui `voorlopig te bewaren` e `nader te bepalen`. Ambos
correspondem a `destino_final: "a_determinar"` no NDF, com
`autoridade_avaliacao` a identificar quem decide. Foi um dos dois casos que
motivaram essa primitiva — o outro é o alemão, ver [`de-barch.md`](de-barch.md).

## 4. O que um schema `nl-na` poderia impor

- fixar `perfil` em `nl-na`;
- exigir `instrumento_ref` não vazio, com recomendação de referenciar a
  publicação em *Staatscourant* e não apenas o nome corrente da lista.

Não foi encontrada evidência de um esquema de codificação nacional único para as
categorias das `selectielijsten`: cada lista aprovada define a sua própria
enumeração. Impor sintaxe seria inventar uma uniformidade que o regime não tem.

## 5. Limitações

- A relação entre `selectielijst` e MDTO (o esquema de metadados do Nationaal
  Archief) não foi analisada. Um mapeamento NDF↔MDTO seria trabalho autónomo e
  potencialmente valioso, por MDTO ser o análogo neerlandês mais próximo do NDF
  no plano dos metadados.
- A Archiefwet foi objeto de revisão legislativa; as fontes consultadas são as
  versões consolidadas em vigor na data indicada. Reverificar antes de qualquer
  transição para perfil registado.

## 6. Fontes

- [Archiefwet 1995 — wetten.overheid.nl](https://wetten.overheid.nl/BWBR0007376)
- [Archiefbesluit 1995, art. 5 — wetten.overheid.nl](https://wetten.overheid.nl/BWBR0007748)
- [Nationaal Archief — MDTO, `waardering`](https://www.nationaalarchief.nl/archiveren/mdto/waardering)
- [Inspectie Overheidsinformatie en Erfgoed — selectie en vernietiging](https://www.inspectie-oe.nl/onderwerpen/selectie-en-vernietiging)
