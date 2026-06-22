# NORMORDIS Roadmap

Estado em: 2026-06-22

---

## Estado actual

| Artefacto | Estado | Versão |
|---|---|---|
| NDF — NORMORDIS Document Format | Draft para implementação | 1.0.0 |
| NDT — NORMORDIS Document Template | Draft para implementação | 2.0.0 |
| NCRTF — NORMORDIS Canonical Rich Text Format | Estável | 2.0.0 |
| JSON Schema NDF-core | Draft | 1.0.0 |
| Registry de tipos de documento | Draft (4 tipos canónicos) | 1.0.0 |
| Suite de conformidade NDF | Draft + CI verde | 1.0.0 |
| Suite conformidade NDT (válidos + inválidos) | Draft executável + CI verde | 2.0.0 |
| Suite conformidade NCRTF | Draft executável + CI verde | 2.0.0 |
| Cadeia de custódia | Schema + vectores draft | 1.0.0 |
| Portal de verificação | Contrato OpenAPI draft | 1.0.0 |
| CI/GitHub Actions | Operacional (3 jobs) | — |

---

## Fase 1 — Spec v1.0.0 estável

Objectivo: spec auto-suficiente e implementável por terceiros sem acesso ao core-documental NORMORDIS.

### NDF

- [x] Campos de topo (`ndf_id`, `payload_hash_alg`, `nivel_assinatura`, `ndt_version_ref`)
- [x] Schema normativo de `metadados` (§2.7) — `entidade_produtora`, RGPD, `classificacao_seguranca`
- [x] Estados de arquivo (`estado`) — mecanismo de transição e log de auditoria (§2.4.1)
- [x] `nivel_assinatura` — enum `nenhuma` / `avancada` / `qualificada` (§2.10)
- [x] `validation_code` — derivação SHA-256 + BASE32, 100 bits (§4.6)
- [x] Pipeline de finalização condicional (§5.2)
- [x] `tipo_classificacao_ref` — formato `<instrumento>/<codigo>` (§3.2.1)
- [x] Requisitos TSA (§4.2.1)
- [x] `versao_anterior` / `hash_anterior` — localização no envelope (§6.2)
- [x] Integridade de arquivo para `nivel_assinatura: "nenhuma"` (§2.10.4)
- [x] JSON Schema machine-readable (`ndf-core.schema.json`, `envelope.schema.json`)
- [x] Registry de tipos (`oficio`, `informacao-tecnica`, `despacho`, `modelo3-irs`)
- [x] Suite de conformidade (válidos + inválidos) — `conformance/ndf/`
- [x] Exemplo `.ndfpkg` auto-suficiente e verificável por hash
- [x] Exemplo render-ready NDF Modelo 3 IRS — `specs/ndf/examples/modelo3-irs-2025.json`
- [x] Conformance test runner NDF + NDT + NCRTF + verificação de pacote (`tools/validate.py`)
- [x] CI/GitHub Actions — pipeline verde em cada push (`50/50` testes)

### NDT

NDT v2.0.0 está especificado e estável. Ver [specs/ndt/SPEC.md](specs/ndt/SPEC.md) e [specs/ndt/CHANGELOG.md](specs/ndt/CHANGELOG.md).

- [x] Axioma layout-puro (sem expressões, sem validação, sem lógica de negócio)
- [x] `paginas_def[]` + `sequencia[]` — modelo multi-página com definições distintas
- [x] Primitivas gráficas: linha, rectangulo, grelha_digitos, imagem, texto_fixo, codigo_barras, poligono, elipse, svg, tabela_visual, assinatura
- [x] `campos[]` — valores NDF escalares posicionados em coordenadas absolutas
- [x] `blocos[]` — tabela (com `min_linhas_visivel`), corpo (NCRTF), cabecalho, rodape
- [x] `fluxo` — layout relativo para documentos administrativos, com `linha_lateral` e `quebra_pagina`
- [x] `estilos` — fonte principal de estilo para renderers ODF/HTML
- [x] Modelo de assinatura híbrida CAdES + PAdES (`modo: "hibrido"`)
- [x] Acessibilidade PDF/UA-2 (`alt`, `rotulo_acessivel`, AcroForm `/TU`)
- [x] `incluir_se` em `campos[]`, `blocos[]`, `fluxo.elementos` e `sequencia[]`
- [x] JSON Schema Draft 2020-12 (`specs/ndt/schemas/ndt.schema.json`)
- [x] Exemplos render-ready validados (`specs/ndt/examples/`) — ofício, Modelo 3 Rosto, Anexo A, Anexo G
- [x] Suite de conformidade NDT (`conformance/ndt/valid/` + `conformance/ndt/invalid/`)

