# Especificação NDF v1.0.0

**NORMORDIS Document Format — Especificação Formal**

Estado: Draft para implementação
Âmbito: documentos gerados internamente pelo core-documental NORMORDIS e normalizados a NDF. Documentos importados/preservados bit-a-bit seguem um regime distinto, fora do âmbito desta especificação.

## Licenciamento

Esta especificação (texto, estrutura, JSON Schemas e exemplos associados) é disponibilizada sob **CC0 1.0** (domínio público). O objetivo é que qualquer produtor de software para a Administração Pública — open source ou proprietário — possa implementar leitura/escrita de NDF/NDT livremente, sem qualquer obrigação contratual ou de licenciamento para com o autor da especificação. Um formato de dados verdadeiramente aberto é o que permite à Administração Pública mudar de fornecedor sem perder acesso aos seus próprios dados — esse é o mecanismo real de soberania digital.

A **implementação de referência** (código-fonte: validadores, serializadores, bibliotecas Rust, `normordis-pdf`, etc.) é distribuída sob licença separada (EUPL v1.2), indicada no respetivo repositório (`LICENSE`). Esta especificação é licenciada separadamente (`LICENSE-SPEC`) precisamente para que a adoção do *formato* não dependa da licença do *código*.

---

## 1. Visão geral

### 1.1 Objetivo

O NDF (NORMORDIS Document Format) é o formato canónico de armazenamento de documentos no core-documental. Garante:

- **Integridade e validade jurídica** conforme eIDAS (Regulamento (UE) n.º 910/2014) e DL n.º 12/2021, com assinatura eletrónica qualificada de nível CAdES-B-LTA (ETSI EN 319 122).
- **Eficiência de armazenamento**, por ser dados estruturados (tipicamente uma a duas ordens de grandeza menor que um binário renderizado equivalente), otimizado para persistência em base de dados relacional (ver §1.5).
- **Reprodutibilidade visual** em qualquer formato de apresentação (PDF, Word, ou formato futuro), através da combinação com o NDT (NORMORDIS Document Template — estrutura/layout).
- **Conformidade arquivística** conforme ISO 15489:2016 (Records Management), MoReq2017, o Modelo de Requisitos para Sistemas de Gestão de Arquivos Eletrónicos (MEG/DGLAB) e os instrumentos de avaliação da DGLAB (Lista Consolidada / Tabelas de Seleção).
- **Conformidade legal** com o RGPD (Regulamento (UE) 2016/679) e a Lei n.º 58/2019, respeitando os princípios de minimização de dados, limitação da conservação e os direitos dos titulares (ver §1.6).

### 1.1.1 Normas e regulamentos de referência

| Norma / Regulamento | Âmbito |
|---|---|
| eIDAS — Regulamento (UE) n.º 910/2014 | Assinaturas eletrónicas qualificadas, selos eletrónicos |
| DL n.º 12/2021 | Transposição nacional de eIDAS |
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

### 1.3 Formato de serialização

- **JSON**, não XML. Justificação: o NDF é formato de armazenamento interno do core-documental, não um formato de troca direta com terceiros. Interoperabilidade XML, quando necessária (ex.: SAFT-PT, UBL, eIDAS de outros Estados-Membros), é resolvida por adapters de exportação fora do âmbito desta especificação — o NDF-core é a fonte de verdade a partir da qual tais exportações são derivadas.
- **Canonicalização**: JCS — JSON Canonicalization Scheme, conforme **RFC 8785**, estrito. Garante que a mesma estrutura lógica produz sempre os mesmos bytes, independentemente de ordem de inserção de chaves ou formatação de origem.

### 1.4 Conformidade jurídica e normativa

#### 1.4.1 Matriz de conformidade

A tabela seguinte mapeia cada requisito legal ou normativo à disposição concreta do NDF que o cumpre. Qualquer alteração ao enquadramento jurídico que invalide uma linha desta tabela implica uma actualização da especificação (ver §1.4.2).

