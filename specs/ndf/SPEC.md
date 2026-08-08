# Especificação NDF v1.0.0

**NORMORDIS Document Format — Especificação Formal**

Estado: Draft — Revisão pública
Âmbito: representação canónica, empacotamento, integridade e verificação de
documentos institucionais estruturados. A ingestão e preservação bit a bit de
documentos preexistentes ficam fora do âmbito.

Convenções editoriais: aplica-se
[`docs/normalization/EDITORIAL-POLICY.md`](../../docs/normalization/EDITORIAL-POLICY.md).
A língua normativa é o português europeu. Notas, exemplos, justificações,
estimativas e roadmaps são informativos.

## Licenciamento

Esta especificação (texto, estrutura, JSON Schemas e exemplos associados) é disponibilizada sob **CC0 1.0** (domínio público). O objetivo é que qualquer produtor de software para a Administração Pública — código aberto ou proprietário — possa implementar leitura/escrita de NDF/NDT livremente, sem qualquer obrigação contratual ou de licenciamento para com o autor da especificação. Um formato de dados verdadeiramente aberto é o que permite à Administração Pública mudar de fornecedor sem perder acesso aos seus próprios dados — esse é o mecanismo real de soberania digital.

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

### 1.0.1 Referências normativas

As dependências comuns e respetivos títulos oficiais estão registados em
[`docs/normalization/NORMATIVE-REFERENCES.md`](../../docs/normalization/NORMATIVE-REFERENCES.md).
Para NDF 1.0.0 são normativos, conforme a cláusula em que são invocados: BCP
14, RFC 8259, RFC 8785, RFC 4648, RFC 9562, RFC 5652, RFC 3161, RFC 5816, RFC
5280, RFC 6960, JSON Schema Draft 2020-12 e as edições ETSI fixadas no registo
de referências. A revisão de uma versão candidata DEVE reconfirmar o estado
destas edições.

### 1.0.2 Termos e definições

Aplicam-se os termos da
[base terminológica comum](../../docs/normalization/TERMINOLOGY.md). Termos
específicos de NDF são definidos na cláusula em que são introduzidos. O Anexo A
reúne um glossário informativo.

### 1.1 Objetivo

O NDF (NORMORDIS Document Format) define uma representação canónica para
armazenamento e intercâmbio de documentos institucionais estruturados. Os seus
mecanismos destinam-se a apoiar:

- **Armazenamento imutável, autocontido e eficiente em base de dados**: o
  NDF-core fornece bytes canónicos e conteúdo estruturado adequado a
  persistência e indexação; o `.ndfpkg` reúne conteúdo, envelope, schemas, NDT
  e recursos numa representação portátil sem dependências externas.
- **Interoperabilidade**: o contrato permite a qualquer sistema conforme produzir, transferir,
  interpretar, verificar e renderizar o mesmo documento sem depender do
  fornecedor, linguagem, runtime ou base de dados de origem.

- **Integridade, autenticidade e suporte a assinaturas eletrónicas**. O nível de
  assinatura é declarado no NDF-core (`nivel_assinatura` — ver §2.10). A
  conformidade e validade jurídica dependem da implementação, certificados,
  políticas, contexto de utilização e legislação aplicável; não são garantidas
  pelo formato isoladamente.
- **Eficiência de armazenamento**, através de dados estruturados e separação de
  recursos deduplicáveis, otimizada para persistência em base de dados
  relacional. O perfil físico e os rácios encontram-se nas
  [orientações informativas](../../docs/normalization/NDF-INFORMATIVE-GUIDANCE.md).
- **Reprodutibilidade visual** em qualquer formato de apresentação (PDF/UA-2 como formato primário, ODF e HTML como formatos secundários, ou formato futuro), através da combinação com o NDT (NORMORDIS Document Template — estrutura/layout).
- **Apoio à gestão arquivística**, tendo como referências informativas a ISO
  15489-1, o MoReq2017, o MEG/DGLAB e os instrumentos de avaliação aplicáveis.
- **Apoio à proteção de dados**, incluindo metadados para minimização, base
  legal e conservação. A conformidade com RGPD e legislação nacional exige
  avaliação própria da entidade responsável (ver §1.4).

### 1.1.1 Orientações informativas

Referências de contexto, estimativas, mapeamento jurídico, perfil físico de armazenamento e roadmap encontram-se em [`docs/normalization/NDF-INFORMATIVE-GUIDANCE.md`](../../docs/normalization/NDF-INFORMATIVE-GUIDANCE.md).

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

A separação evita circularidade: o envelope fica fora dos bytes sobre os quais a própria assinatura é calculada.

### 1.2.1 Recursos desta especificação

| Recurso | Localização | Descrição |
|---|---|---|
| JSON Schema (NDF-core) | `specs/ndf/schemas/ndf-core.schema.json` | Schema legível por máquina do NDF-core completo |
| JSON Schema (Envelope) | `specs/ndf/schemas/envelope.schema.json` | Schema legível por máquina do envelope |
| JSON Schema (Manifest) | `specs/ndf/schemas/manifest.schema.json` | Schema legível por máquina do manifesto `.ndfpkg` |
| JSON Schema (Custódia) | `specs/ndf/schemas/custody-event.schema.json` | Evento encadeado do log de custódia — Perfil de Ciclo de Vida NORMORDIS (§2.4, §9.5), opcional, não requisito de conformidade NDF |
| Registo de tipos de documento | `specs/registry/` | Schemas dos tipos canónicos (`oficio`, `informacao-tecnica`, `despacho`) |
| Suite de conformidade | `conformance/ndf/` | Casos de teste válidos e inválidos para implementações |

### 1.3 Formato de serialização

- **JSON**, não XML. A justificação arquitetural consta de
  `docs/architecture/ADR-001-json-not-xml.md`. NDF é diretamente interoperável
  entre sistemas conformes. Integrações cujo contrato externo exija XML, UBL
  ou outro formato usam adaptadores explícitos, sem retirar ao NDF o seu papel
  de formato de interoperabilidade.
- **Canonicalização**: JCS — JSON Canonicalization Scheme, conforme **RFC 8785**, estrito. Garante que a mesma estrutura lógica produz sempre os mesmos bytes, independentemente de ordem de inserção de chaves ou formatação de origem.

### 1.4 Proteção de dados pessoais

O NDF admite dados pessoais (NIF, dados fiscais, dados de saúde, dados processuais) sujeitos ao RGPD (Regulamento (UE) 2016/679) e à Lei n.º 58/2019. O princípio de imutabilidade do NDF (§2.1) cria uma tensão com o direito ao apagamento (Art.º 17.º RGPD).

#### Resolução da tensão imutabilidade ↔ direito ao apagamento

A tensão é resolvida pela articulação de três mecanismos legais e técnicos:

1. **Base legal de conservação prevalente**: documentos da Administração Pública são conservados com base em obrigação legal (Art.º 6.º, n.º 1, al. c) RGPD) e missão de interesse público (al. e)). O direito ao apagamento cede face a obrigações legais de conservação (Art.º 17.º, n.º 3, al. b) RGPD) — o PCA/DF resolve esta decisão por tipo de documento.

2. **Pseudonimização pré-arquivo**: quando aplicável, é possível pseudonimizar dados pessoais antes da finalização. O NDF finalizado contém o pseudónimo; a tabela de correspondência é gerida fora do NDF com controlos de acesso próprios.

3. **Eliminação no termo do PCA**: documentos com `destino_final: eliminacao`
   são eliminados segundo a decisão e procedimento arquivístico aplicável. O
   mecanismo apoia a limitação da conservação, mas não demonstra por si só
   conformidade integral com o RGPD.

