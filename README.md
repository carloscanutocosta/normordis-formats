# NORMORDIS Formats

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
NORMORDIS Formats
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

See repository documentation.

## Licensing

Specifications (text, schemas, examples) are released under CC0 1.0.

## Contributing

See CONTRIBUTING.md.

## Governance

See GOVERNANCE.md.