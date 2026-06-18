# NCRTF — NORMORDIS Canonical Rich Text Format

**Versão**: 1.0.0
**Estado**: Estável
**Licença**: CC0 1.0 Universal
**Repositório**: normordis-spec

---

## Sumário

| Secção | Conteúdo |
|---|---|
| §1 | Introdução e objectivos |
| §2 | Terminologia normativa |
| §3 | Modelo de documento |
| §4 | Nós bloco |
| §5 | Nós inline e marcas |
| §6 | Regras de canonicalização |
| §7 | Integração com NDT |
| §8 | Integração com `.ndfpkg` |
| §9 | Extensibilidade |
| §10 | Conformidade |
| §11 | Glossário |

---

## 1. Introdução

### 1.1 Objectivo

O NCRTF (NORMORDIS Canonical Rich Text Format) é uma especificação de formato de texto estruturado com os seguintes objectivos, por ordem de prioridade:

1. **Canónico**: a mesma estrutura lógica produz sempre os mesmos bytes JSON, tornando-se compatível com JCS/RFC 8785 e assinável como parte de um NDF-core.
2. **Independente de implementação**: não pressupõe nem depende de nenhum editor ou biblioteca de rich text (Lexical, ProseMirror, Tiptap, Quill, etc.). Editores podem adaptar-se ao NCRTF através de conversores; a spec não refere nenhum.
3. **Eficiente como campo NDT**: um valor NCRTF é um objecto JSON armazenado directamente num campo do bloco `documento` de um NDF-core, sem codificação adicional (sem base64, sem JSON dentro de string). Está sujeito a canonicalização JCS como qualquer outro campo.
4. **Legível por máquina sem renderizador**: a estrutura de nós é interpretável directamente — sem dependência de CSS, fonts ou motores de layout.

### 1.2 O que o NCRTF representa

- Texto com formatação inline (negrito, itálico, sublinhado, subscrito, sobrescrito)
- Parágrafos e títulos estruturados
- Listas ordenadas e não-ordenadas (com suporte a aninhamento)
- Tabelas com cabeçalhos e span
- Imagens referenciadas por caminho dentro do `.ndfpkg`

### 1.3 O que o NCRTF não representa

| O quê | Onde fica |
|---|---|
| O acto jurídico completo | NDF-core (`documento`) |
| Regras de validação e cálculo | NDT |
| Layout de página (margens, tipografia, logótipos) | Bloco `layout` do NDT |
| Metadados do documento | NDF-core (`metadados`) |
| Assinatura e envelope de custódia | Envelope NDF |
| HTML, DOCX, PDF | Artefactos derivados — fora do scope |

### 1.4 Relação com outros componentes NORMORDIS

```
NCRTF (este formato)
  ↓  valor de campo num NDT
NDT [bloco layout define renderização]
  ↓
PDF/A-3 | HTML | outros artefactos derivados

NDF-core (contém o campo NCRTF como parte de `documento`)
  ↓  canonicalizado via JCS + assinado via CAdES
Envelope NDF
```

### 1.5 Referências normativas

| Documento | Relevância |
|---|---|
| RFC 8785 (JCS) | Canonicalização JSON — base da assinabilidade NCRTF |
| JSON Schema Draft 2020-12 | Schema de validação (§10) |
| NORMORDIS NDF v1.x | Formato contentor que embebe valores NCRTF |
| NORMORDIS NDT v2.x | Declaração de campos de tipo `ncrtf` |
| RFC 4122 | UUIDs — não directamente usado, mas referenciado pelo NDF contentor |

---

## 2. Terminologia normativa

Os termos seguintes, quando em maiúsculas, têm o significado definido em RFC 2119 / BCP 14:

| Termo | Significado |
|---|---|
| **DEVE** / **DEVEM** | Requisito obrigatório |
| **NÃO DEVE** / **NÃO DEVEM** | Proibição |
| **RECOMENDA-SE** | Prática aconselhada; desvios aceitáveis com justificação |
| **PODE** / **PODEM** | Comportamento opcional |
| **OPCIONAL** | O campo ou comportamento pode estar ausente |

---

## 3. Modelo de documento

### 3.1 Estrutura raiz

Um valor NCRTF é um objecto JSON com a seguinte estrutura:

```json
{
  "ncrtf_version": "1.0.0",
  "content": [ <bloco>, <bloco>, ... ]
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `ncrtf_version` | string | Sim | Versão da spec NCRTF. DEVE ser `"1.0.0"` para documentos conformes a esta versão. |
| `content` | array de Bloco | Sim | Sequência de nós bloco. DEVE ter pelo menos 1 elemento. |

Campos adicionais NÃO DEVEM estar presentes na raiz (valida `additionalProperties: false`).

### 3.2 Hierarquia de nós

```
Documento
└── content: Bloco[]
    ├── Paragraph      → content: Inline[]
    ├── Heading        → content: Inline[]
    ├── OrderedList    → items: ListItem[]
    │                      └── content: Bloco[]
    ├── UnorderedList  → items: ListItem[]
    │                      └── content: Bloco[]
    ├── Table          → rows: TableRow[]
    │                      └── cells: TableCell[]
    │                              └── content: Bloco[]
    └── Image          (nó folha — sem filhos)

Inline = Text { text: string, marks?: Mark[] }
Mark   = "bold" | "italic" | "subscript" | "superscript" | "underline"
```

**Nós bloco** PODEM conter outros nós bloco (em `ListItem` e `TableCell`), permitindo listas aninhadas e conteúdo misto em células.

**Nós inline** apenas PODEM conter `Text`. Nós inline NÃO DEVEM ser aninhados.

---

## 4. Nós bloco

### 4.1 `paragraph`

```json
{ "type": "paragraph", "content": [ <inline>, ... ] }
```

| Campo | Tipo | Obrigatório |
|---|---|---|
| `type` | `"paragraph"` | Sim |
| `content` | array de Inline | Sim — mínimo 1 elemento |

### 4.2 `heading`

```json
{ "type": "heading", "level": 2, "content": [ <inline>, ... ] }
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"heading"` | Sim | |
| `level` | inteiro 1–3 | Sim | 1 = título principal, 2 = subtítulo, 3 = subtítulo de nível 3 |
| `content` | array de Inline | Sim — mínimo 1 elemento | |

Em documentos administrativos, nível 1 RECOMENDA-SE reservado ao NDT (layout); conteúdo editorial DEVE começar em `level: 2`.

### 4.3 `ordered_list`

```json
{
  "type": "ordered_list",
  "items": [
    { "content": [ <bloco>, ... ] },
    { "content": [ <bloco>, ... ] }
  ]
}
```

| Campo | Tipo | Obrigatório |
|---|---|---|
| `type` | `"ordered_list"` | Sim |
| `items` | array de ListItem | Sim — mínimo 1 elemento |

**ListItem**: `{ "content": [ <bloco>, ... ] }` com `content` obrigatório (mínimo 1 bloco). Um `ListItem` PODE conter outro `ordered_list` ou `unordered_list` no seu `content` para criar listas aninhadas.

### 4.4 `unordered_list`

Idêntico a `ordered_list` mas com `"type": "unordered_list"`. A renderização (marcadores vs. numeração) é determinada pelo tipo de nó, não pelo NDT.

### 4.5 `table`

```json
{
  "type": "table",
  "rows": [
    {
      "cells": [
        { "header": true, "content": [ { "type": "paragraph", "content": [ { "type": "text", "text": "Coluna A" } ] } ] },
        { "header": true, "content": [ { "type": "paragraph", "content": [ { "type": "text", "text": "Coluna B" } ] } ] }
      ]
    },
    {
      "cells": [
        { "content": [ { "type": "paragraph", "content": [ { "type": "text", "text": "Valor 1" } ] } ] },
        { "content": [ { "type": "paragraph", "content": [ { "type": "text", "text": "Valor 2" } ] } ] }
      ]
    }
  ]
}
```

#### `table`

| Campo | Tipo | Obrigatório |
|---|---|---|
| `type` | `"table"` | Sim |
| `rows` | array de TableRow | Sim — mínimo 1 linha |

#### `TableRow`

| Campo | Tipo | Obrigatório |
|---|---|---|
| `cells` | array de TableCell | Sim — mínimo 1 célula |

#### `TableCell`

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `content` | array de Bloco | Sim — mínimo 1 bloco | Conteúdo da célula |
| `header` | boolean | OPCIONAL | `true` indica célula de cabeçalho (renderizadores usam `<th>`). NÃO DEVE ser `false` — omitir quando não aplicável. |
| `colspan` | inteiro ≥ 1 | OPCIONAL | Expansão horizontal. NÃO DEVE ser `1` — omitir quando não aplicável. |
| `rowspan` | inteiro ≥ 1 | OPCIONAL | Expansão vertical. NÃO DEVE ser `1` — omitir quando não aplicável. |

**Nota sobre span**: valores `colspan`/`rowspan` NÃO implicam células fantasma na serialização NCRTF — o modelo declara apenas as células existentes. Renderizadores são responsáveis por calcular o layout de grelha.

### 4.6 `image`

```json
{
  "type": "image",
  "ref": "assets/grafico-1.png",
  "alt": "Gráfico de evolução trimestral de processos",
  "width": 800,
  "height": 450
}
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"image"` | Sim | |
| `ref` | string | Sim | Caminho relativo dentro do `.ndfpkg`. Ver §8. |
| `alt` | string | Sim | Texto alternativo — obrigatório para acessibilidade e preservação. |
| `width` | inteiro ≥ 1 | OPCIONAL | Largura em píxeis do original (informativo). |
| `height` | inteiro ≥ 1 | OPCIONAL | Altura em píxeis do original (informativo). |

`image` é um nó folha — NÃO TEM `content`. Imagens NÃO DEVEM ser codificadas em base64 dentro do valor NCRTF (ver §8).

---

## 5. Nós inline e marcas

### 5.1 `text`

O único nó inline desta versão. Representa uma sequência de caracteres com formatação opcional.

```json
{ "type": "text", "text": "conteúdo textual" }
{ "type": "text", "text": "H", "marks": ["subscript"] }
{ "type": "text", "text": "negrito e itálico", "marks": ["bold", "italic"] }
```

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `type` | `"text"` | Sim | |
| `text` | string | Sim — mínimo 1 caracter | Conteúdo textual. NÃO DEVE ser string vazia. |
| `marks` | array de Mark | OPCIONAL | Formatação aplicada. Se presente, DEVE ter pelo menos 1 elemento. |

### 5.2 Marcas disponíveis (`Mark`)

| Mark | Renderização típica | Notas |
|---|---|---|
| `"bold"` | Negrito | |
| `"italic"` | Itálico | |
| `"underline"` | Sublinhado | |
| `"subscript"` | Subscrito (ex: H₂O) | NÃO DEVE coexistir com `"superscript"` no mesmo nó |
| `"superscript"` | Sobrescrito (ex: m²) | NÃO DEVE coexistir com `"subscript"` no mesmo nó |

### 5.3 Ordem canónica das marcas

Para garantir canonicalização determinística (§6), o array `marks` **DEVE** estar ordenado alfabeticamente:

```
bold → italic → subscript → superscript → underline
```

Implementações produtoras DEVEM ordenar as marcas antes de serializar. Leitores DEVEM rejeitar documentos com `marks` fora desta ordem.

### 5.4 Contiguidade de texto

Nós `text` consecutivos com as mesmas marcas DEVEM ser fundidos num único nó. Exemplo não-conforme:

```json
// NÃO CONFORME — dois nós text com as mesmas marcas contíguos
[
  { "type": "text", "text": "ne", "marks": ["bold"] },
  { "type": "text", "text": "grito", "marks": ["bold"] }
]

