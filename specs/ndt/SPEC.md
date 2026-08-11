# Especificação NDT v2.0.0

**NORMORDIS Document Template — Especificação Formal**

Estado: Draft — revisão pública por abrir
Âmbito: formato declarativo de layout para descrever a composição visual de qualquer documento institucional — desde impressos fiscais complexos (ex.: Modelo 3 IRS) a documentos administrativos correntes (ofícios, informações, despachos).

Objetivo de interoperabilidade: permitir que renderizadores independentes
interpretem o mesmo template e produzam saídas equivalentes segundo um perfil
de conformidade, sem dependência do sistema que criou o NDT.

Convenções editoriais: aplica-se
[`docs/normalization/EDITORIAL-POLICY.md`](../../docs/normalization/EDITORIAL-POLICY.md).
A língua normativa é o português europeu. As palavras **DEVE**, **NÃO DEVE**,
**RECOMENDA-SE**, **NÃO SE RECOMENDA** e **PODE** seguem o BCP 14 (RFC 2119 e
RFC 8174) quando aparecem em maiúsculas. Formas em minúsculas são narrativas.
As referências comuns encontram-se em
[`docs/normalization/NORMATIVE-REFERENCES.md`](../../docs/normalization/NORMATIVE-REFERENCES.md).

## Licenciamento

Esta especificação (texto, estrutura, JSON Schemas e exemplos associados) é disponibilizada sob **CC0 1.0** (domínio público). O objetivo é que qualquer produtor de software para a Administração Pública — código aberto ou proprietário — possa implementar leitura e renderização de NDT livremente, sem qualquer obrigação contratual ou de licenciamento para com o autor da especificação.

A **implementação de referência** (`normordis-pdf`, bibliotecas Rust) é distribuída sob licença separada (EUPL v1.2), indicada no respetivo repositório. Esta especificação é licenciada separadamente (`LICENSE-SPEC`) precisamente para que a adoção do formato não dependa da licença do código.

---

## Referências normativas

Aplicam-se BCP 14, JSON Schema Draft 2020-12 e, quando invocados por um perfil
de saída, os documentos identificados no
[registo de referências](../../docs/normalization/NORMATIVE-REFERENCES.md).
NDF 1.x e NCRTF 2.x são dependências normativas versionadas para resolução de
dados e conteúdo. Referências PDF/A, PDF/UA, ODF, CAdES e PAdES só são
normativas para o perfil que expressamente as declare.

## Termos e definições

Aplicam-se os termos da
[base terminológica comum](../../docs/normalization/TERMINOLOGY.md). Termos NDT
específicos são definidos na cláusula em que são introduzidos. O Anexo A reúne
um glossário informativo.

## 1. Objetivo, âmbito e papel do NDT

**NDF + NDT + renderizador = representação visual do documento.**

- **NDT** (este formato) — descreve *como* o documento é composto visualmente: estrutura de páginas, posições, elementos gráficos, tipografia, tabelas de dados, mobília.
- **NDF** (especificação NDF v1.0.0) — fornece *o quê*: os dados a apresentar, já computados e materializados pela aplicação de domínio.
- **Renderizador** (qualquer implementação conforme) — combina NDT + NDF para
  produzir o documento. Verifica a conformidade estrutural necessária à
  renderização, mas não aplica validações nem regras do domínio.

**Implicações directas:**

1. O NDT não contém regras de validação do domínio, fórmulas de cálculo,
   obrigatoriedade material de campos nem lógica de negócio. Essas regras são
   responsabilidade da aplicação que produz o NDF.
2. O renderizador verifica versões, referências, integridade e estrutura
   necessárias para interpretar NDF e NDT. Não decide se um dado satisfaz uma
   regra jurídica ou de negócio.
3. O mesmo NDT + NDF produz uma representação semanticamente equivalente. A
   a identidade byte a byte é exigível apenas por um perfil de renderizador que
   fixe motor, fontes, recursos, versões e parâmetros de serialização.

### 1.1 Referência NDF ↔ NDT

O NDF-core referencia o NDT mas não o incorpora. No perfil de custódia, o NDT
**PODE** ser deduplicado por hash. O `.ndfpkg` portátil DEVE incorporar a versão
exata do NDT, os schemas e os recursos necessários à renderização.

