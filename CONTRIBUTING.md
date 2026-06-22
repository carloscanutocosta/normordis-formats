# Contributing

Thank you for your interest in NORMORDIS format specifications.

## What lives here

This repository contains **format specifications only** — text, JSON Schemas, and conformance fixtures. Reference implementations live in separate repositories.

## How to contribute

### Reporting issues

Open a GitHub issue for:
- Ambiguities or contradictions in specification text
- Conformance fixture errors (a valid fixture that should be invalid, or vice versa)
- Schema gaps or inconsistencies
- Typos and editorial corrections

### Proposing changes

1. Open an issue first to discuss the change before writing anything.
2. For normative changes (anything that affects what a conforming implementation must do), explain the use case and the impact on existing implementations.
3. Fork the repository, make your changes on a branch, and open a pull request referencing the issue.

### What counts as a normative change

A normative change requires a version bump under the [versioning policy](VERSIONING.md):

- **Breaking (major)**: removes or renames a mandatory field, changes semantics of an existing field.
- **Additive (minor)**: adds a new optional field or capability; existing readers continue to work.
- **Clarification (patch)**: rewording, typo fixes, non-normative note additions — no behavioural impact.

### Conformance fixtures

When adding or modifying fixtures under `conformance/`:
- `valid/` fixtures must satisfy the JSON Schema and all normative rules in the specification.
- `invalid/` fixtures must violate exactly one rule; the filename should name the violated rule.

## Licensing

By contributing to this repository you agree that your contributions are dedicated to the public domain under [CC0 1.0](LICENSE). No CLA is required.

## Code of conduct

Be respectful and constructive. This is a technical specification project; discussions should stay focused on correctness, interoperability, and implementer needs.