#### Campos de metadados obrigatórios relativos a proteção de dados

O bloco `metadados` DEVE incluir:

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

### 1.5 Confidencialidade e controlo de acesso

O NDF admite documentos com diferentes níveis de sensibilidade, declarados
em `metadados.classificacao_seguranca` (§2.7.4) — de `"publico"` a
`"muito_secreto"`. Este campo é descritivo: sinaliza o nível de
sensibilidade do conteúdo. O NDF NÃO DEVE ser apresentado, nem
interpretado, como garantindo confidencialidade, cifra ou controlo de
acesso por si só.

A proteção de um NDF classificado — decidir quem poderá aceder aos seus
bytes, cifra em repouso e em trânsito, gestão de chaves ao longo do prazo
de conservação, auditoria de acessos — é inteiramente responsabilidade do
sistema de custódia que o produz, armazena e disponibiliza. Este princípio
segue a mesma lógica já aplicada à conformidade de RGPD (§1.4) e do AI Act
(§2.13.1): o NDF fornece o sinal estrutural necessário para que o sistema
aplique a proteção adequada; não a substitui nem a garante.

Em particular: cifra em repouso e em trânsito não é, isoladamente, controlo
de acesso — protege contra furto de suporte e interceção de rede, mas não
garante que só quem tem direito legal ao conteúdo consegue decifrá-lo. Essa
garantia depende de autenticação, autorização face a
`classificacao_seguranca`, e auditoria, corretamente implementadas no
sistema de custódia.

Orientações práticas de implementação (não normativas) constam de
[`docs/normalization/NDF-INFORMATIVE-GUIDANCE.md`](../../docs/normalization/NDF-INFORMATIVE-GUIDANCE.md).

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
| `nivel_assinatura` | Sim | Nível de assinatura eletrónica declarado pelo sistema produtor para este documento, segundo a política e o enquadramento jurídico que aplica. Enum fechado — ver §2.10. |
| `ndt_version_ref` | Sim | Referência normativa ao NDT usado na reprodução visual. Formato: `"schema_id@versao_ndt"`. Ver §2.6. |
| `metadados` | Sim | Metadados descritivos, classificação e conformidade. Schema completo definido em §2.7. |
| `documento` | Sim | Conteúdo lógico do documento. Estrutura definida pelo schema referenciado em `metadados.tipo_documento_ref`. |
| `avaliacao` | Sim | Avaliação arquivística (PCA/DF), conforme MEG/DGLAB. Ver §3. |
| `relacoes` | Não | Relações verificáveis com outros documentos NDF. Ver §2.11. |
| `participantes` | Não | Autores, revisores e demais intervenientes, distintos de quem assina. Ver §2.12. |
| `proveniencia_ia` | Não | Evidência de utilização de sistemas de IA na produção ou revisão do documento. Ver §2.13. |

Nenhum dos campos obrigatórios PODE estar ausente — a finalização **DEVE falhar** se algum estiver em falta (ver §5). Os três campos opcionais, quando presentes, entram no NDF-core canonicalizado e assinado tal como os restantes.

### 2.3 `ndf_id`

Identificador permanente do documento no ecossistema NORMORDIS.

- **Tipo**: string, formato UUID v4 (RFC 9562) — ex.: `"a1b2c3d4-e5f6-4789-abcd-ef0123456789"`.
- **Geração**: pelo sistema produtor imediatamente antes da canonicalização, nunca depois.
- **Imutabilidade**: faz parte do NDF-core canonicalizado e assinado — NÃO DEVE ser alterado após finalização.
- **Unicidade**: o sistema produtor DEVE garantir que não existem dois NDF com o mesmo `ndf_id`.
- **Uso**: referência primária em `versao_anterior`, no manifest do `.ndfpkg`, e como chave primária no armazenamento físico.

`ndf_id` é, por desenho, um identificador **opaco** — não incorpora
código de entidade, tipo de documento, nem qualquer outro componente
estrutural. A atribuição a uma entidade produtora fica em
`metadados.entidade_produtora` (§2.7.3), estruturada e coberta pela mesma
assinatura, não no próprio identificador — evita acoplar a identidade
permanente do documento à identidade organizacional da entidade, que muda
ao longo do tempo (reorganizações, fusões, extinções). Ver ADR-009 para a
análise completa desta decisão.

### 2.4 Estado de arquivo (`estado`)

O campo `estado` no NDF-core declara o estado do documento **no momento da finalização** — é sempre `"ativo"`. É canonicalizado e assinado como parte do NDF-core e é **imutável** tal como todos os outros campos.

O estado arquivístico corrente ao longo do ciclo de vida do documento é uma propriedade operacional gerida fora do NDF-core: na base de dados e no campo `estado` do manifesto `.ndfpkg` (§8.2). O valor no NDF-core não reflecte transições posteriores à finalização.

**Valor normativo**: `"ativo"` — único valor válido no NDF-core no momento da finalização.

> **Âmbito de §2.4.1–§2.4.3.** As subsecções seguintes descrevem o **Perfil
> de Ciclo de Vida NORMORDIS** — um modelo de referência para sistemas que
> gerem NDF depois da finalização (transições de estado, log de auditoria,
> WORM, tombstones). Não é requisito de conformidade NDF (§9.1–§9.3); é um
> perfil operacional opcional, com os seus próprios requisitos rastreados
> em §9.5. Um produtor ou leitor NDF conforme não tem de implementar este
> perfil — podendo adotar o seu próprio modelo de gestão de ciclo de vida,
> desde que preserve a imutabilidade de `payload_bytes` (§2.1, §5.3). Ver
> ADR-010 para a justificação desta separação.

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

A transição para suporte a múltiplos algoritmos em paralelo (`"sha256"` + `"sha3-256"`) está prevista na versão 1.2.0 desta especificação (ver roadmap informativo).

### 2.6 `ndt_version_ref`

Identifica univocamente a versão do NDT com que o NDF-core DEVE ser combinado para reprodução visual.

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
- **Resolução**: o NDT referenciado DEVE estar disponível no `.ndfpkg` (§8) ou num registo conforme.

#### 2.6.1 Distinção entre `ndt_version_ref` e `tipo_documento_ref`

Estes dois campos referenciam conceitos distintos e independentes:

| Campo | Referencia | Determina |
|---|---|---|
| `metadados.tipo_documento_ref` | Schema do tipo de documento (ex.: `"oficio@1.0.0"`) | Estrutura de `documento` no NDF-core — o modelo de dados |
| `ndt_version_ref` | Template de layout (ex.: `"oficio-generico@1.0.0"`) | Como o documento é renderizado visualmente — o layout |

Para a maioria dos tipos de documento, os dois são 1:1 — um único NDT serve um único schema. No entanto, são referências independentes porque:

- O mesmo tipo de documento admite **múltiplos NDTs** (ex.: versão simplificada e versão completa de um formulário; versão A4 e versão Letter para exportação).
- O schema de `documento` (`tipo_documento_ref`) evolui independentemente do layout (`ndt_version_ref`) — uma atualização visual do impresso não altera a estrutura de dados e vice-versa.
- Um mesmo NDT é reutilizável por múltiplas versões patch do mesmo schema de documento.