// CONFORME
[
  { "type": "text", "text": "negrito", "marks": ["bold"] }
]
```

Esta regra garante canonicalidade da estrutura, não apenas dos bytes JSON.

---

## 6. Regras de canonicalização

A canonicalização NCRTF é uma pré-condição para a assinabilidade do campo quando embebido num NDF-core.

### 6.1 Canonicalização JCS (RFC 8785)

Todo o valor NCRTF (incluindo o objecto raiz e todos os nós filhos) **DEVE** ser canonicalizado via JCS antes de ser incorporado no `payload_bytes` do NDF-core. JCS garante:

- Chaves de objectos ordenadas lexicograficamente (Unicode code point)
- Sem whitespace extra
- Números em formato canónico
- Strings em UTF-8 com escapes mínimos

### 6.2 Restrições adicionais à estrutura

As seguintes restrições complementam o JCS e asseguram unicidade da representação:

| Regra | Descrição |
|---|---|
| **R1** | `marks` DEVE estar ordenado conforme §5.3 |
| **R2** | Nós `text` contíguos com marcas idênticas DEVEM ser fundidos (§5.4) |
| **R3** | Campos booleanos opcionais com valor `false` NÃO DEVEM estar presentes (omitir) |
| **R4** | Campos inteiros opcionais com valor `1` (`colspan`, `rowspan`) NÃO DEVEM estar presentes (omitir) |
| **R5** | Arrays vazios NÃO DEVEM estar presentes — omitir o campo em vez de `[]` |
| **R6** | `text` NÃO DEVE ser string vazia — dividir em nós separados ou omitir |

### 6.3 Validação da canonicalização

Um produtor conforme **DEVE** verificar, após serializar para JSON, que:

```
JCS(parse(serialize(ncrtf))) == serialize(ncrtf)
```

Ou seja, re-canonicalizar o valor já serializado produz bytes idênticos.

---

## 7. Integração com NDT

### 7.1 Declaração de campo NCRTF num NDT

Um campo de rich text num NDT DEVE ser declarado com `"type": "ncrtf"`:

```json
{
  "name": "corpo",
  "type": "ncrtf",
  "label": "Corpo do documento",
  "required": true
}
```

O sistema de validação do NDT usa o schema `specs/ncrtf/schemas/ncrtf.schema.json` para validar campos deste tipo.

### 7.2 Exemplo — campo `corpo` num NDF-core

```json
{
  "documento": {
    "numero": "OF/2026/00123",
    "data": "2026-06-18",
    "destinatario": { "nome": "Maria da Silva", "cargo": "Directora de Serviços" },
    "corpo": {
      "ncrtf_version": "1.0.0",
      "content": [
        {
          "type": "paragraph",
          "content": [
            { "type": "text", "text": "Em resposta ao ofício n.º 45/2026, informamos que o processo se encontra em fase de análise." }
          ]
        },
        {
          "type": "paragraph",
          "content": [
            { "type": "text", "text": "Apresentamos em anexo o quadro resumo das diligências efectuadas:" }
          ]
        },
        {
          "type": "table",
          "rows": [
            {
              "cells": [
                { "header": true, "content": [ { "type": "paragraph", "content": [ { "type": "text", "text": "Data" } ] } ] },
                { "header": true, "content": [ { "type": "paragraph", "content": [ { "type": "text", "text": "Diligência" } ] } ] },
                { "header": true, "content": [ { "type": "paragraph", "content": [ { "type": "text", "text": "Estado" } ] } ] }
              ]
            },
            {
              "cells": [
                { "content": [ { "type": "paragraph", "content": [ { "type": "text", "text": "2026-06-01" } ] } ] },
                { "content": [ { "type": "paragraph", "content": [ { "type": "text", "text": "Notificação ao interessado" } ] } ] },
                { "content": [ { "type": "paragraph", "content": [ { "type": "text", "text": "Concluída" } ] } ] }
              ]
            }
          ]
        },
        {
          "type": "paragraph",
          "content": [
            { "type": "text", "text": "A fórmula aplicada foi: E = mc" },
            { "type": "text", "text": "2", "marks": ["superscript"] },
            { "type": "text", "text": "." }
          ]
        }
      ]
    }
  }
}
```

### 7.3 Retrocompatibilidade com campos `string`

NDTs existentes que declarem `"type": "string"` para campos como `corpo` continuam a funcionar com plain text. A migração para `"type": "ncrtf"` requer um bump de versão do NDT (ex: `oficio-generico@1.0.0` → `oficio-generico@2.0.0`).

O NDF-core que referenciar `oficio-generico@2.0.0` via `ndt_version_ref` terá o `corpo` como objecto NCRTF; o que referenciar `@1.0.0` terá string. Ambos os formatos são válidos para as respectivas versões do NDT — não há quebra de retrocompatibilidade ao nível do NDF.

---

## 8. Integração com `.ndfpkg`

### 8.1 Referências de imagem

O campo `ref` de um nó `image` é um caminho relativo dentro do arquivo `.ndfpkg`:

```
assets/grafico-evolucao.png
assets/organograma-2026.svg
recursos/foto-assinatura.jpg
```

O caminho DEVE:
- Ser relativo à raiz do `.ndfpkg`
- Usar `/` como separador (independentemente do SO)
- Referenciar um ficheiro presente no arquivo
- Ter uma entrada correspondente no `manifest.inventario` do `.ndfpkg`

Imagens NÃO DEVEM ser embutidas como base64 no valor NCRTF — fazê-lo tornaria o `payload_hash` instável a qualquer alteração da imagem e incharia o registo de base de dados.

### 8.2 Formatos de imagem suportados

| Formato | Extensão | Notas |
|---|---|---|
| PNG | `.png` | RECOMENDADO para gráficos e diagramas |
| SVG | `.svg` | RECOMENDADO para vectorial; renderizadores devem sanitizar SVG |
| JPEG | `.jpg` / `.jpeg` | RECOMENDADO para fotografias |
| PDF/A | `.pdf` | OPCIONAL — para sub-documentos em imagem |

### 8.3 Exemplo de estrutura `.ndfpkg` com imagens

```
oficio-OF-2026-00123.ndfpkg
├── manifest.json          (inventário com hash das imagens)
├── ndf-core.json          (contém o campo corpo em NCRTF)
├── envelope.json
├── ndt/
│   └── oficio-generico@2.0.0.ndt.json
└── assets/
    └── grafico-evolucao.png
