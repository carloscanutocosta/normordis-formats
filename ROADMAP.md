# NORMORDIS Roadmap

Estado em: 2026-06-22

---

## Estado actual

| Artefacto | Estado | Versão |
|---|---|---|
| NDF — NORMORDIS Document Format | Draft — Revisão pública | 1.0.0 |
| NDT — NORMORDIS Document Template | Draft — Revisão pública | 2.0.0 |
| NCRTF — NORMORDIS Canonical Rich Text Format | Draft — Revisão pública | 2.0.0 |
| JSON Schema NDF-core | Draft | 1.0.0 |
| Registo de tipos de documento | Draft (4 tipos canónicos) | 1.0.0 |
| Suite de conformidade NDF | Draft + CI verde | 1.0.0 |
| Suite conformidade NDT (válidos + inválidos) | Draft executável + CI verde | 2.0.0 |
| Suite conformidade NCRTF | Draft executável + CI verde | 2.0.0 |
| Cadeia de custódia | Schema + vetores draft | 1.0.0 |
| Portal de verificação | Contrato OpenAPI draft | 1.0.0 |
| CI/GitHub Actions | Operacional (3 jobs) | — |

**Roadmap operacional curto:** ver
[`docs/roadmap/NGI-MVP-2026.md`](docs/roadmap/NGI-MVP-2026.md) para o plano
de demonstração Modelo 3 XML -> NDF -> NDT -> PDF e preparação de candidatura
até outubro de 2026.

---

## Fase 1 — Especificações tecnicamente completas

Objetivo: especificação autocontido e implementável por terceiros sem acesso ao core-documental NORMORDIS.

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
- [x] JSON Schema legível por máquina (`ndf-core.schema.json`, `envelope.schema.json`)
- [x] Registo de tipos (`oficio`, `informacao-tecnica`, `despacho`, `modelo3-irs`)
- [x] Suite de conformidade (válidos + inválidos) — `conformance/ndf/`
- [x] Exemplo `.ndfpkg` autocontido e verificável por hash
- [x] Exemplo render-ready NDF Modelo 3 IRS — `specs/ndf/examples/modelo3-irs-2025.json`
- [x] Conformance test runner NDF + NDT + NCRTF + verificação de pacote (`tools/validate.py`)
- [x] CI/GitHub Actions — pipeline verde em cada push (`50/50` testes)

### NDT

NDT v2.0.0 está tecnicamente especificado e permanece em revisão pública. Ver
[specs/ndt/SPEC.md](specs/ndt/SPEC.md) e
[specs/ndt/CHANGELOG.md](specs/ndt/CHANGELOG.md).

- [x] Axioma layout-puro (sem expressões, sem validação, sem lógica de negócio)
- [x] `paginas_def[]` + `sequencia[]` — modelo multi-página com definições distintas
- [x] Primitivas gráficas: linha, rectangulo, grelha_digitos, imagem, texto_fixo, codigo_barras, poligono, elipse, svg, tabela_visual, assinatura
- [x] `campos[]` — valores NDF escalares posicionados em coordenadas absolutas
- [x] `blocos[]` — tabela (com `min_linhas_visivel`), corpo (NCRTF), cabecalho, rodape
- [x] `fluxo` — layout relativo para documentos administrativos, com `linha_lateral` e `quebra_pagina`
- [x] `estilos` — fonte principal de estilo para renderizadores ODF/HTML
- [x] Modelo de assinatura híbrida CAdES + PAdES (`modo: "hibrido"`)
- [x] Acessibilidade PDF/UA-2 (`alt`, `rotulo_acessivel`, AcroForm `/TU`)
- [x] `incluir_se` em `campos[]`, `blocos[]`, `fluxo.elementos` e `sequencia[]`
- [x] JSON Schema Draft 2020-12 (`specs/ndt/schemas/ndt.schema.json`)
- [x] Exemplos render-ready validados (`specs/ndt/examples/`) — ofício, Modelo 3 Rosto, Anexo A, Anexo G
- [x] Suite de conformidade NDT (`conformance/ndt/valid/` + `conformance/ndt/invalid/`)

