# NCRTF — NORMORDIS Canonical Rich Text Format

**Versão**: 2.0.0
**Estado**: Draft — revisão pública por abrir
**Licença**: CC0 1.0 Universal
**Repositório**: normordis-spec

**Convenções editoriais**: aplica-se
[`docs/normalization/EDITORIAL-POLICY.md`](../../docs/normalization/EDITORIAL-POLICY.md).
A língua normativa é o português europeu.

---

## Sumário

| Secção | Conteúdo |
|---|---|
| §1 | Introdução e objetivos |
| §2 | Terminologia normativa |
| §3 | Modelo de documento |
| §4 | Nós bloco |
| §5 | Nós inline |
| §6 | Marcas de texto |
| §7 | Famílias de tipo |
| §8 | Regras de canonicalização |
| §9 | Integração com NDT |
| §10 | Integração com `.ndfpkg` |
| §11 | Extensibilidade |
| §12 | Conformidade |
| Anexo A | Glossário informativo |

---

## 1. Introdução

### 1.1 Objetivo

O NCRTF (NORMORDIS Canonical Rich Text Format) é uma especificação de formato de texto estruturado com os seguintes objetivos, por ordem de prioridade:

1. **Canónico**: a mesma estrutura lógica produz sempre os mesmos bytes JSON, tornando-se compatível com JCS/RFC 8785 e assinável como parte de um NDF-core.
2. **Independente de implementação**: não pressupõe nem depende de nenhum editor ou biblioteca de rich text (Lexical, ProseMirror, Tiptap, Quill, etc.). Editores adaptam-se ao NCRTF através de conversores; a especificação não refere nenhum.
3. **Eficiente como conteúdo NDF**: um valor NCRTF é um objeto JSON armazenado
   diretamente num campo do bloco `documento` de um NDF-core, sem codificação
   adicional. Está sujeito a canonicalização JCS como qualquer outro campo.
4. **Legível por máquina sem renderizador**: a estrutura de nós é interpretável
   diretamente, sem dependência de CSS, fontes ou motores de layout.
5. **Interoperável**: produtores, editores, validadores e renderizadores
   independentes trocam o mesmo conteúdo sem preservar o estado proprietário
   do editor de origem.

### 1.2 O que o NCRTF representa

- Texto com formatação inline (negrito, itálico, sublinhado, riscado, código, subscrito, sobrescrito)
- Parágrafos, títulos estruturados e citações em bloco
- Listas ordenadas, não-ordenadas e de verificação (com suporte a aninhamento real)
- Tabelas com cabeçalho opcional e células de texto simples
- Imagens referenciadas por caminho dentro do `.ndfpkg`
- Ligações hipertexto inline
- Quebras de linha forçadas
- Controlo de alinhamento, indentação e família tipográfica por bloco ou por nó inline

### 1.3 O que o NCRTF não representa

| O quê | Onde fica |
|---|---|
| O ato jurídico completo | NDF-core (`documento`) |
| Regras de validação e cálculo | App de domínio (fora do âmbito NORMORDIS-especificação) |
| Layout de página (margens, tipografia, logótipos) | Bloco `layout` do NDT |
| Metadados do documento | NDF-core (`metadados`) |
| Assinatura e envelope de custódia | Envelope NDF |
| PDF/UA-2, ODF, HTML | Artefactos derivados — fora do âmbito |
| Estado interno de editor | Formato proprietário do editor (ex: Lexical JSON) |

### 1.4 Relação com outros componentes NORMORDIS

```
NDF-core.documento.campo_corpo  ←  valor NCRTF (este formato)
  │  canonicalizado via JCS + assinado via CAdES
  │
  ↓
Envelope NDF

NDT: bloco tipo "corpo", referencia: "caminho.ndf"
  │  o renderizador lê o caminho NDF, obtém o valor NCRTF, renderiza
  ↓
PDF/UA-2 + PDF/A-3  |  ODF  |  HTML  |  outros artefactos derivados
```

**Leitura**: o NCRTF é um valor armazenado no **NDF** (como parte de `documento`). O **NDT** não contém NCRTF — declara apenas a posição e o caminho NDF onde o valor NCRTF reside. O renderizador combina os dois para produzir o saída.

### 1.5 Referências normativas

