# Especificação NDF v1.0.0

**NORMORDIS Document Format — Especificação Formal**

Estado: Draft para implementação
Âmbito: documentos gerados internamente pelo core-documental NORMORDIS e normalizados a NDF. Documentos importados/preservados bit-a-bit seguem um regime distinto, fora do âmbito desta especificação.

## Licenciamento

Esta especificação (texto, estrutura, JSON Schemas e exemplos associados) é disponibilizada sob **CC0 1.0** (domínio público). O objetivo é que qualquer produtor de software para a Administração Pública — open source ou proprietário — possa implementar leitura/escrita de NDF/NDT livremente, sem qualquer obrigação contratual ou de licenciamento para com o autor da especificação. Um formato de dados verdadeiramente aberto é o que permite à Administração Pública mudar de fornecedor sem perder acesso aos seus próprios dados — esse é o mecanismo real de soberania digital.

A **implementação de referência** (código-fonte: validadores, serializadores, bibliotecas Rust, `normordis-pdf`, etc.) é distribuída sob licença separada (EUPL v1.2), indicada no respetivo repositório (`LICENSE`). Esta especificação é licenciada separadamente (`LICENSE-SPEC`) precisamente para que a adoção do *formato* não dependa da licença do *código*.

---

## 1. Visão geral

### 1.0 Terminologia normativa

As palavras-chave **DEVE** (*must*), **NÃO DEVE** (*must not*), **RECOMENDADO** (*should*), **NÃO RECOMENDADO** (*should not*), **PODE** (*may*) e **OPCIONAL** (*optional*) nesta especificação são interpretadas conforme o BCP 14 (RFC 2119 e RFC 8174) quando, e apenas quando, aparecem em maiúsculas como aqui apresentadas.

| Palavra-chave | Significado |
|---|---|
| **DEVE** | Requisito absoluto. Uma implementação conforme não pode violar este requisito. |
| **NÃO DEVE** | Proibição absoluta. |
| **RECOMENDADO** | Podem existir razões válidas para não seguir em casos específicos, mas as implicações DEVEM ser compreendidas e pesadas. |
| **NÃO RECOMENDADO** | Podem existir razões válidas para usar em casos específicos, mas as implicações negativas DEVEM ser compreendidas. |
| **PODE** | O item é verdadeiramente opcional — uma implementação pode incluir ou omitir sem perder a designação de conforme. |

### 1.1 Objetivo

O NDF (NORMORDIS Document Format) é o formato canónico de armazenamento de documentos no core-documental. Garante:

- **Integridade e validade jurídica** conforme eIDAS (Regulamento (UE) n.º 910/2014) e DL n.º 12/2021. O nível de assinatura eletrónica é declarado no NDF-core (`nivel_assinatura` — ver §2.10) e varia conforme a natureza jurídica do acto: `"nenhuma"`, `"avancada"` (SEA/AES) ou `"qualificada"` (SEQ/QES). Quando requerido, o envelope CAdES-B-LTA (ETSI EN 319 122) garante validade de longo prazo.
- **Eficiência de armazenamento**, por ser dados estruturados (tipicamente uma a duas ordens de grandeza menor que um binário renderizado equivalente), otimizado para persistência em base de dados relacional (ver §1.5).
- **Reprodutibilidade visual** em qualquer formato de apresentação (PDF/UA-2 como formato primário, ODF e HTML como formatos secundários, ou formato futuro), através da combinação com o NDT (NORMORDIS Document Template — estrutura/layout).
- **Conformidade arquivística** conforme ISO 15489:2016 (Records Management), MoReq2017, o Modelo de Requisitos para Sistemas de Gestão de Arquivos Eletrónicos (MEG/DGLAB) e os instrumentos de avaliação da DGLAB (Lista Consolidada / Tabelas de Seleção).
- **Conformidade legal** com o RGPD (Regulamento (UE) 2016/679) e a Lei n.º 58/2019, respeitando os princípios de minimização de dados, limitação da conservação e os direitos dos titulares (ver §1.6).

### 1.1.1 Normas e regulamentos de referência

| Norma / Regulamento | Âmbito |
|---|---|
| eIDAS — Regulamento (UE) n.º 910/2014 | Assinaturas eletrónicas qualificadas, selos eletrónicos |
| eIDAS 2.0 — Regulamento (UE) 2024/1183 | Revisão eIDAS — European Digital Identity Wallet; QSCD |
| DL n.º 12/2021 | Transposição nacional de eIDAS |
| CPA — Código do Procedimento Administrativo (DL n.º 4/2015) | Forma dos actos administrativos; requisitos de autenticidade (Art.º 61.º) |
| ETSI EN 319 122 | CAdES — nível B-LTA (Long Term Archival) |
| RFC 3161 | Timestamps de confiança |
| RFC 8785 (JCS) | Canonicalização JSON para assinatura |
| ISO 15489:2016 | Gestão de documentos de arquivo (Records Management) |
| MoReq2017 | Modelo de requisitos para sistemas de gestão de arquivos eletrónicos (UE) |
| MEG / DGLAB | Modelo de Requisitos nacional; Lista Consolidada; Tabelas de Seleção |
| RGPD — Regulamento (UE) 2016/679 | Proteção de dados pessoais |
| Lei n.º 58/2019 | Execução nacional do RGPD |

### 1.1.2 Eficiência de armazenamento face a formatos binários

O NDF armazena apenas dados estruturados — sem layout, fontes, imagens de fundo ou páginas não preenchidas. Esta diferença produz ganhos de armazenamento substanciais face a PDF/A.

As estimativas abaixo são calculadas a partir de rácios empíricos observados em documentos reais de referência e estão pendentes de validação formal com corpus representativo da Administração Pública portuguesa. Os valores serão actualizados quando forem disponibilizados dados de medição real.

#### Estimativas por tipo de documento

| Tipo de documento | PDF/A típico | NDF estimado | Rácio estimado |
|---|---|---|---|
| Ofício simples (1–2 pág.) | 80–150 KB | 3–6 KB | 20×–40× |
| Informação técnica (3–5 pág.) | 150–300 KB | 6–12 KB | 15×–30× |
| Despacho / Parecer | 100–250 KB | 4–8 KB | 20×–35× |
| Modelo 3 IRS (rosto + anexos preenchidos) | 800 KB–2 MB | 30–80 KB | 15×–40× |
| Formulário fiscal genérico (1 pág.) | 200–500 KB | 8–20 KB | 15×–30× |

> **Nota metodológica**: o PDF/A inclui fontes embebidas, elementos gráficos do impresso, e todas as páginas de anexos (incluindo as não preenchidas). O NDF contém exclusivamente os campos preenchidos, metadados e avaliação arquivística — não inclui layout nem recursos visuais. O rácio depende da densidade de preenchimento: documentos com muitas secções opcionais vazias têm rácios mais favoráveis ao NDF.

#### Impacto a escala institucional (estimativas)

| Cenário | Volume anual | Armazenamento PDF/A | Armazenamento NDF | Poupança estimada |
|---|---|---|---|---|
| Município médio | 50 000 docs | ~7,5 GB/ano | ~400 MB/ano | ~95% |
| Ministério / Direção-Geral | 500 000 docs | ~75 GB/ano | ~4 GB/ano | ~95% |
| AT — Modelo 3 IRS | 3 500 000 declarações | ~3,5 TB/ano | ~175 GB/ano | ~95% |

Projecção a 10 anos para um município médio: ~75 GB (PDF/A) vs. ~4 GB (NDF) — diferença de uma a duas ordens de grandeza que impacta directamente custos de armazenamento, backup, replicação e transferência para arquivo digital definitivo.

> **Validação empírica pendente**: os valores acima serão substituídos por medições reais quando estiverem disponíveis amostras representativas de documentos produzidos pelo core-documental NORMORDIS. A metodologia de medição (corpus, tipos de documento, densidade de preenchimento) será publicada em `docs/benchmarks/` desta especificação.

### 1.2 Composição

Um NDF completo é composto por três partes logicamente distintas:

```
NDF completo = NDF-core + Envelope
NDF-core + NDT (referenciado) → reprodução visual (PDF, Word, ...)
```

| Parte | Conteúdo | Canonicalizado/assinado? |
|---|---|---|
| **NDF-core** | conteúdo do documento, metadados descritivos, classificação, avaliação arquivística (PCA/DF), referência ao NDT | Sim — é exatamente o que é canonicalizado (JCS) e assinado |
| **Envelope** | assinaturas CAdES-B-LTA, timestamps RFC 3161, material de validação (cadeia de certificados + revogação) | Não — é produzido a partir da assinatura sobre o NDF-core; adicionado depois |

A separação não é arbitrária: o envelope **não pode** fazer parte do que é assinado, sob pena de circularidade (não é possível assinar algo que já contém a própria assinatura sobre si mesmo).

### 1.2.1 Recursos desta especificação

| Recurso | Localização | Descrição |
|---|---|---|
| JSON Schema (NDF-core) | `specs/ndf/schemas/ndf-core.schema.json` | Schema machine-readable do NDF-core completo |
| JSON Schema (Envelope) | `specs/ndf/schemas/envelope.schema.json` | Schema machine-readable do envelope |
| JSON Schema (Manifest) | `specs/ndf/schemas/manifest.schema.json` | Schema machine-readable do manifesto `.ndfpkg` |
| JSON Schema (Custódia) | `specs/ndf/schemas/custody-event.schema.json` | Evento encadeado do log de custódia |
| Registry de tipos de documento | `specs/registry/` | Schemas dos tipos canónicos (`oficio`, `informacao-tecnica`, `despacho`) |
| Suite de conformidade | `conformance/ndf/` | Casos de teste válidos e inválidos para implementações |

### 1.3 Formato de serialização

- **JSON**, não XML. Justificação: o NDF é formato de armazenamento interno do core-documental, não um formato de troca direta com terceiros. Interoperabilidade XML, quando necessária (ex.: SAFT-PT, UBL, eIDAS de outros Estados-Membros), é resolvida por adapters de exportação fora do âmbito desta especificação — o NDF-core é a fonte de verdade a partir da qual tais exportações são derivadas.
- **Canonicalização**: JCS — JSON Canonicalization Scheme, conforme **RFC 8785**, estrito. Garante que a mesma estrutura lógica produz sempre os mesmos bytes, independentemente de ordem de inserção de chaves ou formatação de origem.

### 1.4 Conformidade jurídica e normativa

#### 1.4.1 Matriz de conformidade