O registo (`specs/registry/`) mantém a correspondência canónica entre tipos de documento e os seus NDTs de referência.

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
| `categorias_dados_pessoais` | Condicional | array de string | Obrigatório se `contem_dados_pessoais: true`. Enum aberto: `"identificacao_fiscal"`, `"rendimentos"`, `"saude"`, `"dados_processuais"`, `"biometricos"`, `"outros"`. Ver §1.4. |
| `base_legal_conservacao` | Condicional | string (enum) | Obrigatório se `contem_dados_pessoais: true`. `"obrigacao_legal"` \| `"interesse_publico"` \| `"consentimento"` \| `"contrato"`. Ver §1.4. |
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

- **Tipo**: string no formato normativo `<id>@<versao>` definido pelo registo
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
especificação separada) — não uma string plana. A estrutura concreta continua a ser
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

- **Profundidade de aninhamento e tamanho**: o JCS (RFC 8785) e o JSON em geral não impõem limites teóricos de profundidade/tamanho, mas implementações concretas (parsers, validadores de schema) podem ter limites práticos. Para tipos de documento muito complexos (Modelo 3 IRS pode ter milhares de campos preenchidos com múltiplos anexos), a implementação DEVE validar que: (a) a canonicalização JCS é determinística e performante mesmo para `documento` de grande dimensão; (b) os validadores JSON Schema dos `tipo_documento_ref` mais complexos não excedem limites de profundidade/recursão dos validadores escolhidos (ver prompt de implementação do schema/validador).
- **Eficiência de armazenamento permanece válida**: mesmo um Modelo 3 IRS complexo, em JSON estruturado, é tipicamente muito mais compacto do que o PDF oficial equivalente (que inclui layout completo de todos os anexos, mesmo os não preenchidos). O argumento de economia de espaço (ver discussão de vantagens do NDF) mantém-se, possivelmente de forma ainda mais pronunciada para formulários longos com muitas secções não aplicáveis/vazias no PDF mas ausentes no NDF.
- **Anexos binários dentro de formulários complexos**: se um `tipo_documento` exigir anexos binários (ex. comprovativos digitalizados anexos a uma declaração), estes seguem o regime de documentos importados/preservação bit-a-bit (fora de âmbito desta especificação) — `documento` referencia-os por identificador/hash, nunca os embute.

### 2.10 Nível de assinatura eletrónica (`nivel_assinatura`)

Declara o nível de assinatura eletrónica que o sistema produtor determinou
ser adequado a este documento, segundo a natureza jurídica do ato e a
política aplicável (ver §2.10.2 — a decisão em si é sempre da entidade
produtora, nunca do NDF). Determina quais os passos do pipeline de
finalização (§5.2) que são obrigatórios e que tipo de certificado é
requerido.

**Distinção importante**: `nivel_assinatura` refere-se ao requisito de
assinatura pessoal declarado pelo produtor. É independente da integridade
e da imutabilidade de custódia. Todo o NDF tem JCS e hash; CAdES é
obrigatório apenas para `"avancada"` e `"qualificada"`. Armazenamento
append-only/WORM e auditoria pertencem ao Perfil de Ciclo de Vida
NORMORDIS (§2.4, §9.5), opcional — não são garantidos pelo `nivel_assinatura`
nem por nenhum outro campo do NDF-core. Um documento com
`"nenhuma"` **PODE** receber um selo institucional opcional, sem que isso constitua
uma assinatura pessoal. Ver a arquitetura normativa comum em
`docs/architecture/ARCHITECTURE.md`.

#### 2.10.1 Valores (enum fechado)

| Valor | Nível eIDAS | Requisito de certificado | Passos obrigatórios no pipeline | Exemplos de atos |
|---|---|---|---|---|
| `"nenhuma"` | — | Nenhum | Passos 1–3 e 8 (canonicalização, hash, validation_code, persistência) | Registos internos sem efeito externo, logs de operação, tabelas de presença, minutas. |
| `"avancada"` | SEA — Assinatura Eletrónica Avançada (eIDAS Art.º 26.º) | Certificado com identificação única do signatário; não obrigatoriamente qualificado | Passos 1–8 com CAdES-B-LTA | Ofícios, informações técnicas, pareceres, despachos de mero expediente, notificações de rotina. |
| `"qualificada"` | SEQ — Assinatura Eletrónica Qualificada (eIDAS Art.º 25.º) | Certificado qualificado emitido por PSSC inscrito na lista de confiança eIDAS; equivalente legal à assinatura manuscrita | Passos 1–8 com CAdES-B-LTA | Contratos públicos, atos com efeito patrimonial significativo, decisões com impacto jurídico direto. |

#### 2.10.2 Responsabilidade de classificação

A classificação correcta de um ato num destes três níveis é **responsabilidade da entidade produtora**. A especificação NDF não define o mapeamento entre tipos de ato e níveis de assinatura — essa é uma decisão de direito administrativo, que cada entidade define de acordo com o CPA, os estatutos sectoriais, e as suas normas internas de delegação de competência e autenticidade documental.

#### 2.10.3 Implicações para o envelope

| `nivel_assinatura` | `assinaturas[]` | `timestamps` | `validation_material` | `validation_code` |
|---|---|---|---|---|
| `"nenhuma"` | Ausente ou `[]` | Ausente (opcional por razões de arquivo) | Ausente | **Sempre presente** |
| `"avancada"` | CAdES-B-LTA com certificado SEA | Presente (B-T + B-LTA) | Presente | **Sempre presente** |
| `"qualificada"` | CAdES-B-LTA com certificado SEQ qualificado PSSC | Presente (B-T + B-LTA) | Presente | **Sempre presente** |

#### 2.10.4 Integridade de arquivo para `nivel_assinatura: "nenhuma"`

Mesmo quando o ato não requer assinatura eletrónica para validade jurídica, há casos em que a conservação do registo impõe integridade a longo prazo. A seguinte regra aplica-se:

| Condição arquivística | Requisito de envelope |
|---|---|
| `destino_final: "eliminacao"` E PCA ≤ 5 anos | Envelope mínimo (apenas `validation_code` + `payload_hash`). CAdES-B-LTA **não obrigatório**. |
| `destino_final: "eliminacao"` E PCA > 5 anos | Selo institucional CAdES-B-LTA RECOMENDADO para portabilidade da prova de origem. |
| `destino_final: "conservacao_parcial_por_amostragem"` | Selo institucional CAdES-B-LTA RECOMENDADO para os documentos seleccionados. |
| `destino_final: "conservacao_permanente"` | Selo institucional CAdES-B-LTA RECOMENDADO. Requisitos adicionais de custódia (armazenamento append-only/WORM, auditoria) dependem de o sistema custodiante adotar o Perfil de Ciclo de Vida NORMORDIS (§9.5) ou um modelo próprio equivalente — não são exigidos pela conformidade NDF de base. |

Quando CAdES-B-LTA é aplicado a um documento com `nivel_assinatura: "nenhuma"`, o envelope DEVE usar um **selo institucional** (não uma assinatura pessoal) — um certificado de autenticação da entidade produtora ou do sistema de gestão documental, não um certificado qualificado pessoal. O efeito jurídico é de integridade técnica, não de assinatura com efeito legal equivalente à manuscrita.

### 2.11 Relações documentais (`relacoes`)

#### 2.11.1 Objetivo e princípio

Um procedimento administrativo é tipicamente composto por vários documentos
autónomos e relacionados — uma informação técnica, um ou mais pareceres, um
despacho — cada um com o seu próprio `ndf_id`, hash e assinaturas (§2.9,
Anexo A). O campo opcional `relacoes` regista essas relações **dentro do
NDF-core**, e não no envelope, precisamente para que a relação fique coberta
pela mesma assinatura e canonicalização que protege o conteúdo do documento.

