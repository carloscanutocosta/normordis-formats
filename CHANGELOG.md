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

### Revisão adversarial pós-estabilização — `LACUNAS.md`

Ver `LACUNAS.md` para a análise completa e `docs/reports/CURRENT-STATE-ASSESSMENT.md`
para o histórico de decisões.

- adicionado: SPEC.md §1.5 "Confidencialidade e controlo de acesso" — limite
  normativo explícito: o NDF não define nem garante cifra, controlo de
  acesso ou gestão de credenciação; `classificacao_seguranca` é sinal
  descritivo, a proteção é responsabilidade do sistema de custódia;
- adicionado: `docs/normalization/NDF-INFORMATIVE-GUIDANCE.md` — secção
  "Confidencialidade e controlo de acesso", incluindo pontos a considerar
  na implementação do core-documental (não normativo);
- decisão registada: mitigação de fuga de metadados por `relacoes[]` em
  documentos classificados fica fora de âmbito do NDF — resolvida por
  proteção do artefacto ao nível do core-documental, não por mecanismo do
  formato (`LACUNAS.md` L2);
- adicionado: SPEC.md §2.11.5 "Segurança e privacidade do grafo de
  relações" — relação é afirmação unilateral, não implica reconhecimento
  do alvo (A1/L1); deteção de ciclos é responsabilidade do verificador,
  não do schema (A3/L3);
- adicionado: nota em SPEC.md §4.4.1 — correspondência `papel`↔exigência
  legal de quem assina não é garantida pelo formato (A4/L7);
- adicionado: SPEC.md §2.12.3 — `participante_ref` é referência externa
  não resolvida pelo NDF, por desenho (A5/L9);
- adicionado: SPEC.md §2.12.4 — `validador`/`aprovador` descrevem estado
  de workflow; uso desencorajado fora de sistemas que já os tratem como
  tal, mantidos no enum sem alteração incompatível (A6/L10);
- adicionado: `tools/validate.py` `check_ndf_advisories` — aviso (não
  erro) quando `documento.sobre[]` e `NDF-core.relacoes` divergem (A7/L5);
- adicionado: `delegacao_ref` opcional em `parecer.autor` e
  `informacao-tecnica.autor`, mesmo padrão de `despacho.decisor` (A8/L8).

### Extensibilidade e fecho de `LACUNAS.md` (A9, A10)

- adicionado: extensão qualificada `ext.<entidade>.<tipo>` para
  `relacoes[].tipo`, além do vocabulário base fechado — alteração aditiva
  (`oneOf` no schema), sem quebra de compatibilidade; SPEC.md §2.11.7;
  ADR-008 (A9/L4);
- adicionado: 2 novos casos de conformidade NDF (1 válido com extensão
  qualificada, 1 inválido com extensão malformada) — suite passa a 58/58;
- decidido, e registado em ADR-009: `ndf_id` mantém-se UUID v4 opaco, sem
  espaço de nomes por entidade produtora — a necessidade já estava
  resolvida por `metadados.entidade_produtora`; alterar o identificador
  acoplaria-o a uma identidade organizacional mutável, para um ganho sem
  benefício real (A10/L6). Clarificação normativa acrescentada a SPEC.md
  §2.3, sem alteração de schema;
- `LACUNAS.md` fecha com os dez pontos resolvidos: sete implementados,
  um fechado por decisão de não-alteração, dois fora de âmbito.

### Separação entre conformidade NDF e Perfil de Ciclo de Vida NORMORDIS (ADR-010)

Revisão externa ao estado do repositório identificou que `SPEC.md`
misturava requisitos de formato com requisitos operacionais de gestão de
ciclo de vida documental, criando uma barreira de adoção desnecessária
para sistemas com o seu próprio modelo de custódia.

- adicionado: `docs/architecture/ADR-010-separacao-conformidade-perfil-ciclo-vida.md`;
- adicionado: nova secção "Perfil de Ciclo de Vida NORMORDIS (opcional)"
  em SPEC.md §9.5, com requisitos próprios `CUST-REQ-001..003` — reclassifica
  o requisito de log de auditoria que estava indevidamente em `NDF-PROD-010`;
- alterado: `NDF-PROD-010` deixa de exigir log de custódia; passa a exigir
  persistência atómica de `payload_bytes` e envelope (mantém a mesma ID,
  conteúdo diferente — sem renumeração);
- alterado: SPEC.md §2.4 (nova nota de âmbito), §5.2 passo 8 (dividido em
  requisito de formato + requisito de perfil), §2.10, §4.6.1, §4.6.4 e
  glossário — linguagem sobre `nivel_assinatura` e `validation_code`
  ajustada para não sugerir que o NDF decide juridicamente o nível de
  assinatura exigido, nem que depende de um serviço específico;
- alterado: `docs/architecture/ARCHITECTURE.md` §2.1, §3 — "registo de
  custódia" deixa de ser apresentado como parte constitutiva do NDF;
  passa a Perfil de Ciclo de Vida NORMORDIS opcional;
- alterado: `tools/build_requirements_index.py`, `tools/audit_normative.py`
  — reconhecem a família `CUST-REQ-*` (54 IDs únicos, antes 51);
- atualizado: `docs/normalization/TRACEABILITY.md` — família `CUST-REQ-*`
  com evidência real, já não placeholder.

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
