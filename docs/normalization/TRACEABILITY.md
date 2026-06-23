# Matriz de rastreabilidade normativa

Esta matriz é mantida à medida que requisitos passam de draft a candidatos.
Cada requisito obrigatório deve receber um identificador estável e apontar para
uma regra de schema, vetor positivo, vetor negativo ou avaliação externa.
O índice requisito-a-requisito é gerado em `REQUIREMENTS.md` por
`tools/build_requirements_index.py`.
Todas as declarações com modalidade normativa, incluindo requisitos
subordinados, são inventariadas em `NORMATIVE-STATEMENTS.md` por
`tools/audit_normative.py`.

| Família / prefixo | Regra automática ou vetor | Evidência atual | Lacuna antes de candidata |
|---|---|---|---|
| `NDF-PROD-*`, `NDF-READ-*`, `NDF-PKG-*` | schemas NDF + verificações semânticas | suite NDF válida/inválida e pacote | casos criptográficos reais |
| `REG-REQ-*` — tipos documentais | `registry/schemas/*.json` | aplicação pelo `validate.py` | vetores dedicados do registo |
| `NCRTF-PROD-*`, `NCRTF-READ-*` | schema + verificações semânticas | suite NCRTF válida/inválida | mapear R1–R6 individualmente |
| `NDT-RENDER-*` — estrutura e renderização | schema + verificações semânticas | 9 casos `NDT-SEM-*` + suite negativa | árvores extraídas e resultados de referência independentes |
| `JCS-REQ-*` — bytes e digest | RFC 8785 + vetores JCS | vetores IEEE-754 incluídos | implementação independente adicional |
| `PKG-REQ-*` — caminhos e inventário | schema do manifesto + verificador | pacote autocontido + 7 vetores negativos | ampliar cobertura de ZIP real |
| `SIG-REQ-*` — assinaturas | verificações cruzadas | exemplo estrutural | fixtures CAdES-B-LTA reais |
| `CUST-REQ-*` — cadeia de custódia | schema + verificador | vetores positivo/negativo | integração WORM/TSA |
| `PORTAL-REQ-*` — portal | OpenAPI | contrato draft | revisão de segurança e privacidade |
| `RENDER-REQ-*` — renderização | perfil do renderizador | texto draft | corpus golden e acessibilidade |
| `BENCH-*` — eficiência | metodologia | medição inicial | corpus representativo |

A revisão de uma versão candidata DEVE expandir esta matriz e NÃO DEVE marcar
um requisito como coberto apenas porque existe prosa relacionada. Até o
inventário requisito a requisito estar concluído, a matriz é uma visão por
famílias e não demonstra cobertura integral.