Cada relação DEVE identificar o documento alvo por `ndf_id` **e**
`payload_hash` — nunca apenas por `ndf_id`. O `payload_hash` liga a relação
aos bytes canónicos exatos que existiam no momento em que a relação foi
estabelecida, não a uma identidade lógica que poderá entretanto ter sido
substituída por uma nova versão do mesmo documento.

```json
{
  "relacoes": [
    {
      "tipo": "emite_parecer_sobre",
      "alvo": {
        "ndf_id": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
        "payload_hash": "sha256:3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b",
        "descricao": "Informação técnica IT/2026/00045"
      },
      "papel": "informacao_base"
    }
  ]
}
```

#### 2.11.2 Vocabulário de relações (enum fechado)

| Valor | Significado |
|---|---|
| `substitui` | O documento alvo é substituído por este (cadeia de proveniência de versões, §6). |
| `corrige` | Este documento corrige informação do alvo, sem o substituir formalmente. |
| `complementa` | Este documento acrescenta informação ao alvo, sem o substituir nem corrigir. |
| `anula` | Este documento anula os efeitos do alvo. |
| `responde_a` | Este documento é uma resposta ao alvo (ex.: resposta a requerimento). |
| `emite_parecer_sobre` | Este documento é um parecer emitido sobre o alvo. |
| `decide_sobre` | Este documento é uma decisão (despacho) sobre o alvo. |
| `executa` | Este documento executa o que o alvo determina. |
| `anexa` | O alvo é anexado a este documento. |
| `deriva_de` | Este documento deriva do alvo, sem ser uma nova versão formal. |
| `referencia` | Ligação informativa, sem implicação jurídico-documental direta. |

Este vocabulário base é fechado nesta versão. Estendê-lo requer uma nova
versão minor desta especificação — o mesmo princípio já aplicado a
`classificacao_seguranca` (§2.7.4) e `destino_final` (§3.4). Para tipos de
relação específicos de um domínio ou entidade, sem esperar por uma nova
versão da especificação, ver o mecanismo de extensão qualificada em
§2.11.7.

**Correspondência informativa com PROV-O** (W3C) — não normativa, apenas para
interoperabilidade semântica fora do ecossistema NORMORDIS — consta de
[`docs/normalization/NDF-INFORMATIVE-GUIDANCE.md`](../../docs/normalization/NDF-INFORMATIVE-GUIDANCE.md).

#### 2.11.3 Relação com `versao_anterior`/`hash_anterior` (§6.2)

`relacoes` e `versao_anterior`/`hash_anterior` (envelope) cobrem propósitos
sobrepostos mas não idênticos: `versao_anterior`/`hash_anterior` é um atalho
operacional de cadeia linear, fora do core; uma relação `"tipo": "substitui"`
em `relacoes` é o mesmo facto, mas coberto pela assinatura. Um sistema
produtor que crie um NDF substituto de outro **RECOMENDA-SE** que preencha
ambos, mantendo-os coerentes. Não é uma obrigação — sistemas que só precisem
de versionamento linear simples **PODEM** continuar a usar apenas o
mecanismo do envelope.

#### 2.11.4 Relação com campos de tipo de documento (ex.: `despacho.sobre`)

Alguns tipos de documento do registo (ex.: `despacho@1.0.0`, ver
`specs/registry/SPEC.md`) já têm campos próprios de referência a outros
documentos por `ndf_id`, para legibilidade humana e indexação específica do
tipo. `relacoes` é o mecanismo genérico e a fonte de verdade
criptograficamente verificável para qualquer produtor conforme; quando um
tipo de documento tiver o seu próprio campo de referência, um produtor
conforme DEVE manter os dois coerentes (mesmo conjunto de `ndf_id`
referenciados).

Os requisitos normativos de produtor e leitor para `relacoes` estão
enumerados em §9.1 e §9.2.

#### 2.11.5 Segurança e privacidade do grafo de relações

Uma relação DEVE ser interpretada como uma afirmação unilateral e assinada
da entidade produtora do documento de origem — não implica reconhecimento,
consentimento, nem validação de competência por parte da entidade
produtora do documento alvo. A validação de autoridade para estabelecer
uma relação (quem tem competência para decidir sobre, anular, ou responder
a outro documento) é responsabilidade do sistema de gestão processual,
fora do âmbito desta especificação.

O vocabulário fechado de §2.11.2 não impede ciclos entre documentos
independentes (ex.: A `substitui` B e B `substitui` A). Um verificador ou
renderizador que percorra o grafo DEVE implementar deteção de ciclos — o
schema, por si só, não impõe acircularidade entre documentos assinados de
forma independente.

#### 2.11.6 Exemplo

`specs/ndf/examples/informacao-parecer-despacho/` contém um exemplo completo
de três NDF autónomos (informação técnica, parecer, despacho) ligados por
`relacoes[]`, com hashes reais recalculáveis e diagrama do grafo.

#### 2.11.7 Extensão qualificada de `relacoes[].tipo`

Além do vocabulário base fechado (§2.11.2), `relacoes[].tipo` aceita um
valor de **extensão qualificada**, no formato:

```
ext.<entidade>.<tipo>
```

| Componente | Regras | Exemplo |
|---|---|---|
| `entidade` | lowercase, `[a-z][a-z0-9-]*` | `at`, `municipio-lisboa` |
| `tipo` | lowercase, `[a-z][a-z0-9_-]*` | `retificacao-oficiosa` |

**Exemplo válido**: `"ext.at.retificacao-oficiosa"`.

Este mecanismo permite a uma entidade produtora declarar tipos de relação
específicos do seu domínio administrativo sem esperar por uma nova versão
minor desta especificação — o mesmo espírito do registo de tipos de
documento (`specs/registry/`), aplicado ao vocabulário de relações. Não há
um registo central de extensões: o namespace `<entidade>` é autodeclarado,
com o mesmo risco de colisão semântica que qualquer namespace autodeclarado
(ex.: pacotes Java, namespaces XML) — mitigado, na prática, por
`<entidade>` corresponder tipicamente a um identificador organizacional já
reconhecido (código DGLAB, sigla institucional).

Uma extensão qualificada NÃO DEVE ser interpretada como parte do
vocabulário normativo desta especificação — a sua semântica é definida e da
responsabilidade exclusiva da entidade que a declara. Um leitor conforme
que não reconheça uma extensão qualificada DEVE tratá-la como relação de
tipo desconhecido para efeitos de interpretação semântica, mas NÃO DEVE
rejeitar o documento só por esse motivo — a relação continua
estruturalmente válida (formato correto, `alvo` verificável por hash).

### 2.12 Participantes (`participantes`)

#### 2.12.1 Objetivo

Distingue **autoria e participação** de **assinatura eletrónica** (Anexo A;
ver também §4 — Envelope). Um autor poderá não assinar; um signatário
poderá assinar num papel de aprovador ou representante sem ser autor
material. O
bloco `participantes`, opcional, regista essa informação de forma estrutural
e independente do texto de exibição que já existe nalguns schemas de tipo de
documento (ex.: `informacao-tecnica.autor`, `despacho.decisor`) — esses
campos continuam a servir a apresentação do documento (via NDT); `participantes`
serve a consulta, auditoria e o grafo documental.

```json
{
  "participantes": [
    { "participante_ref": "user:123", "tipo": "pessoa", "papel": "autor" },
    { "participante_ref": "user:456", "tipo": "pessoa", "papel": "revisor_humano" }
  ]
}
```

#### 2.12.2 Campos

