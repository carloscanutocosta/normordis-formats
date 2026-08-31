# NCRTF Changelog

## [Não publicado]

### Células de tabela passam a conter inline (2026-08-23)

**Incompatível**, absorvido em 2.0.0 antes de publicação.

`table_row.cells` era um array de strings, e a §4.5 declarava expressamente que
«o conteúdo das células NÃO suporta formatação rich text». O efeito prático não
é uma funcionalidade em falta: é **perda silenciosa em ida-e-volta**. Um editor
— Lexical, ProseMirror, qualquer um — admite negrito, ligação ou quebra de linha
dentro de uma célula por comportamento por omissão; a serialização deitava-os
fora sem aviso. Um documento administrativo com uma tabela de diplomas e o
respetivo estado é caso corrente, não caso limite.

- `cells` passa a array de `table_cell`, nó com `content` de nós **inline** —
  `text` com marcas, `link`, `hard_break`;
- a forma segue `list_item` (§4.3), que é o precedente do próprio formato para
  «contentor de conteúdo inline com etiqueta de tipo»;
- **blocos continuam excluídos** das células: parágrafos, listas, imagens e
  tabelas aninhadas não são admitidos. Admiti-los seria decisão por antecipação
  (ADR-015) e multiplicaria a complexidade de qualquer renderizador de layout
  fixo. Vetor negativo `celula-com-bloco.json`;
- migradas as quatro instâncias existentes; o vetor
  `tabela-com-cabecalhos.json` passa a exercitar marcas, ligação e quebra de
  linha dentro de células.


## [2.0.0] — 2026-06-18

### Versão major — breaking changes

**Motivação**: absorver todas as capacidades do editor NORMORDIS (normordis-core-ui) e corrigir três problemas críticos de arquivo identificados em v1.3.0 do serializer.

**Correcções críticas**:
- Removido `meta.updated_at` — não determinístico, quebrava a canonicalização JCS
- `image.ref` obrigatório (em vez de `src` com base64) — base64 tornava o hash instável e inchaça o payload
- `font_family` passa de marca-objeto para campo explícito em `text`, `paragraph`, `heading` — eliminando tipos mistos no array `marks`

**Novas capacidades**:
- Nós inline: `link` (hiperligação) e `hard_break` (quebra de linha forçada)
- Nó bloco: `blockquote` (citação em bloco)
- Marcas: `"code"` (monospace inline) e `"strikethrough"` (texto riscado)
- Campos em blocos: `alignment` (`center`/`justify`/`right`), `indent` (indentação), `font_family`
- Imagem: `caption` e `width_percent`; removidos `width`/`height` em pixéis

**Alterações estruturais**:
- Listas unificadas: `ordered_list`/`unordered_list` → `list` com `list_type: "ordered"|"bullet"|"checklist"`; `items` → `content`; `list_item` passa a nó explícito com `type: "list_item"` e conteúdo inline (não blocos)
- Tabelas simplificadas: `rows`/`cells` com `header: true`/`content` → `head`/`body` com `cells: string[]`; células são texto simples (não rich text) — alterado desde então, ver [Não publicado]
- Ordem canónica das marcas actualizada: `bold`, `code`, `italic`, `strikethrough`, `subscript`, `superscript`, `underline`
- R2 atualizado: contiguidade exige marcas E `font_family` idênticos

---

## [1.0.0] — 2026-06-18

### Lançamento inicial

- Especificação completa do NORMORDIS Canonical Rich Text Format
- Nós bloco: `paragraph`, `heading` (level 1–3), `ordered_list`, `unordered_list`, `table`, `image`
- Nós inline: `text` com marcas `bold`, `italic`, `underline`, `subscript`, `superscript`
- Regras de canonicalização R1–R6 para compatibilidade com JCS/RFC 8785
- Integração com NDT: campo `"type": "ncrtf"`
- Integração com `.ndfpkg`: imagens por `ref` (sem base64)
- JSON Schema Draft 2020-12 em `schemas/ncrtf.schema.json`
- Política de extensibilidade e candidatos a versões futuras (§9.3)
