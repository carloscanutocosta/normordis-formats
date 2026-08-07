# Histórico de alterações

As alterações relevantes às especificações NORMORDIS são registadas aqui. Cada
formato mantém também o seu histórico em `specs/<formato>/CHANGELOG.md`.

## [Não publicado]

### Estabilização NDF — relações, assinaturas, participantes e proveniência de IA

Preparação de PR-001 (ver `docs/normalization/REVIEW-LOG.md`). `ndf_version`
mantido em `1.0.0` — ver ADR-007. Detalhe completo em
`docs/design/NDF-STABILIZATION-PROPOSAL.md` e
`docs/reports/NDF-STABILIZATION-REPORT.md`.

- adicionado: bloco opcional `relacoes` ao NDF-core — relações verificáveis
  entre documentos (`ndf_id` + `payload_hash` do alvo), vocabulário fechado
  de 11 tipos, mapeamento informativo a PROV-O (ADR-002);
- adicionado: tipo de documento `parecer@1.0.0` ao registo, distinto de
  `informacao-tecnica` (ADR-003);
- adicionado: `payload_hash` opcional a `despacho.sobre[]`, para coerência
  com `relacoes[]` quando ambos presentes;
- alterado: material de assinatura (`timestamps`, `validation_material`)
  passa de campo global do envelope para campo de cada entrada de
  `assinaturas[]` — unidade de prova autocontida; acrescentados
  `assinatura_id` (obrigatório), `papel` e `ordem` opcionais (ADR-004);
- adicionado: bloco opcional `participantes` ao NDF-core, distinto de
  `assinaturas[].signatario` (ADR-006);
- adicionado: bloco opcional `proveniencia_ia` ao NDF-core — evidência
  proporcional de utilização de sistemas de IA, com estado de revisão
  humana obrigatório por intervenção (ADR-005);
- alterado: padrão de hash em `payload_hash`, `hash_anterior`,
  `event_hash`, `previous_event_hash`, `hash_sha256` (manifest e anexos do
  registo) generalizado de `^sha256:[0-9a-f]{64}$` para
  `^[a-z][a-z0-9-]*:[0-9a-f]+$` — agnóstico de algoritmo, sem quebra de
  compatibilidade (aceita estritamente mais do que antes);
- adicionado: `docs/normalization/AI-PROVENANCE-GUIDANCE.md`;
- adicionado: `specs/ndf/examples/informacao-parecer-despacho/` — três NDF
  autónomos (informação, parecer, despacho) ligados por `relacoes[]`, com
  hashes reais recalculáveis;
- adicionado: 6 novos casos de conformidade NDF (1 válido, 5 inválidos) e um
  novo vetor negativo de pacote (`PKG-NEG-008-assinatura-sem-id`);
- adicionado: ADR-002 a ADR-007.

### Harmonização editorial e de normalização

- estado comum `Draft — Revisão pública` para NDF, NDT e NCRTF;
- política editorial, língua normativa e estrutura documental comum;
- regras de consenso, votação, recurso, conflitos de interesse e IPR;
- referências normativas controladas e migração de RFC 4122 para RFC 9562;
- alegações jurídicas reformuladas como objetivos técnicos condicionados;
- terminologia e ortografia portuguesa harmonizadas;
- referências NDF/NDT harmonizadas em `versao_ndt`, `documento.corpo` e no
  âmbito explícito de `pdf_hash`;
- matriz de rastreabilidade expandida com prefixos estáveis de requisitos.
- auditoria automática de 45 IDs e inventário de declarações subordinadas;
- sete vetores negativos de pacote `.ndfpkg`;
- corpus semântico NDT com nove casos estáveis;
- dossier de revisão pública autocontido e verificado por hashes;
- gates editoriais e normativos integrados na CI.

## [2026-06-20] — NDT v2.0.0 e harmonização NDF/NCRTF

### NDT

- formato declarativo de layout sem motor de regras de negócio;
- `versao_ndt` substitui `versao_impresso`;
- layout de fluxo, campo de assinatura e estilos globais;
- mapeamento NCRTF ↔ NDT;
- suporte estrutural a PDF/UA-2 e PDF/A-3;
- exemplos e suite de conformidade NDT.

### NDF / NCRTF

- harmonização do mapeamento tipográfico;
- revisão de consistência entre schemas e exemplos.

## [2026-06-18] — NCRTF v2.0.0 e NDF v1.0.0

### NCRTF

- listas unificadas, tabelas simplificadas e `font_family` explícito;
- nós `link`, `hard_break` e `blockquote`;
- novas marcas e regras de canonicalização.

### NDF

- estrutura NDF-core, envelope, avaliação arquivística, finalização,
  proveniência e versionamento.

### Repositório

- suites de conformidade NDF e NCRTF;
- schemas JSON para NDF, NDT, NCRTF, envelope, manifesto e registo;
- validador de referência;
- ADR sobre a escolha de JSON.