| NDF-core | NDT | Significado |
|---|---|---|
| `metadados.tipo_documento_ref` | `schema_id` | Identifica o tipo de documento |
| `ndt_version_ref` | `schema_id@versao_ndt` | Identifica a versão concreta do template |

O hash do ficheiro NDT é registado no inventário do `.ndfpkg`. Não existe um
campo `ndt_hash` no NDF-core v1.0.0.

Todos os caminhos de dados declarados pelo NDT são relativos a
`NDF-core.documento`. Por exemplo, `corpo` resolve para
`NDF-core.documento.corpo`. Valores do envelope usam tokens reservados
explicitamente definidos, como `{{validation_code}}`.

### 1.2 Duas fases de uso do NDT

| Fase | Estado NDF | Papel do NDT |
|---|---|---|
| **Apresentação de formulário** | `rascunho` | A aplicação de domínio usa o NDT para saber que campos existem e como estruturar a UI de preenchimento. O NDF está incompleto. |
| **Renderização** | qualquer | O NDT é o único guia visual. O NDF fornece os dados. O renderizador segue o NDT à risca. |

Após o fecho do NDF, o NDT é irrelevante para qualquer operação sobre o conteúdo — é relevante apenas para re-renderização.

### 1.3 Fidelidade por formato de saída

O NDT define um layout prescritivo para PDF/impressão. Para outros formatos, o contrato é diferente — o conteúdo é fiel; o layout é adaptado às convenções de cada formato.

| Formato | Momento no ciclo de vida | Fidelidade de layout | Fidelidade de conteúdo | Fonte de layout |
|---|---|---|---|---|
| **PDF / PDF/A** | Arquivo, prova, entrega formal | **Normativa segundo o perfil de renderizador** | Total | Bloco `layout` do NDT (§5) |
| **ODF** | Intercâmbio, edição, revisão | Best-effort — renderizador usa `estilos` NDT (§3) | Total | Bloco `estilos` do NDT (§3) |
| **HTML** | Publicação, intranet, consulta | Best-effort — layout é CSS flow | Total | Bloco `estilos` do NDT (§3) |
| **Typst** | Composição tipográfica avançada | Alta — mm coords são dicas; renderizador adapta | Total | Bloco `layout` do NDT (§5) |
| **Outros** | Não especificado | Não especificado | Via NCRTF no NDF | — |

**Fidelidade de conteúdo** significa que o texto, tabelas, listas, imagens e estrutura semântica do documento são preservados identicamente. **Fidelidade de layout** significa que posições, fontes, margens e paginação são reproduzidas com exactidão.

**PDF/A e ODF servem momentos distintos** — não são equivalentes. PDF/A é uma
representação fixa preservável e verificável por hash. ODF é um formato
de intercâmbio e trabalho editável. Ambos são projeções da mesma fonte de
verdade; a identidade binária de um PDF só é garantida por um perfil de
renderizador que fixe todo o ambiente de produção.

**ODF como formato secundário** alinha-se com os princípios de soberania digital da especificação NDF e com o RNID (Regulamento Nacional de Interoperabilidade Digital). Para a Administração Pública portuguesa, ODF é o formato de intercâmbio recomendado para documentos editáveis.

Para ODF e HTML, o renderizador **PODE** ignorar o bloco `layout` do NDT; o
bloco `estilos` (§3) é a fonte de verdade para estilo. Um renderizador ODF
conforme produz conteúdo semanticamente fiel, não uma cópia pixel a pixel do
PDF.

**Elementos sem equivalente em formatos de fluxo**: `grelha_digitos`, `tabela_visual`, `rectangulo`, `linha`, `min_linhas_visivel` e `assinatura` (como AcroForm PDF) não têm equivalente direto em ODF/HTML. Renderizadores de fluxo PODEM ignorá-los ou usar aproximações (ex.: `grelha_digitos` → campo de texto ODF; `assinatura` → linha de assinatura ODF com macro de captura).

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

O bloco `estilos` declara os valores por defeito de tipografia e espaçamento para o documento inteiro. É a **fonte principal de estilo para renderizadores de fluxo** (ODF, HTML) e serve como alternativa para renderizadores PDF onde elementos não declarem fonte própria.

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