---

## Fase 2 — Ferramentas de referência (`normordis-tools`)

Ferramentas CLI independentes que demonstram que a spec é implementável e reduzem o custo de adopção para terceiros. Repositório: `normordis-tools` (separado desta spec).

### T1 — `normordis-validate`

**Prioridade: crítica.** A ferramenta mais importante para adopção.

Valida um NDF-core JSON contra:
1. JSON Schema (`ndf-core.schema.json`)
2. Regras semânticas que o schema não captura (ex.: condicionais RGPD, integridade de arquivo por `destino_final`)
3. Formato de `tipo_classificacao_ref`
4. Resolubilidade de `tipo_documento_ref` (se registry disponível)

```
normordis-validate ndf-core.json
normordis-validate --strict ndf-core.json     # inclui recomendados como obrigatórios
normordis-validate --suite conformance/ndf/   # corre toda a suite de conformidade
```

**Dependências**: JSON Schema Draft 2020-12; sem dependências de rede.

### T2 — `normordis-canonicalize`

**Prioridade: alta.** Elimina a principal causa de erros de assinatura.

Toma um NDF-core JSON e produz os bytes canónicos JCS (RFC 8785), o `payload_hash`, e o `validation_code`.

```
normordis-canonicalize ndf-core.json                  # escreve payload_bytes para stdout
normordis-canonicalize --hash ndf-core.json            # imprime payload_hash (hex)
normordis-canonicalize --validation-code ndf-core.json # imprime validation_code
normordis-canonicalize --all ndf-core.json             # imprime os três
```

**Dependências**: implementação JCS (RFC 8785); sem dependências de rede.

### T3 — `normordis-pack` / `normordis-inspect`

**Prioridade: média.** Torna o `.ndfpkg` concreto e utilizável.

`normordis-pack`: cria um `.ndfpkg` a partir dos constituintes.
`normordis-inspect`: lê e valida a integridade de um `.ndfpkg` existente.

```
normordis-pack --core ndf-core.json --envelope envelope.json \
               --ndt oficio-generico@2.0.0.ndt.json -o documento.ndfpkg

normordis-inspect documento.ndfpkg
normordis-inspect --verify documento.ndfpkg   # verifica hashes do inventário
```

**Dependências**: T1, T2; suporte a ZIP.

### T4 — `normordis-verify`

**Prioridade: média.** Verificação end-to-end da cadeia de autenticidade.

Toma um `.ndfpkg` e verifica:
1. `sha256(ndf-core.json) == payload_hash` do manifesto
2. Validade das assinaturas CAdES-B-LTA (quando presentes)
3. Validade dos timestamps RFC 3161
4. `validation_code` correcto

```
normordis-verify documento.ndfpkg
normordis-verify --offline documento.ndfpkg   # sem acesso a OCSP/CRL online
normordis-verify --at "2030-01-01" documento.ndfpkg  # verifica como se fosse nessa data
```

**Dependências**: T3; biblioteca CAdES; TSA trust store.

---

## Fase 3 — Verificação pública e spec v1.1.0

### Portal `validar.normordis.pt`

Interface pública de verificação de `validation_code`. Um cidadão, auditor, ou sistema automatizado insere o código impresso num documento e obtém confirmação de autenticidade.

- Lookup de `validation_code` em base de dados de NDFs publicados
- Recalcula e compara `payload_hash` antes de responder
- Valida assinatura ou selo CAdES quando existente e distingue claramente
  documento assinado, selado e apenas sob custódia