A tabela seguinte mapeia cada requisito legal ou normativo à disposição concreta do NDF que o cumpre. Qualquer alteração ao enquadramento jurídico que invalide uma linha desta tabela implica uma actualização da especificação (ver §1.4.2).

| Requisito | Instrumento legal / normativo | Disposição NDF | Secção |
|---|---|---|---|
| Assinatura eletrónica proporcional ao acto | eIDAS, Art.º 25.º–26.º; DL n.º 12/2021; CPA, Art.º 61.º | `nivel_assinatura` no NDF-core: `"nenhuma"` / `"avancada"` (SEA) / `"qualificada"` (SEQ), conforme a natureza jurídica do acto | §2.10 |
| Preservação de longo prazo da assinatura | eIDAS, Art.º 34.º; ETSI EN 319 122 | Nível CAdES-B-LTA; timestamp de arquivo RFC 3161 — obrigatório quando `nivel_assinatura ≠ "nenhuma"` | §4.2, §5.2 |
| Autenticidade e integridade do documento | ISO 15489:2016, §5.2; MoReq2017, R2 | JCS/RFC 8785 + SHA-256 + CAdES sobre `payload_bytes` | §1.3, §4 |
| Imutabilidade do registo | MoReq2017, R3; MEG, R4 | Princípio de imutabilidade; proibição de edição de NDF finalizado | §2.1 |
| Reprodutibilidade / renderização futura | MoReq2017, R5; OAIS/ISO 14721:2012 | `ndt_version_ref` embebido no NDF-core; NDT incluído no `.ndfpkg` | §2.6, §8 |
| Prazo de conservação administrativa (PCA) | MEG/DGLAB, Lista Consolidada | Bloco `avaliacao.prazo_conservacao_administrativa` com `instrumento_avaliacao_versao_ref` | §3 |
| Destino final (conservação / eliminação) | MEG/DGLAB, Tabelas de Seleção | `avaliacao.destino_final`; eliminação no termo do PCA | §3.4 |
| Classificação documental (MEF/MIP) | MEG/DGLAB, Macroestrutura Funcional | `metadados.tipo_classificacao_ref` | §2.7 |
| Cadeia de custódia / proveniência | ISO 15489:2016, §5.3; MoReq2017, R6 | `versao_anterior` + `hash_anterior`; cadeia de NDF imutáveis | §6 |
| Limitação da conservação de dados pessoais | RGPD, Art.º 5.º, n.º 1, al. e) | PCA + `destino_final: eliminacao` aplicado no termo do prazo | §3, §1.6 |
| Minimização de dados pessoais | RGPD, Art.º 5.º, n.º 1, al. c) | NDF armazena apenas campos preenchidos; sem layout nem páginas vazias | §2.8 |
| Direito ao apagamento | RGPD, Art.º 17.º | Eliminação integral no termo do PCA; base legal de conservação prevalente documentada | §1.6 |
| Identificação do responsável pelo tratamento | RGPD, Art.º 13.º–14.º; Lei n.º 58/2019 | `metadados.responsavel_tratamento` obrigatório | §1.6 |
| Categorias especiais de dados pessoais | RGPD, Art.º 9.º | `metadados.categorias_dados_pessoais` (roadmap §1.1.0) | §9 |
| Interoperabilidade com sistemas da AP | Lei n.º 36/2011 (normas abertas); EIF | Formato JSON aberto; especificação CC0; sem dependência de fornecedor | Licenciamento |
| Acesso à informação administrativa | Lei n.º 26/2016 | `.ndfpkg` auto-suficiente; reprodutibilidade sem infraestrutura original | §8 |
| Agility de algoritmo criptográfico | eIDAS, Art.º 34.º (preservação); ETSI EN 319 122, §6 | Re-selagem periódica; roadmap multi-hash | §4.5, §9 |

#### 1.4.2 Política de actualização por mudança de enquadramento jurídico

O enquadramento jurídico e normativo aplicável ao NDF muda periodicamente. A política seguinte define como cada tipo de mudança se traduz numa versão SemVer desta especificação.

**Tipo A — Mudança absorvida por campos de referência (sem nova versão da spec)**

Certas mudanças são absolvidas pelos campos `*_ref` existentes, sem alterar o formato NDF:

| Mudança | Campo absorvente | Acção |
|---|---|---|
| Nova versão da Lista Consolidada DGLAB | `avaliacao.instrumento_avaliacao_versao_ref` | Implementações actualizam o valor; spec não muda |
| Nova portaria de impressos fiscais | `impresso.versao_impresso` no NDT | NDT actualizado; NDF spec não muda |
| Novo algoritmo de assinatura nos certificados qualificados | `envelope.assinaturas[].algoritmo` | Implementações suportam novo algoritmo; spec não muda |

**Tipo B — Nova versão MINOR (campos opcionais adicionados)**

| Mudança | Exemplo | Versão |
|---|---|---|
| Novo campo de metadados obrigatório por regulamento | RGPD Art.º 9.º — categorias especiais | MINOR |
| Nova forma de contagem de PCA reconhecida pelo MEG | `forma_contagem: fim_mandato` | MINOR |
| Novo mecanismo de assinatura suportado | QSCD via eIDAS 2.0 | MINOR |

**Tipo C — Nova versão MAJOR (mudança incompatível)**

| Mudança | Exemplo | Versão |
|---|---|---|
| Alteração de campo obrigatório existente | Renomeação de `avaliacao` exigida por nova regulação | MAJOR |
| Substituição do algoritmo de canonicalização | RFC 8785 substituído por novo standard | MAJOR |
| Mudança de nível de assinatura mínimo obrigatório | eIDAS exige nível superior a CAdES-B-LTA | MAJOR |
| Alteração de semântica de campo existente | `destino_final` passa a ter novos valores incompatíveis | MAJOR |

**Regra de rastreabilidade**: cada versão da especificação que resulte de uma mudança de enquadramento jurídico deve incluir no `CHANGELOG.md` a referência ao instrumento legal ou normativo que a motivou. Exemplo:

```
## [1.1.0] — 2027-01-15
### Motivação legal
- RGPD Art.º 9.º / Orientação CNPD n.º X/2026 — categorias especiais de dados pessoais
### Alterações
- Adicionado: `metadados.categorias_especiais_dados` (opcional)
```

#### 1.4.3 Monitorização do enquadramento jurídico

Instrumentos legais com revisões previstas ou em curso que podem implicar actualizações à especificação:

| Instrumento | Estado | Impacto previsto |
|---|---|---|
| eIDAS 2.0 — Regulamento (UE) 2024/1183 | Em vigor (transposição em curso) | Suporte a QSCD e European Digital Identity Wallet — MINOR |
| Lista Consolidada DGLAB (revisão periódica) | Actualizações regulares | Absorvida por `instrumento_avaliacao_versao_ref` — sem versão |
| Norma MoReq (revisão prevista) | A confirmar | Avaliação quando publicada |
| Revisão do RGPD / Lei n.º 58/2019 | Sem data | A avaliar conforme publicação |

---

### 1.5 Armazenamento em base de dados (informativo)

O NDF é concebido para persistência eficiente, mas não exige base de dados,
produto ou modelo físico. Uma implementação pode usar SQL, object storage,
content-addressed storage, ficheiros WORM ou outra tecnologia, desde que
preserve os bytes e garantias normativas. O exemplo PostgreSQL abaixo é
puramente informativo e não participa na conformidade.

#### Colunas obrigatórias (fonte de verdade)

| Coluna | Tipo PostgreSQL | Conteúdo |
|---|---|---|
| `id` | `uuid` | Identificador único do NDF |
| `payload_bytes` | `bytea` | Bytes canónicos do NDF-core (JCS/RFC 8785) — imutável após finalização; fonte de verdade para verificação de assinatura |
| `envelope` | `jsonb` ou bytes preservados | Metadados do envelope e provas criptográficas; objectos CAdES, timestamps e material de validação são imutáveis e preservados byte a byte |
| `estado` | `text` | `rascunho` \| `finalizado` |
| `criado_em` | `timestamptz` | Data/hora de criação |
| `finalizado_em` | `timestamptz` | Data/hora de finalização; `null` se rascunho |

#### Colunas desnormalizadas para indexação (extraídas de `payload_bytes`)

Metadados estruturalmente estáveis são promovidos a colunas indexáveis para eficiência de pesquisa e filtragem, sem duplicar a fonte de verdade:

| Coluna | Tipo | Origem em NDF-core |
|---|---|---|
| `ndf_version` | `text` | `ndf_version` |
| `tipo_documento_ref` | `text` | `metadados.tipo_documento_ref` |
| `schema_id` | `text` | Derivado de `ndt_version_ref` |
| `destino_final` | `text` | `avaliacao.destino_final` |
| `pca_valor` | `integer` | `avaliacao.prazo_conservacao_administrativa.valor` |
| `pca_unidade` | `text` | `avaliacao.prazo_conservacao_administrativa.unidade` |
| `elegivel_para_destino_em` | `date` | Calculado; não assinado |
| `payload_hash` | `text` | `sha256(payload_bytes)` em hex — para verificação rápida sem reprocessar o payload |

#### JSONB derivado (opcional, para queries ad-hoc)

```sql
-- Coluna gerada, derivada de payload_bytes, para queries ad-hoc
ALTER TABLE ndf ADD COLUMN payload_jsonb jsonb
  GENERATED ALWAYS AS (convert_from(payload_bytes, 'UTF8')::jsonb) STORED;
```

**Regra de integridade**: `payload_bytes` é a única fonte de verdade. O JSONB derivado e as colunas desnormalizadas não podem ser alterados diretamente — qualquer divergência entre `payload_bytes` e as colunas indexáveis é um erro de implementação. A verificação de integridade é feita sempre sobre `sha256(payload_bytes)`, não sobre o JSONB.

### 1.6 Proteção de dados pessoais

O NDF pode conter dados pessoais (NIF, dados fiscais, dados de saúde, dados processuais) sujeitos ao RGPD (Regulamento (UE) 2016/679) e à Lei n.º 58/2019. O princípio de imutabilidade do NDF (§2.1) cria uma tensão com o direito ao apagamento (Art.º 17.º RGPD).

#### Resolução da tensão imutabilidade ↔ direito ao apagamento

A tensão é resolvida pela articulação de três mecanismos legais e técnicos:

1. **Base legal de conservação prevalente**: documentos da Administração Pública são conservados com base em obrigação legal (Art.º 6.º, n.º 1, al. c) RGPD) e missão de interesse público (al. e)). O direito ao apagamento cede face a obrigações legais de conservação (Art.º 17.º, n.º 3, al. b) RGPD) — o PCA/DF resolve esta decisão por tipo de documento.

