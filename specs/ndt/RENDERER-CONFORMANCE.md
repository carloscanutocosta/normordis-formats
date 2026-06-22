# NDT Renderer Conformance Profiles

This document defines observable, language-neutral renderer roles. It does not
mandate a rendering engine.

## Common profile

Every renderer MUST:

- validate the NDT version and semantic references before rendering;
- resolve NDT paths relative to `NDF-core.documento`;
- reject missing required resources or hash mismatches;
- preserve NCRTF text, order, links, lists, tables and alternative text;
- report unsupported output features instead of silently claiming full
  conformance;
- record renderer name/version and output profile in a rendering report.

## Semantic-output profile

HTML, ODF and future flow formats conform when their extracted semantic tree
matches the expected language-neutral tree: headings, paragraphs, runs, marks,
lists, tables, images, links and reading order. Pixel equality is not required.

## Fixed-layout PDF profile

The PDF profile additionally fixes page geometry, coordinates, overflow rules,
font selection/substitution, resource hashes, colour space, reading order and
accessibility mappings. Golden tests MUST compare:

1. page count and page boxes;
2. normalized text and reading order;
3. element bounding boxes with a declared tolerance;
4. tagged-PDF structure and alternative text;
5. embedded font/resource identities;
6. PDF/A and PDF/UA validation reports for the declared subprofiles.

Binary equality is optional and may only be claimed by a deterministic profile
that fixes the complete engine and serialization environment.

## Required fixture corpus

- every NDT primitive in isolation;
- multi-page overflow with content before and after NCRTF;
- nested lists, tables and images;
- missing optional and required values;
- conditional inclusion;
- resource/hash failure;
- accessibility and bidirectional/Unicode text;
- at least two independently implemented renderers or extractors for semantic
  comparison before a stable interoperability claim.

The repository currently validates NDT structure and references but does not
yet contain these golden rendering outputs; this remains an implementation
gate, not an ambiguity in the conformance contract.