- Devolve: entidade produtora, data, tipo, estado actual, resultado de
  integridade, resultado de autenticidade e nível de assinatura
- Para `nivel_assinatura: "nenhuma"`, a autenticidade institucional resulta da
  custódia do registo pelo portal; não é apresentada como assinatura pessoal
- API REST documentada (OpenAPI) para integração com outros sistemas
- Verificação offline descrita na página (não requer o portal)

**Dependências**: T4; infraestrutura NORMORDIS.

### NDF v1.1.0

| Item | Motivação |
|---|---|
| Agility de algoritmo criptográfico — mecanismo de re-selagem | CAdES-B-LTA mitiga mas não elimina o risco de SHA-256 comprometido a 20+ anos |
| Categorias especiais de dados (RGPD Art.º 9.º) | Dados de saúde, biométricos — schema mais granular em `metadados` |
| Registry remoto `registry.normordis.pt` | Resolução de `tipo_documento_ref` sem acesso ao `.ndfpkg` |
| Suporte a QSCD (eIDAS 2.0 / European Digital Identity Wallet) | Regulamento (UE) 2024/1183 em transposição |

---

## Fase 4 — Renderização

### T5 — `normordis-pdf`

**Prioridade: alta para adopção institucional.** A prova mais tangível de que o formato funciona.

Renderizador NDF + NDT → PDF/A-3 (ISO 19005-3). O PDF/A-3 é escolhido para que o NDF-core possa ser embebido como ficheiro anexo ao PDF, tornando o PDF auto-suficiente (PDF + NDF-core no mesmo ficheiro).

```
normordis-pdf --core ndf-core.json --ndt oficio-generico@2.0.0.ndt.json -o documento.pdf
normordis-pdf --pkg documento.ndfpkg -o documento.pdf
normordis-pdf --embed-ndf --core ndf-core.json --ndt *.ndt.json -o documento.pdf  # PDF/A-3 com NDF embebido
```

**Ponto de partida**: os exemplos render-ready em `specs/ndf/examples/` e os NDTs em `specs/ndt/examples/` são o input de referência para validar o renderer.

**Dependências**: T3; motor de layout (Pango/cairo ou equivalente); engine NDT.

---

## Fase 5 — Arquivo de longo prazo e extensibilidade

### T6 — `normordis-migrate`

**Prioridade: necessária quando SHA-256 se aproximar de fim de vida.** Prevista para ser necessária por volta de 2035–2040.

Re-selagem periódica: aplica novo timestamp de arquivo (com SHA-3 ou algoritmo posterior) sobre o envelope existente, sem alterar `payload_bytes`.

```
normordis-migrate --pkg documento.ndfpkg --tsa https://tsa.example.pt -o documento-migrado.ndfpkg
normordis-migrate --batch *.ndfpkg --out-dir migrado/
```

**Dependências**: T4; TSA com algoritmos de próxima geração.

### NDF v1.2.0

| Item | Motivação |
|---|---|
| Suporte multi-hash (`sha256` + `sha3-256` em paralelo) | Preparação para transição de algoritmo sem ruptura |
| Perfil de alta confidencialidade | Integração com DL n.º 11/2023 para documentos `secreto` / `muito_secreto` |

### NDF v2.0.0

| Item | Motivação |
|---|---|
| Extensões de namespace (`ext.<entidade>`) | Permite que AT, SS, Municípios estendam o NDF-core com campos próprios sem alterar esta spec base |
| Revisão de `tipo_documento_ref` para URI formal | Alinhamento com Linked Data / European Interoperability Framework |

### NCRTF v2.0.0 ✅

NORMORDIS Canonical Rich Text Format — conteúdo de texto estruturado para campos `corpo` e equivalentes. Independente de editores (Lexical, ProseMirror, etc.); canonicalizável via JCS/RFC 8785; armazenado directamente como valor JSON no NDF-core (por exemplo, `documento.corpo`). Suporta parágrafos, títulos, listas, tabelas, imagens por referência, citações e marcas inline. NDTs referenciam conteúdo NCRTF por caminhos relativos a `NDF-core.documento`.

