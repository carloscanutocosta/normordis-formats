# ADR-010: Separação entre conformidade NDF e Perfil de Ciclo de Vida NORMORDIS

**Estado**: Aceite
**Data**: 2026-08-08
**Decisores**: carloscanutocosta

---

## Contexto

Revisão externa ao estado do repositório (commit `40ef47a`) identificou que
`SPEC.md` mistura dois níveis de exigência distintos sob a mesma bandeira
"conformidade NDF":

1. **Formato**: estrutura do NDF-core, canonicalização, integridade,
   assinaturas, relações, proveniência, empacotamento portátil.
2. **Operação pós-finalização**: transições de estado arquivístico,
   `custody-event.schema.json`, cadeia de hash encadeado, armazenamento
   append-only/WORM, tombstones, autorização de eliminação.

Verificação concreta em `specs/ndf/SPEC.md`:

- `NDF-PROD-010` exige "registar cada transição de estado em log de
  auditoria imutável" como requisito de **produtor NDF conforme**.
- §5.2, passo 8 (sempre obrigatório, via `NDF-PROD-005`) exige
  "armazenamento append-only/WORM" e "criar o evento inicial no log de
  custódia" como parte do **pipeline de finalização**.
- `docs/architecture/ARCHITECTURE.md` §3 declara, em bloco: "Todo o NDF
  finalizado DEVE ter... armazenamento append-only ou WORM com log de
  auditoria" — sem distinguir formato de operação.

Consequência prática: uma entidade com sistema de gestão documental
próprio (ex.: uma administração pública fora de Portugal, ou um sistema
que já tenha o seu próprio modelo de custódia) teria de adotar o modelo
operacional completo do NORMORDIS — estados, log de eventos, WORM,
tombstones — só para produzir um NDF "conforme". Isto é exatamente o tipo
de acoplagem a workflow/sistema que a nota de âmbito do NDF (`LACUNAS.md`)
já tinha excluído para notificação (L11) e delegação (L7/L8) — a
inconsistência é que aqui a mesma categoria de exigência tinha ficado
dentro de `§9`, com requisitos numerados e rastreados.

Nota: `docs/normalization/TRACEABILITY.md` já lista uma família `CUST-REQ-*`
distinta de `NDF-PROD-*`/`NDF-READ-*` — a intenção de separar já existia no
projeto, mas nunca foi realizada até este ADR (`CUST-REQ-*` não tinha
nenhum ID real extraído por `tools/build_requirements_index.py`).

## Decisão

Criar o **Perfil de Ciclo de Vida NORMORDIS** — um conjunto de requisitos
distinto, opcional, com a sua própria família de identificadores
(`CUST-REQ-*`), cobrindo exatamente o que estava indevidamente dentro de
`NDF-PROD-*`. Um produtor ou leitor **PODE** ser NDF 1.0 conforme sem
implementar este perfil.

Nome escolhido deliberadamente **sem** a palavra "custódia" isolada, para
não colidir com "perfil de custódia" já usado em `ARCHITECTURE.md` §4 com
um significado diferente (representação em base de dados vs. `.ndfpkg`
portátil — uma distinção física de armazenamento, não de conformidade
operacional).

### O que se move para o Perfil de Ciclo de Vida NORMORDIS

- Transições de estado arquivístico e o log de auditoria imutável (§2.4.2).
- Armazenamento append-only/WORM.
- Evento terminal de eliminação (§2.4.3).
- Validação da cadeia de eventos (`custody-event.schema.json`,
  `tools/check_custody.py`).

### O que permanece requisito de conformidade NDF

- `estado: "ativo"` no NDF-core finalizado (é imutável, faz parte dos
  bytes assinados — isto é formato, não operação).
- Persistência **atómica** de `payload_bytes` e envelope — nenhuma
  escrita parcial visível. Isto é um requisito mínimo de integridade que
  qualquer produtor precisa de satisfazer, independentemente de adotar
  WORM ou qualquer modelo de custódia específico.
- `avaliacao` (PCA/DF) — é metadado do documento, não comportamento
  operacional; mantém-se no NDF-core tal como estava.

## Alternativas consideradas

### Mover fisicamente `custody-event.schema.json` para outro diretório

**Rejeitado nesta ronda** — o próprio pedido que originou este ADR notou
explicitamente que não é necessário mover ficheiros já. A separação que
importa é normativa (o que conta para "conformidade NDF"), não física
(onde o ficheiro vive no repositório). Pode ser reconsiderado numa futura
reorganização do repositório, sem depender desta decisão.

### Não separar — manter como estava

**Rejeitado**: é precisamente a inconsistência identificada. Mantinha uma
especificação de formato de documento a exigir, na prática, um sistema de
gestão de arquivo completo para ser "conforme".

## Justificação da decisão

O teste já usado em `LACUNAS.md` para separar formato de workflow aplica-se
aqui sem alteração: comportamento que ocorre **depois** da finalização e
que pertence à operação de um sistema (não ao conteúdo assinado do
documento) fica fora da conformidade de formato. A diferença entre este
caso e, por exemplo, notificação (L11) é só que este já tinha IDs
rastreados e texto normativo formal — o que tornava o erro menos óbvio,
não menos real.

## Consequências

**Positivas**: um implementador pode adotar NDF como formato de
documento sem adotar o modelo operacional NORMORDIS inteiro — reduz
significativamente a barreira de adoção externa, incluindo por outras
administrações públicas europeias com os seus próprios sistemas de gestão
documental.

**Negativas / mitigações**: `NDF-PROD-010` muda de conteúdo (deixa de
exigir log de custódia, passa a exigir persistência atómica) — não é
removido nem renumerado, para não perturbar referências já existentes a
essa ID. O requisito de log de custódia não desaparece — é reclassificado
como `CUST-REQ-001`, com o mesmo texto normativo, apenas fora da lista de
"produtor NDF conforme".

**Compatibilidade**: sem impacto em schemas — é uma reclassificação de
requisitos de conformidade em `§9` e clarificação em `§2.4`/`§5.2`/
`ARCHITECTURE.md`, não uma alteração ao NDF-core, envelope ou qualquer
outro schema.

## Referências

- SPEC.md §9.1, §9.5 (novo)
- `docs/architecture/ARCHITECTURE.md` §2.1, §3, §4
- `docs/normalization/TRACEABILITY.md` (família `CUST-REQ-*`)
- `LACUNAS.md` L7, L8, L11 — mesmo princípio de separação formato/workflow
