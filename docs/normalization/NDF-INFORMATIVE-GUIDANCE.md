# Orientações informativas NDF

**Estado:** informativo — não constitui requisitos NDF.

Este documento reúne referências de contexto, estimativas, mapeamento jurídico, perfil físico de armazenamento e roadmap anteriormente intercalados no texto normativo.

## Referências informativas e de perfil

| Norma / Regulamento | Âmbito |
|---|---|
| eIDAS — Regulamento (UE) n.º 910/2014 | Assinaturas eletrónicas qualificadas, selos eletrónicos |
| eIDAS 2.0 — Regulamento (UE) 2024/1183 | Revisão eIDAS — European Digital Identity Wallet; QSCD |
| DL n.º 12/2021 | Execução nacional e enquadramento dos serviços de confiança |
| CPA — Código do Procedimento Administrativo (DL n.º 4/2015) | Forma dos atos administrativos; requisitos de autenticidade (Art.º 61.º) |
| ETSI EN 319 122 | CAdES — nível B-LTA (Long Term Archival) |
| RFC 3161 | Timestamps de confiança |
| RFC 8785 (JCS) | Canonicalização JSON para assinatura |
| ISO 15489-1:2016 | Gestão de documentos de arquivo — conceitos e princípios |
| MoReq2017 | Modelo de requisitos para sistemas de gestão de arquivos eletrónicos (UE) |
| MEG / DGLAB | Modelo de Requisitos nacional; Lista Consolidada; Tabelas de Seleção |
| RGPD — Regulamento (UE) 2016/679 | Proteção de dados pessoais |
| Lei n.º 58/2019 | Execução nacional do RGPD |

## Eficiência de armazenamento face a formatos binários (informativo)

O NDF armazena apenas dados estruturados — sem layout, fontes, imagens de fundo ou páginas não preenchidas. Esta diferença produz ganhos de armazenamento substanciais face a PDF/A.

As estimativas abaixo são calculadas a partir de rácios empíricos observados em documentos reais de referência e estão pendentes de validação formal com corpus representativo da Administração Pública portuguesa. Os valores serão actualizados quando forem disponibilizados dados de medição real.

### Estimativas por tipo de documento

| Tipo de documento | PDF/A típico | NDF estimado | Rácio estimado |
|---|---|---|---|
| Ofício simples (1–2 pág.) | 80–150 KB | 3–6 KB | 20×–40× |
| Informação técnica (3–5 pág.) | 150–300 KB | 6–12 KB | 15×–30× |
| Despacho / Parecer | 100–250 KB | 4–8 KB | 20×–35× |
| Modelo 3 IRS (rosto + anexos preenchidos) | 800 KB–2 MB | 30–80 KB | 15×–40× |
| Formulário fiscal genérico (1 pág.) | 200–500 KB | 8–20 KB | 15×–30× |

> **Nota metodológica**: o PDF/A inclui fontes embebidas, elementos gráficos do impresso, e todas as páginas de anexos (incluindo as não preenchidas). O NDF contém exclusivamente os campos preenchidos, metadados e avaliação arquivística — não inclui layout nem recursos visuais. O rácio depende da densidade de preenchimento: documentos com muitas secções opcionais vazias têm rácios mais favoráveis ao NDF.

### Impacto a escala institucional (estimativas)

| Cenário | Volume anual | Armazenamento PDF/A | Armazenamento NDF | Poupança estimada |
|---|---|---|---|---|
| Município médio | 50 000 docs | ~7,5 GB/ano | ~400 MB/ano | ~95% |
| Ministério / Direção-Geral | 500 000 docs | ~75 GB/ano | ~4 GB/ano | ~95% |
| AT — Modelo 3 IRS | 3 500 000 declarações | ~3,5 TB/ano | ~175 GB/ano | ~95% |

Projecção a 10 anos para um município médio: ~75 GB (PDF/A) vs. ~4 GB (NDF) — diferença de uma a duas ordens de grandeza que impacta diretamente custos de armazenamento, backup, replicação e transferência para arquivo digital definitivo.

