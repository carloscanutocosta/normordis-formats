# normordis-spec

Open specifications for document templates, document instances, rich text content and institutional interoperability.

## Specifications

| Spec | Version | Description |
|---|---|---|
| [NDF](specs/ndf/SPEC.md) | 1.0.0 | NORMORDIS Document Format — immutable document instance |
| [NDT](specs/ndt/SPEC.md) | 2.0.0 | NORMORDIS Document Template — declarative template and layout |
| [NCRTF](specs/ncrtf/SPEC.md) | — | NORMORDIS Canonical Rich Text Format — structured content |

## Principles

The truth resides in the data; the PDF is merely a visual projection of that data.

Specifications are sovereign. Implementations are replaceable.

```
normordis-spec
       │
       ├── NDF
       ├── NDT
       └── NCRTF
                │
                ▼
      normordis-pdf
      normordis-html
      normordis-viewer
      ...
```

## Licensing

Specifications (text, schemas, examples) are released under [CC0 1.0](LICENSE-SPEC) (public domain). No conditions, no attribution required.

Reference implementations are distributed under separate licenses (EUPL v1.2) in their respective repositories.

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
│   ├── architecture/
│   ├── concepts/
│   ├── lifecycle/
│   └── interoperability/
│
└── tools/            Reference validators and utilities
```

## Governance

See [GOVERNANCE.md](GOVERNANCE.md).
