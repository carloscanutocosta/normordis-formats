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

### Correções de seguimento pós-revisão

- alterado: SPEC.md §2.12.1 e §2.12.3 — `participantes` deixa de ser descrito
  como servindo "auditoria", termo que após a ADR-010 podia ser lido como
  *audit trail* operacional (Perfil de Ciclo de Vida). Passa a "consulta,
  proveniência e interoperabilidade documental";
- alterado: `.github/workflows/validate.yml` — `actions/checkout`,
  `actions/setup-python` e `actions/setup-node` atualizadas para v7, e o
  runtime Node dos verificadores JS de 20 para 24. Resolve os avisos de
  depreciação de Node.js 20 emitidos pelo GitHub Actions.

### Revisão adversarial pré-RC — 16 achados resolvidos (`NDF-PRE-RC-REVIEW.md`)

Revisão dirigida a contradições, redundâncias e requisitos impossíveis de
implementar, em vez de novas funcionalidades. Relatório completo em
`docs/reports/NDF-PRE-RC-REVIEW.md`.

**Alteração arquitetural (ADR-011):**

- removido: `versao_anterior` e `hash_anterior` do envelope. A sucessão
  documental passa a ser representada exclusivamente por
  `relacoes[{tipo: "substitui"}]` no NDF-core assinado — um facto, um sítio,
  coberto pela assinatura. Resolve em cascata a contradição do manifesto
  (F3), a hierarquia normativa invertida (F6) e a ausência total de
  cobertura de teste do mecanismo removido (F8);
- alterado: SPEC.md §6 reescrita — sucessão é uma relação entre documentos
  autónomos e imutáveis (`A continua a existir; B substitui A`), não
  versionamento interno.

**Contradições SPEC↔schema corrigidas:**

- corrigido: SPEC.md §2.4.2 — o exemplo e a tabela do log de custódia
  descreviam um modelo de dados que falhava 9 validações contra o
  `custody-event.schema.json` que a própria cláusula torna obrigatório
  (só `ndf_id` coincidia). Alinhados ao schema, com a semântica antiga
  (`motivo`, `instrumento_legal`) mapeada para `details` (F1);
- corrigido: SPEC.md §8.2 — o exemplo do `manifest.json` omitia três campos
  obrigatórios (`estado`, `nivel_assinatura`, `validation_code`) (F2);
- corrigido: SPEC.md §2.10.3 — a tabela ainda tratava `timestamps` e
  `validation_material` como campos de topo do envelope, contra a ADR-004
  (F4); mesma correção em §6.2 (F5) e na referência de §4.1, que apontava
  para §4.4.2 em vez de §4.4.1 (F12).

**Simplificações e clarificações:**

- alterado: o tombstone de eliminação (§2.4.3) deixa de ser um artefacto
  normativo próprio sem schema; passa a **evento terminal** no log de
  custódia (`event_type: "eliminado"`, evidência em `details`), reutilizando
  a estrutura já existente (F7);
- adicionado: SPEC.md §2.12.3 — as três noções de autoria
  (`documento.autor`, `participantes[].papel`, `assinaturas[].papel`) são
  declaradas semanticamente distintas, com regra de coerência, sem impor
  uma hierarquia de precedência artificial (F10);
- documentados: campos de schema que existiam sem prosa normativa —
  `assinado_em`, subcampos de `timestamps`, `validation_material` e
  `revogacao`, e `finalidade_detalhe` (F11).

**Guardrails de CI (novo — impede a reincidência do padrão):**

- adicionado: `tools/check_spec_coherence.py` — valida os blocos JSON
  normativos da SPEC contra os schemas, verifica que todo o campo de schema
  está documentado, que as referências `§X.Y` resolvem, que enums
  deliberadamente duplicados não derivam (F16), e que propriedades removidas
  por ADR não reaparecem;
- adicionado: `tools/build_conformance_index.py` — gera `conformance/INDEX.md`
  a partir dos ficheiros reais. O README de conformidade documentava 14 de
  28 casos por ser mantido à mão (F15); o índice passa a ser gerado e
  verificado em CI;
