# ADR-006: Participantes distintos de signatários

**Estado**: Aceite
**Data**: 2026-08-07
**Decisores**: carloscanutocosta

---

## Contexto

Autoria, participação, autenticação e assinatura eletrónica são conceitos
distintos. Antes desta decisão, o NDF só registava identidade em dois
lugares, ambos acoplados a um propósito específico: `signatario` no envelope
(quem assinou, com certificado) e, nalguns tipos de documento do registo,
campos próprios como `informacao-tecnica.autor` ou `despacho.decisor`
(texto de exibição, sem estrutura comum entre tipos).

## Decisão

Introduzir um bloco opcional `participantes` no NDF-core, com
`participante_ref` (identificador institucional estável), `tipo` (pessoa,
sistema, entidade) e `papel` (autor, coautor, revisor_humano, validador,
aprovador, decisor, representante, entidade_produtora, sistema_tecnico) —
independente de `assinaturas[].signatario`.

## Alternativas consideradas

### Fundir `participantes` com os campos de autoria já existentes no registo

**Prós**: eliminaria redundância entre, por exemplo, `informacao-tecnica.autor`
e uma entrada `participantes` com `papel: "autor"` para a mesma pessoa.

**Contras**: exigiria alterar todos os schemas de tipo de documento do
registo na mesma ronda, incluindo os já publicados (`oficio`,
`informacao-tecnica`, `despacho`), fora do âmbito proporcional desta
estabilização. Os campos existentes servem também a apresentação (NDT/PDF)
com dados de exibição (nome, cargo) que não são o propósito de
`participante_ref` (identificador estável, não nome de exibição). Rejeitado
nesta ronda — registado como dívida técnica.

### Registar apenas em `assinaturas[].papel` (ADR-004), sem bloco `participantes` separado

**Prós**: menos um bloco no schema.

**Contras**: não cobre participantes que não assinam — um autor cujo
trabalho é incorporado num documento assinado só por um aprovador não
apareceria em lado nenhum. O princípio "nem todo o autor assina, nem todo o
signatário é autor" (brainstorming original) exige um registo independente
da assinatura.

## Justificação da decisão

A distinção entre `papel` de uma assinatura (ADR-004 — o que uma pessoa fez
*ao assinar este documento*) e `papel` de um participante (o que uma pessoa
ou sistema fez *na produção deste documento*, com ou sem assinatura) é
propositadamente mantida como dois eixos independentes, porque correspondem
a factos diferentes: uma pessoa pode ser autora sem assinar; um signatário
pode assinar como aprovador ou representante sem ser autor material.

Um sistema de IA pode ser registado como `participante` com
`papel: "sistema_tecnico"` — nunca com um papel que implique autoria,
aprovação ou decisão (ver ADR-005, §2.13.4).

## Consequências

**Positivas**: estrutura de consulta/auditoria uniforme entre tipos de
documento, independente de campos de exibição específicos de cada tipo.

**Negativas / mitigações**: redundância consciente e não resolvida entre
`participantes` e campos de autoria do registo (`informacao-tecnica.autor`,
`despacho.decisor`) quando ambos preenchidos para a mesma pessoa — aceite
como dívida técnica para uma versão futura, não como decisão de fusão
imediata.

## Nota de superveniência (2026-08-13)

Parcialmente superado por ADR-013 e ADR-012. `participantes` passa a ser um
índice exclusivamente de **pessoas singulares**:

- removido o campo `tipo` (`pessoa` | `sistema` | `entidade`) — sem sistemas
  nem entidades, um campo com um só valor possível é ruído no core
  canonicalizado;
- removidos do enum `papel`: `sistema_tecnico` (um sistema não participa,
  produz — ver ADR-013), `entidade_produtora` (redundante com
  `metadados.entidade_produtora` e com `imputacao` — ver ADR-012),
  `validador` e `aprovador` (estado de fluxo de aprovação, não facto do
  conteúdo — fecha `LACUNAS.md` L10);
- acrescentado `responsavel_tecnico`, para quem responde tecnicamente em nome
  próprio sem representar (contabilista certificado, ROC, autor de termo de
  responsabilidade);
- acrescentado o bloco opcional `qualificacao` (`{ tipo, identificador }`),
  para registar a qualidade profissional quando esta é condição de validade do
  documento.

Enum resultante: `autor`, `coautor`, `revisor_humano`, `decisor`,
`representante`, `responsavel_tecnico`.

Fica também normativo que `participantes` regista apenas intervenção
**observável e identificada** pelo sistema produtor, e que a ausência de uma
entrada **não é prova de ausência de intervenção** — um terceiro que atue com
as credenciais do titular é indistinguível do titular.

A afirmação acima de que um sistema de IA pode ser registado como
`participante` com `papel: "sistema_tecnico"` deixa de ser válida: a IA fica
exclusivamente em `proveniencia_ia`.

## Referências

- SPEC.md §2.12
- ADR-004-assinatura-autocontida.md
- ADR-005-proveniencia-ia.md §2.13.4
- ADR-012-imputacao-juridica.md
- ADR-013-proveniencia-sistema.md
