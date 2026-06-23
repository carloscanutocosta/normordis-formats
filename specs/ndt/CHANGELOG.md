# NDT Changelog

> Nota: descrições históricas de `ndt_hash`, `NDF.outputs[]` e reutilização do
> mesmo CAdES foram substituídas pelo modelo normativo comum em
> `docs/architecture/ARCHITECTURE.md`. Não constituem requisitos actuais.

## [2.0.0] — Draft — Revisão pública

### Axioma e papel do NDT (revisão fundamental)

Esta versão estabelece o axioma central do formato: **NDT + NDF = documento físico determinístico e rico**.

O NDT é um formato declarativo de **layout puro**. Não contém regras de
validação do domínio, fórmulas de cálculo, motor de expressões nem lógica de
negócio. O renderizador verifica apenas versões, referências, integridade e
estrutura necessárias à renderização; não decide regras jurídicas ou de
negócio.

Face ao draft anterior, foram **removidos** por não pertencerem ao NDT:
- Hierarquia lógica como schema (tipos de campo com validação, `campo_calculado`, `tabela_repetivel` com colunas tipadas, `grupo` com exclusividade)
- Motor de expressões NDT-expr (operadores, funções, referências `linha.`, `impresso.`)
- Funções externas (`funcoes_externas[]`)
- Validações cruzadas (`validacoes[]`)
- Visibilidade e obrigatoriedade condicional por expressão (`visivel_se`, `obrigatorio_se`)
- Campo `perfil` de complexidade

### Identidade e versionamento
- `versao_ndt` substitui `versao_impresso` — aplica-se a qualquer template, não só impressos fiscais
- Campos de metadados simplificados: `titulo`, `emissor`, `referencia_legal`

### Endereçamento NDF
- Caminhos canónicos como **convenção de endereçamento**, não como schema
- **Formatos de display** (§3.3): hints de renderização visual sem semântica de validação (`texto`, `numero`, `inteiro`, `monetario`, `data`, `booleano`, `checkbox`, `radio`)
- Ausência de valor no NDF → campo em branco, sem erro

### Layout
- `paginas_def[]` com `graficos[]`, `campos[]`, `blocos[]`, `mobilia[]`
- Primitivas gráficas: `linha`, `rectangulo`, `grelha_digitos`, `imagem`, `texto_fixo`, `codigo_barras`, `poligono`, `elipse`, `svg`, `tabela_visual`
- `rotacao` e `layer` em qualquer elemento gráfico
- `campos[]`: valores NDF escalares posicionados em coordenadas absolutas
- `blocos[]`: `tabela` (array NDF → linhas), `corpo` (NCRTF com fluxo), `cabecalho`, `rodape`
- **`min_linhas_visivel`** em `tabela`: o renderer completa com linhas em branco até ao mínimo — garante que impressos fiscais renderizam o frame mesmo sem dados
- `sequencia[]`: `unica`, `por_linha`, `conforme_necessario`
- **`incluir_se`** na sequência: referência direta a booleano NDF (não é expressão); controla inclusão de secções de página
- Mobília: `numero_pagina` (`{n}`, `{total}`), `texto_fixo` (placeholders NDT), `marca_agua`
- Recursos: `embebido` (base64 com prefixo `"base64:"`) ou `referenciado_por_hash` (com prefixo `"sha256:"`)

### Composição
- `composicao[]` com `resolver` de tipo `referencia_documental` (template de string, não expressão)
- Cada documento mantém NDT/NDF próprios; documentos compostos têm de estar fechados

### NDF ↔ NDT: reprodutibilidade
- NDF referencia `schema_id@versao_ndt` — não incorpora o NDT, mantém-se eficiente
- Para documentos fechados: `ndt_hash` (SHA-256 do NDT) garante reprodutibilidade bit-perfeita

### Estilos globais (`estilos`) [novo]
- `fonte_padrao`, `cor_texto`, `cor_primaria`, `espacamento_entre_paragrafos_mm`, `identacao_lista_mm`, `cabecalhos[]`
- Fonte principal de estilo para renderers ODF/HTML; fallback para renderers PDF
- Mapeia para estilos Word, variáveis CSS, ou estilos Typst conforme o renderer

### Layout de fluxo (`fluxo`) em `pagina_def` [novo]
- Resolve o posicionamento relativo em documentos administrativos: elementos após `corpo` de extensão variável
- `fluxo.y_inicio` + `fluxo.elementos[]` — pilha vertical a partir de Y declarado
- Tipos em `fluxo.elementos`: `corpo`, `tabela`, `texto_fixo`, `campo`, `espaco`, `separador`, `assinatura`
- Elementos após `corpo` aparecem na última página do overflow, imediatamente após o fim do corpo
- `fluxo` e `blocos[]` são mutuamente exclusivos na mesma `pagina_def`

### Campo de assinatura (`assinatura`) [novo]
- Novo tipo em `graficos[]` e em `fluxo.elementos`
- Novo campo `modo`: `"visual_apenas"` | `"hibrido"` (default) | `"ndf_attachment"`
- **Modelo híbrido (default)**: CAdES-B-LTA do NDF (que inclui `pdf_hash`) é também o contentor PAdES do campo AcroForm no PDF; CAdES embutido como attachment PDF/A-3. PDF autossuficiente para validadores eIDAS; NDF é a fonte de verdade.
- ODF: linha de assinatura com campo de formulário; HTML: `<div class="signature-field" data-id="...">`. `modo` ignorado em formatos de fluxo.
- Campos: `id`, `rotulo`, `posicao` (obrigatório em `graficos[]`, omitido em `fluxo`), `largura`, `altura`, `modo`

