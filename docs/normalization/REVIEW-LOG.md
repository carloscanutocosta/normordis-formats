# Registo de revisão pública

## Regras

Cada comentário recebe um identificador estável e não é eliminado. A decisão
e respetiva fundamentação permanecem públicas, incluindo comentários
rejeitados ou parcialmente aceites.

Estados permitidos: `recebido`, `em análise`, `aceite`, `aceite parcialmente`,
`rejeitado`, `retirado`.

## Períodos de revisão

Estados permitidos para um período: `preparação`, `adiado`, `aberto`,
`encerrado`.

| Revisão | Âmbito | Início | Fim | Versão ou commit | Estado |
|---|---|---|---|---|---|
| PR-001 | NDF 1.0.0, NDT 2.0.0 e NCRTF 2.0.0 | por condição, não por data | a fixar na abertura | a fixar na abertura | **adiado** (2026-08-11) |

### PR-001 — adiamento e condição de abertura

A janela originalmente proposta (2026-07-01 a 2026-08-15) **não foi aberta** e
é dada por caduca. Nenhum comentário foi recebido; nenhum commit foi fixado.

Por decisão de sequenciamento de 2026-08-11 (D1, registada em
[`../../ROADMAP.md`](../../ROADMAP.md) e fundamentada em
[`../reports/READINESS-ASSESSMENT.md`](../reports/READINESS-ASSESSMENT.md)), o
critério de abertura deixa de ser temporal e passa a ser de evidência:

> **PR-001 abre quando `normordis-pdf` produzir, de forma reproduzível por
> terceiros a partir do README, um documento a partir de NDF + NDT.**

Fundamentação: abrir revisão pública sem renderizador funcional convida
comentários sobre o texto e não sobre o comportamento — que é o que a revisão
existe para testar.

`normordis-odf`, quando existir, constitui evidência de segunda implementação
independente do caminho de renderização, mas **não é condição de abertura**.

Na abertura devem ser fixados, e registados nesta tabela: o commit exato sob
revisão, as datas efetivas de início e fim, e os canais de submissão de
comentários previstos em
[`PUBLIC-REVIEW-PLAN.md`](PUBLIC-REVIEW-PLAN.md).

Enquanto PR-001 não abrir, o estado editorial declarado nas especificações é
**Draft — revisão pública por abrir** (nível 1 de
[`../../NORMALIZATION.md`](../../NORMALIZATION.md)), e não «Revisão pública»
(nível 2), que exige um período efetivamente aberto.

## Comentários

| ID | Revisão | Origem/stakeholder | Documento e cláusula | Comentário | Decisão | Fundamentação | Alteração |
|---|---|---|---|---|---|---|---|

Dados pessoais não necessários à rastreabilidade não devem ser registados. A
afiliação ou categoria de stakeholder pode ser usada para avaliar equilíbrio
da participação.