2. **Pseudonimização pré-arquivo**: quando aplicável, dados pessoais podem ser pseudonimizados antes da finalização. O NDF finalizado contém o pseudónimo; a tabela de correspondência é gerida fora do NDF com controlos de acesso próprios.

3. **Eliminação no termo do PCA**: documentos com `destino_final: eliminacao` são eliminados integralmente (incluindo `payload_bytes` e colunas desnormalizadas) no termo do prazo de conservação administrativa — o mecanismo de arquivo já garante a limitação temporal exigida pelo RGPD.

#### Campos de metadados obrigatórios relativos a proteção de dados

O bloco `metadados` deve incluir:

```json
{
  "metadados": {
    "contem_dados_pessoais": true,
    "categorias_dados_pessoais": ["identificacao_fiscal", "rendimentos"],
    "base_legal_conservacao": "obrigacao_legal",
    "responsavel_tratamento": "string (identificador da entidade)"
  }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `contem_dados_pessoais` | Sim | `true` \| `false` |
| `categorias_dados_pessoais` | Condicional | Obrigatório se `contem_dados_pessoais: true`. Enum aberto: `identificacao_fiscal`, `rendimentos`, `saude`, `dados_processuais`, `outros`. |
| `base_legal_conservacao` | Condicional | Obrigatório se `contem_dados_pessoais: true`. `obrigacao_legal` \| `interesse_publico` \| `consentimento` \| `contrato`. |
| `responsavel_tratamento` | Sim | Identificador da entidade responsável pelo tratamento. |

---

## 2. NDF-core

### 2.1 Princípio de imutabilidade

O NDF-core é **congelado no momento da finalização** do documento. A partir desse momento:

- Os bytes canonicalizados (`payload_bytes`) nunca são reserializados, reordenados, ou alterados.
- Qualquer alteração ao conteúdo lógico requer a criação de um **novo documento NDF**, distinto e igualmente imutável, que referencia o documento anterior (ver §4).
- Não existe o conceito de "edição" de um NDF finalizado.

### 2.2 Estrutura

O NDF-core é um objeto JSON com os seguintes campos de topo:

```json
{
  "ndf_version": "1.0.0",
  "ndf_id": "uuid-v4",
  "estado": "ativo",
  "payload_hash_alg": "sha256",
  "nivel_assinatura": "qualificada",
  "ndt_version_ref": "oficio-generico@1.0.0",
  "metadados": { /* ... ver §2.7 ... */ },
  "documento": { /* ... conteúdo lógico, estrutura definida por metadados.tipo_documento_ref ... */ },
  "avaliacao": { /* ... ver §3 ... */ }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `ndf_version` | Sim | Versão desta especificação. Valor normativo deste documento: `"1.0.0"`. |
| `ndf_id` | Sim | Identificador único do documento. UUID v4, gerado pelo sistema produtor antes da canonicalização. Imutável após finalização. Ver §2.3. |
| `estado` | Sim | Estado de arquivo do documento. Enum fechado — ver §2.4. |
| `payload_hash_alg` | Sim | Algoritmo usado para calcular `payload_hash`. Valor normativo desta versão: `"sha256"` (NIST FIPS 180-4). Ver §2.5. |
| `nivel_assinatura` | Sim | Nível mínimo de assinatura eletrónica exigido pela natureza jurídica do acto. Enum fechado — ver §2.10. |
| `ndt_version_ref` | Sim | Referência normativa ao NDT usado na reprodução visual. Formato: `"schema_id@versao_impresso"`. Ver §2.6. |
| `metadados` | Sim | Metadados descritivos, classificação e conformidade. Schema completo definido em §2.7. |
| `documento` | Sim | Conteúdo lógico do documento. Estrutura definida pelo schema referenciado em `metadados.tipo_documento_ref`. |
| `avaliacao` | Sim | Avaliação arquivística (PCA/DF), conforme MEG/DGLAB. Ver §3. |

Nenhum destes campos PODE estar ausente — a finalização **DEVE falhar** se algum estiver em falta (ver §5).

### 2.3 `ndf_id`

Identificador permanente do documento no ecossistema NORMORDIS.

- **Tipo**: string, formato UUID v4 (RFC 4122) — ex.: `"a1b2c3d4-e5f6-4789-abcd-ef0123456789"`.
- **Geração**: pelo sistema produtor imediatamente antes da canonicalização, nunca depois.
- **Imutabilidade**: faz parte do NDF-core canonicalizado e assinado — não pode ser alterado após finalização.
- **Unicidade**: o sistema produtor DEVE garantir que não existem dois NDF com o mesmo `ndf_id`.
- **Uso**: referência primária em `versao_anterior`, no manifest do `.ndfpkg`, e como chave primária no modelo de DB (§1.5).

### 2.4 Estado de arquivo (`estado`)

O campo `estado` no NDF-core declara o estado do documento **no momento da finalização** — é sempre `"ativo"`. É canonicalizado e assinado como parte do NDF-core e é **imutável** tal como todos os outros campos.

O estado arquivístico corrente ao longo do ciclo de vida do documento é uma propriedade operacional gerida fora do NDF-core: na coluna `estado` da base de dados (§1.5) e no campo `estado` do manifesto `.ndfpkg` (§8.2). O valor no NDF-core não reflecte transições posteriores à finalização.

**Valor normativo**: `"ativo"` — único valor válido no NDF-core no momento da finalização.

#### 2.4.1 Ciclo de vida arquivístico (camada operacional)

Os estados do ciclo de vida são geridos pelo sistema de custódia (GED/GCA) fora do NDF-core. As transições válidas são:

```
ativo → substituido          (nova versão NDF criada — §6)
ativo → em_conservacao       (PCA decorrido)
em_conservacao → conservado_permanentemente   (DF: conservação — transferência para arquivo)
em_conservacao → eliminado                    (DF: eliminação — destruição autorizada)
```

| Estado | Descrição |
|---|---|
| `"ativo"` | Documento em uso activo, dentro do PCA. Estado inicial de todos os NDF. |
| `"substituido"` | Documento supersedido por nova versão na cadeia de proveniência (§6). Imutável no arquivo; não é o documento corrente. |
| `"em_conservacao"` | PCA decorrido; aguarda aplicação do destino final — transferência para arquivo definitivo ou eliminação. |
| `"conservado_permanentemente"` | DF aplicado: conservação permanente. Documento transferido para arquivo definitivo (ex.: DGLAB). |
| `"eliminado"` | DF aplicado: eliminação. `payload_bytes` e envelope destruídos; subsiste um registo tombstone (ver §2.4.3). |

#### 2.4.2 Mecanismo de transição de estado

Cada transição de estado DEVE ser registada num **log de auditoria imutável**, separado do NDF e da sua base de dados operacional. O log é da responsabilidade do sistema de custódia.

Cada entrada DEVE validar contra `custody-event.schema.json`. O `event_hash` é
calculado como `SHA-256(JCS(evento sem a propriedade event_hash))`. No primeiro
evento, `sequence` é `0` e `previous_event_hash` é `null`; nos seguintes,
`sequence` incrementa exactamente uma unidade e `previous_event_hash` coincide
com o `event_hash` anterior. Quebras, duplicações ou reordenações invalidam a
cadeia. A cabeça da cadeia DEVE ser periodicamente ancorada em armazenamento
WORM, selo institucional ou serviço temporal; uma cadeia de hashes sem âncora
externa não impede reescrita integral por um custodiante comprometido.

**Estrutura mínima de cada entrada do log de auditoria**:

```json
{
  "ndf_id": "uuid-v4",
  "estado_anterior": "ativo",
  "estado_novo": "em_conservacao",
  "timestamp": "2031-06-18T10:30:00Z",
  "motivo": "PCA de 5 anos decorrido desde 2026-06-18",
  "actualizador": "sistema-gca-v2.1 / utilizador-id-456",
  "instrumento_legal": "lista-consolidada-dglab-2023-v3/lc/450.10.001"
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `ndf_id` | Sim | Identificador do NDF cujo estado transita. |
| `estado_anterior` | Sim | Estado antes da transição. |
| `estado_novo` | Sim | Estado após a transição. |
| `timestamp` | Sim | Data/hora da transição (ISO 8601, UTC). |
| `motivo` | Sim | Justificação textual — rastreável para auditoria. |
| `actualizador` | Sim | Identidade do sistema e/ou utilizador que efectuou a transição. |
| `instrumento_legal` | Recomendado | Referência ao instrumento (Lista Consolidada, despacho, portaria) que autoriza a transição. |

**Autorização**: a transição `em_conservacao → eliminado` DEVE ser autorizada formalmente pelo `responsavel_tratamento` (§2.7.2) e DEVE referenciar explicitamente o instrumento de avaliação que suporta a decisão de eliminação.

#### 2.4.3 Tombstone de eliminação

Quando `estado` transita para `"eliminado"`, o sistema de custódia DEVE:

1. Destruir `payload_bytes` e todos os campos do envelope excepto `validation_code` e `payload_hash`.
2. Criar um registo tombstone imutável com os seguintes campos mínimos:

```json
{
  "ndf_id": "uuid-v4",
  "payload_hash": "sha256:<hex>",
  "validation_code": "NDF-XXXXX-XXXXX-XXXXX-XXXXX",
  "data_eliminacao": "2031-06-18T10:30:00Z",
  "motivo_eliminacao": "Destino final: eliminação. PCA de 5 anos decorrido.",
  "instrumento_avaliacao_versao_ref": "lc/lista-consolidada-dglab-2023-v3",
  "tipo_classificacao_ref": "lc/450.10.001"
}
```

O tombstone garante rastreabilidade sem preservar os dados eliminados: `validation_code` e `payload_hash` permitem confirmar que o documento existiu e foi destruído de forma autorizada.

### 2.5 Algoritmo de hash (`payload_hash_alg`)

O campo `payload_hash_alg` declara o algoritmo usado para calcular o digest sobre o qual recai a assinatura CAdES.

**Valor normativo para NDF v1.x**: `"sha256"` — SHA-256 conforme NIST FIPS 180-4. Este é o único valor válido nesta versão da especificação.

Justificação: SHA-256 é amplamente suportado pelos perfis e bibliotecas CAdES
e TSP relevantes. A conformidade jurídica e criptográfica depende também da
política de algoritmos aplicável no instante de assinatura; nem o eIDAS nem o
RFC 3161 fixam SHA-256 como único algoritmo para sempre.

A transição para suporte a múltiplos algoritmos em paralelo (`"sha256"` + `"sha3-256"`) está prevista na versão 1.2.0 desta especificação (ver §9 — Roadmap).

### 2.6 `ndt_version_ref`

Identifica univocamente a versão do NDT com que o NDF-core deve ser combinado para reprodução visual.

**Formato normativo**: `"<schema_id>@<versao_ndt>"`, onde:
- `schema_id` é o identificador estável do tipo de documento no NDT (ex.: `"oficio-generico"`, `"modelo3-irs"`).
- `versao_ndt` é a versão do template NDT (ex.: `"1.0.0"` para documentos administrativos; `"2026.1"` para impressos fiscais com versão anual).

Exemplos válidos:
```
"oficio-generico@1.0.0"
"modelo3-irs@2026.1"
"informacao-tecnica@2.3.1"
```

- **Imutabilidade**: faz parte do NDF-core canonicalizado e assinado.
- **Resolução**: o NDT referenciado deve estar disponível no `.ndfpkg` (§8) ou num registry conforme.

#### 2.6.1 Distinção entre `ndt_version_ref` e `tipo_documento_ref`

Estes dois campos referenciam conceitos distintos e independentes:

| Campo | Referencia | Determina |
|---|---|---|
| `metadados.tipo_documento_ref` | Schema do tipo de documento (ex.: `"oficio@1.0.0"`) | Estrutura de `documento` no NDF-core — o modelo de dados |
| `ndt_version_ref` | Template de layout (ex.: `"oficio-generico@1.0.0"`) | Como o documento é renderizado visualmente — o layout |

Para a maioria dos tipos de documento, os dois são 1:1 — um único NDT serve um único schema. No entanto, são referências independentes porque:

- O mesmo tipo de documento pode ter **múltiplos NDTs** (ex.: versão simplificada e versão completa de um formulário; versão A4 e versão Letter para exportação).
- O schema de `documento` (`tipo_documento_ref`) evolui independentemente do layout (`ndt_version_ref`) — uma actualização visual do impresso não altera a estrutura de dados e vice-versa.
- Um mesmo NDT pode, em teoria, servir múltiplas versões patch do mesmo schema de documento.

O registry (`specs/registry/`) mantém a correspondência canónica entre tipos de documento e os seus NDTs de referência.

### 2.7 `metadados` — schema normativo

O bloco `metadados` contém os campos descritivos transversais a qualquer tipo de documento NDF, independentes do conteúdo lógico (que fica em `documento`). É canonicalizado e assinado como parte do NDF-core.

#### 2.7.1 Estrutura de referência

```json
{
  "metadados": {
    "tipo_documento_ref": "oficio@1.0.0",
    "entidade_produtora": {
      "designacao": "Direção-Geral de Exemplo",
      "nif": "123456789",
      "codigo_dglab": "PT-DGE-000"
    },
    "assunto": "Resposta ao ofício n.º 123/2026",
    "numero_referencia": "OF/2026/00123",
    "processo_ref": "proc.º 456/2026",
    "idioma": "pt",
    "classificacao_seguranca": "uso_interno",
    "contem_dados_pessoais": false,
    "categorias_dados_pessoais": [],
    "base_legal_conservacao": null,
    "responsavel_tratamento": "Direção-Geral de Exemplo"
  }
}
```

#### 2.7.2 Tabela de campos

| Campo | Obrigatório | Tipo | Descrição |
|---|---|---|---|
| `tipo_documento_ref` | Sim | string | Referência versionada ao schema do tipo de documento. Formato: `"<id>@<versao>"`. Define a estrutura de `documento`. Ver §2.9.2 e `specs/registry/`. |
| `entidade_produtora` | Sim | objeto | Entidade responsável pela produção do documento. Ver §2.7.3. |
| `assunto` | Recomendado | string | Título ou descrição breve do documento — indexável para pesquisa e arquivo. |
| `numero_referencia` | Recomendado | string | Número de referência documental (ex.: `"OF/2026/00123"`). |
| `processo_ref` | Opcional | string | Referência ao processo ou procedimento a que o documento pertence. |
| `idioma` | Opcional | string (ISO 639-1) | Idioma principal do documento. Quando omitido, assume-se `"pt"`. |
| `classificacao_seguranca` | Recomendado | string (enum) | Classificação de segurança da informação. Ver §2.7.4. Quando omitido, o sistema produtor DEVE assumir `"uso_interno"`. |
| `contem_dados_pessoais` | Sim | boolean | `true` se o documento contiver dados pessoais na acepção do RGPD. |
| `categorias_dados_pessoais` | Condicional | array de string | Obrigatório se `contem_dados_pessoais: true`. Enum aberto: `"identificacao_fiscal"`, `"rendimentos"`, `"saude"`, `"dados_processuais"`, `"biometricos"`, `"outros"`. Ver §1.6. |
| `base_legal_conservacao` | Condicional | string (enum) | Obrigatório se `contem_dados_pessoais: true`. `"obrigacao_legal"` \| `"interesse_publico"` \| `"consentimento"` \| `"contrato"`. Ver §1.6. |
| `responsavel_tratamento` | Sim | string | Designação da entidade responsável pelo tratamento. Obrigatório mesmo quando `contem_dados_pessoais: false` — identifica o responsável pela custódia do registo. |

#### 2.7.3 `entidade_produtora`

| Campo | Obrigatório | Descrição |
|---|---|---|
| `designacao` | Sim | Designação oficial da entidade (ex.: `"Autoridade Tributária e Aduaneira"`). |
| `nif` | Recomendado | NIF institucional — 9 dígitos sem espaços ou pontuação. |
| `codigo_dglab` | Opcional | Código de entidade DGLAB para identificação no contexto arquivístico (MEG). |

#### 2.7.4 `classificacao_seguranca` (enum fechado)

Alinhado com o DL n.º 11/2023 (Segurança de Informação do Estado) e a nomenclatura da UE:

| Valor | Descrição |
|---|---|
| `"publico"` | Informação de acesso livre — sem restrições. DEVE ser atribuída explicitamente; NÃO DEVE ser assumida por omissão. |
| `"uso_interno"` | Circulação interna à entidade; não destinada ao exterior. O sistema produtor DEVE assumir este valor quando `classificacao_seguranca` é omitido. |
| `"reservado"` | Divulgação restrita a destinatários identificados. |
| `"confidencial"` | Classificação de segurança formal — acesso controlado com registo de acessos. |
| `"secreto"` | Classificação de segurança elevada — regime de gestão documental especial. |
| `"muito_secreto"` | Nível mais elevado — requer infraestrutura de segurança dedicada. |

### 2.8 Tipos de conteúdo permitidos

Os valores dentro de `documento` e `metadados` seguem as regras gerais do JCS/JSON: strings (UTF-8), números, booleanos, `null`, objetos e arrays. Não são permitidos:

- Tipos binários embutidos diretamente (anexos binários são referenciados por hash/identificador de blob, fora do NDF-core — fora de âmbito desta especificação, que cobre apenas documentos gerados internamente sem anexos binários opacos).
- Valores `NaN`, `Infinity`, `-Infinity` (não representáveis em JSON estrito).
- Chaves duplicadas no mesmo objeto (proibido por JCS).

### 2.9 Tipologias de documento e extensibilidade de `documento`

#### 2.9.1 Princípio: NDF-core é um envelope genérico, `documento` é tipado por schema próprio

Esta especificação define a **estrutura comum** de qualquer NDF (campos de topo, envelope, avaliação, NDT-ref). O conteúdo de `documento` é **intencionalmente opaco** a este nível — a sua estrutura interna é definida por um **schema de tipo de documento** (`tipo_documento`), referenciado, não embutido, na especificação base. Isto permite que o mesmo formato NDF acomode, sem alterações a esta especificação:

- **Documentos administrativos correntes** — ofícios, informações, despachos, pareceres: estrutura predominantemente textual, com poucos campos estruturados (destinatário, assunto, corpo, referências processuais).
- **Formulários fiscais/declarativos complexos** — ex. Modelo 3 de IRS: estrutura profundamente aninhada, com múltiplos anexos/quadros/campos condicionais, validações cruzadas entre campos, e potencialmente centenas de elementos de dados.
- Qualquer tipologia futura, incluindo formatos de outras administrações/domínios, sem necessidade de revisão major desta especificação.

#### 2.9.2 Campo `tipo_documento_ref`

Adicionar a `metadados` (não a `documento`) uma referência ao schema que define a estrutura de `documento`:

```json
{
  "metadados": {
    "tipo_documento_ref": "string (identificador + versão do schema do tipo de documento)",
    "...": "demais metadados descritivos/classificação"
  }
}
```

- **Tipo**: string no formato normativo `<id>@<versao>` definido pelo registry
  (ex. `oficio@1.0.0`, `modelo3-irs@2025.1`). Formas URI/URN exigem uma futura
  revisão da especificação; não são escolhas locais de implementação.
- **Obrigatoriedade**: `tipo_documento_ref` é **obrigatório** em `metadados` (entra portanto no NDF-core, canonicalizado/assinado) — sem ele, não é possível interpretar `documento` de forma fiável a longo prazo.
- **Resolução**: o schema referenciado por `tipo_documento_ref` define a estrutura de `documento` (e tipicamente também orienta o NDT correspondente via `ndt_version_ref`, mas os dois são referências independentes — um mesmo `tipo_documento` pode ter múltiplas versões de NDT ao longo do tempo).
- **Versionamento de schemas de tipo de documento**: segue o mesmo princípio de §7 (compatibilidade major/minor) — um leitor recusa processar `documento` cujo `tipo_documento_ref` tenha versão major não suportada; versões minor adicionam campos opcionais sem quebrar leitores antigos.

#### 2.9.3 Perfis de complexidade — exemplos ilustrativos (não normativos)

Esta especificação não define os schemas de `documento` para tipos concretos (isso é responsabilidade de cada `tipo_documento_ref`), mas ilustra dois perfis para validar que a estrutura genérica acomoda ambos:

**Perfil "documento administrativo corrente"** (ex. `tipo_documento_ref: "oficio@1.0"`):

```json
{
  "documento": {
    "numero": "OF/2026/00123",
    "data": "2026-06-15",
    "destinatario": { "nome": "Entidade Destinatária", "identificacao": "NIF 987654321" },
    "assunto": "Resposta ao ofício n.º 45/2026",
    "corpo": {
      "ncrtf_version": "2.0.0",
      "content": [
        {
          "type": "paragraph",
          "content": [ { "type": "text", "text": "Texto do ofício..." } ]
        }
      ]
    },
    "referencias_processuais": ["proc.º 123/2026"]
  }
}
```

O campo `corpo` é um valor **NCRTF** (NORMORDIS Canonical Rich Text Format,
spec separada) — não uma string plana. A estrutura concreta continua a ser
determinada pelo schema de `tipo_documento_ref`.

**Perfil "formulário fiscal/declarativo complexo"** (ex. `tipo_documento_ref: "modelo3-irs@2025.1"`):

```json
{
  "documento": {
    "ano_fiscal": 2025,
    "sujeitos_passivos": [ { "nif": "...", "...": "..." } ],
    "anexos": {
      "anexo_a": { "quadros": { "...": "..." } },
      "anexo_b": { "quadros": { "...": "..." } }
    },
    "totais_calculados": { "...": "..." },
    "validacoes_cruzadas_aplicadas": ["..."]
  }
}
```

Estrutura profundamente aninhada, com arrays de elementos repetíveis (anexos, sujeitos passivos), campos calculados, e dependências/validações entre secções. **Tudo isto permanece dentro de `documento`, sob `additionalProperties` livre ao nível desta especificação base** — a validação detalhada do conteúdo de `documento` é responsabilidade do schema de `tipo_documento_ref`, não desta especificação NDF-core.

#### 2.9.4 Limites práticos a considerar na implementação

- **Profundidade de aninhamento e tamanho**: o JCS (RFC 8785) e o JSON em geral não impõem limites teóricos de profundidade/tamanho, mas implementações concretas (parsers, validadores de schema) podem ter limites práticos. Para tipos de documento muito complexos (Modelo 3 IRS pode ter milhares de campos preenchidos com múltiplos anexos), a implementação deve validar que: (a) a canonicalização JCS é determinística e performante mesmo para `documento` de grande dimensão; (b) os validadores JSON Schema dos `tipo_documento_ref` mais complexos não excedem limites de profundidade/recursão dos validadores escolhidos (ver prompt de implementação do schema/validador).
- **Eficiência de armazenamento permanece válida**: mesmo um Modelo 3 IRS complexo, em JSON estruturado, é tipicamente muito mais compacto do que o PDF oficial equivalente (que inclui layout completo de todos os anexos, mesmo os não preenchidos). O argumento de economia de espaço (ver discussão de vantagens do NDF) mantém-se, possivelmente de forma ainda mais pronunciada para formulários longos com muitas secções não aplicáveis/vazias no PDF mas ausentes no NDF.
- **Anexos binários dentro de formulários complexos**: se um `tipo_documento` exigir anexos binários (ex. comprovativos digitalizados anexos a uma declaração), estes seguem o regime de documentos importados/preservação bit-a-bit (fora de âmbito desta especificação) — `documento` referencia-os por identificador/hash, nunca os embute.

### 2.10 Nível de assinatura eletrónica (`nivel_assinatura`)

Declara o nível mínimo de assinatura eletrónica exigido pela natureza jurídica do acto representado pelo documento. Determina quais os passos do pipeline de finalização (§5.2) que são obrigatórios e que tipo de certificado é requerido.

**Distinção importante**: `nivel_assinatura` refere-se ao requisito jurídico de
assinatura pessoal. É independente da integridade e da imutabilidade de
custódia. Todo o NDF tem JCS, hash e custódia append-only/WORM auditável; CAdES
é obrigatório apenas para `"avancada"` e `"qualificada"`. Um documento com
`"nenhuma"` pode receber um selo institucional opcional, sem que isso constitua
uma assinatura pessoal. Ver a arquitectura normativa comum em
`docs/architecture/ARCHITECTURE.md`.

#### 2.10.1 Valores (enum fechado)

| Valor | Nível eIDAS | Requisito de certificado | Passos obrigatórios no pipeline | Exemplos de actos |
|---|---|---|---|---|
| `"nenhuma"` | — | Nenhum | Passos 1–3 e 8 (canonicalização, hash, validation_code, persistência) | Registos internos sem efeito externo, logs de operação, tabelas de presença, minutas. |
| `"avancada"` | SEA — Assinatura Eletrónica Avançada (eIDAS Art.º 26.º) | Certificado com identificação única do signatário; não obrigatoriamente qualificado | Passos 1–8 com CAdES-B-LTA | Ofícios, informações técnicas, pareceres, despachos de mero expediente, notificações de rotina. |
| `"qualificada"` | SEQ — Assinatura Eletrónica Qualificada (eIDAS Art.º 25.º) | Certificado qualificado emitido por PSSC inscrito na lista de confiança eIDAS; equivalente legal à assinatura manuscrita | Passos 1–8 com CAdES-B-LTA | Contratos públicos, actos com efeito patrimonial significativo, decisões com impacto jurídico directo. |

#### 2.10.2 Responsabilidade de classificação

A classificação correcta de um acto num destes três níveis é **responsabilidade da entidade produtora**. A especificação NDF não define o mapeamento entre tipos de acto e níveis de assinatura — essa é uma decisão de direito administrativo, que cada entidade define de acordo com o CPA, os estatutos sectoriais, e as suas normas internas de delegação de competência e autenticidade documental.

#### 2.10.3 Implicações para o envelope

| `nivel_assinatura` | `assinaturas[]` | `timestamps` | `validation_material` | `validation_code` |
|---|---|---|---|---|
| `"nenhuma"` | Ausente ou `[]` | Ausente (opcional por razões de arquivo) | Ausente | **Sempre presente** |
| `"avancada"` | CAdES-B-LTA com certificado SEA | Presente (B-T + B-LTA) | Presente | **Sempre presente** |
| `"qualificada"` | CAdES-B-LTA com certificado SEQ qualificado PSSC | Presente (B-T + B-LTA) | Presente | **Sempre presente** |

#### 2.10.4 Integridade de arquivo para `nivel_assinatura: "nenhuma"`

Mesmo quando o acto não requer assinatura eletrónica para validade jurídica, a conservação do registo pode impor requisitos de integridade a longo prazo. A seguinte regra aplica-se:

| Condição arquivística | Requisito de envelope |
|---|---|
| `destino_final: "eliminacao"` E PCA ≤ 5 anos | Envelope mínimo (apenas `validation_code` + `payload_hash`). CAdES-B-LTA **não obrigatório**. |
| `destino_final: "eliminacao"` E PCA > 5 anos | Selo institucional CAdES-B-LTA RECOMENDADO para portabilidade da prova de origem. |
| `destino_final: "conservacao_parcial_por_amostragem"` | Selo institucional CAdES-B-LTA RECOMENDADO para os documentos seleccionados. |
| `destino_final: "conservacao_permanente"` | Selo institucional CAdES-B-LTA RECOMENDADO; custódia append-only/WORM e auditoria continuam obrigatórias. |

Quando CAdES-B-LTA é aplicado a um documento com `nivel_assinatura: "nenhuma"`, o envelope DEVE usar um **selo institucional** (não uma assinatura pessoal) — um certificado de autenticação da entidade produtora ou do sistema de gestão documental, não um certificado qualificado pessoal. O efeito jurídico é de integridade técnica, não de assinatura com efeito legal equivalente à manuscrita.

---

## 3. Avaliação arquivística (PCA/DF — MEG/DGLAB)

### 3.1 Fundamento

Conforme o MEG e os instrumentos da DGLAB (Lista Consolidada e Tabelas de Seleção), todo o documento de arquivo deve ter associada uma decisão de avaliação que determina:

- O **Prazo de Conservação Administrativa (PCA)** — período durante o qual a informação deve ser mantida.
- O **Destino Final (DF)** — decisão de conservação permanente, eliminação, ou conservação parcial por amostragem.

A Lista Consolidada da DGLAB integra estas decisões de avaliação para os processos de negócio executados pela Administração Pública, numa perspetiva suprainstitucional.

### 3.2 Estrutura do bloco `avaliacao`

```json
{
  "avaliacao": {
    "tipo_classificacao_ref": "string",
    "prazo_conservacao_administrativa": {
      "valor": 5,
      "unidade": "anos",
      "forma_contagem": "string (enum)"
    },
    "destino_final": "string (enum)",
    "instrumento_avaliacao_versao_ref": "string"
  }
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| `tipo_classificacao_ref` | string | Referência à classe/série no instrumento de avaliação arquivística. Formato normativo: `"<instrumento>/<codigo_classe>"`. Ver §3.2.1. |
| `prazo_conservacao_administrativa.valor` | número inteiro ≥ 0 | Quantidade do prazo. |
| `prazo_conservacao_administrativa.unidade` | string (enum) | `dias \| meses \| anos`. |
| `prazo_conservacao_administrativa.forma_contagem` | string (enum) | Ver §3.3. |
| `destino_final` | string (enum) | `conservacao_permanente \| eliminacao \| conservacao_parcial_por_amostragem`. |
| `instrumento_avaliacao_versao_ref` | string | Instrumento de avaliação e versão usada para resolver PCA/DF no momento da finalização. Formato: `"<instrumento>/<versao>"`. Ver §3.2.2. |

### 3.2.1 Formato normativo de `tipo_classificacao_ref`

A string segue o formato `"<instrumento>/<codigo_classe>"`:

| Componente | Descrição |
|---|---|
| `instrumento` | Identificador do instrumento de avaliação. Valores canónicos: `"lc"` (Lista Consolidada DGLAB), `"ts"` (Tabela de Seleção institucional), `"portaria"` (Portaria de Gestão de Documentos). Extensível por entidades com instrumentos próprios homologados pela DGLAB. |
| `codigo_classe` | Código da classe ou série dentro do instrumento — segue a codificação definida pelo próprio instrumento (ex.: `"450.10.001"` para a Lista Consolidada DGLAB). |

**Exemplos válidos**:
```
"lc/450.10.001"    — classe 450.10.001 da Lista Consolidada DGLAB
"lc/150.30.400"    — classe 150.30.400 da Lista Consolidada DGLAB
"ts/at/300.20"     — classe 300.20 da Tabela de Seleção da AT
"portaria/1253-A/2009/II-3"  — série II-3 da Portaria n.º 1253-A/2009
```

O instrumento e a versão consultados são registados em `instrumento_avaliacao_versao_ref`, permitindo que a regra aplicável seja rastreável mesmo após actualização do instrumento.

`tipo_classificacao_ref` é **resolvido automaticamente** pelo sistema produtor a partir do tipo de documento — nunca introduzido manualmente por documento.

### 3.2.2 Formato normativo de `instrumento_avaliacao_versao_ref`

A string segue o formato `"<instrumento>/<versao>"`:

| Componente | Descrição |
|---|---|
| `instrumento` | Identificador do instrumento. Valores canónicos: `"lc"` (Lista Consolidada DGLAB), `"pgd"` (Plano de Gestão de Documentos), `"portaria"` (Portaria de Gestão de Documentos), `"ts"` (Tabela de Seleção institucional). Extensível por entidades com instrumentos próprios. |
| `versao` | Identificador da versão ou edição consultada — suficiente para localizar o instrumento exacto. Não há formato imposto; RECOMENDA-SE incluir ano e número de revisão. |

**Exemplos válidos**:
```
"lc/lista-consolidada-dglab-2023-v3"   — Lista Consolidada DGLAB, edição 2023 v3
"pgd/pgd-mf-2019-v2"                  — PGD do Ministério das Finanças, v2
"portaria/1253-A-2009"                 — Portaria n.º 1253-A/2009
"ts/at/tabela-2022"                    — Tabela de Seleção da AT, edição 2022
```

`tipo_classificacao_ref` e `instrumento_avaliacao_versao_ref` DEVEM referenciar o mesmo instrumento: o prefixo de `tipo_classificacao_ref` DEVE corresponder ao `instrumento` de `instrumento_avaliacao_versao_ref`. Exemplo: `"lc/450.10.001"` exige `"lc/..."` em `instrumento_avaliacao_versao_ref`.

### 3.3 Enum `forma_contagem`

Conjunto fechado, alinhado com as formas de contagem de prazo previstas pela Lista Consolidada/MEG. Valores de referência (a confirmar/ajustar contra a Lista Consolidada vigente no momento da implementação):

- `data_documento` — a partir da data de finalização do próprio documento.
- `encerramento_processo` — a partir do encerramento do processo/procedimento a que o documento pertence.
- `fim_ano_civil` — a partir do final do ano civil em que o documento foi finalizado.
- `fim_vigencia` — a partir do termo de vigência (ex.: contratos, regulamentos com prazo de validade).
- `outro` — forma de contagem específica, com descrição textual adicional (campo `forma_contagem_detalhe`, opcional).

### 3.4 Enum `destino_final`

- `conservacao_permanente` — o documento, decorrido o PCA, é destinado a conservação permanente em arquivo.
- `eliminacao` — o documento, decorrido o PCA, é elegível para eliminação.
- `conservacao_parcial_por_amostragem` — apenas uma amostra (conforme critério de amostragem definido na Lista Consolidada/Tabela de Seleção) é conservada permanentemente; o remanescente é eliminado.

### 3.5 Resolução automática

`prazo_conservacao_administrativa` e `destino_final` devem ser **resolvidos automaticamente** a partir de `tipo_classificacao_ref`, consultando o instrumento de avaliação carregado no sistema no momento da finalização — não introduzidos manualmente por documento. `instrumento_avaliacao_versao_ref` regista qual o instrumento e versão consultados, preservando a regra aplicável mesmo que o instrumento seja actualizado posteriormente.

### 3.6 Dados derivados (fora do NDF-core)

A partir de `avaliacao.prazo_conservacao_administrativa` e da data de finalização (`finalizado_em`, campo do envelope/metadados operacionais — não do NDF-core), o sistema calcula e mantém uma data de elegibilidade para aplicação do destino final. Este valor:

- **Não** faz parte do NDF-core (não é canonicalizado nem assinado).
- É puramente operacional, recalculável, e usado para processos de gestão de arquivo (identificação de documentos elegíveis para aplicação de destino final).

---

## 4. Envelope de integridade e autenticidade

### 4.1 Componentes

| Componente | Conteúdo | Norma | Condicional |
|---|---|---|---|
| `assinaturas` | Assinaturas pessoais ou selos institucionais CAdES sobre os `payload_bytes` canónicos, mais metadados de identidade e certificado | CAdES (ETSI EN 319 122), nível B-LTA | Assinatura pessoal obrigatória se `nivel_assinatura ∈ {"avancada", "qualificada"}`; selo institucional opcional se `"nenhuma"` |
| `timestamps` | Timestamps RFC 3161 — de assinatura (B-T) e de arquivo (B-LTA) | RFC 3161 | Obrigatório se `nivel_assinatura ∈ {"avancada", "qualificada"}`; opcional se `"nenhuma"` |
| `validation_material` | Cadeia de certificados (signatário → raiz) + respostas de revogação (OCSP/CRL) capturadas no momento da assinatura | LT/LTA (ETSI EN 319 122) | Obrigatório se `nivel_assinatura ∈ {"avancada", "qualificada"}`; ausente se `"nenhuma"` |
| `validation_code` | Código de verificação canónico — derivado de `ndf_id` + `payload_hash`. Ver §4.6. | Esta especificação | **Sempre presente** — independente de `nivel_assinatura` |

### 4.2 Nível alvo quando CAdES é usado: CAdES-B-LTA

CAdES-B-LTA (Long Term Archival) garante:

- **B** (Basic): assinatura sobre o digest, com certificado do signatário.
- **T** (Timestamp): timestamp sobre o valor da assinatura, prova de quando a assinatura foi criada.
- **LT** (Long Term): inclusão da cadeia de certificados e dados de revogação, permitindo validação mesmo que o repositório de revogação original deixe de estar acessível.
- **A** (Archive): timestamp de arquivo adicional sobre assinatura + dados LT, protegendo contra a expiração/comprometimento futuro dos algoritmos/certificados usados na assinatura original.

### 4.2.1 Requisitos da Autoridade de Timestamp (TSA)

O timestamp RFC 3161 (B-T e B-LTA) deve ser emitido por uma TSA que cumpra os seguintes requisitos:

| Requisito | Especificação |
|---|---|
| Qualificação | A TSA DEVE constar da lista de confiança de um Estado-Membro UE (EU Trusted List, conforme ETSI TS 119 612). |
| Implementação de referência para a AP portuguesa | SCEE — Sistema de Certificação Electrónica do Estado (Agência para a Modernização Administrativa, AMA). |
| Precisão | O timestamp DEVE ter precisão de 1 segundo ou melhor. |
| Algoritmo de hash do timestamp | SHA-256 ou superior (ETSI EN 319 422). |
| Disponibilidade de resposta | A TSA DEVE suportar o protocolo TSP (Time-Stamp Protocol) via HTTP ou HTTPS. |

Quando a implementação opera em ambientes sem acesso à internet (ex.: redes de classificação), o timestamp PODE ser obtido de uma TSA local acreditada, desde que a cadeia de confiança seja incluída no `validation_material` do envelope.

### 4.3 Agility de algoritmo criptográfico

O nível CAdES-B-LTA mitiga parcialmente o risco de comprometimento de algoritmos criptográficos (o timestamp de arquivo sela a assinatura original antes de o algoritmo ser posto em causa). Contudo, a especificação reconhece que:

- O SHA-256 usado em `payload_hash` pode ser comprometido no horizonte de 20+ anos de conservação.
- Os algoritmos de assinatura dos certificados qualificados podem tornar-se obsoletos.

A mitigação completa deste risco faz parte do **roadmap desta especificação** (ver §9). A estratégia prevista é a re-selagem periódica: aplicação de um novo timestamp de arquivo com algoritmos mais recentes sobre o envelope existente, sem alterar `payload_bytes`. Esta operação não viola a imutabilidade do NDF-core — o conteúdo não muda, apenas a camada de prova temporal é reforçada.

### 4.4 Múltiplas assinaturas

`assinaturas` é um array — um NDF pode ter mais do que uma assinatura (ex.:
assinatura de autor + selo institucional/visto). Cada entrada é independente e
assina os mesmos `payload_bytes` canónicos em modo detached. O digest usado
internamente pelo contentor CAdES DEVE coincidir com `payload_hash`.

### 4.4.1 Preservação da assinatura original

Quando `nivel_assinatura ∈ {"avancada", "qualificada"}`, a assinatura CAdES é
parte integrante e obrigatória do documento arquivado. Durante todo o prazo de
conservação, e enquanto o NDF-core for preservado, o sistema de custódia DEVE:

1. preservar byte a byte o contentor CAdES original;
2. preservar os timestamps RFC 3161 e o material de validação associados;
3. impedir alteração, substituição ou remoção isolada destes objectos;
4. incluir estes objectos nos hashes do inventário do `.ndfpkg`;
5. registar qualquer renovação criptográfica como nova prova append-only.

Uma re-selagem, renovação de timestamp ou migração de algoritmo NÃO DEVE
substituir a assinatura original. A nova prova protege a cadeia anterior e é
acrescentada ao envelope ou ao registo de custódia. A eliminação destes
objectos só é permitida juntamente com a eliminação arquivística formalmente
autorizada do próprio documento (§2.4.3).

### 4.5 Mecanismos de assinatura suportados

A especificação do NDF não depende do dispositivo de assinatura. Quando CAdES
é exigido ou aplicado, o resultado DEVE ser uma assinatura detached
CAdES-B-LTA válida sobre `payload_bytes`. Mecanismos possíveis incluem Cartão
de Cidadão, HSM institucional, selo electrónico e Chave Móvel Digital.

### 4.6 `validation_code` — Código de verificação canónico

#### 4.6.1 Propósito

O `validation_code` é um identificador curto aposto à representação visual do
documento. Permite ao público consultar o portal oficial, que resolve o código
para o registo sob custódia e confirma a autenticidade institucional, entidade
produtora, hash e estado corrente. O código também permite confirmar a
correspondência com `ndf_id` e `payload_hash`; isoladamente e fora de um
custodiante confiável, não prova autoria ou origem institucional.

#### 4.6.2 Algoritmo de derivação

```
input      = ndf_id + "|" + payload_hash
digest     = SHA-256( input )          -- SHA-256, NIST FIPS 180-4
code_b32   = BASE32_NOPAD(digest)       -- RFC 4648 §6, sem padding, maiúsculas
validation_code = "NDF-" + code_b32[:20] -- primeiros 100 bits
```

**Formato resultante**: `NDF-` + 20 caracteres Base32 (A–Z, 2–7)

**Exemplo**: `NDF-A3F7K2MXPQR9ZTNW8VJ`

**Formato legível** (grupos de 5 separados por hífen): `NDF-A3F7K-2MXPQ-R9ZTN-W8VJX`

#### 4.6.3 Propriedades do espaço de endereçamento

| Propriedade | Valor |
|---|---|
| Bits de entropia | 100 bits |
| Combinações possíveis | 2¹⁰⁰ ≈ 1.27 × 10³⁰ |
| Probabilidade de colisão com 10⁸ documentos | ≈ 3.9 × 10⁻¹⁵ (negligenciável) |
| Probabilidade de colisão com 10¹² documentos | ≈ 3.9 × 10⁻⁷ (negligenciável) |
| Tentativas médias para adivinhar um código válido | 2⁹⁹ ≈ 6.3 × 10²⁹ |
| Caracteres Base32 (RFC 4648) | A–Z, 2–7 — sem caracteres ambíguos (0/O, 1/I/l) |
| Comprimento com prefixo, sem separadores | 24 caracteres |
| Comprimento com prefixo e separadores | 28 caracteres (`NDF-XXXXX-XXXXX-XXXXX-XXXXX`) |

O espaço de endereçamento de 2¹⁰⁰ suporta a totalidade dos documentos da Administração Pública portuguesa para os próximos séculos sem qualquer pressão de colisão.

#### 4.6.4 Verificabilidade

O `validation_code` é **self-verifiable quanto à correspondência**: qualquer
implementação pode confirmar que o código corresponde ao `ndf_id` e
`payload_hash` apresentados. Esta verificação não autentica o emissor.

O portal de verificação (`https://validar.normordis.pt/<validation_code>`) é a
âncora pública de custódia. Uma resposta positiva DEVE resultar da comparação
do código com o NDF preservado, da verificação do `payload_hash` e da consulta
do estado corrente. Quando exista CAdES, o portal DEVE também validar a
assinatura ou selo e indicar o resultado. A verificação offline continua
possível, mas só confirma autenticidade quando exista uma âncora de confiança
local, assinatura ou selo verificável.

#### 4.6.5 Representações

**Texto** (para impressão, correspondência, citação):
```
NDF-A3F7K-2MXPQ-R9ZTN-W8VJX
```

**QR code** (elemento `codigo_barras` no NDT, §5.3.7 da spec NDT):
```
https://validar.normordis.pt/NDF-A3F7K-2MXPQ-R9ZTN-W8VJX
```

O NDT referencia o `validation_code` através do placeholder `{{validation_code}}` no elemento `codigo_barras` (e em qualquer `texto_fixo` ou `mobilia[]` que o necessite). Este placeholder é resolvido pelo renderer a partir do envelope — não é um dado do NDF-core nem um metadado do NDT, mas um valor computado no momento da finalização. Ambas as representações são obrigatórias em documentos emitidos para o exterior — a forma texto para leitura humana e o QR code para leitura por dispositivo.

#### 4.6.6 Posição no pipeline de finalização

O `validation_code` é calculado **após** a canonicalização e o cálculo do `payload_hash`, sendo adicionado ao envelope antes da assinatura CAdES-B:

```
1. Canonicalizar NDF-core → payload_bytes
2. payload_hash = SHA-256(payload_bytes)
3. validation_code = "NDF-" + BASE32_NOPAD(SHA-256(ndf_id + "|" + payload_hash))[:20]
4. [Se nivel_assinatura ≠ "nenhuma"] Assinar payload_hash (CAdES-B)  ← validation_code não está no que é assinado
5. ...
```

O `validation_code` não faz parte do NDF-core canonicalizado — evita a referência circular (o código depende do hash do conteúdo; se fosse conteúdo, alteraria o hash). Fica no envelope como campo operacional, par do `payload_hash`.

---

## 5. Regras de finalização

A operação de finalização transforma um NDF-core completo (rascunho) num NDF finalizado (NDF-core + envelope), imutável.

### 5.1 Pré-condições

A finalização **DEVE falhar** se:

- Qualquer campo obrigatório do NDF-core (§2.2) estiver ausente, incluindo `ndf_id`, `nivel_assinatura`, `ndt_version_ref`, `payload_hash_alg` e `avaliacao` completo (§3.2).
- `nivel_assinatura` contiver um valor fora do enum definido em §2.10.
- `nivel_assinatura ∈ {"avancada", "qualificada"}` e não estiver disponível um certificado electrónico conforme (SEA ou SEQ, respectivamente).
- `nivel_assinatura = "qualificada"` e o certificado não for emitido por um PSSC inscrito na lista de confiança eIDAS.
- `avaliacao.prazo_conservacao_administrativa` ou `avaliacao.destino_final` não puderem ser resolvidos a partir de `tipo_classificacao_ref` (Lista Consolidada indisponível ou sem entrada correspondente).
- O conteúdo de `documento`/`metadados` violar as regras de tipos permitidos (§2.8).

### 5.2 Pipeline (ordem estrita)

Os passos 1–3 e 8 são **sempre obrigatórios**. Os passos 4–7 são **condicionais** ao valor de `nivel_assinatura` (ver §2.10).

1. Canonicalizar o NDF-core completo (incluindo `ndf_id`, `nivel_assinatura`, `ndt_version_ref` e `avaliacao`) via JCS (RFC 8785) → `payload_bytes`.
2. Calcular `payload_hash = SHA-256(payload_bytes)`.
3. Calcular `validation_code = "NDF-" + BASE32_NOPAD(SHA-256(ndf_id + "|" + payload_hash))[:20]` (ver §4.6).
4. **[Se `nivel_assinatura ∈ {"avancada", "qualificada"}` ou houver selo institucional]** Assinar `payload_bytes` em modo detached (CAdES-B), com certificado conforme ao tipo e nível declarado.
5. **[Se `nivel_assinatura ∈ {"avancada", "qualificada"}`]** Obter timestamp de assinatura (CAdES-B-T).
6. **[Se `nivel_assinatura ∈ {"avancada", "qualificada"}`]** Recolher material de validação — cadeia de certificados + revogação (CAdES-B-LT).
7. **[Se `nivel_assinatura ∈ {"avancada", "qualificada"}`]** Obter timestamp de arquivo selando assinatura + material de validação (CAdES-B-LTA).
8. Persistir atomicamente `payload_bytes` e envelope em armazenamento
append-only/WORM, criando o evento inicial no log de custódia. Para
`nivel_assinatura: "nenhuma"`, assinatura, timestamps e material de validação
podem estar ausentes; um selo institucional continua permitido.

### 5.3 Pós-condições

- `payload_bytes` DEVE ser tratado como imutável para sempre.
- Assinaturas CAdES originais, timestamps e material de validação DEVEM ser
  preservados byte a byte enquanto o documento for conservado.
- Entradas existentes do envelope NÃO DEVEM ser alteradas. Provas de
  re-selagem podem ser acrescentadas de forma append-only e auditada.
- Qualquer necessidade de alteração ao conteúdo lógico DEVE originar um **novo NDF** (ver §6) — NÃO DEVE alterar o NDF finalizado.

---

## 6. Versionamento de documentos (cadeia de proveniência)

### 6.1 Princípio

Um NDF finalizado nunca é editado. Uma "nova versão" de um documento é um **NDF novo e distinto**, com o seu próprio NDF-core, envelope, e ciclo de finalização completo (§5).

### 6.2 Referência ao documento anterior

O novo NDF regista a proveniência no **envelope** (fora do NDF-core), nos seguintes campos de topo:

```json
{
  "versao_anterior": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
  "hash_anterior": "sha256:3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b"
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| `versao_anterior` | string (UUID v4) | `ndf_id` do NDF imediatamente anterior na cadeia de proveniência. |
| `hash_anterior` | string (`"sha256:<hex>"`) | `payload_hash` do NDF anterior — permite verificar que o documento anterior não foi adulterado. |

**Localização normativa**: estes campos ficam no envelope, ao mesmo nível de `assinaturas`, `timestamps` e `validation_code`. Não entram no NDF-core canonicalizado — são metadados relacionais sobre a ligação entre documentos, não conteúdo do documento em si.

****Quando presentes**: DEVEM estar presentes quando o NDF é uma nova versão de um documento anterior (`estado` do anterior transita para `"substituido"`). DEVEM estar ausentes em documentos sem versão prévia.

### 6.3 Pacote de exportação (`.ndfpkg`)

O formato `.ndfpkg` é o **pacote de exportação auto-suficiente** de um NDF finalizado. É definido nesta especificação (§8) e garante que o documento pode ser verificado, renderizado e preservado independentemente da infraestrutura original.

A cadeia de proveniência de um processo documental é uma coleção de pacotes `.ndfpkg` independentes, ligados por referências leves (`versao_anterior`/`hash_anterior`), nunca por conteúdo embutido.

---

## 7. Versionamento da especificação NDF

A especificação NDF segue **Semantic Versioning 2.0.0** (SemVer — https://semver.org/), com as seguintes regras normativas:

### 7.1 `ndf_version`

Cada NDF-core declara a versão da especificação NDF a que adere no campo `ndf_version` (string, formato `MAJOR.MINOR.PATCH`). Este campo é obrigatório, faz parte do NDF-core canonicalizado e assinado, e é imutável após finalização.

| Componente | Quando muda | Impacto |
|---|---|---|
| `MAJOR` | Mudanças incompatíveis: remoção ou renomeação de campos obrigatórios, alteração de semântica existente, mudança de algoritmo de canonicalização | Leitores antigos recusam processar |
| `MINOR` | Adição compatível de campos ou blocos opcionais | Requer schema da nova versão; leitores antigos podem preservar o documento como opaco, mas não ignoram conteúdo assinado desconhecido |
| `PATCH` | Correções de clareza na especificação sem impacto comportamental | Sem impacto em leitores |

### 7.2 Compatibilidade retroativa

Um leitor NDF DEVE declarar explicitamente as versões que suporta. O schema de
cada release valida apenas a sua versão exacta. Um leitor DEVE rejeitar uma
versão que não suporte ou tratá-la como objecto opaco, sem afirmar que
interpretou o documento. Conteúdo assinado desconhecido não é ignorado
silenciosamente. Compatibilidade entre versões é uma propriedade documentada
da implementação, não uma licença para validar um documento novo contra um
schema antigo.

### 7.3 Versionamento de schemas de tipo de documento

O campo `tipo_documento_ref` em `metadados` segue o mesmo princípio SemVer (ex.: `oficio@1.2.0`, `modelo3-irs@2026.1.0`). A versão do schema de tipo de documento é independente da versão da especificação NDF — o mesmo tipo de documento pode ter múltiplas versões de schema sem que a especificação NDF mude.

---

## 8. Pacote de exportação (`.ndfpkg`)

O `.ndfpkg` é o formato de exportação auto-suficiente de um NDF finalizado. Garante que o documento pode ser verificado, renderizado e preservado independentemente da infraestrutura original do core-documental.

### 8.1 Composição

Um `.ndfpkg` é um arquivo ZIP com a seguinte estrutura:

```
documento.ndfpkg (ZIP)
├── manifest.json          — metadados do pacote e inventário com hashes
├── ndf-core.json          — payload_bytes do NDF-core (bytes canonicalizados, UTF-8)
├── envelope.json          — assinaturas, timestamps, material de validação
├── ndt/
│   └── <schema_id>@<versao>.ndt.json   — NDT referenciado por ndt_version_ref
└── recursos/              — recursos visuais partilhados por NDT e NCRTF
    ├── <sha256>.<ext>     — recursos NDT com modo referenciado_por_hash (nome = hash)
    └── <nome>.<ext>       — imagens NCRTF referenciadas por image.ref (nome declarado no campo)
```

### 8.2 `manifest.json`

```json
{
  "ndfpkg_version": "1.0.0",
  "ndf_id": "uuid",
  "ndf_version": "1.0.0",
  "schema_id": "oficio-generico",
  "finalizado_em": "2026-06-18T10:30:00Z",
  "payload_hash": "sha256:abc123...",
  "inventario": [
    { "ficheiro": "ndf-core.json", "hash_sha256": "..." },
    { "ficheiro": "envelope.json", "hash_sha256": "..." },
    { "ficheiro": "ndt/oficio-generico@1.0.0.ndt.json", "hash_sha256": "..." }
  ]
}
```

### 8.3 Garantias do `.ndfpkg`

- **Auto-suficiência**: contém tudo o que é necessário para verificar a assinatura, reproduzir visualmente o documento e confirmar a avaliação arquivística — sem dependência de infraestrutura online.
- **NDT embebido**: o NDT referenciado por `ndt_version_ref` é incluído no pacote, garantindo reprodutibilidade visual mesmo que o NDT evolua ou o repositório original deixe de existir.
- **Verificabilidade**: qualquer implementação conforme pode verificar `sha256(ndf-core.json) == payload_hash` e validar a assinatura CAdES-B-LTA sem acesso ao core-documental original.
- **Cadeia de proveniência**: o `manifest.json` regista `versao_anterior` e `hash_anterior` quando aplicável, permitindo reconstruir a cadeia de versões com múltiplos `.ndfpkg`.

---

## 9. Roadmap

Itens previstos para versões futuras desta especificação. Não são normativos na versão atual.

| Item | Versão prevista | Descrição |
|---|---|---|
| Agility de algoritmo criptográfico | 1.1.0 | Mecanismo formal de re-selagem periódica (re-timestamping) com algoritmos mais recentes, sem alterar `payload_bytes`. Inclui procedimento de migração e requisitos de notificação. |
| Schema de categorias especiais (RGPD Art.º 9.º) | 1.1.0 | Extensão do bloco `metadados` para categorias especiais de dados: dados de saúde, origem racial/étnica, dados biométricos — campos já previstos mas não detalhados em v1.0.0. |
| Validação formal do `.ndfpkg` | 1.1.0 | Expansão da suite de conformidade (`conformance/ndf/`) com testes de empacotamento, resolução de NDT, e verificação de assinatura end-to-end. |
| Registry remoto de tipos de documento | 1.1.0 | URI canónico `https://registry.normordis.pt/<id>/<versao>/schema.json` para resolução de `tipo_documento_ref` sem acesso ao `.ndfpkg`. |
| Suporte multi-hash | 1.2.0 | Permitir `payload_hash` com múltiplos algoritmos em paralelo (`sha256`, `sha3-256`) para preparação de transição. |
| Extensões de namespace | 2.0.0 | Mecanismo formal de extensão do NDF-core por organismos externos (ex.: `ext.at.pt`, `ext.ss.pt`) sem necessidade de revisão desta especificação base. |

---

## 10. Conformidade

### 10.1 Produtor conforme

Uma implementação é um **produtor NDF conforme** se e apenas se satisfizer todos os seguintes requisitos:

1. **DEVE** gerar NDF-core JSON que valida contra o schema `specs/ndf/schemas/ndf-core.schema.json` (JSON Schema Draft 2020-12).
2. **DEVE** canonicalizar o NDF-core via JCS (RFC 8785) produzindo `payload_bytes` determinísticos — bytes idênticos para a mesma estrutura lógica independentemente da ordem de inserção de chaves ou formatação de origem.
3. **DEVE** calcular `payload_hash = SHA-256(payload_bytes)` conforme NIST FIPS 180-4.
4. **DEVE** calcular `validation_code` conforme o algoritmo definido em §4.6.2.
5. **DEVE** executar os passos do pipeline de finalização conforme `nivel_assinatura` declarado (§5.2):
   - Para `"nenhuma"`: passos 1–3 e 8 obrigatórios.
   - Para `"avancada"` ou `"qualificada"`: todos os passos 1–8 obrigatórios.
6. **DEVE** incluir todos os campos obrigatórios de `metadados` (§2.7.2), incluindo os condicionais RGPD quando `contem_dados_pessoais: true`.
7. **DEVE** definir `tipo_classificacao_ref` no formato `<instrumento>/<codigo>` (§3.2.1).
8. **DEVE** gerar `ndf_id` como UUID v4 válido (RFC 4122), único no espaço de nomes do sistema produtor.
9. **DEVE** definir `estado: "ativo"` no NDF-core de qualquer documento recém-finalizado.
10. **DEVE** registar cada transição de estado em log de auditoria imutável (§2.4.2).
11. **DEVE** aceitar todos os casos de `conformance/ndf/valid/` sem erro.

### 10.2 Leitor conforme

Uma implementação é um **leitor NDF conforme** se e apenas se satisfizer todos os seguintes requisitos:

1. **DEVE** rejeitar qualquer NDF-core que não valide contra o schema desta versão.
2. **DEVE** rejeitar versões NDF não suportadas explicitamente ou tratá-las como opacas, sem declarar interpretação completa.
3. **NÃO DEVE** ignorar silenciosamente conteúdo assinado desconhecido.
4. **DEVE** verificar `SHA-256(payload_bytes) == payload_hash` antes de aceitar um documento como íntegro.
5. **DEVE** verificar `validation_code` recalculando o digest conforme §4.6.2.
6. Quando `nivel_assinatura ∈ {"avancada", "qualificada"}`: **DEVE** validar a assinatura CAdES-B-LTA e os timestamps RFC 3161; **NÃO DEVE** aceitar um documento assinado com certificado não conforme ao `nivel_assinatura` declarado; **DEVE** considerar inválido um pacote onde a assinatura original, timestamps ou material de validação estejam ausentes ou tenham sido alterados.
7. **DEVE** rejeitar todos os casos de `conformance/ndf/invalid/`.
8. **DEVE** aceitar todos os casos de `conformance/ndf/valid/`.

### 10.3 Pacote conforme (`.ndfpkg`)

Um arquivo `.ndfpkg` é conforme se satisfizer todos os seguintes requisitos:

1. **DEVE** ser um arquivo ZIP válido.
2. **DEVE** conter `manifest.json`, `ndf-core.json` e `envelope.json` na raiz do arquivo.
3. `manifest.json` **DEVE** incluir inventário com `hash_sha256` de cada ficheiro e os campos obrigatórios definidos em §8.2.
4. `SHA-256(ndf-core.json)` **DEVE** coincidir com `manifest.inventario[ndf-core.json].hash_sha256`.
5. `ndf-core.json` **DEVE** ser um NDF-core conforme (§10.1).
6. O NDT referenciado por `ndt_version_ref` **DEVE** estar presente em `ndt/<schema_id>@<versao>.ndt.json`.

### 10.4 Suite de conformidade e test runner

A suite oficial de casos de teste está em `conformance/ndf/`. O test runner de referência é `tools/validate.py`.

```bash
# Pré-requisito
pip install jsonschema

# Correr toda a suite NDF + NDT + NCRTF
python3 tools/validate.py

# Validar o exemplo portátil end-to-end
python3 tools/validate.py --package specs/ndf/examples/ndfpkg-example

# Validar um ficheiro específico
python3 tools/validate.py path/to/ndf-core.json

# Apenas casos válidos / inválidos
python3 tools/validate.py --valid-only
python3 tools/validate.py --invalid-only
```

Uma implementação conforme **DEVE** passar todos os casos de `conformance/ndf/valid/` e **DEVE** rejeitar todos os casos de `conformance/ndf/invalid/`.

**Nota**: os ficheiros de conformidade contêm campos `_comment` e `_expected_error` prefixados com `_` para documentação interna. Estes campos **NÃO DEVEM** constar do NDF-core produzido por uma implementação — o test runner remove-os automaticamente antes de validar.

---

## 11. Glossário

| Termo | Significado |
|---|---|
| NDF | NORMORDIS Document Format — formato completo (NDF-core + envelope) |
| NDF-core | Parte de dados do NDF, canonicalizada e assinada |
| Envelope | Assinaturas, timestamps e material de validação, associados ao NDF-core mas não assinados |
| NDT | NORMORDIS Document Template — estrutura/layout para reprodução visual |
| JCS | JSON Canonicalization Scheme (RFC 8785) |
| PCA | Prazo de Conservação Administrativa |
| DF | Destino Final |
| MEF | Macroestrutura Funcional (DGLAB) |
| MIP | (classificação documental institucional/processual — DGLAB) |
| Lista Consolidada | Referencial suprainstitucional da DGLAB com classificação + avaliação (PCA/DF) |
| SEA / AES | Assinatura Eletrónica Avançada — eIDAS Art.º 26.º; identificação única do signatário sem obrigatoriedade de certificado qualificado |
| SEQ / QES | Assinatura Eletrónica Qualificada — eIDAS Art.º 25.º; certificado qualificado PSSC; equivalente legal à assinatura manuscrita |
| PSSC | Prestador de Serviços de Confiança Qualificado — entidade inscrita na lista de confiança eIDAS |
| `nivel_assinatura` | Nível mínimo de assinatura eletrónica exigido pela natureza jurídica do acto: `"nenhuma"`, `"avancada"` ou `"qualificada"` (ver §2.10) |
| CAdES-B-LTA | Nível de assinatura eletrónica avançada com timestamp de arquivo (ETSI EN 319 122) |
| `tipo_documento_ref` | Referência ao schema versionado que define a estrutura interna de `documento` (ex.: `oficio@1.0.0`, `modelo3-irs@2025.1`) — ver §2.9.2 |