---

## Fase 1B — Robustez normativa e de segurança (`LACUNAS.md`)

Origem: revisão adversarial pós-estabilização (2026-08-07), registada em
[`LACUNAS.md`](LACUNAS.md), já recalibrada pelo princípio de âmbito do NDF —
*"formato eficiente para guardar documentos reconstituíveis, não substituto
de workflows específicos de procedimento"*. A maioria dos itens desta fase é
**normativa (texto), não estrutural (schema)** — precisamente porque, após
recalibração, a maior parte do que faltava era dizer com clareza o que o
NDF *não* garante, não acrescentar mais schema.

### Lista de alterações

| # | Origem | Alteração | Tipo | Esforço | Estado |
|---|---|---|---|---|---|
| A1 | L1 | Nota normativa em §2.11.5: relação é afirmação unilateral e assinada, não implica reconhecimento/consentimento do alvo | Texto (SPEC.md) | Baixo | ✅ Feito |
| A3 | L3 | Nota de implementação em §2.11.5: deteção de ciclos é responsabilidade do verificador/renderizador de grafo, o schema não impõe acircularidade entre documentos independentes | Texto (SPEC.md) | Baixo | ✅ Feito |
| A4 | L7 | Nota normativa em §4.4.1: correspondência `papel`↔exigência legal de quem assina é responsabilidade da entidade produtora, não garantida pelo formato (mesmo padrão de §2.10.2) | Texto (SPEC.md) | Baixo | ✅ Feito |
| A5 | L9 | Nota normativa em §2.12.3: `participante_ref` é referência externa não resolvida pelo NDF, por desenho — paralelo explícito a `tipo_classificacao_ref` | Texto (SPEC.md) | Baixo | ✅ Feito |
| A6 | L10 | Nota em §2.12.4: `validador`/`aprovador` descrevem estado de workflow, não conteúdo intrínseco — uso desencorajado fora de sistemas que já os tratem como tal; **não removido do enum** (seria alteração incompatível sem necessidade demonstrada) | Texto (SPEC.md) | Baixo | ✅ Feito |
| A7 | L5 | Verificação semântica: `despacho.sobre[]` e `NDF-core.relacoes` com conjuntos divergentes de `ndf_id` produz aviso (não erro) | Código (`tools/validate.py`, `check_ndf_advisories`) | Médio | ✅ Feito |
| A8 | L8 | Estendido `delegacao_ref` (mesmo padrão de `despacho.decisor`) a `parecer.autor` e `informacao-tecnica.autor` | Schema aditivo (`specs/registry/schemas/`), editado em `1.0.0` — mesma lógica do ADR-007, sem consumidores externos a proteger | Médio | ✅ Feito |
| A9 | L4 | Mecanismo de extensão qualificada `relacoes[].tipo` = `ext.<entidade>.<tipo>`, além do enum fechado (`oneOf`, aditivo) | Schema (`ndf-core.schema.json`) + SPEC.md §2.11.7 + ADR-008 | Alto | ✅ Feito |
| A10 | L6 | Analisado e decidido **não alterar** o formato de `ndf_id` — identificador opaco por desenho; entidade produtora já resolvida por `metadados.entidade_produtora` | ADR-009 + clarificação normativa em SPEC.md §2.3 | Alto | ✅ Feito (fechado por decisão, não por schema) |

**A2 retirado.** A mitigação de fuga de metadados por `relacoes[]` em
documentos classificados é resolvida ao nível do core-documental (pacote
NDF protegido como artefacto opaco — cifra em repouso e em trânsito,
controlo de acesso do sistema custodiante), não por nenhum mecanismo do
NDF. Ver `LACUNAS.md` L2 e
`docs/normalization/NDF-INFORMATIVE-GUIDANCE.md`.