> **Validação empírica pendente**: os valores acima serão substituídos por medições reais quando estiverem disponíveis amostras representativas de documentos produzidos pelo core-documental NORMORDIS. A metodologia de medição (corpus, tipos de documento, densidade de preenchimento) será publicada em `docs/benchmarks/` desta especificação.

## Mapeamento jurídico e normativo (informativo)

### Matriz de apoio à conformidade

A tabela seguinte relaciona objetivos externos com mecanismos do NDF. Não
constitui parecer jurídico, certificação nem declaração de conformidade. A
aplicabilidade deve ser validada por especialistas competentes.

| Requisito | Instrumento legal / normativo | Disposição NDF | Secção |
|---|---|---|---|
| Assinatura eletrónica proporcional ao ato | eIDAS, Art.º 25.º–26.º; DL n.º 12/2021; CPA, Art.º 61.º | `nivel_assinatura` no NDF-core: `"nenhuma"` / `"avancada"` (SEA) / `"qualificada"` (SEQ), conforme a natureza jurídica do ato | §2.10 |
| Preservação de longo prazo da assinatura | eIDAS, Art.º 34.º; ETSI EN 319 122 | Nível CAdES-B-LTA; timestamp de arquivo RFC 3161 — obrigatório quando `nivel_assinatura ≠ "nenhuma"` | §4.2, §5.2 |
| Autenticidade e integridade do documento | ISO 15489:2016, §5.2; MoReq2017, R2 | JCS/RFC 8785 + SHA-256 + CAdES sobre `payload_bytes` | §1.3, §4 |
| Imutabilidade do registo | MoReq2017, R3; MEG, R4 | Princípio de imutabilidade; proibição de edição de NDF finalizado | §2.1 |
| Reprodutibilidade / renderização futura | MoReq2017, R5; OAIS/ISO 14721:2012 | `ndt_version_ref` embebido no NDF-core; NDT incluído no `.ndfpkg` | §2.6, §8 |
| Prazo de conservação administrativa (PCA) | MEG/DGLAB, Lista Consolidada | Bloco `avaliacao.prazo_conservacao_administrativa` com `instrumento_avaliacao_versao_ref` | §3 |
| Destino final (conservação / eliminação) | MEG/DGLAB, Tabelas de Seleção | `avaliacao.destino_final`; eliminação no termo do PCA | §3.4 |
| Classificação documental (MEF/MIP) | MEG/DGLAB, Macroestrutura Funcional | `metadados.tipo_classificacao_ref` | §2.7 |
| Cadeia de custódia / proveniência | ISO 15489:2016, §5.3; MoReq2017, R6 | `versao_anterior` + `hash_anterior`; cadeia de NDF imutáveis | §6 |
| Limitação da conservação de dados pessoais | RGPD, Art.º 5.º, n.º 1, al. e) | PCA + `destino_final: eliminacao` aplicado no termo do prazo | §3, §1.4 |
| Minimização de dados pessoais | RGPD, Art.º 5.º, n.º 1, al. c) | NDF armazena apenas campos preenchidos; sem layout nem páginas vazias | §2.8 |
| Direito ao apagamento | RGPD, Art.º 17.º | Eliminação integral no termo do PCA; base legal de conservação prevalente documentada | §1.4 |
| Identificação do responsável pelo tratamento | RGPD, Art.º 13.º–14.º; Lei n.º 58/2019 | `metadados.responsavel_tratamento` obrigatório | §1.4 |
| Categorias especiais de dados pessoais | RGPD, Art.º 9.º | `metadados.categorias_dados_pessoais` (roadmap §1.1.0) | §9 |
| Interoperabilidade com sistemas da AP | Lei n.º 36/2011 (normas abertas); EIF | Formato JSON aberto; especificação CC0; sem dependência de fornecedor | Licenciamento |
| Acesso à informação administrativa | Lei n.º 26/2016 | `.ndfpkg` autocontido; reprodutibilidade sem infraestrutura original | §8 |
| Agility de algoritmo criptográfico | eIDAS, Art.º 34.º (preservação); ETSI EN 319 122, §6 | Re-selagem periódica; roadmap multi-hash | §4.5, §9 |

### Política de atualização por mudança de enquadramento jurídico