- alterado: `.github/workflows/validate.yml` — ambas as ferramentas ligadas
  ao pipeline.

### Resíduos de fronteira NDF/Perfil de Ciclo de Vida (revisão de consistência)

Revisão externa ao ADR-010 encontrou três resíduos onde a separação
formato/perfil não tinha sido aplicada até ao fim:

- corrigido: SPEC.md §2.10.4 — a linha de `conservacao_permanente` dizia
  "custódia append-only/WORM e auditoria continuam obrigatórias", em
  tensão direta com §9.5 (perfil opcional). Reescrita para tornar a
  dependência do perfil explícita;
- corrigido: SPEC.md §4.4.2 — separado o requisito de formato/pacote
  (preservar byte a byte a assinatura original, timestamps e material de
  validação) do requisito específico do Perfil de Ciclo de Vida NORMORDIS
  (registar renovação criptográfica como evento append-only no log de
  custódia);
- suavizado: SPEC.md §3.2.1 e §3.5 — "`tipo_classificacao_ref` é resolvido
  automaticamente... nunca introduzido manualmente" e equivalente para
  `prazo_conservacao_administrativa`/`destino_final` eram regras de
  implementação do sistema produtor apresentadas como requisito do
  formato; passam a **RECOMENDA-SE**, mantendo como requisito apenas que o
  valor final seja válido, coerente e imutável;
- registada em `ROADMAP.md` (v2.0.0): nota sobre generalização futura do
  bloco `avaliacao` — hoje semanticamente acoplado ao modelo arquivístico
  português (PCA/DF/DGLAB), relevante para adoção por outras
  administrações europeias. Sem ação prevista para 1.0, apenas registo da
  questão.

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

### Correção do estado editorial e adiamento de PR-001 (2026-08-11)

Origem: avaliação de prontidão para debate público e candidatura NGI, em
`docs/reports/READINESS-ASSESSMENT.md` (achado `R1`, decisão D1). O estado
declarado descrevia uma revisão pública que nunca chegou a ser aberta.

- alterado: estado editorial de `Draft — Revisão pública` (nível 2 de
  `NORMALIZATION.md`) para `Draft — revisão pública por abrir` (nível 1) em
  `specs/ndf/SPEC.md`, `specs/ndt/SPEC.md`, `specs/ncrtf/SPEC.md`,
  `specs/registry/SPEC.md`, `specs/portal/SPEC.md` e
  `specs/ndt/RENDERER-CONFORMANCE.md`;
- alterado: PR-001 passa a estado `adiado` em
  `docs/normalization/REVIEW-LOG.md`; a janela proposta 2026-07-01 → 2026-08-15
  é dada por caduca sem comentários recebidos e sem commit fixado; o critério
  de abertura passa de temporal a **condição de evidência** — `normordis-pdf`
  a produzir um documento a partir de NDF + NDT, reproduzível por terceiros;
- alterado: secção "Estado" do `README.md` declara explicitamente que nenhum
  período de revisão está aberto e que nenhum dos oito gates externos de
  `READINESS.md` está cumprido;
- alterado: `tools/check_publication_profile.py` valida contra um conjunto
  `ALLOWED_STATES` em vez de exigir literalmente `Draft — Revisão pública` —
  a ferramenta tornava obrigatório por CI o estado incorreto; mantém-se como
  gate real, falhando se nenhum estado admissível for declarado;
- adicionado: `docs/reports/READINESS-ASSESSMENT.md` — documento vivo com as
  decisões de sequenciamento D1–D7, comparação NDF vs. abordagem tradicional
  (12 vantagens, 10 desafios) e achados `R1`–`R13` de estado rastreável;
- adicionado: secção de decisões de sequenciamento e Fase 1D (evidência de
  assinatura CAdES) em `ROADMAP.md`;
- alterado: `docs/roadmap/NGI-MVP-2026.md` marcado como parcialmente superado,
  distinguindo o que caducou (datas dos marcos, centralidade do XML) do que se
  mantém válido.

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
