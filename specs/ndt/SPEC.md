# Especificação NDT v2.0.0

**NORMORDIS Document Template — Especificação Formal**

Estado: Draft para implementação
Âmbito: formato declarativo de layout para descrever a composição visual de qualquer documento institucional — desde impressos fiscais complexos (ex.: Modelo 3 IRS) a documentos administrativos correntes (ofícios, informações, despachos).

## Licenciamento

Esta especificação (texto, estrutura, JSON Schemas e exemplos associados) é disponibilizada sob **CC0 1.0** (domínio público). O objetivo é que qualquer produtor de software para a Administração Pública — open source ou proprietário — possa implementar leitura e renderização de NDT livremente, sem qualquer obrigação contratual ou de licenciamento para com o autor da especificação.

A **implementação de referência** (`normordis-pdf`, bibliotecas Rust) é distribuída sob licença separada (EUPL v1.2), indicada no respetivo repositório. Esta especificação é licenciada separadamente (`LICENSE-SPEC`) precisamente para que a adoção do formato não dependa da licença do código.

---

## 1. Axioma e papel do NDT

**NDT + NDF = documento físico determinístico e rico.**

- **NDT** (este formato) — descreve *como* o documento é composto visualmente: estrutura de páginas, posições, elementos gráficos, tipografia, tabelas de dados, mobília.
- **NDF** (spec NDF v1.0.0) — fornece *o quê*: os dados a apresentar, já computados e materializados pela app de domínio.
- **Renderer** (normordis-pdf, typst, ou qualquer implementação conforme) — combina NDT + NDF para produzir o documento. É um executor puro: não valida dados, não computa valores, não aplica regras de negócio.

**Implicações directas:**

1. O NDT não contém regras de validação, fórmulas de cálculo, obrigatoriedade de campos, nem qualquer lógica de negócio. Esses são responsabilidade exclusiva da app de domínio que produz o NDF.
2. O NDF que chega ao renderer está completo nos seus dados. O renderer não precisa de saber que `valor_realizacao` é monetário obrigatório — só precisa de saber onde o colocar e como formatá-lo.
3. O mesmo NDT + mesmo NDF produz sempre o mesmo documento, independentemente de renderer, data ou contexto de execução.

### 1.1 Referência NDF ↔ NDT

O NDF referencia o NDT necessário para a sua renderização, mas não o incorpora — mantém-se eficiente (apenas dados e metadados). O renderer busca o NDT no registry no momento da renderização.

| NDF-core | NDT | Significado |
|---|---|---|
| `metadados.tipo_documento_ref` | `schema_id` | Identifica o tipo de documento |
| `ndt_version_ref` | `schema_id@versao_ndt` | Identifica a versão concreta do template |

Para documentos **fechados/assinados**, o NDF guarda adicionalmente `ndt_hash` (SHA-256 do NDT no momento do fecho), garantindo reprodutibilidade bit-perfeita mesmo que o registry evolua.

### 1.2 Duas fases de uso do NDT

| Fase | Estado NDF | Papel do NDT |
|---|---|---|
| **Apresentação de formulário** | `rascunho` | A app de domínio usa o NDT para saber que campos existem e como estruturar a UI de preenchimento. O NDF está incompleto. |
| **Renderização** | qualquer | O NDT é o único guia visual. O NDF fornece os dados. O renderer segue o NDT à risca. |

Após o fecho do NDF, o NDT é irrelevante para qualquer operação sobre o conteúdo — é relevante apenas para re-renderização.

### 1.3 Fidelidade por formato de saída

O NDT define um layout prescritivo para PDF/impressão. Para outros formatos, o contrato é diferente — o conteúdo é fiel; o layout é adaptado às convenções de cada formato.

| Formato | Momento no ciclo de vida | Fidelidade de layout | Fidelidade de conteúdo | Fonte de layout |
|---|---|---|---|---|
| **PDF / PDF/A** | Arquivo, prova, entrega formal | **Normativa** — bit-idêntico para o mesmo NDT+NDF | Total | Bloco `layout` do NDT (§5) |
| **ODF** | Intercâmbio, edição, revisão | Best-effort — renderer usa `estilos` NDT (§3) | Total | Bloco `estilos` do NDT (§3) |
| **HTML** | Publicação, intranet, consulta | Best-effort — layout é CSS flow | Total | Bloco `estilos` do NDT (§3) |
| **Typst** | Composição tipográfica avançada | Alta — mm coords são dicas; renderer adapta | Total | Bloco `layout` do NDT (§5) |
| **Outros** | Não especificado | Não especificado | Via NCRTF no NDF | — |

**Fidelidade de conteúdo** significa que o texto, tabelas, listas, imagens e estrutura semântica do documento são preservados identicamente. **Fidelidade de layout** significa que posições, fontes, margens e paginação são reproduzidas com exactidão.

**PDF/A e ODF servem momentos distintos** — não são equivalentes. PDF/A é o artefacto de arquivo e prova legal: imutável, bit-idêntico, verificável por hash. ODF é o formato de intercâmbio e trabalho: editável por qualquer implementação conforme (LibreOffice, Collabora, OpenOffice, EuroOffice, OnlyOffice) sem dependência de licença proprietária. Um documento finalizado produz ambos a partir do mesmo NDT+NDF; são duas projecções da mesma fonte de verdade.

**ODF como formato secundário** alinha-se com os princípios de soberania digital da spec NDF e com o RNID (Regulamento Nacional de Interoperabilidade Digital). Para a Administração Pública portuguesa, ODF é o formato de intercâmbio recomendado para documentos editáveis.

Para ODF e HTML, o bloco `layout` do NDT pode ser ignorado pelo renderer; o bloco `estilos` (§3) é a fonte de verdade para estilo. Um renderer ODF conforme produz um documento profissional e fiel no conteúdo — não uma cópia pixel-perfect do PDF.

**Elementos sem equivalente em formatos de fluxo**: `grelha_digitos`, `tabela_visual`, `rectangulo`, `linha`, `min_linhas_visivel` e `assinatura` (como AcroForm PDF) não têm equivalente directo em ODF/HTML. Renderers de fluxo podem ignorá-los ou usar aproximações (ex.: `grelha_digitos` → campo de texto ODF; `assinatura` → linha de assinatura ODF com macro de captura).

---

## 2. Identidade e versionamento

