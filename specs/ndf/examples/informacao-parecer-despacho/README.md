# Exemplo — Informação → Parecer → Despacho

Três documentos NDF autónomos, cada um com o seu `ndf_id`, conteúdo,
assinatura(s) e avaliação arquivística próprios, ligados por `relacoes[]`
verificáveis (SPEC.md §2.11) — não um único documento com secções
sucessivamente assinadas.

```text
01-informacao-tecnica (IT/2026/00045)
    │
    └── 02-parecer (PAR/2026/00012) — emite_parecer_sobre → 01
              │
              └── 03-despacho (DESP/2026/00089) — decide_sobre    → 02
                                                 — referencia      → 01
```

Cada seta é uma entrada em `relacoes[]` no NDF-core do documento de origem,
contendo `tipo`, `alvo.ndf_id` **e** `alvo.payload_hash` — não apenas uma
referência lógica, mas o hash exato do conteúdo canónico apreciado no
momento em que a relação foi estabelecida.

## Conteúdo de cada pasta

Cada pasta contém um par `ndf-core.json` (bytes canónicos JCS/RFC 8785 —
`payload_bytes` tal como produzidos pelo pipeline de finalização, §5.2) e
`envelope.json` (assinaturas, timestamps e material de validação — não
canonicalizado). Não são pacotes `.ndfpkg` completos (sem NDT, recursos nem
manifesto) — o objetivo aqui é ilustrar o grafo de relações e o modelo de
assinatura, não a portabilidade completa (para isso, ver
`specs/ndf/examples/ndfpkg-example/`).

| # | Documento | `tipo_documento_ref` | `ndf_id` | `payload_hash` |
|---|---|---|---|---|
| 01 | Informação Técnica IT/2026/00045 | `informacao-tecnica@1.0.0` | `b55c4eaa-6fb0-4024-8317-3a4a5eedccbd` | `sha256:fa4b0a248cd1141488d37712610bb38daf25d6fea98f798e9bb13eda2a6bc8e8` |
| 02 | Parecer PAR/2026/00012 | `parecer@1.0.0` | `8e234253-b404-4aeb-80f0-f456e6d17e88` | `sha256:4e8c3e0faea8f0324f794e50bd9b714b35da6a7ae5b0ede6dcf535578a3a8d1f` |
| 03 | Despacho DESP/2026/00089 | `despacho@1.0.0` | `b82c82a4-d1ac-490a-8103-a47580ee651c` | `sha256:08cca747bc47d2181b85e8d99475cd6dd3f16f8d6ff49e84ab0502260523856e` |

Os `payload_hash` acima foram calculados a partir dos bytes reais de cada
`ndf-core.json` (canonicalização RFC 8785 via `rfc8785`, a mesma biblioteca
usada por `tools/canonicalize.py`) — não são valores fabricados. Qualquer
implementação conforme pode confirmá-los recalculando `SHA-256(ndf-core.json)`
sobre os bytes exatos do ficheiro.

## O que este exemplo demonstra

- **Documentos autónomos, não secções assinadas em conjunto** (§3 da missão
  de estabilização): três `ndf_id`, três `payload_hash`, três blocos
  `avaliacao` e `participantes` distintos.
- **Relações assinadas e verificáveis por hash** (§2.11): `relacoes[]` está
  dentro do NDF-core de cada documento — cobertas pela mesma assinatura que
  protege o conteúdo, não apenas registadas no envelope.
- **Reconciliação com `despacho.sobre[]`**: o despacho (03) preenche tanto
  `relacoes[]` (mecanismo genérico) como `documento.sobre[]` (campo de
  conveniência específico do tipo), com o mesmo conjunto de `ndf_id` e
  `payload_hash` em ambos — consistente com SPEC.md §2.11.4.
- **Múltiplas assinaturas autocontidas** (§4.4): o despacho (03) tem duas
  assinaturas independentes — uma pessoal qualificada (`papel: "decisor"`) e
  um selo institucional (`papel: "selante"`) — cada uma com o seu
  `assinatura_id`, `timestamps` e `validation_material` próprios.
- **Proveniência de IA** (§2.13): o parecer (02) foi redigido com apoio de um
  sistema de IA (`finalidade: "apoio_redacao"`) e revisto por um humano antes
  de aprovação (`revisao_humana.estado: "revisto_e_aprovado"`) — a informação
  (01) e o despacho (03) declaram `proveniencia_ia.utilizada: false`.
- **Participantes distintos de signatários** (§2.12): cada documento regista
  `participantes[]` (autor, revisor humano, decisor) independentemente de
  quem assina no envelope.

## Nota sobre as assinaturas e certificados

Os valores `cades_b_lta`, `timestamps` e `validation_material` são
*placeholders* ilustrativos — não são assinaturas CAdES-B-LTA reais. O gate
de fixtures CAdES reais permanece pendente e está identificado como tal em
`docs/normalization/READINESS.md`; este exemplo não o antecipa nem o declara
concluído.

## Verificação

```bash
python3 tools/validate.py specs/ndf/examples/informacao-parecer-despacho/01-informacao-tecnica/ndf-core.json
python3 tools/validate.py specs/ndf/examples/informacao-parecer-despacho/02-parecer/ndf-core.json
python3 tools/validate.py specs/ndf/examples/informacao-parecer-despacho/03-despacho/ndf-core.json
```

Cada `ndf-core.json` valida de forma independente contra
`specs/ndf/schemas/ndf-core.schema.json` e contra o schema do respetivo tipo
de documento em `specs/registry/schemas/`.
