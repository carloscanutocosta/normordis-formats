# ADR-007: Manter NDF 1.0.0 sem bump durante a preparação da revisão pública

**Estado**: Aceite
**Data**: 2026-08-07
**Decisores**: carloscanutocosta

---

## Contexto

Esta ronda de estabilização introduz seis alterações ao NDF-core e ao
envelope: `relacoes`, `participantes`, `proveniencia_ia`, assinatura
autocontida (ADR-004), padrão de hash agnóstico de algoritmo, e o tipo de
documento `parecer` no registo. `docs/normalization/REVIEW-LOG.md` regista
uma revisão pública planeada (PR-001) para NDF 1.0.0, NDT 2.0.0 e NCRTF
2.0.0, no período 2026-07-01–2026-08-15, em estado `preparação` à data desta
decisão.

## Decisão

Manter `ndf_version: "1.0.0"` (sem bump para 1.1.0 ou 2.0.0). Tratar todas as
alterações desta ronda como parte da própria preparação de PR-001, não como
uma revisão candidata subsequente. Registar as alterações em
`CHANGELOG.md` sob "[Não publicado]".

## Alternativas consideradas

### Publicar 1.0.0 tal como estava e propor esta ronda como candidata a 1.1.0

**Prós**: preservaria byte a byte o schema submetido a revisão pública desde
o primeiro dia.

**Contras**: contraria a decisão explícita do responsável do projeto — esta
ronda foi tratada como parte da própria preparação da revisão, não como
sequela dela. Introduziria também complexidade de manter dois conjuntos de
schemas em paralelo (1.0.0 "publicado" + 1.1.0 "candidato") sem nenhum
consumidor a proteger em nenhum dos dois.

### Bump automático para 1.1.0 por serem todas adições opcionais

**Prós**: seguiria a letra da política SemVer de `VERSIONING.md` para
adições compatíveis.

**Contras**: `GOVERNANCE.md` só exige imutabilidade de artefactos a partir
do estado **Estável** — NDF 1.0.0 está em Draft/Revisão pública, sem revisão
aberta e sem implementação independente conhecida
(`docs/normalization/READINESS.md`, gate 6, confirmado nesta ronda). Não há
compatibilidade retroativa real a preservar com um bump. Rejeitado por
introduzir cerimónia sem benefício correspondente nesta fase do projeto.

## Justificação da decisão

Confirmado explicitamente antes desta decisão: (1) o formato está a ser
criado de raiz, sem revisão pública ainda formalmente aberta; (2) não existe
nenhum consumidor ou implementação externa do NDF. Nestas condições, a
política de versionamento formal (SemVer, imutabilidade de artefactos
publicados) aplica-se a partir do momento em que a especificação for
efetivamente submetida a revisão externa — não durante a sua preparação
interna.

## Consequências

**Positivas**: simplicidade — um único conjunto de schemas, sem necessidade
de reconciliar duas versões em paralelo antes de qualquer revisão externa
ter começado.

**Negativas / mitigações**: se PR-001 já estiver formalmente aberta a
comentário externo no momento em que estas alterações forem publicadas, a
ausência de bump poderia confundir revisores que já tenham começado a
comentar a versão anterior — mitigado por esta ADR e pelo registo explícito
em `CHANGELOG.md`; a decisão foi confirmada como segura antes de aplicar
qualquer alteração de schema.

## Referências

- `docs/design/NDF-STABILIZATION-PROPOSAL.md` §1, §11
- `docs/normalization/REVIEW-LOG.md` (PR-001)
- `VERSIONING.md`, `GOVERNANCE.md`
