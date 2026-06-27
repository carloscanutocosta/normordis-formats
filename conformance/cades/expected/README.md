# Modelos de expected.json para fixtures CAdES

Esta pasta contém modelos da expectativa de validação para cada fixture
CAdES.

## Objetivo

Separar a descrição do caso da expectativa de decisão, para que um caso
positivo ou negativo declare de forma uniforme o resultado esperado e o
motivo da decisão.

## Ficheiros

- `expected.template.json` — modelo genérico a copiar para cada caso;
- `expected.example.json` — exemplo preenchido com valores de referência.

## Regra

Cada caso deve manter o seu próprio `expected.json` ao lado dos artefactos
correspondentes. Os ficheiros nesta pasta são apenas modelos e não substituem o
ficheiro por caso.
