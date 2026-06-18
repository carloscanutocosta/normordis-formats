# Versioning Policy

> This document is a stub. Versioning policy to be defined.

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
