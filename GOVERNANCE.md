# Governance

**Estado:** política provisória aplicável enquanto o projeto não for entregue
a uma Comissão Técnica de Normalização.

## Princípios

- As especificações são soberanas e independentes de qualquer implementação.
- Qualquer fornecedor, organização pública ou projeto de código aberto pode implementar
  estas especificações sem dependência das implementações de referência NORMORDIS.
- As alterações às especificações seguem uma política de versionamento (ver [VERSIONING.md](VERSIONING.md)).
- Integridade técnica, autenticidade, assinatura jurídica e apresentação são
  conceitos distintos e não podem ser alterados por mera correção editorial.
- Nenhuma implementação de referência tem autoridade para contradizer o texto
  normativo, schemas e vetores de conformidade publicados.

## Ciclo de Vida das Especificações

As especificações usam exclusivamente os níveis definidos em
[NORMALIZATION.md](NORMALIZATION.md): Conceito, Draft, Revisão pública,
Candidata, Estável, Base candidata a normalização, Descontinuada e Retirada.

O estado deve ser indicado explicitamente em cada especificação publicada.

## Papéis

- **Maintainers:** gerem propostas e versões; não podem declarar conformidade
  sem evidência produzida pela suite pública.
- **Editors:** mantêm texto, schemas, exemplos e testes sincronizados.
- **Responsáveis pelo registo:** aprovam identificadores e asseguram que versões
  publicadas permanecem resolúveis e imutáveis.
- **Reviewers externos:** especialistas de arquivo, segurança, acessibilidade e
  direito chamados para alterações no respetivo domínio.

Uma pessoa pode acumular papéis, mas uma alteração normativa não pode ser
aprovada apenas pelo seu autor. Os participantes devem declarar conflitos de
interesse relevantes para a matéria em apreciação.

## Processo de alteração

1. A proposta identifica problema, âmbito e compatibilidade.
2. Alterações normativas incluem texto, schema e casos de conformidade.
3. Pelo menos um maintainer diferente do autor revê a proposta.
4. Alterações criptográficas, jurídicas ou arquivísticas exigem revisão de um
   especialista do domínio antes de versão publicada estável.
5. A decisão e alternativas rejeitadas são registadas num ADR ou na proposta.

## Consenso, votação e recurso

- O objetivo é o consenso: ausência de objeções sustentadas depois de todos os
  pontos de vista relevantes terem sido considerados.
- Consenso não significa unanimidade nem maioria simples. Uma objeção técnica
  deve receber resposta fundamentada e ficar registada.
- Na ausência de consenso, uma proposta normativa só pode avançar com dois
  terços dos votantes elegíveis, quórum de metade dos membros sem conflito de
  interesse e relatório das posições minoritárias.
- Qualquer participante pode pedir reapreciação por erro processual ou por
  desconsideração de evidência técnica. O recurso é decidido por pessoas que
  não tenham aprovado a decisão contestada.
- Antes de uma versão candidata ou estável existe revisão pública, com prazo,
  lista de comentários, decisão e justificação publicadas em
  `docs/normalization/REVIEW-LOG.md`.

## Compatibilidade

Salvo indicação explícita em contrário:

- versões PATCH não quebram compatibilidade;
- versões MINOR apenas acrescentam capacidades opcionais;
- versões MAJOR podem introduzir alterações incompatíveis.

Uma alteração incompatível deve ser documentada e acompanhada de estratégia de migração.

## Versões e congelamento

- Uma versão estável exige schemas válidos, exemplos válidos, suite integral
  verde e um `.ndfpkg` verificável end-to-end.
- Artefactos de uma versão estável são imutáveis. Correções comportamentais
  originam nova versão; ficheiros publicados não são substituídos in-place.
- Identificadores e URLs de registo publicados nunca são reciclados.

## Conformidade

O projeto publica testes e vetores, mas não concede certificação formal. Uma
 declaração de conformidade deve indicar formato, versão, papel (produtor,
 leitor, renderizador ou verificador), perfil e versão da suite utilizada.

## Propriedade intelectual e patentes

- As contribuições permanecem sujeitas à licença e às declarações indicadas em
  [CONTRIBUTING.md](CONTRIBUTING.md) e `LICENSE-SPEC`.
- Um participante deve revelar, de boa-fé, patentes ou pedidos de patente de que
  tenha conhecimento e que possam ser essenciais à implementação. As
  declarações são registadas em `docs/normalization/IPR-DECLARATIONS.md`.
- O projeto não determina essencialidade nem concede licenças de patente. Uma
  futura submissão fica sujeita à política IPR do organismo competente.
- A transferência editorial deve preservar autoria, proveniência,
  declarações IPR e autorização para o organismo publicar o documento segundo
  as suas próprias regras.

## Transparência

Todas as decisões normativas relevantes devem permanecer publicamente acessíveis através de:

- ADRs
- Issues
- Pull Requests
- Historial Git

A rastreabilidade das decisões faz parte integrante da governação do projeto.

## Normalização futura

Quando uma Comissão Técnica competente assumir o trabalho, as suas regras de
consenso, votação e manutenção prevalecem. A migração deve preservar histórico,
licença aberta, issues, ADRs, comentários, declarações IPR e vetores de
conformidade.
