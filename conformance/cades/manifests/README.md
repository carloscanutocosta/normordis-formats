# Modelos de manifesto CAdES

Esta pasta contém modelos de manifesto para as fixtures CAdES do projeto.

## Objetivo

Uniformizar os metadados de cada caso antes de existirem artefactos reais,
para que todas as fixtures publiquem a mesma estrutura de origem, hashes,
ambiente e limitação declarada.

## Ficheiros

- `manifest.template.json` — modelo genérico a copiar para cada caso;
- `manifest.example.json` — exemplo preenchido com valores de referência.

## Regra

Cada caso deve manter o seu próprio `manifest.json` ao lado dos artefactos
correspondentes. Os ficheiros nesta pasta são apenas modelos e não substituem o
manifesto por caso.
