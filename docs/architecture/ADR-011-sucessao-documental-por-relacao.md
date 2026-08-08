# ADR-011: Sucessão documental exclusivamente por `relacoes[substitui]`

**Estado**: Aceite
**Data**: 2026-08-08
**Decisores**: carloscanutocosta

---

## Contexto

Até esta decisão, o NDF tinha **dois mecanismos distintos** para representar
o mesmo facto — que um documento sucede a outro:

| | `versao_anterior`/`hash_anterior` | `relacoes[{tipo:"substitui"}]` |
|---|---|---|
| Localização | envelope | NDF-core |
| Coberto pela assinatura | **não** | sim |
| Liga a bytes exatos | sim (`hash_anterior`) | sim (`alvo.payload_hash`) |
| Cardinalidade | linear 1:1 | array, N antecedentes |
| Generaliza a outras relações | não | sim (11 tipos + extensões) |
| Cobertura de teste | **nenhuma** | 3 casos de conformidade |

A revisão pré-RC (`docs/reports/NDF-PRE-RC-REVIEW.md`) documentou três
consequências concretas desta duplicação:

- **F3**: §8.3 e §2.3 afirmavam que o `manifest.json` regista
  `versao_anterior`/`hash_anterior`, mas `manifest.schema.json` tem
  `additionalProperties: false` e não declara nenhum dos dois — garantia
  impossível de implementar de forma conforme.
- **F6**: §6.2 exigia (**DEVEM**) os campos do envelope, enquanto §2.11.3
  apenas **RECOMENDA-SE** a relação equivalente no core. O mecanismo *não
  assinado* era obrigatório e o *assinado* opcional — o inverso da
  fundamentação da ADR-002.
- **F8**: o mecanismo do envelope nunca foi exercitado por nenhum caso de
  conformidade. `conformance/ndf/valid/versao-substituicao.json` é apenas um
  NDF-core, sem envelope; o `_comment` descrevia em prosa o que o envelope
  *conteria*.

## Decisão

**Remover `versao_anterior` e `hash_anterior` do envelope.** A sucessão
documental passa a ser representada exclusivamente por
`relacoes[{tipo: "substitui"}]` no NDF-core, coberta pela assinatura.

```json
{
  "relacoes": [
    {
      "tipo": "substitui",
      "alvo": {
        "ndf_id": "<ndf_id do documento substituído>",
        "payload_hash": "<payload_hash do documento substituído>"
      }
    }
  ]
}
```

### Enquadramento conceptual que acompanha a decisão

Substituição **não é versionamento interno de um documento**; é uma
**relação entre dois documentos NDF autónomos e imutáveis**:

```text
A continua a existir, imutável
B substitui A
```

e não:

```text
A passou a ser B
```

Isto é coerente com o princípio de imutabilidade (§2.1) e com a ADR-003
(documentos autónomos). `substitui` deixa de ter estatuto especial: é uma
relação semântica como as outras, sem infraestrutura paralela própria.

## Alternativas consideradas

### Manter os dois mecanismos e corrigir as inconsistências

Exigiria: acrescentar `versao_anterior`/`hash_anterior` ao
`manifest.schema.json` (F3), inverter a hierarquia normativa para tornar o
core obrigatório (F6), e criar cobertura de teste para o mecanismo do
envelope (F8).

**Rejeitado.** Mantém dois sítios para o mesmo facto, com o custo permanente
de os manter coerentes, e enriquece o manifesto com informação documental —
contra o princípio de que o manifesto é inventário físico do pacote, não uma
segunda representação semântica do NDF (ver Consequências).

### Manter `versao_anterior` como projeção derivada, com o core a prevalecer

Declarar normativamente que o campo do envelope é uma projeção de
`relacoes[substitui]` e que, havendo divergência, o core prevalece.

**Rejeitado.** É a opção que menos altera artefactos, mas obriga todos os
implementadores a conhecer duas representações e uma regra de precedência,
para não ganhar nenhuma capacidade nova. A duplicação continuaria a existir,
apenas documentada.

## Justificação da decisão

Um facto, um sítio, preferencialmente coberto pela assinatura — o mesmo
princípio já aplicado em toda a revisão anterior. O mecanismo que sobrevive
é estritamente mais capaz do que o removido: assinado, verificável por hash,
com múltiplos antecedentes, e já testado.

A remoção é possível sem custo de compatibilidade porque não existem
consumidores externos do formato (confirmado antes da ADR-007 e reconfirmado
na ADR-009).

## Consequências

**Positivas**:
- Elimina F3, F6 e F8 numa única alteração.
- A cadeia de sucessão passa a ser reconstruível a partir dos **bytes
  assinados** de cada `ndf-core.json`, sem depender de metadados de envelope
  ou de manifesto.
- Reforça a separação de responsabilidades entre os três artefactos:

```text
ndf-core   = verdade documental (inclui relações)
envelope   = prova criptográfica
manifest   = inventário físico do pacote
```

O manifesto **não** deve ser enriquecido com informação documental: quanto
mais semântica for duplicada nele, mais superfície existe para divergir do
core.

**Negativas / mitigações**:
- Remoção de dois campos de um schema publicado — alteração incompatível em
  abstrato, sem impacto real por ausência de consumidores externos.
- Um sistema que só precise de sucessão linear simples passa a ter de
  preencher `relacoes[]` no core, ligeiramente mais verboso que dois campos
  no envelope. Aceite: é o preço de a relação ficar assinada.

## Referências

- `docs/reports/NDF-PRE-RC-REVIEW.md` — F3, F6, F8, F9
- ADR-002 (relações no core), ADR-003 (documentos autónomos)
- ADR-007, ADR-009 (ausência de consumidores externos)
- SPEC.md §2.11, §6
