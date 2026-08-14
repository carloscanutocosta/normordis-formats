# Conformidade

## Finalidade

Este documento define as condições gerais para uma implementação declarar
conformidade com uma especificação NORMORDIS.

## Princípios

- A conformidade é demonstrada por evidência verificável.
- As especificações são normativas; implementações de referência não o são.
- Passar uma suite não transfere autoridade normativa para a implementação.
- Uma declaração é sempre específica de versão, papel e perfil.
- A suite complementa, mas não substitui, requisitos normativos ainda não
  traduzidos em testes.
- Um caso negativo tem de ser rejeitado **pela violação que documenta**.
  Rejeição por defeito acidental não constitui evidência: o caso deixa de
  cobrir a regra sem que a suite o assinale. Ver NDF SPEC.md §9.4.1 e o campo
  `_expected_match` dos casos em `conformance/*/invalid/`.

## Papéis

Uma implementação pode declarar um ou mais papéis:

- produtor;
- leitor;
- renderizador;
- verificador.

Conformidade num papel não implica conformidade noutro.

## Requisitos gerais

Uma implementação conforme DEVE:

- cumprir os requisitos normativos aplicáveis ao papel declarado;
- processar corretamente os vetores oficiais abrangidos pelo perfil;
- declarar as versões suportadas;
- identificar papel, perfil, versão da suite e eventuais limitações;
- disponibilizar resultados reproduzíveis suficientes para sustentar a
  declaração.

## Declaração de conformidade

A declaração DEVE identificar:

- especificação e versão exata;
- papel;
- perfil;
- versão ou hash da suite utilizada;
- implementação, versão e ambiente de execução;
- testes não executados, exceções e limitações conhecidas;
- data da avaliação.

## Certificação

O projeto não fornece certificação, acreditação nem aprovação jurídica. As
declarações são da responsabilidade de quem as emite. Uma futura entidade de
certificação fica sujeita às regras de avaliação da conformidade e acreditação
aplicáveis.