Um renderizador ODF mapeia `estilos` para estilos de parágrafo nativos (`Default Paragraph Style`, `Heading 1`, etc.). Um renderizador HTML mapeia para variáveis CSS (`--font-primary`, `--color-text`, etc.). Um renderizador PDF usa `fonte_padrao` como alternativa onde nenhum elemento declara fonte própria.

---

## 4. Endereçamento de dados NDF

O NDT referencia valores do NDF através de **caminhos canónicos** — strings que identificam um valor pelo seu percurso hierárquico de identificadores. O NDF armazena valores nessas mesmas posições.

A hierarquia é uma **convenção de endereçamento**, não um schema. O NDT não valida se o caminho existe no NDF nem o tipo do valor — o renderizador escreve o que encontrar, ou deixa em branco se o caminho não existir.

A sintaxe canónica é uma sequência de segmentos separados por `.`, em que cada
segmento cumpre `[A-Za-z_][A-Za-z0-9_-]*`. A raiz implícita é sempre
`NDF-core.documento`; os prefixos `documento.` e `NDF-core.` NÃO DEVEM aparecer
no NDT. Tokens de envelope, como `{{validation_code}}`, pertencem a um espaço
reservado separado.

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

O NDT não precisa de conhecer o comprimento do array — o renderizador itera sobre os itens presentes no NDF.

### 4.3 Formatos de display

O NDT **PODE** declarar um **formato de apresentação** para orientar o
renderizador. Não é um tipo de dados com validação; é uma indicação visual.

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

Formatos numéricos aceitam o parâmetro opcional `"casas_decimais"` (inteiro). Predefinição: `2` para `"monetario"`, `0` para `"inteiro"`, variável para `"numero"`.

---

## 5. Layout (PDF e impressão)

O bloco `layout` descreve a composição visual prescritiva do documento para PDF e impressão. É **normativo para renderizadores PDF**; renderizadores de fluxo (ODF, HTML) PODEM ignorá-lo em favor de `estilos` (§3).

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

O objeto `fluxo` declara uma **região de fluxo vertical** dentro da `pagina_def`: os seus elementos empilham-se de cima para baixo a partir de `y_inicio`, ocupando a altura que o conteúdo requerer.

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
      { "tipo": "corpo", "referencia": "corpo" },
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

**Comportamento de extravasamento do `corpo` dentro do `fluxo`**: quando o conteúdo NCRTF de um elemento `tipo: "corpo"` não cabe na área disponível (entre `y_inicio` e o limite inferior da área útil), o extravasamento é gerido por `sequencia[]` (§5.7) da mesma forma que um `bloco corpo` absoluto. Os elementos de `fluxo.elementos` que aparecem **depois** do `corpo` são renderizados na **última página** da sequência de extravasamento, imediatamente após o fim do corpo. Os elementos **antes** do `corpo` são renderizados apenas na primeira instância da `pagina_def`.

**Elementos suportados em `fluxo.elementos`:**

| `tipo` | Descrição |
|---|---|
| `corpo` | Bloco de texto NCRTF com fluxo (`referencia` = caminho NDF). Único por `fluxo`; o extravasamento propaga-se pela `sequencia[]`. |
| `tabela` | Tabela de dados NDF (mesma estrutura de `blocos[]` tipo tabela, §5.5.1). Sem `posicao` — posicionada automaticamente. |
| `texto_fixo` | Texto estático ou com placeholders NDT (`{{versao_ndt}}`). Faz wrapping automático na largura disponível. |
| `campo` | Valor NDF escalar (mesma semântica de `campos[]`, §5.4, sem `posicao`). |
| `imagem` | Imagem a partir de um recurso (§5.9). Campos: `referencia_recurso`, `largura`, `altura`, `manter_proporcao`, `alinhamento`, `alt`. |
| `espaco` | Espaço vertical explícito. Campos: `altura` (mm). |
| `separador` | Linha horizontal. Campos: `espessura` (mm, default 0.3), `cor` (hex). |
| `assinatura` | Campo de assinatura (§5.3.6). Sem `posicao` — posicionado em fluxo. |
| `linha_lateral` | Agrupa dois ou mais elementos lado a lado numa mesma linha horizontal. Ver §5.2.2. |
| `quebra_pagina` | Força início de nova página. O renderizador termina a instância actual da `pagina_def` e avança para a seguinte entrada em `sequencia[]`. Sem campos adicionais. |