O enquadramento jurídico e normativo aplicável ao NDF muda periodicamente. A política seguinte define como cada tipo de mudança se traduz numa versão SemVer desta especificação.

**Tipo A — Mudança absorvida por campos de referência (sem nova versão da especificação)**

Certas mudanças são absolvidas pelos campos `*_ref` existentes, sem alterar o formato NDF:

| Mudança | Campo absorvente | Acção |
|---|---|---|
| Nova versão da Lista Consolidada DGLAB | `avaliacao.instrumento_avaliacao_versao_ref` | Implementações atualizam o valor; especificação não muda |
| Nova portaria de impressos fiscais | `impresso.versao_impresso` no NDT | NDT atualizado; NDF especificação não muda |
| Novo algoritmo de assinatura nos certificados qualificados | `envelope.assinaturas[].algoritmo` | Implementações suportam novo algoritmo; especificação não muda |

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

**Regra de rastreabilidade**: cada versão da especificação que resulte de uma mudança de enquadramento jurídico DEVE incluir no `CHANGELOG.md` a referência ao instrumento legal ou normativo que a motivou. Exemplo:

```
## [1.1.0] — 2027-01-15
### Motivação legal
- RGPD Art.º 9.º / Orientação CNPD n.º X/2026 — categorias especiais de dados pessoais
### Alterações
- Adicionado: `metadados.categorias_especiais_dados` (opcional)
```

### Monitorização do enquadramento jurídico

Instrumentos legais com revisões previstas ou em curso que podem implicar actualizações à especificação:

| Instrumento | Estado | Impacto previsto |
|---|---|---|
| eIDAS 2.0 — Regulamento (UE) 2024/1183 | Em vigor (transposição em curso) | Suporte a QSCD e European Digital Identity Wallet — MINOR |
| Lista Consolidada DGLAB (revisão periódica) | Actualizações regulares | Absorvida por `instrumento_avaliacao_versao_ref` — sem versão |
| Norma MoReq (revisão prevista) | A confirmar | Avaliação quando publicada |
| Revisão do RGPD / Lei n.º 58/2019 | Sem data | A avaliar conforme publicação |

---

## Armazenamento em base de dados (informativo)

O NDF é concebido para persistência eficiente, mas não exige base de dados,
produto ou modelo físico. Uma implementação pode usar SQL, object storage,
content-addressed storage, ficheiros WORM ou outra tecnologia, desde que
preserve os bytes e garantias normativas. O exemplo PostgreSQL abaixo é
puramente informativo e não participa na conformidade.

### Colunas obrigatórias (fonte de verdade)

| Coluna | Tipo PostgreSQL | Conteúdo |
|---|---|---|
| `id` | `uuid` | Identificador único do NDF |
| `payload_bytes` | `bytea` | Bytes canónicos do NDF-core (JCS/RFC 8785) — imutável após finalização; fonte de verdade para verificação de assinatura |
| `envelope` | `jsonb` ou bytes preservados | Metadados do envelope e provas criptográficas; objetos CAdES, timestamps e material de validação são imutáveis e preservados byte a byte |
| `estado` | `text` | `rascunho` \| `finalizado` |
| `criado_em` | `timestamptz` | Data/hora de criação |
| `finalizado_em` | `timestamptz` | Data/hora de finalização; `null` se rascunho |

### Colunas desnormalizadas para indexação (extraídas de `payload_bytes`)

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

### JSONB derivado (opcional, para queries ad-hoc)

```sql
-- Coluna gerada, derivada de payload_bytes, para queries ad-hoc
ALTER TABLE ndf ADD COLUMN payload_jsonb jsonb
  GENERATED ALWAYS AS (convert_from(payload_bytes, 'UTF8')::jsonb) STORED;
```

**Regra de integridade**: `payload_bytes` é a única fonte de verdade. O JSONB derivado e as colunas desnormalizadas NÃO DEVEM ser alterados diretamente — qualquer divergência entre `payload_bytes` e as colunas indexáveis é um erro de implementação. A verificação de integridade é feita sempre sobre `sha256(payload_bytes)`, não sobre o JSONB.

## Roadmap (informativo)

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