| Campo | Obrigatório | Descrição |
|---|---|---|
| `participante_ref` | Sim | Identificador institucional estável — não um nome de exibição. |
| `tipo` | Não | `pessoa` \| `sistema` \| `entidade`. Assume-se `pessoa` quando omitido. |
| `papel` | Sim | `autor`, `coautor`, `revisor_humano`, `validador`, `aprovador`, `decisor`, `representante`, `entidade_produtora`, `sistema_tecnico`. |

Um sistema de IA interveniente PODE ser registado com `tipo: "sistema"` e
`papel: "sistema_tecnico"` — nunca com um papel que implique autoria,
aprovação ou decisão (ver §2.13.4).

#### 2.12.3 `participante_ref` como referência externa

`participante_ref` é uma referência externa, não resolvida pelo NDF —
paralelo direto a `avaliacao.tipo_classificacao_ref` (§3.2.1), que também
referencia um instrumento externo sem o incorporar. O NDF não define nem
embute um esquema de identidade verificável: a resolução de
`participante_ref` para uma identidade concreta (nome, função,
credenciais) é responsabilidade do sistema produtor, que mantém o registo
correspondente na sua própria base de dados.

#### 2.12.4 `validador` e `aprovador` — estado de workflow, não de conteúdo

Os papéis `validador` e `aprovador` descrevem estado de um fluxo de
aprovação, tipicamente já gerido pelo sistema de workflow do produtor
(GED/GCA) — o seu uso em `participantes` é desaconselhado fora de sistemas
que já tratem esse estado como parte constitutiva do conteúdo do documento.
Não foram removidos do enum de §2.12.2: retirá-los seria uma alteração
incompatível sem necessidade demonstrada. A decisão de os usar, ou de
manter esse estado apenas no sistema de workflow, cabe ao sistema produtor.

### 2.13 Proveniência de IA (`proveniencia_ia`)

#### 2.13.1 Objetivo e âmbito

Bloco opcional, só relevante quando um sistema de IA influenciou
materialmente a criação, transformação, classificação, fundamentação ou
revisão do conteúdo de `documento`. O NDF não impõe nem garante conformidade
com o AI Act ou qualquer outro regime jurídico — fornece mecanismos técnicos
que poderão apoiar rastreabilidade, transparência, supervisão humana e
conservação de evidências relativas ao uso de sistemas de IA. A conformidade
jurídica depende do sistema, finalidade, classificação de risco, operadores,
contexto jurídico e medidas técnicas e organizativas aplicáveis — não é
garantida pelo formato isoladamente (mesmo princípio de §1.1 e §1.4 aplicado
a IA). Orientação informativa adicional consta de
[`docs/normalization/AI-PROVENANCE-GUIDANCE.md`](../../docs/normalization/AI-PROVENANCE-GUIDANCE.md).

#### 2.13.2 Dois níveis de evidência

1. **Proveniência essencial** — no NDF-core, coberta pela assinatura:
   finalidade, sistema/fornecedor/modelo/versão, data, resultado incorporado,
   segmentos afetados, estado da revisão humana.
2. **Logs detalhados** — fora do NDF (prompts integrais, respostas
   completas), sob política própria de acesso e retenção, ligados por
   `evidencia_ref` (identificador + hash). NÃO DEVEM ser embutidos
   obrigatoriamente no NDF-core: poderão conter dados pessoais, informação
   confidencial ou material desproporcionado para conservação permanente.

```json
{
  "proveniencia_ia": {
    "utilizada": true,
    "intervencoes": [
      {
        "intervencao_id": "b2c3d4e5-f6a7-4890-bcde-f01234567890",
        "finalidade": "apoio_redacao",
        "sistema": { "nome": "string", "fornecedor": "string", "modelo": "string", "versao": "string" },
        "executada_em": "2026-06-18T10:30:00Z",
        "resultado_incorporado": "parcialmente",
        "segmentos_afetados": ["documento.fundamentacao"],
        "revisao_humana": {
          "estado": "revisto_e_aprovado",
          "revisor_ref": "user:456",
          "revisto_em": "2026-06-18T11:00:00Z"
        },
        "evidencia_ref": { "tipo": "registo_externo", "identificador": "string", "hash": "sha256:..." }
      }
    ]
  }
}
```

#### 2.13.3 Estado de revisão humana

`revisao_humana.estado` é obrigatório em cada intervenção — incluindo o
valor `"pendente"`, para que a ausência de revisão seja **representável e
visível**, não apenas omitida. Quando o estado for `revisto_e_aprovado`,
`revisto_com_alteracoes` ou `rejeitado`, `revisor_ref` e `revisto_em` DEVEM
estar presentes.

#### 2.13.4 IA não é signatária nem decisora

Um sistema de IA NÃO DEVE ser registado como `signatario` de uma assinatura
(§4), nem como `participante` com papel de autor, aprovador ou decisor
(§2.12.2). A IA **PODE** ser registada em `proveniencia_ia.intervencoes[].sistema`
como sistema técnico interveniente, e opcionalmente em `participantes` com
`papel: "sistema_tecnico"`. O ato administrativo depende sempre de
intervenção humana identificável.

Os requisitos normativos de produtor e leitor para `proveniencia_ia` estão
enumerados em §9.1 e §9.2.

---

## 3. Avaliação arquivística (PCA/DF — MEG/DGLAB)

### 3.1 Fundamento

Conforme o MEG e os instrumentos da DGLAB (Lista Consolidada e Tabelas de Seleção), todo o documento de arquivo DEVE ter associada uma decisão de avaliação que determina:

- O **Prazo de Conservação Administrativa (PCA)** — período de manutenção da informação segundo o instrumento aplicável.
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

O instrumento e a versão consultados são registados em `instrumento_avaliacao_versao_ref`, permitindo que a regra aplicável seja rastreável mesmo após atualização do instrumento.

**RECOMENDA-SE** que o sistema produtor resolva `tipo_classificacao_ref`
automaticamente a partir do tipo de documento, para reduzir erro humano e
garantir consistência entre documentos do mesmo tipo. O NDF não exige um
processo específico de resolução — manual, automático, ou por outra regra
é responsabilidade da aplicação produtora — apenas que o valor final seja
válido, coerente com o instrumento referenciado, e imutável após a
finalização (§2.1).

### 3.2.2 Formato normativo de `instrumento_avaliacao_versao_ref`

A string segue o formato `"<instrumento>/<versao>"`:

| Componente | Descrição |
|---|---|
| `instrumento` | Identificador do instrumento. Valores canónicos: `"lc"` (Lista Consolidada DGLAB), `"pgd"` (Plano de Gestão de Documentos), `"portaria"` (Portaria de Gestão de Documentos), `"ts"` (Tabela de Seleção institucional). Extensível por entidades com instrumentos próprios. |
| `versao` | Identificador da versão ou edição consultada — suficiente para localizar o instrumento exato. Não há formato imposto; RECOMENDA-SE incluir ano e número de revisão. |

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

### 3.5 Resolução de `prazo_conservacao_administrativa` e `destino_final`

`prazo_conservacao_administrativa` e `destino_final` DEVEM ser coerentes
com `tipo_classificacao_ref` e com o instrumento de avaliação identificado
em `instrumento_avaliacao_versao_ref` no momento da finalização — este
último regista qual o instrumento e versão consultados, preservando a
regra aplicável mesmo que o instrumento seja atualizado posteriormente. O
NDF não impõe o processo pelo qual esses valores são determinados;
**RECOMENDA-SE** resolvê-los automaticamente a partir do instrumento de
avaliação carregado no sistema, para reduzir erro humano — mas essa é uma
decisão de implementação da aplicação produtora, não um requisito do
formato.

