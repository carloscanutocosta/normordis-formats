# MANUAL — Formatos NORMORDIS

**Âmbito deste manual:** NDF 1.0.0, NDT 2.0.0, NCRTF 2.0.0 e os artefactos
associados (envelope, `.ndfpkg`, registo de tipos e perfis, log de custódia,
conjunto de transferência, portal de verificação).

**Natureza deste documento:** manual **informativo**. Explica o propósito, o
conteúdo, os limites, a estrutura e o uso de cada formato. Não substitui nem
altera o texto normativo — em caso de divergência prevalecem
[`specs/ndf/SPEC.md`](specs/ndf/SPEC.md),
[`specs/ndt/SPEC.md`](specs/ndt/SPEC.md) e
[`specs/ncrtf/SPEC.md`](specs/ncrtf/SPEC.md).

**Estado das especificações:** Draft — revisão pública por abrir (nível 1 de
[`NORMALIZATION.md`](NORMALIZATION.md)). Estado interno ao projeto; não
representa aprovação, homologação ou publicação por IPQ, CEN, ISO, IEC ou
outra entidade normalizadora. Nenhum período de revisão pública está aberto.

---

## Índice

| Secção | Conteúdo |
|---|---|
| [§1](#1-visão-de-conjunto) | Visão de conjunto — que formatos existem e como se articulam |
| [§2](#2-conceitos-transversais) | Conceitos transversais — canonicalização, integridade, perfis, versões |
| [§3](#3-ndf--normordis-document-format) | NDF — instância documental canónica |
| [§4](#4-envelope-de-integridade-e-autenticidade) | Envelope — assinaturas, selos, timestamps, `validation_code` |
| [§5](#5-ndfpkg--pacote-portátil) | `.ndfpkg` — pacote de exportação autocontido |
| [§6](#6-ndt--normordis-document-template) | NDT — template declarativo de apresentação |
| [§7](#7-ncrtf--normordis-canonical-rich-text-format) | NCRTF — conteúdo de texto rico canónico |
| [§8](#8-registo-de-tipos-e-perfis) | Registo — schemas de tipo documental e perfis de avaliação |
| [§9](#9-custódia-transferência-e-verificação-pública) | Custódia, transferência entre entidades e portal |
| [§10](#10-produzir-e-verificar-na-prática) | Pipelines de finalização e de verificação |
| [§11](#11-conformidade-e-ferramentas) | Papéis de conformidade, suites e comandos |
| [Anexo A](#anexo-a--glossário-consolidado) | Glossário consolidado |
| [Anexo B](#anexo-b--mapa-de-ficheiros-do-repositório) | Mapa de ficheiros do repositório |

---

## 1. Visão de conjunto

### 1.1 O princípio

**A fonte de verdade reside nos dados; o PDF é uma projeção desses dados.**

Um documento institucional não é um ficheiro de apresentação com metadados
colados. É um objeto lógico — conteúdo, metadados, avaliação arquivística,
proveniência, imputação — de que o PDF, o ODF ou o HTML são representações.
Os formatos NORMORDIS separam esse objeto lógico (NDF), o seu texto rico
(NCRTF) e a sua apresentação (NDT).

### 1.2 Os três formatos

| Formato | Nome | Versão | O que é |
|---|---|---|---|
| **NDF** | NORMORDIS Document Format | 1.0.0 | Instância documental canónica e imutável — os dados, os metadados e a prova |
| **NDT** | NORMORDIS Document Template | 2.0.0 | Template declarativo de apresentação — como o documento se compõe visualmente |
| **NCRTF** | NORMORDIS Canonical Rich Text Format | 2.0.0 | Texto rico canónico — o conteúdo textual estruturado, embebido no NDF |

### 1.3 Como se articulam

```text
editor ──► NCRTF ──┐
                   ├──► NDF-core ──┐
dados/metadados ───┘               ├──► renderizador ──► PDF / ODF / HTML / …
                                   │
NDT + recursos ────────────────────┘

NDF-core + envelope + NDT + schemas + recursos ──► .ndfpkg
```

Leitura do diagrama:

1. O **NCRTF** não é um ficheiro autónomo: é um **valor JSON** guardado dentro
   de um campo do bloco `documento` do NDF-core (tipicamente `corpo`).
2. O **NDF-core** é o objeto canonicalizado e assinado. Contém o NCRTF, mas
   não contém o NDT.
3. O **NDT** é referenciado pelo NDF-core (`ndt_version_ref`), nunca embebido
   nele — porque não faz parte dos bytes assinados.
4. O **renderizador** é o único componente que conhece os dois: lê o NDF,
   resolve o NDT, e produz a saída.
5. O **`.ndfpkg`** reúne tudo num ZIP autocontido, para transferência,
   verificação independente e preservação.

### 1.4 Duas unidades com nome próprio

```text
artefacto NDF assinado  = NDF-core + Envelope
pacote NDF (.ndfpkg)    = NDF-core + Envelope + NDT + schemas + recursos
```

- O **artefacto NDF assinado** é a *unidade mínima verificável*: tem tudo o que
  é preciso para provar integridade e, havendo assinatura, autoria.
- O **pacote NDF** é a *unidade mínima autossuficiente*: tem, além disso, tudo
  o que é preciso para interpretar e reproduzir o documento sem qualquer
  serviço externo.

Evite a expressão «NDF completo» — é ambígua entre as duas.

### 1.5 Dever do formato e responsabilidade do produtor

Esta é a linha divisória que explica a maior parte das decisões de desenho:

| | Dever de quem |
|---|---|
| **Capacidade de representação** — existir lugar para tudo o que é relevante e necessário | **do formato** |
| **Correção do que se representa** — que o declarado seja verdadeiro, competente, completo e legal | **do produtor** |

O critério é operacional: *um verificador consegue decidir isto tendo apenas o
pacote em mãos?* Se sim, pode ser conformidade. Se exige o mundo — a lei, a
orgânica, o procedimento, os factos —, é do produtor.

Consequência prática: **um `.ndfpkg` válido garante integridade, identidade e
interpretabilidade — não legalidade, completude nem correção.** Um produtor
pode emitir um documento juridicamente incompleto e o NDF ser válido: o ato
existe, e a sua validade é decidida pelas autoridades competentes, como sucede
com um documento em papel.

### 1.6 Quem faz o quê

| Papel | Responsabilidade |
|---|---|
| **Produtor** | Cria NDF-core conforme, canonicaliza, calcula hash e `validation_code`, assina quando aplicável, persiste atomicamente |
| **Leitor** | Valida contra o schema da versão declarada, verifica hash, rejeita o que não suporta em vez de o interpretar em silêncio |
| **Renderizador** | Combina NDF + NDT e produz PDF/ODF/HTML; verifica estrutura e referências, mas **não aplica regras de negócio** |
| **Verificador** | Percorre a ordem de verificação (§10.2) e devolve estados separados de integridade, autenticidade e assinatura |
| **Custodiante** | Guarda, protege, audita e transfere; opcionalmente implementa o Perfil de Ciclo de Vida (§9) |

Conformidade num papel não implica conformidade noutro.

---

## 2. Conceitos transversais

### 2.1 JSON, não XML — e JSON canonicalizado

Todos os formatos são JSON (RFC 8259). A canonicalização é **JCS — JSON
Canonicalization Scheme, RFC 8785, estrito**: a mesma estrutura lógica produz
sempre os mesmos bytes, independentemente da ordem de inserção de chaves ou da
formatação de origem.

JCS garante:

- chaves de objeto ordenadas por *code point* Unicode;
- sem espaço em branco supérfluo;
- números em forma canónica;
- strings UTF-8 com escapes mínimos;
- **ordem dos arrays preservada** — o que torna a ordem de um array parte do
  hash, e por isso normativa onde existe (ver `proveniencia_sistema`, §3.13).

Consequência para quem implementa: nunca reserializar bytes já assinados. Os
`payload_bytes` guardam-se tal como foram produzidos.

### 2.2 Integridade, imutabilidade e autenticidade não são sinónimos

| Conceito | O que significa | Como se obtém |
|---|---|---|
| **Integridade** | Uma alteração dos bytes canónicos é detetável | JCS + `payload_hash` SHA-256 — **sempre**, em qualquer NDF |
| **Imutabilidade de custódia** | O sistema impede substituição silenciosa e regista o que sucede depois da finalização | Armazenamento append-only/WORM + log de auditoria — **Perfil de Ciclo de Vida, opcional** |
| **Autenticidade** | A identidade ou autoridade do emissor pode ser validada contra uma âncora de confiança | Assinatura ou selo CAdES verificável, ou custodiante confiável |
| **Assinatura qualificada** | Nível jurídico específico (eIDAS Art.º 25.º) | Certificado qualificado emitido por PSSC da lista de confiança |

Aviso recorrente e importante: **um hash sem âncora de custódia** permite
detetar alterações face a uma cópia conhecida, mas não impede que um atacante
substitua simultaneamente conteúdo e hash.

Sem assinatura ou selo válido, o resultado de uma verificação deve ser descrito
como **«íntegro sob a custódia avaliada»** — nunca como «autenticamente emitido
por uma identidade criptograficamente comprovada».

### 2.3 Perfis de assinatura

CAdES **não** é obrigatório para todos os documentos:

| Perfil | Requisito | Uso típico |
|---|---|---|
| `integridade` | JCS + hash (formato) + custódia append-only/WORM + auditoria (perfil opcional) | Registos internos sem ato assinável |
| `selo_institucional` | `integridade` + selo eletrónico CAdES da entidade | Prova portátil de origem e integridade institucional |
| `assinatura_avancada` | `integridade` + assinatura CAdES avançada | Atos que exigem identificação do signatário |
| `assinatura_qualificada` | `integridade` + assinatura CAdES qualificada | Atos para os quais a lei exige assinatura qualificada |

O campo `nivel_assinatura` do NDF-core declara o requisito de **assinatura
pessoal** (`nenhuma`, `avancada`, `qualificada`). Um documento com
`nivel_assinatura: "nenhuma"` pode receber selo institucional; o selo não o
transforma numa assinatura pessoal.

### 2.4 Duas representações conformes do mesmo documento

| Perfil | O que é | Otimiza |
|---|---|---|
| **Perfil de custódia** | NDF-core canónico + envelope em base de dados; NDT, schemas, certificados e recursos deduplicados por hash dentro do domínio de custódia | Persistência, indexação, deduplicação |
| **Perfil portátil** | `.ndfpkg` sem dependências externas, com todos os objetos materializados e inventariados por hash | Transferência, verificação, preservação independente |

Ambos representam o mesmo documento lógico. Um sistema conforme **deve** poder
exportar o primeiro para o segundo sem perda semântica. A deduplicação é uma
otimização física e nunca altera o modelo lógico.

### 2.5 Versionamento

Todas as especificações seguem SemVer 2.0.0.

| Componente | Muda quando | Efeito em leitores |
|---|---|---|
| `MAJOR` | Remoção/renomeação de campos obrigatórios, alteração de semântica, mudança de algoritmo de canonicalização | Leitores antigos recusam processar |
| `MINOR` | Adição compatível de campos ou blocos opcionais | Requer o schema da nova versão; leitores antigos podem tratar como opaco, mas **não ignoram** conteúdo assinado desconhecido |
| `PATCH` | Clarificações sem impacto comportamental | Sem impacto |

Distinção essencial, fonte frequente de confusão:

| Campo | O que versiona | Exemplo |
|---|---|---|
| `ndf_version`, `ndt_version`, `ncrtf_version` | A **especificação do formato** | `"1.0.0"`, `"2.0.0"` |
| `versao_ndt` | A **instância do template** — pode mudar anualmente | `"2026.1"` |
| `tipo_documento_ref` | O **schema do tipo documental** no registo | `"oficio@1.0.0"`, `"modelo3-irs@2026.1"` |

Uma campanha fiscal nova (`modelo3-irs@2027`) é versão nova no registo, **não**
uma versão nova de NDF ou de NDT.

### 2.6 Ritmos de alteração — porque as camadas estão separadas

| Camada | Altera-se quando | Ritmo típico |
|---|---|---|
| Regras materiais — **fora do NDF** | A lei altera taxas, deduções, prazos, condições | Frequente, por vezes intra-anual |
| Schema do tipo (registo) | A **estrutura** do documento muda: campo novo no impresso | Ocasional |
| NDT | O grafismo ou o layout muda | Ocasional, independente do anterior |
| NDF | O **formato de documento** muda | Raro — escala de décadas |

Uma alteração legislativa atinge, na esmagadora maioria dos casos, apenas a
primeira linha. É por isso que os schemas de tipo **não devem** codificar
regras materiais de negócio: um documento finalizado em 2026 tem de continuar
validável em 2046, e validar conformidade estrutural não é apreciar legalidade
material.

### 2.7 Extensões qualificadas

Onde o vocabulário canónico é fechado mas o domínio é aberto, existe um
mecanismo uniforme de extensão por entidade:

| Onde | Forma | Exemplo |
|---|---|---|
| `metadados.tipo_documento_ref` | `ext.<entidade>.<tipo>@<versao>` | `ext.at.liquidacao-irs@2026.1` |
| `relacoes[].tipo` | `ext.<entidade>.<tipo>` | `ext.at.retificacao-oficiosa` |

Regras comuns: `<entidade>` e `<tipo>` em minúsculas (`[a-z][a-z0-9-]*`); não
há registo central; o *namespace* é autodeclarado; a semântica é da
responsabilidade exclusiva de quem a declara.

Tratamento distinto, e deliberadamente assimétrico:

| Caso | Comportamento do leitor |
|---|---|
| **Relação** de tipo desconhecido | Trata como semanticamente desconhecida, mas **não rejeita** o documento — a relação continua verificável por hash |
| **Tipo documental** não resolúvel dentro de um `.ndfpkg` | Pacote **não conforme** — falhou a promessa de autocontenção |
| **Tipo documental** não resolúvel fora de pacote | Rejeitar **ou** tratar `documento` como opaco; nunca declarar validado o que não foi validado |

Tolerância semântica num caso, exigência estrutural no outro.

### 2.8 Referências externas não resolvidas pelo NDF

Vários campos são, por desenho, **referências opacas** que o NDF regista mas
não resolve — a resolução pertence ao sistema produtor:

`participantes[].participante_ref`, `imputacao[].imputado.ref`,
`avaliacao.classificacao_ref`, `avaliacao.instrumento_ref`,
`proveniencia_sistema[].regra_ref` / `build_ref` / `configuracao_ref`,
`proveniencia_ia.intervencoes[].evidencia_ref`,
`participantes[].qualificacao.identificador`,
`protecao_dados.base_legal_conservacao.fundamento_ref`.

O padrão comum de referência com prova é `{ tipo, identificador, hash }`.

### 2.9 A ausência não é uma afirmação

Regra transversal, aplicada de forma consistente:

- `contem_dados_pessoais: false` é **declaração**, não silêncio — por isso é
  obrigatório mesmo quando falso.
- `estado: "ativo"` tem um único valor admissível e ainda assim é obrigatório,
  pela mesma razão.
- `proveniencia_ia.utilizada: false` declara que não houve IA.
- `revisao_humana.estado: "pendente"` torna a ausência de revisão **visível**.
- A **omissão** de `classificacao_seguranca` significa «não declarada», e não
  um nível por omissão.
- A **omissão** de `idiomas_autenticos` significa «a questão não se coloca», e
  não «documento monolingue em direito».
- `participantes` vazio é **silêncio, não negação**: não prova ausência de
  intervenção de terceiros.

---

## 3. NDF — NORMORDIS Document Format

**Especificação:** [`specs/ndf/SPEC.md`](specs/ndf/SPEC.md) · **Schema:**
[`specs/ndf/schemas/ndf-core.schema.json`](specs/ndf/schemas/ndf-core.schema.json)

### 3.1 Propósito

O NDF define uma representação canónica para **armazenamento e intercâmbio de
documentos institucionais estruturados**. Os seus mecanismos servem cinco
objetivos:

1. **Armazenamento imutável, autocontido e eficiente** — bytes canónicos e
   conteúdo estruturado adequados a persistência e indexação em base de dados.
2. **Interoperabilidade** — qualquer sistema conforme produz, transfere,
   interpreta, verifica e renderiza o mesmo documento sem depender do
   fornecedor, linguagem, runtime ou base de dados de origem.
3. **Integridade, autenticidade e suporte a assinaturas eletrónicas** —
   canonicalização, hash, código de verificação e envelope CAdES.
4. **Reprodutibilidade visual** — em combinação com o NDT, para PDF/UA-2 (alvo
   primário), ODF e HTML.
5. **Apoio à gestão arquivística e à proteção de dados** — avaliação
   arquivística obrigatória, metadados de minimização, base legal e
   conservação.

### 3.2 O que o NDF contém

| Bloco | Contém |
|---|---|
| Identidade | `ndf_version`, `ndf_id`, `estado`, `payload_hash_alg` |
| Ligação à apresentação | `ndt_version_ref` |
| Nível de assinatura declarado | `nivel_assinatura` |
| Metadados descritivos | `metadados` — tipo, entidades, assunto, referências, idioma, classificação de segurança, proteção de dados |
| Conteúdo lógico | `documento` — estrutura definida pelo schema do tipo; inclui valores NCRTF e declarações de componentes binários |
| Avaliação arquivística | `avaliacao` — perfil, classificação, prazo de conservação, destino final, instrumento |
| Relações documentais | `relacoes[]` — ligações verificáveis por hash a outros NDF |
| Origem do conteúdo | `participantes[]` (pessoas), `proveniencia_sistema[]` (sistemas determinísticos), `proveniencia_ia` (sistemas não determinísticos) |
| Responsabilidade jurídica | `imputacao[]` |
| Prova (fora do core) | Envelope — assinaturas, timestamps, material de validação, `validation_code` |

### 3.3 O que o NDF **não** contém

| Não contém | Onde vive |
|---|---|
| **Bytes binários embutidos** — nem base64, nem data URL | Componentes referenciados por digest; ficheiros no `.ndfpkg` ou no domínio de custódia |
| **Layout, margens, tipografia, posições** | NDT |
| **Regras de validação material ou de cálculo** | Sistema produtor — nunca no schema do tipo |
| **A assinatura, dentro dos bytes assinados** | Envelope (evita circularidade) |
| **`validation_code`** | Envelope — depende do hash, logo não pode ser conteúdo |
| **O NDT** | Referenciado por `ndt_version_ref`; incluído no `.ndfpkg`, não no core |
| **Estado corrente do ciclo de vida** | Base de dados operacional e `manifest.estado`; o `estado` do core é o do momento da finalização |
| **Data de elegibilidade para destino final** | Derivada e recalculável, fora do core |
| **Log de acessos, prompts de IA, traces, SBOM, configuração operacional** | Sistemas próprios, ligados por referência com hash |
| **Cifra ou controlo de acesso** | Sistema de custódia — o NDF sinaliza sensibilidade, não a impõe (SPEC NDF §4.7) |
| **Envelope cifrado normativo, algoritmo de cifra, gestão de chaves** | Provedor de armazenamento ou base de dados do custodiante — nenhum campo do NDF-core ou do envelope depende da cifra aplicada (SPEC NDF §4.7.1) |
| **Um «modo classificado»** | Não existe nem é necessário: documentos classificados tratam-se por topologia do sistema de custódia, com o mesmo NDF-core, pipeline e envelope (SPEC NDF §4.7.2) |
| **Mecanismo de workflow — quórum, sequência de aprovação, estado processual** | GED/GCA do produtor |
| **`NaN`, `Infinity`, chaves duplicadas** | Proibidos por JSON estrito e por JCS |

### 3.4 Estrutura de topo

```json
{
  "ndf_version": "1.0.0",
  "ndf_id": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
  "estado": "ativo",
  "payload_hash_alg": "sha256",
  "nivel_assinatura": "qualificada",
  "ndt_version_ref": "oficio-generico@2.0.0",
  "metadados": { },
  "documento": { },
  "avaliacao": { },
  "relacoes": [ ],
  "participantes": [ ],
  "proveniencia_ia": { },
  "proveniencia_sistema": [ ],
  "imputacao": [ ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `ndf_version` | Sim | Versão da especificação. Valor desta versão: `"1.0.0"` |
| `ndf_id` | Sim | UUID v4 (RFC 9562), gerado antes da canonicalização, imutável |
| `estado` | Sim | Estado no momento da finalização. Enum de um só valor: `"ativo"` |
| `payload_hash_alg` | Sim | Algoritmo do digest. Valor desta versão: `"sha256"` |
| `nivel_assinatura` | Sim | `"nenhuma"` \| `"avancada"` \| `"qualificada"` |
| `ndt_version_ref` | Sim | `"<schema_id>@<versao_ndt>"` |
| `metadados` | Sim | Ver §3.7 |
| `documento` | Sim | Conteúdo lógico; estrutura definida por `metadados.tipo_documento_ref` |
| `avaliacao` | Sim | Ver §3.10 |
| `relacoes` | Não | Ver §3.11 |
| `participantes` | Não | Ver §3.12 |
| `proveniencia_ia` | Não | Ver §3.14 |
| `proveniencia_sistema` | Não | Ver §3.13 |
| `imputacao` | Não | Ver §3.15 |

A finalização **falha** se faltar qualquer campo obrigatório. Os cinco campos
opcionais, quando presentes, entram nos bytes canonicalizados e assinados como
os restantes.

### 3.5 O invariante de origem

Os campos opcionais são individualmente opcionais, mas **não em conjunto**.
Todo o NDF deve declarar pelo menos uma origem identificável do conteúdo, por
um de quatro modos:

| Modo | Como se declara |
|---|---|
| Humana | `participantes[]` com pelo menos uma entrada de `papel` em `autor`, `coautor` ou `decisor` |
| De sistema | `proveniencia_sistema` presente e não vazio |
| De IA | `proveniencia_ia.utilizada: true` |
| Não apurável | `metadados.origem_nao_identificavel` com `fundamento` |

Um NDF que não declare nenhuma destas origens **é rejeitado**. A regra é
expressa no JSON Schema por `anyOf`, pelo que qualquer validador Draft 2020-12
a aplica sem código adicional.

Notas de leitura:

- `revisor_humano`, `representante` e `responsavel_tecnico` **não** satisfazem
  o invariante: rever, representar ou responder tecnicamente não é produzir.
- O invariante não obriga a inventar informação: um documento produzido por um
  sistema sem qualquer intervenção humana declara `proveniencia_sistema` e
  nada mais.
- O quarto modo existe para os documentos que entram em custódia sem origem
  apurável — papel digitalizado sem menção de autor, denúncia anónima, ficheiro
  de terceiro sem identificação. Recusá-los ou fabricar-lhes um autor seriam as
  duas alternativas, e ambas piores.

### 3.6 Imutabilidade

O NDF-core é **congelado no momento da finalização**. A partir daí:

- os bytes canonicalizados nunca são reserializados, reordenados ou alterados;
- não existe «edição» de um NDF finalizado;
- qualquer alteração ao conteúdo lógico origina um **novo NDF**, distinto e
  igualmente imutável, ligado ao anterior por `relacoes[]`.

### 3.7 `metadados`

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
    "assunto": "Resposta ao ofício n.º 45/2026",
    "numero_referencia": "OF/2026/00123",
    "processo_ref": "proc.º 456/2026",
    "idioma": "pt-PT",
    "classificacao_seguranca": { "perfil": "pt", "nivel": "uso_interno" },
    "contem_dados_pessoais": false
  }
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `tipo_documento_ref` | Sim | `"<id>@<versao>"` ou `"ext.<entidade>.<tipo>@<versao>"`. Define a estrutura de `documento` |
| `entidade_produtora` | Sim | Objeto `{designacao, identificadores[]}`. A **pessoa coletiva** cuja produção documental é objeto de avaliação |
| `entidade_responsavel` | Sim | Designação de quem custodia o registo. Obrigatório sempre |
| `assunto` | Recomendado | Título ou descrição breve — indexável |
| `numero_referencia` | Recomendado | Número de referência documental |
| `processo_ref` | Opcional | Processo ou procedimento a que pertence |
| `idioma` | Opcional | Subconjunto `língua[-escrita][-região]` do BCP 47. Omitido, assume-se `"pt"` |
| `idiomas_autenticos` | Não | Línguas com **igual força jurídica**. Ver abaixo |
| `classificacao_seguranca` | Recomendado | `{perfil, nivel}`. A omissão significa **não declarada** |
| `contem_dados_pessoais` | Sim | `true` \| `false` |
| `protecao_dados` | Condicional | Obrigatório se `contem_dados_pessoais: true`; **proibido** caso contrário |
| `origem_nao_identificavel` | Não | `{fundamento}` — quarto modo do invariante de origem |

#### `entidade_produtora.identificadores`

Cada identificador é um par `{sistema, valor}`, em que `sistema` é um
identificador opaco qualificado de dois ou mais segmentos: `pt-nif`,
`pt-dglab`, `fr-siren`, `nl-kvk`, `eu-vat`, `eu-pic`. A validade do `valor`
face às regras do esquema — dígitos, dígito de controlo, formato — é do
esquema e do sistema produtor, não desta especificação.

Três entidades coexistem e são independentes:

| Campo | Responde à pergunta |
|---|---|
| `metadados.entidade_produtora` | Que organismo produziu, para efeitos arquivísticos? |
| `metadados.entidade_responsavel` | Quem custodia o registo? |
| `imputacao[].imputado` | Que órgão ou pessoa responde juridicamente pelo ato? |
| `proveniencia_sistema[].sistema` | Que sistema produziu materialmente o conteúdo? |

Exemplo: uma liquidação automática tem `entidade_produtora` «Autoridade
Tributária e Aduaneira», `imputacao[].imputado` o órgão com competência para o
ato, e `proveniencia_sistema[].sistema` o motor de liquidação.

#### `classificacao_seguranca`

```json
{ "classificacao_seguranca": { "perfil": "pt", "nivel": "reservado" } }
```

- `perfil` — regime de classificação aplicável. Enum **aberto**: `"pt"`,
  `"eu"`, `"nato"`, …
- `nivel` — enum **fechado**, escala ordinal neutra: `publico`, `uso_interno`,
  `reservado`, `confidencial`, `secreto`, `muito_secreto`.

O vocabulário legal é do perfil; a **estrutura** — a escala ordinal — fica no
core. Isto permite a um leitor que desconheça o regime declarado ordenar
documentos por sensibilidade.

Limites que devem ser lidos com precisão:

- Ordenar `nivel` **não** é comparação objetiva entre regimes soberanos.
  `{"perfil":"eu","nivel":"reservado"}` e `{"perfil":"pt","nivel":"reservado"}`
  declaram o mesmo nível abstrato, não equivalência entre `RESTREINT UE` e o
  regime português.
- O campo é **descritivo**. Não é mecanismo de controlo de acesso, nem cifra,
  nem garantia de confidencialidade. A proteção efetiva — quem acede, cifra em
  repouso e em trânsito, gestão de chaves, auditoria — é do sistema de custódia.
- Cifra não é, isoladamente, controlo de acesso: protege contra furto de
  suporte e interceção, não garante que só quem tem direito legal consegue
  decifrar.
- **Não existe «modo classificado» do NDF.** O mesmo NDF-core, o mesmo pipeline
  de finalização e o mesmo envelope aplicam-se a qualquer nível declarado.
  Tratar documentos classificados é uma questão de **topologia do sistema de
  gestão documental** — custódia isolada ou *air-gapped*, TSA local acreditada,
  verificação não exposta —, nunca de modelação no formato (SPEC NDF §4.7.2).

#### `protecao_dados`

Obrigatório se e só se `contem_dados_pessoais: true`.

```json
{
  "protecao_dados": {
    "categorias": ["identificacao_fiscal", "dados_processuais"],
    "base_legal_conservacao": { "regime": "eu-gdpr", "base": "art6-1-c" },
    "responsavel_tratamento": "Direção-Geral de Exemplo"
  }
}
```

| Campo | Descrição |
|---|---|
| `categorias` | Pelo menos um valor. Enum aberto: `identificacao_fiscal`, `rendimentos`, `saude`, `dados_processuais`, `biometricos`, `outros` |
| `base_legal_conservacao` | Par `{regime, base}`, com `fundamento_ref` opcional |
| `responsavel_tratamento` | Identificador da entidade responsável pelo tratamento (RGPD, Art.º 13.º–14.º) |

**A base legal é declarada num regime, não escolhida de uma lista.** A
especificação **não enumera** as bases legais de nenhum regime: uma lista
fechada ficaria presa a um ordenamento — o RGPD — num formato que se quer
neutro quanto à jurisdição, e ficaria incompleta mesmo nesse ordenamento. Um
leitor **não deve** interpretar `base` sem conhecer o `regime`, nem inferir um
regime do silêncio.

Tensão imutabilidade ↔ direito ao apagamento, resolvida por três mecanismos:
base legal de conservação prevalente (obrigação legal e missão de interesse
público); pseudonimização **antes** da finalização, com a tabela de
correspondência gerida fora do NDF; e eliminação no termo do prazo de
conservação segundo a decisão arquivística aplicável.

#### `origem_nao_identificavel`

```json
{
  "metadados": {
    "origem_nao_identificavel": {
      "fundamento": "Documento em papel digitalizado, sem menção de autor nem de serviço emissor."
    }
  }
}
```

`fundamento` é obrigatório e sem valor por omissão — sem ele o bloco seria uma
via de fuga ao invariante. Regras:

- **Não pode** coexistir com `participantes` de papel `autor`/`coautor`/`decisor`
  nem com `proveniencia_sistema` não vazio. O schema rejeita a contradição.
- **Pode** coexistir com `proveniencia_ia`: a intervenção de IA num documento
  capturado é tipicamente assistência (classificação, extração, sumarização),
  não produção do conteúdo.
- **Não substitui** `entidade_produtora` nem `entidade_responsavel`, que
  continuam obrigatórios. Ter entidade produtora conhecida e autor não apurável
  é situação corrente, não contradição.

#### `idiomas_autenticos`

Só para documentos cujas versões linguísticas têm **a mesma força jurídica** —
legislação da União, tratados, atos de Estados plurilingues.

```json
{ "metadados": { "idioma": "pt-PT", "idiomas_autenticos": ["pt-PT", "en-GB"] } }
```

`idiomas_autenticos` deve conter o valor de `idioma`. Quando o bloco está
presente, `idioma` deixa de significar «a língua principal» e passa a
identificar apenas a versão que este NDF apresenta em primeiro lugar.

Uma tradução que **não** seja igualmente autêntica não se declara aqui — é
outro documento, com autor próprio, ligado por `relacoes[]`.

### 3.8 `documento` — conteúdo lógico

O NDF-core é um **envelope genérico**; `documento` é **tipado por schema
próprio**, referenciado em `metadados.tipo_documento_ref`. Isto permite que o
mesmo formato acomode, sem alterar a especificação:

- documentos administrativos correntes — ofícios, informações, despachos,
  pareceres: estrutura predominantemente textual;
- formulários fiscais/declarativos complexos — Modelo 3 de IRS: estrutura
  profundamente aninhada, com anexos, quadros e centenas de campos;
- qualquer tipologia futura, incluindo de outras administrações.

**Perfil «documento administrativo corrente»:**

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
        { "type": "paragraph", "content": [ { "type": "text", "text": "Texto do ofício…" } ] }
      ]
    },
    "referencias": ["proc.º 123/2026"]
  }
}
```

**Perfil «formulário complexo»:**

```json
{
  "documento": {
    "ano_fiscal": 2025,
    "sujeitos_passivos": [ { "nif": "…" } ],
    "anexos": { "anexo_a": { "quadros": { } }, "anexo_b": { "quadros": { } } },
    "totais_calculados": { }
  }
}
```

#### Porque o schema do tipo não é substituível pelo NDT

Pergunta natural: se a reconstrução depende de NDF **e** NDT, e o NDT já
declara que campos são apresentados, para que serve um schema de tipo à parte?

- **Reconstruir não é interpretar.** O NDT declara *onde imprimir* um valor; o
  schema do tipo declara *o que o valor é*. Um sistema de arquivo que indexe,
  pesquise ou migre daqui a décadas não passa pelo renderizador.
- **A independência é simétrica.** Sem schema de tipo, o documento renderiza-se
  mas não se valida; sem NDT, valida-se mas não se renderiza.
- **Fundir os dois acoplaria dados a apresentação** — alterar o grafismo
  passaria a ser alteração do modelo de dados.

Critério operacional: uma restrição pertence ao **NDT** quando a sua violação
significa «não cabe *neste* layout»; pertence ao **schema do tipo** quando
significa «o dado está mal formado».

Limite normativo: um schema de tipo restringe-se à **forma** dos dados — campos
presentes, tipos, formatos, cardinalidades. **Não deve** codificar regras
materiais de negócio.

### 3.9 Componentes binários

A proibição de bytes embutidos recai sobre **bytes**, não sobre a **referência**
a eles. Um schema de tipo pode declarar componentes binários por digest.

```json
{
  "documento": {
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

| Campo | Obrigatório | Descrição |
|---|---|---|
| `id` | Sim | Unívoco dentro do documento |
| `papel` | Sim | `original` \| `representacao_congelada` \| `anexo` \| `evidencia` |
| `derivado_de` | Condicional | `id` do componente de origem — obrigatório em `representacao_congelada` |
| `media_type` | Sim | MIME determinado por **inspeção do conteúdo**, nunca inferido da extensão |
| `sha256` | Sim | `"<alg>:<hex>"`. É a **identidade** do componente e a chave da sua resolução |
| `tamanho` | Sim | Bytes |
| `nome_original` | Não | Descritivo. **Não** é caminho no pacote e **não** serve para resolver o componente |
| `validacao_formato` | Não | `{norma, parte, nivel, resultado, validador{nome,versao}, verificado_em}` — registo, não juízo |

Regras essenciais:

- `componentes` é o mecanismo **único** de binários no NDF. Qualquer schema de
  tipo pode declará-lo; nenhum deve inventar vocabulário próprio para o mesmo
  fim (duas regras de fecho de pacote, só uma verificada).
- O digest entra nos `payload_bytes` e fica **coberto pela assinatura** — é por
  isso que a declaração vive em `documento` e não no manifesto, que não é
  assinado.
- Uma declaração de componente **não deve** conter localização de armazenamento
  — URI, *bucket*, caminho no pacote ou nome de adaptador.
- Os bytes de um componente **nunca** são reescritos, recomprimidos ou
  reserializados — destruiria qualquer assinatura contida.

#### Submeter não é produzir

Um sistema de captura observa **a entrada**, não a produção. Quem submeteu, por
que canal e com que autenticação é facto declarável em
`proveniencia_submissao`; quem escreveu o conteúdo é outro facto. Um
contabilista apresenta documento do cliente; um mandatário submete peça
assinada pelo representado.

Um produtor **não deve** declarar o submissor como `autor` apenas por ele ter
submetido. Não havendo fundamento para estabelecer autoria, a origem não é
apurável e declara-se pelo quarto modo — sem apagar o que se sabe sobre a
submissão, que é bloco independente.

#### Divergência entre declaração e componente

Os campos descritivos e o conteúdo do componente são **asserções
independentes**. Em caso de divergência:

> **O componente é autoritativo quanto ao conteúdo do ato; o NDF é autoritativo
> quanto a identidade, custódia e classificação.**

Nenhum corrige o outro. Um erro nos campos descritivos corrige-se por **novo
NDF** com `relacoes[{tipo: "corrige"}]`.

#### Anexo ou documento autónomo? — o teste de identidade documental

> **O anexo tem existência documental própria — autor, data, número, ciclo de
> vida, avaliação ou autenticidade que não sejam os do documento que o
> acompanha?**

| Resposta | Representação |
|---|---|
| **Não** — material de apoio | `componentes[]` com `papel: "anexo"`, dentro deste NDF |
| **Sim** — é um documento que por acaso segue outro | **NDF autónomo**, ligado por `relacoes[{tipo: "anexa"}]` |

O segundo caso é o que permite ao anexo ter avaliação, prazo, assinatura e
destino final próprios, e continuar identificável quando o documento que o
acompanhava for eliminado.

#### Função do NDT num documento capturado

| | Documento nativo | Documento capturado |
|---|---|---|
| Reproduz o documento | o NDT, a partir de `documento` | o **componente**, tal como preservado |
| O NDT reproduz | o ato | o **auto de captura** e os seus metadados |

Um leitor **não deve** aplicar o NDT ao bloco `documento` de um capturado
esperando obter o ato, nem apresentar a saída do NDT como sendo o documento
recebido.

### 3.10 `avaliacao` — avaliação arquivística

Bloco **obrigatório** em qualquer NDF-core. Fixa o trio comum aos sistemas
arquivísticos europeus: prazo de conservação, destino final e instrumento que
autoriza a decisão.

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

| Campo | Obrigatório | Descrição |
|---|---|---|
| `perfil` | Sim | Regime arquivístico aplicável. Determina o vocabulário e a sintaxe das referências |
| `classificacao_ref` | Sim | Classe/série no instrumento. Sintaxe definida pelo perfil |
| `prazo_conservacao.valor` | Sim | Inteiro ≥ 0 |
| `prazo_conservacao.unidade` | Sim | `dias` \| `meses` \| `anos` |
| `prazo_conservacao.forma_contagem` | Sim | Facto desencadeador — enum fechado |
| `destino_final` | Sim | Enum fechado |
| `autoridade_avaliacao` | Condicional | Obrigatório **se e só se** `destino_final: "a_determinar"` |
| `instrumento_ref` | Sim | Instrumento e versão consultados. Sintaxe definida pelo perfil |

**`forma_contagem`** (enum fechado): `data_documento`,
`encerramento_processo`, `fim_ano_civil`, `fim_vigencia`, `outro` (com
`forma_contagem_detalhe` obrigatório).

**`destino_final`** (enum fechado):

| Valor | Significado |
|---|---|
| `conservacao_permanente` | Conservação permanente em arquivo — cobre conservação no produtor e transferência para o arquivo competente |
| `eliminacao` | Elegível para eliminação decorrido o prazo |
| `conservacao_parcial_por_amostragem` | Só uma amostra é conservada; o remanescente é eliminado |
| `a_determinar` | Decisão diferida — exige `autoridade_avaliacao` |

`a_determinar` existe porque em vários sistemas europeus a decisão **não
compete à entidade produtora**: é o modelo alemão de *Anbietung/Bewertung*, e
corresponde a `nader te bepalen` nos Países Baixos e à ação `review` das
*retention schedules* britânicas e europeias. `a_determinar` difere o
**destino**, nunca o **prazo**.

#### Perfis de avaliação

`perfil` é um **identificador opaco qualificado**, com o padrão
`^(generic|[a-z][a-z0-9]*(-[a-z0-9]+)+)$` — convenção `<namespace>-<autoridade>`.
Os perfis nomeiam a **autoridade** com competência sobre o regime, não o
instrumento que ela publica: os instrumentos mudam de nome e de edição, a
autoridade mantém-se.

| Perfil | Âmbito |
|---|---|
| `pt-dglab` | Administração Pública portuguesa — MEG/DGLAB. Impõe a sintaxe `<instrumento>/<…>` e a correspondência de instrumento entre `classificacao_ref` e `instrumento_ref` |
| `generic` | Sem restrições jurisdicionais — a estrutura continua exigida, nenhuma sintaxe nacional é imposta |

Exemplos no perfil `pt-dglab`:

```text
classificacao_ref:  "lc/450.10.001"       "ts/at/300.20"       "portaria/1253-A/2009/II-3"
instrumento_ref:    "lc/lista-consolidada-dglab-2023-v3"   "pgd/pgd-mf-2019-v2"
```

O schema do perfil **viaja sempre dentro do `.ndfpkg`**, em
`schemas/<perfil>.schema.json`.

#### Porque a estrutura fica no core e o vocabulário no perfil

Critério que dá sentido à generalização:

> Um leitor que nunca ouviu falar do perfil declarado deve conseguir, **apenas
> com o NDF-core**, determinar se o documento é elegível para aplicação do
> destino final e a partir de que facto se conta o prazo.

É o que permite gerir retenção sobre um acervo multi-jurisdicional sem resolver
perfil nenhum.

#### Dados derivados

A data de elegibilidade para aplicação do destino final é calculada a partir de
`prazo_conservacao` e da data de finalização. **Não** faz parte do NDF-core, não
é canonicalizada nem assinada: é operacional e recalculável.

### 3.11 `relacoes[]` — relações documentais

Um procedimento administrativo é composto por vários documentos **autónomos e
relacionados** — uma informação técnica, um ou mais pareceres, um despacho —
cada um com o seu `ndf_id`, hash e assinaturas. Nunca um único documento com
secções sucessivamente assinadas.

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

Cada relação identifica o alvo por `ndf_id` **e** `payload_hash` — nunca só por
`ndf_id`. O hash prende a relação aos bytes exatos que existiam quando ela foi
estabelecida, e não a uma identidade lógica que entretanto pode ter sido
substituída.

As relações vivem no **NDF-core**, não no envelope, precisamente para ficarem
cobertas pela mesma assinatura que protege o conteúdo.

**Vocabulário base (enum fechado):**

| Valor | Significado |
|---|---|
| `substitui` | O alvo é substituído por este — sucessão documental |
| `corrige` | Corrige informação do alvo, sem o substituir formalmente |
| `complementa` | Acrescenta informação, sem substituir nem corrigir |
| `anula` | Anula os efeitos do alvo |
| `responde_a` | É resposta ao alvo |
| `emite_parecer_sobre` | É parecer emitido sobre o alvo |
| `decide_sobre` | É decisão (despacho) sobre o alvo |
| `executa` | Executa o que o alvo determina |
| `anexa` | O alvo é anexado a este documento |
| `deriva_de` | Deriva do alvo, sem ser nova versão formal |
| `referencia` | Ligação informativa, sem implicação jurídico-documental direta |

Extensão qualificada: `ext.<entidade>.<tipo>`, por exemplo
`ext.at.retificacao-oficiosa`. Caso de uso corrente: `ext.<entidade>.instrui`
para ligar um requerimento recebido à informação técnica que sobre ele se
produz — não é `anexa` (o requerimento não é anexo) nem `responde_a` (a
informação não responde ao requerente).

**Avisos de leitura:**

- Uma relação é **afirmação unilateral e assinada** da entidade produtora do
  documento de origem. Não implica reconhecimento, consentimento nem validação
  de competência por parte da entidade do documento alvo.
- O vocabulário não impede **ciclos** entre documentos independentes. Um
  verificador ou renderizador que percorra o grafo deve implementar deteção de
  ciclos — o schema, só por si, não impõe aciclicidade.
- Quando um tipo documental tem campo próprio de referência (por exemplo
  `despacho.sobre`), o produtor deve manter os dois coerentes; `relacoes` é a
  fonte de verdade verificável.

**Sucessão documental.** `substitui` é a **única** representação normativa de
sucessão. Não existe mecanismo paralelo no envelope nem no manifesto.

```text
A continua a existir, imutável
B substitui A
```

e não «A passou a ser B». O documento substituído não é alterado nem destruído
pela existência do sucessor; apenas deixa de ser o corrente, o que é propriedade
operacional gerida fora do core.

### 3.12 `participantes[]` — pessoas singulares

Índice **exclusivamente de pessoas singulares**. Distingue autoria e
participação de assinatura eletrónica.

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
| `participante_ref` | Sim | Identificador institucional estável — **não** um nome de exibição |
| `papel` | Sim | Enum fechado (abaixo) |
| `qualificacao` | Não | `{tipo, identificador}` — qualidade profissional, quando é condição de validade |

| Papel | Significado | Satisfaz o invariante? |
|---|---|---|
| `autor` | Produziu materialmente o conteúdo — o conteúdo canonicalizado ou o componente binário | **Sim** |
| `coautor` | Produziu materialmente parte do conteúdo | **Sim** |
| `decisor` | Praticou a decisão que constitui o conteúdo | **Sim** |
| `revisor_humano` | Reviu conteúdo produzido por outrem — pessoa, sistema ou IA | Não |
| `representante` | Atuou por conta de outrem, ao abrigo de mandato | Não |
| `responsavel_tecnico` | Responde tecnicamente em nome próprio, sem representar | Não |

Um sistema — determinístico ou de IA — **nunca** é registado em `participantes`,
sob nenhum papel. Um sistema não *participa* na produção de um documento:
**produz** o documento.

#### Autoria — três noções distintas

| Mecanismo | O que significa |
|---|---|
| `documento.autor` (schema do tipo) | Autoria **representada no conteúdo** — o que o renderizador apresenta |
| `participantes[].papel = "autor"` | Autoria **estrutural declarada** — por identificador, para indexação e proveniência |
| `assinaturas[].papel = "autor"` (envelope) | A **qualidade** em que uma assinatura foi aposta |

Não são equivalentes nem formam hierarquia. Divergir é legítimo (um documento
assinado por representante em nome do autor material); por isso a especificação
não impõe validação automática de igualdade — impõe que a diferença, quando
exista, seja intencional.

#### `qualificacao`

Para documentos cuja validade depende de qualidade profissional determinada:
contabilista certificado, ROC, advogado, engenheiro, arquiteto, médico.

`qualificacao` é **ortogonal** a `papel`: um advogado mandatado é
`representante` com `qualificacao.tipo: "advogado"`; um contabilista certificado
que responde tecnicamente é `responsavel_tecnico` com
`qualificacao.tipo: "contabilista_certificado"`.

Distinção face a `imputacao`: o contabilista responde tecnicamente, mas a
declaração continua imputada ao sujeito passivo; o advogado atua por conta do
mandante, e é ao mandante que o requerimento é imputado. Ambos ficam em
`participantes`.

#### A ausência não é prova de ausência

`participantes` regista intervenção **observável e identificada** pelo sistema
produtor. Quando um terceiro atua com as credenciais do titular — contabilista
ou familiar que submete no portal —, o sistema não tem como o distinguir do
titular. Registá-lo seria inventar informação; omiti-lo é o comportamento
correto. Um `participantes` vazio ou ausente é **silêncio, não negação**.

### 3.13 `proveniencia_sistema[]` — sistemas determinísticos

Uma parte substancial dos documentos da Administração é gerada por sistemas
determinísticos, sem autor humano material: liquidações, notificações, certidões
automáticas, avisos de cobrança.

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
        "hash": "sha256:…"
      }
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `sistema.nome` | Sim | Designação do sistema produtor |
| `sistema.identificador` | Sim | Identificador institucional estável — referência externa |
| `sistema.versao` | Sim | Versão em produção quando o conteúdo foi produzido |
| `componente` / `versao_componente` | Não | Componente responsável por este passo |
| `gerado_em` | Sim | Instante em que este passo produziu o seu resultado |
| `regra_ref` | Não | Conjunto de regras, tabela ou base de cálculo aplicada |
| `build_ref` | Não | *Build* exato do sistema |
| `configuracao_ref` | Não | Configuração em vigor |

**É um array porque um documento atravessa por vezes uma cadeia de produção** —
motor de cálculo, sistema de validação, sistema de emissão.

**As entradas devem estar ordenadas cronologicamente**, por `gerado_em` não
decrescente. A regra não é estética: JCS preserva a ordem dos arrays, logo a
ordem entra nos `payload_bytes` e no `payload_hash`. Sem ordem normativa, dois
produtores que registem os mesmos factos produziriam hashes diferentes,
quebrando a comparação por hash de que dependem `relacoes[].alvo.payload_hash` e
a cadeia de custódia. Como a ordem não é exprimível em JSON Schema, é uma
verificação **semântica** obrigatória, com caso de conformidade próprio.

**Fronteira com `proveniencia_ia` (normativa).** Qualquer componente **não
determinístico** pertence a `proveniencia_ia`, sem exceção, mesmo quando
embebido num *pipeline* automático. A razão é prática: declarar um modelo como
«sistema» contornaria o estado de revisão humana obrigatório. A fronteira não é
arrumação — é o que impede que a supervisão humana seja evitada por escolha de
campo.

**Âmbito mínimo.** Não é SBOM, inventário de dependências nem registo de
execução. Recomenda-se ponderar a omissão de `build_ref` e `configuracao_ref` em
documentos de circulação externa: nomes, versões e referências de *build* de
sistemas internos constituem superfície de ataque, e o NDF-core é legível por
quem receber o pacote.

**Não há promessa de reprodutibilidade byte a byte:** com `gerado_em` no core e
`ndf_id` como UUID v4, reexecutar o mesmo motor sobre os mesmos dados não produz
o mesmo documento canónico. O bloco entrega **identificação estável da origem e
das regras**, e o caminho para a evidência detalhada.

### 3.14 `proveniencia_ia` — sistemas de IA

Bloco opcional, relevante quando um sistema de IA influenciou materialmente a
criação, transformação, classificação, fundamentação ou revisão do conteúdo.

```json
{
  "proveniencia_ia": {
    "utilizada": true,
    "intervencoes": [
      {
        "intervencao_id": "b2c3d4e5-f6a7-4890-bcde-f01234567890",
        "finalidade": "apoio_redacao",
        "sistema": { "nome": "…", "fornecedor": "…", "modelo": "…", "versao": "…" },
        "executada_em": "2026-06-18T10:30:00Z",
        "resultado_incorporado": "parcialmente",
        "segmentos_afetados": ["documento.fundamentacao"],
        "revisao_humana": {
          "estado": "revisto_e_aprovado",
          "revisor_ref": "user:456",
          "revisto_em": "2026-06-18T11:00:00Z"
        },
        "evidencia_ref": { "tipo": "registo_externo", "identificador": "…", "hash": "sha256:…" }
      }
    ]
  }
}
```

**Dois níveis de evidência:**

1. **Proveniência essencial** — no NDF-core, coberta pela assinatura:
   finalidade, sistema/fornecedor/modelo/versão, data, resultado incorporado,
   segmentos afetados, estado da revisão humana.
2. **Logs detalhados** — prompts e respostas completas ficam **fora** do NDF,
   sob política própria de acesso e retenção, ligados por `evidencia_ref`. Não
   devem ser embutidos: podem conter dados pessoais, informação confidencial ou
   material desproporcionado para conservação permanente.

**`finalidade`** (enum fechado): `apoio_redacao`, `resumo`, `classificacao`,
`pesquisa`, `traducao`, `deteccao_erros`, `outro` (com `finalidade_detalhe`
recomendado).

**`revisao_humana.estado`** é obrigatório em cada intervenção — incluindo o
valor `"pendente"`, para que a ausência de revisão seja **representável e
visível**. Nos estados terminais (`revisto_e_aprovado`,
`revisto_com_alteracoes`, `rejeitado`), `revisor_ref` e `revisto_em` são
obrigatórios.

**A IA não é signatária, participante nem decisora.** Regista-se
exclusivamente em `proveniencia_ia.intervencoes[].sistema`. O ato administrativo
depende sempre de intervenção humana identificável.

Regras de coerência: `utilizada: true` exige `intervencoes` com pelo menos um
elemento; `utilizada: false` exige `intervencoes` ausente ou vazio.

**Limite de âmbito:** o NDF não impõe nem garante conformidade com o AI Act ou
qualquer outro regime. Fornece mecanismos que podem apoiar rastreabilidade,
transparência e supervisão humana.

### 3.15 `imputacao[]` — responsabilidade jurídica

`participantes`, `proveniencia_sistema` e `proveniencia_ia` registam **factos** —
quem ou o quê produziu materialmente o conteúdo. `imputacao` regista **direito**
— quem responde juridicamente, e a que título.

Os dois eixos são independentes por desenho: podem coincidir (declaração
entregue pelo próprio), divergir (declaração pré-preenchida por um sistema e
confirmada pelo interessado) ou ser mutuamente exclusivos (declaração produzida
por um sistema e imputada por efeito da lei a quem nada fez).

O bloco responde a exigências concretas do direito administrativo português:
CPA art. 151.º, n.º 1, al. a) (indicação da autoridade e menção da delegação);
CPPT art. 36.º, n.º 2 (notificações); CPPT art. 66.º, n.º 2 (recurso hierárquico
dirigido ao superior do autor do ato).

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

| `titulo` | Regime | Significado | Exige |
|---|---|---|---|
| `competencia_propria` | Ato administrativo | Competência própria do órgão | — |
| `delegacao` | Ato administrativo | Poderes delegados | `fundamento.publicacao_ref` |
| `subdelegacao` | Ato administrativo | Poderes subdelegados | `fundamento.publicacao_ref` |
| `declaracao_propria` | Declarativo | O declarante produziu e apresentou a declaração | — |
| `aceitacao_expressa` | Declarativo | Conteúdo produzido por outrem e expressamente aceite | `em` |
| `efeito_legal` | Declarativo | Imputação resulta da lei, sem ato do imputado | `fundamento.descricao` |

As condicionais são exprimíveis em JSON Schema (`if`/`then`) e estão lá.

**Cardinalidade — co-titularidade, não cadeia de delegação.** Mais do que uma
entrada significa que várias pessoas ou órgãos respondem pelo mesmo documento:
ato conjunto, ou declaração conjunta (IRS em tributação conjunta, com uma
entrada e uma autenticação por sujeito passivo). Uma delegação **não** se modela
como duas entradas (delegante e delegado): é **uma** entrada com
`titulo: "delegacao"` e o `fundamento` a identificar o ato publicado.

#### Submissão por meio autenticado

Muitos documentos entregues à Administração não têm assinatura eletrónica: são
submetidos por canal autenticado — Portal das Finanças, Segurança Social Direta.

```json
{
  "imputacao": [
    {
      "imputado": { "designacao": "Sujeito passivo A", "ref": "nif:123456789" },
      "titulo": "declaracao_propria",
      "em": "2026-05-20T14:03:00Z",
      "autenticacao": { "meio": "chave_movel_digital", "nivel_garantia": "elevado" }
    }
  ]
}
```

`autenticacao.meio` é enum **aberto**: `chave_movel_digital`, `cartao_cidadao`,
`senha_acesso`, `certificado_qualificado`, `presencial`. A inclusão do
presencial é deliberada: um vocabulário só digital obrigaria a modelar o
atendimento ao balcão por omissão, tornando-o indistinguível de um documento sem
identificação nenhuma.

`nivel_garantia` (`baixo`, `substancial`, `elevado`) é opcional e descreve o
**nível técnico do mecanismo de autenticação**, na terminologia eIDAS. **Não**
gradua a imputação: um leitor **não deve** derivar de um `nivel_garantia` mais
baixo uma imputação mais fraca, uma presunção ilidível ou tratamento
diferenciado.

Regras associadas:

- **A imputação não é qualificável.** Uma entrada afirma-se ou omite-se; não
  admite grau de confiança, presunção ou reserva. Graduar exigiria que o formato
  arbitrasse sobre a força de uma declaração alheia. Alegações de uso indevido de
  credenciais dirimem-se pelas vias competentes.
- **A imputação é histórica, não revogável no documento.** Uma anulação
  posterior **não altera** o NDF: a anulação é documento novo, ligado por
  `relacoes[{tipo: "anula"}]`. Um leitor não deve tratar a imputação de um
  documento anulado como retroativamente viciada.
- **Equivalência entre canais.** Um pedido por e-balcão e um pedido presencial
  por interessado identificado têm o mesmo valor jurídico. Modelam-se da mesma
  forma, variando apenas `autenticacao.meio`.
- **`nivel_assinatura: "nenhuma"` e `autenticacao` não são contraditórios.** Um
  documento pode não ter assinatura eletrónica e ainda assim ter autoria
  vinculativa. Um leitor **não deve** concluir de `"nenhuma"` que o documento é
  anónimo ou não imputável.

#### Casos de referência

| Caso | `participantes` | `proveniencia_sistema` | `imputacao` |
|---|---|---|---|
| Declaração entregue pelo sujeito passivo | `autor` | — | 1 entrada, `declaracao_propria` + `autenticacao` |
| Declaração conjunta | `autor`, `coautor` | — | **2 entradas**, cada uma com autenticação própria |
| Declaração automática confirmada | — | sistema da AT | 1 entrada, `aceitacao_expressa` + `autenticacao` |
| Declaração automática convertida sem confirmação | — | sistema da AT | 1 entrada, `efeito_legal` |
| Liquidação oficiosa | — | sistema da AT | 1 entrada, `competencia_propria` ou `delegacao` |

O quarto caso é o que justifica a existência do bloco: a autoria é imputada, por
efeito da lei, a quem não produziu o conteúdo nem praticou qualquer ato.
Registar o sujeito passivo como `autor` seria juridicamente correto e
**factualmente falso**; registar apenas `proveniencia_sistema` seria
factualmente correto e **juridicamente incompleto**. Os dois eixos, em conjunto,
dizem a verdade nos dois planos.

`imputacao` é **opcional** no core — nem todo o NDF é ato ou declaração. O
schema do tipo documental **pode** torná-la obrigatória para os tipos em que a
lei o exige.

### 3.16 Exemplo completo de NDF-core

Ofício com anexo, resposta a outro documento, dados pessoais e assinatura
qualificada. Apresentado formatado para leitura; **os bytes guardados são a
forma JCS** (chaves ordenadas, sem espaços).

```json
{
  "ndf_version": "1.0.0",
  "ndf_id": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
  "estado": "ativo",
  "payload_hash_alg": "sha256",
  "nivel_assinatura": "qualificada",
  "ndt_version_ref": "oficio-generico@2.0.0",
  "metadados": {
    "tipo_documento_ref": "oficio@1.0.0",
    "entidade_produtora": {
      "designacao": "Direção-Geral de Exemplo",
      "identificadores": [
        { "sistema": "pt-dglab", "valor": "PT-DGE-000" },
        { "sistema": "pt-nif", "valor": "123456789" }
      ]
    },
    "entidade_responsavel": "Direção-Geral de Exemplo",
    "assunto": "Resposta ao ofício n.º 45/2026 — Pedido de informação sobre processo X",
    "numero_referencia": "OF/2026/00123",
    "processo_ref": "proc.º 456/2026",
    "idioma": "pt",
    "classificacao_seguranca": { "perfil": "pt", "nivel": "uso_interno" },
    "contem_dados_pessoais": true,
    "protecao_dados": {
      "categorias": ["identificacao_fiscal", "dados_processuais"],
      "base_legal_conservacao": { "regime": "eu-gdpr", "base": "art6-1-c" },
      "responsavel_tratamento": "Direção-Geral de Exemplo"
    }
  },
  "documento": {
    "numero": "OF/2026/00123",
    "data": "2026-06-18",
    "assunto": "Resposta ao ofício n.º 45/2026",
    "destinatario": {
      "nome": "Maria da Silva",
      "cargo": "Directora de Serviços",
      "entidade": "Ministério de Exemplo"
    },
    "referencias": ["OF n.º 45/2026", "proc.º 456/2026"],
    "signatario": { "nome": "João Costa", "cargo": "Director-Geral" },
    "corpo": {
      "ncrtf_version": "2.0.0",
      "content": [
        {
          "type": "paragraph",
          "content": [
            { "type": "text", "text": "Em resposta ao ofício n.º 45/2026, cumpre-nos informar o seguinte:" }
          ]
        },
        {
          "type": "heading",
          "level": 2,
          "content": [ { "type": "text", "text": "Enquadramento" } ]
        },
        {
          "type": "paragraph",
          "content": [
            { "type": "text", "text": "Nos termos do artigo " },
            { "type": "text", "text": "62.º do CPA", "marks": ["bold"] },
            { "type": "text", "text": ", o prazo de decisão é de 90 dias." }
          ]
        }
      ]
    },
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
  },
  "avaliacao": {
    "perfil": "pt-dglab",
    "classificacao_ref": "lc/450.10.001",
    "prazo_conservacao": { "valor": 5, "unidade": "anos", "forma_contagem": "data_documento" },
    "destino_final": "eliminacao",
    "instrumento_ref": "lc/lista-consolidada-dglab-2023-v3"
  },
  "participantes": [
    { "participante_ref": "user:100", "papel": "autor" }
  ],
  "relacoes": [
    {
      "tipo": "responde_a",
      "alvo": {
        "ndf_id": "2d6f80b1-9c47-4a35-8e12-5b90fa73cd48",
        "payload_hash": "sha256:4c1f9a02e7b53d84610cf27a95d3e8b1f60427cda9e3f815b2704d6c8ae19f3b",
        "descricao": "Ofício n.º 45/2026 — Pedido de informação sobre processo X"
      }
    }
  ]
}
```

Exemplos completos e executáveis no repositório:

| Exemplo | Ilustra |
|---|---|
| [`specs/ndf/examples/ndfpkg-example/`](specs/ndf/examples/ndfpkg-example/) | Pacote portátil completo com anexo, NCRTF e recursos |
| [`specs/ndf/examples/informacao-parecer-despacho/`](specs/ndf/examples/informacao-parecer-despacho/) | Três NDF autónomos ligados por `relacoes[]` |
| [`specs/ndf/examples/captura-requerimento/`](specs/ndf/examples/captura-requerimento/) | Documento capturado, com componente original e imputação por canal autenticado |
| [`specs/ndf/examples/liquidacao-irs-automatica/`](specs/ndf/examples/liquidacao-irs-automatica/) | Origem de sistema e imputação por efeito legal |
| [`specs/ndf/examples/modelo3-irs-2025.json`](specs/ndf/examples/modelo3-irs-2025.json) | Formulário complexo |

---

## 4. Envelope de integridade e autenticidade

**Schema:** [`specs/ndf/schemas/envelope.schema.json`](specs/ndf/schemas/envelope.schema.json)

### 4.1 Propósito

O envelope reúne as **provas criptográficas** associadas ao NDF-core. Está
separado do core por uma razão estrutural: evita circularidade — fica **fora**
dos bytes sobre os quais a própria assinatura é calculada.

### 4.2 O que contém

| Componente | Conteúdo | Condicional |
|---|---|---|
| `assinaturas[]` | Assinaturas pessoais ou selos institucionais CAdES sobre os `payload_bytes`, cada entrada uma unidade de prova autocontida | Obrigatória se `nivel_assinatura ∈ {avancada, qualificada}`; selo opcional se `nenhuma` |
| `validation_code` | Código de verificação canónico derivado de `ndf_id` + `payload_hash` | **Sempre presente** |
| `payload_hash` | Digest dos bytes canónicos | Sempre presente |

`timestamps` e `validation_material` **não** são componentes de topo: vivem
dentro de **cada entrada** de `assinaturas[]`, para que a associação entre
prova, certificado, cadeia e timestamp nunca seja ambígua quando existe mais do
que uma assinatura independente.

### 4.3 O que não contém

- Não contém o conteúdo do documento nem os seus metadados.
- Não contém relações documentais nem sucessão — essas vivem no core, para
  ficarem cobertas pela assinatura.
- Não é canonicalizado nem assinado — é produzido **a partir** da assinatura
  sobre o core.

### 4.4 Estrutura de cada assinatura

| Campo | Obrigatório | Descrição |
|---|---|---|
| `assinatura_id` | Sim | Identificador estável desta entrada — permite referenciá-la sem ambiguidade |
| `nivel` | Sim | `selo_institucional` \| `avancada` \| `qualificada` |
| `papel` | Não | Papel exercido **neste documento**: `autor`, `coautor`, `validador`, `aprovador`, `decisor`, `representante`, `testemunha`, `selante` |
| `ordem` | Não | Indicação **descritiva** de ordem entre coassinaturas — não é motor de workflow |
| `signatario` | Condicional | `{nome, certificado_serie, cargo?}` — obrigatório em `avancada`/`qualificada` |
| `assinado_em` | Não | Instante declarado pelo produtor. **Não substitui** o timestamp RFC 3161 |
| `cades_b_lta` | Sim | Assinatura CAdES-B-LTA detached (DER, base64) |
| `timestamps` | Condicional | `{assinatura, arquivo}` — DER base64. Obrigatório em `avancada`/`qualificada` |
| `validation_material` | Condicional | `{cadeia_certificados[], revogacao[]?}` — obrigatório em `avancada`/`qualificada` |

`papel` (envelope) é distinto de `signatario.cargo`: uma pessoa pode ter o cargo
«Diretor de Serviços» e assinar no papel de `decisor`.

### 4.5 CAdES-B-LTA

Nível alvo quando CAdES é usado:

| Nível | O que acrescenta |
|---|---|
| **B** (Basic) | Assinatura sobre o digest, com certificado do signatário |
| **T** (Timestamp) | Timestamp sobre o valor da assinatura — prova de quando foi criada |
| **LT** (Long Term) | Cadeia de certificados e dados de revogação, permitindo validar mesmo que o repositório de revogação desapareça |
| **A** (Archive) | Timestamp de arquivo sobre assinatura + dados LT, protegendo contra expiração ou comprometimento futuro dos algoritmos |

**Requisitos da TSA:** timestamp RFC 3161 emitido por TSA de uma lista de
confiança de Estado-Membro (ETSI TS 119 612); precisão de 1 segundo ou melhor;
hash SHA-256 ou superior; protocolo TSP sobre HTTP(S). Em ambientes sem acesso à
internet, pode usar-se TSA local acreditada desde que a cadeia de confiança seja
incluída no `validation_material`.

**Múltiplas assinaturas** destinam-se a coautoria, aprovação conjunta ou selo
institucional **sobre o mesmo conteúdo**. Um parecer sobre uma informação, ou um
despacho sobre um parecer, **não** se representam como segunda assinatura do
documento original: são NDF autónomos ligados por `relacoes`.

### 4.6 Preservação da assinatura original

Quando `nivel_assinatura ∈ {avancada, qualificada}`, a assinatura CAdES é parte
inseparável do registo arquivístico. Enquanto o NDF-core for preservado:

1. preservar **byte a byte** o contentor CAdES original;
2. preservar os timestamps RFC 3161 e o material de validação associados;
3. impedir alteração, substituição ou remoção isolada destes objetos;
4. incluí-los nos hashes do inventário do `.ndfpkg`.

Uma re-selagem, renovação de timestamp ou migração de algoritmo **nunca**
substitui a assinatura original: a nova prova protege a cadeia anterior e é
**acrescentada** ao envelope. A eliminação dos objetos de assinatura só é
permitida com a eliminação arquivística formalmente autorizada do documento.

### 4.7 Assinaturas contidas em componentes

Um componente binário pode transportar assinatura própria, produzida fora do
sistema — tipicamente PAdES sobre um PDF recebido de terceiro.

- `nivel_assinatura` descreve **a assinatura do NDF** e **não** se deriva de
  assinaturas contidas. Um NDF que preserve um PDF com assinatura qualificada de
  terceiro declara `nivel_assinatura: "nenhuma"`, com ou sem selo institucional.
- Um leitor **não deve** apresentar a assinatura de um componente como sendo a
  assinatura do NDF.
- Preservar os bytes **não** preserva a verificabilidade: uma assinatura de
  terceiro torna-se inverificável quando os certificados expiram, salvo se
  cadeia, revogação e timestamp forem congelados no momento da captura — como
  componente de `papel: "evidencia"`.
- Quando este sistema produz uma assinatura **PAdES** sobre uma representação, a
  ordem é normativa: assinar o PDF → calcular o hash do PDF **já assinado** →
  declarar esse hash no componente → só então finalizar o NDF. A ordem inversa
  produz um hash que não corresponde ao ficheiro distribuído.

### 4.8 `validation_code`

Identificador curto aposto à representação visual, derivado deterministicamente:

```text
input           = ndf_id + "|" + payload_hash
digest          = SHA-256(input)
code_b32        = BASE32_NOPAD(digest)            -- RFC 4648 §6, maiúsculas
validation_code = "NDF-" + code_b32[:20]          -- primeiros 100 bits
```

**Formato:** `NDF-` + 20 caracteres Base32 (A–Z, 2–7).
**Exemplo:** `NDF-A3F7K2MXPQR9ZTNW8VJ`
**Forma legível:** `NDF-A3F7K-2MXPQ-R9ZTN-W8VJX`

| Propriedade | Valor |
|---|---|
| Entropia | 100 bits |
| Combinações | 2¹⁰⁰ ≈ 1,27 × 10³⁰ |
| Colisão com 10¹² documentos | ≈ 3,9 × 10⁻⁷ |
| Alfabeto | Base32 RFC 4648 — sem caracteres ambíguos (0/O, 1/I/l) |

**O que o código prova e o que não prova.** É *self-verifiable* quanto à
**correspondência**: qualquer implementação confirma que o código corresponde ao
`ndf_id` e ao `payload_hash` apresentados. Essa verificação **não autentica o
emissor**. Fora de um custodiante confiável, não prova autoria nem origem
institucional.

**Posição no pipeline.** Calculado **após** a canonicalização e o hash, e
**antes** da assinatura. Não faz parte do core — evita a referência circular (o
código depende do hash do conteúdo; se fosse conteúdo, alteraria o hash).

**Representações.** Texto para leitura humana e QR code para leitura por
dispositivo. Ambas são obrigatórias em documentos emitidos para o exterior. No
NDT, resolve-se pelo placeholder `{{validation_code}}`.

**Âmbito de «emitido para o exterior»** (SPEC NDF §4.6.5): um documento é
emitido para o exterior quando a sua representação visual se destina a circular
**fora do domínio de custódia** do emissor — cidadãos, empresas ou entidades sem
relação de custódia sobre o registo. A transferência de custódia entre
custodiantes **não** é emissão para o exterior: o que aí circula é o pacote
verificável, não a representação impressa, e a obrigatoriedade das duas
representações não se lhe aplica. O URL codificado no QR é escolhido pelo
custodiante — o portal público é exemplo, não requisito — e pode resolver para
um serviço interno ao domínio de custódia.

### 4.9 Fronteira de responsabilidade: formato vs. sistema de gestão documental

A SPEC NDF §4.7 fixa como princípio arquitetural o que §1.5 deste manual
resume: **as garantias do NDF terminam na integridade, na autenticidade e na
declaração fiel do conteúdo e dos seus metadados**. Proteger os bytes e
controlar quem lhes acede é responsabilidade do sistema de gestão documental —
nunca do formato. Quem avalie as especificações para contextos sensíveis não
deve presumir que resolvem segurança de armazenamento, de transporte ou de
acesso.

**Cifra em trânsito e em repouso** (SPEC NDF §4.7.1):

- a especificação **não define envelope cifrado normativo**, não impõe
  algoritmo de cifra e não assume nenhum esquema de gestão de chaves;
- o NDF é **opaco** a essa camada: nenhum campo do core ou do envelope declara,
  referencia ou depende da cifra aplicada pelo custodiante;
- um NDF lido e verificado é idêntico, byte a byte, quer o sistema cifre de
  forma agressiva quer não cifre de todo — é isso que mantém o formato
  desacoplado da política de segurança de cada implementador;
- a ordem correta é sempre a mesma: **assinar primeiro, cifrar na camada de
  armazenamento depois da finalização, decifrar antes de verificar** — nunca ao
  contrário. A assinatura CAdES-B-LTA, os timestamps e o `validation_code`
  operam sobre o conteúdo canónico **em claro**; cifrar antes de assinar
  acoplaria a prova de longa duração a material de chaves cuja rotação ou perda
  destruiria a verificabilidade.

**Documentos classificados** (SPEC NDF §4.7.2): tratam-se por topologia, não
por formato. Em particular, um serviço de verificação pública **não deve** ser
assumido como aplicável: resolver um `validation_code` num serviço exposto
revela a existência do documento, o custodiante e metadados temporais —
informação que, num regime de classificação, é frequentemente ela própria
protegida. A inclusão de um documento em qualquer serviço de verificação deve
ser decisão explícita do custodiante face ao nível declarado, nunca
comportamento por omissão.

**Pontos de decisão de uma topologia classificada** (SPEC NDF §4.7.3,
informativa) — o que uma implementação para contextos classificados tem de
responder explicitamente:

| Ponto de decisão | Referência na SPEC NDF |
|---|---|
| Rede e isolamento — rede segregada ou *air-gapped*? Sincronização com que fronteira? | §1.5 |
| Timestamping — TSA pública qualificada ou TSA local acreditada, com a cadeia em `validation_material`? | §4.2.1 |
| Verificação — existe serviço de resolução de `validation_code`? Acessível a quem? | §4.6.4, §4.7.2 |
| Representação visual — o QR/URL resolve para que serviço? O elemento existe sequer nos templates? | §4.6.5 |
| Divulgação parcial — versões expurgadas são representações derivadas, assinadas à parte, nunca alteração ao core | §2.1 |
| Acesso, chaves e auditoria — autenticação, autorização face a `classificacao_seguranca`, *escrow*, registo de acessos | guia informativo |

Estas orientações **não acrescentam requisitos de conformidade**: um produtor e
um leitor conformes são-no nos mesmos termos em qualquer topologia.

### 4.10 Exemplo de envelope

```json
{
  "estado": "ativo",
  "payload_hash": "sha256:223624028013a35e513d5907109402f740a72e86f75f302605597197b4d30a3a",
  "validation_code": "NDF-4L64GNOHXKBEBOX7FTR3",
  "assinaturas": [
    {
      "assinatura_id": "79f85831-5fa1-4ee8-bc16-8bcd468f9a4c",
      "nivel": "qualificada",
      "papel": "decisor",
      "signatario": {
        "nome": "João Costa",
        "certificado_serie": "0a1b2c3d4e5f6a7b",
        "cargo": "Director-Geral"
      },
      "cades_b_lta": "<BASE64_DER_CADES_B_LTA>",
      "assinado_em": "2026-06-18T10:30:00Z",
      "timestamps": {
        "assinatura": "<BASE64_RFC3161_B_T>",
        "arquivo": "<BASE64_RFC3161_B_LTA>"
      },
      "validation_material": {
        "cadeia_certificados": [
          "<BASE64_DER_CERT_SIGNATARIO>",
          "<BASE64_DER_CERT_INTERMEDIO>",
          "<BASE64_DER_CERT_RAIZ>"
        ],
        "revogacao": [ { "tipo": "ocsp", "dados": "<BASE64_OCSP_RESPONSE>" } ]
      }
    }
  ]
}
```

---

## 5. `.ndfpkg` — pacote portátil

**Schema do manifesto:** [`specs/ndf/schemas/manifest.schema.json`](specs/ndf/schemas/manifest.schema.json)

### 5.1 Propósito

Formato de exportação **autocontido** de um NDF finalizado. Reúne o necessário
para verificar, renderizar e preservar o documento sem depender do sistema
produtor original nem de qualquer serviço online.

### 5.2 Composição

```text
documento.ndfpkg (ZIP)
├── manifest.json          — metadados do pacote e inventário com hashes
├── ndf-core.json          — payload_bytes do NDF-core (bytes canonicalizados, UTF-8)
├── envelope.json          — assinaturas, timestamps, material de validação
├── ndt/
│   └── <schema_id>@<versao>.ndt.json   — o NDT referenciado por ndt_version_ref
├── schemas/
│   ├── <tipo_id>.schema.json           — schema do tipo documental
│   └── <perfil>.schema.json            — schema do perfil de avaliação
├── recursos/              — recursos visuais partilhados por NDT e NCRTF
├── original/              — componentes de papel «original», bytes tal como emitidos/recebidos
├── representacoes/        — componentes derivados de um original
├── anexos/                — componentes de apoio sem identidade documental própria
└── evidencias/            — material de validação de assinaturas contidas
```

Os quatro últimos diretórios existem apenas quando o documento declarar
componentes dos papéis correspondentes.

**O nome de cada ficheiro é livre.** O diretório reflete o papel, e a
correspondência com a declaração faz-se **pelo digest**, nunca pelo caminho. Um
pacote materializado de outra forma continua a corresponder ao mesmo NDF e à
mesma assinatura.

### 5.3 Regras de fecho

O fecho vale **nos dois sentidos** (`NDF-PKG-009`):

- cada componente declarado em `documento` tem de estar presente, com digest
  coincidente e entrada no inventário;
- cada ficheiro em `original/`, `representacoes/`, `anexos/` ou `evidencias/`
  tem de corresponder a um componente declarado.

Um ficheiro colocado num destes diretórios sem declaração torna o pacote **não
conforme**: estar inventariado garante-lhe integridade, não estatuto documental
— sem declaração em `documento`, nenhum leitor sabe que papel tem, e a
assinatura não o cobre.

Quanto a `schemas/`:

| Schema | Obrigatoriedade |
|---|---|
| Perfil de avaliação (`avaliacao.perfil`) | **Sempre obrigatório** |
| Tipo documental de extensão qualificada (`ext.…`) | **Obrigatório** — não há outro sítio onde possa ser resolvido |
| Tipo documental canónico | Recomendado |

Um leitor resolve o schema do tipo **preferencialmente a partir do pacote**,
recorrendo ao registo canónico apenas quando o pacote não o contiver.

### 5.4 `manifest.json`

O manifesto é **inventário físico do pacote** — não duplica informação
documental do NDF-core.

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
    { "ficheiro": "ndf-core.json", "hash_sha256": "sha256:7196abc4…" },
    { "ficheiro": "envelope.json", "hash_sha256": "sha256:f37a43b3…" },
    { "ficheiro": "ndt/oficio-generico@2.0.0.ndt.json", "hash_sha256": "sha256:f036d126…" }
  ]
}
```

Note-se que `estado` no manifesto é o **estado corrente** do ciclo de vida, ao
contrário do `estado` do NDF-core, que é sempre `"ativo"` — o do momento da
finalização.

### 5.5 Garantias

- **Auto-suficiência** — tudo o necessário para verificar a assinatura,
  reproduzir visualmente o documento e confirmar a avaliação arquivística, sem
  infraestrutura online.
- **NDT embebido** — reprodutibilidade visual mesmo que o NDT evolua ou o
  repositório original desapareça.
- **Verificabilidade** — qualquer implementação confirma
  `sha256(ndf-core.json) == payload_hash` e valida o CAdES sem acesso ao sistema
  de origem.
- **Cadeia de sucessão** — reconstruível a partir das `relacoes` no
  `ndf-core.json` de cada pacote, isto é, **a partir dos bytes assinados**. O
  manifesto não duplica essa informação.

### 5.6 O que o `.ndfpkg` **não** transporta

- **O log de custódia.** O pacote é a unidade de **um documento**; o log é do
  custodiante. A transferência de evidência entre entidades faz-se pelo conjunto
  de transferência (§9.3).
- **Segredos, chaves privadas, credenciais.**
- **Dados derivados** — datas de elegibilidade, índices, contadores.

---

## 6. NDT — NORMORDIS Document Template

**Especificação:** [`specs/ndt/SPEC.md`](specs/ndt/SPEC.md) · **Schema:**
[`specs/ndt/schemas/ndt.schema.json`](specs/ndt/schemas/ndt.schema.json)

### 6.1 Propósito

**NDF + NDT + renderizador = representação visual do documento.**

- **NDT** descreve *como* o documento é composto visualmente: páginas,
  posições, elementos gráficos, tipografia, tabelas, mobília.
- **NDF** fornece *o quê*: os dados já computados pela aplicação de domínio.
- **Renderizador** combina os dois e produz a saída.

Âmbito: documentos administrativos e legais/normativos — predominantemente
textuais, tabulares ou formularizados. Desde impressos fiscais complexos
(Modelo 3 IRS) e documentos administrativos correntes a texto legal publicado.

### 6.2 O que o NDT contém

| Bloco | Conteúdo |
|---|---|
| Identidade | `ndt_version`, `schema_id`, `versao_ndt`, `titulo`, `emissor`, `referencia_legal` |
| `estilos` | Tipografia e espaçamento por defeito — fonte principal para ODF e HTML |
| `layout` | Formato de página, orientação, margens |
| `paginas_def[]` | Modelos de página: `graficos[]`, `campos[]`, `blocos[]`, `fluxo`, `mobilia[]` |
| `sequencia[]` | Ordem e número de instâncias das páginas no documento final |
| `recursos[]` | Imagens e fontes, embebidas ou referenciadas por hash |
| `composicao[]` | Entrega conjunta de documentos independentes num único ficheiro |

### 6.3 O que o NDT **não** contém

| Não contém | Porquê |
|---|---|
| **Dados de negócio** | Vêm do NDF |
| **Regras de validação do domínio** | Da aplicação produtora |
| **Fórmulas de cálculo** | Idem |
| **Obrigatoriedade material de campos** | Idem |
| **Conteúdo NCRTF** | O NCRTF vive no NDF; o NDT declara apenas o caminho |
| **Lógica condicional expressiva** | `incluir_se` aceita **apenas** um caminho para booleano — sem operadores, sem funções |
| **Prefixos `documento.` ou `NDF-core.`** | A raiz `NDF-core.documento` é implícita |
| **Uma linguagem de desenho genérica** | As primitivas existem para documentos institucionais; novas só quando representem padrões recorrentes |

O renderizador verifica versões, referências, integridade e estrutura. **Não
decide** se um dado satisfaz uma regra jurídica ou de negócio.

### 6.4 Identidade e versionamento

```json
{
  "ndt_version": "2.0.0",
  "schema_id": "oficio-generico",
  "versao_ndt": "2026.1",
  "titulo": "Ofício Genérico",
  "emissor": "AT",
  "referencia_legal": "Portaria n.º .../2026"
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `ndt_version` | Sim | Versão do **formato NDT** (SemVer) |
| `schema_id` | Sim | Identificador **estável** do tipo de documento — identifica o tipo, não a versão |
| `versao_ndt` | Sim | Versão desta instância do template |
| `titulo`, `emissor`, `referencia_legal` | Não | Descritivos |

**Cada `versao_ndt` é um template autónomo.** Não há garantia de continuidade,
compatibilidade ou parecença entre duas versões: um impresso muda por vezes
radicalmente de um ano para o seguinte. `versao_ndt` é uma **etiqueta de
identidade** — não segue SemVer e não implica relação de compatibilidade.

A continuidade histórica não depende disso: cada NDF declara o seu
`ndt_version_ref` dentro do payload assinado, e o `.ndfpkg` incorpora essa
versão exata — um documento renderiza-se sempre com o template com que foi
produzido.

### 6.5 Referência NDF ↔ NDT

| NDF-core | NDT | Significado |
|---|---|---|
| `metadados.tipo_documento_ref` | `schema_id` | Identifica o tipo de documento |
| `ndt_version_ref` | `schema_id@versao_ndt` | Identifica a versão concreta do template |

O hash do ficheiro NDT é registado no inventário do `.ndfpkg`. **Não existe
campo `ndt_hash` no NDF-core v1.0.0.**

### 6.6 Duas fases de uso

| Fase | Estado do NDF | Papel do NDT |
|---|---|---|
| **Apresentação de formulário** | rascunho | A aplicação usa o NDT para saber que campos existem e como estruturar a UI |
| **Renderização** | qualquer | O NDT é o único guia visual; o NDF fornece os dados |

### 6.7 Fidelidade por formato de saída

| Formato | Momento | Fidelidade de layout | Fidelidade de conteúdo | Fonte de layout |
|---|---|---|---|---|
| **PDF / PDF/A** | Arquivo, prova, entrega formal | **Normativa segundo o perfil de renderizador** | Total | Bloco `layout` |
| **ODF** | Intercâmbio, edição, revisão | Melhor esforço | Total | Bloco `estilos` |
| **HTML** | Publicação, intranet, consulta | Melhor esforço — CSS flow | Total | Bloco `estilos` |
| **Typst** | Composição avançada | Alta — coordenadas são dicas | Total | Bloco `layout` |

**Fidelidade de conteúdo** = texto, tabelas, listas, imagens e estrutura
semântica preservados identicamente. **Fidelidade de layout** = posições,
fontes, margens e paginação reproduzidas com exatidão.

PDF/A e ODF servem momentos distintos e **não são equivalentes**: PDF/A é
representação fixa preservável e verificável por hash; ODF é formato de
intercâmbio e trabalho editável. A identidade **binária** de um PDF só é
garantida por um perfil de renderizador que fixe motor, fontes, recursos,
versões e parâmetros de serialização.

Elementos sem equivalente em formatos de fluxo — `grelha_digitos`,
`tabela_visual`, `rectangulo`, `linha`, `min_linhas_visivel` e `assinatura` como
AcroForm — podem ser ignorados ou aproximados por renderizadores ODF/HTML, que
**devem declarar** essas aproximações no relatório de renderização.

### 6.8 Endereçamento de dados

Caminhos canónicos: sequência de segmentos separados por `.`, cada segmento
cumprindo `[A-Za-z_][A-Za-z0-9_-]*`. A raiz implícita é sempre
`NDF-core.documento`.

```text
identificacao.nif_titular          → NDF-core.documento.identificacao.nif_titular
quadro4.imoveis                    → array de linhas
quadro4.imoveis[i].freguesia       → propriedade de uma linha
```

A hierarquia é **convenção de endereçamento, não schema**: o NDT não valida se o
caminho existe nem o tipo do valor. Se o caminho não existir ou o valor for
nulo, **o elemento renderiza em branco — sem erro e sem aviso**.

Três espaços de tokens, distintos e coexistentes no mesmo campo:

| Token | O que é | Resolvido a partir de |
|---|---|---|
| `{{versao_ndt}}`, `{{schema_id}}`, `{{titulo}}`, `{{emissor}}` | Placeholders NDT | Cabeçalho do próprio NDT |
| `{{validation_code}}` | Valor de envelope | Envelope NDF, no momento da renderização |
| `{ndf:caminho.canonico}` | Valor de dados | NDF-core.documento |
| `{n}`, `{total}` | Tokens de paginação | Runtime do renderizador |

### 6.9 Formatos de apresentação

| Formato | Apresentação |
|---|---|
| `texto` | Valor tal qual (predefinição) |
| `numero` | Numérico com separador de milhar |
| `inteiro` | Sem casas decimais |
| `monetario` | Duas casas decimais e separador de milhar |
| `data` | DD/MM/YYYY |
| `data_hora` | DD/MM/YYYY HH:MM:SS + designação do desvio |
| `booleano` | ✓ / ✗ |
| `checkbox` | Caixa de verificação |
| `radio` | Ponto de seleção |

É **indicação visual**, não tipo de dados com validação.

**`data_hora` é determinístico e essa regra é normativa.** Um renderizador
**não deve** converter para o fuso local da máquina, do utilizador ou do
serviço: renderiza a data e a hora **tal como declaradas**, apresentando o
desvio.

| Valor no NDF | Renderização |
|---|---|
| `2026-06-18T09:10:00Z` | `18/06/2026 09:10:00 UTC` |
| `2026-06-18T10:10:00+01:00` | `18/06/2026 10:10:00 +01:00` |
| `2026-06-18T09:10:00.472Z` | `18/06/2026 09:10:00 UTC` — a fração é dado, não apresentação |

Converter destruiria a reprodutibilidade: dois renderizadores em fusos
diferentes produziriam páginas diferentes a partir do mesmo NDF.

### 6.10 Layout

Dimensões e coordenadas em **milímetros**; tamanho de fonte em **pontos
tipográficos**. `largura`, `altura` e `tamanho` devem ser estritamente
positivos.

```json
{
  "layout": {
    "formato": "A4",
    "orientacao": "portrait",
    "margens": { "topo": 20, "fundo": 20, "esq": 15, "dir": 15 }
  }
}
```

`formato`: `"A4"` | `"A3"` | `"Letter"` | `{largura, altura}` em mm.

#### `paginas_def[]`

A unidade fundamental é a **definição de página**. Cada página estruturalmente
distinta — rosto, página de dados, página de fecho — é uma `pagina_def` própria.
A repetição é controlada por `sequencia[]`.

Sistema de coordenadas partilhado: **milímetros, origem (0,0) no canto superior
esquerdo da área útil**, dentro das margens.

| Coleção | Propósito |
|---|---|
| `graficos[]` | Elementos visuais puros a coordenadas absolutas |
| `campos[]` | Valores NDF escalares a coordenadas absolutas |
| `blocos[]` | Conteúdo estruturado a coordenadas absolutas: tabelas, corpo de texto |
| `fluxo` | Elementos que se empilham verticalmente — para corpo de extensão variável |
| `mobilia[]` | Numeração de página, marca de água, textos de rodapé |

`fluxo` e `blocos[]` são **mutuamente exclusivos** na mesma `pagina_def`.
`graficos[]`, `campos[]` e `mobilia[]` coexistem com qualquer modelo.

#### Elementos gráficos

| `tipo` | Liga ao NDF? | Uso típico |
|---|---|---|
| `linha` | Não | Separadores, bordas |
| `rectangulo` | Não | Caixas de secção, molduras |
| `grelha_digitos` | **Sim** | Uma caixa por carácter — NIFs, datas, códigos postais |
| `imagem` | Não | Logótipos, brasões |
| `texto_fixo` | Não (aceita placeholders) | Títulos, legendas do impresso |
| `assinatura` | Não | Campo de assinatura eletrónica/manuscrita |
| `codigo_barras` | **Sim** | Código de validação (QR, Code128, EAN13) |
| `poligono` | Não | Setas, formas |
| `elipse` | Não | Círculos |
| `svg` | Não | Fundos vetoriais, gráficos complexos |
| `tabela_visual` | Não | Grelha estrutural do impresso |

Campos transversais a todos: `layer` (`background` | `content` | `foreground` |
`overlay`) e `rotacao` (graus, sentido horário).

O elemento `assinatura` tem um campo `modo` que controla a relação entre a
assinatura CAdES do NDF e o PDF gerado:

| `modo` | Comportamento no PDF |
|---|---|
| `visual_apenas` | Placeholder visual sem AcroForm. A assinatura vive no envelope NDF |
| `hibrido` (predefinição) | Cria campo AcroForm que suporta uma operação PAdES independente |
| `ndf_attachment` | Sem AcroForm; o CAdES é embutido como anexo PDF/A-3 (`ndf-signature.p7s`) |

**O URL de um `codigo_barras` é decisão do custodiante.** O endereço
`https://validar.normordis.pt/…` que aparece nos exemplos é ilustrativo — o
serviço de resolução para onde o QR aponta é escolhido pelo sistema
custodiante, não pelo formato nem pelo template (SPEC NDT §5.3.7). Um NDT
destinado a documentos classificados **não deve** assumir por omissão o URL de
um serviço público de verificação; o endereço a codificar, ou a própria
presença do elemento, é decisão explícita do custodiante (SPEC NDF §4.7.2).

#### Layout de fluxo

Para documentos onde o corpo tem extensão variável — ofícios, relatórios,
informações — os elementos que se seguem ao corpo precisam de aparecer *depois
de onde o corpo terminar*, não em coordenadas fixas.

```json
{
  "fluxo": {
    "y_inicio": 60,
    "elementos": [
      { "tipo": "corpo", "referencia": "corpo" },
      { "tipo": "espaco", "altura": 10 },
      { "tipo": "texto_fixo", "conteudo": "Com os melhores cumprimentos," },
      { "tipo": "espaco", "altura": 20 },
      { "tipo": "assinatura", "id": "sig_autor", "rotulo": "O Dirigente", "largura": 80, "altura": 25 },
      { "tipo": "campo", "referencia": "signatario.nome" },
      { "tipo": "campo", "referencia": "signatario.cargo" }
    ]
  }
}
```

Tipos admitidos em `fluxo.elementos`: `corpo` (único por fluxo), `tabela`,
`texto_fixo`, `campo`, `imagem`, `espaco`, `separador`, `assinatura`,
`linha_lateral`, `quebra_pagina`. Todos aceitam `incluir_se`.

**Regra de extravasamento:** quando o `corpo` não cabe na área disponível, o
extravasamento é gerido por `sequencia[]`. Os elementos **posteriores** ao
`corpo` são renderizados na **última página** da sequência, imediatamente após o
fim do corpo; os **anteriores**, apenas na primeira instância da `pagina_def`.

`linha_lateral` agrupa elementos lado a lado — blocos de dupla assinatura, por
exemplo. Não é aninhável e não admite `corpo` no conteúdo de uma coluna; a soma
das larguras não pode exceder a largura útil.

#### Blocos de conteúdo

`tabela` renderiza um array NDF como tabela; as colunas são definidas no NDT com
layout visual, os valores vêm do NDF.

**Regra `min_linhas_visivel`:** o renderizador **desenha sempre** a estrutura da
tabela — moldura, cabeçalho, linhas — e completa com linhas em branco quando o
NDF tiver menos itens. É o que garante que impressos fiscais apresentam as
linhas oficiais mesmo sem dados.

`corpo` renderiza um valor NCRTF a partir de um caminho NDF, com extravasamento
gerido por `sequencia[]`.

#### Sequenciamento

`paginas_def[]` descreve **modelos**; `sequencia[]` determina a ordem e o número
de instâncias.

| Modo de `repeticao` | Comportamento |
|---|---|
| `unica` | Exatamente uma instância |
| `por_linha` | Uma instância por item do array `fonte_overflow` |
| `conforme_necessario` | Repete enquanto houver itens ou conteúdo por colocar; exige `fonte_overflow` |

```json
{
  "sequencia": [
    { "pagina_def": "oficio_pag1", "repeticao": "unica" },
    { "pagina_def": "oficio_pag_seguinte", "repeticao": "conforme_necessario", "fonte_overflow": "corpo" }
  ]
}
```

#### Recursos

Cada recurso usa um de dois modos:

| Modo | Campos obrigatórios |
|---|---|
| `embebido` | `dados` (base64 com prefixo `"base64:"`) |
| `referenciado_por_hash` | `hash_sha256` e `content_type` |

Recursos de tipo fonte (`fonte_ttf`, `fonte_otf`) exigem `familia`. Qualquer
família tipográfica que não seja `Helvetica`, `Times` ou `Courier` **deve** ser
declarada em `recursos[]`.

**Mapeamento NCRTF ↔ NDT:**

| NCRTF `font_family` | NDT `familia` | Classe |
|---|---|---|
| `LiberationSans` | `Helvetica` | Sem serifas |
| `LiberationSerif` | `Times` | Com serifas |
| `LiberationMono` | `Courier` | Monospace |

Fontes declaradas em `recursos[]` com o mesmo nome canónico têm precedência
sobre esta tabela.

### 6.11 Acessibilidade — PDF/UA-2

O perfil PDF acessível tem como alvo **PDF/UA-2** (ISO 14289-2, sobre PDF 2.0).

| Requisito | Implicação NDT/NDF |
|---|---|
| Estrutura lógica com tags | O renderizador infere tags de `blocos[]` e `fluxo.elementos`; tabelas geram `/Table` com `/THead` e `/TBody` |
| Ordem de leitura | Gerada da sequência lógica; gráficos decorativos marcados `Artifact` |
| Texto alternativo | `alt` em `imagem` e `svg`; `alt: ""` para elementos puramente decorativos |
| Idioma do documento | De `NDF.metadados.idioma`; com `idiomas_autenticos`, `/Lang` refere a versão apresentada |
| Fontes embebidas | Todas em `recursos[]` ou standard com `ToUnicode` |
| Campos com legenda | `rotulo_acessivel` → `/TU` no AcroForm; **obrigatório** em `checkbox` e `radio` |

PDF/UA-2 e PDF/A-3 são compatíveis: um mesmo ficheiro admite conformidade
simultânea, sujeita à validação independente de cada perfil.

### 6.12 Dois perfis de documento

| Perfil | Blocos determinantes | Exemplos |
|---|---|---|
| **Impresso** | `graficos[]`, `campos[]`, `blocos[]` a coordenadas absolutas | Modelo 3 IRS e demais impressos fiscais |
| **Texto corrido** | `estilos`, `fluxo`, `corpo` NCRTF, `sequencia[]` | Ofício, informação, parecer, despacho, diploma legal |

No impresso a geometria **é** o documento oficial e a extensão do conteúdo é
conhecida ao desenhar o template. No texto corrido a extensão é arbitrária: o
template fixa estrutura e estilo, e a paginação resulta do conteúdo. Um template
pode combinar os dois perfis — a distinção organiza a leitura dos requisitos,
não cria classes de conformidade separadas.

### 6.13 Fluxo de renderização

1. Verificar a conformidade estrutural do NDF e ler `ndt_version_ref`.
2. Resolver o NDT no `.ndfpkg` ou no domínio de custódia.
3. Verificar o hash do NDT contra o manifesto ou catálogo imutável.
4. Confirmar `schema_id@versao_ndt == ndt_version_ref`.
5. Resolver caminhos relativamente a `NDF-core.documento`.
6. Combinar NDT + NDF e produzir a saída pedida.

Sem o NDT exato, os dados continuam legíveis, mas a renderização **não deve**
ser declarada reprodutível. Reprodutibilidade visual não implica identidade
binária.

### 6.14 Exemplo — ofício de fluxo

```json
{
  "ndt_version": "2.0.0",
  "schema_id": "oficio-generico",
  "versao_ndt": "2.0.0",
  "titulo": "Ofício Genérico",
  "estilos": {
    "fonte_padrao": { "familia": "Times", "tamanho": 11 },
    "cor_texto": "#1A1A1A",
    "cor_primaria": "#003366",
    "espacamento_entre_paragrafos_mm": 4,
    "identacao_lista_mm": 6,
    "cabecalhos": [
      { "nivel": 1, "fonte": { "tamanho": 14, "peso": "bold" } },
      { "nivel": 2, "fonte": { "tamanho": 12, "peso": "bold" } }
    ]
  },
  "layout": {
    "formato": "A4",
    "orientacao": "portrait",
    "margens": { "topo": 20, "fundo": 20, "esq": 20, "dir": 20 }
  },
  "recursos": [
    {
      "id": "brasao-republica.svg",
      "tipo": "svg",
      "modo": "referenciado_por_hash",
      "hash_sha256": "sha256:32c937bf849181d3799a656e088b304f575311b141e557aba7682e50b38c3316",
      "content_type": "image/svg+xml"
    }
  ],
  "paginas_def": [
    {
      "id": "oficio_pag1",
      "graficos": [
        {
          "tipo": "imagem",
          "referencia_recurso": "brasao-republica.svg",
          "posicao": { "x": 0, "y": 0 },
          "largura": 25, "altura": 25,
          "manter_proporcao": true,
          "alt": "Brasão da República Portuguesa"
        },
        {
          "tipo": "linha",
          "de": { "x": 0, "y": 35 }, "para": { "x": 170, "y": 35 },
          "espessura": 0.5, "cor": "#003366", "estilo": "solido"
        },
        {
          "tipo": "codigo_barras",
          "formato_barras": "qrcode",
          "conteudo": "https://validar.normordis.pt/{{validation_code}}",
          "posicao": { "x": 145, "y": 5 },
          "largura": 22, "altura": 22,
          "nivel_correcao": "M"
        }
      ],
      "campos": [
        {
          "referencia": "numero",
          "posicao": { "x": 30, "y": 2 }, "largura": 110, "altura": 6,
          "fonte": { "familia": "Helvetica", "tamanho": 9 }
        },
        {
          "referencia": "data",
          "posicao": { "x": 30, "y": 18 }, "largura": 110, "altura": 6,
          "formato": "data"
        }
      ],
      "fluxo": {
        "y_inicio": 60,
        "elementos": [
          { "tipo": "corpo", "referencia": "corpo" },
          { "tipo": "espaco", "altura": 10 },
          { "tipo": "texto_fixo", "conteudo": "Com os melhores cumprimentos," },
          { "tipo": "espaco", "altura": 20 },
          { "tipo": "assinatura", "id": "sig_autor", "rotulo": "O Director-Geral", "largura": 80, "altura": 25 },
          { "tipo": "campo", "referencia": "signatario.nome" },
          { "tipo": "campo", "referencia": "signatario.cargo" }
        ]
      },
      "mobilia": [
        {
          "tipo": "texto_fixo",
          "conteudo": "Proc. {ndf:numero} — Pág. {n}/{total}",
          "posicao": { "x": 0, "y": 265 },
          "fonte": { "familia": "Helvetica", "tamanho": 8 }
        }
      ]
    }
  ],
  "sequencia": [
    { "pagina_def": "oficio_pag1", "repeticao": "unica" }
  ]
}
```

Exemplos no repositório: [`specs/ndt/examples/`](specs/ndt/examples/) —
`oficio-generico.ndt.json`, `documento-capturado.ndt.json`,
`modelo3-irs-rosto.ndt.json`, `modelo3-irs-anexoA.ndt.json`,
`modelo3-irs-anexoG.ndt.json`.

---

## 7. NCRTF — NORMORDIS Canonical Rich Text Format

**Especificação:** [`specs/ncrtf/SPEC.md`](specs/ncrtf/SPEC.md) · **Schema:**
[`specs/ncrtf/schemas/ncrtf.schema.json`](specs/ncrtf/schemas/ncrtf.schema.json)

### 7.1 Propósito

Formato de texto estruturado com cinco objetivos, por ordem de prioridade:

1. **Canónico** — a mesma estrutura lógica produz sempre os mesmos bytes JSON,
   compatível com JCS e assinável como parte de um NDF-core.
2. **Independente de implementação** — não pressupõe Lexical, ProseMirror,
   Tiptap, Quill ou qualquer outro editor. Os editores são **adaptadores de
   entrada e saída**, não formatos persistentes normativos.
3. **Eficiente como conteúdo NDF** — é um objeto JSON guardado diretamente num
   campo de `documento`, sem codificação adicional.
4. **Legível por máquina sem renderizador** — a estrutura de nós é
   interpretável sem CSS, fontes ou motores de layout.
5. **Interoperável** — produtores, editores, validadores e renderizadores
   independentes trocam o mesmo conteúdo sem preservar estado proprietário.

### 7.2 O que o NCRTF representa

- Texto com formatação inline: negrito, itálico, sublinhado, riscado, código,
  subscrito, sobrescrito
- Parágrafos, títulos estruturados e citações em bloco
- Listas ordenadas, não ordenadas e de verificação, com aninhamento real
- Tabelas com cabeçalho opcional e células com conteúdo inline
- Imagens referenciadas por caminho dentro do `.ndfpkg`
- Ligações hipertexto inline
- Quebras de linha forçadas
- Alinhamento, indentação e família tipográfica por bloco ou por nó inline

### 7.3 O que o NCRTF **não** representa

| O quê | Onde fica |
|---|---|
| O ato jurídico completo | NDF-core (`documento`) |
| Regras de validação e cálculo | Aplicação de domínio |
| Layout de página — margens, tipografia, logótipos | Bloco `layout` do NDT |
| Metadados do documento | NDF-core (`metadados`) |
| Assinatura e envelope de custódia | Envelope NDF |
| PDF/UA-2, ODF, HTML | Artefactos derivados |
| Estado interno de editor | Formato proprietário do editor |
| **Imagens em base64 ou data URL** | `recursos/` do `.ndfpkg`, referenciadas por `ref` |
| **Blocos dentro de células de tabela** | Não admitido — as células contêm inline |
| **Nós de tipo desconhecido** | Schema fechado; o leitor rejeita |

### 7.4 Estrutura raiz

```json
{
  "ncrtf_version": "2.0.0",
  "content": [
    { "type": "paragraph", "content": [ { "type": "text", "text": "Primeiro bloco." } ] }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `ncrtf_version` | Sim | `"2.0.0"` nesta versão |
| `content` | Sim | Array de blocos, **mínimo 1 elemento** |

Campos adicionais na raiz são proibidos (`additionalProperties: false`).

### 7.5 Hierarquia de nós

```text
Documento
└── content: Bloco[]
    ├── paragraph     → content: Inline[]     alignment?, indent?, font_family?
    ├── heading       → content: Inline[]     level (1–3), alignment?, font_family?
    ├── list          → content: ListItem[]   list_type
    │     ListItem  → content: (Inline | list)[]   checked? (checklist)
    ├── blockquote    → content: Inline[]     alignment?, font_family?
    ├── table         → head?: TableRow[], body: TableRow[]
    │     TableRow  → cells: TableCell[]
    │     TableCell → content: Inline[]
    └── image                                  ref, alt, caption?, width_percent?

Inline = text | link | hard_break
text   = { type, text, marks?, font_family? }
link   = { type, href, content: text[], title?, target? }
```

### 7.6 Nós bloco

#### `paragraph`

```json
{
  "type": "paragraph",
  "alignment": "justify",
  "indent": 1,
  "font_family": "LiberationSerif",
  "content": [ { "type": "text", "text": "Texto com formatação de bloco." } ]
}
```

`alignment` admite `center` | `justify` | `right` — **omitir** quando `left`
(predefinição). `indent` é inteiro ≥ 1 — **omitir** quando 0.

#### `heading`

```json
{ "type": "heading", "level": 2, "content": [ { "type": "text", "text": "Enquadramento" } ] }
```

`level` é inteiro 1–3. Em documentos administrativos, recomenda-se reservar o
nível 1 ao NDT (layout); o conteúdo editorial começa em `level: 2`.

#### `list` e `list_item`

```json
{
  "type": "list",
  "list_type": "ordered",
  "content": [
    { "type": "list_item", "content": [ { "type": "text", "text": "Primeiro item." } ] },
    {
      "type": "list_item",
      "content": [
        { "type": "text", "text": "Segundo item, com sub-lista:" },
        {
          "type": "list",
          "list_type": "bullet",
          "content": [
            { "type": "list_item", "content": [ { "type": "text", "text": "Sub-item A." } ] }
          ]
        }
      ]
    }
  ]
}
```

`list_type`: `bullet` | `checklist` | `ordered`. Em `checklist`, **cada**
`list_item` deve ter `checked` explicitamente `true` ou `false` — `false` é
semanticamente relevante e **não se omite**.

Uma lista aninhada aparece **após** os inlines do item pai.

#### `blockquote`

```json
{ "type": "blockquote", "content": [ { "type": "text", "text": "Citação do documento referenciado." } ] }
```

#### `table`

As células contêm **inline, não blocos**:

```json
{
  "type": "table",
  "head": [
    { "cells": [
      { "type": "table_cell", "content": [ { "type": "text", "text": "Data" } ] },
      { "type": "table_cell", "content": [ { "type": "text", "text": "Diligência" } ] }
    ] }
  ],
  "body": [
    { "cells": [
      { "type": "table_cell", "content": [ { "type": "text", "text": "2026-06-01" } ] },
      { "type": "table_cell", "content": [ { "type": "text", "text": "Notificação ao requerente" } ] }
    ] }
  ]
}
```

- `body` é obrigatório, mínimo 1 linha; `head` é opcional — **omitir** quando
  ausente, nunca `[]`.
- Todas as linhas devem ter o mesmo número de células.
- Parágrafos, listas, imagens e tabelas aninhadas **não** são admitidos numa
  célula.
- **Uma célula sem conteúdo não é representável, e é intencional.** Numa tabela
  em que todas as linhas têm o mesmo número de células, a célula que nada contém
  é ainda assim uma posição declarada: o produtor declara o que lá está — um
  traço, um `n.a.`, um zero — em vez de deixar ao renderizador a decisão de como
  mostrar uma ausência.

#### `image`

```json
{
  "type": "image",
  "ref": "recursos/grafico-1.png",
  "alt": "Gráfico de evolução trimestral de processos",
  "caption": "Figura 1 — Evolução 2024–2026",
  "width_percent": 75
}
```

`ref` é caminho relativo dentro do `.ndfpkg`; `alt` é obrigatório (pode ser
string vazia se puramente decorativa); `width_percent` é inteiro 25–100. É um
**nó folha** — não tem `content`.

### 7.7 Nós inline

| Nó | Campos |
|---|---|
| `text` | `text` (string **não vazia**), `marks?`, `font_family?` |
| `link` | `href`, `content` (array de `text`, sem links aninhados), `title?`, `target?` (`_blank` \| `_self`) |
| `hard_break` | apenas `type` — quebra de linha dentro de um bloco, distinta de novo parágrafo |

### 7.8 Marcas

| Marca | Renderização | Nota |
|---|---|---|
| `bold` | Negrito | |
| `code` | Monospace inline | Fragmentos de código, identificadores técnicos |
| `italic` | Itálico | |
| `strikethrough` | Riscado | Correções, atas, retificações |
| `subscript` | Subscrito | **Não** coexiste com `superscript` no mesmo nó |
| `superscript` | Sobrescrito | **Não** coexiste com `subscript` no mesmo nó |
| `underline` | Sublinhado | |

**Ordem canónica obrigatória** (alfabética):

```text
bold → code → italic → strikethrough → subscript → superscript → underline
```

Produtores ordenam antes de serializar; leitores **rejeitam** documentos com
`marks` fora desta ordem.

### 7.9 Famílias de tipo

`font_family` admite `LiberationMono`, `LiberationSans`, `LiberationSerif` —
nomes canónicos independentes de implementação. Declarada num bloco, aplica-se
aos nós `text` filhos que não declarem a sua; a do nó `text` tem precedência.

### 7.10 Regras de canonicalização

Todo o valor NCRTF é canonicalizado via JCS antes de entrar nos
`payload_bytes`. Além disso, seis restrições estruturais:

| Regra | Descrição |
|---|---|
| **R1** | `marks` em ordem canónica |
| **R2** | Nós `text` contíguos com marcas **e** `font_family` idênticos devem ser **fundidos** num único nó |
| **R3** | Campos com valor igual ao default não devem estar presentes: `alignment` quando `left`, `indent` quando `0` |
| **R4** | Arrays vazios não devem estar presentes — omitir o campo em vez de `[]`. Exceção: `checked: false` é semanticamente relevante |
| **R5** | `text` não deve ser string vazia |
| **R6** | `subscript` e `superscript` não coexistem no mesmo nó |

Verificação exigida ao produtor:

```text
JCS(parse(serialize(ncrtf))) == serialize(ncrtf)
```

### 7.11 Integração com o NDT

O NDT **não contém NCRTF**. Declara apenas a posição e o caminho onde o valor
NCRTF reside:

```json
{ "tipo": "corpo", "referencia": "corpo", "posicao": { "x": 15, "y": 60 }, "largura": 180 }
```

ou, em fluxo:

```json
{ "tipo": "corpo", "referencia": "corpo" }
```

**Princípio:** o NCRTF vive no NDF; o NDT descreve onde e como renderizá-lo; o
renderizador é o único componente que conhece ambos.

### 7.12 Integração com o `.ndfpkg`

O `ref` de uma imagem deve:

- ser relativo à raiz do `.ndfpkg`;
- usar `/` como separador, independentemente do SO;
- referenciar um ficheiro presente no arquivo;
- ter entrada correspondente em `manifest.inventario`.

| Formato | Extensão | Nota |
|---|---|---|
| PNG | `.png` | Recomendado para gráficos e diagramas |
| SVG | `.svg` | Recomendado para vetorial; renderizadores **devem sanitizar** |
| JPEG | `.jpg` / `.jpeg` | Recomendado para fotografias |
| PDF/A | `.pdf` | Opcional — sub-documentos em imagem |

**Fluxo recomendado para editores:** durante a edição, imagens mantidas
internamente como data URL no estado do editor; **na finalização**, extraídas
para `recursos/` e o `src` substituído por `ref` no valor que vai para
`ndf-core.json`.

### 7.13 Extensibilidade

| Mudança | Versão |
|---|---|
| Novo tipo de nó bloco opcional | MINOR |
| Nova marca opcional | MINOR |
| Novo campo opcional num nó existente | MINOR |
| Alteração de campo obrigatório / remoção de nó | MAJOR |
| Alteração das regras de canonicalização | MAJOR |

O schema é **fechado**: um leitor conforme rejeita tipos de nó desconhecidos.
Uma versão minor pode acrescentar um nó opcional, mas o documento que o use
declara essa versão. **Um leitor nunca ignora silenciosamente conteúdo assinado
que não compreende.**

### 7.14 Exemplo completo

```json
{
  "ncrtf_version": "2.0.0",
  "content": [
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Em resposta ao ofício n.º 45/2026, cumpre-nos informar o seguinte:" }
      ]
    },
    {
      "type": "heading",
      "level": 2,
      "content": [ { "type": "text", "text": "Enquadramento" } ]
    },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Nos termos do artigo " },
        { "type": "text", "text": "62.º do CPA", "marks": ["bold"] },
        { "type": "text", "text": ", o prazo de decisão é de " },
        { "type": "text", "text": "90 dias", "marks": ["bold"] },
        { "type": "text", "text": "." }
      ]
    },
    {
      "type": "table",
      "head": [
        { "cells": [
          { "type": "table_cell", "content": [ { "type": "text", "text": "Data" } ] },
          { "type": "table_cell", "content": [ { "type": "text", "text": "Diligência" } ] },
          { "type": "table_cell", "content": [ { "type": "text", "text": "Estado" } ] }
        ] }
      ],
      "body": [
        { "cells": [
          { "type": "table_cell", "content": [ { "type": "text", "text": "2026-06-01" } ] },
          { "type": "table_cell", "content": [ { "type": "text", "text": "Notificação ao requerente" } ] },
          { "type": "table_cell", "content": [ { "type": "text", "text": "Concluída" } ] }
        ] }
      ]
    },
    {
      "type": "list",
      "list_type": "ordered",
      "content": [
        { "type": "list_item", "content": [ { "type": "text", "text": "Certidão de teor do registo predial" } ] },
        { "type": "list_item", "content": [ { "type": "text", "text": "Comprovativo de NIF actualizado" } ] }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "O coeficiente aplica-se conforme V = V" },
        { "type": "text", "text": "0", "marks": ["subscript"] },
        { "type": "text", "text": " × (1 + r)" },
        { "type": "text", "text": "n", "marks": ["superscript"] },
        { "type": "text", "text": ", onde " },
        { "type": "text", "text": "r", "marks": ["italic"] },
        { "type": "text", "text": " é a taxa anual." }
      ]
    }
  ]
}
```

Exemplo no repositório:
[`specs/ncrtf/examples/oficio-corpo.ncrtf.json`](specs/ncrtf/examples/oficio-corpo.ncrtf.json).

---

## 8. Registo de tipos e perfis

**Especificação:** [`specs/registry/SPEC.md`](specs/registry/SPEC.md)

### 8.1 Propósito

O registo define o mecanismo de resolução de `tipo_documento_ref` — cada entrada
é um JSON Schema Draft 2020-12 que valida o conteúdo de `documento` para um tipo
específico. Mantém também os **perfis de avaliação arquivística** referenciados
por `avaliacao.perfil`.

Destina-se a **formas documentais transversais** — as que atravessam organismos e
cuja estrutura é matéria de normalização. **Não** se destina a acomodar a
tipologia própria de cada entidade: mantê-la centralmente produziria um número
indeterminado de tipos sem capacidade nem legitimidade de manutenção, e um
registo não mantido deixa de ser fonte de verdade. Para esses casos existe a
extensão qualificada (§2.7).

### 8.2 Formato do identificador

```text
<id>@<versao>
```

| Componente | Regras | Exemplos |
|---|---|---|
| `id` | Minúsculas, hífens, estável entre versões | `oficio`, `informacao-tecnica`, `despacho`, `parecer`, `modelo3-irs` |
| `versao` | SemVer para tipos normativos; `YYYY.N` para impressos anuais | `1.0.0`, `2026.1` |

### 8.3 Tipos canónicos

| `tipo_documento_ref` | Descrição |
|---|---|
| `oficio@1.0.0` | Ofício — comunicação formal externa |
| `informacao-tecnica@1.0.0` | Informação técnica — nota interna fundamentada |
| `parecer@1.0.0` | Parecer — apreciação fundamentada com sentido explícito, sobre outro documento |
| `despacho@1.0.0` | Despacho — decisão ou instrução de serviço |
| `documento-capturado@1.0.0` | Documento cujo conteúdo reside em componentes binários |
| `aceitacao-custodia@1.0.0` | Aceitação de custódia — resposta do recetor a um conjunto de transferência |

`informacao-tecnica`, `parecer` e `despacho` formam, com `relacoes[]`, a cadeia
**Informação → Parecer → Despacho**: três NDF autónomos ligados por relações
verificáveis, **nunca** um único documento com secções sucessivamente assinadas.

`documento-capturado` é **um** tipo genérico, e não uma família
(`oficio-capturado`, `parecer-capturado`, …): o campo opcional
`tipo_equivalente` transporta a correspondência com o tipo nativo sem duplicar o
registo.

### 8.4 Estrutura de `documento-capturado`

Campos obrigatórios: `assunto`, `data`, `componentes`, `reconstituicao`.

| Campo | Descrição |
|---|---|
| `numero` | Número ou referência, quando exista |
| `data` | Data do documento tal como o produtor o emitiu — **não** a data de captura |
| `assunto` | Afirmado na captura, não extraído do binário |
| `destinatario`, `referencias` | Descritivos |
| `tipo_equivalente` | Tipo nativo correspondente, quando determinável — serve a medida de progresso da transição |
| `componentes[]` | Ver §3.9 |
| `reconstituicao` | `{estado, fundamento?}` — `adequada` \| `adequada_com_deficiencia` \| `ausente`; `fundamento` obrigatório nos dois últimos |
| `proveniencia_submissao` | `{canal, canal_detalhe?, recebido_em, protocolo?, submissor_ref?, autenticacao?}` |
| `verificacao_assinaturas[]` | `{componente_id, tipo, resultado, verificado_em, material_ref?}` — resultado **no instante da captura**, não promessa de verificabilidade futura |

`proveniencia_submissao.canal`: `e_balcao`, `digitalizacao`,
`correio_eletronico`, `transferencia_sistema`, `presencial`, `outro` (com
`canal_detalhe` obrigatório).

A ausência de `material_ref` numa verificação de assinatura significa que a
verificabilidade dessa assinatura contida **caduca com os certificados**.

### 8.5 Perfis de avaliação registados

| Perfil | Âmbito | Schema |
|---|---|---|
| `pt-dglab` | Administração Pública portuguesa — MEG/DGLAB | [`specs/registry/profiles/pt-dglab.schema.json`](specs/registry/profiles/pt-dglab.schema.json) |
| `generic` | Sem restrições jurisdicionais | [`specs/registry/profiles/generic.schema.json`](specs/registry/profiles/generic.schema.json) |

Perfis já mapeados mas ainda **sem schema publicado** — `fr-siaf`, `de-barch`,
`nl-na`, `eu-ec` — estão documentados em [`docs/profiles/`](docs/profiles/).

### 8.6 Resolução de `tipo_documento_ref`

Ordem de precedência:

1. **`.ndfpkg`** — schema presente no pacote;
2. **Registo local** — cópia dos schemas canónicos mantida pela implementação;
3. **Registo remoto** (roadmap) — URI canónico.

### 8.7 Via de produção admissível por tipo

Um documento nasce por duas vias: **estruturada** (editor que produz `documento`
tipado, com NDT e NCRTF) ou **capturada** (binário emitido fora do sistema e
preservado como componente).

Cada entrada do registo **pode** declarar:

| Campo | Valores | Significado |
|---|---|---|
| `via_predefinida` | `estruturada` \| `capturada` | Via proposta por omissão |
| `captura_admissivel` | `true` \| `false` | Se o tipo aceita `documento-capturado` como forma válida |

Na ausência de declaração, o tipo não impõe restrição.

**Roquete, não interruptor.** A transição é unidirecional por desenho:
`captura_admissivel` move-se de `true` para `false` quando o editor passa a
cobrir o tipo; voltar atrás exige justificação expressa e registada, com data e
responsável. Sem esta regra, o regime de transição converter-se-ia em permanente
por inércia.

Alterar qualquer dos dois campos é alteração **do registo**, não do NDF-core:
nenhum documento já produzido é afetado, porque a declaração governa a produção
futura.

---

## 9. Custódia, transferência e verificação pública

### 9.1 Perfil de Ciclo de Vida NORMORDIS — **opcional**

> **Aviso de âmbito.** Tudo o que se segue nesta subsecção **não é requisito de
> conformidade NDF**. É um perfil operacional opcional, com requisitos próprios
> (`CUST-REQ-*`). Um produtor ou leitor NDF conforme pode adotar o seu próprio
> modelo de gestão de ciclo de vida, desde que preserve a imutabilidade dos
> `payload_bytes`.

#### Estados do ciclo de vida

Geridos pelo sistema de custódia **fora do NDF-core**. O `estado` do core é
sempre `"ativo"` — o do momento da finalização.

```text
ativo → substituido                            (nova versão NDF criada)
ativo → em_conservacao                         (PCA decorrido)
em_conservacao → conservado_permanentemente    (DF: conservação)
em_conservacao → eliminado                     (DF: eliminação autorizada)
```

| Estado | Descrição |
|---|---|
| `ativo` | Em uso, dentro do prazo. Estado inicial de todos os NDF |
| `substituido` | Supersedido por nova versão. Imutável no arquivo; não é o corrente |
| `em_conservacao` | Prazo decorrido; aguarda aplicação do destino final |
| `conservado_permanentemente` | Destino aplicado: conservação permanente |
| `eliminado` | Destino aplicado: eliminação. Subsiste um evento terminal no log |

#### Log de custódia

**Schema:** [`specs/ndf/schemas/custody-event.schema.json`](specs/ndf/schemas/custody-event.schema.json)

Cada transição é registada num log de auditoria imutável, separado do NDF e da
base de dados operacional, com **cadeia de hash encadeado**:

```text
event_hash = SHA-256( JCS( evento sem a propriedade event_hash ) )
```

No primeiro evento, `sequence` é `0` e `previous_event_hash` é `null`; nos
seguintes, `sequence` incrementa exatamente uma unidade e `previous_event_hash`
coincide com o `event_hash` anterior.

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
  "previous_event_hash": "sha256:9f2c1a7b…",
  "event_hash": "sha256:3a7bd3e2…"
}
```

**`event_type` (enum fechado):** `capturado`, `recebido`, `finalizado`,
`verificado`, `exportado`, `estado_alterado`, `assinatura_renovada`,
`selo_acrescentado`, `transferido`, `eliminado`.

Distinções importantes:

- **`capturado`** — os bytes entram em custódia antes de o NDF ser finalizado.
  É tipicamente o evento de `sequence` 0, seguido de `finalizado`. Um documento
  cujo conteúdo seja estruturado **não** tem evento de captura.
- **`recebido`** — um documento vindo de outra entidade não é capturado nem
  finalizado por quem o recebe: já existe, com identidade, assinatura e história
  próprias. Um recetor **não deve** registar `capturado` — seria declarar uma
  produção que não ocorreu.
- **`verificado`** — verificação periódica de fixidez, com os digests em
  `details.componentes_verificados`. Um objeto sem histórico de verificações tem
  **uma** verificação, não uma história de verificações — e é a história que
  sustenta a alegação de preservação.

**As cadeias de custódia são por custodiante, não globais.** A do recetor começa
em `sequence` 0 com `previous_event_hash` `null` e **não** continua a do
transmitente: o recetor não detém os eventos anteriores, e encadeá-los sem os
deter exigiria falsificá-los. O que liga as cadeias não é criptográfico, é
documental — a evidência de custódia transferida e o documento de aceitação. Um
leitor que tenha apenas uma cadeia tem a história **desse** custodiante e **não
deve** apresentá-la como sendo a história do documento.

**Ancoragem.** A cabeça da cadeia deve ser periodicamente ancorada em
armazenamento WORM, selo institucional ou serviço temporal. Uma cadeia de hashes
**sem âncora externa** não impede reescrita integral por um custodiante
comprometido.

#### Evento terminal de eliminação

Quando o estado transita para `eliminado`, um sistema que implemente o perfil:

1. destrói `payload_bytes` e todos os campos do envelope **exceto**
   `validation_code` e `payload_hash`;
2. destrói **todos os componentes binários** declarados em `documento` — um
   documento cujo conteúdo resida em componentes não fica eliminado pela
   destruição do core; a eliminação é operação **única e indivisível** sobre o
   documento inteiro;
3. regista um evento terminal com `event_type: "eliminado"`, conservando em
   `details` a evidência mínima: `payload_hash`, `validation_code`, motivo,
   `instrumento_ref`, `classificacao_ref`, `autorizado_por` e os **digests dos
   componentes destruídos**.

Os digests provam o que existiu, sem que os bytes subsistam nem sejam
reconstituíveis a partir do digest.

#### Evidência transferível vs. auditoria interna

| Evento | Classe |
|---|---|
| `capturado`, `recebido`, `finalizado`, `estado_alterado`, `assinatura_renovada`, `selo_acrescentado`, `verificado`, `transferido`, `eliminado` | **Evidência transferível** |
| `exportado` | Auditoria interna do custodiante |

`verificado` é deliberadamente transferível: é o histórico de fixidez que
sustenta a alegação de preservação, e omiti-lo esvaziaria a transferência
daquilo que a torna útil.

**A omissão é detetável, e é essa a garantia.** Uma cadeia de que se tenham
retirado eventos apresenta saltos de `sequence` e uma ligação de hash que não
fecha. A entidade recetora sabe sempre **que** algo foi retido, ainda que não
saiba o quê. Daqui decorre `CUST-REQ-004`: os eventos transferem-se íntegros e
não editados, e a cadeia **não deve** ser renumerada ou recomposta para
dissimular omissões.

### 9.2 Evidência de custódia transferível

**Schema:** [`specs/ndf/schemas/evidencia-custodia.schema.json`](specs/ndf/schemas/evidencia-custodia.schema.json)

Extrato **atestado** da cadeia de custódia de uma unidade, para acompanhar uma
transferência. **Não é uma cadeia:** é objeto novo, selado pelo transmitente,
que declara o que transferiu e o que reteve. Transferir a cadeia com menos
eventos seria mutilá-la — a divulgação parcial resolve-se por objeto novo, nunca
por mutilação.

| Campo | Descrição |
|---|---|
| `evidencia_version` | `"1.0.0"` |
| `ndf_id` | Unidade a que respeita |
| `extraida_em` | Instante da extração — a evidência descreve a cadeia **nesse momento** |
| `politica_extracao` | `{id, tipos[]}` — política declarada, **não** seleção caso a caso. `tipos` **deve incluir** `finalizado` |
| `cadeia` | `{eventos_total, ultimo_event_hash}` — afirmação do transmitente, coberta pelo selo |
| `eventos[]` | Eventos transferidos, íntegros e não editados, por `sequence` crescente. **As sequências podem ter saltos** — é isso que torna a omissão visível |
| `omitidos` | `{contagem, fundamento}` — `fundamento` obrigatório **mesmo com contagem zero** |

Declara-se uma **política**, e não uma seleção caso a caso, porque a mesma
política vale para toda a transferência: a omissão fica auditável por comparação
entre unidades, em vez de depender do fundamento escrito para cada documento.

`tipos` deve incluir `finalizado` porque, sem ele, o extrato não estabelece
quando o documento se tornou imutável — deixa de ser evidência de custódia para
ser uma lista de acontecimentos.

**Limitação declarada, não escondida:** `eventos_total` e `ultimo_event_hash`
são afirmação do transmitente. Um recetor não os pode provar sem confiar nele.

### 9.3 Conjunto de transferência (`.ndfxfer`)

> **Estado:** desenho, materializado para poder ser exercitado. **Não** é
> requisito de conformidade NDF e não faz parte da SPEC. Ver
> [`docs/design/NDF-CONJUNTO-DE-TRANSFERENCIA.md`](docs/design/NDF-CONJUNTO-DE-TRANSFERENCIA.md).

**Problema que resolve:** o `.ndfpkg` é a unidade de **um documento**. Quando se
transfere um conjunto de documentos para outra entidade, N pacotes soltos não
permitem ao recetor afirmar que recebeu tudo.

```text
processo-789-2026.ndfxfer (ZIP)
├── transferencia.json           — declaração do conjunto e do seu fecho
├── transferencia-envelope.json  — selo da entidade transmitente
├── evidencia/
│   └── <ndf_id>.evidencia.json  — evidência de custódia por unidade
└── unidades/
    └── <nome livre>.ndfpkg      — um pacote por unidade documental
```

**Schema:** [`specs/ndf/schemas/transferencia.schema.json`](specs/ndf/schemas/transferencia.schema.json)

| Campo | Descrição |
|---|---|
| `ndfxfer_version` | `"1.0.0"` |
| `transferencia_id` | UUID v4 — referência que o documento de aceitação usa para responder |
| `criada_em` | Instante de criação |
| `transmitente`, `destinatario` | `{designacao, identificadores[]}`. Declarar o destinatário **não** estabelece que ele aceitou |
| `fundamento` | Fundamento invocado. Declaração do transmitente; o NDF não aprecia se é bastante |
| `unidades[]` | `{ndf_id, payload_hash, validation_code, ficheiro}` — uma por `.ndfpkg` |
| `referencias_externas[]` | Relações declaradas pelas unidades cujo alvo **não** faz parte do conjunto |
| `inventario[]` | Inventário físico dos ficheiros **próprios do contentor** — declaração, selo e evidência |

Propriedades que o desenho garante:

- **Fecho nos dois sentidos.** Cada unidade declarada tem de estar presente, e
  cada pacote presente tem de estar declarado. Um pacote a mais é tão grave como
  um a menos: foi acrescentado por alguém, e o selo não o cobre.
- **Ligação à versão exata.** As unidades identificam-se por `ndf_id` **e**
  `payload_hash`. O digest do ficheiro `.ndfpkg` **não** é usado — o mesmo
  documento materializado noutro ZIP continua a ser a mesma unidade documental.
- **`referencias_externas` é informação derivada e por isso verificável.** O
  recetor recomputa-a a partir das unidades recebidas e compara: o valor
  declarado deve coincidir, nem a mais nem a menos. Array vazio significa que o
  conjunto fecha sobre si mesmo.
- **O conjunto declara composição, nunca estrutura intelectual.** As relações
  documentais vivem em `relacoes[]` dentro de cada unidade, assinadas pelo
  produtor.

**A aceitação é ela própria um NDF** (`aceitacao-custodia@1.0.0`), produzido
pelo recetor: transferir custódia é ato bilateral, e sem artefacto do recetor
«enviado de forma segura» é propriedade do transporte, não da custódia. Contém
referência à transferência, resultado por unidade (`aceite` | `recusada` +
fundamento) e uma relação por unidade aceite. **Aceitação parcial é o caso
normal, não a exceção**; os critérios de recusa são do recetor.

### 9.4 Portal público de verificação

**Especificação:** [`specs/portal/SPEC.md`](specs/portal/SPEC.md) ·
**Contrato:** [`specs/portal/openapi.yaml`](specs/portal/openapi.yaml)

Serviço de custódia que resolve um `validation_code`. **Não é requisito de
conformidade NDF** — é funcionalidade que qualquer custodiante está livre de
disponibilizar sobre o seu acervo.

Procedimento de verificação, por consulta bem-sucedida:

1. resolver o registo exato sem depender de metadados fornecidos pelo utilizador;
2. recalcular JCS e `payload_hash` a partir do NDF-core preservado;
3. recalcular e comparar `validation_code`;
4. validar a cadeia de custódia e a última âncora externa;
5. validar CAdES, timestamps, revogação e confiança, quando presentes;
6. obter o estado arquivístico corrente;
7. devolver **separadamente** os estados de integridade, autenticidade e
   assinatura.

Regras de apresentação: `trusted_custody` significa que o portal atesta emissão
e preservação pela instituição identificada — **não deve** ser apresentado como
assinatura eletrónica pessoal. `integrity_only` **não deve** ser apresentado
como prova da identidade do emissor.

**Privacidade.** A resposta pública contém apenas entidade produtora, tipo, data
de finalização e estado. Assunto, destinatário, identificadores pessoais,
classificação, conteúdo e detalhes de conservação **não** são expostos. O serviço
limita enumeração, regista abuso e devolve a **mesma resposta** para registos
desconhecidos e não públicos.

**Disponibilidade.** Indisponibilidade produz `unavailable`, **nunca**
`invalid`. Pacotes assinados ou selados permanecem verificáveis offline.

**Documentos classificados.** A inclusão de um documento num serviço de
verificação deve ser decisão explícita do custodiante face ao nível de
classificação declarado — nunca comportamento por omissão herdado da
configuração aplicada a documentos não classificados (SPEC NDF §4.7.2).

---

## 10. Produzir e verificar na prática

### 10.1 Pipeline de finalização

A finalização transforma um NDF-core completo (rascunho) num NDF finalizado
(core + envelope), imutável.

**Pré-condições — a finalização falha se:**

- faltar qualquer campo obrigatório do core;
- `nivel_assinatura` contiver valor fora do enum;
- `nivel_assinatura ∈ {avancada, qualificada}` e não houver certificado
  conforme disponível;
- `nivel_assinatura = "qualificada"` e o certificado não for emitido por PSSC
  inscrito na lista de confiança eIDAS;
- `prazo_conservacao` ou `destino_final` não puderem ser resolvidos a partir de
  `classificacao_ref` e do instrumento — **exceto** quando a decisão de destino
  compete a outra autoridade, caso em que se declara `a_determinar`;
- o conteúdo violar as regras de tipos permitidos (bytes embutidos, `NaN`,
  chaves duplicadas).

**Passos (ordem estrita).** Os passos 1–3 e 8 são **sempre** obrigatórios; 4–7
são condicionais a `nivel_assinatura`.

| # | Passo | Condição |
|---|---|---|
| 1 | Canonicalizar o NDF-core completo via JCS → `payload_bytes` | sempre |
| 2 | `payload_hash = SHA-256(payload_bytes)` | sempre |
| 3 | `validation_code = "NDF-" + BASE32_NOPAD(SHA-256(ndf_id + "\|" + payload_hash))[:20]` | sempre |
| 4 | Assinar `payload_bytes` em modo detached (CAdES-B) | `avancada`/`qualificada`, ou selo institucional |
| 5 | Obter timestamp de assinatura (CAdES-B-T) | `avancada`/`qualificada` |
| 6 | Recolher material de validação — cadeia + revogação (CAdES-B-LT) | `avancada`/`qualificada` |
| 7 | Obter timestamp de arquivo sobre assinatura + material (CAdES-B-LTA) | `avancada`/`qualificada` |
| 8 | Persistir `payload_bytes` e envelope **atomicamente** | sempre |

Nenhuma escrita parcial ou inconsistente entre os dois deve ficar visível a um
leitor.

**Pós-condições:**

- `payload_bytes` é imutável para sempre;
- assinaturas, timestamps e material de validação preservados **byte a byte**;
- entradas existentes do envelope não são alteradas — provas de re-selagem
  acrescentam-se de forma append-only;
- qualquer alteração ao conteúdo lógico origina um **novo NDF**.

### 10.2 Ordem de verificação

Um verificador deve, **por esta ordem**:

1. validar o manifesto e **impedir caminhos absolutos ou com `..`**;
2. verificar os hashes de todos os ficheiros inventariados;
3. validar NDF-core e envelope contra os schemas da versão declarada;
4. recalcular JCS, `payload_hash` e `validation_code`;
5. resolver e validar o schema de `tipo_documento_ref`;
6. validar todos os valores NCRTF;
7. validar assinaturas, selos, timestamps e cadeia de confiança, se presentes;
8. confirmar a correspondência entre `ndt_version_ref` e o NDT incluído.

Quando a assinatura for juridicamente obrigatória, a ausência ou alteração de
**qualquer byte** da assinatura original, timestamp ou material de validação
produz resultado **inválido**, ainda que o NDF-core permaneça íntegro.

Sem assinatura ou selo válido, o resultado deve ser descrito como **«íntegro sob
a custódia avaliada»**.

### 10.3 Regras de integração entre formatos

1. `NDF-core.ndt_version_ref` corresponde a `NDT.schema_id` e `NDT.versao_ndt`.
2. O `.ndfpkg` inclui esse NDT exato e o respetivo hash no manifesto.
3. `metadados.tipo_documento_ref` resolve para o schema usado para validar
   `NDF-core.documento`.
4. Um caminho NDT `a.b.c` resolve para `NDF-core.documento.a.b.c`.
5. Um valor NCRTF valida contra a versão NCRTF declarada e cumpre as regras de
   canonicalização dessa versão.
6. Recursos NDT e NCRTF resolvem dentro do pacote ou do domínio de custódia e
   são **verificados por hash antes de uso**.
7. A ausência de um NDT não impede a leitura dos dados, mas **impede declarar
   uma renderização como reprodutível**.

### 10.4 Erros comuns a evitar

| Erro | Porquê está errado |
|---|---|
| Reserializar o NDF-core ao lê-lo da base de dados | Destrói os bytes assinados |
| Embutir base64 num campo de `documento` | Proibido — usar componentes por digest |
| Resolver um componente pelo `nome_original` | O digest é a identidade; o nome é descritivo |
| Declarar `nivel_assinatura: "qualificada"` porque o PDF preservado tem PAdES | `nivel_assinatura` descreve a assinatura **do NDF** |
| Registar o submissor como `autor` | Submeter não é produzir |
| Registar um sistema em `participantes` | Um sistema produz, não participa |
| Declarar um modelo de linguagem em `proveniencia_sistema` | Contorna o estado de revisão humana obrigatório |
| Modelar delegação como duas entradas de `imputacao` | Destrói a distinção entre ato conjunto e ato por delegação |
| Encadear a cadeia de custódia do recetor na do transmitente | As cadeias são por custodiante; encadear exigiria falsificar |
| Editar um NDF finalizado para corrigir um erro | Corrige-se por **novo NDF** com `relacoes[{tipo:"corrige"}]` |
| Prefixar caminhos NDT com `documento.` | A raiz é implícita |
| Converter `data_hora` para o fuso local | Destrói a reprodutibilidade da projeção |
| Colocar um ficheiro em `anexos/` sem o declarar em `documento` | Quebra o fecho de `NDF-PKG-009` |
| Renumerar uma cadeia de custódia ao transferir parte dela | Torna a omissão indistinguível de uma cadeia completa |

---

## 11. Conformidade e ferramentas

### 11.1 Papéis

Uma implementação pode declarar um ou mais papéis: **produtor**, **leitor**,
**renderizador**, **verificador**. Conformidade num papel não implica
conformidade noutro.

Uma declaração de conformidade deve identificar: especificação e versão exata;
papel; perfil; versão ou hash da suite utilizada; implementação, versão e
ambiente; testes não executados, exceções e limitações conhecidas; data da
avaliação.

**O projeto não fornece certificação, acreditação nem aprovação jurídica.** As
declarações são da responsabilidade de quem as emite.

### 11.2 Blocos de requisitos

| Prefixo | Papel | Onde |
|---|---|---|
| `NDF-PROD-*` | Produtor NDF (23 requisitos) | SPEC NDF §9.1 |
| `NDF-READ-*` | Leitor NDF (24 requisitos) | SPEC NDF §9.2 |
| `NDF-PKG-*` | Pacote `.ndfpkg` (9 requisitos) | SPEC NDF §9.3 |
| `CUST-REQ-*` | Perfil de Ciclo de Vida — **opcional** (4 requisitos) | SPEC NDF §9.5 |
| `NDT-PROD-*` | Produtor NDT (19 requisitos) | SPEC NDT §9.2 |
| `NDT-RENDER-*` | Renderizador NDT (12 requisitos) | SPEC NDT §9.3 |
| `NCRTF-PROD-*` | Produtor NCRTF (7 requisitos) | SPEC NCRTF §12.1 |
| `NCRTF-READ-*` | Leitor NCRTF (5 requisitos) | SPEC NCRTF §12.2 |

Índice consolidado em
[`docs/normalization/REQUIREMENTS.md`](docs/normalization/REQUIREMENTS.md);
matriz de rastreabilidade em
[`docs/normalization/TRACEABILITY.md`](docs/normalization/TRACEABILITY.md).

### 11.3 Suites de conformidade

```text
conformance/
├── ndf/      valid/ + invalid/     casos NDF-core
├── ndt/      valid/ + invalid/ + semantic/
├── ncrtf/    valid/ + invalid/
├── package/                        vetores de pacote
├── custody/                        cadeias válidas, inválidas e recompostas
├── jcs/      vectors.json + numbers.json
└── cades/    valid/ + negative/ + manifests/ + expected/ + trust/
```

**Rejeitar pelo motivo certo.** Rejeitar um caso inválido não basta: um caso
rejeitado por defeito acidental — identificador malformado, campo obrigatório em
falta — é indistinguível, para um runner que compare apenas aceite/rejeitado, de
um caso que exerça a regra que documenta. Por isso cada ficheiro de `invalid/`
declara `_expected_match`: uma expressão regular que deve encontrar
correspondência em pelo menos um dos erros reportados.

Os campos `_comment`, `_expected_error` e `_expected_match` são internos aos
casos de teste e **nunca** constam de um NDF-core produzido por uma
implementação; o runner remove-os antes de validar.

### 11.4 Comandos

```bash
# Pré-requisito
pip install jsonschema

# Suite completa NDF + NDT + NCRTF
python3 tools/validate.py

# Apenas um formato
python3 tools/validate.py --format ndt

# Validar um exemplo portátil end-to-end
python3 tools/validate.py --package specs/ndf/examples/ndfpkg-example

# Validar um ficheiro específico
python3 tools/validate.py path/to/ndf-core.json

# Apenas casos válidos / inválidos
python3 tools/validate.py --valid-only
python3 tools/validate.py --invalid-only

# Verificações específicas
python3 tools/check_custody.py                 # cadeias de custódia
python3 tools/check_transferencia.py specs/ndf/examples/ndfxfer-example
python3 tools/check_ndt_semantic_corpus.py     # cobertura do corpus semântico
python3 tools/check_jcs_vectors.py             # vetores JCS
python3 tools/check_package_vectors.py         # vetores de pacote
python3 tools/check_cades_gate.py              # gate CAdES
python3 tools/canonicalize.py                  # canonicalização JCS
```

### 11.5 Estado de prontidão

Nenhum dos gates externos de
[`docs/normalization/READINESS.md`](docs/normalization/READINESS.md) está
cumprido, e nenhum deles pode ser cumprido por revisão interna. O período de
revisão pública PR-001 **não** tem data: abre quando `normordis-pdf` produzir,
de forma reproduzível por terceiros, um documento a partir de NDF + NDT — ver
[`docs/normalization/REVIEW-LOG.md`](docs/normalization/REVIEW-LOG.md).

**O que pode ser comunicado:** que o conjunto é uma proposta técnica madura para
revisão externa, com objetivos claros, separação de responsabilidades, schemas,
suites de conformidade, matriz de rastreabilidade e gates explícitos.

**O que não deve ser comunicado:** que exista estatuto formal de norma,
equivalência certificada com qualquer entidade normalizadora, ou revisão pública
em curso. Nenhuma conformidade com OAIS, PREMIS, METS ou eIDAS é alegada — ver a
reserva em
[`docs/interoperability/INTEROPERABILITY-LAYERS.md`](docs/interoperability/INTEROPERABILITY-LAYERS.md) §6.

### 11.6 Licenciamento

| Artefacto | Licença |
|---|---|
| Texto das especificações, schemas, exemplos | **CC0 1.0** ([`LICENSE-SPEC`](LICENSE-SPEC)) — domínio público |
| Implementações de referência (`normordis-pdf`, bibliotecas) | **EUPL v1.2**, nos respetivos repositórios |

A separação é deliberada: qualquer produtor de software para a Administração
Pública — aberto ou proprietário — pode implementar leitura e escrita de
NDF/NDT/NCRTF sem qualquer obrigação contratual para com o autor da
especificação. Um formato verdadeiramente aberto é o que permite à Administração
mudar de fornecedor sem perder acesso aos seus próprios dados.

---

## Anexo A — Glossário consolidado

| Termo | Significado |
|---|---|
| **NDF** | NORMORDIS Document Format — o formato e o seu modelo documental, no conjunto |
| **NDF-core** | Fonte de verdade documental: o objeto JSON canonicalizado e assinado |
| **Envelope** | Assinaturas, timestamps e material de validação; associados ao core mas **não** abrangidos pela assinatura |
| **Artefacto NDF assinado** | NDF-core + envelope — unidade mínima verificável |
| **Pacote NDF (`.ndfpkg`)** | NDF-core + envelope + NDT + schemas + recursos — unidade mínima autossuficiente |
| **`.ndfxfer`** | Conjunto de transferência — contentor de várias unidades documentais (desenho, não normativo) |
| **NDT** | NORMORDIS Document Template — formato declarativo de layout |
| **NCRTF** | NORMORDIS Canonical Rich Text Format — texto rico canónico embebido no NDF |
| **JCS** | JSON Canonicalization Scheme (RFC 8785) |
| **`payload_bytes`** | Os bytes canónicos do NDF-core — nunca reserializados |
| **`payload_hash`** | SHA-256 dos `payload_bytes` |
| **`validation_code`** | Código curto derivado de `ndf_id` + `payload_hash`, aposto à representação visual |
| **Perfil de custódia** | Representação otimizada para persistência e deduplicação |
| **Perfil portátil** | `.ndfpkg` autocontido |
| **Perfil de avaliação** | Regime arquivístico declarado em `avaliacao.perfil` — identificador opaco qualificado |
| **PCA** | Prazo de Conservação Administrativa |
| **DF** | Destino Final |
| **MEG** | Macroestrutura / instrumentos de gestão documental da DGLAB |
| **Lista Consolidada** | Referencial suprainstitucional da DGLAB com classificação e avaliação |
| **CAdES** | CMS Advanced Electronic Signatures (ETSI EN 319 122) |
| **CAdES-B-LTA** | Nível com timestamp de arquivo — Basic + Timestamp + Long Term + Archive |
| **PAdES** | PDF Advanced Electronic Signatures (ETSI EN 319 142-1) — opcional e independente do CAdES do NDF |
| **SEA / AES** | Assinatura Eletrónica Avançada — eIDAS Art.º 26.º |
| **SEQ / QES** | Assinatura Eletrónica Qualificada — eIDAS Art.º 25.º |
| **PSSC** | Prestador de Serviços de Confiança Qualificado inscrito na lista eIDAS |
| **TSA** | Autoridade de Timestamp (RFC 3161) |
| **PDF/UA-2** | ISO 14289-2 — perfil de acessibilidade sobre PDF 2.0; formato alvo do renderizador |
| **PDF/A-3** | ISO 19005-3 — perfil de arquivo com suporte a anexos; compatível com PDF/UA-2 |
| **`pagina_def`** | Modelo de página NDT, instanciado por `sequencia[]` |
| **`grelha_digitos`** | Primitiva NDT de caixas por carácter, ligada a um caminho NDF |
| **`fluxo`** | Região de layout vertical sequencial, para corpo de extensão variável |
| **`mobilia`** | Elementos fixos de página: numeração, marca de água, rodapé |
| **Componente** | Ficheiro binário declarado em `documento` por digest, com papel `original`, `representacao_congelada`, `anexo` ou `evidencia` |
| **Extensão qualificada** | `ext.<entidade>.<tipo>[@<versao>]` — vocabulário declarado por uma entidade, sem registo central |
| **Renderizador** | Implementação que combina NDF + NDT e produz uma representação |
| **Verificador** | Implementação que avalia integridade e conformidade |

---

## Anexo B — Mapa de ficheiros do repositório

### Especificações normativas

| Caminho | Conteúdo |
|---|---|
| [`specs/ndf/SPEC.md`](specs/ndf/SPEC.md) | Especificação NDF 1.0.0 |
| [`specs/ndt/SPEC.md`](specs/ndt/SPEC.md) | Especificação NDT 2.0.0 |
| [`specs/ncrtf/SPEC.md`](specs/ncrtf/SPEC.md) | Especificação NCRTF 2.0.0 |
| [`specs/registry/SPEC.md`](specs/registry/SPEC.md) | Registo de tipos e perfis |
| [`specs/portal/SPEC.md`](specs/portal/SPEC.md) | Portal público de verificação |
| [`specs/ndt/RENDERER-CONFORMANCE.md`](specs/ndt/RENDERER-CONFORMANCE.md) | Perfis de verificação de renderizadores |

### Schemas

| Caminho | Valida |
|---|---|
| `specs/ndf/schemas/ndf-core.schema.json` | NDF-core completo |
| `specs/ndf/schemas/envelope.schema.json` | Envelope |
| `specs/ndf/schemas/manifest.schema.json` | `manifest.json` do `.ndfpkg` |
| `specs/ndf/schemas/custody-event.schema.json` | Evento do log de custódia (perfil opcional) |
| `specs/ndf/schemas/evidencia-custodia.schema.json` | Evidência de custódia transferível |
| `specs/ndf/schemas/transferencia.schema.json` | Declaração de conjunto de transferência |
| `specs/ndt/schemas/ndt.schema.json` | Template NDT |
| `specs/ncrtf/schemas/ncrtf.schema.json` | Valor NCRTF |
| `specs/registry/schemas/*.schema.json` | Bloco `documento` por tipo canónico |
| `specs/registry/profiles/*.schema.json` | Bloco `avaliacao` por perfil |

### Governação e normalização

| Caminho | Conteúdo |
|---|---|
| [`README.md`](README.md) | Apresentação, estado, princípios |
| [`GOVERNANCE.md`](GOVERNANCE.md) | Governação do projeto |
| [`VERSIONING.md`](VERSIONING.md) | Política de versões |
| [`CONFORMANCE.md`](CONFORMANCE.md) | Condições gerais de declaração de conformidade |
| [`NORMALIZATION.md`](NORMALIZATION.md) | Percurso de maturidade (níveis 0–5) |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Como contribuir |
| [`LACUNAS.md`](LACUNAS.md) | Lacunas identificadas e em aberto |
| [`ROADMAP.md`](ROADMAP.md) | Roadmap informativo |
| [`docs/normalization/`](docs/normalization/) | Política editorial, terminologia, referências normativas, requisitos, rastreabilidade, prontidão, IPR, revisão pública |
| [`docs/architecture/`](docs/architecture/) | `ARCHITECTURE.md` e os ADR (numeração ADR-001 a ADR-025, 23 publicados) |
| [`docs/interoperability/`](docs/interoperability/) | Camadas de interoperabilidade, mapeamentos OAIS e PREMIS/METS |
| [`docs/profiles/`](docs/profiles/) | Matriz de compatibilidade de regimes arquivísticos (PT, FR, DE, NL, UE) |
| [`docs/design/`](docs/design/) | Documentos de desenho — captura, transferência, estabilização, paginação |

### ADR — decisões de arquitetura

Registo completo em [`docs/architecture/`](docs/architecture/). Os que mais
condicionam a leitura deste manual:

| ADR | Decisão |
|---|---|
| ADR-001 | JSON, não XML |
| ADR-003 | Documentos autónomos ligados por relações |
| ADR-004 | Assinatura autocontida |
| ADR-005 | Proveniência de IA |
| ADR-009 | `ndf_id` opaco, sem namespace |
| ADR-010 | Separação entre conformidade, perfil e ciclo de vida |
| ADR-011 | Sucessão documental por relação |
| ADR-012 | Imputação jurídica |
| ADR-015 | Generalização da avaliação arquivística |
| ADR-016 | Custódia vs. responsável pelo tratamento |
| ADR-017 | Identificadores e classificação por perfil |
| ADR-020 | Um formato, duas realidades — nativo e capturado |
| ADR-021 | Componentes nos bytes assinados |
| ADR-022 | Dever do formato |
| ADR-023 | Origem não apurável |
| ADR-024 | Fronteira OAIS — modelo de informação, não modelo funcional |
| ADR-025 | Componentes como mecanismo único |