| Requisito | Instrumento legal / normativo | Disposição NDF | Secção |
|---|---|---|---|
| Assinatura eletrónica qualificada | eIDAS, Art.º 25.º; DL n.º 12/2021 | Envelope CAdES-B com certificado qualificado | §4 |
| Preservação de longo prazo da assinatura | eIDAS, Art.º 34.º; ETSI EN 319 122 | Nível CAdES-B-LTA; timestamp de arquivo RFC 3161 | §4.2 |
| Autenticidade e integridade do documento | ISO 15489:2016, §5.2; MoReq2017, R2 | JCS/RFC 8785 + SHA-256 + CAdES sobre `payload_bytes` | §1.3, §4 |
| Imutabilidade do registo | MoReq2017, R3; MEG, R4 | Princípio de imutabilidade; proibição de edição de NDF finalizado | §2.1 |
| Reprodutibilidade / renderização futura | MoReq2017, R5; OAIS/ISO 14721:2012 | `ndt_version_ref` embebido no NDF-core; NDT incluído no `.ndfpkg` | §2.3, §8 |
| Prazo de conservação administrativa (PCA) | MEG/DGLAB, Lista Consolidada | Bloco `avaliacao.prazo_conservacao_administrativa` com `lista_consolidada_versao_ref` | §3 |
| Destino final (conservação / eliminação) | MEG/DGLAB, Tabelas de Seleção | `avaliacao.destino_final`; eliminação no termo do PCA | §3.4 |
| Classificação documental (MEF/MIP) | MEG/DGLAB, Macroestrutura Funcional | `metadados.tipo_classificacao_ref` | §2.2 |
| Cadeia de custódia / proveniência | ISO 15489:2016, §5.3; MoReq2017, R6 | `versao_anterior` + `hash_anterior`; cadeia de NDF imutáveis | §6 |
| Limitação da conservação de dados pessoais | RGPD, Art.º 5.º, n.º 1, al. e) | PCA + `destino_final: eliminacao` aplicado no termo do prazo | §3, §1.6 |
| Minimização de dados pessoais | RGPD, Art.º 5.º, n.º 1, al. c) | NDF armazena apenas campos preenchidos; sem layout nem páginas vazias | §2.4 |
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
| Nova versão da Lista Consolidada DGLAB | `avaliacao.lista_consolidada_versao_ref` | Implementações actualizam o valor; spec não muda |
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
| Lista Consolidada DGLAB (revisão periódica) | Actualizações regulares | Absorvida por `lista_consolidada_versao_ref` — sem versão |
| Norma MoReq (revisão prevista) | A confirmar | Avaliação quando publicada |
| Revisão do RGPD / Lei n.º 58/2019 | Sem data | A avaliar conforme publicação |

---

### 1.5 Armazenamento em base de dados

O NDF é concebido para persistência eficiente em base de dados relacional. O modelo recomendado para implementações PostgreSQL:

#### Colunas obrigatórias (fonte de verdade)

| Coluna | Tipo PostgreSQL | Conteúdo |
|---|---|---|
| `id` | `uuid` | Identificador único do NDF |
| `payload_bytes` | `bytea` | Bytes canónicos do NDF-core (JCS/RFC 8785) — imutável após finalização; fonte de verdade para verificação de assinatura |
| `envelope` | `jsonb` | Assinaturas, timestamps e material de validação |
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

O NDF-core é um objeto JSON com (no mínimo) os seguintes campos de topo:

```json
{
  "ndf_version": "1.0.0",
  "documento": { /* ... conteúdo lógico do documento, estrutura definida por tipo_documento_ref ... */ },
  "metadados": {
    "tipo_documento_ref": "...",
    "...": "... demais metadados descritivos, classificação MEF/MIP/DGLAB ..."
  },
  "ndt_version_ref": "...",
  "avaliacao": { /* ... ver §3 ... */ }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `ndf_version` | Sim | Versão desta especificação a que o documento adere (semver). Permite evolução compatível/incompatível do formato. |
| `documento` | Sim | Conteúdo lógico do documento — estrutura definida pelo tipo de documento (`.ndf` type), independente desta especificação base. |
| `metadados` | Sim | Metadados descritivos e classificação (MEF/MIP/DGLAB), via `tipo_classificacao` (mapeamento existente em `crates/domain`). Inclui obrigatoriamente `tipo_documento_ref` (ver §2.5.2), que define o schema estrutural de `documento`. |
| `ndt_version_ref` | Sim | Referência à versão do NDT (estrutura/layout) com que este NDF-core deve ser combinado para reprodução visual. Ver §2.3. |
| `avaliacao` | Sim | Dados de avaliação arquivística (PCA/DF), conforme MEG/DGLAB. Ver §3. |

Nenhum destes campos pode estar ausente no momento da finalização — a finalização **falha** se algum estiver em falta (ver §5).

### 2.3 `ndt_version_ref`

Identifica univocamente a versão do NDT (template/layout) com que o NDF-core foi pensado para ser combinado na reprodução visual no momento da finalização.

- **Tipo**: string (formato a definir conforme o esquema de versionamento de NDT já em uso — ex. semver do template, ou identificador composto `tipo_documento@versao`).
- **Propósito**: garantir reprodução determinística mesmo que o NDT evolua (novas versões de templates não afetam a renderização correta de NDFs antigos, desde que a versão referenciada do NDT permaneça disponível/resoluvel).
- **Imutabilidade**: faz parte do NDF-core, logo está sujeito à mesma imutabilidade pós-finalização.

### 2.4 Tipos de conteúdo permitidos

Os valores dentro de `documento` e `metadados` seguem as regras gerais do JCS/JSON: strings (UTF-8), números, booleanos, `null`, objetos e arrays. Não são permitidos:

- Tipos binários embutidos diretamente (anexos binários são referenciados por hash/identificador de blob, fora do NDF-core — fora de âmbito desta especificação, que cobre apenas documentos gerados internamente sem anexos binários opacos).
- Valores `NaN`, `Infinity`, `-Infinity` (não representáveis em JSON estrito).
- Chaves duplicadas no mesmo objeto (proibido por JCS).

### 2.5 Tipologias de documento e extensibilidade de `documento`

#### 2.5.1 Princípio: NDF-core é um envelope genérico, `documento` é tipado por schema próprio

Esta especificação define a **estrutura comum** de qualquer NDF (campos de topo, envelope, avaliação, NDT-ref). O conteúdo de `documento` é **intencionalmente opaco** a este nível — a sua estrutura interna é definida por um **schema de tipo de documento** (`tipo_documento`), referenciado, não embutido, na especificação base. Isto permite que o mesmo formato NDF acomode, sem alterações a esta especificação:

- **Documentos administrativos correntes** — ofícios, informações, despachos, pareceres: estrutura predominantemente textual, com poucos campos estruturados (destinatário, assunto, corpo, referências processuais).
- **Formulários fiscais/declarativos complexos** — ex. Modelo 3 de IRS: estrutura profundamente aninhada, com múltiplos anexos/quadros/campos condicionais, validações cruzadas entre campos, e potencialmente centenas de elementos de dados.
- Qualquer tipologia futura, incluindo formatos de outras administrações/domínios, sem necessidade de revisão major desta especificação.

#### 2.5.2 Campo `tipo_documento_ref`

Adicionar a `metadados` (não a `documento`) uma referência ao schema que define a estrutura de `documento`:

```json
{
  "metadados": {
    "tipo_documento_ref": "string (identificador + versão do schema do tipo de documento)",
    "...": "demais metadados descritivos/classificação"
  }
}
```

- **Tipo**: string, identificador versionado (ex. `oficio@1.0`, `modelo3-irs@2025.1`, ou um URI/URN se se preferir um espaço de nomes mais formal — decidir na implementação, mas manter consistência com `ndt_version_ref`, que segue lógica semelhante).
- **Obrigatoriedade**: `tipo_documento_ref` é **obrigatório** em `metadados` (entra portanto no NDF-core, canonicalizado/assinado) — sem ele, não é possível interpretar `documento` de forma fiável a longo prazo.
- **Resolução**: o schema referenciado por `tipo_documento_ref` define a estrutura de `documento` (e tipicamente também orienta o NDT correspondente via `ndt_version_ref`, mas os dois são referências independentes — um mesmo `tipo_documento` pode ter múltiplas versões de NDT ao longo do tempo).
- **Versionamento de schemas de tipo de documento**: segue o mesmo princípio de §7 (compatibilidade major/minor) — um leitor recusa processar `documento` cujo `tipo_documento_ref` tenha versão major não suportada; versões minor adicionam campos opcionais sem quebrar leitores antigos.

#### 2.5.3 Perfis de complexidade — exemplos ilustrativos (não normativos)

Esta especificação não define os schemas de `documento` para tipos concretos (isso é responsabilidade de cada `tipo_documento_ref`), mas ilustra dois perfis para validar que a estrutura genérica acomoda ambos:

**Perfil "documento administrativo corrente"** (ex. `tipo_documento_ref: "oficio@1.0"`):

```json
{
  "documento": {
    "numero": "OF/2026/00123",
    "data": "2026-06-15",
    "destinatario": { "nome": "...", "identificacao": "..." },
    "assunto": "...",
    "corpo": "...",
    "referencias_processuais": ["proc.º 123/2026"]
  }
}
```

Estrutura plana, predominantemente textual, poucos níveis de aninhamento.

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

#### 2.5.4 Limites práticos a considerar na implementação

- **Profundidade de aninhamento e tamanho**: o JCS (RFC 8785) e o JSON em geral não impõem limites teóricos de profundidade/tamanho, mas implementações concretas (parsers, validadores de schema) podem ter limites práticos. Para tipos de documento muito complexos (Modelo 3 IRS pode ter milhares de campos preenchidos com múltiplos anexos), a implementação deve validar que: (a) a canonicalização JCS é determinística e performante mesmo para `documento` de grande dimensão; (b) os validadores JSON Schema dos `tipo_documento_ref` mais complexos não excedem limites de profundidade/recursão dos validadores escolhidos (ver prompt de implementação do schema/validador).
- **Eficiência de armazenamento permanece válida**: mesmo um Modelo 3 IRS complexo, em JSON estruturado, é tipicamente muito mais compacto do que o PDF oficial equivalente (que inclui layout completo de todos os anexos, mesmo os não preenchidos). O argumento de economia de espaço (ver discussão de vantagens do NDF) mantém-se, possivelmente de forma ainda mais pronunciada para formulários longos com muitas secções não aplicáveis/vazias no PDF mas ausentes no NDF.
- **Anexos binários dentro de formulários complexos**: se um `tipo_documento` exigir anexos binários (ex. comprovativos digitalizados anexos a uma declaração), estes seguem o regime de documentos importados/preservação bit-a-bit (fora de âmbito desta especificação) — `documento` referencia-os por identificador/hash, nunca os embute.

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
    "lista_consolidada_versao_ref": "string"
  }
}
```