### 3.6 Dados derivados (fora do NDF-core)

A partir de `avaliacao.prazo_conservacao_administrativa` e da data de finalização (`finalizado_em`, campo do envelope/metadados operacionais — não do NDF-core), o sistema calcula e mantém uma data de elegibilidade para aplicação do destino final. Este valor:

- **Não** faz parte do NDF-core (não é canonicalizado nem assinado).
- É puramente operacional, recalculável, e usado para processos de gestão de arquivo (identificação de documentos elegíveis para aplicação de destino final).

---

## 4. Envelope de integridade e autenticidade

### 4.1 Componentes

| Componente | Conteúdo | Norma | Condicional |
|---|---|---|---|
| `assinaturas[]` | Assinaturas pessoais ou selos institucionais CAdES sobre os `payload_bytes` canónicos — cada entrada é uma unidade de prova autocontida (identidade, certificado, timestamps RFC 3161 e material de validação próprios). Ver §4.4. | CAdES (ETSI EN 319 122), nível B-LTA | Assinatura pessoal obrigatória se `nivel_assinatura ∈ {"avancada", "qualificada"}`; selo institucional opcional se `"nenhuma"` |
| `validation_code` | Código de verificação canónico — derivado de `ndf_id` + `payload_hash`. Ver §4.6. | Esta especificação | **Sempre presente** — independente de `nivel_assinatura` |

`timestamps` e `validation_material` **não são componentes de topo do
envelope** — vivem dentro de cada entrada de `assinaturas[]` (§4.4.2), para
que a associação entre prova, certificado, cadeia e timestamp nunca seja
ambígua quando existir mais do que uma assinatura independente.

### 4.2 Nível alvo quando CAdES é usado: CAdES-B-LTA

CAdES-B-LTA (Long Term Archival) fornece mecanismos para:

- **B** (Basic): assinatura sobre o digest, com certificado do signatário.
- **T** (Timestamp): timestamp sobre o valor da assinatura, prova de quando a assinatura foi criada.
- **LT** (Long Term): inclusão da cadeia de certificados e dados de revogação, permitindo validação mesmo que o repositório de revogação original deixe de estar acessível.
- **A** (Archive): timestamp de arquivo adicional sobre assinatura + dados LT, protegendo contra a expiração/comprometimento futuro dos algoritmos/certificados usados na assinatura original.

### 4.2.1 Requisitos da Autoridade de Timestamp (TSA)

O timestamp RFC 3161 (B-T e B-LTA) DEVE ser emitido por uma TSA que cumpra os seguintes requisitos:

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

A mitigação completa deste risco faz parte do **roadmap desta especificação** (ver roadmap informativo). A estratégia prevista é a re-selagem periódica: aplicação de um novo timestamp de arquivo com algoritmos mais recentes sobre o envelope existente, sem alterar `payload_bytes`. Esta operação não viola a imutabilidade do NDF-core — o conteúdo não muda, apenas a camada de prova temporal é reforçada.

### 4.4 Múltiplas assinaturas

`assinaturas` é um array — um NDF aceita mais do que uma assinatura (ex.:
assinatura de autor + selo institucional/visto, ou coautoria). Cada entrada é
independente e assina os mesmos `payload_bytes` canónicos em modo detached. O
digest usado internamente pelo contentor CAdES DEVE coincidir com
`payload_hash`.

Múltiplas assinaturas do mesmo NDF destinam-se a coautoria, aprovação
conjunta ou selo institucional sobre o mesmo conteúdo — não a encadear
documentos distintos. Um parecer sobre uma informação, ou um despacho sobre
um parecer, NÃO DEVEM ser representados como uma segunda assinatura do
documento original: são NDF autónomos, ligados por `relacoes` (§2.11).

#### 4.4.1 Unidade de prova autocontida

Cada entrada de `assinaturas[]` é autossuficiente: inclui identidade,
certificado, `timestamps` e `validation_material` próprios, além de:

| Campo | Obrigatório | Descrição |
|---|---|---|
| `assinatura_id` | Sim | Identificador estável desta entrada de assinatura — permite referenciá-la sem ambiguidade (ex.: de um evento de custódia de renovação). |
| `nivel` | Sim | `selo_institucional` \| `avancada` \| `qualificada`. |
| `papel` | Não | Papel administrativo exercido **neste documento**: `autor`, `coautor`, `validador`, `aprovador`, `decisor`, `representante`, `testemunha`, `selante`. Distinto de `signatario.cargo` (cargo organizacional) — uma pessoa poderá ter o cargo "Diretor de Serviços" e assinar no papel de `decisor`. |
| `ordem` | Não | Indicação descritiva de ordem entre coassinaturas. Não é um motor de workflow: quórum, sequência obrigatória e estado de aprovação pertencem ao sistema de gestão documental, não a esta especificação. |
| `signatario` | Condicional | Identidade do signatário — obrigatório quando `nivel ∈ {"avancada", "qualificada"}`. |
| `cades_b_lta` | Sim | Assinatura CAdES-B-LTA detached (DER). |
| `timestamps` | Condicional | RFC 3161 B-T + B-LTA desta assinatura — obrigatório quando `nivel ∈ {"avancada", "qualificada"}`. |
| `validation_material` | Condicional | Cadeia de certificados + revogação desta assinatura — obrigatório quando `nivel ∈ {"avancada", "qualificada"}`. |

Não existe um modelo dual (campos globais + campos por assinatura): manter
os dois caminhos de leitura válidos para o mesmo dado obrigaria qualquer
verificador a saber qual usar, sem benefício de compatibilidade — não há
implementação nem adoção externa do formato de envelope anterior a proteger.

O NDF não garante, nem verifica, que exista uma assinatura com `papel`
correspondente à exigência legal de quem tem de assinar um determinado ato
(ex.: que um `decisor` tenha efetivamente assinado, e não apenas uma
`testemunha`). Essa correspondência é responsabilidade da entidade
produtora, decidida segundo o CPA, estatutos setoriais e normas internas de
delegação — o mesmo princípio já aplicado à classificação de
`nivel_assinatura` (§2.10.2).

#### 4.4.2 Preservação da assinatura original

Quando `nivel_assinatura ∈ {"avancada", "qualificada"}`, a assinatura CAdES é
parte integrante e obrigatória do documento arquivado. Este é um requisito
de formato/pacote — aplica-se a qualquer implementação que preserve o
NDF-core, independentemente de adotar ou não o Perfil de Ciclo de Vida
NORMORDIS (§9.5). Enquanto o NDF-core for preservado, a implementação DEVE:

1. preservar byte a byte o contentor CAdES original;
2. preservar os timestamps RFC 3161 e o material de validação associados;
3. impedir alteração, substituição ou remoção isolada destes objetos;
4. incluir estes objetos nos hashes do inventário do `.ndfpkg`, quando exportado nesse formato.

Uma re-selagem, renovação de timestamp ou migração de algoritmo NÃO DEVE
substituir a assinatura original. A nova prova protege a cadeia anterior e é
acrescentada ao envelope. Sistemas que implementem o Perfil de Ciclo de
Vida NORMORDIS DEVEM, adicionalmente, registar cada renovação criptográfica
como novo evento append-only no log de custódia (§2.4.2, §9.5) — este passo
adicional não é requisito de conformidade NDF de base. A eliminação dos
objetos de assinatura só é permitida juntamente com a eliminação
arquivística formalmente autorizada do próprio documento (§2.4.3).

### 4.5 Mecanismos de assinatura suportados

