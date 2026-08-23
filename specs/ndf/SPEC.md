# Especificação NDF v1.0.0

**NORMORDIS Document Format — Especificação Formal**

Estado: Draft — revisão pública por abrir
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

O modelo documental NDF distingue **três artefactos**, com funções e ciclos de
vida distintos:

| Artefacto | Função | Canonicalizado/assinado? |
|---|---|---|
| **NDF-core** | Fonte de verdade documental: conteúdo, metadados descritivos, classificação, avaliação arquivística e a referência ao NDT | Sim — é exatamente o que é canonicalizado (JCS) e assinado |
| **Envelope** | Provas criptográficas: assinaturas CAdES-B-LTA, timestamps RFC 3161, material de validação (cadeia de certificados + revogação) | Não — é produzido a partir da assinatura sobre o NDF-core; adicionado depois |
| **NDT** | Definição de apresentação, necessária à reprodução visual | Não — não integra os bytes assinados; é referenciado por `ndt_version_ref` |

Estes três artefactos combinam-se em duas unidades com nome próprio:

```
artefacto NDF assinado  = NDF-core + Envelope
pacote NDF (.ndfpkg)    = NDF-core + Envelope + NDT + schemas + recursos
```

O **artefacto NDF assinado** é a unidade mínima verificável: contém tudo o que
é necessário para provar integridade e autoria. O **pacote NDF** é a unidade
mínima autossuficiente: contém, além disso, tudo o que é necessário para
interpretar e reproduzir o documento sem depender de qualquer serviço externo
(§8).

O NDT não pertence aos bytes assinados, mas é indispensável à reprodução: sem
ele os dados continuam interpretáveis e verificáveis, e a apresentação não é
reconstituível. É por isso um artefacto do modelo, e não uma parte do
artefacto assinado.

A separação entre NDF-core e Envelope evita circularidade: o envelope fica fora
dos bytes sobre os quais a própria assinatura é calculada.

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

1. **Base legal de conservação prevalente**: documentos da Administração Pública são conservados com base em obrigação legal (Art.º 6.º, n.º 1, al. c) RGPD) e missão de interesse público (al. e)). O direito ao apagamento cede face a obrigações legais de conservação (Art.º 17.º, n.º 3, al. b) RGPD) — o prazo de conservação e o destino final (§3) resolvem esta decisão por tipo de documento.

2. **Pseudonimização pré-arquivo**: quando aplicável, é possível pseudonimizar dados pessoais antes da finalização. O NDF finalizado contém o pseudónimo; a tabela de correspondência é gerida fora do NDF com controlos de acesso próprios.

3. **Eliminação no termo do PCA**: documentos com `destino_final: eliminacao`
   são eliminados segundo a decisão e procedimento arquivístico aplicável. O
   mecanismo apoia a limitação da conservação, mas não demonstra por si só
   conformidade integral com o RGPD.

#### Campos de metadados obrigatórios relativos a proteção de dados

O bloco `metadados` DEVE declarar sempre `contem_dados_pessoais` e, **se e só se**
esse valor for `true`, o bloco `protecao_dados`:

