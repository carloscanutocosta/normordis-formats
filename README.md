# NORMORDIS Formats

[![Licença: CC0-1.0](https://img.shields.io/badge/licen%C3%A7a-CC0%201.0-lightgrey.svg)](LICENSE-SPEC)
[![NDF](https://img.shields.io/badge/NDF-v1.0.0-blue)](specs/ndf/SPEC.md)
[![NDT](https://img.shields.io/badge/NDT-v2.0.0-blue)](specs/ndt/SPEC.md)
[![NCRTF](https://img.shields.io/badge/NCRTF-v2.0.0-blue)](specs/ncrtf/SPEC.md)

Especificações abertas para instâncias documentais, templates de apresentação e
conteúdo de texto estruturado.

## Objetivos centrais

O conjunto NORMORDIS Formats tem dois objetivos complementares:

1. **Armazenamento imutável, autocontido e eficiente em base de dados** — o
   NDF-core é canónico e adequado a persistência e indexação; o `.ndfpkg`
   materializa uma representação portátil sem dependências externas.
2. **Interoperabilidade** — NDF, NDT e NCRTF constituem contratos públicos,
   versionados e independentes de fornecedor, linguagem, runtime, base de dados
   ou implementação de referência.

## Estado

NDF, NDT e NCRTF encontram-se em **Draft — revisão pública por abrir**
(nível 1 de [NORMALIZATION.md](NORMALIZATION.md)). Este estado é interno ao
projeto e não representa aprovação, homologação ou publicação pelo IPQ, CEN,
ISO, IEC ou outra entidade normalizadora.

**Nenhum período de revisão pública está aberto.** O período PR-001 foi
adiado: por decisão de 2026-08-11, a abertura deixou de ter data e passou a
ter condição de evidência — abre quando `normordis-pdf` produzir, de forma
reproduzível por terceiros, um documento a partir de NDF + NDT. Condição,
fundamentação e o que fica por fixar na abertura estão em
[REVIEW-LOG.md](docs/normalization/REVIEW-LOG.md).

Em termos práticos, o conjunto pode ser apresentado publicamente como uma
proposta técnica madura para revisão externa: os formatos já possuem objetivos
claros, separação de responsabilidades, esquema e suites de conformidade,
matriz de rastreabilidade e gates explícitos para o que ainda depende de
evidência externa. Nenhum dos oito gates externos de
[READINESS.md](docs/normalization/READINESS.md) está cumprido, e nenhum deles
pode ser cumprido por revisão interna.

O que não deve ser comunicado é que exista já um estatuto formal de norma, uma
equivalência certificada com qualquer entidade normalizadora, ou uma revisão
pública em curso.

| Especificação | Versão | Finalidade |
|---|---:|---|
| [NDF](specs/ndf/SPEC.md) | 1.0.0 | instância documental canónica e imutável |
| [NDT](specs/ndt/SPEC.md) | 2.0.0 | template declarativo de apresentação |
| [NCRTF](specs/ncrtf/SPEC.md) | 2.0.0 | conteúdo de texto rico canónico |

## Princípios

**A fonte de verdade reside nos dados; o PDF é uma projeção desses dados.**

- As especificações são independentes das implementações.
- A conformidade é específica de uma versão, papel e perfil.
- Alegações jurídicas ou de conformidade externa exigem avaliação competente.
- Qualquer fornecedor ou entidade pode implementar os formatos sem dependência
  contratual das implementações NORMORDIS.

A arquitetura normativa comum encontra-se em
[docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md).

```text
NDF  — instância documental canónica
NDT  — apresentação declarativa
NCRTF — conteúdo de texto estruturado
  │
  └── renderizadores PDF, HTML, ODF ou outros
```

## Documentação do projeto

- [Governação](GOVERNANCE.md)
- [Política de versões](VERSIONING.md)
- [Conformidade](CONFORMANCE.md)
- [Política editorial](docs/normalization/EDITORIAL-POLICY.md)
- [Base terminológica](docs/normalization/TERMINOLOGY.md)
- [Referências normativas](docs/normalization/NORMATIVE-REFERENCES.md)
- [Orientações informativas NDF](docs/normalization/NDF-INFORMATIVE-GUIDANCE.md)
- [Orientações de proveniência de IA](docs/normalization/AI-PROVENANCE-GUIDANCE.md)
- [Camadas de interoperabilidade](docs/interoperability/INTEROPERABILITY-LAYERS.md)
- [Matriz de rastreabilidade](docs/normalization/TRACEABILITY.md)
- [Índice de requisitos](docs/normalization/REQUIREMENTS.md)
- [Inventário de declarações normativas](docs/normalization/NORMATIVE-STATEMENTS.md)
- [Registo de revisão pública](docs/normalization/REVIEW-LOG.md)
- [Plano de revisão pública](docs/normalization/PUBLIC-REVIEW-PLAN.md)
- [Perfil editorial de publicação](docs/normalization/PUBLICATION-PROFILE.md)
- [Declarações IPR](docs/normalization/IPR-DECLARATIONS.md)
- [Gates de prontidão](docs/normalization/READINESS.md)
- [Plano do gate CAdES](docs/normalization/CADES-GATE-PLAN.md)
- [Percurso de normalização](NORMALIZATION.md)
- [Contribuição](CONTRIBUTING.md)
- [Segurança](SECURITY.md)
- [Política de utilização de IA generativa](AI_USAGE.md)
- [Checklist de publicação pública](docs/PUBLICATION-CHECKLIST.md)

## Licenciamento

O texto das especificações, schemas e exemplos é disponibilizado nos termos de
[`LICENSE-SPEC`](LICENSE-SPEC). Implementações de referência podem usar
licenças diferentes nos respetivos repositórios.
