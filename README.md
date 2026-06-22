# normordis-spec

[![License: CC0-1.0](https://img.shields.io/badge/license-CC0%201.0-lightgrey.svg)](LICENSE)
[![NDF](https://img.shields.io/badge/NDF-v1.0.0-blue)](specs/ndf/SPEC.md)
[![NDT](https://img.shields.io/badge/NDT-v2.0.0-blue)](specs/ndt/SPEC.md)
[![NCRTF](https://img.shields.io/badge/NCRTF-v2.0.0-blue)](specs/ncrtf/SPEC.md)

Open specifications for document templates, document instances, and rich text content — designed for institutional document production, digital archiving, and eIDAS-compliant signing.

## Specifications

| Spec | Version | Description |
|---|---|---|
| [NDF](specs/ndf/SPEC.md) | 1.0.0 | NORMORDIS Document Format — immutable document instance |
| [NDT](specs/ndt/SPEC.md) | 2.0.0 | NORMORDIS Document Template — declarative layout template |
| [NCRTF](specs/ncrtf/SPEC.md) | 2.0.0 | NORMORDIS Canonical Rich Text Format — structured content |

## Principles

**The truth resides in the data; the PDF is merely a visual projection of that data.**

Specifications are sovereign. Implementations are replaceable.

```
normordis-spec
       │
       ├── NDF   — immutable signed document instance
       ├── NDT   — declarative layout template
       └── NCRTF — canonical rich text
                │
                ▼
      normordis-pdf
      normordis-html
      normordis-viewer
      ...
```

Any software producer, public organisation, or open source project may implement NDF, NDT, and NCRTF freely, with no contractual dependency on the authors.

## Repository structure

```
normordis-spec/
│
├── specs/
│   ├── ndf/          NDF specification, schemas, examples
│   ├── ndt/          NDT specification, schemas, examples
│   ├── ncrtf/        NCRTF specification, schemas, examples
│   └── registry/     Canonical identifier registry
│
├── conformance/      Official conformance test suites
│   ├── ndf/
│   ├── ndt/
│   └── ncrtf/
│
├── docs/             Conceptual documentation
│   └── architecture/ Architecture decision records (ADRs)
│
└── tools/            Reference validator
```

## Licensing

Specifications (text, schemas, examples) are released under [CC0 1.0](LICENSE) — public domain. No conditions, no attribution required.

Reference implementations are distributed under separate licenses (EUPL v1.2) in their respective repositories.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Governance

See [GOVERNANCE.md](GOVERNANCE.md).