| Documento | Relevância |
|---|---|
| BCP 14 (RFC 2119 e RFC 8174) | Linguagem normativa |
| RFC 8259 | Sintaxe e modelo JSON |
| RFC 8785 (JCS) | Canonicalização JSON — base da assinabilidade NCRTF |
| JSON Schema Draft 2020-12 | Schema de validação (§12) |
| NORMORDIS NDF v1.x | Formato contentor que embebe valores NCRTF |
| NORMORDIS NDT v2.x | Declaração de campos de tipo `ncrtf` |

### 1.6 Alterações de v1.0.0 para v2.0.0

Esta é uma versão **MAJOR** — documentos v1.0.0 NÃO são válidos contra este schema.

| Área | Alteração |
|---|---|
| Listas | `ordered_list`/`unordered_list` unificados em `list` com campo `list_type`; `items` renomeado para `content`; `list_item` passa a ser um nó explícito com `type: "list_item"` e conteúdo inline (não blocos) |
| Tabelas | `rows`/`cells` com `header: true` substituído por `head`/`body`; células passam a ser strings simples (não objetos com `content`) |
| Inline | Adicionados `link` e `hard_break`; `font_family` deixa de ser marca-objeto e passa a campo explícito nos nós `text` |
| Marcas | Adicionadas `"code"` e `"strikethrough"`; ordem canónica actualizada |
| Bloco | Adicionado `blockquote`; campos `alignment`, `indent`, `font_family` em `paragraph` e `heading` |
| Imagem | Adicionados `caption` e `width_percent`; removidos `width`/`height` em pixéis |
| Raiz | Mantém `ncrtf_version`/`content`; removido `meta`/`updated_at` (não determinístico) |

---

## 2. Terminologia normativa

Os termos seguintes, quando em maiúsculas, têm o significado definido no BCP
14 (RFC 2119 e RFC 8174). Formas em minúsculas são narrativas e não criam
requisitos:

| Termo | Significado |
|---|---|
| **DEVE** / **DEVEM** | Requisito obrigatório |
| **NÃO DEVE** / **NÃO DEVEM** | Proibição |
| **RECOMENDA-SE** | Prática aconselhada; desvios aceitáveis com justificação |
| **PODE** / **PODEM** | Comportamento opcional |
| **OPCIONAL** | O campo ou comportamento pode estar ausente |

Aplicam-se igualmente os termos da
[base terminológica comum](../../docs/normalization/TERMINOLOGY.md). Termos
NCRTF específicos são definidos na cláusula em que são introduzidos. O Anexo A
reúne um glossário informativo.

---

## 3. Modelo de documento

### 3.1 Estrutura raiz

Um valor NCRTF é um objeto JSON com a seguinte estrutura:

```json
{
  "ncrtf_version": "2.0.0",
  "content": [ <bloco>, <bloco>, ... ]
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `ncrtf_version` | string | Sim | Versão da especificação NCRTF. DEVE ser `"2.0.0"` para documentos conformes a esta versão. |
| `content` | array de Bloco | Sim | Sequência de nós bloco. DEVE ter pelo menos 1 elemento. |

Campos adicionais NÃO DEVEM estar presentes na raiz (`additionalProperties: false`).

### 3.2 Hierarquia de nós

```
Documento
└── content: Bloco[]
    ├── paragraph     → content: Inline[]
    │     alignment?, indent?, font_family?
    ├── heading       → content: Inline[]
    │     level, alignment?, font_family?
    ├── list          → content: ListItem[]
    │     list_type
    │     ListItem  → content: (Inline | list)[]
    │                  checked? (checklist apenas)
    ├── blockquote    → content: Inline[]
    ├── table         → head?: TableRow[], body: TableRow[]
    │     TableRow  → cells: string[]
    └── image         (nó folha)
          ref, alt, caption?, width_percent?

