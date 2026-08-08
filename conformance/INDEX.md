# Índice de casos de conformidade

Este ficheiro é gerado por `tools/build_conformance_index.py`. Não deve ser
editado manualmente. A definição normativa de conformidade está em
`specs/ndf/SPEC.md` §9.

## NDF

### `valid/` — devem ser aceites (8)

| Ficheiro | Descrição |
|---|---|
| `ndf/valid/despacho-avancado.json` | Caso de teste: despacho com assinatura avançada (SEA). Sem dados pessoais. |
| `ndf/valid/modelo3-irs.json` | Caso de teste: Modelo 3 IRS 2026 — SP A solteiro, 1 empregador, Anexo A incluído. Demonstra tipo_documento_ref com schema do registry modelo3-irs@2026. |
| `ndf/valid/oficio-com-ncrtf.json` | NDF-core válido com campo 'corpo' em NCRTF v2.0.0. Valida integração NDF+registry+NCRTF. |
| `ndf/valid/oficio-qualificado.json` | Caso de teste: ofício com assinatura qualificada e dados pessoais. Todos os campos obrigatórios presentes. |
| `ndf/valid/parecer-com-relacoes-e-ia.json` | Caso de teste: parecer com relacoes[] (emite_parecer_sobre), participantes[] e proveniencia_ia (utilizada com revisão humana concluída). Cobre §2.11, §2.12, §2.… |
| `ndf/valid/registo-interno-sem-assinatura.json` | Caso de teste: registo interno sem assinatura eletrónica (nivel_assinatura: nenhuma), com destino_final conservacao_permanente. Requer CAdES-B-LTA para integrid… |
| `ndf/valid/relacao-extensao-qualificada.json` | Caso de teste: relacoes[0].tipo usa extensão qualificada 'ext.<entidade>.<tipo>' (§2.11.7), fora do vocabulário base fechado mas estruturalmente válida. |
| `ndf/valid/versao-substituicao.json` | Caso de teste: NDF-core de um documento que SUBSTITUI um anterior, via relacoes[{tipo:'substitui'}] no core assinado (§6, ADR-011). O NDF-core em si tem estado=… |

### `invalid/` — devem ser rejeitados (20)

