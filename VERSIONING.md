# Versioning Policy

## Principles

Specifications follow semantic versioning (semver):

- **Major** (`x.0.0`): incompatible changes — removed or renamed mandatory fields, changed semantics. Readers must explicitly support each major version.
- **Minor** (`1.x.0`): backward-compatible additions — new optional fields. Existing readers continue to work.
- **Patch** (`1.0.x`): clarifications, typo fixes, non-normative changes. No behavioural impact.

## Spec vs. document version

`ndf_version` / `ndt_version` tracks the **format specification** version — it changes only when the format itself changes.

`impresso.versao_impresso` (NDT) tracks the **template instance** version — it changes annually for fiscal forms without altering the format version.

## Stability guarantees

- Canonical field paths (`id`s) are never renamed between minor versions.
- Discontinued fields are marked `"descontinuado": true` rather than removed, preserving readability of older documents.

## Compatibilidade e schemas

Cada schema valida exactamente a versão indicada no seu `$id`; o campo de
versão usa `const`, não um padrão SemVer genérico. Um leitor só declara suporte
a versões que reconheça explicitamente.

Uma versão minor pode acrescentar campos ou nós opcionais, mas um documento que
os use declara a nova versão. Leitores antigos não devem ignorar silenciosamente
conteúdo assinado desconhecido. Podem recusar o documento ou operá-lo apenas em
modo opaco, sem afirmar interpretação completa.

## Artefactos abrangidos

Uma release inclui como unidade indivisível:

- texto normativo;
- JSON Schemas;
- registry e schemas de tipos canónicos;
- exemplos e vectores canónicos;
- suite e runner de conformidade.

Alterar comportamento observável de qualquer destes artefactos exige uma nova
versão. URLs, hashes e artefactos de releases anteriores permanecem disponíveis.