### Roadmap de implementação

**A1, A3–A8 — concluídos.** Todos os itens de baixo/médio esforço da lista
de alterações estão implementados, verificados (`tools/validate.py`
56/56, `check_package_vectors.py` 8/8, `audit_normative.py` e
`build_requirements_index.py` regenerados) e prontos a rever. §1.5
("Confidencialidade e controlo de acesso") também ficou concluída no
mesmo lote, embora não fizesse parte da lista original A1–A10 — emergiu
da mesma revisão adversarial. Fecha, com isto, a secção de Segurança e
Privacidade que tinha ficado por escrever na ronda de estabilização
anterior (mission §13, nunca cumprida até agora).

**A9, A10 — concluídos (2026-08-08).** A9 implementado como alteração
aditiva ao schema (todos os 11 valores base continuam válidos), com
mecanismo de extensão qualificada documentado em SPEC.md §2.11.7 e ADR-008.
A10 fechado por decisão registada em ADR-009: `ndf_id` mantém-se opaco,
sem alteração de schema — a necessidade original (identificar a entidade
produtora) já estava resolvida por `metadados.entidade_produtora`. Com
isto, `LACUNAS.md` fica com os dez pontos totalmente resolvidos: sete
implementados por texto/código, um fechado por decisão de não-alteração
(A10), dois retirados por estarem fora de âmbito (L2, L11).

Verificado: `tools/validate.py` 58/58 (56 + 2 novos casos de conformidade
para A9), `check_package_vectors.py` 8/8, `audit_normative.py` e
`build_requirements_index.py` regenerados sem erros.

**Separação NDF/Perfil de Ciclo de Vida NORMORDIS — concluída
(2026-08-08).** Revisão externa ao commit `40ef47a` identificou acoplagem
indevida entre conformidade de formato e requisitos operacionais de
custódia (`NDF-PROD-010`, §5.2 passo 8, `ARCHITECTURE.md` §2.1/§3).
Resolvido com ADR-010: nova família `CUST-REQ-*` (3 IDs, SPEC.md §9.5),
`NDF-PROD-010` reclassificado para persistência atómica (mesma ID,
conteúdo diferente), e clarificação de que `nivel_assinatura` é uma
declaração do produtor (não uma decisão jurídica do NDF) e que
`validation_code` é intrínseco ao formato, independente de qualquer
serviço específico. `tools/build_requirements_index.py` e
`audit_normative.py` passam a reconhecer `CUST-REQ-*` (54 IDs, antes 51).

---

## Fase 1C — Revisão adversarial pré-RC (concluída, 2026-08-08)

Revisão dirigida a **contradições, redundâncias e requisitos impossíveis de
implementar**, em vez de novas funcionalidades. Relatório completo, com os
16 achados e a resolução de cada um, em
[`docs/reports/NDF-PRE-RC-REVIEW.md`](docs/reports/NDF-PRE-RC-REVIEW.md).

Resultado: todos resolvidos. A decisão de fundo foi a **ADR-011** —
`versao_anterior`/`hash_anterior` removidos do envelope, ficando
`relacoes[{tipo:"substitui"}]` como única representação normativa de
sucessão documental, coberta pela assinatura.

**Lição registada para o processo, não só para o formato:** uma suite de
conformidade verde não demonstra coerência da especificação. Os 58 casos
passavam enquanto três blocos JSON da própria SPEC eram inválidos contra os
schemas que a SPEC torna obrigatórios. A validação passa a ter três camadas
distintas:

```text
correção dos schemas
        ↓
corpus de conformidade
        ↓
coerência SPEC ↔ schemas ↔ exemplos   ← acrescentada nesta fase
```

Guardrails introduzidos, ligados à CI:

| Ferramenta | O que impede |
|---|---|
| `tools/check_spec_coherence.py` | blocos JSON da SPEC inválidos; campos de schema não documentados; referências `§X.Y` quebradas; deriva entre enums duplicados; reaparecimento de propriedades removidas por ADR |
| `tools/build_conformance_index.py` | índice de conformidade desatualizado face aos ficheiros reais |