A especificação do NDF não depende do dispositivo de assinatura. Quando CAdES
é exigido ou aplicado, o resultado DEVE ser uma assinatura detached
CAdES-B-LTA válida sobre `payload_bytes`. Mecanismos possíveis incluem Cartão
de Cidadão, HSM institucional, selo eletrónico e Chave Móvel Digital.

### 4.6 `validation_code` — Código de verificação canónico

#### 4.6.1 Propósito

O `validation_code` é um identificador curto aposto à representação visual
do documento. É intrinsecamente do formato: derivado deterministicamente de
`ndf_id` e `payload_hash` (§4.6.2), verificável por qualquer implementação
sem depender de nenhum serviço externo (§4.6.4). O seu uso típico é permitir
ao público consultar um serviço de verificação — por exemplo, mas não
exclusivamente, o portal público de uma entidade custodiante — que resolve
o código para o registo sob custódia e confirma autenticidade
institucional, entidade produtora, hash e estado corrente. O código também
permite confirmar a correspondência com `ndf_id` e `payload_hash`;
isoladamente e fora de um custodiante confiável, não prova autoria ou
origem institucional.

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
implementação consegue confirmar que o código corresponde ao `ndf_id` e
`payload_hash` apresentados. Esta verificação não autentica o emissor.

Um serviço de verificação pública (ex.: o portal de referência NORMORDIS,
`https://validar.normordis.pt/<validation_code>`) serve tipicamente de
âncora pública de custódia — não é requisito de conformidade NDF, é uma
funcionalidade de serviço que qualquer entidade custodiante está livre de
disponibilizar sobre o seu próprio acervo. Quando um serviço deste tipo
existir, uma resposta positiva DEVE resultar da comparação do código com o
NDF preservado, da verificação do `payload_hash` e da consulta do estado
corrente; quando exista CAdES, DEVE também validar a assinatura ou selo e
indicar o resultado. A verificação offline continua possível, mas só
confirma autenticidade quando exista uma âncora de confiança local,
assinatura ou selo verificável.

#### 4.6.5 Representações

**Texto** (para impressão, correspondência, citação):
```
NDF-A3F7K-2MXPQ-R9ZTN-W8VJX
```

**QR code** (elemento `codigo_barras` no NDT, §5.3.7 da especificação NDT):
```
https://validar.normordis.pt/NDF-A3F7K-2MXPQ-R9ZTN-W8VJX
```

O NDT referencia o `validation_code` através do placeholder `{{validation_code}}` no elemento `codigo_barras` (e em qualquer `texto_fixo` ou `mobilia[]` que o necessite). Este placeholder é resolvido pelo renderizador a partir do envelope — não é um dado do NDF-core nem um metadado do NDT, mas um valor computado no momento da finalização. Ambas as representações são obrigatórias em documentos emitidos para o exterior — a forma texto para leitura humana e o QR code para leitura por dispositivo.

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
- `nivel_assinatura ∈ {"avancada", "qualificada"}` e não estiver disponível um certificado eletrónico conforme (SEA ou SEQ, respectivamente).
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
8. Persistir `payload_bytes` e envelope de forma atómica — nenhuma escrita
parcial ou inconsistente entre os dois DEVE ficar visível a um leitor. Para
`nivel_assinatura: "nenhuma"`, assinatura, timestamps e material de validação
**PODEM** estar ausentes; um selo institucional continua permitido. Um
sistema que implemente o Perfil de Ciclo de Vida NORMORDIS (§2.4, §9.5)
DEVE, adicionalmente, usar armazenamento append-only/WORM e criar o evento
inicial no log de custódia — não é requisito de conformidade NDF de base.

### 5.3 Pós-condições

- `payload_bytes` DEVE ser tratado como imutável para sempre.
- Assinaturas CAdES originais, timestamps e material de validação DEVEM ser
  preservados byte a byte enquanto o documento for conservado.
- Entradas existentes do envelope NÃO DEVEM ser alteradas. Provas de
  re-selagem **PODEM** ser acrescentadas de forma append-only e auditada.
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

O formato `.ndfpkg` é o **pacote de exportação autocontido** de um NDF
finalizado. É definido nesta especificação (§8) e reúne os objetos necessários
para verificação, renderização e preservação sem dependências externas.

A cadeia de proveniência de um processo documental é uma coleção de pacotes `.ndfpkg` independentes, ligados por referências leves (`versao_anterior`/`hash_anterior`), nunca por conteúdo embutido.

---

## 7. Versionamento da especificação NDF