| Campo | Tipo | Descrição |
|---|---|---|
| `tipo_classificacao_ref` | string | Referência ao mapeamento `tipo_classificacao` existente em `crates/domain`, ligando o tipo de documento `.ndf` à classificação MEF/MIP/DGLAB. |
| `prazo_conservacao_administrativa.valor` | número inteiro ≥ 0 | Quantidade do prazo. |
| `prazo_conservacao_administrativa.unidade` | string (enum) | `dias \| meses \| anos`. |
| `prazo_conservacao_administrativa.forma_contagem` | string (enum) | Ver §3.3. |
| `destino_final` | string (enum) | `conservacao_permanente \| eliminacao \| conservacao_parcial_por_amostragem`. |
| `lista_consolidada_versao_ref` | string | Identificador/versão da Lista Consolidada (ou tabela de seleção derivada) usada para resolver PCA/DF no momento da finalização. |

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

`prazo_conservacao_administrativa` e `destino_final` devem ser **resolvidos automaticamente** a partir de `tipo_classificacao_ref`, consultando a Lista Consolidada/Tabela de Seleção carregada no sistema no momento da finalização — não introduzidos manualmente por documento. `lista_consolidada_versao_ref` regista qual a versão consultada, preservando a regra aplicável mesmo que a Lista Consolidada seja atualizada posteriormente.