```json
{
  "ndt_version": "2.0.0",
  "schema_id": "modelo3-irs-anexoG",
  "versao_ndt": "2026.1",
  "titulo": "Modelo 3 IRS — Anexo G",
  "emissor": "AT",
  "referencia_legal": "Portaria n.º .../2026"
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `ndt_version` | Sim | Versão do **formato NDT** (SemVer). Só muda com alterações ao próprio formato. |
| `schema_id` | Sim | Identificador estável do tipo de documento. Imutável — identifica o tipo, não a versão. |
| `versao_ndt` | Sim | Versão desta instância do template (ex.: `"2026.1"` para o impresso fiscal de 2026). |
| `titulo` | Não | Nome legível do template. |
| `emissor` | Não | Entidade emissora (ex.: `"AT"`, `"SS"`). |
| `referencia_legal` | Não | Referência legal do impresso (ex.: portaria). |

**Regra de versionamento**: `ndt_version` segue SemVer — versões minor adicionam campos opcionais sem quebrar leitores existentes; versões major introduzem mudanças incompatíveis.

---

## 3. Estilos globais do documento

O bloco `estilos` declara os valores por defeito de tipografia e espaçamento para o documento inteiro. É a **fonte principal de estilo para renderers de fluxo** (ODF, HTML) e serve como fallback para renderers PDF onde elementos não declarem fonte própria.

```json
{
  "estilos": {
    "fonte_padrao": { "familia": "Times", "tamanho": 11 },
    "cor_texto": "#1A1A1A",
    "cor_primaria": "#003366",
    "espacamento_entre_paragrafos_mm": 4,
    "identacao_lista_mm": 6,
    "cabecalhos": [
      { "nivel": 1, "fonte": { "tamanho": 14, "peso": "bold" } },
      { "nivel": 2, "fonte": { "tamanho": 12, "peso": "bold" } },
      { "nivel": 3, "fonte": { "tamanho": 11, "peso": "bold", "estilo": "italico" } }
    ]
  }
}
```

| Campo | Descrição |
|---|---|
| `fonte_padrao` | Fonte base do documento. Propagada a todos os elementos sem fonte declarada. |
| `cor_texto` | Cor de texto por defeito (hex). |
| `cor_primaria` | Cor de destaque institucional — usada em cabeçalhos, linhas decorativas, etc. |
| `espacamento_entre_paragrafos_mm` | Espaço vertical entre parágrafos NCRTF. |
| `identacao_lista_mm` | Indentação por nível de lista NCRTF. |
| `cabecalhos[]` | Estilos por nível de heading NCRTF (1–6). |

Um renderer ODF mapeia `estilos` para estilos de parágrafo nativos (`Default Paragraph Style`, `Heading 1`, etc.). Um renderer HTML mapeia para variáveis CSS (`--font-primary`, `--color-text`, etc.). Um renderer PDF usa `fonte_padrao` como fallback onde nenhum elemento declara fonte própria.

---

## 4. Endereçamento de dados NDF

O NDT referencia valores do NDF através de **caminhos canónicos** — strings que identificam um valor pelo seu percurso hierárquico de identificadores. O NDF armazena valores nessas mesmas posições.

A hierarquia é uma **convenção de endereçamento**, não um schema. O NDT não valida se o caminho existe no NDF nem o tipo do valor — o renderer escreve o que encontrar, ou deixa em branco se o caminho não existir.

### 4.1 Caminhos simples

```
identificacao.nif_titular
quadro5.total_mais_valias
flags.incluir_anexoG
```

### 4.2 Arrays e iteração

Para tabelas com N linhas, o caminho referencia o array; as colunas identificam propriedades de cada item:

```
quadro4.imoveis              → array de linhas
quadro4.imoveis[i].freguesia → propriedade de uma linha
```

O NDT não precisa de conhecer o comprimento do array — o renderer itera sobre os itens presentes no NDF.

### 4.3 Formatos de display

O NDT pode declarar um **formato de display** para orientar o renderer na apresentação visual de um valor. Não é um tipo de dados com validação — é uma hint de renderização.

| Formato | Apresentação visual |
|---|---|
| `"texto"` | Valor tal qual (default) |
| `"numero"` | Numérico com separador de milhar |
| `"inteiro"` | Inteiro sem casas decimais |
| `"monetario"` | Valor monetário com duas casas decimais e separador de milhar |
| `"data"` | Data formatada (DD/MM/YYYY) |
| `"booleano"` | `true`/`false` → símbolo visual (✓/✗) |
| `"checkbox"` | Caixa de verificação marcada/desmarcada |
| `"radio"` | Ponto de seleção ativo/inativo |

Formatos numéricos aceitam o parâmetro opcional `"casas_decimais"` (inteiro). Default: `2` para `"monetario"`, `0` para `"inteiro"`, variável para `"numero"`.

---

## 5. Layout (PDF e impressão)

O bloco `layout` descreve a composição visual prescritiva do documento para PDF e impressão. É **normativo para renderers PDF**; renderers de fluxo (ODF, HTML) podem ignorá-lo em favor de `estilos` (§3).

### 5.1 Configuração global de página

```json
{
  "layout": {
    "formato": "A4",
    "orientacao": "portrait",
    "margens": { "topo": 20, "fundo": 20, "esq": 15, "dir": 15 }
  }
}
```

`formato`: `"A4"` | `"A3"` | `"Letter"` | `{ "largura": num, "altura": num }` (mm).
`orientacao`: `"portrait"` | `"landscape"`.
`margens`: em milímetros. Aplica-se a todas as `paginas_def[]` que não declarem margens próprias.

### 5.2 Definições de página (`paginas_def[]`)

A unidade fundamental do layout é a **definição de página** (`pagina_def`). Cada página estruturalmente distinta — rosto, Anexo G página 1, página de dados adicional, página de fecho — é uma `pagina_def` própria. Repetição é controlada por `sequencia[]` (§5.7).

Cada `pagina_def` organiza os seus elementos em cinco colecções. Todas partilham o sistema de coordenadas: **milímetros, origem `(0,0)` no canto superior-esquerdo da área útil** (dentro das margens).

| Colecção | Propósito |
|---|---|
| `graficos[]` | Elementos visuais puros a coordenadas absolutas: linhas, caixas, imagens, texto estático, assinaturas (§5.3) |
| `campos[]` | Valores NDF escalares a coordenadas absolutas (§5.4) |
| `blocos[]` | Conteúdo estruturado a coordenadas absolutas: tabelas de dados, corpo de texto (§5.5) |
| `fluxo` | Elementos que se empilham verticalmente em sequência — para documentos com corpo de extensão variável (§5.2.1) |
| `mobilia[]` | Numeração de página, marca de água, textos de rodapé (§5.6) |

```json
{
  "paginas_def": [
    {
      "id": "rosto",
      "formato": "A4",
      "margens": { "topo": 25, "fundo": 20, "esq": 15, "dir": 15 },
      "graficos": [],
      "campos": [],
      "blocos": [],
      "fluxo": null,
      "mobilia": []
    }
  ]
}
```

`formato` e `margens` numa `pagina_def` sobrepõem-se à configuração global para essa página.

#### 5.2.1 Layout de fluxo (`fluxo`)

Para documentos administrativos onde o corpo tem extensão variável (ofícios, relatórios, informações), os elementos que se seguem ao corpo — fórmula de encerramento, bloco de assinatura, data — precisam de aparecer *depois de onde o corpo terminar*, não em coordenadas absolutas fixas.

O objecto `fluxo` declara uma **região de fluxo vertical** dentro da `pagina_def`: os seus elementos empilham-se de cima para baixo a partir de `y_inicio`, ocupando a altura que o conteúdo requerer.

```json
{
  "id": "oficio_pag1",
  "graficos": [
    { "tipo": "imagem", "referencia_recurso": "brasao.svg", "posicao": { "x": 15, "y": 10 }, "largura": 25, "altura": 25 }
  ],
  "campos": [
    { "referencia": "cabecalho.referencia", "posicao": { "x": 120, "y": 38 }, "largura": 75, "altura": 6, "alinhamento": "direita" },
    { "referencia": "cabecalho.data", "posicao": { "x": 120, "y": 46 }, "largura": 75, "altura": 6, "formato": "data", "alinhamento": "direita" }
  ],
  "fluxo": {
    "y_inicio": 60,
    "elementos": [
      { "tipo": "corpo", "referencia": "conteudo.corpo" },
      { "tipo": "espaco", "altura": 10 },
      { "tipo": "texto_fixo", "conteudo": "Com os melhores cumprimentos," },
      { "tipo": "espaco", "altura": 20 },
      { "tipo": "assinatura", "id": "sig_autor", "rotulo": "O Dirigente", "largura": 80, "altura": 25 },
      { "tipo": "campo", "referencia": "signatario.nome", "formato": "texto" },
      { "tipo": "campo", "referencia": "signatario.cargo", "formato": "texto" }
    ]
  },
  "mobilia": [
    { "tipo": "numero_pagina", "formato": "Pág. {n}/{total}", "posicao": { "x": 180, "y": 285 }, "fonte": { "tamanho": 8 } }
  ]
}
```

**Comportamento de overflow do `corpo` dentro do `fluxo`**: quando o conteúdo NCRTF de um elemento `tipo: "corpo"` não cabe na área disponível (entre `y_inicio` e o limite inferior da área útil), o overflow é gerido por `sequencia[]` (§5.7) da mesma forma que um `bloco corpo` absoluto. Os elementos de `fluxo.elementos` que aparecem **depois** do `corpo` são renderizados na **última página** da sequência de overflow, imediatamente após o fim do corpo. Os elementos **antes** do `corpo` são renderizados apenas na primeira instância da `pagina_def`.

**Elementos suportados em `fluxo.elementos`:**

| `tipo` | Descrição |
|---|---|
| `corpo` | Bloco de texto NCRTF com fluxo (`referencia` = caminho NDF). Único por `fluxo`; o overflow propaga-se pela `sequencia[]`. |
| `tabela` | Tabela de dados NDF (mesma estrutura de `blocos[]` tipo tabela, §5.5.1). Sem `posicao` — posicionada automaticamente. |
| `texto_fixo` | Texto estático ou com placeholders NDT (`{{versao_ndt}}`). Faz wrapping automático na largura disponível. |
| `campo` | Valor NDF escalar (mesma semântica de `campos[]`, §5.4, sem `posicao`). |
| `imagem` | Imagem a partir de um recurso (§5.9). Campos: `referencia_recurso`, `largura`, `altura`, `manter_proporcao`, `alinhamento`, `alt`. |
| `espaco` | Espaço vertical explícito. Campos: `altura` (mm). |
| `separador` | Linha horizontal. Campos: `espessura` (mm, default 0.3), `cor` (hex). |
| `assinatura` | Campo de assinatura (§5.3.6). Sem `posicao` — posicionado em fluxo. |
| `linha_lateral` | Agrupa dois ou mais elementos lado a lado numa mesma linha horizontal. Ver §5.2.2. |
| `quebra_pagina` | Força início de nova página. O renderer termina a instância actual da `pagina_def` e avança para a seguinte entrada em `sequencia[]`. Sem campos adicionais. |

Todos os elementos de `fluxo.elementos` aceitam `"incluir_se"` (ver §5.4) para renderização condicional.

`fluxo` e `blocos[]` são **mutuamente exclusivos** na mesma `pagina_def`: uma página usa um dos dois modelos para o conteúdo principal. `graficos[]`, `campos[]` e `mobilia[]` coexistem com qualquer modelo.

#### 5.2.2 Layout lateral em fluxo (`linha_lateral`)

Agrupa elementos de `fluxo` lado a lado numa mesma linha horizontal. Útil para blocos de dupla assinatura, datas com referências, ou qualquer par/grupo de elementos que devem partilhar a largura disponível.

```json
{
  "tipo": "linha_lateral",
  "elementos": [
    {
      "largura": 90,
      "conteudo": [
        { "tipo": "assinatura", "id": "sig_dirigente", "rotulo": "O Dirigente", "largura": 80, "altura": 25 },
        { "tipo": "campo", "referencia": "signatario_a.nome" },
        { "tipo": "campo", "referencia": "signatario_a.cargo" }
      ]
    },
    {
      "largura": 90,
      "conteudo": [
        { "tipo": "assinatura", "id": "sig_secretario", "rotulo": "O Secretário", "largura": 80, "altura": 25 },
        { "tipo": "campo", "referencia": "signatario_b.nome" },
        { "tipo": "campo", "referencia": "signatario_b.cargo" }
      ]
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `elementos[]` | Sim | Array de colunas laterais. |
| `elementos[].largura` | Sim | Largura da coluna (mm). A soma das larguras não deve exceder a largura útil da `pagina_def`. |
| `elementos[].conteudo[]` | Sim | Lista de elementos de fluxo dentro desta coluna. Aceita todos os tipos de `fluxo.elementos` excepto `corpo` e `linha_lateral` (não aninhável). |

**Comportamento de altura**: a `linha_lateral` tem a altura do elemento mais alto entre as suas colunas. As colunas mais curtas deixam espaço em branco abaixo. Cada coluna empilha os seus elementos verticalmente da mesma forma que `fluxo.elementos`.

### 5.3 Elementos gráficos (`graficos[]`)

Elementos visuais a coordenadas absolutas. Sem ligação a dados do NDF, excepto `grelha_digitos` e `codigo_barras` que referenciam caminhos NDF para o seu conteúdo.

> **Nota normativa**: o NDT não é uma linguagem de desenho genérica. As primitivas existem para suportar documentos institucionais. Novas primitivas são adicionadas apenas quando representem padrões recorrentes de documentação administrativa.

Todos os elementos gráficos partilham o campo discriminante `"tipo"` e dois campos opcionais transversais:

- `"layer"`: camada de renderização — `"background"` | `"content"` (default) | `"foreground"` | `"overlay"`
- `"rotacao"`: rotação em graus no sentido horário (qualquer valor numérico)

#### 5.3.1 `linha`

```json
{
  "tipo": "linha",
  "de": { "x": 15, "y": 40 },
  "para": { "x": 195, "y": 40 },
  "espessura": 0.3,
  "cor": "#000000",
  "estilo": "solido"
}
```

`estilo`: `"solido"` | `"tracejado"` | `"ponteado"`.

#### 5.3.2 `rectangulo`

```json
{
  "tipo": "rectangulo",
  "posicao": { "x": 15, "y": 45 },
  "largura": 180,
  "altura": 30,
  "preenchimento": "none",
  "contorno": { "espessura": 0.3, "cor": "#000000" },
  "raio_canto": 0
}
```

`preenchimento`: `"none"` | cor hex. `raio_canto`: mm; `0` = ângulos rectos.

#### 5.3.3 `grelha_digitos`

Primitiva específica para impressos fiscais — caixas individuais por carácter (NIFs, datas, códigos postais). Encapsula o padrão "uma caixa por carácter" sem declarar cada caixa individualmente.

```json
{
  "tipo": "grelha_digitos",
  "referencia": "identificacao.nif_titular",
  "posicao": { "x": 60, "y": 52 },
  "num_caixas": 9,
  "largura_caixa": 5,
  "altura_caixa": 6,
  "espacamento": 0.5,
  "cor_contorno": "#000000",
  "espessura_contorno": 0.3,
  "rotulo_acessivel": "NIF do Titular"
}
```

`referencia`: caminho NDF cujos caracteres preenchem as caixas (esquerda para direita); caixas sobrantes ficam vazias.
`rotulo_acessivel`: texto legível por leitores de ecrã (PDF/UA-2 `/TU`). Recomendado em todos os `grelha_digitos`; em PDF/UA-2, a ausência gera aviso de conformidade.

#### 5.3.4 `imagem`

```json
{
  "tipo": "imagem",
  "referencia_recurso": "logo-at.svg",
  "posicao": { "x": 15, "y": 10 },
  "largura": 30,
  "altura": 12,
  "manter_proporcao": true
}
```

`referencia_recurso`: id de um recurso declarado em `recursos[]` (§5.9).

#### 5.3.5 `texto_fixo`

Texto estático não proveniente do NDF — títulos, legendas, texto do impresso oficial.

```json
{
  "tipo": "texto_fixo",
  "conteudo": "MODELO 3 — {{versao_ndt}}",
  "posicao": { "x": 150, "y": 12 },
  "fonte": { "familia": "Helvetica", "tamanho": 14, "peso": "bold" },
  "alinhamento": "esquerda"
}
```

`conteudo` aceita dois tipos de placeholders:
- **Metadados NDT** (resolvidos a partir do cabeçalho do NDT): `{{schema_id}}`, `{{versao_ndt}}`, `{{titulo}}`, `{{emissor}}`
- **Valores de envelope** (resolvidos pelo renderer a partir do envelope NDF no momento da renderização): `{{validation_code}}`

`{{validation_code}}` é o código de verificação canónico do NDF (ver NDF spec §4.6). Não é um dado do NDF-core nem um metadado do NDT — é computado durante a finalização e fornecido ao renderer pelo envelope. Deve ser usado no elemento `codigo_barras` e/ou em `texto_fixo` de mobília para emissão de documentos para o exterior.

#### 5.3.6 `assinatura`

Campo de assinatura electrónica ou manuscrita. O campo `modo` controla a relação entre a assinatura CAdES guardada no NDF e o PDF gerado — ver §8.1 para o modelo completo de assinatura.

```json
{
  "tipo": "assinatura",
  "id": "assinatura_titular",
  "rotulo": "O Sujeito Passivo",
  "posicao": { "x": 15, "y": 262 },
  "largura": 80,
  "altura": 25,
  "modo": "hibrido"
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `id` | Sim | Identificador único. Referenciado pelo NDF ao registar a assinatura. |
| `rotulo` | Não | Texto da legenda abaixo do campo de assinatura. |
| `posicao` | Cond. | Coordenadas de origem (mm). Obrigatório em `graficos[]`; omitido em `fluxo.elementos`. |
| `largura` | Sim | Largura do campo (mm). |
| `altura` | Sim | Altura do campo (mm). |
| `modo` | Não | Modo de integração CAdES↔PDF. Default: `"hibrido"`. Ver §8.1. |

**Valores de `modo`:**

| Valor | Comportamento no PDF gerado |
|---|---|
| `"visual_apenas"` | Placeholder visual sem campo AcroForm. A assinatura vive exclusivamente no NDF (CAdES cobre NDF + `pdf_hash`). Adequado quando o receptor verifica via NDF. |
| `"hibrido"` | **(Default)** Cria campo AcroForm PAdES no PDF, preenchido com o mesmo CAdES do NDF (que inclui `pdf_hash` como atributo assinado). O CAdES do NDF é também embutido como attachment PDF/A-3. O PDF é autossuficiente para validadores eIDAS; o NDF é a fonte de verdade. |
| `"ndf_attachment"` | Sem AcroForm. O CAdES do NDF é embutido como attachment PDF/A-3 (`ndf-signature.p7s`). Útil quando o validador de destino suporta PDF/A-3 mas não requer AcroForm. |

Em ODF, `assinatura` é renderizada como linha de assinatura com campo de formulário (`com.sun.star.text.TextField.Input`) e legenda. Em HTML, como `<div class="signature-field" data-id="{{id}}">`. O `modo` é ignorado em formatos de fluxo — aplica-se apenas ao renderer PDF.

#### 5.3.7 `codigo_barras`

```json
{
  "tipo": "codigo_barras",
  "formato_barras": "qrcode",
  "referencia": "sistema.codigo_validacao",
  "posicao": { "x": 170, "y": 270 },
  "largura": 25,
  "altura": 25,
  "nivel_correcao": "M"
}
```

`formato_barras`: `"qrcode"` | `"code128"` | `"ean13"`.
`referencia`: caminho NDF com o valor a codificar. Para conteúdo composto, usar `"conteudo"` (string com interpolações `{{caminho_ndf}}`). Para o código de validação do documento, usar `{{validation_code}}` (resolvido pelo renderer a partir do envelope NDF):

```json
{
  "tipo": "codigo_barras",
  "formato_barras": "qrcode",
  "conteudo": "https://validar.normordis.pt/{{validation_code}}",
  "posicao": { "x": 170, "y": 270 },
  "largura": 25,
  "altura": 25,
  "nivel_correcao": "M"
}
```

`nivel_correcao` (só QR): `"L"` | `"M"` | `"Q"` | `"H"`.

#### 5.3.8 `poligono`

```json
{
  "tipo": "poligono",
  "pontos": [
    { "x": 10, "y": 10 },
    { "x": 30, "y": 10 },
    { "x": 20, "y": 25 }
  ],
  "preenchimento": "none",
  "contorno": { "espessura": 0.3, "cor": "#000000" }
}
```

Lista ordenada de vértices (mm); o último ponto liga ao primeiro.

#### 5.3.9 `elipse`

```json
{
  "tipo": "elipse",
  "centro": { "x": 100, "y": 80 },
  "raio_x": 15,
  "raio_y": 10,
  "preenchimento": "none",
  "contorno": { "espessura": 0.3, "cor": "#000000" }
}
```

Quando `raio_x == raio_y`, a figura é um círculo.

#### 5.3.10 `svg`

```json
{
  "tipo": "svg",
  "referencia_recurso": "fundo-pagina.svg",
  "posicao": { "x": 0, "y": 0 },
  "largura": 210,
  "altura": 297,
  "layer": "background"
}
```

Gráfico vectorial completo de um recurso (§5.9). Independente de resolução.

#### 5.3.11 `tabela_visual`

Grelha de linhas e colunas fixas — estrutura visual do impresso sem dados.

```json
{
  "tipo": "tabela_visual",
  "posicao": { "x": 15, "y": 50 },
  "largura": 180,
  "altura_linha": 6,
  "num_linhas": 10,
  "colunas": [30, 50, 40, 60],
  "contorno": { "espessura": 0.3, "cor": "#000000" }
}
```

`colunas`: array de larguras (mm); a soma deve igualar `largura`.

#### 5.3.12 Sumário de tipos gráficos

| `tipo` | Liga ao NDF? | Uso típico |
|---|---|---|
| `linha` | Não | Separadores, bordas |
| `rectangulo` | Não | Caixas de secção, molduras |
| `grelha_digitos` | Sim — valor do campo | NIFs, datas, códigos em caixas |
| `imagem` | Não | Logótipos, brasões |
| `texto_fixo` | Não (placeholders NDT) | Títulos, legendas do impresso |
| `assinatura` | Não (registada no NDF) | Campo de assinatura electrónica/manuscrita |
| `codigo_barras` | Sim — valor a codificar | Código de validação |
| `poligono` | Não | Setas, formas personalizadas |
| `elipse` | Não | Círculos decorativos |
| `svg` | Não | Fundos vectoriais, gráficos complexos |
| `tabela_visual` | Não | Grelha estrutural do impresso |

### 5.4 Campos posicionados (`campos[]`)

Valores NDF escalares a coordenadas absolutas. Cada entrada em `campos[]` é um valor NDF renderizado numa caixa definida por posição e dimensões.

```json
{
  "campos": [
    {
      "referencia": "identificacao.nif_titular",
      "posicao": { "x": 120, "y": 30 },
      "largura": 60,
      "altura": 7,
      "formato": "texto",
      "fonte": { "familia": "Helvetica", "tamanho": 10 },
      "alinhamento": "esquerda"
    },
    {
      "referencia": "quadro5.total_mais_valias",
      "posicao": { "x": 150, "y": 200 },
      "largura": 45,
      "altura": 7,
      "formato": "monetario",
      "casas_decimais": 2,
      "alinhamento": "direita"
    },
    {
      "referencia": "regime.taxa_especial",
      "posicao": { "x": 20, "y": 140 },
      "largura": 5,
      "altura": 5,
      "formato": "checkbox",
      "incluir_se": "flags.regime_taxa_especial"
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `referencia` | Sim | Caminho NDF do valor a apresentar. |
| `posicao` | Sim | Coordenadas de origem da caixa (mm). |
| `largura` | Sim | Largura da caixa (mm). |
| `altura` | Sim | Altura da caixa (mm). |
| `formato` | Não | Formato de display (§4.3). Default: `"texto"`. |
| `casas_decimais` | Não | Para `"monetario"` e `"numero"`. |
| `fonte` | Não | Ver §5.8. Herda de `estilos.fonte_padrao` se omitido. |
| `alinhamento` | Não | `"esquerda"` \| `"centro"` \| `"direita"`. Default: `"esquerda"`. |
| `preenchimento_fundo` | Não | `"none"` ou cor hex. |
| `rotulo_acessivel` | Não | Texto legível por leitores de ecrã (PDF/UA-2 `/TU`). Obrigatório para campos interactivos (`"checkbox"`, `"radio"`). Se omitido em campos de texto, o renderer usa o valor de `referencia` como fallback. |
| `incluir_se` | Não | Caminho NDF de booleano. Se `false` ou ausente, o elemento é omitido. Ver regra abaixo. |
| `descontinuado` | Não | Default `false`. Ver §8. |

**Regra `incluir_se`**: aceita apenas um caminho NDF directo para um campo booleano. Não é uma expressão — não suporta operadores nem funções. Se o caminho não existir ou o valor não for booleano, o renderer inclui o elemento. Aplica-se a `campos[]`, a `blocos[]` e a `fluxo.elementos`.

**Regra de ausência**: se o caminho NDF não existir ou o valor for nulo, o campo renderiza em branco — sem erro, sem aviso.

### 5.5 Blocos de conteúdo (`blocos[]`)

Conteúdo estruturado a coordenadas absolutas. Um `bloco` difere de um `campo` na sua natureza: um `campo` é um valor escalar; um `bloco` é uma estrutura (tabela de múltiplas linhas, texto com fluxo).

#### 5.5.1 `tabela`

Renderiza um array NDF como tabela de linhas e colunas. As colunas são definidas no NDT com layout visual; os valores provêm do NDF.

```json
{
  "tipo": "tabela",
  "referencia": "quadro4.imoveis",
  "posicao": { "x": 15, "y": 50 },
  "largura": 180,
  "altura_linha": 6,
  "min_linhas_visivel": 8,
  "repete_cabecalho": true,
  "estilo_cabecalho": {
    "fundo": "#EEEEEE",
    "fonte": { "tamanho": 8, "peso": "bold" }
  },
  "incluir_se": null,
  "colunas": [
    {
      "id": "freguesia",
      "cabecalho": "Cód. Freg.",
      "largura": 25,
      "alinhamento": "centro",
      "formato": "texto"
    },
    {
      "id": "data_aquisicao",
      "cabecalho": "Data Aq.",
      "largura": 30,
      "alinhamento": "centro",
      "formato": "data"
    },
    {
      "id": "valor_realizacao",
      "cabecalho": "Valor Realização (€)",
      "largura": 45,
      "alinhamento": "direita",
      "formato": "monetario",
      "casas_decimais": 2
    },
    {
      "id": "mais_valia",
      "cabecalho": "Mais-valia (€)",
      "largura": 45,
      "alinhamento": "direita",
      "formato": "monetario"
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `tipo` | Sim | `"tabela"` |
| `referencia` | Sim | Caminho NDF do array de linhas. |
| `posicao` | Sim (em `blocos[]`; omitido em `fluxo`) | Coordenadas de origem (mm). |
| `largura` | Sim | Largura total (mm). |
| `altura_linha` | Não | Altura de cada linha de dados (mm). |
| `min_linhas_visivel` | Não | Número mínimo de linhas a renderizar. Default: `0`. |
| `repete_cabecalho` | Não | Se `true`, cabeçalho repete no topo de cada página quando a tabela transborda. |
| `incluir_se` | Não | Caminho NDF de booleano (ver §5.4). |
| `colunas[].id` | Sim | Propriedade do item NDF para esta coluna. |
| `colunas[].cabecalho` | Não | Texto do cabeçalho da coluna. |
| `colunas[].largura` | Sim | Largura da coluna (mm). |
| `colunas[].alinhamento` | Não | `"esquerda"` \| `"centro"` \| `"direita"`. |
| `colunas[].formato` | Não | Formato de display (§4.3). Default: `"texto"`. |
| `colunas[].descontinuado` | Não | Default `false`. Ver §8. |

**Regra `min_linhas_visivel`**: o renderer DEVE sempre desenhar a estrutura da tabela (frame, cabeçalho, linhas) e preencher com os itens do NDF. Se o NDF tiver menos itens do que `min_linhas_visivel`, o renderer completa com linhas em branco. Esta regra garante que impressos fiscais apresentam as linhas oficiais mesmo sem dados.

#### 5.5.2 `corpo`

Bloco de texto com fluxo em formato NCRTF, a coordenadas absolutas. Para documentos administrativos com fórmulas de encerramento e assinatura após o corpo, usar o modelo `fluxo` (§5.2.1) em vez de `corpo` em `blocos[]`.

```json
{
  "tipo": "corpo",
  "referencia": "conteudo.corpo",
  "posicao": { "x": 15, "y": 60 },
  "largura": 180,
  "fonte_base": { "familia": "Times", "tamanho": 11 },
  "incluir_se": null
}
```

O renderer renderiza o NCRTF do caminho NDF referenciado a partir de `posicao`, até ao limite inferior da área útil. Overflow gerido por `sequencia[]` (§5.7).

#### 5.5.3 `cabecalho` e `rodape`

Blocos de cabeçalho ou rodapé de documento (não de página — para mobília de página ver §5.6).

```json
{
  "tipo": "cabecalho",
  "referencia": "cabecalho",
  "posicao": { "x": 45, "y": 10 },
  "largura": 150,
  "incluir_se": null
}
```

`referencia` aponta para o path NDF com os dados do cabeçalho. A disposição visual interna é definida pelos `campos[]` e `graficos[]` da mesma `pagina_def`.

### 5.6 Mobília de página (`mobilia[]`)

Elementos fixos de cada `pagina_def`. Cada `pagina_def` tem a sua própria `mobilia` — páginas diferentes podem ter numerações e marcas de água distintas.

```json
{
  "mobilia": [
    {
      "tipo": "numero_pagina",
      "formato": "Página {n} de {total}",
      "posicao": { "x": 180, "y": 285 },
      "fonte": { "familia": "Helvetica", "tamanho": 8, "cor": "#666666" }
    },
    {
      "tipo": "texto_fixo",
      "conteudo": "Modelo 3 — {{versao_ndt}}",
      "posicao": { "x": 15, "y": 285 },
      "fonte": { "familia": "Helvetica", "tamanho": 8 }
    },
    {
      "tipo": "marca_agua",
      "conteudo": "RASCUNHO",
      "opacidade": 0.15,
      "angulo": 45,
      "fonte": { "familia": "Helvetica", "tamanho": 60, "peso": "bold", "cor": "#FF0000" }
    }
  ]
}
```

| `tipo` | Tokens | Notas |
|---|---|---|
| `"numero_pagina"` | `{n}`, `{total}` | Tokens de paginação resolvidos pelo renderer |
| `"texto_fixo"` | `{{versao_ndt}}`, `{ndf:caminho}`, `{n}`, `{total}` | Placeholders NDT, valores NDF e tokens de paginação |
| `"campo_ndf"` | — | Valor NDF escalar formatado; mesma semântica de `campos[]` sem `posicao` |
| `"marca_agua"` | — | Renderizada apenas quando o NDF está em estado `rascunho` |

**Interpolação de dados NDF em `mobilia`**: o campo `conteudo` de `texto_fixo` em `mobilia[]` aceita a sintaxe `{ndf:caminho.canonico}` para incorporar valores NDF escalares. Distinção de tokens no mesmo campo:

```json
{
  "tipo": "texto_fixo",
  "conteudo": "Proc. {ndf:cabecalho.referencia} — {ndf:cabecalho.entidade} — Pág. {n}/{total}",
  "posicao": { "x": 15, "y": 285 },
  "fonte": { "familia": "Helvetica", "tamanho": 8 }
}
```

**`tipo: "campo_ndf"`** para valores formatados (data, monetário, etc.) na mobília:

```json
{
  "tipo": "campo_ndf",
  "referencia": "cabecalho.data",
  "formato": "data",
  "posicao": { "x": 160, "y": 285 },
  "largura": 35,
  "altura": 5,
  "alinhamento": "direita",
  "fonte": { "familia": "Helvetica", "tamanho": 8 }
}
```

`campo_ndf` em `mobilia[]` aceita os mesmos campos de `campos[]` (§5.4) excepto `incluir_se` e `descontinuado`.

**Distinção de todos os tokens**: `{n}` e `{total}` são tokens de paginação resolvidos em runtime; `{{versao_ndt}}` e `{{schema_id}}` são placeholders NDT (metadados do template); `{ndf:caminho}` são referências a valores NDF (dados do documento). Os três coexistem num mesmo campo `conteudo`.

### 5.7 Sequenciamento (`sequencia[]`)

`paginas_def[]` descreve **modelos**. `sequencia[]` determina a ordem e o número de instâncias no documento final.

```json
{
  "sequencia": [
    {
      "pagina_def": "rosto",
      "repeticao": "unica"
    },
    {
      "pagina_def": "anexoG_pag_dados",
      "repeticao": "conforme_necessario",
      "fonte_overflow": "quadro4.imoveis",
      "linhas_por_pagina": 8,
      "incluir_se": "flags.incluir_anexoG"
    },
    {
      "pagina_def": "anexoG_pag_final",
      "repeticao": "unica",
      "incluir_se": "flags.incluir_anexoG"
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `pagina_def` | Sim | `id` da `pagina_def` a instanciar. |
| `repeticao` | Sim | Modo de repetição (ver tabela abaixo). |
| `fonte_overflow` | Cond. | Caminho NDF do array ou bloco a distribuir por páginas. Obrigatório para `"conforme_necessario"`. |
| `linhas_por_pagina` | Cond. | Itens por instância de página (para arrays). |
| `incluir_se` | Não | Caminho NDF de booleano; se `false` ou ausente, a entrada é omitida. Ver regra §5.4. |

**Modos de `repeticao`:**

| Modo | Comportamento |
|---|---|
| `"unica"` | Exactamente uma instância. |
| `"por_linha"` | Uma instância por item do array `fonte_overflow`. |
| `"conforme_necessario"` | Repete enquanto `fonte_overflow` tiver itens ou conteúdo NCRTF por colocar; cada instância recebe até `linhas_por_pagina` itens, ou o conteúdo que cabe na área disponível. |

**Exemplo — primeira página diferente:**

```json
{
  "sequencia": [
    { "pagina_def": "oficio_pag1", "repeticao": "unica" },
    { "pagina_def": "oficio_pag_seguinte", "repeticao": "conforme_necessario", "fonte_overflow": "conteudo.corpo" }
  ]
}
```

### 5.8 Tipografia

O objecto `fonte` é partilhado por `texto_fixo`, `campos[]`, `blocos[]` e `mobilia[]`. Quando omitido, herda de `estilos.fonte_padrao` (§3).

```json
{
  "fonte": {
    "familia": "Helvetica",
    "tamanho": 10,
    "peso": "normal",
    "estilo": "normal",
    "cor": "#000000"
  }
}
```

| Campo | Valores | Default |
|---|---|---|
| `familia` | Nome da fonte | Herda de `estilos.fonte_padrao` |
| `tamanho` | Pontos tipográficos | Herda de `estilos.fonte_padrao` |
| `peso` | `"normal"` \| `"bold"` | `"normal"` |
| `estilo` | `"normal"` \| `"italico"` | `"normal"` |
| `cor` | Hex `"#RRGGBB"` | Herda de `estilos.cor_texto` |

**Famílias base** (suportadas por qualquer renderer conforme): `"Helvetica"`, `"Times"`, `"Courier"`. Fontes adicionais são declaradas como recursos (§5.9).

#### Mapeamento NCRTF ↔ NDT

O NCRTF usa nomes canónicos independentes de implementação (famílias Liberation). O NDT usa nomes de fontes PDF. O renderer é responsável pela resolução, usando a seguinte tabela canónica:

| NCRTF `font_family` | NDT `familia` equivalente | Classe tipográfica |
|---|---|---|
| `"LiberationSans"` | `"Helvetica"` | Sem serifas |
| `"LiberationSerif"` | `"Times"` | Com serifas |
| `"LiberationMono"` | `"Courier"` | Monospace |

Quando um bloco NCRTF com `font_family: "LiberationSerif"` é renderizado numa `pagina_def` que declara `estilos.fonte_padrao.familia: "Times"`, o resultado é consistente — ambos referem a mesma família tipográfica através das suas denominações canónicas em cada spec.

Fontes declaradas em `recursos[]` (§5.9) com campo `familia` têm precedência sobre esta tabela para o mesmo nome canónico NCRTF, se o renderer suportar substituição.

### 5.9 Recursos (`recursos[]`)

Imagens e fontes referenciadas no layout. Um recurso pode ser **embebido** (template autossuficiente) ou **referenciado por hash** (infraestrutura controlada).

```json
{
  "recursos": [
    {
      "id": "logo-at.svg",
      "tipo": "svg",
      "modo": "embebido",
      "dados": "base64:PHN2ZyB4bWxucy4uLg=="
    },
    {
      "id": "brasao-republica.svg",
      "tipo": "svg",
      "modo": "referenciado_por_hash",
      "hash_sha256": "sha256:a1b2c3...",
      "content_type": "image/svg+xml"
    },
    {
      "id": "Arial",
      "tipo": "fonte_ttf",
      "familia": "Arial",
      "modo": "embebido",
      "dados": "base64:..."
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `id` | Sim | Identificador — referenciado em `referencia_recurso`. |
| `tipo` | Sim | `"svg"` \| `"png"` \| `"jpeg"` \| `"fonte_ttf"` \| `"fonte_otf"` |
| `modo` | Sim | `"embebido"` \| `"referenciado_por_hash"` |
| `dados` | Cond. | Base64 com prefixo `"base64:"`. Obrigatório quando `modo == "embebido"`. |
| `hash_sha256` | Cond. | SHA-256 com prefixo `"sha256:"`. Obrigatório quando `modo == "referenciado_por_hash"`. |
| `content_type` | Cond. | MIME type. Obrigatório quando `modo == "referenciado_por_hash"`. |
| `familia` | Cond. | Nome da família. Obrigatório para fontes. |

---

## 6. Composição de documentos (`composicao[]`)

Permite que um documento principal seja entregue com outros documentos independentes (impressos, certidões) como um único ficheiro — sem fundir as estruturas lógicas.

```json
{
  "composicao": [
    {
      "id": "anexo_modelo3_anexoG",
      "schema_id": "modelo3-irs-anexoG",
      "resolver": {
        "tipo": "referencia_documental",
        "template": "{{numero_processo}}/anexoG"
      },
      "posicao": "apos",
      "obrigatorio": true
    }
  ]
}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `id` | Sim | Identificador único. |
| `schema_id` | Sim | `schema_id` do NDT do documento a incorporar. |
| `resolver` | Sim | Como localizar o NDF concreto (ver §6.1). |
| `posicao` | Sim | `"antes"` \| `"apos"` \| `"apos_bloco"` |
| `apos_bloco` | Cond. | ID do bloco (quando `posicao == "apos_bloco"`). |
| `obrigatorio` | Não | Default `false`. Se `true`, falha de resolução bloqueia o fecho. |

### 6.1 Resolver

```json
{
  "resolver": {
    "tipo": "referencia_documental",
    "template": "{{numero_processo}}/anexoG"
  }
}
```

`template` é uma string com interpolações `{{caminho_ndf}}` resolvidas pelo core-documental com valores do NDF principal no momento do fecho. Não é uma expressão — não suporta operadores, funções, nem condicionais.

### 6.2 Regras

- Cada documento mantém o seu NDT/NDF próprios.
- No fecho do documento principal, o NDF de cada componente **tem de estar também fechado**.
- O NDF principal regista `schema_id`, `ndf_id`, `ndf_hash` e `pdf_hash` de cada componente, para verificação de integridade componente a componente.
- A `mobilia` do documento principal não se propaga aos documentos compostos.

---

## 7. NDF e NDT: referência e reprodutibilidade

O NDF referencia o NDT necessário para a sua renderização, mas não o incorpora.

```json
{
  "metadados": {
    "tipo_documento_ref": "modelo3-irs-anexoG",
    "ndt_version_ref": "modelo3-irs-anexoG@2026.1"
  }
}
```

Para documentos **fechados/assinados**, o NDF guarda adicionalmente o hash do NDT:

```json
{
  "ndt_hash": "sha256:a1b2c3..."
}
```

**Fluxo de renderização:**
1. O renderer recebe o NDF
2. Lê `ndt_version_ref` → busca o NDT no registry
3. Se o NDF está fechado: verifica `sha256(NDT) == ndt_hash`
4. Combina NDT + NDF → renderiza

---

## 8. Conformidade e migração

**Para renderers PDF:**
- Um renderer conforme não recusa renderizar por dados ausentes ou incorrectos — renderiza o que tem, deixa em branco o que falta.
- Respeita `min_linhas_visivel`, desenhando linhas em branco quando necessário.
- Respeita `incluir_se` ao nível de elemento e de sequência: ausência de caminho NDF ou valor não booleano trata-se como `true` (incluir).
- Implementa `assinatura` de acordo com o `modo` declarado (ver §8.1).
- Implementa `fluxo` e garante que os elementos após `corpo` aparecem na última página do overflow.
- O formato de saída alvo é **PDF/UA-2** (ISO 14289-2) — ver §8.2.

### 8.1 Modelo de assinatura CAdES ↔ PDF

A assinatura aposta ao documento NORMORDIS é **CAdES-B-LTA** (ETSI EN 319 122), guardada no NDF. PAdES (ETSI EN 319 132) é um perfil de CAdES para PDF — a infraestrutura criptográfica é a mesma; o objecto assinado difere.

**Workflow de fecho e assinatura:**

```
1. App de domínio → NDF completo (dados + metadados)
2. Renderer → gera PDF/UA-2 deterministicamente
3. pdf_hash = sha256(PDF gerado)
4. pdf_hash adicionado a NDF.outputs[].sha256
5. CAdES-B-LTA assina NDF canónico (que inclui pdf_hash)
6. CAdES guardado em NDF.signatures[]
```

**Workflow de verificação:**

```
1. Verificador lê NDF → valida CAdES (chain, timestamp, revogação)
2. Regenera PDF a partir de NDT + NDF
3. Confirma sha256(PDF regenerado) == NDF.outputs[].sha256
   → PDF autêntico: é a projecção determinística dos dados assinados
```

**Modelo híbrido (`modo: "hibrido"`, default):**

O mesmo CAdES do NDF é também usado para preencher o campo AcroForm PAdES no PDF. O contentor CAdES inclui `pdf_hash` como atributo assinado (`id-aa-ets-signerAttr` ou atributo proprietário NORMORDIS). O PDF resultante:

```
PDF/UA-2
├── conteúdo visual (acessível, tagged)
├── /Sig  ←  campo AcroForm PAdES
│   └── CAdES-B-LTA (mesmo cert; signed attribute: ndf_ref + pdf_hash)
└── /EmbeddedFiles (PDF/A-3)
    ├── source.ndf  ←  NDF completo com o seu CAdES
    └── ndf-signature.p7s  ←  contentor CAdES standalone
```

O PDF é **autossuficiente** para qualquer validador PDF/eIDAS (Adobe, DSS, EJBCA). O NDF embutido permite verificação completa da cadeia de dados. A assinatura cobre a fonte de verdade (NDF + `pdf_hash`), não apenas a projecção.

**Nota sobre dois objectos de assinatura**: tecnicamente, o PAdES embutido no PDF assina os bytes do PDF (ByteRange); o CAdES no NDF assina o JSON canónico do NDF. São instâncias distintas do mesmo algoritmo (CMS/CAdES), com o mesmo certificado, que se cross-referenciam via `pdf_hash` (no NDF) e `ndf_ref` (no atributo assinado do PAdES). Não é uma re-assinatura — o material criptográfico e o timestamp são os mesmos.

### 8.2 PDF/UA-2 como formato alvo

O renderer PDF conforme produz **PDF/UA-2** (ISO 14289-2, baseado em PDF 2.0 / ISO 32000-2). PDF/UA-2 incorpora os requisitos de acessibilidade universal — obrigação legal na Administração Pública portuguesa (DL n.º 83/2018, transposição da Directiva EU 2016/2102) e condição de conformidade eIDAS para documentos electrónicos acessíveis.

**Implicações para o renderer:**

| Requisito PDF/UA-2 | Implicação NDT/NDF |
|---|---|
| Estrutura lógica com tags (`/Document`, `/Sect`, `/P`, `/Table`, `/TH`, `/TD`, etc.) | O renderer infere tags a partir dos `blocos[]` e `fluxo.elementos`; tabelas NDT geram `/Table` com `/THead` e `/TBody` |
| Ordem de leitura (`/Order` na `StructTreeRoot`) | O renderer gera a ordem a partir da sequência lógica: `graficos[]` (decorativos → marcados `Artifact`), depois `campos[]` e `blocos[]` por ordem de leitura natural |
| Texto alternativo para imagens | `graficos[].imagem` e `graficos[].svg` aceitam campo `alt` (texto alternativo); obrigatório para conformidade UA |
| Idioma do documento | Derivado de `NDF.metadados.idioma` (ex.: `"pt-PT"`) |
| Fontes embebidas | Todas as fontes usadas devem estar em `recursos[]` ou ser fontes standard com `ToUnicode` |
| Campos de formulário com legenda | `assinatura`, `grelha_digitos` e `campos[]` com `formato: "checkbox"/"radio"` geram campos AcroForm com `/TU` (tooltip legível) |

**PDF/UA-2 e PDF/A-3 são compatíveis**: o mesmo ficheiro pode conformar com ambos simultaneamente — PDF/UA-2 para acessibilidade, PDF/A-3 para arquivo a longo prazo com attachments (necessário para o modelo híbrido §8.1).

Para o campo `alt` em elementos visuais:

```json
{
  "tipo": "imagem",
  "referencia_recurso": "brasao-republica.svg",
  "posicao": { "x": 15, "y": 10 },
  "largura": 25,
  "altura": 25,
  "alt": "Brasão da República Portuguesa"
}
```

Elementos puramente decorativos (linhas, rectângulos, fundos SVG) devem ser marcados `"alt": ""` — o renderer emite-os como `Artifact`, invisíveis para leitores de ecrã.

**Para renderers ODF (LibreOffice, Collabora, OnlyOffice, etc.):**
- O bloco `layout` é opcional — pode ser ignorado.
- `estilos` é a fonte principal; o renderer mapeia `fonte_padrao` → estilo `Default Paragraph Style`; `cabecalhos[]` → estilos `Heading 1`–`Heading N`; `cor_primaria` → cor de parágrafo de destaque.
- Elementos sem equivalente ODF (`grelha_digitos`, `tabela_visual`, `min_linhas_visivel`) podem ser omitidos ou aproximados (ex.: `grelha_digitos` → campo de texto com comprimento máximo; tabela com `min_linhas_visivel` → tabela com o número de linhas do NDF sem linhas em branco adicionais).
- `assinatura` pode ser renderizada como linha de assinatura ODF com campo de formulário (`com.sun.star.text.TextField.Input`) e legenda.
- A fidelidade de conteúdo (NCRTF) é normativa; a fidelidade de layout é best-effort.
- O output ODF destina-se a intercâmbio e edição — não a arquivo. Para arquivo, usar PDF/A.

**Para renderers HTML:**
- O bloco `layout` é ignorado.
- `estilos` mapeia para variáveis CSS (`--font-family`, `--color-primary`, `--color-text`, `--spacing-paragraph`).
- `assinatura` é renderizada como `<div class="signature-field" data-id="{{id}}">` para captura por JavaScript.
- A fidelidade de conteúdo (NCRTF) é normativa; paginação e posicionamento são CSS flow.

**Estabilidade de caminhos:**
- Os `id` de campos, colunas de tabelas e `paginas_def` não são renomeados entre versões de `versao_ndt`.
- Campos e colunas removidos são marcados `"descontinuado": true`, não eliminados.

---

## 9. Glossário

| Termo | Significado |
|---|---|
| NDT | NORMORDIS Document Template — formato declarativo de layout (este documento) |
| NDF | NORMORDIS Document Format — instância de dados materializados (spec NDF v1.0.0) |
| Renderer | Executor puro que combina NDT + NDF → documento. Não aplica regras de negócio. |
| `schema_id` | Identificador estável do tipo de documento; corresponde a `tipo_documento_ref` no NDF |
| `versao_ndt` | Versão desta instância do template; parte de `ndt_version_ref` no NDF |
| `ndt_hash` | SHA-256 do NDT no momento do fecho do NDF — garante reprodutibilidade bit-perfeita |
| `estilos` | Bloco de estilos globais do documento; fonte principal para renderers ODF/HTML |
| `pagina_def` | Modelo de página instanciado por `sequencia[]` |
| `grafico` | Elemento visual puro de uma `pagina_def`, a coordenadas absolutas |
| `grelha_digitos` | Primitiva de caixas por carácter, ligada a um caminho NDF |
| `assinatura` | Campo de assinatura electrónica/manuscrita; AcroForm PAdES em PDF; modos: `visual_apenas`, `hibrido` (default), `ndf_attachment` |
| CAdES | CMS Advanced Electronic Signatures (ETSI EN 319 122); algoritmo de assinatura usado pelo NDF (`CAdES-B-LTA`) |
| PAdES | PDF Advanced Electronic Signatures (ETSI EN 319 132); perfil de CAdES para PDF; usado no campo AcroForm do modo `hibrido` |
| PDF/UA-2 | ISO 14289-2 — perfil de acessibilidade universal para PDF 2.0; formato alvo do renderer normordis-pdf |
| PDF/A-3 | ISO 19005-3 — perfil de arquivo a longo prazo com suporte a attachments; compatível com PDF/UA-2 |
| `pdf_hash` | SHA-256 do PDF gerado, incluído no NDF antes de assinar; permite verificação determinística sem nova assinatura |
| `alt` | Texto alternativo em elementos visuais (`imagem`, `svg`); obrigatório para conformidade PDF/UA-2 |
| `rotulo_acessivel` | Tooltip acessível em campos interactivos (`campos[]`, `grelha_digitos`); emitido como `/TU` no AcroForm para PDF/UA-2 |
| `linha_lateral` | Elemento de `fluxo.elementos` que agrupa elementos lado a lado; resolve duplos blocos de assinatura e disposições colunares em documentos de fluxo |
| `campo_ndf` | Tipo de elemento em `mobilia[]` — valor NDF escalar formatado no cabeçalho/rodapé de página |
| `{ndf:caminho}` | Sintaxe de interpolação de dados NDF em `texto_fixo` de `mobilia[]`; distinto de `{{placeholder_ndt}}` e de `{n}/{total}` |
| `quebra_pagina` | Elemento de `fluxo.elementos` que força início de nova página na `sequencia[]` |
| `tabela` (bloco) | Array NDF renderizado como tabela de linhas e colunas com layout definido no NDT |
| `min_linhas_visivel` | Número mínimo de linhas a renderizar; o renderer completa com linhas em branco |
| `fluxo` | Região de layout vertical sequencial numa `pagina_def`; para documentos com corpo de extensão variável |
| `corpo` | Bloco de texto NCRTF com fluxo, referenciado por caminho NDF |
| `mobilia` | Elementos fixos de página: numeração, marca de água, texto de rodapé |
| `sequencia` | Ordenação e modos de repetição das `paginas_def` no documento final |
| `incluir_se` | Referência directa a booleano NDF; controla a inclusão condicional de elementos e secções |
| `recurso` | Imagem ou fonte referenciada no layout: embebida no NDT ou por hash |
| `composicao` | Mecanismo de entrega conjunta de documentos independentes num único ficheiro |
| Caminho canónico | Referência a um dado NDF por percurso hierárquico de identificadores |
| Formato de display | Hint de renderização visual (monetario, data, checkbox, etc.) sem semântica de validação |
| Token de paginação | `{n}`, `{total}` — resolvidos pelo renderer; distintos de placeholders NDT e caminhos NDF |
| Placeholder NDT | `{{versao_ndt}}`, `{{schema_id}}` — metadados do próprio NDT, em `texto_fixo` |
| Fidelidade normativa | Garantia de output bit-idêntico para o mesmo NDT+NDF; aplica-se a PDF/A |
| Fidelidade best-effort | Conteúdo fiel; layout adaptado às convenções do formato; aplica-se a ODF e HTML |
| ODF | OpenDocument Format — ISO/IEC 26300; formato secundário para intercâmbio e edição |
