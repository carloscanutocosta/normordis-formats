# NORMORDIS Roadmap

Estado em: 2026-06-18

---

## Estado actual

| Artefacto | Estado | Versão |
|---|---|---|
| NDF — NORMORDIS Document Format | Draft para implementação | 1.0.0 |
| NDT — NORMORDIS Document Template | Draft para implementação | 2.0.0 |
| NCRTF — NORMORDIS Canonical Rich Text Format | Stub | — |
| JSON Schema NDF-core | Draft | 1.0.0 |
| Registry de tipos de documento | Draft (3 tipos canónicos) | 1.0.0 |
| Suite de conformidade NDF | Draft | 1.0.0 |

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
- [x] Registry de tipos (`oficio`, `informacao-tecnica`, `despacho`)
- [x] Suite de conformidade (válidos + inválidos)
- [x] Exemplo `.ndfpkg` auto-suficiente
- [ ] Conformance test runner (`tools/validate.py`)

### NDT

- [x] `perfil` — `administrativo_simples` / `impresso_complexo` / `misto`
- [x] Primitivas gráficas completas (§8.3.1–8.3.13)
- [x] `campos[]` como mecanismo canónico de posicionamento NDF→NDT
- [x] `funcoes_externas[]` — puras, versionadas, auditáveis
- [x] `resolver` explícito para composição documental
- [x] Recursos `embebido` e `referenciado_por_hash`

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
               --ndt oficio-generico@1.0.0.ndt.json -o documento.ndfpkg

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
- Devolve: entidade produtora, data, tipo de documento, estado actual
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
normordis-pdf --core ndf-core.json --ndt oficio-generico@1.0.0.ndt.json -o documento.pdf
normordis-pdf --pkg documento.ndfpkg -o documento.pdf
normordis-pdf --embed-ndf --core ndf-core.json --ndt *.ndt.json -o documento.pdf  # PDF/A-3 com NDF embebido
```

**Dependências**: T3; motor de layout (Pango/cairo ou equivalente); engine NDT-expr.

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

### NCRTF v1.0.0

Especificação do NORMORDIS Canonical Rich Text Format — conteúdo de texto estruturado (para o campo `corpo` de documentos que hoje usam plain text). Substitui a referência a plain text em `oficio.schema.json` e similares. Alinhamento com subset do formato interno do NORMORDIS.

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