---

## Fase 2 — Ferramentas de referência (`normordis-tools`)

Ferramentas CLI independentes que demonstram que a especificação é implementável e reduzem o custo de adoção para terceiros. Repositório: `normordis-tools` (separado desta especificação).

### T1 — `normordis-validate`

**Prioridade: crítica.** A ferramenta mais importante para adoção.

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

## Fase 3 — Verificação pública e especificação v1.1.0

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
| Registo remoto `registry.normordis.pt` | Resolução de `tipo_documento_ref` sem acesso ao `.ndfpkg` |
| Suporte a QSCD (eIDAS 2.0 / European Digital Identity Wallet) | Regulamento (UE) 2024/1183 em transposição |
| Extensão qualificada do vocabulário de `relacoes[].tipo` (A9, `LACUNAS.md` L4) | Vocabulário fechado hoje sem via de extensão institucional, inconsistente com o registo de tipos de documento |

---

## Fase 4 — Renderização

### T5 — `normordis-pdf`

**Prioridade: alta para adoção institucional.** A prova mais tangível de que o formato funciona.

Renderizador NDF + NDT → PDF/A-3 (ISO 19005-3). O PDF/A-3 é escolhido para que o NDF-core possa ser embebido como ficheiro anexo ao PDF, tornando o PDF autocontido (PDF + NDF-core no mesmo ficheiro).

```
normordis-pdf --core ndf-core.json --ndt oficio-generico@2.0.0.ndt.json -o documento.pdf
normordis-pdf --pkg documento.ndfpkg -o documento.pdf
normordis-pdf --embed-ndf --core ndf-core.json --ndt *.ndt.json -o documento.pdf  # PDF/A-3 com NDF embebido
```

**Ponto de partida**: os exemplos render-ready em `specs/ndf/examples/` e os NDTs em `specs/ndt/examples/` são o input de referência para validar o renderizador.

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
| Extensões de namespace (`ext.<entidade>`) | Permite que AT, SS, Municípios estendam o NDF-core com campos próprios sem alterar esta especificação base |
| Espaço de nomes por entidade produtora em `ndf_id` (A10, `LACUNAS.md` L6) | Resolvido em conjunto com extensões de namespace, acima — evita duas rondas de alteração incompatível separadas |
| Revisão de `tipo_documento_ref` para URI formal | Alinhamento com Linked Data / European Interoperability Framework |
| Generalização do bloco `avaliacao` (conceito abstrato + perfil PT/DGLAB) | Ver nota "Generalização arquivística europeia" abaixo |

#### Generalização arquivística europeia (nota, sem ação prevista para 1.0)

Identificado em revisão externa (2026-08-08): a ADR-010 desacoplou o NDF do
modelo operacional NORMORDIS (custódia, lifecycle), mas o bloco `avaliacao`
continua semanticamente acoplado ao modelo arquivístico português (PCA,
DF, Lista Consolidada, DGLAB, PGD, Tabela de Seleção — SPEC.md §3). Isto é
aceitável para uma versão 1.0 focada na AP portuguesa, mas é a próxima
questão de generalização a considerar caso o objetivo seja adoção por
outras administrações públicas europeias (relevante para uma eventual
candidatura NGI com âmbito além de Portugal).

Direção a explorar, sem comprometer agora: separar um conceito abstrato de
avaliação arquivística (`retention_classification`, `retention_period`,
`disposition`, `governing_instrument` — nomes ilustrativos) de um perfil
`PT-DGLAB` que o instancia com os termos portugueses atuais
(`tipo_classificacao_ref`, PCA, DF). Não decidido nem desenhado — registo
da questão para não se perder, não uma proposta.

### NCRTF v2.0.0 ✅