```

---

## 9. Extensibilidade

### 9.1 Política de extensão

O NCRTF v1.0.0 define um subconjunto intencional. Novos tipos de nó e marcas podem ser adicionados em versões futuras:

| Mudança | Versão SemVer |
|---|---|
| Novo tipo de nó bloco OPCIONAL | MINOR |
| Nova marca OPCIONAL | MINOR |
| Novo campo OPCIONAL num nó existente | MINOR |
| Alteração de campo obrigatório / remoção de nó | MAJOR |
| Alteração das regras de canonicalização | MAJOR |

### 9.2 Nós desconhecidos

Um leitor conforme que encontre um `type` desconhecido num bloco ou inline:
- Se a versão MAJOR de `ncrtf_version` for igual à suportada: **DEVE** ignorar o nó e continuar a processar os restantes.
- Se a versão MAJOR for superior: **DEVE** rejeitar o documento inteiro.

### 9.3 Candidatos a versões futuras

Os seguintes elementos **não fazem parte de v1.0.0** mas estão antecipados para versões MINOR:

| Elemento | Tipo | Motivação |
|---|---|---|
| `code_block` | Bloco | Documentos técnicos com excertos de código |
| `blockquote` | Bloco | Citações de documentos referenciados |
| `horizontal_rule` | Bloco | Separador de secções |
| `"strikethrough"` | Marca | Texto riscado (actas, rectificações) |
| `"code"` | Marca | Inline monospace |
| `caption` em `image` | Campo | Legenda de figura |
| `start` em `ordered_list` | Campo | Numeração inicial diferente de 1 |

---

## 10. Conformidade

### 10.1 Produtor conforme

Uma implementação é um **produtor NCRTF conforme** se:

1. **DEVE** gerar valores NCRTF que validam contra `specs/ncrtf/schemas/ncrtf.schema.json`.
2. **DEVE** aplicar todas as regras de canonicalização R1–R6 (§6.2).
3. **DEVE** verificar que `JCS(parse(serialize(ncrtf))) == serialize(ncrtf)` antes de incorporar o valor num NDF-core.
4. **NÃO DEVE** incluir nós `image` com `ref` que não existam no `manifest.inventario` do `.ndfpkg`.
5. **NÃO DEVE** codificar imagens em base64 dentro de valores NCRTF.
6. **DEVE** ordenar `marks` conforme §5.3.
7. **DEVE** fundir nós `text` contíguos com marcas idênticas (§5.4).

### 10.2 Leitor conforme

Uma implementação é um **leitor NCRTF conforme** se:

1. **DEVE** rejeitar qualquer valor NCRTF que não valide contra o schema desta versão.
2. **DEVE** rejeitar documentos com `marks` fora da ordem canónica (R1).
3. **DEVE** ignorar nós de tipo desconhecido quando `ncrtf_version` MAJOR for igual ao suportado.
4. **DEVE** rejeitar o documento quando `ncrtf_version` MAJOR for superior ao suportado.
5. **DEVE** resolver referências `image.ref` dentro do `.ndfpkg` corrente.

---

## 11. Glossário

| Termo | Definição |
|---|---|
| **Bloco** | Nó de nível superior na hierarquia NCRTF: `paragraph`, `heading`, `ordered_list`, `unordered_list`, `table`, `image`. |
| **Canonicalização** | Processo de serialização determinística que produz sempre os mesmos bytes para a mesma estrutura lógica. |
| **Inline** | Nó filho de um bloco que contém texto com formatação. Em v1.0.0, apenas `text`. |
| **JCS** | JSON Canonicalization Scheme, RFC 8785. Algoritmo de canonicalização JSON. |
| **Marca** | Atributo de formatação aplicado a um nó `text`: `bold`, `italic`, `underline`, `subscript`, `superscript`. |
| **NDT** | NORMORDIS Document Template — declara campos de tipo `ncrtf`. |
| **NDF-core** | NORMORDIS Document Format core — JSON assinável que contém valores NCRTF como campos. |
| **`.ndfpkg`** | Arquivo ZIP que agrupa NDF-core, envelope, NDT e recursos (incluindo imagens referenciadas por NCRTF). |
| **Produtor** | Sistema que gera valores NCRTF conformes e os incorpora em NDF-core. |
| **Leitor** | Sistema que consome, valida e renderiza valores NCRTF. |
