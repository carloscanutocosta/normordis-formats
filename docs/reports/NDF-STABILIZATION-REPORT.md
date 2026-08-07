# Relatório de estabilização NDF — Fase 4

**Missão de referência:** [`../design/NDF-STABILIZATION-MISSION.md`](../design/NDF-STABILIZATION-MISSION.md)
**Fases anteriores:** [`CURRENT-STATE-ASSESSMENT.md`](CURRENT-STATE-ASSESSMENT.md) (Fase 0),
[`../design/NDF-STABILIZATION-PROPOSAL.md`](../design/NDF-STABILIZATION-PROPOSAL.md) (Fase 1)
**Data:** 2026-08-07
**Estado do repositório:** nenhuma alteração foi commitada, publicada ou
enviada (`git push`) — todo o trabalho está na árvore de trabalho local,
pendente de revisão e confirmação explícita antes de qualquer commit.

## Resumo executivo

Implementadas as seis áreas identificadas na Fase 1: relações documentais
verificáveis, tipo de documento `parecer`, assinatura autocontida por
entrada, bloco de participantes, bloco de proveniência de IA, e agilidade de
algoritmo de hash. `ndf_version` mantido em `1.0.0` (ADR-007). Toda a suite
de conformidade existente continua a passar; foram acrescentados 6 novos
casos de conformidade NDF, 1 novo vetor negativo de pacote, 6 novos ADRs, um
exemplo completo de três NDF ligados por relações, e um guia informativo de
proveniência de IA.

## Ficheiros alterados

**Modificados (25):** `specs/ndf/SPEC.md`; schemas
`ndf-core.schema.json`, `envelope.schema.json`, `manifest.schema.json`,
`custody-event.schema.json` (e as suas cópias em
`specs/ndf/examples/ndfpkg-example/schemas/`); `specs/registry/SPEC.md`;
`specs/registry/schemas/despacho.schema.json`,
`informacao-tecnica.schema.json`, `oficio.schema.json`;
`specs/ndf/examples/ndfpkg-example/envelope.json` e `manifest.json`;
`tools/validate.py`, `tools/check_package_vectors.py`; `CHANGELOG.md`,
`README.md`; `docs/normalization/NDF-INFORMATIVE-GUIDANCE.md`,
`TRACEABILITY.md`, `READINESS.md`, `REQUIREMENTS.md` e
`NORMATIVE-STATEMENTS.md` (estes dois últimos regenerados por ferramenta,
não editados à mão).

**Novos (17):** `specs/registry/schemas/parecer.schema.json`;
`specs/ndf/examples/informacao-parecer-despacho/` (README + 3×
ndf-core.json + 3× envelope.json); 6 casos de conformidade em
`conformance/ndf/valid/` e `conformance/ndf/invalid/`; 6 ADRs
(`ADR-002` a `ADR-007`); `docs/design/NDF-STABILIZATION-MISSION.md` e
`NDF-STABILIZATION-PROPOSAL.md`; `docs/reports/CURRENT-STATE-ASSESSMENT.md`;
`docs/normalization/AI-PROVENANCE-GUIDANCE.md`.

## Decisões tomadas

Ver ADR-002 a ADR-007 para justificação completa de cada uma. Resumo:

| Decisão | ADR |
|---|---|
| `relacoes[]` no NDF-core, vocabulário fechado de 11 tipos, hash obrigatório no alvo | ADR-002 |
| Documentos autónomos (não secções sucessivamente assinadas) | ADR-003 |
| Assinatura autocontida — `timestamps`/`validation_material` por entrada, não globais | ADR-004 |
| Proveniência de IA em dois níveis (essencial no core / logs externos) | ADR-005 |
| `participantes[]` independente de `assinaturas[].signatario` | ADR-006 |
| Manter `1.0.0` — tratado como preparação de PR-001, não candidata subsequente | ADR-007 |

Decisões de menor alcance, sem ADR dedicado: `despacho.sobre[]` mantido e
estendido com `payload_hash` opcional (não descontinuado); padrão de hash
generalizado para `^[a-z][a-z0-9-]*:[0-9a-f]+$` em todos os campos de
referência (envelope, manifest, custody-event, anexos do registo).

## Versão resultante

`ndf_version: "1.0.0"` — sem alteração. Ver ADR-007. `registry` (tipos de
documento) também mantido em `1.0.0` para todos os tipos, incluindo
`despacho` (a proposta de Fase 1 tinha equacionado `despacho@1.1.0`; optou-se
por editar em raiz para consistência com a decisão geral de não versionar
durante a preparação da revisão — desvio da proposta original, justificado
pela mesma lógica do ADR-007).

## Compatibilidade

Todas as adições ao NDF-core (`relacoes`, `participantes`, `proveniencia_ia`)
são campos opcionais — nenhum documento existente deixa de validar. A
reestruturação do envelope (assinatura autocontida) altera a forma de um
campo já existente; não há adoção externa a proteger (confirmado
explicitamente pelo responsável do projeto antes da implementação). A
generalização do padrão de hash é estritamente mais permissiva do que o
padrão anterior — nenhum valor anteriormente válido deixa de o ser.

## Exemplos adicionados

`specs/ndf/examples/informacao-parecer-despacho/` — três NDF autónomos
(informação técnica, parecer, despacho) ligados por `relacoes[]`, com
`payload_hash` reais calculados por canonicalização RFC 8785 efetiva (não
fabricados), múltiplas assinaturas autocontidas no despacho (pessoal +
selo institucional), e proveniência de IA no parecer com revisão humana
concluída. README próprio com diagrama do grafo e tabela de hashes
verificáveis.

## Testes executados

Todos os comandos abaixo foram executados localmente com resultado
integralmente positivo, replicando `.github/workflows/validate.yml`:

| Comando | Resultado |
|---|---|
| `python3 tools/validate.py` | 56/56 (50 anteriores + 6 novos) |
| `python3 tools/validate.py --package specs/ndf/examples/ndfpkg-example` | PASS |
| `python3 tools/check_package_vectors.py` | 8/8 (7 anteriores + `PKG-NEG-008`) |
| `python3 tools/check_ndt_semantic_corpus.py` | PASS — 9 casos |
| `python3 tools/build_requirements_index.py` | PASS — 51 IDs únicos (era 45) |
| `python3 tools/audit_normative.py` | PASS — 51 IDs; 167 declarações |
| `python3 tools/check_publication_profile.py` | PASS — 3 drafts |
| `python3 tools/check_jcs_vectors.py` (Python) e `check-jcs-vectors.mjs` (Node) | PASS — 12/12 em ambas as linguagens |
| `python3 tools/check_custody.py` (válido e inválido) | PASS — aceita a cadeia válida, rejeita a inválida |
| `node tools/check-custody.mjs` (válido e inválido) | PASS — idêntico ao Python |
| Verificação de boa-formação de todos os `*.json` do repositório | 227 ficheiros OK |

**Não executado nesta fase:** `python3 tools/build_review_bundle.py` —
recusa-se a correr com árvore Git suja por desenho (`FAIL: árvore Git com
alterações; use --allow-dirty apenas para pré-visualização`). Este é um
passo de empacotamento do dossier de revisão pública, não uma verificação de
correção do conteúdo — deve ser corrido depois de decidires sobre commit, não
antes.

## Ferramentas de terceiros necessárias e não pré-instaladas

`rfc8785==0.1.4` (fixado em `tools/requirements.txt`) não estava disponível
no ambiente Python do sistema (gerido externamente, `pip install` direto
bloqueado). Foi usado um venv temporário em `/tmp/ndf-tmp-venv` apenas para
correr os passos que dependem dele (`check_jcs_vectors.py`,
`check_custody.py`, e o cálculo dos hashes reais do novo exemplo) — não faz
parte do repositório nem foi persistido.

## Limitações e riscos conhecidos

- `despacho.sobre[]` e `NDF-core.relacoes` podem divergir se um produtor só
  preencher um dos dois — a especificação recomenda coerência (§2.11.4), mas
  não há validação cruzada automática no schema (ficaria acoplada ao
  registo, fora do NDF-core). Não implementado nesta ronda.
- `participantes[]` pode ficar redundante com `informacao-tecnica.autor` /
  `despacho.decisor` quando preenchidos para a mesma pessoa — decisão
  consciente de não fundir (ADR-006), registada como dívida técnica.
- O exemplo `informacao-parecer-despacho/` não é um `.ndfpkg` completo (sem
  NDT, recursos nem manifesto) — por desenho, para manter o foco no grafo de
  relações; `ndfpkg-example/` continua a ser a referência de portabilidade
  completa.
- As assinaturas CAdES em todos os exemplos (novos e existente) continuam a
  ser *placeholders* ilustrativos, não assinaturas reais — consistente com o
  estado do gate CAdES em `READINESS.md`.

## Gates externos — inalterados, continuam pendentes

Nenhum gate externo foi declarado concluído por este trabalho. Continuam
pendentes, tal como antes: fixtures CAdES-B-LTA reais, revisão criptográfica
independente, revisão arquivística, revisão jurídica, revisão de
acessibilidade, implementação/piloto independente, manifestação de
necessidade institucional, definição de Comissão Técnica. Ver
`docs/normalization/READINESS.md` (não alterado nestes itens, apenas nas
duas contagens de vetores de pacote, de 7 para 8).

## Próximos passos recomendados

1. Rever este relatório e os 6 ADRs antes de qualquer commit.
2. Decidir se e quando `git add`/`git commit` — não foi feito automaticamente.
3. Correr `tools/build_review_bundle.py` depois do commit, para reconstruir
   o dossier de revisão pública com o conteúdo atualizado.
4. Confirmar formalmente o estado de PR-001 (aberta/preparação) antes de
   comunicar externamente estas alterações como parte da revisão em curso.
5. Considerar, em ronda futura e fora do âmbito desta: harmonizar
   `informacao-tecnica.corpo`/`parecer.corpo` (string simples) com o uso de
   NCRTF já feito por `oficio.documento.corpo` — inconsistência pré-existente
   identificada mas não corrigida nesta ronda (§3.2 da proposta de Fase 1).

## O que pode ser comunicado publicamente

- O NDF suporta relações documentais verificáveis por hash entre documentos
  autónomos, com um exemplo completo e reprodutível (informação → parecer →
  despacho).
- O NDF suporta múltiplas assinaturas independentes, cada uma unidade de
  prova autocontida.
- O NDF regista proveniência proporcional de utilização de IA, com
  supervisão humana explícita, sem alegar conformidade automática com o AI
  Act.
- Todos os pontos acima passam a suite de conformidade automatizada,
  verificada em duas linguagens (Python e Node.js) para a camada de
  canonicalização e custódia.

## O que NÃO deve ser alegado publicamente

- Que as assinaturas CAdES-B-LTA destes exemplos são reais — são
  *placeholders*.
- Que o gate CAdES, a revisão criptográfica, jurídica ou arquivística estão
  concluídos — continuam pendentes, sem alteração desta ronda.
- Que existe conformidade demonstrada com o AI Act — o NDF fornece
  mecanismos de evidência, não uma certificação de conformidade (SPEC.md
  §2.13.1).
- Que esta versão passou por revisão pública — PR-001 continua em
  `preparação` em `docs/normalization/REVIEW-LOG.md` à data deste relatório.
