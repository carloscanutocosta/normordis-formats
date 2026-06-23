# Política editorial normativa

## 1. Finalidade

Esta política aplica-se ao texto normativo de NDF, NDT e NCRTF. Documentos de
governação, roadmaps, tutoriais e exemplos são informativos, salvo indicação
expressa em contrário.

## 2. Língua e precedência

- A língua normativa do projeto é o português europeu segundo o Acordo
  Ortográfico de 1990.
- Uma tradução inglesa pode ser publicada, mas deve identificar a versão
  portuguesa de origem. Em caso de divergência, prevalece a versão portuguesa.
- Identificadores de dados e nomes próprios não são traduzidos.
- A base terminológica controlada encontra-se em `TERMINOLOGY.md`.
- Termos preferidos: **especificação**, **schema JSON**, **registo**,
  **renderizador**, **versão**, **saída** e **âmbito**.
- Termos ingleses necessários são definidos na primeira ocorrência.

## 3. Estrutura comum

Cada especificação deve conter, por esta ordem, ou justificar a omissão:

1. Objetivo e âmbito;
2. Referências normativas;
3. Termos, definições, símbolos e abreviaturas;
4. Modelo ou arquitetura;
5. Requisitos;
6. Conformidade;
7. Anexos normativos;
8. Anexos informativos;
9. Bibliografia.

Licenciamento, estado, versão e metadados editoriais pertencem ao preâmbulo e
não são cláusulas técnicas. Roadmaps, estimativas, tutoriais, histórico e
justificações extensas não constituem requisitos e devem ficar em anexos
informativos ou documentos separados.

## 4. Linguagem normativa

As formas **DEVE**, **NÃO DEVE**, **RECOMENDA-SE**, **NÃO SE RECOMENDA** e
**PODE**, quando escritas em maiúsculas, exprimem respetivamente requisito,
proibição, recomendação, não recomendação e permissão. O seu significado segue
o BCP 14 (RFC 2119 e RFC 8174).

As formas em minúsculas são exclusivamente narrativas e não criam requisitos.
Um requisito deve:

- identificar um sujeito responsável;
- conter uma única obrigação verificável, sempre que possível;
- evitar termos vagos como “adequado”, “normal”, “rápido” ou “seguro” sem
  critério mensurável;
- receber um identificador estável do papel aplicável (por exemplo,
  `NDF-PROD-nnn`, `NDF-READ-nnn`, `NDT-RENDER-nnn` ou `NCRTF-READ-nnn`)
  quando promovido à base de rastreabilidade.

Notas e exemplos são informativos e não contêm requisitos.

## 5. Referências

Uma referência normativa é indispensável à aplicação de um requisito. Deve
indicar organismo, identificador completo, edição ou data e título oficial.
Séries abertas e referências sem edição só são admitidas quando a própria
especificação define como selecionar a parte e edição aplicáveis.

Referências meramente explicativas pertencem à bibliografia. Antes de cada
versão candidata, os editores verificam substituições, emendas, erratas e
retiradas na fonte oficial.

## 6. Alegações de conformidade

O texto distingue:

- conformidade estrutural com esta especificação;
- suporte técnico a legislação ou normas externas;
- conformidade legal, certificação ou acreditação, que dependem do contexto e
  de avaliação competente.

Uma especificação não “garante validade jurídica”. Pode definir mecanismos que
apoiam objetivos de integridade, autenticidade, preservação ou assinatura.

## 7. Alterações e traduções

Qualquer alteração normativa atualiza conjuntamente texto, schemas, exemplos,
vetores, matriz de rastreabilidade e changelog. Traduções são revistas contra
uma base terminológica bilingue e nunca introduzem requisitos novos.