Todos os elementos de `fluxo.elementos` aceitam `"incluir_se"` (ver §5.4) para renderização condicional.

`fluxo` e `blocos[]` são **mutuamente exclusivos** na mesma `pagina_def`: uma página usa um dos dois modelos para o conteúdo principal. `graficos[]`, `campos[]` e `mobilia[]` coexistem com qualquer modelo.

#### 5.2.2 Layout lateral em fluxo (`linha_lateral`)

Agrupa elementos de `fluxo` lado a lado numa mesma linha horizontal. É usado
para blocos de dupla assinatura, datas com referências ou outros elementos que
partilham a largura disponível.

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
| `elementos[].largura` | Sim | Largura da coluna (mm). A soma das larguras NÃO DEVE exceder a largura útil da `pagina_def`. |
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
- **Valores de envelope** (resolvidos pelo renderizador a partir do envelope NDF no momento da renderização): `{{validation_code}}`

`{{validation_code}}` é o código de verificação canónico do NDF (ver NDF especificação §4.6). Não é um dado do NDF-core nem um metadado do NDT — é computado durante a finalização e fornecido ao renderizador pelo envelope. Deve ser usado no elemento `codigo_barras` e/ou em `texto_fixo` de mobília para emissão de documentos para o exterior.

#### 5.3.6 `assinatura`

Campo de assinatura eletrónica ou manuscrita. O campo `modo` controla a relação entre a assinatura CAdES guardada no NDF e o PDF gerado — ver §8.1 para o modelo completo de assinatura.

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
| `modo` | Não | Modo de integração CAdES↔PDF. Predefinição: `"hibrido"`. Ver §8.1. |

**Valores de `modo`:**

| Valor | Comportamento no PDF gerado |
|---|---|
| `"visual_apenas"` | Placeholder visual sem campo AcroForm. A assinatura ou selo, se existente, vive no envelope NDF. |
| `"hibrido"` | **(Predefinido)** Cria campo AcroForm que suporta uma operação PAdES independente. O `.ndfpkg` **PODE** também ser incorporado como anexo PDF/A. |
| `"ndf_attachment"` | Sem AcroForm. O CAdES do NDF é embutido comoanexo PDF/A-3 (`ndf-signature.p7s`). Útil quando o validador de destino suporta PDF/A-3 mas não requer AcroForm. |

Em ODF, `assinatura` é renderizada como linha de assinatura com campo de formulário (`com.sun.star.text.TextField.Input`) e legenda. Em HTML, como `<div class="signature-field" data-id="{{id}}">`. O `modo` é ignorado em formatos de fluxo — aplica-se apenas ao renderizador PDF.

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
`referencia`: caminho NDF com o valor a codificar. Para conteúdo composto, usar `"conteudo"` (string com interpolações `{{caminho_ndf}}`). Para o código de validação do documento, usar `{{validation_code}}` (resolvido pelo renderizador a partir do envelope NDF):

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

`colunas`: array de larguras (mm); a soma DEVE igualar `largura`.

#### 5.3.12 Sumário de tipos gráficos

| `tipo` | Liga ao NDF? | Uso típico |
|---|---|---|
| `linha` | Não | Separadores, bordas |
| `rectangulo` | Não | Caixas de secção, molduras |
| `grelha_digitos` | Sim — valor do campo | NIFs, datas, códigos em caixas |
| `imagem` | Não | Logótipos, brasões |
| `texto_fixo` | Não (placeholders NDT) | Títulos, legendas do impresso |
| `assinatura` | Não (registada no NDF) | Campo de assinatura eletrónica/manuscrita |
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
| `formato` | Não | Formato de apresentação (§4.3). Predefinição: `"texto"`. |
| `casas_decimais` | Não | Para `"monetario"` e `"numero"`. |
| `fonte` | Não | Ver §5.8. Herda de `estilos.fonte_padrao` se omitido. |
| `alinhamento` | Não | `"esquerda"` \| `"centro"` \| `"direita"`. Predefinição: `"esquerda"`. |
| `preenchimento_fundo` | Não | `"none"` ou cor hex. |
| `rotulo_acessivel` | Não | Texto legível por leitores de ecrã (PDF/UA-2 `/TU`). Obrigatório para campos interativos (`"checkbox"`, `"radio"`). Se omitido em campos de texto, o renderizador usa o valor de `referencia` como alternativa. |
| `incluir_se` | Não | Caminho NDF de booleano. Se `false` ou ausente, o elemento é omitido. Ver regra abaixo. |
| `descontinuado` | Não | Default `false`. Ver §8. |