### PDF/UA-2 como formato alvo [novo §8.2]
- Renderer PDF conforme produz PDF/UA-2 (ISO 14289-2) + PDF/A-3 (ISO 19005-3) simultaneamente
- Implicações NDT: `graficos[].imagem` e `graficos[].svg` aceitam campo `alt`; elementos decorativos marcados `"alt": ""`
- Tags de estrutura lógica inferidas a partir de `blocos[]` e `fluxo.elementos`
- Campos `assinatura`, `grelha_digitos` e `checkbox`/`radio` geram AcroForm com `/TU` (tooltip acessível)
- Idioma do documento via `NDF.metadados.idioma`

### Modelo de assinatura CAdES ↔ PDF [novo §8.1]
- Workflow de fecho: `pdf_hash` adicionado ao NDF antes de assinar; CAdES-B-LTA cobre NDF + `pdf_hash`
- Workflow de verificação determinística: regenerar PDF → confirmar `sha256(PDF) == NDF.outputs[].sha256`
- Distinção CAdES/PAdES: mesmo algoritmo CMS; objetos assinados distintos (NDF JSON vs. PDF ByteRange); cross-referenciados via `pdf_hash` e `ndf_ref`

### `incluir_se` ao nível de elemento [novo]
- Anteriormente só disponível em `sequencia[]`; agora disponível em `campos[]`, `blocos[]` e `fluxo.elementos`
- Referência direta a booleano NDF — não é uma expressão

### Fidelidade por formato de saída [novo §1.3]
- **PDF/A** — formato primário; fidelidade normativa (bit-idêntico para o mesmo NDT+NDF); arquivo, prova, entrega formal
- **ODF** — formato secundário; fidelidade de conteúdo via `estilos` NDT; intercâmbio, edição, revisão. Escolha motivada por soberania digital: ISO/IEC 26300, sem dependência de licença proprietária, alinhado com o RNID. Implementações: LibreOffice, Collabora, OpenOffice, EuroOffice, OnlyOffice.
- **HTML** — fidelidade de conteúdo; publicação e consulta; layout CSS flow
- **Typst** — fidelidade alta; mm coords como dicas; composição tipográfica avançada
- DOCX/Word excluído: apesar de normativo (ISO 29500), é controlado por fornecedor único — contradiz o princípio de soberania digital do projeto

### Dados NDF em `mobilia[]` [novo]
- `tipo: "texto_fixo"` em mobília aceita `{ndf:caminho.canonico}` para interpolação de valores NDF (referência, entidade, etc.)
- Novo `tipo: "campo_ndf"` em mobilia — valor NDF escalar formatado (data, monetário); mesma semântica de `campos[]`
- Distinção de três famílias de tokens: `{ndf:caminho}` (dados NDF), `{{placeholder_ndt}}` (metadados NDT), `{n}/{total}` (paginação)

### Layout lateral em `fluxo` (`linha_lateral`) [novo §5.2.2]
- Novo tipo em `fluxo.elementos` — agrupa colunas lado a lado (ex.: duplo bloco de assinatura)
- Campos: `elementos[]` com `largura` e `conteudo[]` (pilha vertical de elementos de fluxo por coluna)
- Altura da `linha_lateral` = altura máxima entre colunas; colunas mais curtas deixam espaço em branco

### Imagem em `fluxo.elementos` [novo]
- Novo `tipo: "imagem"` em `fluxo.elementos` — logo, gráfico ou ilustração após o corpo de texto
- Campos: `referencia_recurso`, `largura`, `altura`, `manter_proporcao`, `alinhamento`, `alt`

### Quebra de página em `fluxo` [novo]
- Novo `tipo: "quebra_pagina"` em `fluxo.elementos` — força início de nova instância de `pagina_def` na `sequencia[]`

### `rotulo_acessivel` em `campos[]` e `grelha_digitos` [novo]
- Campo opcional em `campos[]` e `grelha_digitos` com o texto legível por leitores de ecrã
- Emitido como `/TU` no AcroForm PDF/UA-2; obrigatório para `checkbox` e `radio`
- Se omitido em campos de texto, o renderer usa `referencia` como fallback

### Harmonização NDT + NDF + NCRTF [alinhamento inter-specs]
- Mapeamento canónico NCRTF ↔ NDT em §5.8: `LiberationSans`↔`Helvetica`, `LiberationSerif`↔`Times`, `LiberationMono`↔`Courier`
- `{{validation_code}}` definido como token renderer-provided em `texto_fixo` e `codigo_barras` — resolvido pelo renderer a partir do envelope NDF (não é dado do NDF-core nem metadado NDT)
- Exemplo QR code em `codigo_barras` com `"conteudo": "https://validar.normordis.pt/{{validation_code}}"`

### Conformidade
- Renderer conforme não recusa renderizar por dados ausentes ou incorrectos
- Renderer conforme respeita `min_linhas_visivel`
- Renderer conforme implementa `fluxo` e garante posicionamento de elementos pós-`corpo`
- Renderer conforme interpreta `{ndf:caminho}` em `mobilia[].texto_fixo.conteudo`
- Renderer conforme emite `rotulo_acessivel` como `/TU` em campos AcroForm (PDF/UA-2)
- Renderer conforme resolve `{{validation_code}}` a partir do envelope NDF
- Campos e colunas descontinuados marcados `"descontinuado": true`, não removidos
- Caminhos canónicos estáveis entre versões de `versao_ndt`