---

## Fase 6 — Normalização técnica

**Objectivo expresso do projecto**: NDF, NDT e NCRTF tornarem-se standards técnicos sérios — NP (Norma Portuguesa), EN (Norma Europeia), ou ISO/IEC — adoptáveis por terceiros sem dependência da implementação NORMORDIS.

### Caminho de normalização

```
NP — via IPQ/Comissão Técnica competente
EN — via CEN/Comité Técnico competente
ISO — via membro nacional e ISO/TC competente (provavelmente TC 46/SC 11 e/ou TC 171)

Estas vias não formam uma sequência obrigatória. O projecto pode começar em
Portugal, seguir em paralelo com CEN ou ser proposto directamente ao comité ISO
competente, desde que demonstre necessidade de mercado e obtenha apoio dos
membros.
```

### Estado da maturidade arquitectural (2026-06-22)

O conjunto NDF + NDT + NCRTF tem hoje a profundidade técnica necessária:

| Critério | Estado |
|---|---|
| Separação de âmbitos sem sobreposição | ✅ Completo |
| Referências a standards reais (ISO 14289-2, ISO 19005-3, ETSI EN 319 122, ISO/IEC 26300) | ✅ Completo |
| Cláusulas de conformidade com comportamento observável | ✅ Completo |
| Schema machine-readable (JSON Schema Draft 2020-12) | ✅ NDF-core + envelope + manifest + NDT + NCRTF + registry (4 tipos) |
| Exemplos concretos validados contra schema | ✅ NDT + NDF, incluindo render-ready Modelo 3 IRS |
| Suite de conformidade executável com CI | ✅ 50/50 testes, pipeline verde em cada push |
| Glossários e modelo de endereçamento canónico | ✅ Completo |

### Gaps editoriais para normalização

O trabalho restante é **editorial e processual**, não arquitectural:

| Gap | O que é necessário |
|---|---|
| **Linguagem normativa** | RFC 2119 / ISO Directives Part 2 — DEVE/DEVE-SE/PODE em maiúsculas, consistente em todo o texto dos três specs |
| **Secção "Termos e definições"** | Formato ISO 10241 (não glossário livre) — entradas com forma verbal, domínio, definição, nota |
| **Secção "Referências normativas"** | Secção própria com citações ISO formais (número, título, ano); separar de referências informativas |
| **Conformance test suite executável** | ✅ Runner automatizado existente; expandir até cobrir cada requisito SHALL individualmente |
| **Implementações e adopção independente** | Produzir evidência de implementabilidade e necessidade de mercado; múltiplas implementações são desejáveis, mas não constituem requisito ISO universal |
| **Estrutura de anexos** | Distinguir Annex A normativo de Annex B informativo; mover exemplos para anexo informativo |

### Pré-requisitos antes de submeter a NP

1. **Spec freeze v1.0.0** — NDF, NDT, NCRTF com linguagem RFC 2119 e secções ISO
2. **Suite de conformidade executável** — runner existente ✅, a expandir até cobrir cada requisito normativo
3. **Implementação e pilotos independentes** — evidência recomendada de implementabilidade, interoperabilidade e necessidade real
4. **Tradução do glossário** — termos em PT e EN (requisito ISO)

### Estimativa de esforço editorial (passagem de spec draft → NP)

| Tarefa | Estimativa |
|---|---|
| Reformatar linguagem RFC 2119 nos três specs | 2–3 sessões |
| Criar secção "Termos e definições" ISO | 1 sessão |
| Criar secção "Referências normativas" | 1 sessão |
| Reorganizar anexos (normativos vs. informativos) | 1 sessão |
| Suite de conformidade executável (requer T1) | depende de Fase 2 |

---

## Dependências entre ferramentas

```
T2 (canonicalize)
    └── T1 (validate)
            └── T3 (pack/inspect)
                    └── T4 (verify)
                            ├── Portal validar.normordis.pt
                            └── T6 (migrate)
T5 (pdf) ← T3

normordis-spec (esta repo) ← todas as ferramentas (implementam a spec)
```