| Ficheiro | Descrição |
|---|---|
| `ndf/invalid/dados-pessoais-sem-base-legal.json` | INVÁLIDO: contem_dados_pessoais: true mas base_legal_conservacao ausente. Violação: §2.7.2, §1.6. |
| `ndf/invalid/document-schema-mismatch.json` | INVÁLIDO: documento não cumpre o schema oficio@1.0.0. |
| `ndf/invalid/invalid-estado.json` | INVÁLIDO: estado no NDF-core com valor diferente de 'ativo'. Violação: §2.4. O NDF-core declara sempre estado='ativo' no momento da finalização — estados de cic… |
| `ndf/invalid/invalid-ndt-version-ref.json` | INVÁLIDO: ndt_version_ref não segue o formato normativo '<schema_id>@<versao_ndt>'. Violação: §2.6. |
| `ndf/invalid/invalid-nivel-assinatura.json` | INVÁLIDO: nivel_assinatura com valor fora do enum. Violação: §2.10.1. |
| `ndf/invalid/invalid-tipo-classificacao-ref.json` | INVÁLIDO: tipo_classificacao_ref não segue o formato normativo '<instrumento>/<codigo>'. Violação: §3.2.1. |
| `ndf/invalid/invalid-uuid.json` | INVÁLIDO: ndf_id não é UUID v4 válido (não segue o formato RFC 9562 UUIDv4). Violação: §2.3. |
| `ndf/invalid/mismatched-instrument.json` | INVÁLIDO: referências de classificação usam instrumentos diferentes. |
| `ndf/invalid/missing-avaliacao.json` | INVÁLIDO: bloco avaliacao ausente. Violação: §3.2, §5.1. |
| `ndf/invalid/missing-ndf-id.json` | INVÁLIDO: campo obrigatório ndf_id ausente. Violação: §2.3, §5.1. |
| `ndf/invalid/missing-nivel-assinatura.json` | INVÁLIDO: campo obrigatório nivel_assinatura ausente. Violação: §2.2, §5.1. |
| `ndf/invalid/missing-tipo-documento-ref.json` | INVÁLIDO: metadados.tipo_documento_ref ausente. Violação: §2.7.2. Sem este campo não é possível interpretar 'documento' de forma fiável a longo prazo. |
| `ndf/invalid/ncrtf-marks-fora-de-ordem.json` | NDF estruturalmente válido, mas campo 'corpo' tem NCRTF com marks fora da ordem canónica (['italic','bold'] viola R1). Deve ser rejeitado pelo validador semânti… |
| `ndf/invalid/ncrtf-subscript-superscript.json` | NDF estruturalmente válido, mas campo 'corpo' tem NCRTF com subscript e superscript no mesmo nó text. Viola §5.2 da spec NCRTF. |
| `ndf/invalid/proveniencia-ia-inconsistente.json` | INVÁLIDO: proveniencia_ia.utilizada é false mas intervencoes não está vazio. Violação: §2.13.2 — quando utilizada é false, intervencoes DEVE estar ausente ou va… |
| `ndf/invalid/relacao-extensao-malformada.json` | INVÁLIDO: relacoes[0].tipo tenta usar extensão qualificada mas o formato está malformado (entidade em maiúsculas). Violação: §2.11.7 — 'entidade' DEVE ser lower… |
| `ndf/invalid/relacao-payload-hash-formato-invalido.json` | INVÁLIDO: relacoes[0].alvo.payload_hash não segue o formato '<alg>:<hex>'. Violação: §2.11.1. |
| `ndf/invalid/relacao-sem-payload-hash.json` | INVÁLIDO: relacoes[0].alvo sem payload_hash. Violação: §2.11.1, §2.11.5 — o alvo DEVE ser identificado por ndf_id e payload_hash. |
| `ndf/invalid/relacao-tipo-invalido.json` | INVÁLIDO: relacoes[0].tipo fora do vocabulário fechado. Violação: §2.11.2. |
| `ndf/invalid/revisao-humana-sem-revisor.json` | INVÁLIDO: intervencao com estado de revisão terminal ('revisto_e_aprovado') sem revisor_ref nem revisto_em. Violação: §2.13.3. |

## NCRTF

### `valid/` — devem ser aceites (7)

| Ficheiro | Descrição |
|---|---|
| `ncrtf/valid/heading-todos-niveis.json` | Valida os três níveis de heading suportados. |
| `ncrtf/valid/lista-aninhada.json` | Lista ordenada com um item que contém uma lista não-ordenada aninhada. Valida o modelo list_item com inlines + lista nested em content. |
| `ncrtf/valid/lista-com-alinhamento.json` | Lista ordenada com alinhamento central — valida o campo 'alignment' em nós 'list' (adicionado em v2.0.0 para preservar fidelidade ao editor). |
| `ncrtf/valid/lista-verificacao.json` | Lista de verificação (checklist) com dois itens: um assinalado e um por assinalar. Todos os list_item têm checked explícito. |
| `ncrtf/valid/marcas-inline.json` | Valida todas as 7 marcas disponíveis em v2.0.0, na ordem canónica correcta. Subscrito e sobrescrito em nós separados (não coexistem). |
| `ncrtf/valid/paragraph-simples.json` | Caso mínimo: dois parágrafos com texto simples, sem marcas. |
| `ncrtf/valid/tabela-com-cabecalhos.json` | Tabela com linha de cabeçalho (head) e duas linhas de dados (body). Células são strings simples — v2.0.0. |

### `invalid/` — devem ser rejeitados (9)

