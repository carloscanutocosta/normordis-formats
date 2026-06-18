# NCRTF Changelog

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