A especificação NDF segue **Semantic Versioning 2.0.0** (SemVer — https://semver.org/), com as seguintes regras normativas:

### 7.1 `ndf_version`

Cada NDF-core declara a versão da especificação NDF a que adere no campo `ndf_version` (string, formato `MAJOR.MINOR.PATCH`). Este campo é obrigatório, faz parte do NDF-core canonicalizado e assinado, e é imutável após finalização.

| Componente | Quando muda | Impacto |
|---|---|---|
| `MAJOR` | Mudanças incompatíveis: remoção ou renomeação de campos obrigatórios, alteração de semântica existente, mudança de algoritmo de canonicalização | Leitores antigos recusam processar |
| `MINOR` | Adição compatível de campos ou blocos opcionais | Requer schema da nova versão; leitores antigos **PODEM** preservar o documento como opaco, mas não ignoram conteúdo assinado desconhecido |
| `PATCH` | Correções de clareza na especificação sem impacto comportamental | Sem impacto em leitores |

### 7.2 Compatibilidade retroativa

Um leitor NDF DEVE declarar explicitamente as versões que suporta. O schema de
cada release valida apenas a sua versão exata. Um leitor DEVE rejeitar uma
versão que não suporte ou tratá-la como objeto opaco, sem afirmar que
interpretou o documento. Conteúdo assinado desconhecido não é ignorado
silenciosamente. Compatibilidade entre versões é uma propriedade documentada
da implementação, não uma licença para validar um documento novo contra um
schema antigo.

### 7.3 Versionamento de schemas de tipo de documento

O campo `tipo_documento_ref` em `metadados` segue o mesmo princípio SemVer (ex.: `oficio@1.2.0`, `modelo3-irs@2026.1.0`). A versão do schema de tipo de documento é independente da versão da especificação NDF — o mesmo tipo de documento pode ter múltiplas versões de schema sem que a especificação NDF mude.

---

## 8. Pacote de exportação (`.ndfpkg`)

O `.ndfpkg` é o formato de exportação autocontido de um NDF finalizado. Reúne
os objetos necessários para verificar, renderizar e preservar o documento sem
depender do sistema produtor original.

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
- **Verificabilidade**: o pacote permite a qualquer implementação conforme verificar `sha256(ndf-core.json) == payload_hash` e validar a assinatura CAdES-B-LTA sem acesso ao core-documental original.
- **Cadeia de proveniência**: o `manifest.json` regista `versao_anterior` e `hash_anterior` quando aplicável, permitindo reconstruir a cadeia de versões com múltiplos `.ndfpkg`.

---

## 9. Conformidade

### 9.1 Produtor conforme

Uma implementação é um **produtor NDF conforme** se e apenas se satisfizer todos os seguintes requisitos:

1. **NDF-PROD-001 — DEVE** gerar NDF-core JSON que valida contra o schema `specs/ndf/schemas/ndf-core.schema.json` (JSON Schema Draft 2020-12).
2. **NDF-PROD-002 — DEVE** canonicalizar o NDF-core via JCS (RFC 8785) produzindo `payload_bytes` determinísticos — bytes idênticos para a mesma estrutura lógica independentemente da ordem de inserção de chaves ou formatação de origem.
3. **NDF-PROD-003 — DEVE** calcular `payload_hash = SHA-256(payload_bytes)` conforme NIST FIPS 180-4.
4. **NDF-PROD-004 — DEVE** calcular `validation_code` conforme o algoritmo definido em §4.6.2.
5. **NDF-PROD-005 — DEVE** executar os passos do pipeline de finalização conforme `nivel_assinatura` declarado (§5.2):
   - Para `"nenhuma"`: passos 1–3 e 8 obrigatórios.
   - Para `"avancada"` ou `"qualificada"`: todos os passos 1–8 obrigatórios.
6. **NDF-PROD-006 — DEVE** incluir todos os campos obrigatórios de `metadados` (§2.7.2), incluindo os condicionais RGPD quando `contem_dados_pessoais: true`.
7. **NDF-PROD-007 — DEVE** definir `tipo_classificacao_ref` no formato `<instrumento>/<codigo>` (§3.2.1).
8. **NDF-PROD-008 — DEVE** gerar `ndf_id` como UUID v4 válido (RFC 9562), único no espaço de nomes do sistema produtor.
9. **NDF-PROD-009 — DEVE** definir `estado: "ativo"` no NDF-core de qualquer documento recém-finalizado.
10. **NDF-PROD-010 — DEVE** persistir `payload_bytes` e o envelope de forma atómica — nenhuma escrita parcial ou inconsistente entre os dois deve ficar visível a um leitor (§5.2, passo 8). Não inclui o Perfil de Ciclo de Vida NORMORDIS — ver §9.5.
11. **NDF-PROD-011 — DEVE** produzir saídas aceites pelo validador e pelas verificações semânticas oficiais; os casos válidos são referências de interoperabilidade, não entradas do produtor. todos os casos de `conformance/ndf/valid/` sem erro.
12. **NDF-PROD-012 — DEVE**, quando `relacoes` estiver presente, incluir em cada elemento `tipo`, `alvo.ndf_id` e `alvo.payload_hash` (§2.11).
13. **NDF-PROD-013 — DEVE** incluir `intervencoes` com pelo menos um elemento quando `proveniencia_ia.utilizada` for `true`, e omitir ou esvaziar `intervencoes` quando for `false` (§2.13).
14. **NDF-PROD-014 — DEVE** incluir `revisao_humana.estado` em cada elemento de `proveniencia_ia.intervencoes`, e `revisor_ref`+`revisto_em` quando o estado for terminal (§2.13.3).

### 9.2 Leitor conforme

Uma implementação é um **leitor NDF conforme** se e apenas se satisfizer todos os seguintes requisitos:

1. **NDF-READ-001 — DEVE** rejeitar qualquer NDF-core que não valide contra o schema desta versão.
2. **NDF-READ-002 — DEVE** rejeitar versões NDF não suportadas explicitamente ou tratá-las como opacas, sem declarar interpretação completa.
3. **NDF-READ-003 — NÃO DEVE** ignorar silenciosamente conteúdo assinado desconhecido.
4. **NDF-READ-004 — DEVE** verificar `SHA-256(payload_bytes) == payload_hash` antes de aceitar um documento como íntegro.
5. **NDF-READ-005 — DEVE** verificar `validation_code` recalculando o digest conforme §4.6.2.
6. **NDF-READ-006 — DEVE**, quando `nivel_assinatura ∈ {"avancada", "qualificada"}`, validar a assinatura CAdES-B-LTA e os timestamps RFC 3161.
7. **NDF-READ-007 — NÃO DEVE** aceitar um documento assinado com certificado incompatível com o `nivel_assinatura` declarado.
8. **NDF-READ-008 — DEVE** considerar inválido um pacote onde assinatura original, timestamps ou material de validação obrigatórios estejam ausentes ou alterados.
9. **NDF-READ-009 — DEVE** rejeitar todos os casos de `conformance/ndf/invalid/`.
10. **NDF-READ-010 — DEVE** aceitar todos os casos de `conformance/ndf/valid/`.
11. **NDF-READ-011 — DEVE** rejeitar uma relação em `relacoes` sem `alvo.payload_hash`, ou com `alvo.payload_hash` em formato inválido, ou com `tipo` fora do vocabulário base fechado de §2.11.2 e fora do formato de extensão qualificada de §2.11.7.
12. **NDF-READ-012 — DEVE** rejeitar `proveniencia_ia` com `utilizada: false` e `intervencoes` não vazio.
13. **NDF-READ-013 — DEVE** rejeitar uma intervenção de `proveniencia_ia` com estado de revisão terminal (`revisto_e_aprovado`, `revisto_com_alteracoes` ou `rejeitado`) sem `revisor_ref` ou sem `revisto_em`.

### 9.3 Pacote conforme (`.ndfpkg`)

Um arquivo `.ndfpkg` é conforme se satisfizer todos os seguintes requisitos:

1. **NDF-PKG-001 — DEVE** ser um arquivo ZIP válido.
2. **NDF-PKG-002 — DEVE** conter `manifest.json`, `ndf-core.json` e `envelope.json` na raiz do arquivo.
3. **NDF-PKG-003** — `manifest.json` **DEVE** incluir inventário com `hash_sha256` de cada ficheiro e os campos obrigatórios definidos em §8.2.
4. **NDF-PKG-004** — `SHA-256(ndf-core.json)` **DEVE** coincidir com `manifest.inventario[ndf-core.json].hash_sha256`.
5. **NDF-PKG-005** — `ndf-core.json` **DEVE** ser um NDF-core conforme (§9.1).
6. **NDF-PKG-006** — O NDT referenciado por `ndt_version_ref` **DEVE** estar presente em `ndt/<schema_id>@<versao>.ndt.json`.

### 9.4 Suite de conformidade e test runner

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

### 9.5 Perfil de Ciclo de Vida NORMORDIS (opcional)

Este perfil **NÃO É** requisito de conformidade NDF (§9.1–§9.3). Cobre o
modelo de referência descrito em §2.4.1–§2.4.3 para sistemas que gerem NDF
depois da finalização. Um produtor ou leitor NDF conforme PODE optar por
não o implementar, adotando o seu próprio modelo de gestão de ciclo de
vida — ver ADR-010.

1. **CUST-REQ-001 — DEVE** registar cada transição de estado (§2.4.1) num log de auditoria imutável, validando cada entrada contra `custody-event.schema.json` e mantendo a cadeia de hash encadeado (§2.4.2).
2. **CUST-REQ-002 — DEVE** usar armazenamento append-only ou WORM para `payload_bytes`, envelope e log de custódia.
3. **CUST-REQ-003 — DEVE** aplicar o mecanismo de tombstone (§2.4.3) antes de destruir `payload_bytes` de um documento elegível para eliminação, preservando `validation_code` e `payload_hash`.

Ferramenta de referência: `tools/check_custody.py`; vetores em
`conformance/custody/`.

---

## Anexo A (informativo) — Glossário

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
| `nivel_assinatura` | Nível de assinatura eletrónica declarado pelo sistema produtor: `"nenhuma"`, `"avancada"` ou `"qualificada"` (ver §2.10) |
| CAdES-B-LTA | Nível de assinatura eletrónica avançada com timestamp de arquivo (ETSI EN 319 122) |
| `tipo_documento_ref` | Referência ao schema versionado que define a estrutura interna de `documento` (ex.: `oficio@1.0.0`, `modelo3-irs@2025.1`) — ver §2.9.2 |