**Regra `incluir_se`**: aceita apenas um caminho NDF direto para um campo booleano. Não é uma expressão — não suporta operadores nem funções. Se o caminho não existir ou o valor não for booleano, o renderizador inclui o elemento. Aplica-se a `campos[]`, a `blocos[]` e a `fluxo.elementos`.

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
| `min_linhas_visivel` | Não | Número mínimo de linhas a renderizar. Predefinição: `0`. |
| `repete_cabecalho` | Não | Se `true`, cabeçalho repete no topo de cada página quando a tabela transborda. |
| `incluir_se` | Não | Caminho NDF de booleano (ver §5.4). |
| `colunas[].id` | Sim | Propriedade do item NDF para esta coluna. |
| `colunas[].cabecalho` | Não | Texto do cabeçalho da coluna. |
| `colunas[].largura` | Sim | Largura da coluna (mm). |
| `colunas[].alinhamento` | Não | `"esquerda"` \| `"centro"` \| `"direita"`. |
| `colunas[].formato` | Não | Formato de apresentação (§4.3). Predefinição: `"texto"`. |
| `colunas[].descontinuado` | Não | Default `false`. Ver §8. |

**Regra `min_linhas_visivel`**: o renderizador DEVE sempre desenhar a estrutura da tabela (frame, cabeçalho, linhas) e preencher com os itens do NDF. Se o NDF tiver menos itens do que `min_linhas_visivel`, o renderizador completa com linhas em branco. Esta regra garante que impressos fiscais apresentam as linhas oficiais mesmo sem dados.

#### 5.5.2 `corpo`

Bloco de texto com fluxo em formato NCRTF, a coordenadas absolutas. Para documentos administrativos com fórmulas de encerramento e assinatura após o corpo, usar o modelo `fluxo` (§5.2.1) em vez de `corpo` em `blocos[]`.

```json
{
  "tipo": "corpo",
  "referencia": "corpo",
  "posicao": { "x": 15, "y": 60 },
  "largura": 180,
  "fonte_base": { "familia": "Times", "tamanho": 11 },
  "incluir_se": null
}
```

O renderizador renderiza o NCRTF do caminho NDF referenciado a partir de `posicao`, até ao limite inferior da área útil. Overflow gerido por `sequencia[]` (§5.7).

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