```json
{
  "metadados": {
    "entidade_responsavel": "string (entidade que custodia o registo)",
    "contem_dados_pessoais": true,
    "protecao_dados": {
      "categorias": ["identificacao_fiscal", "rendimentos"],
      "base_legal_conservacao": { "regime": "eu-gdpr", "base": "art6-1-c" },
      "responsavel_tratamento": "string (identificador da entidade)"
    }
  }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `contem_dados_pessoais` | Sim | `true` \| `false` |
| `protecao_dados` | Condicional | Obrigatório se `contem_dados_pessoais: true`; **PROIBIDO** caso contrário. |
| `protecao_dados.categorias` | Sim, dentro do bloco | Pelo menos um valor. Enum aberto: `identificacao_fiscal`, `rendimentos`, `saude`, `dados_processuais`, `biometricos`, `outros`. |
| `protecao_dados.base_legal_conservacao` | Sim, dentro do bloco | Par `{regime, base}`, com `fundamento_ref` opcional. Ver §1.4.1. |
| `protecao_dados.responsavel_tratamento` | Sim, dentro do bloco | Identificador da entidade responsável pelo tratamento (RGPD, Art.º 13.º–14.º). |

#### 1.4.1 A base legal é declarada num regime, não escolhida de uma lista

`base_legal_conservacao` é um par `{regime, base}`, no mesmo padrão de
`classificacao_seguranca` (§2.7.4): o `regime` identifica o quadro de proteção
de dados aplicável e fornece o vocabulário; a `base` é o identificador da base
legal **dentro desse vocabulário**, tal como o produtor a determinou.

```json
{
  "base_legal_conservacao": {
    "regime": "eu-gdpr",
    "base": "art6-1-c",
    "fundamento_ref": "desp-int-2026-014"
  }
}
```

`fundamento_ref` é opcional e opaco ao NDF: refere o instrumento ou ato interno
que sustenta a declaração, e é resolvido pelo sistema produtor.

**Esta especificação NÃO ENUMERA as bases legais de nenhum regime.** Uma lista
fechada teria dois defeitos, e o NDF teve os dois: ficaria presa a um
ordenamento — o RGPD — num formato que se quer neutro quanto à jurisdição
(ADR-017); e ficaria incompleta mesmo nesse ordenamento, por omitir bases
efetivamente previstas. Um documento cuja conservação assentasse numa base não
listada não tinha como a declarar, o que é lacuna do formato nos termos de
ADR-022.

Um leitor conforme **NÃO DEVE** interpretar `base` sem conhecer o `regime`, nem
inferir um regime do silêncio ou do contexto. Se a base declarada é a correta, e
se o tratamento que ela fundamenta é lícito, são questões de direito, decididas
por quem tem competência para as decidir — o NDF regista a declaração e
preserva-a intacta (§1.4, ADR-022).

**Responsável pelo tratamento e custódia do registo são conceitos distintos.**
A responsabilidade pelo tratamento na aceção do RGPD só existe quando há dados
pessoais e vive dentro de `protecao_dados`. A responsabilidade pela custódia do
registo existe em qualquer documento e declara-se em
`metadados.entidade_responsavel` (§2.7.2), que é obrigatório sempre. As duas
entidades coincidem com frequência, mas não têm de coincidir. Ver ADR-016.

`contem_dados_pessoais` mantém-se obrigatório mesmo quando é `false`: num
documento imutável e assinado, a declaração explícita de ausência de dados
pessoais é uma afirmação com valor probatório, distinta da simples omissão de
informação sobre o assunto.

### 1.5 Confidencialidade e controlo de acesso

O NDF admite documentos com diferentes níveis de sensibilidade, declarados
em `metadados.classificacao_seguranca` (§2.7.4) — um par `{perfil, nivel}`, em
que `perfil` identifica o regime de classificação aplicável e `nivel` é uma
escala abstrata de `"publico"` a `"muito_secreto"`. Este campo é descritivo:
sinaliza o nível de sensibilidade do conteúdo. O NDF NÃO DEVE ser apresentado, nem
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
| `avaliacao` | Sim | Avaliação arquivística — prazo de conservação e destino final, sob o perfil declarado. Ver §3. |
| `relacoes` | Não | Relações verificáveis com outros documentos NDF. Ver §2.11. |
| `participantes` | Não | Pessoas singulares que intervieram na produção, distintas de quem assina. Ver §2.12. |
| `proveniencia_ia` | Não | Evidência de utilização de sistemas de IA na produção ou revisão do documento. Ver §2.13. |
| `proveniencia_sistema` | Não | Sistema ou cadeia de sistemas determinísticos que produziu o conteúdo. Ver §2.14. |
| `imputacao` | Não | Quem responde juridicamente pelo documento, e a que título. Ver §2.15. |

Nenhum dos campos obrigatórios PODE estar ausente — a finalização **DEVE falhar** se algum estiver em falta (ver §5). Os cinco campos opcionais, quando presentes, entram no NDF-core canonicalizado e assinado tal como os restantes.

#### 2.2.1 Invariante de origem

Os campos opcionais são individualmente opcionais, mas não o são em conjunto.
Todo o NDF **DEVE** declarar pelo menos uma **origem identificável do
conteúdo**, de um dos três modos seguintes:

| Modo | Como se declara |
|---|---|
| Humana | `participantes` contém pelo menos uma entrada com `papel` em `autor`, `coautor` ou `decisor` |
| De sistema | `proveniencia_sistema` presente e não vazio |
| De IA | `proveniencia_ia.utilizada` é `true` |
| **Não apurável** | `metadados.origem_nao_identificavel` presente, com `fundamento` (§2.7.6) |

Um NDF que não declare nenhuma destas origens **DEVE** ser rejeitado
(ver §9.1 e §9.2). A regra é verificável apenas por estrutura,
sem inferência sobre o conteúdo: é expressa no JSON Schema por `anyOf`, pelo
que qualquer validador Draft 2020-12 a aplica sem código adicional.

Papéis como `revisor_humano` ou `responsavel_tecnico` **não** satisfazem o
invariante: rever ou responder tecnicamente por um conteúdo não é o mesmo que
produzi-lo. Um documento revisto por uma pessoa continua a ter de declarar
quem — ou o quê — o produziu.

O invariante não obriga a inventar informação. Um documento produzido por um
sistema sem qualquer intervenção humana declara `proveniencia_sistema` e
nada mais; nenhum autor humano tem de ser fabricado para satisfazer a regra
(ver §2.15.5, caso da declaração automática convertida).

O quarto modo existe pela mesma razão. Há documentos que entram em custódia sem
que a sua origem seja apurável — um documento em papel digitalizado sem menção
de autor, uma denúncia anónima, um ficheiro recebido de sistema de terceiro sem
identificação. Antes de a captura existir (§2.8.1), o caso não se colocava:
todo o NDF nascia no sistema produtor e a origem era sempre conhecida. Recusar
estes documentos ou fabricar-lhes um autor são as duas alternativas, e ambas
são piores do que declarar, com fundamento, que a origem não é apurável. Ver
§2.7.6 e [ADR-023](../../docs/architecture/ADR-023-origem-nao-apuravel.md).

### 2.3 `ndf_id`

Identificador permanente do documento no ecossistema NORMORDIS.

- **Tipo**: string, formato UUID v4 (RFC 9562) — ex.: `"a1b2c3d4-e5f6-4789-abcd-ef0123456789"`.
- **Geração**: pelo sistema produtor imediatamente antes da canonicalização, nunca depois.
- **Imutabilidade**: faz parte do NDF-core canonicalizado e assinado — NÃO DEVE ser alterado após finalização.
- **Unicidade**: o sistema produtor DEVE garantir que não existem dois NDF com o mesmo `ndf_id`.
- **Uso**: referência primária em `relacoes[].alvo.ndf_id` (§2.11), no `manifest.json` do `.ndfpkg` (§8.2), e como chave primária no armazenamento físico.

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

**Porque é que um campo com um único valor admissível não é redundante.** Num
documento imutável e assinado, afirmar explicitamente um facto não é
equivalente a omiti-lo: a ausência de `estado` seria indistinguível de um
produtor que não sabe, não verificou, ou não considerou a questão. Com o campo
presente, os bytes assinados contêm uma **declaração** de que estes são um
documento finalizado e ativo, oponível a terceiros como qualquer outro campo
assinado. É o mesmo raciocínio já aceite para `proveniencia_ia.utilizada:
false` (§2.13.2, ADR-005) e para `contem_dados_pessoais: false` (§1.4,
ADR-016) — em ambos os casos o valor por omissão é declarado, e não inferido
do silêncio. O `enum` de um só valor é ainda o que torna detetável, e não
silenciosa, qualquer futura admissão de outros valores.

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
| `"eliminado"` | DF aplicado: eliminação. `payload_bytes` e envelope destruídos; subsiste um evento terminal no log de custódia (ver §2.4.3). |

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

**Estrutura de cada entrada do log de auditoria** (conforme
`custody-event.schema.json` — este exemplo valida contra o schema):

```json
{
  "custody_event_version": "1.0.0",
  "event_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "ndf_id": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
  "sequence": 3,
  "event_type": "estado_alterado",
  "occurred_at": "2031-06-18T10:30:00Z",
  "actor": {
    "type": "sistema",
    "id": "sistema-gca-v2.1",
    "display_name": "Sistema de Gestão de Custódia"
  },
  "details": {
    "estado_anterior": "ativo",
    "estado_novo": "em_conservacao",
    "motivo": "PCA de 5 anos decorrido desde 2026-06-18",
    "instrumento_legal": "lc/lista-consolidada-dglab-2023-v3"
  },
  "previous_event_hash": "sha256:9f2c1a7b3d4e5f60718293a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4",
  "event_hash": "sha256:3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b"
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `custody_event_version` | Sim | Versão do schema de evento. Valor normativo: `"1.0.0"`. |
| `event_id` | Sim | Identificador único do evento (UUID v4). |
| `ndf_id` | Sim | Identificador do NDF a que o evento respeita. |
| `sequence` | Sim | Posição na cadeia; `0` no primeiro evento, incrementa exatamente uma unidade. |
| `event_type` | Sim | Enum fechado: `capturado`, `recebido`, `finalizado`, `verificado`, `exportado`, `estado_alterado`, `assinatura_renovada`, `selo_acrescentado`, `transferido`, `eliminado`. |
| `occurred_at` | Sim | Data/hora do evento (ISO 8601, UTC). |
| `actor` | Sim | Quem originou o evento: `type` (`sistema` \| `utilizador` \| `entidade`), `id`, e `display_name` opcional. |
| `details` | Não | Objeto livre para a semântica específica do tipo de evento. Para `estado_alterado`, RECOMENDA-SE `estado_anterior`, `estado_novo`, `motivo` e `instrumento_legal`. Para `capturado`, RECOMENDA-SE `componentes` (lista de digests), `canal` e `recebido_em`. Para `verificado` sobre componentes, RECOMENDA-SE `componentes_verificados`. Para `recebido`, RECOMENDA-SE `transferencia_ref`, `transmitente` e a referência ao documento de aceitação. |
| `previous_event_hash` | Sim | `event_hash` do evento anterior; `null` no primeiro. |
| `event_hash` | Sim | `SHA-256(JCS(evento sem a propriedade event_hash))`. |

**Evento `capturado`**: um documento cujo conteúdo resida em componentes
binários (§2.8.1) entra em custódia quando os bytes entram, o que antecede a
finalização do NDF. O evento `capturado` regista esse momento — canal, instante
e digests dos componentes recebidos — e é tipicamente o evento de `sequence` 0
da cadeia, seguido de `finalizado`. Um documento cujo conteúdo seja estruturado
não tem evento de captura.

**Evento `recebido`**: um documento que entra em custódia **vindo de outra
entidade** não é capturado nem finalizado por quem o recebe — já existe, com
identidade, assinatura e história próprias. `recebido` regista esse momento e é
o evento de `sequence` 0 da cadeia do custodiante recetor. Um recetor **NÃO
DEVE** registar `capturado` para um documento que recebeu: seria declarar uma
produção que não ocorreu, do mesmo modo que declarar como autor quem apenas
submeteu (§2.8.1.1).

**As cadeias de custódia são por custodiante, não globais.** Decorre do anterior
e vale a pena ser explícito, porque um implementador que assuma o contrário
desenha algo que não funciona. Cada custodiante mantém a **sua** cadeia para um
dado `ndf_id`: a do recetor começa em `sequence` 0 com `previous_event_hash`
`null`, e **não** continua a cadeia do transmitente. Não há, nem poderia haver,
continuidade de hash entre custodiantes: o recetor não detém os eventos do
transmitente, e encadeá-los sem os deter exigiria falsificá-los.

O que liga as duas cadeias não é criptográfico, é documental: a evidência de
custódia transferida pelo transmitente, e o documento de aceitação produzido pelo
recetor. Um verificador que queira a história completa de um documento reúne as
cadeias dos vários custodiantes por esses artefactos. Um leitor que tenha apenas
uma cadeia tem a história **desse** custodiante, e **NÃO DEVE** apresentá-la como
sendo a história do documento. Ver
[`../../docs/design/NDF-CONJUNTO-DE-TRANSFERENCIA.md`](../../docs/design/NDF-CONJUNTO-DE-TRANSFERENCIA.md).

A verificação periódica de fixidez dos componentes regista-se como `verificado`,
com os digests em `details.componentes_verificados`. Um objeto sem histórico de
verificações tem **uma** verificação, não uma história de verificações — e é a
história que sustenta a alegação de preservação (ver
[`PREMIS-METS-MAPPING.md`](../../docs/interoperability/PREMIS-METS-MAPPING.md) §4).

**Autorização**: um sistema que implemente este perfil DEVE registar, no
evento de eliminação, a identidade de quem autorizou formalmente a operação
e o instrumento de avaliação que a suporta (ver §2.4.3). Quem tem
competência para conceder essa autorização é matéria de política
arquivística e organizacional da entidade, fora do âmbito desta
especificação.

#### 2.4.3 Evento terminal de eliminação

Quando `estado` transita para `"eliminado"`, um sistema que implemente este
perfil DEVE:

1. Destruir `payload_bytes` e todos os campos do envelope excepto `validation_code` e `payload_hash`.
2. Destruir **todos os componentes binários** declarados em `documento`
   (§2.8.1). Um documento cujo conteúdo resida em componentes não fica
   eliminado pela destruição do NDF-core: o conteúdo do ato continuaria a
   existir nos ficheiros preservados. A eliminação é uma operação única e
   indivisível sobre o documento inteiro.
3. Registar um **evento terminal** no log de custódia (§2.4.2), com
   `event_type: "eliminado"`, conservando em `details` a evidência mínima
   necessária para rastreabilidade posterior — incluindo os digests dos
   componentes destruídos, que subsistem como prova de que existiram e do que
   eram, sem que os bytes subsistam.

Não existe um artefacto normativo separado para este efeito: o evento de
custódia já definido em `custody-event.schema.json` é a estrutura usada,
evitando um segundo schema a versionar, testar e manter sincronizado.

```json
{
  "custody_event_version": "1.0.0",
  "event_id": "0b5ed7e9-1c2d-4e3f-a4b5-c6d7e8f90a1b",
  "ndf_id": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
  "sequence": 7,
  "event_type": "eliminado",
  "occurred_at": "2031-06-18T10:30:00Z",
  "actor": { "type": "utilizador", "id": "user:456" },
  "details": {
    "payload_hash": "sha256:3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b",
    "validation_code": "NDF-A3F7K2MXPQR9ZTNW8VJ",
    "motivo_eliminacao": "Destino final: eliminação. PCA de 5 anos decorrido.",
    "instrumento_ref": "lc/lista-consolidada-dglab-2023-v3",
    "classificacao_ref": "lc/450.10.001",
    "autorizado_por": "user:123",
    "componentes_destruidos": [
      { "id": "principal", "sha256": "sha256:9741495bbc5aa8f2575339e28eb60663d1c480cfa3d4df41f20cb486cd88a053" }
    ]
  },
  "previous_event_hash": "sha256:9f2c1a7b3d4e5f60718293a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4",
  "event_hash": "sha256:5c1e2f3a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f9a0b1c2d3e4f5a"
}
```

O evento garante rastreabilidade sem preservar os dados eliminados:
`validation_code` e `payload_hash` conservados em `details` permitem
confirmar que o documento existiu e foi destruído de forma autorizada, sem
reconstituir o seu conteúdo. Os digests dos componentes destruídos têm a mesma
função e a mesma propriedade: provam o que existiu, sem que os bytes subsistam
nem sejam reconstituíveis a partir do digest.

#### 2.4.4 Evidência transferível e auditoria interna

O log de custódia serve dois fins que não coincidem. Uma parte é **evidência do
documento** — quando foi capturado, quando foi finalizado, que selagens
recebeu, que verificações de fixidez passou, para quem foi transferido. Essa
parte pertence ao documento e acompanha-o quando a custódia muda de mãos: sem
ela, a entidade recetora recebe bytes íntegros sem história, e a alegação de
preservação fica por sustentar. A outra parte é **operação do custodiante** —
quem extraiu cópias e quando — e não pertence a quem recebe o documento.

Classificação por tipo de evento:

| Evento | Classe |
|---|---|
| `capturado`, `finalizado`, `estado_alterado`, `assinatura_renovada`, `selo_acrescentado`, `verificado`, `transferido`, `eliminado` | **evidência transferível** |
| `exportado` | auditoria interna do custodiante |

`verificado` é deliberadamente transferível: é o histórico de fixidez que
sustenta a alegação de preservação ao longo do tempo, e omiti-lo esvaziaria a
transferência daquilo que a torna útil.

**A omissão é detetável, e é essa a garantia.** Cada evento transporta
`sequence` e `previous_event_hash`. Uma cadeia transferida de que se tenham
retirado eventos apresenta saltos de `sequence` e uma ligação de hash que não
fecha. A entidade recetora sabe sempre **que** algo foi retido, ainda que não
saiba o quê — e isso basta para não confundir uma história parcial com uma
história completa.

Daqui decorre `CUST-REQ-004`: os eventos transferem-se íntegros e não editados,
e a cadeia **NÃO DEVE** ser renumerada ou recomposta para dissimular omissões.
Uma cadeia recomposta é indistinguível de uma cadeia completa, e destrói
precisamente a propriedade que torna a transferência parcial honesta.

**Por definir.** Esta versão classifica a evidência e fixa a regra de
integridade, mas **não define o veículo**: o `.ndfpkg` (§8) é a unidade de um
documento e não transporta o log de custódia. Como um conjunto de documentos e
a respetiva evidência se transferem para outra entidade, ou se depositam num
arquivo conforme OAIS, é matéria de contrato próprio, ainda por especificar —
ver a cláusula sobre transferência entre entidades em
[`docs/design/NDFPKG-CAPTURA-E-INGESTAO.md`](../../docs/design/NDFPKG-CAPTURA-E-INGESTAO.md).

### 2.5 Algoritmo de hash (`payload_hash_alg`)

O campo `payload_hash_alg` declara o algoritmo usado para calcular o digest sobre o qual recai a assinatura CAdES.

**Valor normativo para NDF 1.0.0**: `"sha256"` — SHA-256 conforme NIST FIPS 180-4. Este é o único valor válido nesta versão da especificação.

Justificação: SHA-256 é amplamente suportado pelos perfis e bibliotecas CAdES
e TSP relevantes. A conformidade jurídica e criptográfica depende também da
política de algoritmos aplicável no instante de assinatura; nem o eIDAS nem o
RFC 3161 fixam SHA-256 como único algoritmo para sempre.

A introdução de outros algoritmos, isoladamente ou em paralelo, **exige uma
versão futura desta especificação**. O `enum` fechado de `payload_hash_alg` é o
mecanismo que torna essa transição explícita e detetável, em vez de silenciosa.
Esta especificação não fixa em que versão isso acontecerá: compromissos de
versão pertencem ao roadmap informativo, não ao texto normativo.

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
      "identificadores": [
        { "sistema": "pt-nif", "valor": "123456789" },
        { "sistema": "pt-dglab", "valor": "PT-DGE-000" }
      ]
    },
    "entidade_responsavel": "Direção-Geral de Exemplo",
    "assunto": "Resposta ao ofício n.º 123/2026",
    "numero_referencia": "OF/2026/00123",
    "processo_ref": "proc.º 456/2026",
    "idioma": "pt-PT",
    "classificacao_seguranca": { "perfil": "pt", "nivel": "uso_interno" },
    "contem_dados_pessoais": false
  }
}
```

Com dados pessoais, o mesmo bloco acresce `protecao_dados` (§1.4):

```json
{
  "metadados": {
    "contem_dados_pessoais": true,
    "protecao_dados": {
      "categorias": ["identificacao_fiscal", "dados_processuais"],
      "base_legal_conservacao": { "regime": "eu-gdpr", "base": "art6-1-c" },
      "responsavel_tratamento": "Direção-Geral de Exemplo"
    }
  }
}
```

#### 2.7.2 Tabela de campos

| Campo | Obrigatório | Tipo | Descrição |
|---|---|---|---|
| `tipo_documento_ref` | Sim | string | Referência versionada ao schema do tipo de documento. Formato canónico `"<id>@<versao>"` ou extensão qualificada `"ext.<entidade>.<tipo>@<versao>"`. Define a estrutura de `documento`. Ver §2.9.2, §2.9.5 e `specs/registry/`. |
| `entidade_produtora` | Sim | objeto | Entidade responsável pela produção do documento. Ver §2.7.3. |
| `entidade_responsavel` | Sim | string | Designação da entidade responsável pela **custódia do registo**. Obrigatório em qualquer documento, com ou sem dados pessoais. NÃO DEVE ser confundido com `protecao_dados.responsavel_tratamento` (§1.4), que é o responsável pelo tratamento na aceção do RGPD e só existe quando há dados pessoais. Ver ADR-016. |
| `assunto` | Recomendado | string | Título ou descrição breve do documento — indexável para pesquisa e arquivo. |
| `numero_referencia` | Recomendado | string | Número de referência documental (ex.: `"OF/2026/00123"`). |
| `processo_ref` | Opcional | string | Referência ao processo ou procedimento a que o documento pertence. |
| `idioma` | Opcional | string | Idioma principal do documento, no subconjunto `língua[-escrita][-região]` das etiquetas BCP 47 (RFC 5646) — ex.: `"pt-PT"`, `"en-GB"`, `"zh-Hant"`. **Não** é a gramática BCP 47 completa: extlang, variants, extensions, private-use e grandfathered tags não são admitidos, por não terem uso documental estabelecido e por não serem exprimíveis de forma fiável em JSON Schema. Quando omitido, assume-se `"pt"`. |
| `idiomas_autenticos` | Não | array | Línguas em que o texto é **igualmente autêntico**. Só para documentos cujas versões têm a mesma força jurídica. Ver §2.7.7. |
| `classificacao_seguranca` | Recomendado | objeto | Classificação de segurança da informação, com o regime aplicável e o nível ordinal. Ver §2.7.4. A omissão significa **não declarada** — ver §2.7.4.2. |
| `contem_dados_pessoais` | Sim | boolean | `true` se o documento contiver dados pessoais na acepção do RGPD. |
| `protecao_dados` | Condicional | objeto | Obrigatório se `contem_dados_pessoais: true`; **PROIBIDO** caso contrário. Agrupa `categorias`, `base_legal_conservacao` e `responsavel_tratamento`. Ver §1.4. |

#### 2.7.3 `entidade_produtora`

| Campo | Obrigatório | Descrição |
|---|---|---|
| `designacao` | Sim | Designação oficial da entidade (ex.: `"Autoridade Tributária e Aduaneira"`). |
| `identificadores` | Recomendado | Array de identificadores institucionais, cada um qualificado pelo esquema a que pertence. Ver abaixo. |

```json
{
  "entidade_produtora": {
    "designacao": "Autoridade Tributária e Aduaneira",
    "identificadores": [
      { "sistema": "pt-nif", "valor": "600037398" },
      { "sistema": "pt-dglab", "valor": "PT-AT-000" }
    ]
  }
}
```

`sistema` é um **identificador opaco qualificado** de dois ou mais segmentos,
pela mesma razão de `avaliacao.perfil` (§3.2.3): o significado vem do esquema
referenciado, não da forma da string. Exemplos: `pt-nif`, `pt-dglab`,
`fr-siren`, `nl-kvk`, `eu-vat`, `eu-pic`.

A validade do `valor` face às regras do esquema — número de dígitos, dígito de
controlo, formato — é responsabilidade do esquema e do sistema produtor, não
desta especificação. Impor no NDF-core a sintaxe de um identificador nacional
tornaria o formato dependente de regras que mudam por decisão de uma
jurisdição, e que o NDF não tem competência para arbitrar.

`entidade_produtora` identifica a **pessoa coletiva** para efeitos
arquivísticos — o organismo cuja produção documental é objeto de avaliação e
conservação (§3). NÃO DEVE ser confundida com `imputacao` (§2.15), que
identifica o **órgão ou a pessoa que responde juridicamente** pelo documento,
nem com `proveniencia_sistema` (§2.14), que identifica o sistema que produziu
o conteúdo. Os três coexistem e são independentes: uma liquidação automática
tem `entidade_produtora` "Autoridade Tributária e Aduaneira",
`imputacao[].imputado` o órgão concreto com competência para o ato, e
`proveniencia_sistema[].sistema` o motor de liquidação.

#### 2.7.6 `origem_nao_identificavel`

Bloco opcional que declara que a origem do conteúdo **não pôde ser apurada**. É
o quarto modo do invariante de origem (§2.2.1).

```json
{
  "metadados": {
    "origem_nao_identificavel": {
      "fundamento": "Documento em papel digitalizado, sem menção de autor nem de serviço emissor."
    }
  }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `fundamento` | Sim | Razão pela qual a origem não é apurável. |

`fundamento` é obrigatório e não tem valor por omissão. Sem ele, o bloco seria
uma via de fuga ao invariante — bastaria declará-lo vazio para dispensar
qualquer origem. Com ele, é uma afirmação que alguém assume, que entra nos
`payload_bytes` e que a assinatura cobre.

O bloco **NÃO DEVE** coexistir com uma declaração que identifique a origem:
`participantes` com `papel` em `autor`, `coautor` ou `decisor`, ou
`proveniencia_sistema` não vazio. Declarar autor e origem não apurável ao mesmo
tempo é contradição, e o schema rejeita-a.

**Pode** coexistir com `proveniencia_ia`: a intervenção de um sistema de IA num
documento capturado é tipicamente assistência — classificação, extração,
sumarização — e não produção do conteúdo. Nesse caso a origem do conteúdo
continua por apurar, e as duas declarações são simultaneamente verdadeiras.

Este bloco descreve o que **não** se sabe. Não substitui
`metadados.entidade_produtora`, que continua obrigatório e identifica a entidade
a que o documento é atribuído para efeitos arquivísticos, nem
`entidade_responsavel`, que identifica quem o custodia (§2.7.2, §2.7.3, ADR-016).
Ter entidade produtora conhecida e autor não apurável é situação corrente, não contradição.

#### 2.7.4 `classificacao_seguranca`

```json
{
  "classificacao_seguranca": { "perfil": "pt", "nivel": "reservado" }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `perfil` | Sim | Regime de classificação de segurança cujas etiquetas legais correspondem a `nivel`. Enum aberto — ex.: `"pt"`, `"eu"`, `"nato"`. |
| `nivel` | Sim | Nível ordinal neutro de sensibilidade. Enum fechado. |

**Enum fechado de `nivel`** — escala ordinal, do menos para o mais restrito:

| Valor | Descrição |
|---|---|
| `"publico"` | Informação de acesso livre — sem restrições. DEVE ser atribuída explicitamente; NÃO DEVE ser assumida por omissão. |
| `"uso_interno"` | Circulação interna à entidade; não destinada ao exterior. |
| `"reservado"` | Divulgação restrita a destinatários identificados. |
| `"confidencial"` | Acesso controlado com registo de acessos. |
| `"secreto"` | Regime de gestão documental especial. |
| `"muito_secreto"` | Nível mais elevado — requer infraestrutura de segurança dedicada. |

#### 2.7.4.1 Porque o nível fica no core e o regime no perfil

A classificação de segurança não é universalmente representável por um único
vocabulário: o regime português do DL n.º 11/2023, o regime da União Europeia
(`RESTREINT UE`, `CONFIDENTIEL UE`, `SECRET UE`, `TRÈS SECRET UE`) e os regimes
NATO e de cada Estado-membro divergem em etiquetas, número de níveis e regras
de manuseamento.

Aplica-se aqui a mesma solução de `avaliacao` (§3.2.4): **o vocabulário legal é
do perfil, a estrutura fica no core**. A estrutura, neste caso, é a escala
ordinal — o que permite a um leitor que desconheça o regime declarado ordenar
documentos pelo **nível abstrato que os respetivos produtores declararam**.

O alcance dessa ordenação DEVE ser lido com precisão. Ordenar `nivel` **não**
constitui comparação objetiva entre regimes de classificação soberanos, e não
autoriza concluir que um documento é juridicamente mais protegido do que outro:
`{"perfil": "eu", "nivel": "reservado"}` e `{"perfil": "pt", "nivel":
"reservado"}` declaram o mesmo nível abstrato, não uma equivalência entre
`RESTREINT UE` e o regime português. O que a escala suporta é triagem e
priorização operacional dentro de um acervo; não substitui a leitura do regime
declarado.

Mapear `nivel` para a etiqueta legal do regime — e para as obrigações de
manuseamento que dela decorrem — é matéria do perfil e do sistema custodiante.
O mapeamento é declarado pelo produtor e **não é verificado por esta
especificação**: o NDF regista qual o regime e qual o nível, não arbitra se a
correspondência entre ambos está juridicamente correta.

Reforça-se o que §1.5 já estabelece: este campo é um **sinal descritivo** para
o sistema de custódia, nunca um mecanismo de controlo de acesso.

#### 2.7.4.2 Ausência de `classificacao_seguranca`

`classificacao_seguranca` é opcional. A sua **ausência significa que a
classificação não foi declarada** — não um nível por omissão.

Versões anteriores desta especificação fixavam `"uso_interno"` como valor
assumido quando o campo era omitido. Essa regra deixou de ser exprimível quando
o campo passou a objeto `{perfil, nivel}` (ADR-017): não é possível inferir um
**regime** a partir do silêncio, e um nível sem regime não tem significado
determinado. Uma regra que só se aplica a metade do campo é pior do que nenhuma.

A regra é, por isso, retirada. Um sistema custodiante que aplique um nível
conservador por omissão está a exercer **política própria de custódia**, o que é
legítimo e expressamente previsto por §1.5 — mas essa decisão não é uma leitura
do NDF nem é oponível como declaração do produtor. Um leitor conforme NÃO DEVE
representar um nível não declarado como se tivesse sido declarado.

**RECOMENDA-SE** declarar sempre o campo. Um produtor que conheça a
sensibilidade do documento e a omita perde a única oportunidade de a fixar
dentro dos bytes assinados.

#### 2.7.7 Documentos multilingues (`idiomas_autenticos`)

`idioma` declara **uma** língua, descrita como principal. Para a generalidade dos
documentos isso basta e é verdadeiro. Não basta para o documento cujas versões
linguísticas têm a **mesma força jurídica** — legislação da União Europeia,
tratados, atos de Estados plurilingues —, onde dizer que uma das línguas é a
principal é afirmar uma hierarquia que o regime aplicável não estabelece.

O bloco opcional `idiomas_autenticos` exprime esse caso:

```json
{
  "metadados": {
    "idioma": "pt-PT",
    "idiomas_autenticos": ["pt-PT", "en-GB"]
  }
}
```

`idiomas_autenticos` **DEVE** conter o valor de `idioma`. Quando o bloco está
presente, `idioma` deixa de significar «a língua principal» e passa a identificar
apenas **a versão que este NDF apresenta em primeiro lugar** — o que é facto sobre
esta materialização, não sobre a hierarquia entre as versões.

**Uma tradução que não seja igualmente autêntica NÃO DEVE ser declarada aqui.** É
outro documento, com a sua própria identidade e o seu próprio autor, ligado por
`relacoes[]` (§2.11) — do mesmo modo que um anexo com identidade documental
própria não é um componente (§2.8.1.3). Declará-la em `idiomas_autenticos`
afirmaria uma autenticidade que o produtor não tem, e é a mesma família de erro
que declarar como autor quem apenas submeteu (§2.8.1.1).

**A ausência do bloco significa que a questão não se coloca**, e não que o
documento seja monolingue em direito — o mesmo critério de §2.7.4.2 para a
classificação de segurança. Um leitor **NÃO DEVE** inferir do silêncio que existe
uma única versão autêntica.

**Onde vivem os textos.** Esta especificação declara o **facto** de haver mais do
que uma versão autêntica; não determina se os vários textos vivem em `documento`,
em componentes distintos ou em NDF relacionados. Essa é decisão do schema do tipo
e do produtor, pela regra geral de §2.9.6.

### 2.8 Tipos de conteúdo permitidos

Os valores dentro de `documento` e `metadados` seguem as regras gerais do JCS/JSON: strings (UTF-8), números, booleanos, `null`, objetos e arrays. Não são permitidos:

- Tipos binários embutidos diretamente — nem base64, nem data URL, nem qualquer outra codificação de bytes opacos dentro de `documento` ou `metadados`.
- Valores `NaN`, `Infinity`, `-Infinity` (não representáveis em JSON estrito).
- Chaves duplicadas no mesmo objeto (proibido por JCS).

#### 2.8.1 Componentes binários referenciados por hash

A proibição anterior recai sobre **bytes embutidos**, não sobre a referência a
eles. Um schema de tipo documental (§2.9) **PODE** declarar componentes binários
por digest — identidade, papel, tipo MIME, dimensão e hash — mantendo os bytes
fora do NDF-core.

Isto é o que permite representar em NDF um documento cujo conteúdo não nasceu no
editor estruturado: emitido noutra ferramenta e preservado, ou recebido do
exterior. O tipo canónico para esse caso é `documento-capturado@<versao>`
(`specs/registry/`); a decisão e o seu alcance constam de
[ADR-020](../../docs/architecture/ADR-020-um-formato-duas-realidades.md).

**A faculdade não é exclusiva desse tipo.** `componentes` é o mecanismo **único**
de componentes binários no NDF, e qualquer schema de tipo **PODE** declará-lo —
um documento nativo com anexos usa-o exatamente como um documento capturado usa
para o seu original (§2.8.1.3). Um schema de tipo **NÃO DEVE** definir vocabulário
próprio para o mesmo fim: dois vocabulários para binários significam duas regras
de fecho de pacote, e apenas uma delas está verificada.

Um componente declarado por hash fica dentro dos `payload_bytes` e, portanto,
coberto pela canonicalização e pela assinatura — é essa a razão de a declaração
viver em `documento` e não no manifesto do pacote, que não é assinado
([ADR-021](../../docs/architecture/ADR-021-componentes-nos-bytes-assinados.md),
§8.3).

Uma declaração de componente **NÃO DEVE** conter localização de armazenamento —
URI, *bucket*, caminho dentro do pacote ou nome de adaptador. O digest é a
identidade do componente e a chave da sua resolução; um leitor **NÃO DEVE**
resolver um componente pelo seu nome de origem, que é descritivo. Num `.ndfpkg`,
a correspondência faz-se com `manifest.inventario` (§8.1, `NDF-PKG-009`).

O invariante de origem de §2.2.1 aplica-se sem excepção a estes documentos. A
origem do conteúdo é quem produziu o componente, e declara-se do modo normal:
`participantes` com `papel: "autor"` para um documento produzido por pessoa —
incluindo pessoa exterior à entidade, cujo `participante_ref` é opaco e
resolvido fora do NDF (§2.12.4) —, ou `proveniencia_sistema` quando o
componente tiver sido produzido por um sistema. A captura não dispensa declarar
quem ou o que produziu o documento; apenas desloca o objeto dessa produção do
texto para o componente.

#### 2.8.1.1 Submeter não é produzir

Um sistema de captura observa tipicamente **a entrada**, não a produção. Quem
submeteu um ficheiro, por que canal e com que autenticação é facto declarável em
`proveniencia_submissao`; quem escreveu o conteúdo é outro facto, que a
submissão não estabelece. Um contabilista apresenta documento do cliente; um
mandatário submete peça assinada pelo representado; um funcionário carrega
documento produzido por terceiro.

Um produtor **NÃO DEVE** declarar o submissor como `autor`, `coautor` ou
`decisor` apenas por ele ter submetido o documento. A declaração de autoria
exige que o produtor a estabeleça — pelo conteúdo do próprio componente, por
assinatura contida, por procedimento, ou por outro fundamento que assuma. Não
havendo esse fundamento, a origem não é apurável, e declara-se pelo quarto modo
de §2.2.1 (`metadados.origem_nao_identificavel`, ADR-023) sem que isso apague o
que se sabe sobre a submissão: os dois blocos são independentes e coexistem.

Quando o que releva é a responsabilidade jurídica e não a autoria material, o
bloco próprio é `imputacao` (§2.15), que regista o título invocado e o facto de
autenticação que o fundamenta. É o eixo do direito, distinto por desenho do eixo
dos factos (§2.15.1) — e é frequentemente o único dos dois que uma captura
autoriza a preencher. Ver o exemplo em
`specs/ndf/examples/captura-requerimento/`.

#### 2.8.1.2 Função do NDT num documento capturado

`ndt_version_ref` é obrigatório em todo o NDF (§2.6), mas o que ele designa num
documento capturado **não** é o que designa num documento nativo, e a diferença
é normativa.

| | Documento nativo | Documento capturado |
|---|---|---|
| Reproduz o documento | o NDT, a partir de `documento` | o **componente**, tal como preservado |
| O NDT reproduz | o ato | o **auto de captura** e os seus metadados |

Num documento capturado, `ndt_version_ref` designa a representação documental da
**captura** — identidade, componentes, proveniência da submissão, validações de
formato, avaliação. **NÃO DEVE** ser interpretado como template capaz de
reconstruir o componente original: o componente é o original, e nada o
substitui (§2.8.2). Um leitor conforme **NÃO DEVE** aplicar o NDT ao bloco
`documento` de um capturado esperando obter o ato, e **NÃO DEVE** apresentar a
saída do NDT como sendo o documento recebido.

#### 2.8.2 Divergência entre declaração e componente

Num documento cujo conteúdo resida em componentes, os campos descritivos de
`documento` e o conteúdo do componente são **asserções independentes**: nada
impede que divirjam, ao contrário de um documento cujo conteúdo é estruturado
na própria declaração.

Em caso de divergência: **o componente é autoritativo quanto ao conteúdo do
ato; o NDF é autoritativo quanto a identidade, custódia e classificação.**

Nenhum dos dois corrige o outro. Um erro nos campos descritivos corrige-se por
novo NDF com `relacoes[{tipo: "corrige"}]` (§2.11.2), nunca por alteração do
documento finalizado (§2.1, §5.3). Um produtor **NÃO DEVE** alterar os bytes de
um componente para os harmonizar com a declaração.

#### 2.8.1.3 Anexos de um documento nativo

Um ofício com um mapa de medições, uma informação com uma planta, um parecer com
o extrato que o fundamenta — o documento é nativo, o anexo não é. É o caso
corrente, e o NDF representa-o sem tipo especial e sem sair da via nativa: o ato
vive nos campos estruturados do schema do tipo, e o anexo é um componente com
`papel: "anexo"`.

```json
{
  "documento": {
    "numero": "OF/2026/00123",
    "assunto": "Resposta ao pedido de informação",
    "corpo": "...",
    "componentes": [
      {
        "id": "mapa-medicoes",
        "papel": "anexo",
        "media_type": "text/plain",
        "sha256": "sha256:165830ce12904531cd539298f3ad8066d94fcf678755401ff78b28776edb97ef",
        "tamanho": 130,
        "nome_original": "mapa-medicoes.txt"
      }
    ]
  }
}
```

Daqui decorrem, sem regra nova, as propriedades que interessam: o digest do anexo
entra nos `payload_bytes` e fica **coberto pela assinatura** do documento
(ADR-021); o anexo **viaja** no `.ndfpkg`, em `anexos/` (§8.1); e o fecho de
`NDF-PKG-009` vale nos dois sentidos, pelo que um pacote a que falte um anexo
declarado, ou que transporte um ficheiro não declarado, **NÃO É** conforme.

##### O teste de identidade documental

A pergunta a fazer perante cada anexo não é sobre o seu formato, mas sobre o que
ele é:

> **O anexo tem existência documental própria — autor, data, número, ciclo de
> vida, avaliação ou autenticidade que não sejam os do documento que o
> acompanha?**

| Resposta | Como se representa |
|---|---|
| **Não** — material de apoio, sem vida própria | `componentes[]` com `papel: "anexo"`, dentro deste NDF |
| **Sim** — é um documento, que por acaso segue outro | **NDF autónomo**, ligado por `relacoes[{ tipo: "anexa" }]` (§2.11) |

O segundo caso não é um contorno do primeiro: é o que permite que o anexo tenha a
sua própria avaliação arquivística, o seu prazo de conservação, a sua assinatura e
o seu destino final — e que continue identificável quando o documento que o
acompanhava for eliminado. A relação liga `ndf_id` **e** `payload_hash`, pelo que
fica presa à versão exata do alvo (§2.11.3).

Um produtor **NÃO DEVE** declarar como `componentes[]` um anexo que satisfaça o
teste; e **NÃO DEVE** fragmentar em NDF autónomos material que não o satisfaça,
o que produziria documentos sem conteúdo próprio apenas para transportar
ficheiros.

**Nota de âmbito.** Quais os anexos legalmente exigidos por um ato, e se estão
todos presentes, não é matéria do formato — é o exemplo dado em
[ADR-022](../../docs/architecture/ADR-022-dever-do-formato.md). O NDF garante que
os anexos declarados existem, estão íntegros e viajam; não que sejam os certos
nem que estejam completos.

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

- **Tipo**: string em uma de duas formas normativas — canónica `<id>@<versao>`
  (ex. `oficio@1.0.0`, `modelo3-irs@2025.1`), definida pelo registo, ou
  extensão qualificada `ext.<entidade>.<tipo>@<versao>` (ex.
  `ext.at.liquidacao-irs@2026.1`), definida pela entidade produtora. Ver
  §2.9.5. Formas URI/URN exigem uma futura revisão da especificação; não são
  escolhas locais de implementação.
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

#### 2.9.5 Extensão qualificada por entidade

O registo canónico (`specs/registry/`) destina-se a **formas documentais
transversais** — as que atravessam organismos e cuja estrutura é matéria de
normalização (ofício, despacho, informação, parecer). Não se destina a
acomodar a tipologia documental própria de cada entidade: mantê-la
centralmente produziria um número indeterminado de tipos que esta
especificação não tem capacidade nem legitimidade para manter, e um registo
não mantido deixa de ser fonte de verdade.

Para esses casos, `tipo_documento_ref` aceita uma **extensão qualificada**:

```
ext.<entidade>.<tipo>@<versao>
```

| Componente | Regras | Exemplo |
|---|---|---|
| `entidade` | lowercase, `[a-z][a-z0-9-]*` | `at`, `municipio-lisboa` |
| `tipo` | lowercase, `[a-z][a-z0-9-]*` | `liquidacao-irs` |
| `versao` | começa por dígito | `2026.1` |

**Exemplo válido**: `"ext.at.liquidacao-irs@2026.1"`.

Mesmo mecanismo, mesmo regime de responsabilidade e mesma justificação de
§2.11.7 (extensão qualificada de `relacoes[].tipo`): não há registo central, o
namespace `<entidade>` é autodeclarado, e a semântica do tipo é definida e da
responsabilidade exclusiva da entidade que o declara.

**Resolução do schema.** O schema de um tipo de extensão **DEVE** viajar
dentro do `.ndfpkg`, em `schemas/<tipo_id>.schema.json` (§8.1) — por exemplo
`schemas/ext.at.liquidacao-irs.schema.json`. Um verificador independente
valida `documento` contra o schema que veio no pacote, sem acesso a registo
nenhum, o que preserva a garantia de autocontenção de §8.3.

Um leitor **DEVE** resolver o schema do tipo preferencialmente a partir do
pacote, recorrendo ao registo canónico apenas quando o pacote o não contiver.

**O schema do tipo é artefacto de validação, não de reconstrução.** Esta
distinção determina o que sucede quando ele não resolve. Os dados do documento
estão em `documento`, no NDF-core assinado; o layout está no NDT. Um documento
cujo schema de tipo não resolva continua integralmente **reconstituível** e
**verificável quanto à integridade**: o `payload_hash` confere, a assinatura
valida, e `proveniencia_sistema`, `imputacao`, `participantes` e `relacoes`
continuam garantidos pelo schema do NDF-core, que é independente. O que se
perde é apenas a garantia sobre a estrutura **interna** de `documento`.

Por isso, um leitor que não consiga resolver o schema do tipo **DEVE**
rejeitar o documento **ou** tratar `documento` como opaco, sem declarar
interpretação completa — mesma disciplina já aplicada a versões NDF não
suportadas (ver §9.2). O que um leitor **NÃO DEVE** fazer é
declarar `documento` validado quando o não validou: o problema a evitar não é
a interpretação incompleta, é a **incompletude silenciosa**.

Três contextos, portanto:

| Contexto | Tipo não resolúvel |
|---|---|
| Dentro de um `.ndfpkg` | Pacote **não conforme** (ver §9.3) — falhou a promessa de autocontenção de §8.3. É afirmação sobre o pacote, não sobre o documento |
| Leitor com acesso ao registo | Erro — o tipo canónico não existe onde deveria |
| Leitor sem registo, ficheiro avulso | `documento` opaco, declarado como tal |

O test runner de referência (`tools/validate.py`, §9.4) trata o caso como erro
porque **detém o registo canónico**: nele, um tipo canónico não resolúvel
significa que não existe, não que o leitor não lhe tem acesso. Essa
severidade decorre da posição do runner, não é uma norma que os leitores
tenham de replicar.

Esta é uma diferença deliberada face a §2.11.7. Uma relação de tipo
desconhecido **não** conduz à rejeição do documento, porque continua
verificável por hash e só a interpretação semântica fica limitada. Um
`documento` cujo schema não é resolúvel **é** motivo de rejeição em contexto
de pacote, porque sem schema não há garantia estrutural nenhuma sobre o
conteúdo. Tolerância semântica num caso, exigência estrutural no outro.

#### 2.9.6 Porque o schema do tipo não é substituível pelo NDT

§2.6.1 estabelece que `tipo_documento_ref` e `ndt_version_ref` são referências
independentes. Fica por responder uma pergunta que decorre naturalmente dela:
se a reconstrução de um documento depende de NDF **e** NDT, e se o NDT já
declara que campos de `documento` são apresentados, para que serve um schema
de tipo à parte?

**Reconstruir não é interpretar.** O NDT declara **onde imprimir** um valor; o
schema do tipo declara **o que o valor é**. Um sistema de arquivo que indexe,
pesquise ou migre formatos daqui a décadas não passa pelo renderizador: para
esse sistema, sem schema de tipo, um campo de `documento` é uma chave JSON com
um número, sem que se saiba se admite valores negativos, se é obrigatório, ou
que forma tem. O princípio de âmbito desta especificação abrange
explicitamente interpretar corretamente o conteúdo imutável, e não apenas
reconstituí-lo.

**A independência é simétrica.** Sem schema de tipo, o documento ainda se
renderiza mas não se valida; sem NDT, ainda se valida mas não se renderiza. Se
um substituísse o outro, uma das metades desta frase seria falsa.

**Fundir os dois acoplaria dados a apresentação.** Se o NDT fosse também o
contrato de dados, alterar o grafismo de um impresso passaria a ser uma
alteração ao modelo de dados, e um mesmo tipo documental deixaria de admitir
vários NDTs — versão simplificada e completa, formatos de página distintos —
sem duplicar a definição dos dados. É precisamente o acoplamento que §2.6.1
evita.

**Critério operacional.** Uma restrição pertence ao NDT quando a sua violação
significa «não cabe **neste** layout», e ao schema do tipo quando significa «o
dado está mal formado». Um limite de dimensão de texto é exemplo do primeiro
caso: o mesmo conteúdo poderá ser válido noutro NDT. Um NIF com número errado
de dígitos é exemplo do segundo: é inválido independentemente de como venha a
ser apresentado.

**Limite normativo — estrutura, não regras de negócio.** Um schema de tipo
**DEVE** restringir-se à forma dos dados: campos presentes, tipos, formatos,
cardinalidades. **NÃO DEVE** codificar regras materiais de negócio — se um
montante foi corretamente apurado, se uma dedução é elegível, se um prazo está
cumprido. Essas regras pertencem ao sistema produtor, que o NDF não substitui,
e a sua inclusão faria dos schemas de tipo réplicas desatualizadas da lógica
aplicacional, com custo de manutenção crescente e sem garantia real acrescida.

#### 2.9.7 Estabilidade por separação de ritmos de alteração

A razão de fundo para os limites de §2.9.6 é a estabilidade do formato a longo
prazo. Cada camada altera-se por motivos próprios e a ritmos muito diferentes,
e o desenho existe para que a camada mais estável não fique refém da mais
volátil:

| Camada | Altera-se quando | Ritmo típico |
|---|---|---|
| Regras materiais — **fora do NDF** | a lei altera taxas, deduções, prazos, condições | frequente, por vezes intra-anual |
| Schema do tipo (registo) | a **estrutura** do documento muda: campo novo no impresso | ocasional |
| NDT | o grafismo ou o layout muda | ocasional, e independente do anterior |
| NDF | o **formato de documento** muda | raro — escala de décadas |

Uma alteração legislativa atinge, na esmagadora maioria dos casos, apenas a
primeira linha: é absorvida pelo sistema produtor, sem qualquer efeito sobre o
NDF, o NDT ou o registo. Quando cria um campo novo no impresso, atinge também
a segunda — produzindo uma versão nova do tipo no registo, por exemplo
`modelo3-irs@2027` —, ainda assim **sem** implicar versão nova de NDF ou de
NDT (ver `VERSIONING.md`). Uma alteração de grafismo atinge apenas o NDT, e
não invalida nem obriga a alterar o NDF.

**Onde a dimensão legislativa entra no NDF.** Entra como **proveniência, não
como validação**: `proveniencia_sistema[].regra_ref` (§2.14.2) referencia o
conjunto de regras, tabela ou base de cálculo aplicada, por identificador e
hash. É uma referência ao que vigorava no momento da produção — não uma cópia
das regras, nem uma restrição que o validador aplique.

**Consequência para o arquivo.** Um documento finalizado em 2026 tem de
continuar validável em 2046. Se o schema do seu tipo codificasse regras
materiais de 2026, validá-lo décadas depois exigiria reconstituir o direito
vigente à data — confundindo **conformidade estrutural** com **legalidade
material**, que são juízos distintos e de naturezas distintas. A conformidade
estrutural é permanente e verificável por máquina; a legalidade material é
histórica e da competência de quem a aprecia. O NDF garante a primeira e
regista os elementos que permitem apreciar a segunda, sem a substituir.

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

| Valor | Nível eIDAS | Requisito de certificado | Passos obrigatórios no pipeline |
|---|---|---|---|
| `"nenhuma"` | — | Nenhum | Passos 1–3 e 8 (canonicalização, hash, validation_code, persistência) |
| `"avancada"` | SEA — Assinatura Eletrónica Avançada (eIDAS Art.º 26.º) | Certificado com identificação única do signatário; não obrigatoriamente qualificado | Passos 1–8 com CAdES-B-LTA |
| `"qualificada"` | SEQ — Assinatura Eletrónica Qualificada (eIDAS Art.º 25.º) | Certificado qualificado emitido por PSSC inscrito na lista de confiança eIDAS | Passos 1–8 com CAdES-B-LTA |

**Esta tabela não dá exemplos de tipos de ato, e a omissão é deliberada.** Uma
coluna que associasse ofícios a `"avancada"` e contratos públicos a
`"qualificada"` seria lida como classificação jurídica, e copiada como tal —
apesar de §2.10.2 dizer o contrário duas linhas abaixo. A tabela fixa apenas o
que se decide dentro do artefacto: que certificado cada valor exige e que passos
do pipeline desencadeia. Que atos pertencem a cada classe é matéria de §2.10.2.

#### 2.10.2 Responsabilidade de classificação

A classificação correcta de um ato num destes três níveis é **responsabilidade da entidade produtora**. A especificação NDF não define o mapeamento entre tipos de ato e níveis de assinatura — essa é uma decisão de direito administrativo, que cada entidade define de acordo com o CPA, os estatutos sectoriais, e as suas normas internas de delegação de competência e autenticidade documental.

#### 2.10.3 Implicações para o envelope

`timestamps` e `validation_material` são campos **de cada entrada** de
`assinaturas[]`, não do envelope (§4.4.1) — as colunas abaixo referem-se ao
conteúdo de cada assinatura presente.

| `nivel_assinatura` | `assinaturas[]` | `timestamps` (por assinatura) | `validation_material` (por assinatura) | `validation_code` |
|---|---|---|---|---|
| `"nenhuma"` | Ausente ou `[]`; selo institucional opcional | Presente no selo, quando exista | Presente no selo, quando exista | **Sempre presente** |
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

#### 2.11.3 Sucessão documental (`substitui`)

A relação `substitui` é a **única** representação normativa de sucessão entre
documentos (§6). Um NDF que suceda a outro DEVE incluí-la. Não existe
mecanismo paralelo no envelope nem no manifesto — a sucessão fica coberta
pela assinatura do NDF-core, como qualquer outra relação. Ver ADR-011.

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

**Exemplo de uso corrente — instrução do procedimento.** O vocabulário base tem
`anexa` (o alvo é anexado a este documento) e `responde_a` (este documento é
resposta ao alvo), mas não tem valor para «o alvo instrui este procedimento»,
que é o vínculo entre um requerimento recebido e a informação técnica que sobre
ele se produz. Uma entidade que precise dele declara-o como
`ext.<entidade>.instrui` — não é `anexa`, porque o requerimento não é anexo da
informação, e não é `responde_a`, porque a informação não responde ao
requerente. Ambos os documentos são NDF autónomos, ligados por relação
verificável, e não secções do mesmo documento (ADR-003).

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
poderá assinar num papel de representante sem ser autor
material. O
bloco `participantes`, opcional, regista essa informação de forma estrutural
e independente do texto de exibição que já existe nalguns schemas de tipo de
documento (ex.: `informacao-tecnica.autor`, `despacho.decisor`) — esses
campos continuam a servir a apresentação do documento (via NDT); `participantes`
serve a consulta, a proveniência e a interoperabilidade documental.

`participantes` é um índice **exclusivamente de pessoas singulares**. Os
sistemas determinísticos ficam em `proveniencia_sistema` (§2.14), os sistemas
de IA em `proveniencia_ia` (§2.13), a responsabilidade jurídica em `imputacao`
(§2.15) e a entidade produtora em `metadados.entidade_produtora` (§2.7.3). Um
sistema não *participa* na produção de um documento — **produz** o documento.

```json
{
  "participantes": [
    { "participante_ref": "user:123", "papel": "autor" },
    { "participante_ref": "user:456", "papel": "revisor_humano" }
  ]
}
```

#### 2.12.2 Campos

| Campo | Obrigatório | Descrição |
|---|---|---|
| `participante_ref` | Sim | Identificador institucional estável da pessoa singular — não um nome de exibição. |
| `papel` | Sim | `autor`, `coautor`, `revisor_humano`, `decisor`, `representante`, `responsavel_tecnico`. |
| `qualificacao` | Não | Qualidade profissional, quando é condição de validade do documento. Ver §2.12.6. |

| Papel | Significado |
|---|---|
| `autor` | Produziu materialmente o conteúdo do documento: o conteúdo estruturado que é canonicalizado, ou o componente binário que o constitui (§2.8.1). |
| `coautor` | Produziu materialmente parte do conteúdo, em conjunto com o autor. |
| `revisor_humano` | Reviu conteúdo produzido por outrem — pessoa, sistema ou IA. |
| `decisor` | Praticou a decisão que constitui o conteúdo do documento (ex.: despacho). |
| `representante` | Atuou por conta de outrem, ao abrigo de mandato ou representação. |
| `responsavel_tecnico` | Responde tecnicamente em nome próprio, sem representar (ex.: contabilista certificado, ROC, autor de termo de responsabilidade). |

`autor`, `coautor` e `decisor` são os papéis que satisfazem o invariante de
origem de §2.2.1. `revisor_humano`, `representante` e `responsavel_tecnico`
não o satisfazem: rever, representar ou responder tecnicamente por um conteúdo
não é o mesmo que produzi-lo.

Um sistema — determinístico ou de IA — **NÃO DEVE** ser registado em
`participantes` sob nenhum papel. O papel `sistema_tecnico` e o campo `tipo`
existiram em versões anteriores desta preparação e foram removidos; ver
§2.12.7 (nota de migração).

#### 2.12.3 Autoria — três noções distintas, não equivalentes

Três mecanismos são capazes de afirmar autoria num NDF. São **semanticamente
distintos** e NÃO DEVEM ser interpretados como equivalentes nem como uma
hierarquia de precedência:

| Mecanismo | O que significa |
|---|---|
| `documento.autor` (schema do tipo, §2.9) | Autoria **representada no conteúdo documental** — o que o renderizador apresenta no documento reproduzido (ex.: "Autor: Maria Silva"). |
| `participantes[].papel = "autor"` (§2.12) | Autoria **estrutural declarada**, para indexação, proveniência e interoperabilidade documental — por identificador institucional, não por nome de exibição. |
| `assinaturas[].papel = "autor"` (envelope, §4.4.1) | A qualidade em que uma assinatura foi aposta: esta pessoa assinou **na qualidade declarada de autor**. |

Quando coexistam, o produtor DEVE assegurar coerência entre a autoria
estrutural declarada em `participantes` e a autoria representada no conteúdo
documental, salvo quando o tipo documental justificar explicitamente a
diferença. `assinaturas[].papel` descreve apenas a qualidade em que a
assinatura foi aposta e **não redefine** a autoria documental — nem prova,
isoladamente, que o signatário seja o único autor.

Divergir entre os três é legítimo em casos concretos (ex.: um documento
assinado por um representante em nome do autor material). Por isso esta
especificação não impõe validação automática de igualdade — impõe que a
diferença, quando exista, seja intencional e não acidental.

#### 2.12.4 `participante_ref` como referência externa

`participante_ref` é uma referência externa, não resolvida pelo NDF —
paralelo direto a `avaliacao.classificacao_ref` (§3.2.1), que também
referencia um instrumento externo sem o incorporar. O NDF não define nem
embute um esquema de identidade verificável: a resolução de
`participante_ref` para uma identidade concreta (nome, função,
credenciais) é responsabilidade do sistema produtor, que mantém o registo
correspondente na sua própria base de dados.

#### 2.12.5 A ausência de um participante não é prova de ausência de intervenção

`participantes` regista apenas intervenção **observável e identificada** pelo
sistema produtor. A ausência de uma entrada **NÃO DEVE** ser interpretada como
demonstração de que ninguém mais interveio.

A razão é concreta e não teórica: quando um terceiro atua com as credenciais
do titular — um contabilista ou um familiar que submete uma declaração no
portal com as credenciais do contribuinte — o sistema produtor não tem como o
distinguir do titular. Registá-lo seria inventar informação que o sistema não
observou; omiti-lo é o comportamento correto.

Daqui decorre que um `participantes` vazio ou ausente é **silêncio, não
negação**. Um leitor — incluindo um sistema de análise ou uma parte em
contencioso — NÃO DEVE derivar de tal silêncio qualquer conclusão sobre a
inexistência de intervenção de terceiros.

Esta cláusula é o correspondente, no eixo dos participantes, do princípio já
adotado em §2.13.3 para a revisão humana: o formato distingue **o que é
afirmado** do **que não é conhecido**, em vez de deixar a omissão fazer
afirmações por conta própria.

#### 2.12.6 `qualificacao` — qualidade profissional como condição de validade

Há documentos cuja validade depende da intervenção de pessoa com qualidade
profissional determinada: contabilista certificado numa declaração Modelo 22
ou num anexo de rendimentos empresariais, revisor oficial de contas numa
certificação legal, advogado mandatado num requerimento, engenheiro ou
arquiteto num termo de responsabilidade de licenciamento urbanístico, médico
num atestado.

Nesses casos, o bloco opcional `qualificacao` regista a qualidade e a
inscrição na ordem profissional respetiva:

```json
{
  "participantes": [
    { "participante_ref": "user:123", "papel": "autor" },
    {
      "participante_ref": "user:900",
      "papel": "responsavel_tecnico",
      "qualificacao": { "tipo": "contabilista_certificado", "identificador": "occ:12345" }
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `tipo` | Sim | Qualidade profissional. Enum aberto: `contabilista_certificado`, `revisor_oficial_contas`, `advogado`, `engenheiro`, `arquiteto`, `medico`, entre outros. |
| `identificador` | Sim | Identificador de inscrição na ordem profissional. Referência externa, não resolvida pelo NDF — mesmo princípio de §2.12.4. |

`qualificacao` é ortogonal a `papel`. Um advogado mandatado é
`representante` com `qualificacao.tipo: "advogado"`; um contabilista
certificado que responde tecnicamente pela declaração é
`responsavel_tecnico` com `qualificacao.tipo: "contabilista_certificado"`.

A distinção face a `imputacao` (§2.15) é a seguinte: o contabilista responde
tecnicamente, mas a declaração continua imputada ao sujeito passivo; o
advogado atua por conta do mandante, e é ao mandante que o requerimento é
imputado. Ambos ficam em `participantes`, não em `imputacao`.

#### 2.12.7 Nota de migração — papéis e campos removidos

Esta ronda de preparação removeu de `participantes` os seguintes elementos.
`ndf_version` mantém-se em `1.0.0` (ADR-007): o NDF está em Draft, sem revisão
pública aberta e sem implementação externa conhecida, pelo que não há
compatibilidade retroativa a preservar.

| Removido | Motivo | Onde passa a ficar |
|---|---|---|
| campo `tipo` (`pessoa`/`sistema`/`entidade`) | Sem sistemas nem entidades, um campo com um só valor possível é ruído no core canonicalizado | — (implícito: todos os participantes são pessoas singulares) |
| `papel: sistema_tecnico` | Um sistema não participa, produz | `proveniencia_sistema` (§2.14) ou `proveniencia_ia` (§2.13) |
| `papel: entidade_produtora` | Redundante — a mesma informação existiria em três sítios | `metadados.entidade_produtora` (§2.7.3) e `imputacao` (§2.15) |
| `papel: validador` | Estado de fluxo de aprovação, não facto do conteúdo | Sistema de workflow do produtor (GED/GCA) |
| `papel: aprovador` | Idem | Idem |

A remoção de `validador` e `aprovador` encerra a lacuna L10 de `LACUNAS.md`,
que identificara estes dois papéis como descrevendo estado processual e não
autoria do conteúdo canonicalizado, e deixara a decisão em aberto.

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

`finalidade` é um enum fechado (`apoio_redacao`, `resumo`, `classificacao`,
`pesquisa`, `traducao`, `deteccao_erros`, `outro`). Quando o valor for
`"outro"`, RECOMENDA-SE preencher `finalidade_detalhe` com uma descrição
textual — o mesmo padrão já usado em
`avaliacao.prazo_conservacao.forma_contagem_detalhe` (§3.3).

#### 2.13.4 IA não é signatária, participante nem decisora

Um sistema de IA **NÃO DEVE** ser registado como `signatario` de uma
assinatura (§4) nem como `participante` sob qualquer papel (§2.12.2) — o
papel `sistema_tecnico`, que anteriormente o admitia, foi removido. A IA
**DEVE** ser registada exclusivamente em
`proveniencia_ia.intervencoes[].sistema`. O ato administrativo depende sempre
de intervenção humana identificável.

Os requisitos normativos de produtor e leitor para `proveniencia_ia` estão
enumerados em §9.1 e §9.2. A fronteira entre `proveniencia_ia` e
`proveniencia_sistema` está definida em §2.14.4 e é normativa.

---

### 2.14 Proveniência de sistema produtor (`proveniencia_sistema`)

#### 2.14.1 Objetivo e âmbito

Uma parte substancial dos documentos da Administração Pública é gerada por
sistemas determinísticos, sem autor humano material: liquidações de impostos,
notificações, certidões automáticas, avisos de cobrança. Nesses documentos não
há ninguém que tenha "escrito" o conteúdo, mas há um sistema identificável que
o produziu, segundo regras identificáveis, numa versão identificável.

O bloco opcional `proveniencia_sistema` regista essa origem técnica. É
independente de:

- `metadados.entidade_produtora` (§2.7.3) — o organismo, para efeitos
  arquivísticos;
- `imputacao` (§2.15) — quem responde juridicamente pelo documento. **O
  sistema não é autor jurídico de coisa nenhuma**;
- `participantes` (§2.12) — as pessoas singulares que intervieram.

#### 2.14.2 Estrutura e campos

```json
{
  "proveniencia_sistema": [
    {
      "sistema": {
        "nome": "Sistema de Liquidação de IRS",
        "identificador": "at:sliq-irs",
        "versao": "2026.4.17"
      },
      "componente": "motor-calculo",
      "versao_componente": "3.2.0",
      "gerado_em": "2026-07-31T03:14:00Z",
      "regra_ref": {
        "tipo": "tabela-retencao",
        "identificador": "at:tabelas-irs-2026",
        "hash": "sha256:..."
      }
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `sistema.nome` | Sim | Designação do sistema produtor. |
| `sistema.identificador` | Sim | Identificador institucional estável. Referência externa, não resolvida pelo NDF. |
| `sistema.versao` | Sim | Versão em produção no momento em que o conteúdo foi produzido. |
| `componente` | Não | Componente do sistema responsável por este passo. |
| `versao_componente` | Não | Versão do componente. |
| `gerado_em` | Sim | Instante em que este passo produziu o seu resultado. |
| `regra_ref` | Não | Referência ao conjunto de regras, tabela ou base de cálculo aplicada. |
| `build_ref` | Não | Referência ao *build* exato do sistema. |
| `configuracao_ref` | Não | Referência à configuração em vigor. |

`regra_ref`, `build_ref` e `configuracao_ref` seguem a mesma forma de
`proveniencia_ia.intervencoes[].evidencia_ref` — `{ tipo, identificador,
hash }` — e são **referências externas não resolvidas pelo NDF**, em paralelo
explícito a `participante_ref` (§2.12.4) e a `classificacao_ref`
(§3.2.1). O NDF regista a referência e o hash; o artefacto referenciado vive
no sistema produtor, sob política própria de acesso e retenção.

Esta especificação **não** promete reprodutibilidade byte a byte. Com
`gerado_em` no NDF-core — e já com `ndf_id` como UUID v4 (§2.3) — reexecutar o
mesmo motor sobre os mesmos dados não produz o mesmo documento canónico. O que
o bloco entrega é **identificação estável da origem e das regras aplicadas**,
e o caminho para ir buscar a evidência detalhada onde ela viva.

#### 2.14.3 Cardinalidade e ordem

`proveniencia_sistema` é um **array**, não um objeto único, porque um
documento atravessa por vezes uma cadeia de produção — motor de cálculo, sistema
de validação, sistema de emissão — cada um com produtor e versão próprios.

As entradas **DEVEM** estar ordenadas cronologicamente, por `gerado_em` não
decrescente (ver §9.1 e §9.2).

Esta regra não é estética. JCS (RFC 8785, §2.5) preserva a ordem dos elementos
de um array; a ordem entra, portanto, nos `payload_bytes` e no `payload_hash`.
Sem ordem normativa, dois produtores que registem exatamente os mesmos factos
produziriam documentos com hashes diferentes, o que quebraria a comparação por
hash de que dependem `relacoes[].alvo.payload_hash` (§2.11) e a cadeia de
custódia.

A ordem cronológica não é exprimível em JSON Schema — nenhum vocabulário Draft
2020-12 compara elementos de um array entre si. É, por isso, uma verificação
semântica obrigatória, com caso de conformidade próprio.

#### 2.14.4 Fronteira com `proveniencia_ia` (normativa)

**Qualquer componente não determinístico pertence a `proveniencia_ia`, sem
exceção**, mesmo quando embebido num *pipeline* automático declarado em
`proveniencia_sistema` (ver §9.1 e §9.2).

Um sistema que incorpore um modelo de linguagem, um classificador estatístico
ou qualquer componente cujo resultado não seja função determinística das
entradas **NÃO DEVE** declarar esse componente em `proveniencia_sistema`. Deve
declarar em `proveniencia_sistema` a parte determinística do *pipeline*, e a
intervenção do componente não determinístico em `proveniencia_ia`, com o
`revisao_humana.estado` que §2.13.3 exige.

A regra existe porque a alternativa tem consequência prática direta: declarar
um modelo como "sistema" contornaria o estado de revisão humana obrigatório,
que é o mecanismo de garantia central de §2.13. A fronteira entre os dois
blocos não é uma questão de arrumação — é o que impede que a supervisão humana
seja evitada por escolha de campo.

#### 2.14.5 Âmbito mínimo e circulação externa

`proveniencia_sistema` regista o **mínimo necessário** para identificação
estável e para localizar a evidência detalhada. **NÃO DEVE** ser usado como
SBOM, inventário de dependências ou registo de execução. *Logs*, *traces* e
configuração operacional ficam fora do NDF, pelas mesmas razões já decididas
para a IA em §2.13.2: o NDF-core é conservado, por vezes permanentemente, e
embutir material operacional significa conservá-lo indefinidamente.

Consideração adicional, informativa: o NDF-core é assinado e legível por quem
receber o pacote — incluindo o particular notificado de um ato. Nomes,
versões e referências de *build* de sistemas internos constituem superfície de
ataque. RECOMENDA-SE ponderar a omissão de `build_ref` e `configuracao_ref`
em documentos de circulação externa. Esta especificação não define nem
garante controlo de acesso ao artefacto (§1.5); a proteção é responsabilidade
do sistema de custódia.

---

### 2.15 Imputação jurídica (`imputacao`)

#### 2.15.1 Objetivo

`participantes`, `proveniencia_sistema` e `proveniencia_ia` registam **factos**
— quem ou o quê produziu materialmente o conteúdo. `imputacao` regista
**direito**: quem responde juridicamente pelo documento, e a que título.

Os dois eixos são independentes por desenho. Podem coincidir (uma declaração
entregue pelo próprio), divergir (uma declaração pré-preenchida por um sistema
e confirmada pelo interessado) ou ser mutuamente exclusivos (uma declaração
produzida por um sistema e imputada por efeito da lei a quem nada fez).

O bloco responde a exigências legais concretas do direito administrativo
português:

- **CPA, art. 151.º, n.º 1, al. a)** — do ato tem de constar a indicação da
  autoridade que o pratica **e a menção da delegação ou subdelegação de
  poderes, quando exista**;
- **CPPT, art. 36.º, n.º 2** — as notificações têm de conter a indicação da
  entidade que praticou o ato e se o fez no uso de delegação ou subdelegação;
- **CPPT, art. 66.º, n.º 2** — o recurso hierárquico é dirigido ao mais
  elevado superior hierárquico **do autor do ato**, o que exige que o órgão
  autor seja identificável.

Sem estas menções, o interessado não consegue determinar a quem recorrer, e o
ato fica ferido de vício de forma. `imputacao` torna a informação estrutural e
verificável, em vez de a deixar dispersa no texto do documento.

Esta especificação fornece o mecanismo de registo; **não** garante, por si só,
a legalidade do ato nem a suficiência das menções em qualquer caso concreto —
mesmo limite de âmbito de §1.1 e §1.4.

#### 2.15.2 Campos e títulos

```json
{
  "imputacao": [
    {
      "imputado": { "designacao": "Diretor de Serviços do IRS", "ref": "at:dsirs" },
      "titulo": "delegacao",
      "fundamento": {
        "descricao": "Despacho n.º 000/2026",
        "publicacao_ref": "DR, 2.ª série, n.º 000, de 2026-01-15"
      }
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `imputado.designacao` | Sim | Designação do órgão ou pessoa que responde juridicamente. |
| `imputado.ref` | Não | Identificador institucional estável. Referência externa, não resolvida pelo NDF. |
| `titulo` | Sim | Título ao abrigo do qual a responsabilidade é assumida. Enum fechado — ver abaixo. |
| `fundamento.descricao` | Condicional | Fundamento em forma legível. |
| `fundamento.publicacao_ref` | Condicional | Referência de publicação oficial do ato habilitante. |
| `em` | Condicional | Instante do ato que estabeleceu a imputação. Numa submissão autenticada, o instante da submissão. |
| `autenticacao` | Não | Meio pelo qual este imputado foi autenticado. Ver §2.15.4. |

| `titulo` | Regime | Significado | Exige |
|---|---|---|---|
| `competencia_propria` | Ato administrativo | O órgão pratica o ato ao abrigo de competência própria | — |
| `delegacao` | Ato administrativo | O órgão pratica ao abrigo de poderes delegados | `fundamento.publicacao_ref` |
| `subdelegacao` | Ato administrativo | O órgão pratica ao abrigo de poderes subdelegados | `fundamento.publicacao_ref` |
| `declaracao_propria` | Declarativo | O declarante produziu e apresentou a declaração | — |
| `aceitacao_expressa` | Declarativo | O conteúdo foi produzido por outrem e expressamente aceite pelo imputado | `em` |
| `efeito_legal` | Declarativo | A imputação resulta de efeito da lei, sem ato do imputado | `fundamento.descricao` |

A exigência de `publicacao_ref` em `delegacao` e `subdelegacao` é o reflexo
direto da menção obrigatória do CPA art. 151.º, n.º 1, al. a): declarar que se
atua por delegação sem identificar o ato de delegação publicado seria registar
metade da menção que a lei exige.

Estas condicionais são exprimíveis em JSON Schema (`if`/`then`) e estão lá,
pelo que qualquer validador Draft 2020-12 as aplica sem código adicional.

#### 2.15.3 Cardinalidade — co-titularidade, não cadeia de delegação

`imputacao` é um array. Mais do que uma entrada significa **co-titularidade da
responsabilidade jurídica** — várias pessoas ou órgãos respondem pelo mesmo
documento. Dois casos típicos:

- **ato conjunto**: dois ou mais órgãos praticam o mesmo ato administrativo;
- **declaração conjunta**: dois ou mais declarantes respondem pela mesma
  declaração. Numa declaração de IRS em tributação conjunta, ambos os sujeitos
  passivos (A e B) são imputados, cada um com a sua entrada e a sua
  `autenticacao` (§2.15.4).

Uma delegação **NÃO DEVE** ser modelada como duas entradas (delegante e
delegado). É **uma** entrada, com `titulo: "delegacao"` e o `fundamento` a
identificar o ato de delegação. Modelar delegação como duas autoridades
destruiria a distinção entre "dois órgãos praticaram o ato" e "um órgão
praticou ao abrigo de poderes de outro" — que é precisamente a distinção que o
CPA manda mencionar.

#### 2.15.4 Submissão por meio autenticado

Uma parte substancial dos documentos entregues à Administração não tem
assinatura eletrónica: é submetida através de um canal autenticado — Portal
das Finanças, Segurança Social Direta e equivalentes. O formato tem de
conseguir representar esse caso sem o forçar ao vocabulário da assinatura
eletrónica.

O produtor **PODE** declarar a imputação ao titular identificado pelo mecanismo
de autenticação, quando essa conclusão resulte do regime jurídico e da política
que lhe são aplicáveis. O bloco opcional `autenticacao`, em cada entrada de
`imputacao`, regista o **facto observado** que o produtor invoca como fundamento
dessa declaração; a conclusão jurídica em si é da entidade produtora, nos termos
de §2.15.1:

```json
{
  "imputacao": [
    {
      "imputado": { "designacao": "Sujeito passivo A", "ref": "nif:123456789" },
      "titulo": "declaracao_propria",
      "em": "2026-05-20T14:03:00Z",
      "autenticacao": { "meio": "chave_movel_digital", "nivel_garantia": "elevado" }
    },
    {
      "imputado": { "designacao": "Sujeito passivo B", "ref": "nif:987654321" },
      "titulo": "declaracao_propria",
      "em": "2026-05-20T14:06:00Z",
      "autenticacao": { "meio": "senha_acesso", "nivel_garantia": "substancial" }
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `meio` | Sim | Meio de autenticação. Enum aberto: `chave_movel_digital`, `cartao_cidadao`, `senha_acesso`, `certificado_qualificado`, `presencial`. |
| `nivel_garantia` | Não | Nível de garantia, na terminologia eIDAS: `baixo`, `substancial`, `elevado`. Opcional — o sistema produtor poderá não o classificar. |

O enum é aberto e **inclui deliberadamente o atendimento presencial**. Um
vocabulário que só exprimisse meios digitais obrigaria a modelar o caso
presencial por omissão, tornando-o indistinguível de um documento sem
identificação nenhuma — e a identificação ao balcão é um facto observado como
qualquer outro. Que efeito lhe corresponde é matéria do regime aplicável, não do
vocabulário que o regista.

**Por entrada, não por documento.** Quando a lei exige autenticação de mais do
que um interessado — o caso da declaração de IRS em tributação conjunta, que
requer a autenticação de ambos os sujeitos passivos —, cada um constitui uma
entrada própria, com o seu instante e o seu meio. Registar a autenticação ao
nível do documento perderia essa informação, que é exatamente a que
demonstra que a exigência legal foi satisfeita.

**A imputação não é qualificável.** Esta especificação **NÃO DEFINE** nenhum
mecanismo para exprimir grau de confiança, presunção ou reserva sobre uma
imputação: uma entrada de `imputacao` afirma-se ou omite-se, e não admite
gradação. A razão é de âmbito, não de direito — graduar exigiria que o formato
arbitrasse sobre a força de uma declaração alheia, que é precisamente o que não
lhe compete (§1.5; ADR-022). Alegações de extravio ou uso indevido de
credenciais dirimem-se pelas vias competentes, fora do formato: o NDF regista o
facto invocado como fundamento e preserva-o intacto para essa apreciação. Um
produtor **NÃO DEVE** introduzir campos próprios com essa finalidade.

**`nivel_garantia` não gradua a imputação.** Este ponto merece regra própria,
porque o campo tem aparência de qualificador e não o é. `nivel_garantia`
descreve o nível de garantia **técnico do mecanismo de autenticação**, na
terminologia eIDAS, para efeitos de interoperabilidade e de caracterização do
canal. NÃO descreve a força com que o documento é imputado.

A regra que daqui decorre é semântica, não jurídica: um leitor conforme **NÃO
DEVE** derivar de um `nivel_garantia` mais baixo uma imputação mais fraca, uma
presunção ilidível, ou qualquer tratamento diferenciado do documento (ver
§9.2) — porque o campo não exprime nada disso, e inferi-lo seria atribuir-lhe
significado que a especificação não lhe dá. Se um regime aplicável associa
consequências ao nível de garantia do meio utilizado, essa apreciação cabe a
quem aplica o regime, sobre o facto que o NDF preservou.

**A imputação é histórica, não revogável no documento.** A imputação registada
num NDF afirma a quem o ato era imputado **no momento da finalização**. Uma
anulação posterior — judicial ou administrativa — **NÃO ALTERA** o NDF: o
NDF-core é imutável e assinado (§2.1), e o ato existiu, na forma em que foi
praticado, ainda que venha a ser anulado.

A anulação é um **documento novo**, ligado ao anterior por
`relacoes[].tipo: "anula"` (§2.11.2). Um leitor conforme **NÃO DEVE** tratar a
imputação de um documento anulado como viciada, retroativamente inválida ou
inexistente: era correta quando foi registada, e a anulação é um facto
distinto e posterior, legível no grafo de relações.

O mesmo se aplica à alegação de uso indevido de credenciais. Enquanto não
houver decisão que anule o ato, o ato é formalmente do titular das
credenciais; havendo-a, o registo do ato mantém-se e passa a existir o
registo da anulação a par dele. O NDF preserva os dois, em vez de apagar o
primeiro.

**Equivalência entre canais.** Um pedido apresentado por canal autenticado —
e-balcão e equivalentes — e um pedido apresentado presencialmente por
interessado identificado têm o mesmo valor jurídico, incluindo para efeitos de
legitimidade para obter informação sujeita a sigilo. Um produtor **DEVE**
modelar os dois casos da mesma forma, variando apenas `autenticacao.meio`. O
formato **NÃO DEVE** ser usado de modo que o canal, por si só, produza
diferença de tratamento entre situações que a lei equipara.

**Dupla função do registo de autenticação.** O mesmo facto fundamenta duas
coisas distintas: a **imputação de autoria** do documento submetido, e a
**legitimidade de acesso** do interessado a informação que lhe respeite,
incluindo informação sob sigilo. Quando um documento divulga informação
protegida em resposta a um pedido, é a autenticação do **requerente**, no
documento do pedido, que fundamenta a divulgação — não a imputação do
documento de resposta, que pertence ao órgão que responde.

Essa ligação não exige campo novo: exprime-se pela relação
`relacoes[].tipo: "responde_a"` (§2.11.2) entre a resposta e o pedido, sendo o
registo de autenticação legível na `imputacao` do pedido. A cadeia
pedido→resposta é assim reconstruível e verificável por hash.

Note-se o limite: este registo é **prova, não autorização**. Esta
especificação não define nem garante controlo de acesso, nem verifica
legitimidade (§1.5, §2.7.4). Regista o facto em que uma decisão de divulgação
se apoiou; a decisão em si é do sistema de custódia.

**Relação com `nivel_assinatura`.** `nivel_assinatura: "nenhuma"` (§2.10) e
`imputacao[].autenticacao` **não são contraditórios**, e um leitor conforme
não os trata como tal. `nivel_assinatura` descreve a existência e o nível de uma assinatura
eletrónica no sentido do eIDAS, materializada no envelope (§4);
`autenticacao` descreve o meio pelo qual o interessado foi identificado no
canal de submissão. Um documento é capaz de não ter assinatura
eletrónica e ainda assim ter autoria vinculativa. Um leitor **NÃO DEVE** concluir, de
`nivel_assinatura: "nenhuma"`, que o documento é anónimo ou não imputável.

#### 2.15.5 Casos de referência

Os casos seguintes, quase todos sobre a mesma tipologia documental (a
declaração Modelo 3 de IRS e a liquidação subsequente), motivaram o desenho
deste bloco e ilustram a independência dos eixos.

| Caso | `participantes` | `proveniencia_sistema` | `imputacao` |
|---|---|---|---|
| Declaração entregue pelo sujeito passivo (CIRS art. 56.º) | `autor` | — | 1 entrada, `declaracao_propria` + `autenticacao` |
| Declaração conjunta, tributação conjunta | `autor`, `coautor` | — | **2 entradas** (A e B), `declaracao_propria` + `autenticacao` cada |
| Declaração automática confirmada (CIRS art. 58.º-A) | — | sistema da AT | 1 entrada, `aceitacao_expressa` + `autenticacao` |
| Declaração automática convertida sem confirmação (CIRS art. 58.º-A) | — | sistema da AT | 1 entrada, `efeito_legal` |
| Liquidação oficiosa (CIRS art. 76.º, n.º 1, al. b)) | — | sistema da AT | 1 entrada, `competencia_propria` ou `delegacao` |
| Pedido por e-balcão ou ao balcão | `autor` | — | 1 entrada, `declaracao_propria` + `autenticacao` (`meio` distingue o canal) |

O terceiro caso é o que justifica a existência do bloco. Não havendo
confirmação nem entrega até ao termo do prazo, a declaração provisória
converte-se em declaração apresentada pelo sujeito passivo nos termos legais:
a autoria é imputada, por efeito da lei, a quem não produziu o conteúdo nem
praticou qualquer ato. Registar o sujeito passivo como
`participantes[].papel: "autor"` seria juridicamente correto e **factualmente
falso**; registar apenas `proveniencia_sistema` seria factualmente correto e
**juridicamente incompleto**. Os dois eixos, em conjunto, dizem a verdade nos
dois planos.

Note-se ainda que, no terceiro e no quarto casos, `participantes` está
legitimamente ausente — o invariante de origem de §2.2.1 é satisfeito por
`proveniencia_sistema`, e nenhum autor humano é fabricado para o cumprir.

#### 2.15.6 Obrigatoriedade

`imputacao` é **opcional** no NDF-core: nem todo o NDF é ato administrativo ou
declaração. Uma informação técnica interna, uma nota de serviço ou um registo
de trabalho não têm imputação no sentido aqui definido.

O schema do tipo documental (`metadados.tipo_documento_ref`, §2.9.2) **PODE**
tornar `imputacao` obrigatória para os tipos em que a lei o exige — mesma
camada de exigência já usada noutros pontos desta especificação. Um tipo
documental que represente um ato administrativo notificável DEVERIA fazê-lo.

---

## 3. Avaliação arquivística

### 3.1 Fundamento

Todo o documento de arquivo DEVE ter associada uma decisão de avaliação que
determina:

- O **prazo de conservação** — período durante o qual a informação é mantida,
  contado a partir de um facto desencadeador declarado.
- O **destino final** — decisão sobre o que sucede ao documento decorrido esse
  prazo.
- O **instrumento** que autoriza a decisão, na versão consultada.

Este trio é comum aos sistemas arquivísticos europeus, ainda que com
terminologia distinta: em Portugal, PCA e Destino Final segundo os instrumentos
da DGLAB (Lista Consolidada, Tabelas de Seleção, Portarias de Gestão de
Documentos); em França, *durée d'utilité administrative* e *sort final* segundo o
*tableau de gestion*; nos Países Baixos, *bewaartermijn* e *waardering* segundo a
*selectielijst*; na Alemanha, *Aufbewahrungsfrist* seguida de apreciação pelo
arquivo competente; no Reino Unido e nas instituições europeias, *retention
period* e *disposal action* segundo a *retention and disposal schedule*.

O NDF-core fixa a **estrutura** deste trio e delega o **vocabulário** num perfil
declarado (§3.2.3). O bloco `avaliacao` é obrigatório em qualquer NDF-core.

### 3.2 Estrutura do bloco `avaliacao`

```json
{
  "avaliacao": {
    "perfil": "pt-dglab",
    "classificacao_ref": "lc/450.10.001",
    "prazo_conservacao": {
      "valor": 5,
      "unidade": "anos",
      "forma_contagem": "data_documento"
    },
    "destino_final": "eliminacao",
    "instrumento_ref": "lc/lista-consolidada-dglab-2023-v3"
  }
}
```

| Campo | Obrigatório | Tipo | Descrição |
|---|---|---|---|
| `perfil` | Sim | string | Perfil de avaliação arquivística aplicável. Determina o vocabulário e a sintaxe de `classificacao_ref` e `instrumento_ref`. Ver §3.2.3. |
| `classificacao_ref` | Sim | string | Referência à classe/série no instrumento aplicável. Sintaxe definida pelo perfil. Ver §3.2.1. |
| `prazo_conservacao.valor` | Sim | inteiro ≥ 0 | Quantidade do prazo. |
| `prazo_conservacao.unidade` | Sim | string (enum) | `dias` \| `meses` \| `anos`. |
| `prazo_conservacao.forma_contagem` | Sim | string (enum) | Facto a partir do qual o prazo é contado. Ver §3.3. |
| `destino_final` | Sim | string (enum) | Destino decorrido o prazo. Ver §3.4. |
| `autoridade_avaliacao` | Condicional | string | Obrigatório **se e só se** `destino_final: "a_determinar"`. Ver §3.4.1. |
| `instrumento_ref` | Sim | string | Instrumento e versão consultados para resolver prazo e destino no momento da finalização. Sintaxe definida pelo perfil. Ver §3.2.2. |

#### 3.2.1 `classificacao_ref`

Identifica a classe, série ou entrada do instrumento de avaliação sob a qual o
documento é classificado. A sintaxe **DEVE** obedecer ao schema do perfil
declarado; o NDF-core exige apenas que seja uma string não vazia.

No perfil `pt-dglab`, a string segue o formato `"<instrumento>/<codigo_classe>"`:

| Componente | Descrição |
|---|---|
| `instrumento` | Identificador do instrumento. Valores canónicos: `"lc"` (Lista Consolidada DGLAB), `"ts"` (Tabela de Seleção institucional), `"portaria"` (Portaria de Gestão de Documentos). Extensível por entidades com instrumentos próprios homologados pela DGLAB. |
| `codigo_classe` | Código da classe ou série dentro do instrumento — segue a codificação definida pelo próprio instrumento. |

**Exemplos válidos no perfil `pt-dglab`**:
```
"lc/450.10.001"    — classe 450.10.001 da Lista Consolidada DGLAB
"lc/150.30.400"    — classe 150.30.400 da Lista Consolidada DGLAB
"ts/at/300.20"     — classe 300.20 da Tabela de Seleção da AT
"portaria/1253-A/2009/II-3"  — série II-3 da Portaria n.º 1253-A/2009
```

**RECOMENDA-SE** que o sistema produtor resolva `classificacao_ref`
automaticamente a partir do tipo de documento, para reduzir erro humano e
garantir consistência entre documentos do mesmo tipo. O NDF não exige um
processo específico de resolução — manual, automático, ou por outra regra é
responsabilidade da aplicação produtora — apenas que o valor final seja válido
para o perfil declarado, coerente com o instrumento referenciado, e imutável
após a finalização (§2.1).

#### 3.2.2 `instrumento_ref`

Regista o instrumento e a versão consultados, permitindo que a regra aplicável
seja rastreável mesmo após atualização do instrumento. A sintaxe **DEVE**
obedecer ao schema do perfil declarado; o NDF-core exige apenas que seja uma
string não vazia.

No perfil `pt-dglab`, a string segue o formato `"<instrumento>/<versao>"`:

| Componente | Descrição |
|---|---|
| `instrumento` | Identificador do instrumento. Valores canónicos: `"lc"`, `"pgd"` (Plano de Gestão de Documentos), `"portaria"`, `"ts"`. Extensível por entidades com instrumentos próprios. |
| `versao` | Identificador da versão ou edição consultada — suficiente para localizar o instrumento exato. Não há formato imposto; RECOMENDA-SE incluir ano e número de revisão. |

**Exemplos válidos no perfil `pt-dglab`**:
```
"lc/lista-consolidada-dglab-2023-v3"   — Lista Consolidada DGLAB, edição 2023 v3
"pgd/pgd-mf-2019-v2"                  — PGD do Ministério das Finanças, v2
"portaria/1253-A-2009"                 — Portaria n.º 1253-A/2009
"ts/at/tabela-2022"                    — Tabela de Seleção da AT, edição 2022
```

No perfil `pt-dglab`, `classificacao_ref` e `instrumento_ref` **DEVEM**
referenciar o mesmo instrumento: o prefixo de `classificacao_ref` DEVE
corresponder ao `instrumento` de `instrumento_ref`. Exemplo: `"lc/450.10.001"`
exige `"lc/..."` em `instrumento_ref`. Esta regra é específica deste perfil e
não se aplica a perfis que não a declarem.

#### 3.2.3 Perfis de avaliação

O campo `perfil` identifica o sistema arquivístico sob o qual a decisão de
avaliação foi tomada. É um **identificador opaco qualificado**: dois ou mais
segmentos separados por hífen, com o padrão
`^(generic|[a-z][a-z0-9]*(-[a-z0-9]+)+)$`.

A convenção do registo é `<namespace>-<autoridade>` — por exemplo `pt-dglab`,
`fr-siaf`, `de-barch`, `eu-ec`. O `namespace` é tipicamente o código ISO 3166-1
alpha-2 da jurisdição, mas **o padrão não o impõe**, e deliberadamente: nem
todos os regimes arquivísticos são nacionais. Perfis institucionais
(`eu-ec`), internacionais (`int-un`) ou setoriais têm de caber no mesmo
mecanismo sem alteração incompatível. O significado de um identificador vem do
registo, não da sua forma.

Os perfis nomeiam a **autoridade** com competência sobre o regime, não o
instrumento que ela publica: os instrumentos mudam de nome e de edição, a
autoridade é o que se mantém estável ao longo da vida do documento.

Cada perfil registado tem um schema em
`specs/registry/profiles/<perfil>.schema.json` que restringe o bloco `avaliacao`
para essa jurisdição. O schema do perfil **DEVE viajar dentro do `.ndfpkg`**, em
`schemas/` — pela mesma razão e com o mesmo mecanismo dos schemas de tipo
documental (§2.9.5, ADR-014): um verificador independente tem de conseguir
validar o bloco sem acesso a registo nenhum, hoje e daqui a décadas.

Perfis definidos por esta especificação:

| Perfil | Âmbito |
|---|---|
| `pt-dglab` | Administração Pública portuguesa — MEG/DGLAB. Impõe a sintaxe `<instrumento>/<...>` (§3.2.1, §3.2.2) e a regra de correspondência de instrumento. |
| `generic` | Sem restrições jurisdicionais. Para entidades cujo sistema arquivístico não tem ainda perfil registado: a estrutura do bloco continua exigida, nenhuma sintaxe nacional é imposta. |

Um perfil não resolúvel em contexto de pacote é **erro** — o pacote tem de o
transportar. Fora de contexto de pacote, um perfil não registado é validado
apenas contra a estrutura do NDF-core.

**Definir um perfil não é matéria desta especificação**: um perfil jurisdicional
exige confirmação contra os instrumentos legais da jurisdição respetiva, e é
introduzido por acréscimo ao registo, sem alteração incompatível do NDF-core.

O mapeamento entre estas primitivas e os regimes de Portugal, França, Alemanha
federal, Países Baixos e Comissão Europeia, com as respetivas fontes jurídicas
primárias, consta da matriz de compatibilidade em
[`docs/profiles/`](../../docs/profiles/README.md) — informativa, não normativa.

#### 3.2.4 Porque a estrutura fica no core e o vocabulário no perfil

A alternativa considerada — delegar o bloco inteiro ao schema do perfil — foi
rejeitada por falhar o critério que dá sentido à generalização (ADR-015):

> Um leitor que nunca ouviu falar do perfil declarado DEVE conseguir, apenas com
> o NDF-core, determinar se o documento é elegível para aplicação do destino
> final e a partir de que facto se conta o prazo.

Por isso `prazo_conservacao` e `destino_final` são campos concretos do NDF-core,
com enums fechados, e o perfil restringe vocabulário sem substituir estrutura.
É o que permite gerir retenção sobre um acervo multi-jurisdicional sem resolver
perfil nenhum.

### 3.3 Enum `forma_contagem`

Conjunto fechado. Declara o facto desencadeador a partir do qual o prazo é
contado — o *trigger* das *retention schedules* anglo-saxónicas e o critério de
contagem dos instrumentos português e francês.

- `data_documento` — a partir da data de finalização do próprio documento.
- `encerramento_processo` — a partir do encerramento do processo/procedimento a que o documento pertence.
- `fim_ano_civil` — a partir do final do ano civil em que o documento foi finalizado.
- `fim_vigencia` — a partir do termo de vigência (ex.: contratos, regulamentos com prazo de validade).
- `outro` — forma de contagem específica, com descrição textual obrigatória em `forma_contagem_detalhe`.

### 3.4 Enum `destino_final`

- `conservacao_permanente` — decorrido o prazo, o documento é destinado a conservação permanente em arquivo. Cobre tanto a conservação no produtor como a transferência para o arquivo competente; o NDF não distingue os dois casos.
- `eliminacao` — decorrido o prazo, o documento é elegível para eliminação.
- `conservacao_parcial_por_amostragem` — apenas uma amostra, conforme o critério definido no instrumento, é conservada permanentemente; o remanescente é eliminado.
- `a_determinar` — a decisão de destino final não está tomada no momento da finalização. Ver §3.4.1.

#### 3.4.1 `a_determinar` e `autoridade_avaliacao`

Em vários sistemas arquivísticos europeus a decisão de destino final **não
compete à entidade produtora**: esta conserva o documento pelo prazo legal e, no
termo, oferece-o à autoridade arquivística, que aprecia o seu valor e decide.
É o modelo alemão de `Anbietung`/`Bewertung`, e corresponde também a
`voorlopig te bewaren` e `nader te bepalen` nos Países Baixos e à ação `review`
das *retention schedules* britânicas e das instituições europeias.

Nesses casos, exigir ao produtor que declare um destino final concreto
obrigá-lo-ia a afirmar o que não sabe. O valor `a_determinar` declara
explicitamente que a decisão está diferida, e `autoridade_avaliacao` — obrigatório
se e só se este valor for usado — identifica quem tem competência para a tomar.

O prazo de conservação continua obrigatório: nos sistemas em causa o prazo é
legal e conhecido mesmo quando a apreciação está pendente. `a_determinar`
difere o **destino**, nunca o **prazo**.

`autoridade_avaliacao` é PROIBIDO quando `destino_final` tem qualquer outro
valor — declarar quem decidiria um destino que já está decidido não tem
significado.

### 3.5 Resolução de `prazo_conservacao` e `destino_final`

`prazo_conservacao` e `destino_final` DEVEM ser coerentes com
`classificacao_ref` e com o instrumento identificado em `instrumento_ref` no
momento da finalização — este último regista qual o instrumento e versão
consultados, preservando a regra aplicável mesmo que o instrumento seja
atualizado posteriormente. O NDF não impõe o processo pelo qual esses valores
são determinados; **RECOMENDA-SE** resolvê-los automaticamente a partir do
instrumento carregado no sistema, para reduzir erro humano — mas essa é uma
decisão de implementação da aplicação produtora, não um requisito do formato.

### 3.6 Dados derivados (fora do NDF-core)

A partir de `avaliacao.prazo_conservacao` e da data de finalização
(`finalizado_em`, campo do envelope/metadados operacionais — não do NDF-core), o
sistema calcula e mantém uma data de elegibilidade para aplicação do destino
final. Este valor:

- **Não** faz parte do NDF-core (não é canonicalizado nem assinado).
- É puramente operacional, recalculável, e usado para processos de gestão de
  arquivo (identificação de documentos elegíveis para aplicação de destino
  final).

Quando `destino_final` é `a_determinar`, a data calculada identifica o momento
de submissão do documento à autoridade indicada em `autoridade_avaliacao`, e não
um momento de eliminação ou de conservação definitiva.

---

## 4. Envelope de integridade e autenticidade

### 4.1 Componentes

| Componente | Conteúdo | Norma | Condicional |
|---|---|---|---|
| `assinaturas[]` | Assinaturas pessoais ou selos institucionais CAdES sobre os `payload_bytes` canónicos — cada entrada é uma unidade de prova autocontida (identidade, certificado, timestamps RFC 3161 e material de validação próprios). Ver §4.4. | CAdES (ETSI EN 319 122), nível B-LTA | Assinatura pessoal obrigatória se `nivel_assinatura ∈ {"avancada", "qualificada"}`; selo institucional opcional se `"nenhuma"` |
| `validation_code` | Código de verificação canónico — derivado de `ndf_id` + `payload_hash`. Ver §4.6. | Esta especificação | **Sempre presente** — independente de `nivel_assinatura` |

`timestamps` e `validation_material` **não são componentes de topo do
envelope** — vivem dentro de cada entrada de `assinaturas[]` (§4.4.1), para
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
| `signatario` | Condicional | Identidade do signatário — obrigatório quando `nivel ∈ {"avancada", "qualificada"}`. Contém `nome` (common name do certificado), `certificado_serie` (número de série, hex) e `cargo` opcional. |
| `assinado_em` | Não | Instante da assinatura (ISO 8601, UTC), declarado pelo produtor. Não substitui o timestamp RFC 3161 de `timestamps.assinatura`, que é a prova temporal oponível. |
| `cades_b_lta` | Sim | Assinatura CAdES-B-LTA detached (DER). |
| `timestamps` | Condicional | Timestamps RFC 3161 desta assinatura — obrigatório quando `nivel ∈ {"avancada", "qualificada"}`. Contém `assinatura` (timestamp B-T sobre o valor da assinatura) e `arquivo` (timestamp B-LTA sobre assinatura + material de validação), ambos DER base64. |
| `validation_material` | Condicional | Material de validação desta assinatura — obrigatório quando `nivel ∈ {"avancada", "qualificada"}`. Contém `cadeia_certificados` (array DER base64, signatário → raiz) e `revogacao` opcional — cada entrada com `tipo` (`ocsp` ou `crl`) e `dados` (resposta DER base64 capturada no momento da assinatura). |

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

### 4.5.1 Assinaturas contidas em componentes

Um documento cujo conteúdo resida em componentes binários (§2.8) inclui, por
vezes, binários que transportam assinaturas próprias, produzidas fora deste
sistema — tipicamente PAdES sobre um PDF recebido de terceiro.

`nivel_assinatura` (§2.10) descreve **a assinatura do NDF** e NÃO DEVE ser
derivado de assinaturas contidas em componentes. Um NDF que preserve um PDF com
assinatura qualificada de terceiro declara
`nivel_assinatura: "nenhuma"`, com ou sem selo institucional — a declaração
PODE ser essa sem que isso constitua defeito. Um leitor NÃO DEVE
apresentar a assinatura de um componente como se fosse assinatura do NDF.

Os bytes de um componente assinado **NÃO DEVEM** ser reescritos, recomprimidos
ou reserializados em circunstância alguma — é o mesmo princípio já aplicado a
`payload_bytes` em §5.3, e a sua violação destrói a assinatura que se pretendia
preservar.

Preservar os bytes não preserva a verificabilidade. Uma assinatura de terceiro
torna-se inverificável quando os certificados expiram, salvo se a cadeia, os
dados de revogação e o timestamp forem recolhidos e congelados no momento da
captura. Esse material DEVE ser preservado como componente próprio quando a
verificabilidade futura da assinatura contida for relevante.

Uma assinatura PAdES produzida por este sistema sobre uma representação do
documento é operação distinta da assinatura CAdES do envelope, sobre objeto
distinto — ver a cláusula «Assinatura do NDF e assinatura de representações»
em [`specs/ndt/SPEC.md`](../ndt/SPEC.md). Quando produzida, a ordem é normativa: assinar o
PDF, calcular o hash do PDF **já assinado**, declarar esse hash no componente e
só então finalizar o NDF. A ordem inversa produz um hash que não corresponde ao
ficheiro distribuído.

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
- `avaliacao.prazo_conservacao` ou `avaliacao.destino_final` não puderem ser resolvidos a partir de `classificacao_ref` e do instrumento identificado em `instrumento_ref` (instrumento indisponível ou sem entrada correspondente). Quando o instrumento existe mas a decisão de destino compete a outra autoridade, o caso não é de recusa: declara-se `destino_final: "a_determinar"` (§3.4.1).
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

## 6. Sucessão documental

### 6.1 Princípio

Um NDF finalizado nunca é editado. Uma "nova versão" de um documento é um
**NDF novo e distinto**, com o seu próprio NDF-core, envelope, e ciclo de
finalização completo (§5).

Sucessão **não é versionamento interno de um documento** — é uma **relação
entre dois documentos NDF autónomos e imutáveis**:

```text
A continua a existir, imutável
B substitui A
```

e não `A passou a ser B`. O documento substituído não é alterado nem
destruído pela existência do sucessor; apenas deixa de ser o documento
corrente, o que é uma propriedade operacional gerida fora do NDF-core
(§2.4.1).

### 6.2 Representação normativa

A sucessão é registada no **NDF-core**, como relação `substitui` (§2.11):

```json
{
  "relacoes": [
    {
      "tipo": "substitui",
      "alvo": {
        "ndf_id": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
        "payload_hash": "sha256:3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b"
      }
    }
  ]
}
```

Um NDF que suceda a outro **DEVE** incluir esta relação. `alvo.payload_hash`
liga a sucessão aos bytes canónicos exatos do documento substituído,
permitindo confirmar que não foi adulterado.

Esta é a **única** representação normativa de sucessão. Não existe mecanismo
paralelo no envelope nem no manifesto: a relação fica coberta pela assinatura
do NDF-core, ao contrário de qualquer campo de envelope. Ver ADR-011 para a
justificação, e ADR-002 para o modelo geral de relações.

`substitui` não tem estatuto especial face aos restantes tipos de relação
(§2.11.2) — um documento é livre de suceder a mais do que um antecedente
(`relacoes` é um array), e de combinar `substitui` com outras relações no
mesmo NDF.

### 6.3 Pacote de exportação (`.ndfpkg`)

O formato `.ndfpkg` é o **pacote de exportação autocontido** de um NDF
finalizado. É definido nesta especificação (§8) e reúne os objetos necessários
para verificação, renderização e preservação sem dependências externas.

A cadeia de sucessão de um processo documental é uma coleção de pacotes
`.ndfpkg` independentes, reconstruível a partir das `relacoes` no
`ndf-core.json` de cada pacote — isto é, a partir dos bytes assinados, nunca
por conteúdo embutido nem por metadados de empacotamento.

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
├── schemas/               — schemas necessários à validação autónoma do pacote
│   ├── <tipo_id>.schema.json           — schema do tipo referenciado por tipo_documento_ref
│   └── <perfil>.schema.json            — schema do perfil referenciado por avaliacao.perfil
├── recursos/              — recursos visuais partilhados por NDT e NCRTF
│   ├── <sha256>.<ext>     — recursos NDT com modo referenciado_por_hash (nome = hash)
│   └── <nome>.<ext>       — imagens NCRTF referenciadas por image.ref (nome declarado no campo)
├── original/              — componentes com papel «original» (§2.8.1), bytes tal como emitidos ou recebidos
├── representacoes/        — componentes derivados de um original para garantir fidelidade visual
├── anexos/                — componentes de apoio sem identidade documental própria
└── evidencias/            — material de validação de assinaturas contidas em componentes (§4.5.1)
```

Os quatro últimos diretórios existem apenas quando o documento declarar
componentes com os papéis correspondentes; um NDF cujo conteúdo seja
estruturado não os tem.

O nome de cada ficheiro dentro deles é livre — o diretório reflete o papel, e a
correspondência com a declaração faz-se **pelo digest** e nunca pelo caminho
(§2.8.1). Um pacote materializado de outra forma, com outros nomes de ficheiro,
continua a corresponder ao mesmo NDF e à mesma assinatura.

Todos os componentes declarados em `documento` integram a materialização; um
`.ndfpkg` que omita qualquer um deles não é conforme (`NDF-PKG-009`). Não há
categoria de componente documental omissível.

O fecho vale nos dois sentidos: um ficheiro colocado num destes diretórios sem
corresponder a componente declarado também torna o pacote não conforme. Estar
inventariado garante-lhe integridade, não estatuto documental — sem declaração
em `documento`, nenhum leitor sabe que papel tem, e a assinatura não o cobre.

O diretório `schemas/` torna o pacote autonomamente validável: um verificador
independente valida `documento` contra o schema que veio no pacote, sem acesso
ao registo canónico. É **obrigatório** quando `tipo_documento_ref` usa uma
extensão qualificada `ext.<entidade>.<tipo>@<versao>` (§2.9.5), por não haver
outro local onde o schema possa ser resolvido, e RECOMENDADO nos restantes
casos. O nome do ficheiro é o identificador do tipo sem a versão — por exemplo
`schemas/ext.at.liquidacao-irs.schema.json` para
`ext.at.liquidacao-irs@2026.1`.

O schema do perfil de avaliação declarado em `avaliacao.perfil` (§3.2.3) é
**sempre obrigatório** em `schemas/`, pela mesma razão: sem ele, um verificador
independente não consegue validar o bloco `avaliacao` contra as regras da
jurisdição sob a qual a decisão de avaliação foi tomada. O nome do ficheiro é o
identificador do perfil — por exemplo `schemas/pt-dglab.schema.json`.

### 8.2 `manifest.json`

O manifesto é **inventário físico do pacote** — não duplica informação
documental do NDF-core. Todos os campos abaixo são obrigatórios (este
exemplo valida contra `manifest.schema.json`):

```json
{
  "ndfpkg_version": "1.0.0",
  "ndf_id": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
  "ndf_version": "1.0.0",
  "schema_id": "oficio-generico",
  "estado": "ativo",
  "nivel_assinatura": "qualificada",
  "finalizado_em": "2026-06-18T10:30:00Z",
  "payload_hash": "sha256:7196abc4d62371c2fea9da9d409d72d8d128244f4447b0cf8121b5d0fcbfce5f",
  "validation_code": "NDF-COXWCCZKZUUKRS76N7OJ",
  "inventario": [
    { "ficheiro": "ndf-core.json", "hash_sha256": "sha256:7196abc4d62371c2fea9da9d409d72d8d128244f4447b0cf8121b5d0fcbfce5f" },
    { "ficheiro": "envelope.json", "hash_sha256": "sha256:f37a43b32b61ecccf22d8408b4fb1fa0ee2be3e7ed3c5181d3a75878a6272410" },
    { "ficheiro": "ndt/oficio-generico@2.0.0.ndt.json", "hash_sha256": "sha256:f036d126366753ae21c47881c03f05ecf5a9d15359a597c339f88d8e2195f575" }
  ]
}
```

### 8.3 Garantias do `.ndfpkg`

- **Auto-suficiência**: contém tudo o que é necessário para verificar a assinatura, reproduzir visualmente o documento e confirmar a avaliação arquivística — sem dependência de infraestrutura online.
- **NDT embebido**: o NDT referenciado por `ndt_version_ref` é incluído no pacote, garantindo reprodutibilidade visual mesmo que o NDT evolua ou o repositório original deixe de existir.
- **Verificabilidade**: o pacote permite a qualquer implementação conforme verificar `sha256(ndf-core.json) == payload_hash` e validar a assinatura CAdES-B-LTA sem acesso ao core-documental original.
- **Cadeia de sucessão**: reconstruível a partir das `relacoes` no `ndf-core.json` de cada pacote (§6.3) — os bytes assinados. O `manifest.json` é inventário físico do pacote e NÃO DEVE duplicar informação documental do NDF-core.

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
6. **NDF-PROD-006 — DEVE** incluir todos os campos obrigatórios de `metadados` (§2.7.2), incluindo o bloco `protecao_dados` quando `contem_dados_pessoais: true` e omitindo-o quando é `false`.
7. **NDF-PROD-007 — DEVE** declarar `avaliacao.perfil` e definir `classificacao_ref` e `instrumento_ref` em conformidade com o schema desse perfil (§3.2.1, §3.2.2, §3.2.3).
8. **NDF-PROD-008 — DEVE** gerar `ndf_id` como UUID v4 válido (RFC 9562), único no espaço de nomes do sistema produtor.
9. **NDF-PROD-009 — DEVE** definir `estado: "ativo"` no NDF-core de qualquer documento recém-finalizado.
10. **NDF-PROD-010 — DEVE** persistir `payload_bytes` e o envelope de forma atómica — nenhuma escrita parcial ou inconsistente entre os dois deve ficar visível a um leitor (§5.2, passo 8). Não inclui o Perfil de Ciclo de Vida NORMORDIS — ver §9.5.
11. **NDF-PROD-011 — DEVE** produzir saídas aceites pelo validador e pelas verificações semânticas oficiais; os casos válidos são referências de interoperabilidade, não entradas do produtor. todos os casos de `conformance/ndf/valid/` sem erro.
12. **NDF-PROD-012 — DEVE**, quando `relacoes` estiver presente, incluir em cada elemento `tipo`, `alvo.ndf_id` e `alvo.payload_hash` (§2.11).
13. **NDF-PROD-013 — DEVE** incluir `intervencoes` com pelo menos um elemento quando `proveniencia_ia.utilizada` for `true`, e omitir ou esvaziar `intervencoes` quando for `false` (§2.13).
14. **NDF-PROD-014 — DEVE** incluir `revisao_humana.estado` em cada elemento de `proveniencia_ia.intervencoes`, e `revisor_ref`+`revisto_em` quando o estado for terminal (§2.13.3).
15. **NDF-PROD-015 — DEVE** declarar pelo menos uma origem identificável do conteúdo: `participantes` com pelo menos uma entrada de papel `autor`, `coautor` ou `decisor`; ou `proveniencia_sistema` não vazio; ou `proveniencia_ia.utilizada: true` (§2.2.1).
16. **NDF-PROD-016 — DEVE** ordenar as entradas de `proveniencia_sistema` cronologicamente, por `gerado_em` não decrescente (§2.14.3).
17. **NDF-PROD-017 — DEVE**, quando `imputacao` estiver presente, incluir em cada elemento `imputado.designacao` e `titulo`, e satisfazer as condicionais do título: `fundamento.publicacao_ref` para `delegacao` e `subdelegacao`, `em` para `aceitacao_expressa`, `fundamento.descricao` para `efeito_legal` (§2.15.2).
18. **NDF-PROD-018 — DEVE**, quando `metadados.tipo_documento_ref` usar uma extensão qualificada `ext.<entidade>.<tipo>@<versao>`, incluir o schema correspondente em `schemas/<tipo_id>.schema.json` no `.ndfpkg` (§2.9.5, §8.1).
19. **NDF-PROD-019 — NÃO DEVE** declarar em `proveniencia_sistema` qualquer componente não determinístico; tais componentes pertencem a `proveniencia_ia` (§2.14.4).
20. **NDF-PROD-020 — NÃO DEVE** reescrever, recomprimir ou reserializar os bytes de um componente binário declarado em `documento`, nem alterá-los para os harmonizar com os campos descritivos; os componentes preservam-se tal como emitidos ou recebidos (§2.8.1, §2.8.2, §4.5.1).
21. **NDF-PROD-021 — NÃO DEVE** incluir numa declaração de componente qualquer localização de armazenamento — URI, *bucket*, caminho dentro do pacote ou nome de adaptador (§2.8.1).
22. **NDF-PROD-022 — NÃO DEVE** derivar `nivel_assinatura` de assinaturas contidas em componentes binários; o campo descreve a assinatura do NDF (§2.10, §4.5.1).
23. **NDF-PROD-023 — NÃO DEVE** declarar `metadados.origem_nao_identificavel` em conjunto com `participantes` contendo `papel` em `autor`, `coautor` ou `decisor`, ou com `proveniencia_sistema` não vazio; e **DEVE** preencher `fundamento` com a razão concreta pela qual a origem não é apurável (§2.2.1, §2.7.6).

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
14. **NDF-READ-014 — DEVE** rejeitar um NDF que não declare nenhuma origem do conteúdo nos termos de §2.2.1.
15. **NDF-READ-015 — DEVE** rejeitar uma entrada de `imputacao` com `titulo` `delegacao` ou `subdelegacao` sem `fundamento.publicacao_ref`, com `aceitacao_expressa` sem `em`, ou com `efeito_legal` sem `fundamento.descricao` (§2.15.2).
16. **NDF-READ-016 — DEVE** rejeitar `proveniencia_sistema` cujas entradas não estejam ordenadas por `gerado_em` não decrescente (§2.14.3).
17. **NDF-READ-017 — NÃO DEVE** aceitar como determinística uma entrada de `proveniencia_sistema` que declare um componente não determinístico; tais componentes pertencem a `proveniencia_ia` (§2.14.4).
18. **NDF-READ-018 — DEVE**, quando não conseguir resolver o schema referenciado por `metadados.tipo_documento_ref`, rejeitar o documento **ou** tratar `documento` como opaco, sem declarar interpretação completa; e **NÃO DEVE**, em caso algum, declarar `documento` validado sem o ter validado (§2.9.5). Em contexto de pacote, a ausência do schema de um tipo de extensão é falta de conformidade do pacote — ver §9.3.
19. **NDF-READ-019 — NÃO DEVE** interpretar a ausência de entradas em `participantes` como prova de ausência de intervenção de terceiros (§2.12.5).
20. **NDF-READ-020 — NÃO DEVE** derivar de `imputacao[].autenticacao.nivel_garantia` qualquer gradação da imputação, presunção ilidível ou tratamento diferenciado do documento; o campo descreve o mecanismo de autenticação, não a força da imputação (§2.15.4).
21. **NDF-READ-021 — NÃO DEVE** apresentar a projeção do NDT de um documento com componentes binários como sendo o documento; o NDT desse documento descreve a captura, e o conteúdo do ato obtém-se resolvendo o componente (§2.8.1, §2.8.2).
22. **NDF-READ-022 — NÃO DEVE** apresentar uma assinatura contida num componente como assinatura do NDF, nem inferir dela o `nivel_assinatura` (§4.5.1).
23. **NDF-READ-023 — DEVE** resolver um componente declarado em `documento` pelo seu digest, e **NÃO DEVE** resolvê-lo pelo nome de origem declarado, que é descritivo (§2.8.1).
24. **NDF-READ-024 — NÃO DEVE** interpretar `metadados.origem_nao_identificavel` como ausência de entidade produtora ou de responsável pela custódia, que continuam obrigatórios; o bloco declara apenas que a origem do conteúdo não é apurável (§2.7.6).

### 9.3 Pacote conforme (`.ndfpkg`)

Um arquivo `.ndfpkg` é conforme se satisfizer todos os seguintes requisitos:

1. **NDF-PKG-001 — DEVE** ser um arquivo ZIP válido.
2. **NDF-PKG-002 — DEVE** conter `manifest.json`, `ndf-core.json` e `envelope.json` na raiz do arquivo.
3. **NDF-PKG-003** — `manifest.json` **DEVE** incluir inventário com `hash_sha256` de cada ficheiro e os campos obrigatórios definidos em §8.2.
4. **NDF-PKG-004** — `SHA-256(ndf-core.json)` **DEVE** coincidir com `manifest.inventario[ndf-core.json].hash_sha256`.
5. **NDF-PKG-005** — `ndf-core.json` **DEVE** ser um NDF-core conforme (§9.1).
6. **NDF-PKG-006** — O NDT referenciado por `ndt_version_ref` **DEVE** estar presente em `ndt/<schema_id>@<versao>.ndt.json`.
7. **NDF-PKG-007** — O schema do tipo referenciado por `metadados.tipo_documento_ref` **DEVE** ser resolúvel a partir do pacote em `schemas/<tipo_id>.schema.json` quando o tipo for uma extensão qualificada (§2.9.5); um verificador **DEVE** resolver o schema do tipo preferencialmente a partir do pacote, recorrendo ao registo canónico apenas quando o pacote não o contiver.
8. **NDF-PKG-008** — O schema do perfil referenciado por `avaliacao.perfil` **DEVE** estar presente em `schemas/<perfil>.schema.json` (§3.2.3, §8.1), e o bloco `avaliacao` **DEVE** validar contra ele; um verificador **DEVE** resolvê-lo preferencialmente a partir do pacote.
9. **NDF-PKG-009** — A correspondência entre componentes declarados e ficheiros do pacote **DEVE** fechar nos dois sentidos. Cada componente declarado em `documento` nos termos de §2.8.1 **DEVE** ter, em `manifest.inventario`, uma entrada cujo `hash_sha256` coincida com o seu digest, e o ficheiro correspondente **DEVE** estar presente. Inversamente, cada ficheiro contido em `original/`, `representacoes/`, `anexos/` ou `evidencias/` (§8.1) **DEVE** corresponder a um componente declarado. Um pacote que declare um componente ausente, cujo digest não coincida com os bytes presentes, ou que transporte num destes diretórios um ficheiro não declarado, **NÃO É** conforme.

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

#### 9.4.1 Rejeição pelo motivo certo

Rejeitar um caso inválido não basta: um caso rejeitado por um defeito acidental
— um identificador malformado, um campo obrigatório em falta — é
indistinguível, para um runner que compare apenas aceite/rejeitado, de um caso
que exerça a regra que documenta. Um caso nessas condições não testa nada, e
continua a passar mesmo que a regra que devia cobrir seja removida da
especificação.

Por isso, cada ficheiro de `invalid/` declara `_expected_match`: uma expressão
regular — ou lista de expressões — que **DEVE** encontrar correspondência em
pelo menos um dos erros reportados. O runner de referência trata como falha
tanto a ausência do campo como a ausência de correspondência, mesmo quando o
caso é corretamente rejeitado.

Uma implementação alternativa não é obrigada a reproduzir as mensagens do
runner de referência, e portanto não é obrigada a satisfazer estes padrões. É
obrigada a rejeitar os casos, e **RECOMENDA-SE** que verifique, por meio
equivalente, a correspondência entre a rejeição e a violação documentada em
`_expected_error`.

**Nota**: os ficheiros de conformidade contêm campos `_comment`,
`_expected_error` e `_expected_match` prefixados com `_` para documentação e
verificação internas. Estes campos **NÃO DEVEM** constar do NDF-core produzido
por uma implementação — o test runner remove-os automaticamente antes de
validar.

### 9.5 Perfil de Ciclo de Vida NORMORDIS (opcional)

Este perfil **NÃO É** requisito de conformidade NDF (§9.1–§9.3). Cobre o
modelo de referência descrito em §2.4.1–§2.4.3 para sistemas que gerem NDF
depois da finalização. Um produtor ou leitor NDF conforme PODE optar por
não o implementar, adotando o seu próprio modelo de gestão de ciclo de
vida — ver ADR-010.

1. **CUST-REQ-001 — DEVE** registar cada transição de estado (§2.4.1) num log de auditoria imutável, validando cada entrada contra `custody-event.schema.json` e mantendo a cadeia de hash encadeado (§2.4.2).
2. **CUST-REQ-002 — DEVE** usar armazenamento append-only ou WORM para `payload_bytes`, envelope e log de custódia.
3. **CUST-REQ-003 — DEVE** registar o evento terminal de eliminação (§2.4.3) antes de destruir `payload_bytes` **e todos os componentes binários declarados em `documento`** (§2.8.1) de um documento elegível para eliminação, conservando `validation_code`, `payload_hash` e os digests dos componentes destruídos em `details`.
4. **CUST-REQ-004 — DEVE**, ao transferir evidência de custódia para outra entidade, transferir eventos íntegros e não editados, e **NÃO DEVE** reescrever, renumerar ou recompor a cadeia para ocultar as omissões (§2.4.4).

Ferramenta de referência: `tools/check_custody.py`; vetores em
`conformance/custody/`.

---

## Anexo A (informativo) — Glossário

| Termo | Significado |
|---|---|
| NDF | NORMORDIS Document Format — o formato e o seu modelo documental, no seu conjunto |
| NDF-core | Fonte de verdade documental: o objeto JSON canonicalizado e assinado (§2) |
| Envelope | Assinaturas, timestamps e material de validação, associados ao NDF-core mas não abrangidos pela assinatura (§4) |
| artefacto NDF assinado | NDF-core + Envelope — a unidade mínima verificável (§1.2) |
| pacote NDF (`.ndfpkg`) | NDF-core + Envelope + NDT + schemas + recursos — a unidade mínima autossuficiente (§8) |
| NDT | NORMORDIS Document Template — estrutura/layout para reprodução visual |
| perfil de avaliação | Identificador do regime arquivístico aplicável, declarado em `avaliacao.perfil` (§3.2.3) |
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
