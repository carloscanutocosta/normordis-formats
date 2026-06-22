# Normative traceability matrix

This matrix is maintained as requirements are promoted from draft to stable.
Every mandatory behavioural requirement must eventually map to a schema rule,
positive vector, negative vector or an explicitly external assessment.

| Requirement family | Machine rule / vector | Current evidence |
|---|---|---|
| NDF structure and exact version | `ndf-core.schema.json` | NDF valid/invalid suite |
| Registry document shape | `registry/schemas/*.json` | registry applied by `validate.py` |
| NCRTF structure and canonical rules | `ncrtf.schema.json` + semantic checks | NCRTF valid/invalid suite |
| NDT structure and references | `ndt.schema.json` + semantic checks | NDT examples and negative suite |
| JCS bytes and digest | RFC 8785 + `conformance/jcs/vectors.json` | basic vectors; IEEE-754 set pending |
| Package paths and inventory | `manifest.schema.json` + package verifier | autocontained example |
| Required signature presence | cross-document package checks | structural example only |
| CAdES cryptographic validity | `conformance/cades` profile | real B-LTA fixtures pending externally |
| Custody event shape and chain | `custody-event.schema.json` + custody vectors | positive/negative draft vectors |
| Portal semantics | `specs/portal/openapi.yaml` | contract review pending |
| Renderer semantics | `RENDERER-CONFORMANCE.md` | golden output corpus pending |
| Storage efficiency | benchmark methodology | representative corpus pending |

Release review MUST expand this matrix and MUST NOT mark a requirement covered
merely because related prose exists.
