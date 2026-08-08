# Índice de requisitos normativos

Este ficheiro é gerado por `tools/build_requirements_index.py`. Não deve ser
editado manualmente. A cláusula de origem permanece normativa; esta tabela é
um índice de rastreabilidade.

| ID | Origem | Resumo | Evidência atual |
|---|---|---|---|
| `CUST-REQ-001` | `specs/ndf/SPEC.md:1461` | CUST-REQ-001 — DEVE registar cada transição de estado (§2.4.1) num log de auditoria imutável, validando cada entrada contra custody-event.schema.json e mantendo a cadeia de hash encadeado (§2.4.2). | schema custody-event + `tools/check_custody.py` + `conformance/custody/` — Perfil de Ciclo de Vida NORMORDIS, opcional (não requisito de conformidade NDF) |
| `CUST-REQ-002` | `specs/ndf/SPEC.md:1462` | CUST-REQ-002 — DEVE usar armazenamento append-only ou WORM para payload_bytes, envelope e log de custódia. | schema custody-event + `tools/check_custody.py` + `conformance/custody/` — Perfil de Ciclo de Vida NORMORDIS, opcional (não requisito de conformidade NDF) |
| `CUST-REQ-003` | `specs/ndf/SPEC.md:1463` | CUST-REQ-003 — DEVE aplicar o mecanismo de tombstone (§2.4.3) antes de destruir payload_bytes de um documento elegível para eliminação, preservando validation_code e payload_hash. | schema custody-event + `tools/check_custody.py` + `conformance/custody/` — Perfil de Ciclo de Vida NORMORDIS, opcional (não requisito de conformidade NDF) |
| `NCRTF-PROD-001` | `specs/ncrtf/SPEC.md:677` | NCRTF-PROD-001 — DEVE gerar valores NCRTF que validam contra specs/ncrtf/schemas/ncrtf.schema.json. | schema NCRTF + vetores válidos + regras R1–R6 |
| `NCRTF-PROD-002` | `specs/ncrtf/SPEC.md:678` | NCRTF-PROD-002 — DEVE aplicar todas as regras de canonicalização R1–R6 (§8.2). | schema NCRTF + vetores válidos + regras R1–R6 |
| `NCRTF-PROD-003` | `specs/ncrtf/SPEC.md:679` | NCRTF-PROD-003 — DEVE verificar que JCS(parse(serialize(ncrtf))) == serialize(ncrtf) antes de incorporar o valor num NDF-core. | schema NCRTF + vetores válidos + regras R1–R6 |
| `NCRTF-PROD-004` | `specs/ncrtf/SPEC.md:680` | NCRTF-PROD-004 — NÃO DEVE incluir nós image com ref que não existam no manifest.inventario do .ndfpkg. | schema NCRTF + vetores válidos + regras R1–R6 |
| `NCRTF-PROD-005` | `specs/ncrtf/SPEC.md:681` | NCRTF-PROD-005 — NÃO DEVE incluir src com data URL num NDF-core finalizado — apenas ref. | schema NCRTF + vetores válidos + regras R1–R6 |
| `NCRTF-PROD-006` | `specs/ncrtf/SPEC.md:682` | NCRTF-PROD-006 — DEVE ordenar marks conforme §6.2. | schema NCRTF + vetores válidos + regras R1–R6 |
| `NCRTF-PROD-007` | `specs/ncrtf/SPEC.md:683` | NCRTF-PROD-007 — DEVE fundir nós text contíguos com marcas e font_family idênticos (R2). | schema NCRTF + vetores válidos + regras R1–R6 |
| `NCRTF-READ-001` | `specs/ncrtf/SPEC.md:689` | NCRTF-READ-001 — DEVE rejeitar qualquer valor NCRTF que não valide contra o schema desta versão. | vetores NCRTF válidos e inválidos |
| `NCRTF-READ-002` | `specs/ncrtf/SPEC.md:690` | NCRTF-READ-002 — DEVE rejeitar documentos com marks fora da ordem canónica (R1). | vetores NCRTF válidos e inválidos |
| `NCRTF-READ-003` | `specs/ncrtf/SPEC.md:691` | NCRTF-READ-003 — DEVE rejeitar nós de tipo desconhecido. | vetores NCRTF válidos e inválidos |
| `NCRTF-READ-004` | `specs/ncrtf/SPEC.md:692` | NCRTF-READ-004 — DEVE rejeitar versões NCRTF que não suporte explicitamente. | vetores NCRTF válidos e inválidos |
| `NCRTF-READ-005` | `specs/ncrtf/SPEC.md:693` | NCRTF-READ-005 — DEVE resolver referências image.ref dentro do .ndfpkg corrente. | vetores NCRTF válidos e inválidos |
| `NDF-PKG-001` | `specs/ndf/SPEC.md:1420` | NDF-PKG-001 — DEVE ser um arquivo ZIP válido. | verificador de pacote + exemplo `.ndfpkg` |
| `NDF-PKG-002` | `specs/ndf/SPEC.md:1421` | NDF-PKG-002 — DEVE conter manifest.json, ndf-core.json e envelope.json na raiz do arquivo. | verificador de pacote + exemplo `.ndfpkg` |
| `NDF-PKG-003` | `specs/ndf/SPEC.md:1422` | NDF-PKG-003 — manifest.json DEVE incluir inventário com hash_sha256 de cada ficheiro e os campos obrigatórios definidos em §8.2. | verificador de pacote + exemplo `.ndfpkg` |
| `NDF-PKG-004` | `specs/ndf/SPEC.md:1423` | NDF-PKG-004 — SHA-256(ndf-core.json) DEVE coincidir com manifest.inventario[ndf-core.json].hash_sha256. | verificador de pacote + exemplo `.ndfpkg` |
| `NDF-PKG-005` | `specs/ndf/SPEC.md:1424` | NDF-PKG-005 — ndf-core.json DEVE ser um NDF-core conforme (§9.1). | verificador de pacote + exemplo `.ndfpkg` |
| `NDF-PKG-006` | `specs/ndf/SPEC.md:1425` | NDF-PKG-006 — O NDT referenciado por ndt_version_ref DEVE estar presente em ndt/<schema_id>@<versao>.ndt.json. | verificador de pacote + exemplo `.ndfpkg` |
| `NDF-PROD-001` | `specs/ndf/SPEC.md:1381` | NDF-PROD-001 — DEVE gerar NDF-core JSON que valida contra o schema specs/ndf/schemas/ndf-core.schema.json (JSON Schema Draft 2020-12). | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-002` | `specs/ndf/SPEC.md:1382` | NDF-PROD-002 — DEVE canonicalizar o NDF-core via JCS (RFC 8785) produzindo payload_bytes determinísticos — bytes idênticos para a mesma estrutura lógica independentemente da ordem de inserção de chaves ou formatação de origem. | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-003` | `specs/ndf/SPEC.md:1383` | NDF-PROD-003 — DEVE calcular payload_hash = SHA-256(payload_bytes) conforme NIST FIPS 180-4. | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-004` | `specs/ndf/SPEC.md:1384` | NDF-PROD-004 — DEVE calcular validation_code conforme o algoritmo definido em §4.6.2. | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-005` | `specs/ndf/SPEC.md:1385` | NDF-PROD-005 — DEVE executar os passos do pipeline de finalização conforme nivel_assinatura declarado (§5.2): | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-006` | `specs/ndf/SPEC.md:1388` | NDF-PROD-006 — DEVE incluir todos os campos obrigatórios de metadados (§2.7.2), incluindo os condicionais RGPD quando contem_dados_pessoais: true. | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-007` | `specs/ndf/SPEC.md:1389` | NDF-PROD-007 — DEVE definir tipo_classificacao_ref no formato <instrumento>/<codigo> (§3.2.1). | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-008` | `specs/ndf/SPEC.md:1390` | NDF-PROD-008 — DEVE gerar ndf_id como UUID v4 válido (RFC 9562), único no espaço de nomes do sistema produtor. | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-009` | `specs/ndf/SPEC.md:1391` | NDF-PROD-009 — DEVE definir estado: "ativo" no NDF-core de qualquer documento recém-finalizado. | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-010` | `specs/ndf/SPEC.md:1392` | NDF-PROD-010 — DEVE persistir payload_bytes e o envelope de forma atómica — nenhuma escrita parcial ou inconsistente entre os dois deve ficar visível a um leitor (§5.2, passo 8). Não inclui o Perfil de Ciclo de Vida NORMORDIS — ver §9.5. | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-011` | `specs/ndf/SPEC.md:1393` | NDF-PROD-011 — DEVE produzir saídas aceites pelo validador e pelas verificações semânticas oficiais; os casos válidos são referências de interoperabilidade, não entradas do produtor. todos os casos de conformance/ndf/valid/ sem erro. | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-012` | `specs/ndf/SPEC.md:1394` | NDF-PROD-012 — DEVE, quando relacoes estiver presente, incluir em cada elemento tipo, alvo.ndf_id e alvo.payload_hash (§2.11). | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-013` | `specs/ndf/SPEC.md:1395` | NDF-PROD-013 — DEVE incluir intervencoes com pelo menos um elemento quando proveniencia_ia.utilizada for true, e omitir ou esvaziar intervencoes quando for false (§2.13). | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-PROD-014` | `specs/ndf/SPEC.md:1396` | NDF-PROD-014 — DEVE incluir revisao_humana.estado em cada elemento de proveniencia_ia.intervencoes, e revisor_ref+revisto_em quando o estado for terminal (§2.13.3). | schema NDF + `conformance/ndf/valid/` + verificações semânticas |
| `NDF-READ-001` | `specs/ndf/SPEC.md:1402` | NDF-READ-001 — DEVE rejeitar qualquer NDF-core que não valide contra o schema desta versão. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-002` | `specs/ndf/SPEC.md:1403` | NDF-READ-002 — DEVE rejeitar versões NDF não suportadas explicitamente ou tratá-las como opacas, sem declarar interpretação completa. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-003` | `specs/ndf/SPEC.md:1404` | NDF-READ-003 — NÃO DEVE ignorar silenciosamente conteúdo assinado desconhecido. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-004` | `specs/ndf/SPEC.md:1405` | NDF-READ-004 — DEVE verificar SHA-256(payload_bytes) == payload_hash antes de aceitar um documento como íntegro. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-005` | `specs/ndf/SPEC.md:1406` | NDF-READ-005 — DEVE verificar validation_code recalculando o digest conforme §4.6.2. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-006` | `specs/ndf/SPEC.md:1407` | NDF-READ-006 — DEVE, quando nivel_assinatura ∈ {"avancada", "qualificada"}, validar a assinatura CAdES-B-LTA e os timestamps RFC 3161. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-007` | `specs/ndf/SPEC.md:1408` | NDF-READ-007 — NÃO DEVE aceitar um documento assinado com certificado incompatível com o nivel_assinatura declarado. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-008` | `specs/ndf/SPEC.md:1409` | NDF-READ-008 — DEVE considerar inválido um pacote onde assinatura original, timestamps ou material de validação obrigatórios estejam ausentes ou alterados. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-009` | `specs/ndf/SPEC.md:1410` | NDF-READ-009 — DEVE rejeitar todos os casos de conformance/ndf/invalid/. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-010` | `specs/ndf/SPEC.md:1411` | NDF-READ-010 — DEVE aceitar todos os casos de conformance/ndf/valid/. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-011` | `specs/ndf/SPEC.md:1412` | NDF-READ-011 — DEVE rejeitar uma relação em relacoes sem alvo.payload_hash, ou com alvo.payload_hash em formato inválido, ou com tipo fora do vocabulário base fechado de §2.11.2 e fora do formato de extensão qualificada de §2.11.7. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-012` | `specs/ndf/SPEC.md:1413` | NDF-READ-012 — DEVE rejeitar proveniencia_ia com utilizada: false e intervencoes não vazio. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDF-READ-013` | `specs/ndf/SPEC.md:1414` | NDF-READ-013 — DEVE rejeitar uma intervenção de proveniencia_ia com estado de revisão terminal (revisto_e_aprovado, revisto_com_alteracoes ou rejeitado) sem revisor_ref ou sem revisto_em. | `conformance/ndf/valid/` e `conformance/ndf/invalid/` |
| `NDT-RENDER-001` | `specs/ndt/RENDERER-CONFORMANCE.md:12` | - NDT-RENDER-001 — verificar versão NDT e referências semânticas antes de renderizar; | suite NDT; resultados de referência pendentes quando aplicável |
| `NDT-RENDER-002` | `specs/ndt/RENDERER-CONFORMANCE.md:13` | - NDT-RENDER-002 — resolver caminhos relativamente a NDF-core.documento; | suite NDT; resultados de referência pendentes quando aplicável |
| `NDT-RENDER-003` | `specs/ndt/RENDERER-CONFORMANCE.md:14` | - NDT-RENDER-003 — rejeitar recursos obrigatórios ausentes ou com hash incorreto; | suite NDT; resultados de referência pendentes quando aplicável |
| `NDT-RENDER-004` | `specs/ndt/RENDERER-CONFORMANCE.md:15` | - NDT-RENDER-004 — preservar texto, ordem, ligações, listas, tabelas e texto alternativo NCRTF; | suite NDT; resultados de referência pendentes quando aplicável |
| `NDT-RENDER-005` | `specs/ndt/RENDERER-CONFORMANCE.md:16` | - NDT-RENDER-005 — comunicar capacidades de saída não suportadas em vez de declarar | suite NDT; resultados de referência pendentes quando aplicável |
| `NDT-RENDER-006` | `specs/ndt/RENDERER-CONFORMANCE.md:18` | - NDT-RENDER-006 — registar nome e versão do renderizador e perfil de saída num relatório. | suite NDT; resultados de referência pendentes quando aplicável |

Total: **54 requisitos identificados**.