| Ficheiro | Descrição |
|---|---|
| `ncrtf/invalid/checked-em-lista-bullet.json` | Inválido: campo 'checked' num list_item de lista não-checklist. 'checked' é exclusivo de list_type: 'checklist'. |
| `ncrtf/invalid/checklist-sem-checked.json` | Inválido: lista de verificação com list_item sem campo 'checked'. Em checklist, todos os itens DEVEM ter 'checked' explicitamente (true ou false). |
| `ncrtf/invalid/content-vazio.json` | Inválido: content vazio na raiz. Viola minItems:1 no schema. |
| `ncrtf/invalid/header-false.json` | Inválido: nó image com campo 'src' (data URL) em vez de 'ref'. Em v2.0.0, 'ref' é obrigatório e 'src' não é um campo permitido (additionalProperties: false). Vi… |
| `ncrtf/invalid/marks-fora-de-ordem.json` | Inválido: marks em ordem errada — ['italic', 'bold'] viola R1. Ordem canónica: bold, code, italic, strikethrough, subscript, superscript, underline. |
| `ncrtf/invalid/subscript-superscript-simultaneos.json` | Inválido: subscript e superscript no mesmo nó text. Estão em ordem canónica (R1 passa) mas violam a exclusão mútua de §5.2. |
| `ncrtf/invalid/tabela-colunas-inconsistentes.json` | Inválido: tabela com número inconsistente de células por linha — linha de cabeçalho tem 3 células, primeira linha de body tem 2. Viola SPEC.md §4.5. |
| `ncrtf/invalid/text-contiguo-mesmas-marcas.json` | Inválido: dois nós text contíguos com as mesmas marcas ['bold']. Viola R2 — devem ser fundidos num único nó. |
| `ncrtf/invalid/text-vazio.json` | Inválido: nó text com string vazia. Viola minLength:1 no schema (R6). |

## NDT

### `valid/` — devem ser aceites (5)

| Ficheiro | Descrição |
|---|---|
| `ndt/valid/blocos-tabela.json` | BlocoTabela com colunas de múltiplos formatos. Verifica BlocoTabela, ColunaDef, estilo_cabecalho e todos os FormatoDisplay usados em colunas. |
| `ndt/valid/minimal.json` | NDT mínimo válido — apenas campos obrigatórios: ndt_version, schema_id, versao_ndt, paginas_def e sequencia. Verifica que o schema aceita um template sem grafic… |
| `ndt/valid/recurso-embebido.json` | Recurso SVG embebido em base64 (modo: embebido). Verifica RecursoEmbebido e referencia_recurso em GraficoImagem. |
| `ndt/valid/recurso-referenciado-por-hash.json` | Recurso SVG referenciado por hash SHA-256 (modo: referenciado_por_hash). Verifica RecursoReferenciadoPorHash com hash_sha256 e content_type. |
| `ndt/valid/sequencia-overflow.json` | Sequência com página de continuação (repeticao: conforme_necessario). Verifica fonte_overflow, linhas_por_pagina e incluir_se em SequenciaEntrada. |

### `invalid/` — devem ser rejeitados (5)

| Ficheiro | Descrição |
|---|---|
| `ndt/invalid/duplicate-page-id.json` | ids de pagina devem ser únicos |
| `ndt/invalid/missing-sequencia.json` | sequencia é obrigatória |
| `ndt/invalid/non-positive-dimension.json` | dimensões devem ser positivas |
| `ndt/invalid/unknown-page-ref.json` | sequencia deve referenciar pagina existente |
| `ndt/invalid/wrong-version.json` | ndt_version deve ser 2.0.0 |

## CUSTODY

### vetores diretos (2)

| Ficheiro | Descrição |
|---|---|
| `custody/invalid-chain.json` | — |
| `custody/valid-chain.json` | — |

## JCS

### vetores diretos (2)

| Ficheiro | Descrição |
|---|---|
| `jcs/numbers.json` | — |
| `jcs/vectors.json` | — |

**Total: 58 casos.**
