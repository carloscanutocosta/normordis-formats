# NCRTF Changelog

## [2.0.0] — 2026-06-18

### Versão major — breaking changes

**Motivação**: absorver todas as capacidades do editor NORMORDIS (normordis-core-ui) e corrigir três problemas críticos de arquivo identificados em v1.3.0 do serializer.

**Correcções críticas**:
- Removido `meta.updated_at` — não determinístico, quebrava a canonicalização JCS
- `image.ref` obrigatório (em vez de `src` com base64) — base64 tornava o hash instável e inchaça o payload
- `font_family` passa de marca-objecto para campo explícito em `text`, `paragraph`, `heading` — eliminando tipos mistos no array `marks`

**Novas capacidades**:
- Nós inline: `link` (hiperligação) e `hard_break` (quebra de linha forçada)
- Nó bloco: `blockquote` (citação em bloco)
- Marcas: `"code"` (monospace inline) e `"strikethrough"` (texto riscado)
- Campos em blocos: `alignment` (`center`/`justify`/`right`), `indent` (indentação), `font_family`
- Imagem: `caption` e `width_percent`; removidos `width`/`height` em pixéis

**Alterações estruturais**:
- Listas unificadas: `ordered_list`/`unordered_list` → `list` com `list_type: "ordered"|"bullet"|"checklist"`; `items` → `content`; `list_item` passa a nó explícito com `type: "list_item"` e conteúdo inline (não blocos)
- Tabelas simplificadas: `rows`/`cells` com `header: true`/`content` → `head`/`body` com `cells: string[]`; células são texto simples (não rich text)
- Ordem canónica das marcas actualizada: `bold`, `code`, `italic`, `strikethrough`, `subscript`, `superscript`, `underline`
- R2 actualizado: contiguidade exige marcas E `font_family` idênticos

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
