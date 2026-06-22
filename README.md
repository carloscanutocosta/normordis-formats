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

The formats are language- and runtime-neutral. C#, Rust, Go, Python, Java or
any other implementation is conformant when it produces the normative bytes
and observable results defined by the schemas and conformance vectors.

The shared normative architecture, including the distinction between
integrity, custody, institutional seals and personal signatures, is defined in
[docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md).

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
│   ├── ncrtf/
│   ├── jcs/
│   ├── custody/
│   └── cades/
│
├── docs/             Conceptual documentation
│   ├── architecture/ Normative architecture and ADRs
│   ├── normalization/ Normalization gates, traceability and references
│   └── benchmarks/  Storage efficiency methodology
│
├── benchmarks/       Benchmark results (reproducible measurements)
│
└── tools/            Reference validator and utilities
```

Normalization gates and external-review requirements are tracked in
[docs/normalization/READINESS.md](docs/normalization/READINESS.md). The public
verification protocol is defined by [specs/portal/SPEC.md](specs/portal/SPEC.md)
and its OpenAPI contract.

## Licensing

Specifications (text, schemas, examples) are released under [CC0 1.0](LICENSE) — public domain. No conditions, no attribution required.

Reference implementations are distributed under separate licenses (EUPL v1.2) in their respective repositories.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Governance

See [GOVERNANCE.md](GOVERNANCE.md).