Elementos fixos de cada `pagina_def`. Cada `pagina_def` tem a sua própria
`mobilia`, permitindo numerações e marcas de água distintas.

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
| `"numero_pagina"` | `{n}`, `{total}` | Tokens de paginação resolvidos pelo renderizador |
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
    { "pagina_def": "oficio_pag_seguinte", "repeticao": "conforme_necessario", "fonte_overflow": "corpo" }
  ]
}
```

### 5.8 Tipografia

O objeto `fonte` é partilhado por `texto_fixo`, `campos[]`, `blocos[]` e `mobilia[]`. Quando omitido, herda de `estilos.fonte_padrao` (§3).

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

| Campo | Valores | Predefinição |
|---|---|---|
| `familia` | Nome da fonte | Herda de `estilos.fonte_padrao` |
| `tamanho` | Pontos tipográficos | Herda de `estilos.fonte_padrao` |
| `peso` | `"normal"` \| `"bold"` | `"normal"` |
| `estilo` | `"normal"` \| `"italico"` | `"normal"` |
| `cor` | Hex `"#RRGGBB"` | Herda de `estilos.cor_texto` |

**Famílias base** (suportadas por qualquer renderizador conforme): `"Helvetica"`, `"Times"`, `"Courier"`. Fontes adicionais são declaradas como recursos (§5.9).

#### Mapeamento NCRTF ↔ NDT

O NCRTF usa nomes canónicos independentes de implementação (famílias Liberation). O NDT usa nomes de fontes PDF. O renderizador é responsável pela resolução, usando a seguinte tabela canónica:

| NCRTF `font_family` | NDT `familia` equivalente | Classe tipográfica |
|---|---|---|
| `"LiberationSans"` | `"Helvetica"` | Sem serifas |
| `"LiberationSerif"` | `"Times"` | Com serifas |
| `"LiberationMono"` | `"Courier"` | Monospace |

Quando um bloco NCRTF com `font_family: "LiberationSerif"` é renderizado numa `pagina_def` que declara `estilos.fonte_padrao.familia: "Times"`, o resultado é consistente — ambos referem a mesma família tipográfica através das suas denominações canónicas em cada especificação.

Fontes declaradas em `recursos[]` (§5.9) com campo `familia` têm precedência sobre esta tabela para o mesmo nome canónico NCRTF, se o renderizador suportar substituição.

### 5.9 Recursos (`recursos[]`)

Imagens e fontes referenciadas no layout. Um recurso usa um dos modos
**embebido** ou **referenciado por hash**.

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
- Quando o schema do tipo de documento principal suportar composição, o registo de `schema_id`, `ndf_id`, `ndf_hash` e `pdf_hash` de cada componente pertence ao respetivo bloco em `documento`. Estes valores não são campos universais implícitos do NDF-core.
- A `mobilia` do documento principal não se propaga aos documentos compostos.

---

## 7. NDF e NDT: referência e reprodutibilidade

O NDF-core contém `ndt_version_ref` no topo:

```json
{
  "ndt_version_ref": "modelo3-irs-anexoG@2026.1",
  "metadados": {
    "tipo_documento_ref": "modelo3-irs@2026.1"
  }
}
```

**Fluxo de renderização:**

1. O renderizador verifica a conformidade estrutural do NDF e lê `ndt_version_ref`.
2. Resolve o NDT no `.ndfpkg` ou no domínio de custódia.
3. Verifica o hash do NDT contra o manifesto ou catálogo imutável.
4. Confirma `schema_id@versao_ndt == ndt_version_ref`.
5. Resolve caminhos NDT relativamente a `NDF-core.documento`.
6. Combina NDT + NDF e produz o formato de saída pedido.

Sem o NDT exato, os dados continuam legíveis, mas a renderização NÃO DEVE ser
declarada reprodutível. Reprodutibilidade visual não implica identidade binária;
esta última exige um perfil de renderizador adicional.

---

## 8. Conformidade e migração

Os requisitos por papel encontram-se em
[`RENDERER-CONFORMANCE.md`](RENDERER-CONFORMANCE.md), com identificadores
`NDT-RENDER-*`. Esta cláusula descreve a articulação dos perfis e não duplica a
declaração de conformidade.

### 8.1 Assinatura do NDF e assinatura de representações

O NDF e as suas representações são objetos distintos:

- CAdES no envelope NDF assina os `payload_bytes` canónicos;
- uma assinatura PAdES, quando produzida, assina os bytes do PDF através do seu
  `ByteRange`;
- as duas assinaturas **PODEM** usar o mesmo certificado, mas são operações,
  valores criptográficos e timestamps distintos.

CAdES NÃO é obrigatório quando `nivel_assinatura` é `"nenhuma"`. Todo o NDF
continua sujeito a JCS, hash, custódia append-only/WORM e auditoria. Um selo
institucional CAdES **PODE** ser acrescentado para tornar a prova de origem
portátil, sem representar assinatura pessoal.

Um renderizador PODE produzir PDF sem PAdES, PDF com PAdES, ou PDF/A com o
`.ndfpkg` embebido. A ausência de PAdES não altera a validade estrutural do NDF.
Se houver referências cruzadas entre NDF e PDF, estas pertencem a um perfil de
saída versionado; não são campos implícitos `saídas[]` ou `signatures[]` do
NDF-core v1.0.0.

### 8.2 PDF/UA-2 como formato alvo

O perfil PDF acessível tem como alvo **PDF/UA-2** (ISO 14289-2, baseado em PDF
2.0 / ISO 32000-2). Este perfil apoia requisitos de acessibilidade aplicáveis à
Administração Pública, mas a conformidade legal depende do serviço, conteúdo e
contexto concretos e requer avaliação própria.

**Implicações para o renderizador:**

| Requisito PDF/UA-2 | Implicação NDT/NDF |
|---|---|
| Estrutura lógica com tags (`/Document`, `/Sect`, `/P`, `/Table`, `/TH`, `/TD`, etc.) | O renderizador infere tags a partir dos `blocos[]` e `fluxo.elementos`; tabelas NDT geram `/Table` com `/THead` e `/TBody` |
| Ordem de leitura (`/Order` na `StructTreeRoot`) | O renderizador gera a ordem a partir da sequência lógica: `graficos[]` (decorativos → marcados `Artifact`), depois `campos[]` e `blocos[]` por ordem de leitura natural |
| Texto alternativo para imagens | `graficos[].imagem` e `graficos[].svg` aceitam campo `alt` (texto alternativo); obrigatório para conformidade UA |
| Idioma do documento | Derivado de `NDF.metadados.idioma` (ex.: `"pt"`, conforme ISO 639-1 no NDF v1.0.0) |
| Fontes embebidas | Todas as fontes usadas DEVEM estar em `recursos[]` ou ser fontes standard com `ToUnicode` |
| Campos de formulário com legenda | `assinatura`, `grelha_digitos` e `campos[]` com `formato: "checkbox"/"radio"` geram campos AcroForm com `/TU` (tooltip legível) |

**PDF/UA-2 e PDF/A-3 são compatíveis**: um mesmo ficheiro admite conformidade
simultânea, sujeita à validação independente de cada perfil.

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

Elementos puramente decorativos (linhas, retângulos, fundos SVG) DEVEM ser marcados `"alt": ""` — o renderizador emite-os como `Artifact`, invisíveis para leitores de ecrã.

**Para renderizadores ODF (LibreOffice, Collabora, OnlyOffice, etc.):**
- O renderizador ODF **PODE** ignorar o bloco `layout`.
- `estilos` é a fonte principal; o renderizador mapeia `fonte_padrao` → estilo `Default Paragraph Style`; `cabecalhos[]` → estilos `Heading 1`–`Heading N`; `cor_primaria` → cor de parágrafo de destaque.
- O renderizador ODF **PODE** omitir ou aproximar elementos sem equivalente ODF (`grelha_digitos`, `tabela_visual`, `min_linhas_visivel`), mas **DEVE** declarar essas aproximações no relatório de renderização.
- O renderizador ODF **PODE** representar `assinatura` como linha de assinatura com campo de formulário (`com.sun.star.text.TextField.Input`) e legenda.
- A fidelidade de conteúdo (NCRTF) é normativa; a fidelidade de layout é melhor esforço.
- A saída ODF destina-se a intercâmbio e edição — não a arquivo. Para arquivo, usar PDF/A.

**Para renderizadores HTML:**
- O bloco `layout` é ignorado.
- `estilos` mapeia para variáveis CSS (`--font-family`, `--color-primary`, `--color-text`, `--spacing-paragraph`).
- `assinatura` é renderizada como `<div class="signature-field" data-id="{{id}}">` para captura por JavaScript.
- A fidelidade de conteúdo (NCRTF) é normativa; paginação e posicionamento são CSS flow.

**Estabilidade de caminhos:**
- Os `id` de campos, colunas de tabelas e `paginas_def` não são renomeados entre versões de `versao_ndt`.
- Campos e colunas removidos são marcados `"descontinuado": true`, não eliminados.

---

## Anexo A (informativo) — Glossário

| Termo | Significado |
|---|---|
| NDT | NORMORDIS Document Template — formato declarativo de layout (este documento) |
| NDF | NORMORDIS Document Format — instância de dados materializados (especificação NDF v1.0.0) |
| Renderizador | Executor que combina NDT + NDF e produz uma representação. Verifica estrutura e referências, mas não aplica regras do domínio. |
| `schema_id` | Identificador estável do tipo de documento; corresponde a `tipo_documento_ref` no NDF |
| `versao_ndt` | Versão desta instância do template; parte de `ndt_version_ref` no NDF |
| Hash do NDT | SHA-256 do ficheiro NDT registado no manifesto ou catálogo de custódia; não é campo do NDF-core |
| `estilos` | Bloco de estilos globais do documento; fonte principal para renderizadores ODF/HTML |
| `pagina_def` | Modelo de página instanciado por `sequencia[]` |
| `grafico` | Elemento visual puro de uma `pagina_def`, a coordenadas absolutas |
| `grelha_digitos` | Primitiva de caixas por carácter, ligada a um caminho NDF |
| `assinatura` | Campo de assinatura eletrónica/manuscrita; AcroForm PAdES em PDF; modos: `visual_apenas`, `hibrido` (default), `ndf_attachment` |
| CAdES | CMS Advanced Electronic Signatures (ETSI EN 319 122); algoritmo de assinatura usado pelo NDF (`CAdES-B-LTA`) |
| PAdES | PDF Advanced Electronic Signatures (ETSI EN 319 142-1); assinatura opcional e independente da assinatura CAdES do NDF |
| PDF/UA-2 | ISO 14289-2 — perfil de acessibilidade universal para PDF 2.0; formato alvo do renderizador normordis-pdf |
| PDF/A-3 | ISO 19005-3 — perfil de arquivo a longo prazo com suporte a anexos; compatível com PDF/UA-2 |
| `pdf_hash` | SHA-256 de uma representação PDF. Não é um campo implícito do NDF-core v1.0.0; só pertence a um schema de documento ou perfil de saída versionado que o declare. |
| `alt` | Texto alternativo em elementos visuais (`imagem`, `svg`); obrigatório para conformidade PDF/UA-2 |
| `rotulo_acessivel` | Tooltip acessível em campos interativos (`campos[]`, `grelha_digitos`); emitido como `/TU` no AcroForm para PDF/UA-2 |
| `linha_lateral` | Elemento de `fluxo.elementos` que agrupa elementos lado a lado; resolve duplos blocos de assinatura e disposições colunares em documentos de fluxo |
| `campo_ndf` | Tipo de elemento em `mobilia[]` — valor NDF escalar formatado no cabeçalho/rodapé de página |
| `{ndf:caminho}` | Sintaxe de interpolação de dados NDF em `texto_fixo` de `mobilia[]`; distinto de `{{placeholder_ndt}}` e de `{n}/{total}` |
| `quebra_pagina` | Elemento de `fluxo.elementos` que força início de nova página na `sequencia[]` |
| `tabela` (bloco) | Array NDF renderizado como tabela de linhas e colunas com layout definido no NDT |
| `min_linhas_visivel` | Número mínimo de linhas a renderizar; o renderizador completa com linhas em branco |
| `fluxo` | Região de layout vertical sequencial numa `pagina_def`; para documentos com corpo de extensão variável |
| `corpo` | Bloco de texto NCRTF com fluxo, referenciado por caminho NDF |
| `mobilia` | Elementos fixos de página: numeração, marca de água, texto de rodapé |
| `sequencia` | Ordenação e modos de repetição das `paginas_def` no documento final |
| `incluir_se` | Referência direta a booleano NDF; controla a inclusão condicional de elementos e secções |
| `recurso` | Imagem ou fonte referenciada no layout: embebida no NDT ou por hash |
| `composicao` | Mecanismo de entrega conjunta de documentos independentes num único ficheiro |
| Caminho canónico | Referência a um dado NDF por percurso hierárquico de identificadores |
| Formato de apresentação | Hint de renderização visual (monetario, data, checkbox, etc.) sem semântica de validação |
| Token de paginação | `{n}`, `{total}` — resolvidos pelo renderizador; distintos de placeholders NDT e caminhos NDF |
| Placeholder NDT | `{{versao_ndt}}`, `{{schema_id}}` — metadados do próprio NDT, em `texto_fixo` |
| Fidelidade normativa | Equivalência visual e semântica segundo um perfil de renderizador; identidade binária exige perfil determinístico específico |
| Fidelidade melhor esforço | Conteúdo fiel; layout adaptado às convenções do formato; aplica-se a ODF e HTML |
| ODF | OpenDocument Format — ISO/IEC 26300; formato secundário para intercâmbio e edição |