NORMORDIS Canonical Rich Text Format — conteúdo de texto estruturado para campos `corpo` e equivalentes. Independente de editores (Lexical, ProseMirror, etc.); canonicalizável via JCS/RFC 8785; armazenado diretamente como valor JSON no NDF-core (por exemplo, `documento.corpo`). Suporta parágrafos, títulos, listas, tabelas, imagens por referência, citações e marcas inline. NDTs referenciam conteúdo NCRTF por caminhos relativos a `NDF-core.documento`.

---

## Fase 6 — Normalização técnica

**Objetivo expresso do projeto**: NDF, NDT e NCRTF tornarem-se standards técnicos sérios — NP (Norma Portuguesa), EN (Norma Europeia), ou ISO/IEC — adoptáveis por terceiros sem dependência da implementação NORMORDIS.

### Caminho de normalização

```
NP — via IPQ/Comissão Técnica competente
EN — via CEN/Comité Técnico competente
ISO — via membro nacional e ISO/TC competente (provavelmente TC 46/SC 11 e/ou TC 171)

Estas vias não formam uma sequência obrigatória. O projeto pode começar em
Portugal, seguir em paralelo com CEN ou ser proposto diretamente ao comité ISO
competente, desde que demonstre necessidade de mercado e obtenha apoio dos
membros.
```

### Estado da maturidade arquitectural (2026-06-22)

O conjunto NDF + NDT + NCRTF tem hoje a profundidade técnica necessária:

| Critério | Estado |
|---|---|
| Separação de âmbitos | ✅ Definida; revisão cruzada contínua |
| Referências a standards reais (ISO 14289-2, ISO 19005-3, ETSI EN 319 122, ISO/IEC 26300) | ✅ Completo |
| Cláusulas de conformidade com comportamento observável | Parcial; falta inventário requisito a requisito |
| Schema legível por máquina (JSON Schema Draft 2020-12) | ✅ NDF-core + envelope + manifest + NDT + NCRTF + registry (4 tipos) |
| Exemplos concretos validados contra schema | ✅ NDT + NDF, incluindo render-ready Modelo 3 IRS |
| Suite de conformidade executável com CI | ✅ 50/50 testes, pipeline verde em cada push |
| Termos e modelo de endereçamento canónico | Parcial; falta converter glossários para termos e definições controlados |

### Gaps editoriais para normalização

O trabalho restante é editorial, processual e de validação independente. Não
estão previstas alterações arquiteturais de fundo, mas a revisão pode revelar
correções técnicas.

| Gap | O que é necessário |
|---|---|
| **Linguagem normativa** | Aplicar a política editorial e eliminar formas normativas ambíguas nos três textos |
| **Secção "Termos e definições"** | Formato ISO 10241 (não glossário livre) — entradas com forma verbal, domínio, definição, nota |
| **Secção "Referências normativas"** | Secção própria com citações ISO formais (número, título, ano); separar de referências informativas |
| **Suite de conformidade executável** | Runner automatizado existente; expandir até cobrir cada requisito individualmente |
| **Implementações e adoção independente** | Produzir evidência de implementabilidade e necessidade de mercado; múltiplas implementações são desejáveis, mas não constituem requisito ISO universal |
| **Estrutura de anexos** | Distinguir Annex A normativo de Annex B informativo; mover exemplos para anexo informativo |

### Pré-requisitos antes de submeter a NP

1. **Congelamento editorial** — NDF, NDT e NCRTF com linguagem e estrutura uniformes
2. **Suite de conformidade executável** — runner existente ✅, a expandir até cobrir cada requisito normativo
3. **Implementação e pilotos independentes** — evidência recomendada de implementabilidade, interoperabilidade e necessidade real
4. **Base terminológica bilingue** — necessária para uma tradução controlada; não é apresentada como requisito ISO universal

### Estimativa de esforço editorial (passagem de especificação draft → NP)

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

normordis-spec (esta repo) ← todas as ferramentas (implementam a especificação)
```
