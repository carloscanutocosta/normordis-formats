# Avaliação do estado atual — Fase 0

**Missão de referência:** [`docs/design/NDF-STABILIZATION-MISSION.md`](../design/NDF-STABILIZATION-MISSION.md)
**Data:** 2026-08-07
**Âmbito desta fase:** inspeção apenas. Nenhuma alteração normativa foi feita
a SPEC.md, schemas, exemplos ou suites de conformidade.

## Estado do repositório

- Branch `devel`, a acompanhar `origin/devel`; `git status` limpo, sem stash.
  Nada a preservar/reconciliar antes de propor alterações.
- Último commit: `69bf9a0` — "docs: harmonizar contratos NDF NDT NCRTF".
- `docs/normalization/REVIEW-LOG.md` regista **PR-001** (revisão pública de
  NDF 1.0.0, NDT 2.0.0, NCRTF 2.0.0), período 2026-07-01–2026-08-15, estado
  `preparação`. À data de hoje essa janela está tecnicamente a decorrer, mas
  o estado sugere que pode não ter sido formalmente aberta. **Isto é uma
  decisão a esclarecer contigo antes da Fase 1** — não presumi resposta.

---

## Já implementado

Mais do que o brainstorming original assumia. Em particular:

| Área | Onde | Nota |
|---|---|---|
| Retenção/destino final AP | `avaliacao` no NDF-core (SPEC.md §3), `estado` no envelope (§2.4.1) | PCA, `destino_final` (permanente/eliminação/amostragem), referência a Lista Consolidada DGLAB/PGD/Portaria |
| Tombstone de eliminação | SPEC.md §2.4.3 | Já especificado byte a byte: o que se destrói, o que subsiste, campos obrigatórios |
| Tensão imutabilidade↔RGPD | SPEC.md §1.4 | Já resolvida com o mesmo raciocínio (base legal prevalente, pseudonimização, eliminação no termo do PCA) que motivou a proposta de bloco de retenção no brainstorming |
| NDT como apresentação, não estrutura lógica | `docs/architecture/ARCHITECTURE.md` §2.2 | Já corrigido — "NDT é um template declarativo de apresentação. Não contém dados de negócio..." |
| Cadeia de custódia append-only | `custody-event.schema.json`, SPEC.md §2.4.2 | Hash encadeado (`previous_event_hash`/`event_hash`), sequência, ator, motivo, instrumento legal |
| Múltiplas assinaturas — estrutura base | `envelope.schema.json` `assinaturas[]` | Já é array; suporta N entradas |
| Rastreabilidade normativa auto-gerada | `tools/build_requirements_index.py`, `tools/audit_normative.py` | `REQUIREMENTS.md`/`NORMATIVE-STATEMENTS.md` não se editam à mão — geram-se a partir de **DEVE**/**NÃO DEVE** no SPEC.md |
| Tom cauteloso sobre conformidade legal | SPEC.md §1.1, §1.4 | O padrão de redação "a conformidade jurídica depende de..., não é garantida pelo formato isoladamente" já existe e está pronto a replicar para IA/AI Act |
| Prazo previsto para agilidade de hash | SPEC.md §2.5 | `payload_hash_alg` já enum extensível, com nota explícita de que 1.2.0 trará múltiplos algoritmos |

**Consequência prática:** a "Emenda 1" que propus na conversa (bloco de
retenção/destino-final AP + tombstone) estava, na sua formulação original,
a pedir para criar algo que **já existe e está bem especificado**. Corrigi
isto no ficheiro de missão (secção "4bis") — o trabalho real aí é de
**integração** do novo modelo de relações com este mecanismo já maduro, não
de criação. Reporto isto explicitamente porque a avaliação anterior, feita
sem ler o SPEC.md completo, estava incorreta neste ponto.

---

## Parcialmente implementado

| Área | Estado atual | Gap concreto |
|---|---|---|
| Relações entre documentos | `despacho.schema.json` tem `documento.sobre[]` com `{ndf_id, descricao}` | Sem `payload_hash` (não liga a bytes imutáveis exatos); vive dentro de `documento`, específico do tipo `despacho`, não reutilizável; não está coberto pelo modelo geral do core |
| Cadeia de proveniência de versões | `versao_anterior`/`hash_anterior` no envelope (SPEC.md §6.2) | Só cobre substituição linear 1:1; não cobre `anula`/`corrige`/`emite_parecer_sobre`/etc.; fica fora dos bytes assinados |
| Múltiplas assinaturas — material de prova | `assinaturas[]` existe | `timestamps` e `validation_material` são globais ao envelope, não por assinatura — ambíguo com N certificados/cadeias/OCSP distintos |
| Papel do signatário | `signatario.cargo` existe | Não distingue cargo organizacional de papel exercido no documento (autor/aprovador/decisor/...); sem `ordem` |
| Identidade de participantes | `autor` (informacao-tecnica), `decisor` (despacho), `signatario` (envelope) | Três modelos de identidade não coordenados; sem bloco comum `participantes` |
| Informação → Parecer → Despacho | `informacao-tecnica` e `despacho` já registados | **Falta o schema `parecer`** — o terceiro tipo do exemplo-âncora ainda não existe no registo |

---

## Ausente

- Bloco `relacoes[]` genérico no NDF-core.
- Bloco `proveniencia_ia` (qualquer nível — core ou externo).
- Bloco `participantes` unificado.
- Schema de tipo de documento `parecer`.
- `assinatura_id`, `papel`, `ordem`, `validation_material`/`timestamps` por
  assinatura em `envelope.schema.json`.
- Qualquer menção a relações documentais, múltiplas assinaturas ou IA em
  `ROADMAP.md` — confirmando que este trabalho ainda não está planeado
  formalmente, só discutido em brainstorming.
- ADRs além de `ADR-001-json-not-xml.md` (é o único existente).
- Padrão de hash agnóstico de algoritmo nas strings de referência
  (`^sha256:[0-9a-f]{64}$` está hardcoded em `envelope.schema.json`,
  `manifest.schema.json` e `custody-event.schema.json`).

---

## Contraditório

Nada de grave. A especificação é internamente consistente em tudo o que foi
lido (SPEC.md completo, ARCHITECTURE.md, ADR-001, VERSIONING.md,
CONFORMANCE.md, GOVERNANCE.md, os quatro schemas NDF, os quatro schemas de
registo). A única tensão a resolver — não é contradição, é sobreposição a
reconciliar — é `despacho.sobre[]` vs. o futuro `relacoes[]` do core (ver
tabela "Parcialmente implementado").

---

## Dependente de validação externa

Confirmado em `docs/normalization/READINESS.md` — gates que **não** devem ser
"resolvidos" por trabalho normativo:

1. fixtures CAdES-B-LTA reais (plano em `CADES-GATE-PLAN.md`, verificador em
   `tools/check_cades_gate.py`, evidência ainda pendente);
2. revisão criptográfica independente;
3. revisão arquivística por especialista;
4. revisão jurídica portuguesa/eIDAS;
5. revisão de acessibilidade;
6. implementação/piloto independente;
7. manifestação de necessidade por utilizadores institucionais;
8. definição de Comissão Técnica NP/CEN/ISO.

---

## Inventário de suporte (para a Fase 1)

- Suite de conformidade NDF: 6 casos válidos, 14 inválidos, em
  `conformance/ndf/`.
- Tipos de documento registados: `oficio`, `despacho`, `informacao-tecnica`,
  `modelo3-irs` (`specs/registry/schemas/`).
- Ferramentas de validação: `tools/validate.py` (runner principal),
  `tools/canonicalize.py`, `tools/check_custody.py`,
  `tools/check_cades_gate.py`, `tools/build_requirements_index.py`,
  `tools/audit_normative.py`, entre outras — todas com equivalente `.mjs`
  para alguns casos (JCS, custódia), sinal de verificação cruzada
  Python/JavaScript já em prática.
- CI: `.github/workflows/validate.yml`.

---

## Recomendação para a Fase 1

Avançar para `docs/design/NDF-STABILIZATION-PROPOSAL.md` cobrindo, por ordem
de dependência: (1) modelo de relações no core + reconciliação com
`despacho.sobre[]` e `versao_anterior`/`hash_anterior`; (2) schema `parecer`;
(3) modelo de assinatura autocontida por entrada; (4) bloco `participantes`;
(5) bloco `proveniencia_ia`; (6) padrão de hash agnóstico de algoritmo nos
campos de referência. Cada um com `DECISION REQUIRED` explícito onde a
compatibilidade de versão estiver em causa — e, antes de tudo, resolver
contigo a questão do estado de PR-001.