Inline = text | link | hard_break
text   = { type, text, marks?, font_family? }
link   = { type, href, content: text[], title?, target? }
```

---

## 4. Nós bloco

### 4.1 `paragraph`

```json
{
  "type": "paragraph",
  "content": [
    { "type": "text", "text": "Texto simples." }
  ]
}
```

```json
{
  "type": "paragraph",
  "alignment": "justify",
  "indent": 1,
  "font_family": "LiberationSerif",
  "content": [
    { "type": "text", "text": "Texto com formatação de bloco." }
  ]
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"paragraph"` | Sim | |
| `content` | array de Inline | Sim — mínimo 1 elemento | |
| `alignment` | `"center"` \| `"justify"` \| `"right"` | OPCIONAL | Omitir quando `"left"` (default). |
| `indent` | inteiro ≥ 1 | OPCIONAL | Nível de indentação. Omitir quando 0 (default). |
| `font_family` | ver §7 | OPCIONAL | Família tipográfica do bloco. |

### 4.2 `heading`

```json
{ "type": "heading", "level": 2, "content": [ { "type": "text", "text": "Título de nível 2" } ] }
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"heading"` | Sim | |
| `level` | inteiro 1–3 | Sim | 1 = título principal, 2 = subtítulo, 3 = subtítulo de nível 3. |
| `content` | array de Inline | Sim — mínimo 1 elemento | |
| `alignment` | `"center"` \| `"justify"` \| `"right"` | OPCIONAL | Omitir quando `"left"` (default). |
| `font_family` | ver §7 | OPCIONAL | Família tipográfica do título. |

Em documentos administrativos, nível 1 RECOMENDA-SE reservado ao NDT (layout); conteúdo editorial DEVE começar em `level: 2`.

### 4.3 `list` e `list_item`

#### `list`

```json
{
  "type": "list",
  "list_type": "ordered",
  "content": [
    {
      "type": "list_item",
      "content": [ { "type": "text", "text": "Primeiro item." } ]
    },
    {
      "type": "list_item",
      "content": [
        { "type": "text", "text": "Segundo item com sub-lista:" },
        {
          "type": "list",
          "list_type": "bullet",
          "content": [
            { "type": "list_item", "content": [ { "type": "text", "text": "Sub-item A." } ] },
            { "type": "list_item", "content": [ { "type": "text", "text": "Sub-item B." } ] }
          ]
        }
      ]
    }
  ]
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"list"` | Sim | |
| `list_type` | `"bullet"` \| `"checklist"` \| `"ordered"` | Sim | Tipo de lista. |
| `content` | array de `list_item` | Sim — mínimo 1 elemento | |
| `alignment` | `"center"` \| `"justify"` \| `"right"` | OPCIONAL | Alinhamento da lista. Omitir quando `"left"` (default). |

#### `list_item`

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"list_item"` | Sim | |
| `content` | array de (Inline \| `list`) | Sim — mínimo 1 elemento | Inlines e/ou listas aninhadas. |
| `checked` | boolean | OPCIONAL | Apenas para `list_type: "checklist"`. `false` = não assinalado; `true` = assinalado. NÃO omitir `false` — o valor é semanticamente relevante. |

**Listas de verificação** (`list_type: "checklist"`): cada `list_item` DEVE ter o campo `checked` (explicitamente `true` ou `false`).

**Listas aninhadas**: um `list_item.content` PODE conter um ou mais nós `list` adicionais para criar hierarquia. A lista aninhada aparece após os inlines do item pai.

### 4.4 `blockquote`

```json
{
  "type": "blockquote",
  "content": [ { "type": "text", "text": "Citação de documento referenciado." } ]
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"blockquote"` | Sim | |
| `content` | array de Inline | Sim — mínimo 1 elemento | |
| `alignment` | `"center"` \| `"justify"` \| `"right"` | OPCIONAL | Omitir quando `"left"` (default). |
| `font_family` | ver §7 | OPCIONAL | Família tipográfica da citação. |

### 4.5 `table`

Tabelas representam dados tabulares com células de texto simples. O conteúdo das células NÃO suporta formatação rich text — é texto plano.

```json
{
  "type": "table",
  "head": [
    { "cells": ["Referência", "Data", "Estado"] }
  ],
  "body": [
    { "cells": ["REF/2026/001", "2026-06-01", "Concluído"] },
    { "cells": ["REF/2026/002", "2026-06-15", "Em curso"] }
  ]
}
```

#### `table`

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"table"` | Sim | |
| `body` | array de TableRow | Sim — mínimo 1 linha | Linhas de dados. |
| `head` | array de TableRow | OPCIONAL | Linha(s) de cabeçalho. Omitir quando ausente (não usar `[]`). |

#### `TableRow`

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `cells` | array de string | Sim — mínimo 1 célula | Cada elemento é o texto de uma célula. |

Todas as linhas de uma tabela DEVEM ter o mesmo número de células.

### 4.6 `image`

```json
{
  "type": "image",
  "ref": "recursos/grafico-1.png",
  "alt": "Gráfico de evolução trimestral de processos",
  "caption": "Figura 1 — Evolução 2024–2026",
  "width_percent": 75
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"image"` | Sim | |
| `ref` | string | Sim | Caminho relativo dentro do `.ndfpkg`. Ver §10. |
| `alt` | string | Sim | Texto alternativo — obrigatório para acessibilidade e preservação. Pode ser string vazia se a imagem for puramente decorativa. |
| `caption` | string | OPCIONAL | Legenda da figura. |
| `width_percent` | inteiro 25–100 | OPCIONAL | Largura como percentagem da largura disponível (sugestão editorial). |

`image` é um nó folha — NÃO TEM `content`. Imagens NÃO DEVEM ser codificadas em base64 dentro do valor NCRTF (ver §10.1).

---

## 5. Nós inline

### 5.1 `text`

O nó inline de texto com formatação opcional.

```json
{ "type": "text", "text": "conteúdo simples" }
{ "type": "text", "text": "negrito e itálico", "marks": ["bold", "italic"] }
{ "type": "text", "text": "H", "marks": ["subscript"], "font_family": "LiberationSerif" }
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"text"` | Sim | |
| `text` | string | Sim — mínimo 1 caracter | Conteúdo textual. NÃO DEVE ser string vazia. |
| `marks` | array de Mark | OPCIONAL | Formatação aplicada. Se presente, DEVE ter pelo menos 1 elemento e DEVE estar em ordem canónica (§6). |
| `font_family` | ver §7 | OPCIONAL | Família tipográfica do nó de texto, quando diferente do bloco pai. |

### 5.2 `link`

```json
{
  "type": "link",
  "href": "https://dre.pt",
  "content": [ { "type": "text", "text": "Diário da República Electrónico" } ],
  "title": "Acesso ao DRE",
  "target": "_blank"
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"link"` | Sim | |
| `href` | string | Sim | URI da ligação. |
| `content` | array de `text` | Sim — mínimo 1 elemento | Texto âncora (apenas nós `text`; não permite `link` aninhados). |
| `title` | string | OPCIONAL | Texto do atributo `title`. |
| `target` | `"_blank"` \| `"_self"` | OPCIONAL | Comportamento de abertura. |

### 5.3 `hard_break`

Quebra de linha forçada dentro de um bloco. Diferente de um novo parágrafo.

```json
{ "type": "hard_break" }
```

| Campo | Tipo | Obrigatório |
|---|---|---|
| `type` | `"hard_break"` | Sim |

---

## 6. Marcas de texto

### 6.1 Marcas disponíveis

| Mark | Renderização típica | Notas |
|---|---|---|
| `"bold"` | Negrito | |
| `"code"` | Monospace inline | Para fragmentos de código ou identificadores técnicos. |
| `"italic"` | Itálico | |
| `"strikethrough"` | Riscado | Para correções, actas, rectificações. |
| `"subscript"` | Subscrito (ex: H₂O) | NÃO DEVE coexistir com `"superscript"` no mesmo nó. |
| `"superscript"` | Sobrescrito (ex: m²) | NÃO DEVE coexistir com `"subscript"` no mesmo nó. |
| `"underline"` | Sublinhado | |

### 6.2 Ordem canónica das marcas

Para garantir canonicalização determinística (§8), o array `marks` **DEVE** estar ordenado alfabeticamente:

```
bold → code → italic → strikethrough → subscript → superscript → underline
```

Implementações produtoras DEVEM ordenar as marcas antes de serializar. Leitores DEVEM rejeitar documentos com `marks` fora desta ordem.

---

## 7. Famílias de tipo

O campo `font_family` (em nós `text`, `paragraph` e `heading`) aceita os seguintes valores canónicos:

| Valor | Classe | Intenção |
|---|---|---|
| `"LiberationMono"` | Monospace | Código, identificadores, dados tabulares em campos de texto |
| `"LiberationSans"` | Sem serifas | Texto de corpo padrão |
| `"LiberationSerif"` | Com serifas | Citações, referências, texto formal |

Estes valores são nomes canónicos independentes de qualquer implementação. O renderizador é responsável por resolver o mapeamento para as fontes disponíveis no ambiente de saída.

Quando `font_family` é especificado num bloco (`paragraph`, `heading`), aplica-se a todos os nós `text` filhos que não especifiquem `font_family` próprio. O `font_family` de um nó `text` tem precedência sobre o do bloco pai.

---

## 8. Regras de canonicalização

A canonicalização NCRTF é pré-condição para a assinabilidade do campo quando embebido num NDF-core.

### 8.1 Canonicalização JCS (RFC 8785)

Todo o valor NCRTF **DEVE** ser canonicalizado via JCS antes de ser incorporado no `payload_bytes` do NDF-core. JCS garante:

- Chaves de objetos ordenadas lexicograficamente (Unicode code point)
- Sem whitespace extra
- Números em formato canónico
- Strings em UTF-8 com escapes mínimos

### 8.2 Restrições adicionais à estrutura

| Regra | Descrição |
|---|---|
| **R1** | `marks` DEVE estar em ordem canónica (§6.2). |
| **R2** | Nós `text` contíguos com marcas idênticas E `font_family` idêntico DEVEM ser fundidos num único nó. |
| **R3** | Campos com valor igual ao default NÃO DEVEM estar presentes: `alignment` quando `"left"`, `indent` quando `0`. |
| **R4** | Arrays vazios NÃO DEVEM estar presentes — omitir o campo em vez de `[]`. Nota: `checked: false` em checklist é semanticamente relevante e NÃO DEVE ser omitido. |
| **R5** | `text` NÃO DEVE ser string vazia. |
| **R6** | `"subscript"` e `"superscript"` NÃO DEVEM coexistir no mesmo nó `text`. |

### 8.3 Verificação de canonicalização

Um produtor conforme **DEVE** verificar, após serializar para JSON, que:

```
JCS(parse(serialize(ncrtf))) == serialize(ncrtf)
```

---

## 9. Integração com NDT

### 9.1 Como o NDT referencia um campo NCRTF

O NDT v2.0.0 é um formato de **layout puro** — não contém dados nem declara tipos de campo. Um campo NCRTF num documento é referenciado no NDT através de um bloco `tipo: "corpo"` com um caminho NDF:

```json
{
  "blocos": [
    {
      "tipo": "corpo",
      "referencia": "corpo",
      "posicao": { "x": 15, "y": 60 },
      "largura": 180
    }
  ]
}
```

Ou, em layout de fluxo:

```json
{
  "fluxo": {
    "y_inicio": 60,
    "elementos": [
      { "tipo": "corpo", "referencia": "corpo" }
    ]
  }
}
```

O campo `referencia` é um caminho relativo a `NDF-core.documento` (ex.:
`"corpo"`, `"parecer.texto"`). O renderizador lê o valor NCRTF nesse caminho e
renderiza-o segundo as regras de layout do NDT.

**Princípio**: o NCRTF vive no NDF. O NDT descreve onde e como renderizá-lo. O renderizador é o único componente que conhece ambos.

### 9.2 Exemplo completo — NDF-core com campo NCRTF

```json
{
  "ndf_version": "1.0.0",
  "ndf_id": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
  "estado": "ativo",
  "payload_hash_alg": "sha256",
  "nivel_assinatura": "avancada",
  "ndt_version_ref": "oficio-generico@1.0.0",
  "metadados": {
    "tipo_documento_ref": "oficio@1.0.0",
    "entidade_produtora": { "designacao": "Direção-Geral de Exemplo", "nif": "123456789" },
    "assunto": "Resposta ao ofício n.º 45/2026",
    "numero_referencia": "OF/2026/00123",
    "contem_dados_pessoais": false,
    "responsavel_tratamento": "Direção-Geral de Exemplo"
  },
  "documento": {
    "numero": "OF/2026/00123",
    "data": "2026-06-18",
    "destinatario": { "nome": "Entidade Destinatária", "identificacao": "NIF 987654321" },
    "corpo": {
      "ncrtf_version": "2.0.0",
      "content": [
        {
          "type": "paragraph",
          "content": [
            { "type": "text", "text": "Em resposta ao ofício n.º 45/2026, informamos que o prazo termina em " },
            { "type": "text", "text": "30 de julho de 2026", "marks": ["bold"] },
            { "type": "text", "text": "." }
          ]
        },
        {
          "type": "table",
          "head": [ { "cells": ["Data", "Diligência", "Estado"] } ],
          "body": [
            { "cells": ["2026-06-01", "Notificação ao interessado", "Concluída"] }
          ]
        },
        {
          "type": "paragraph",
          "content": [
            { "type": "text", "text": "Aguardamos o vosso contacto." }
          ]
        }
      ]
    }
  },
  "avaliacao": {
    "tipo_classificacao_ref": "lc/450.10.001",
    "prazo_conservacao_administrativa": { "valor": 5, "unidade": "anos", "forma_contagem": "data_documento" },
    "destino_final": "eliminacao",
    "instrumento_avaliacao_versao_ref": "lc/lista-consolidada-dglab-2023-v3"
  }
}
```

O campo NCRTF é canonicalizado como parte do NDF-core. Se existir CAdES, fica
coberto pela assinatura ou selo do NDF. O caminho NDT é relativo a
`NDF-core.documento`.

### 9.3 Famílias tipográficas: NCRTF e NDT

O NCRTF usa nomes canónicos de famílias tipográficas independentes de implementação (§7). O NDT usa nomes de fontes PDF para elementos de layout. A tabela de equivalência canónica está definida no NDT v2.0.0 §5.8. O renderizador é responsável por aplicar o mapeamento ao combinar conteúdo NCRTF com estilos NDT.

---

## 10. Integração com `.ndfpkg`

### 10.1 Referências de imagem

O campo `ref` de um nó `image` é um caminho relativo dentro do arquivo `.ndfpkg`:

```
recursos/grafico-evolucao.png
recursos/organograma-2026.svg
recursos/foto-assinatura.jpg
```

O caminho DEVE:
- Ser relativo à raiz do `.ndfpkg`
- Usar `/` como separador (independentemente do SO)
- Referenciar um ficheiro presente no arquivo
- Ter uma entrada correspondente no `manifest.inventario` do `.ndfpkg`

Imagens NÃO DEVEM ser embutidas como base64 no valor NCRTF. O valor `src` com data URL é um artefacto interno de editores; NÃO DEVE aparecer num NDF-core finalizado.

Fluxo recomendado para editores:
1. Durante a edição: imagens mantidas internamente como data URL no estado do editor.
2. Na finalização do NDF: imagens extraídas para `recursos/` do `.ndfpkg`; `src` substituído por `ref` no valor NCRTF que vai para `ndf-core.json`.

### 10.2 Formatos de imagem suportados

| Formato | Extensão | Notas |
|---|---|---|
| PNG | `.png` | RECOMENDADO para gráficos e diagramas |
| SVG | `.svg` | RECOMENDADO para conteúdo vetorial; renderizadores DEVEM sanitizar SVG |
| JPEG | `.jpg` / `.jpeg` | RECOMENDADO para fotografias |
| PDF/A | `.pdf` | OPCIONAL — para sub-documentos em imagem |

### 10.3 Exemplo de estrutura `.ndfpkg` com imagens

```
oficio-OF-2026-00123.ndfpkg
├── manifest.json
├── ndf-core.json          (campo corpo em NCRTF — imagens com ref)
├── envelope.json
├── ndt/
│   └── oficio-generico@2.0.0.ndt.json
└── recursos/
    └── grafico-evolucao.png
```

---

## 11. Extensibilidade

### 11.1 Política de extensão

| Mudança | Versão SemVer |
|---|---|
| Novo tipo de nó bloco OPCIONAL | MINOR |
| Nova marca OPCIONAL | MINOR |
| Novo campo OPCIONAL num nó existente | MINOR |
| Alteração de campo obrigatório / remoção de nó | MAJOR |
| Alteração das regras de canonicalização | MAJOR |

### 11.2 Nós desconhecidos

O schema NCRTF é fechado. Um leitor conforme DEVE rejeitar tipos de nó
desconhecidos. Uma versão MINOR **PODE** acrescentar um nó opcional, mas o documento
que o utilize declara essa versão e requer um leitor/schema que a suporte. Um
leitor nunca ignora silenciosamente conteúdo assinado que não compreende.

### 11.3 Candidatos a versões futuras

| Elemento | Tipo | Motivação |
|---|---|---|
| `code_block` | Bloco | Documentos técnicos com excertos de código |
| `horizontal_rule` | Bloco | Separador de secções |
| `caption` em `image` | Campo de bloco | Já definido; aguarda suporte no editor |
| `start` em `list` | Campo | Numeração inicial diferente de 1 |
| Rich text em células de tabela | Estrutura | Células como array de Inline em vez de string |

---

## 12. Conformidade

### 12.1 Produtor conforme

Uma implementação é um **produtor NCRTF conforme** se:

1. **NCRTF-PROD-001 — DEVE** gerar valores NCRTF que validam contra `specs/ncrtf/schemas/ncrtf.schema.json`.
2. **NCRTF-PROD-002 — DEVE** aplicar todas as regras de canonicalização R1–R6 (§8.2).
3. **NCRTF-PROD-003 — DEVE** verificar que `JCS(parse(serialize(ncrtf))) == serialize(ncrtf)` antes de incorporar o valor num NDF-core.
4. **NCRTF-PROD-004 — NÃO DEVE** incluir nós `image` com `ref` que não existam no `manifest.inventario` do `.ndfpkg`.
5. **NCRTF-PROD-005 — NÃO DEVE** incluir `src` com data URL num NDF-core finalizado — apenas `ref`.
6. **NCRTF-PROD-006 — DEVE** ordenar `marks` conforme §6.2.
7. **NCRTF-PROD-007 — DEVE** fundir nós `text` contíguos com marcas e `font_family` idênticos (R2).

### 12.2 Leitor conforme

Uma implementação é um **leitor NCRTF conforme** se:

1. **NCRTF-READ-001 — DEVE** rejeitar qualquer valor NCRTF que não valide contra o schema desta versão.
2. **NCRTF-READ-002 — DEVE** rejeitar documentos com `marks` fora da ordem canónica (R1).
3. **NCRTF-READ-003 — DEVE** rejeitar nós de tipo desconhecido.
4. **NCRTF-READ-004 — DEVE** rejeitar versões NCRTF que não suporte explicitamente.
5. **NCRTF-READ-005 — DEVE** resolver referências `image.ref` dentro do `.ndfpkg` corrente.

### 12.3 Suite de conformidade

A suite de testes encontra-se em `conformance/ncrtf/`. Implementações conformes DEVEM passar todos os casos válidos sem erros e rejeitar todos os casos inválidos com erro.

```
conformance/ncrtf/
├── valid/      — documentos NCRTF que DEVEM ser aceites
└── invalid/    — documentos NCRTF que DEVEM ser rejeitados
```

---

## Anexo A (informativo) — Glossário

| Termo | Definição |
|---|---|
| **Bloco** | Nó de nível superior na hierarquia NCRTF: `paragraph`, `heading`, `list`, `blockquote`, `table`, `image`. |
| **Canonicalização** | Processo de serialização determinística que produz sempre os mesmos bytes para a mesma estrutura lógica. |
| **Font family** | Família tipográfica canónica (`LiberationSans`, `LiberationSerif`, `LiberationMono`). |
| **Inline** | Nó filho de um bloco que contém texto ou ligação: `text`, `link`, `hard_break`. |
| **JCS** | JSON Canonicalization Scheme, RFC 8785. Algoritmo de canonicalização JSON. |
| **Marca** | Atributo de formatação aplicado a um nó `text`: `bold`, `code`, `italic`, `strikethrough`, `subscript`, `superscript`, `underline`. |
| **NDT** | NORMORDIS Document Template — referencia por caminho valores NCRTF armazenados no NDF-core. |
| **NDF-core** | NORMORDIS Document Format core — JSON assinável que contém valores NCRTF como campos. |
| **`.ndfpkg`** | Arquivo ZIP que agrupa NDF-core, envelope, NDT e recursos (incluindo imagens referenciadas por NCRTF). |
| **Produtor** | Sistema que gera valores NCRTF conformes e os incorpora em NDF-core. |
| **Leitor** | Sistema que consome, valida e renderiza valores NCRTF. |