### 3.6 Dados derivados (fora do NDF-core)

A partir de `avaliacao.prazo_conservacao_administrativa` e da data de finalização (`finalizado_em`, campo do envelope/metadados operacionais — não do NDF-core), o sistema calcula e mantém uma data de elegibilidade para aplicação do destino final. Este valor:

- **Não** faz parte do NDF-core (não é canonicalizado nem assinado).
- É puramente operacional, recalculável, e usado para processos de gestão de arquivo (identificação de documentos elegíveis para aplicação de destino final).

---

## 4. Envelope de segurança jurídica

### 4.1 Componentes

| Componente | Conteúdo | Norma |
|---|---|---|
| `assinaturas` | Uma ou mais assinaturas CAdES (CMS/PKCS#7, ASN.1 DER) sobre `sha256(payload_bytes)`, mais metadados (signatário, certificado, nível) | CAdES (ETSI EN 319 122), nível B-LTA |
| `timestamps` | Timestamps RFC 3161 — de assinatura (B-T) e de arquivo (B-LTA) | RFC 3161 |
| `validation_material` | Cadeia de certificados (signatário → raiz) + respostas de revogação (OCSP/CRL) capturadas no momento da assinatura | LT/LTA (ETSI EN 319 122) |

### 4.2 Nível alvo: CAdES-B-LTA

CAdES-B-LTA (Long Term Archival) garante:

- **B** (Basic): assinatura sobre o digest, com certificado do signatário.
- **T** (Timestamp): timestamp sobre o valor da assinatura, prova de quando a assinatura foi criada.
- **LT** (Long Term): inclusão da cadeia de certificados e dados de revogação, permitindo validação mesmo que o repositório de revogação original deixe de estar acessível.
- **A** (Archive): timestamp de arquivo adicional sobre assinatura + dados LT, protegendo contra a expiração/comprometimento futuro dos algoritmos/certificados usados na assinatura original.

### 4.5 Agility de algoritmo criptográfico

O nível CAdES-B-LTA mitiga parcialmente o risco de comprometimento de algoritmos criptográficos (o timestamp de arquivo sela a assinatura original antes de o algoritmo ser posto em causa). Contudo, a especificação reconhece que:

- O SHA-256 usado em `payload_hash` pode ser comprometido no horizonte de 20+ anos de conservação.
- Os algoritmos de assinatura dos certificados qualificados podem tornar-se obsoletos.

A mitigação completa deste risco faz parte do **roadmap desta especificação** (ver §9). A estratégia prevista é a re-selagem periódica: aplicação de um novo timestamp de arquivo com algoritmos mais recentes sobre o envelope existente, sem alterar `payload_bytes`. Esta operação não viola a imutabilidade do NDF-core — o conteúdo não muda, apenas a camada de prova temporal é reforçada.

### 4.3 Múltiplas assinaturas

`assinaturas` é um array — um NDF pode ter mais do que uma assinatura (ex.: assinatura de autor + selo institucional/visto). Cada entrada do array é independente, todas sobre o mesmo `sha256(payload_bytes)`.

### 4.4 Mecanismos de assinatura suportados

A especificação do NDF não depende de um mecanismo específico — apenas exige que o resultado seja uma assinatura CAdES-B-LTA válida sobre `sha256(payload_bytes)`. Mecanismos previstos (ver especificação de implementação, §6): Cartão de Cidadão, smartcard ECCE (ECCE/ARTE — sucessora do CEGER), HSM institucional (selo eletrónico), Chave Móvel Digital.

---

## 5. Regras de finalização

A operação de finalização transforma um NDF-core completo (rascunho) num NDF finalizado (NDF-core + envelope), imutável.

### 5.1 Pré-condições

A finalização **falha** se:

- Qualquer campo obrigatório do NDF-core (§2.2) estiver ausente, incluindo `ndt_version_ref` e `avaliacao` completo (§3.2).
- `avaliacao.prazo_conservacao_administrativa` ou `avaliacao.destino_final` não puderem ser resolvidos a partir de `tipo_classificacao_ref` (Lista Consolidada indisponível ou sem entrada correspondente).
- O conteúdo de `documento`/`metadados` violar as regras de tipos permitidos (§2.4).

### 5.2 Pipeline (ordem estrita)

1. Canonicalizar o NDF-core completo (incluindo `ndt_version_ref` e `avaliacao`) via JCS (RFC 8785) → `payload_bytes`.
2. Calcular `payload_hash = sha256(payload_bytes)`.
3. Assinar `payload_hash` (CAdES-B).
4. Obter timestamp de assinatura (CAdES-B-T).
5. Recolher material de validação — cadeia de certificados + revogação (CAdES-B-LT).
6. Obter timestamp de arquivo selando assinatura + material de validação (CAdES-B-LTA).
7. Persistir atomicamente: `payload_bytes` (imutável a partir daqui) + envelope completo.

### 5.3 Pós-condições

- `payload_bytes` é imutável para sempre.
- `envelope` (assinaturas, timestamps, validation_material) é imutável para sempre.
- Qualquer necessidade de alteração ao conteúdo lógico origina um **novo NDF** (ver §6).

---

## 6. Versionamento de documentos (cadeia de proveniência)

### 6.1 Princípio

Um NDF finalizado nunca é editado. Uma "nova versão" de um documento é um **NDF novo e distinto**, com o seu próprio NDF-core, envelope, e ciclo de finalização completo (§5).

### 6.2 Referência ao documento anterior

O novo NDF regista, fora do NDF-core (metadados operacionais — ver especificação de implementação para localização exata):

- `versao_anterior` — identificador do NDF anterior na cadeia.
- `hash_anterior` — `payload_hash` do NDF anterior, para verificação de cadeia.

Estes campos **não** entram na canonicalização/assinatura do novo NDF-core (são metadados operacionais sobre a relação entre documentos, não conteúdo do documento em si). Ficam disponíveis para reconstrução de cadeias de proveniência auditáveis.

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
| `MINOR` | Adição de campos opcionais ou novos blocos sem alterar semântica existente | Leitores antigos ignoram campos desconhecidos |
| `PATCH` | Correções de clareza na especificação sem impacto comportamental | Sem impacto em leitores |

### 7.2 Compatibilidade retroativa

Um leitor de NDF **deve**:

- Recusar processar um NDF cuja `ndf_version` MAJOR seja superior à suportada (evolução futura com mudanças incompatíveis desconhecidas).
- Processar corretamente NDFs com `ndf_version` MAJOR igual e MINOR igual ou inferior (campos adicionados em versões MINOR mais recentes são tratados como `null`/omissos).
- Processar NDFs com qualquer `ndf_version` PATCH dentro do mesmo MAJOR.MINOR.

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
└── recursos/              — recursos embebidos referenciados no NDT (se modo referenciado_por_hash)
    └── <hash>.<ext>
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
| Schema de RGPD para dados especiais | 1.1.0 | Extensão do bloco `metadados` para categorias especiais de dados (Art.º 9.º RGPD): dados de saúde, origem racial/étnica, dados biométricos. |
| Validação formal do `.ndfpkg` | 1.1.0 | Conjunto de testes de conformidade para implementações do pacote de exportação (ver `conformance/ndf/`). |
| Suporte multi-hash | 1.2.0 | Permitir `payload_hash` com múltiplos algoritmos em paralelo (`sha256`, `sha3-256`) para preparação de transição. |
| Extensões de namespace | 2.0.0 | Mecanismo formal de extensão do NDF-core por organismos externos (ex.: `ext.at.pt`, `ext.ss.pt`) sem necessidade de revisão desta especificação base. |

---

## 10. Glossário

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
| CAdES-B-LTA | Nível de assinatura eletrónica avançada com timestamp de arquivo (ETSI EN 319 122) |
| `tipo_documento_ref` | Referência ao schema versionado que define a estrutura interna de `documento` (ex.: `oficio@1.0`, `modelo3-irs@2025.1`) — ver §2.5 |
