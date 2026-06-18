# Especificação NDF v1.0.0

**NORDOCS — NORMORDIS Document Format — Especificação Formal**

Estado: Draft para implementação
Âmbito: documentos gerados internamente pelo core-documental NORMORDIS e normalizados a NDF. Documentos importados/preservados bit-a-bit seguem um regime distinto, fora do âmbito desta especificação.

## Licenciamento

Esta especificação (texto, estrutura, JSON Schemas e exemplos associados) é disponibilizada sob **CC0 1.0** (domínio público). O objetivo é que qualquer produtor de software para a Administração Pública — open source ou proprietário — possa implementar leitura/escrita de NDF/NDT livremente, sem qualquer obrigação contratual ou de licenciamento para com o autor da especificação. Um formato de dados verdadeiramente aberto é o que permite à Administração Pública mudar de fornecedor sem perder acesso aos seus próprios dados — esse é o mecanismo real de soberania digital.

A **implementação de referência** (código-fonte: validadores, serializadores, bibliotecas Rust, `normordis-pdf`, etc.) é distribuída sob licença separada (EUPL v1.2), indicada no respetivo repositório (`LICENSE`). Esta especificação é licenciada separadamente (`LICENSE-SPEC`) precisamente para que a adoção do *formato* não dependa da licença do *código*.

---

## 1. Visão geral

### 1.1 Objetivo

O NDF (NORMORDIS Document Format) é o formato canónico de armazenamento de documentos no core-documental. Garante:

- **Integridade e validade jurídica** conforme eIDAS (Regulamento (UE) n.º 910/2014) e DL n.º 12/2021, com assinatura eletrónica qualificada de nível CAdES-B-LTA.
- **Eficiência de armazenamento**, por ser dados estruturados (tipicamente uma a duas ordens de grandeza menor que um binário renderizado equivalente).
- **Reprodutibilidade visual** em qualquer formato de apresentação (PDF, Word, ou formato futuro), através da combinação com o NDT (NORMORDIS Document Template — estrutura/layout).
- **Conformidade arquivística** conforme o Modelo de Requisitos para Sistemas de Gestão de Arquivos Eletrónicos (MEG) e os instrumentos de avaliação da DGLAB (Lista Consolidada / Tabelas de Seleção).

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

### 6.3 Implicação para `.ndfpkg` (exportação)

Cada NDF finalizado é autossuficiente e exportável individualmente (formato `.ndfpkg`, fora de âmbito desta especificação). A cadeia de proveniência de um processo documental é uma coleção de pacotes `.ndfpkg` independentes, ligados por referências leves (`versao_anterior`/`hash_anterior`), nunca por conteúdo embutido.

---

## 7. Versionamento da especificação NDF

### 7.1 `ndf_version`

Cada NDF-core declara a versão da especificação NDF a que adere (`ndf_version`, semver). Isto permite:

- Introduzir novos campos opcionais em versões minor (`1.x.0`) sem quebrar a leitura de NDFs antigos.
- Introduzir mudanças incompatíveis (remoção/renomeação de campos obrigatórios, mudança de semântica) apenas em versões major (`x.0.0`), exigindo lógica de leitura compatível com múltiplas versões major em paralelo, se NDFs de versões antigas continuarem em uso.

### 7.2 Compatibilidade retroativa

Um leitor de NDF deve:

- Recusar processar um NDF cuja `ndf_version` major seja superior à suportada pelo leitor (evolução futura desconhecida).
- Processar corretamente NDFs com `ndf_version` major igual e minor igual ou inferior à suportada (campos minor mais recentes podem estar ausentes — tratados como `null`/omissos conforme definido em cada versão minor).

---

## 8. Glossário

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
