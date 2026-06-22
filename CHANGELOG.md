# Changelog

All notable changes to NORMORDIS format specifications are documented here.
Individual specifications maintain their own changelogs under `specs/<spec>/CHANGELOG.md`.

## [Unreleased]

## [2026-06-20] — NDT v2.0.0 stable + NDF/NCRTF harmonisation

### NDT
- v2.0.0 stable: declarative layout-only format; removed expression engine, validation rules, and domain logic
- `versao_ndt` replaces `versao_impresso`; applies to any template, not just fiscal forms
- `fluxo` layout mode for administrative documents (relative positioning after variable-length body)
- Signature field (`assinatura`) with hybrid CAdES/PAdES model
- PDF/UA-2 + PDF/A-3 simultaneous conformance
- `estilos` global styles block for ODF/HTML renderer mapping
- `incluir_se` at element level (previously only in `sequencia[]`)
- `linha_lateral`, `quebra_pagina`, `imagem` in `fluxo.elementos`
- Canonical NCRTF ↔ NDT font mapping (§5.8)
- `{{validation_code}}` token defined as renderer-provided
- See full details: [specs/ndt/CHANGELOG.md](specs/ndt/CHANGELOG.md)

### NDF / NCRTF
- Harmonisation with NDT v2.0.0 canonical font mapping
- Cross-spec consistency verified across schemas and examples

## [2026-06-18] — NCRTF v2.0.0 + NDF v1.0.0 initial release

### NCRTF
- v2.0.0: breaking changes from v1.0.0 — unified list type, simplified tables, explicit `font_family` field
- Inline nodes: `link`, `hard_break`; block node: `blockquote`
- Marks: `code`, `strikethrough`
- `alignment`, `indent`, `font_family` on block nodes
- Image `caption` and `width_percent`; removed pixel dimensions
- Canonical mark order updated; R2 contiguity rule includes `font_family`
- See full details: [specs/ncrtf/CHANGELOG.md](specs/ncrtf/CHANGELOG.md)

### NDF
- v1.0.0: initial specification — NDF-core structure, envelope (CAdES-B-LTA), archival evaluation (PCA/DF), finalisation pipeline, provenance chain, versioning policy
- See full details: [specs/ndf/CHANGELOG.md](specs/ndf/CHANGELOG.md)

### Repository
- Conformance test suites for NDF and NCRTF (valid/invalid fixtures)
- JSON Schema Draft 2020-12 for NDF-core, envelope, NDT, NCRTF, and registry types
- Registry specification and canonical document type schemas (ofício, despacho, informação técnica)
- Reference validator (`tools/validate.py`)
- ADR-001: JSON over XML rationale
