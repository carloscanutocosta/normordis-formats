# Estudo de alinhamento com o OpenDocument (ODF)

**Estado:** estudo de desenho, não normativo. Nenhuma decisão aqui registada
altera uma especificação enquanto não for aprovada e vertida para a SPEC
respetiva.

**Origem:** pedido do responsável do projeto (2026-08-17), na sequência da
verificação T3 do roadmap NDT — cobertura NCRTF para documentos normativos.

**Objetivo:** determinar o que o NCRTF e o NDT devem incorporar, por inspiração
no ODF, para cumprirem o propósito esperado — exprimir documentos institucionais
completos, incluindo texto normativo publicado (o cenário de referência é a
publicação de diplomas em NDF+NDT em vez de PDF), mantendo a separação entre
dados e estrutura.

---

## 1. Porquê o ODF como referência

O ODF (ISO/IEC 26300, OASIS OpenDocument) resolveu há duas décadas os problemas
que o NCRTF e o NDT enfrentam agora, é norma internacional aberta, e é o formato
de intercâmbio recomendado para a Administração Pública portuguesa — a mesma
razão que levou o NDT a adotá-lo como formato secundário (SPEC NDT §1.3).

Usá-lo como referência de vocabulário tem três vantagens: evita reinventar
soluções para problemas resolvidos; torna o mapeamento NDT→ODF quase direto, o
que reduz o custo do renderizador; e alinha o projeto com uma norma existente,
o que ajuda o objetivo declarado de normalização (NP/EN/ISO).

**Não significa copiar o ODF.** O ODF é um formato de aplicação de escritório:
carrega estado de edição, estado da aplicação e mecanismos de autoria que
colidem frontalmente com a imutabilidade do NDF. A cláusula 4 fixa o critério
de triagem.

## 2. Mapeamento de camadas

O ODF separa em ficheiros o que o NORMORDIS separa em formatos. A
correspondência é reveladora:

| Camada ODF | Papel | Correspondente NORMORDIS | Estado |
|---|---|---|---|
| `content.xml` → `office:text` | conteúdo estruturado do documento | NCRTF, como valor dentro do NDF | **subconjunto** |
| `styles.xml` → `style:style`, `text:list-style` | estilos nomeados e herança | NDT `estilos` | **subconjunto** |
| `styles.xml` → `style:page-layout`, `style:master-page` | geometria, páginas mestras, cabeçalhos | NDT `layout`, `paginas_def`, `mobilia` | **subconjunto** |
| `meta.xml` → `office:meta` (Dublin Core) | metadados do documento | NDF `metadados` | **superconjunto** |
| `META-INF/manifest.xml` | inventário do pacote | `.ndfpkg` `manifest.json` | equivalente |
| `META-INF/documentsignatures.xml` (XAdES) | assinatura do pacote | envelope NDF (CAdES-B-LTA) | **superconjunto** |
| `settings.xml` | estado da aplicação | — | deliberadamente ausente |
| `text:tracked-changes`, `office:annotation` | estado de edição | — | deliberadamente ausente |

O quadro mostra onde está o trabalho: o NORMORDIS **excede** o ODF nas camadas
de metadados, assinatura e custódia — que são a sua razão de existir — e fica
**aquém** nas camadas de conteúdo e de estilo. É exatamente aí, e só aí, que
deve importar.

## 3. O que o cenário de referência exige

Publicar um diploma em NDF+NDT, e não em PDF, só tem valor se o resultado for
*mais* processável do que o PDF. Isso exige, no mínimo:

1. **estrutura de articulado** — artigos, números, alíneas, subalíneas, com
   numeração correta e estável;
2. **remissões que resolvem** — "nos termos do artigo 5.º" tem de ser um
   ponteiro, não texto morto;
3. **notas de rodapé** — aparato de notas é constitutivo do texto legal;
4. **paginação de qualidade** — sem títulos isolados no fim da página, com
   páginas espelhadas para impressão frente e verso;
5. **fidelidade nas três saídas** — PDF/A para arquivo, ODF para intercâmbio,
   HTML para consulta pública, a partir do mesmo par NDF+NDT.

Dos cinco, **nenhum está hoje inteiramente coberto**.

## 4. Critério de triagem

Três perguntas, por esta ordem. Qualquer elemento ODF candidato tem de passar
as três.

O critério geral de colocação por camada — incluindo o teste decisivo *"quando
isto mudar, é preciso reassinar o documento?"* — está em
[`CRITERIO-DE-CAMADAS.md`](CRITERIO-DE-CAMADAS.md). As três perguntas seguintes
são a sua aplicação à triagem de vocabulário ODF.

**P1 — É necessário para reconstituir o documento finalizado?**
Se não, está fora, seja qual for a sua utilidade num editor. É o mesmo teste de
âmbito que o `LACUNAS.md` aplica ao NDF.

**P2 — Varia por documento, ou é estável por tipo de documento?**
O que varia é conteúdo: vai para o NCRTF, dentro do NDF. O que é estável é
estrutura e estilo: vai para o NDT. Esta é a fronteira que o utilizador fixou —
NDT como `styles.xml`, NDF como o que varia — e resolve por si a maioria dos
casos duvidosos.

**P3 — Sobrevive à finalização?**
Estado de edição, estado da aplicação e intenções de autoria não sobrevivem: o
NDF é imutável e a sucessão documental faz-se por `relacoes[]` (ADR-011), não
por marcas de revisão dentro do conteúdo.

## 5. Avaliação do NCRTF

Estado de partida: NCRTF v2.0.0 tem `paragraph`, `heading`, `list`/`list_item`,
`blockquote`, `table`, `image`, `text`, `link`, `hard_break` e sete marcas
inline. A verificação T3 (roadmap NDT) está registada em `specs/ndt/ROADMAP.md`.

### Prioridade 1 — bloqueiam o texto normativo

| Ref | Lacuna | Vocabulário ODF | Notas |
|---|---|---|---|
| **N1** | Notas de rodapé e de fim | `text:note` com `text:note-class` (`footnote`/`endnote`), `text:note-citation`, `text:note-body` | Exige articulação com o NDT — ver A2 |
| **N2** | Referências cruzadas internas | `text:reference-mark`, `text:reference-mark-start`/`-end`, `text:reference-ref` | Sem isto, uma remissão é texto morto e o NDF não é mais processável que um PDF |
| **N3** | Listas com numeração por nível | `text:list-level-style-number` (`style:num-format`, `text:start-value`, `text:display-levels`) | O *estilo* de numeração pertence ao NDT — ver A1 |

### Prioridade 2 — qualidade editorial

| Ref | Lacuna | Vocabulário ODF | Notas |
|---|---|---|---|
| **N4** | Células combinadas em tabela | `table:number-columns-spanned`, `table:number-rows-spanned`, `table:covered-table-cell` | Já ausente no NDT por decisão, mas em texto corrido é frequente |
| **N5** | Formatação dentro de células | conteúdo de `table:table-cell` | Já candidato em NCRTF §11.3; obriga a estender as regras de canonicalização R1–R6 ao conteúdo das células |
| **N6** | `code_block`, `horizontal_rule` | `text:p` com estilo; separadores | Já candidatos em NCRTF §11.3 |

### Prioridade 3 — a decidir por estudo próprio

| Ref | Questão | Vocabulário ODF | Porque não é imediata |
|---|---|---|---|
| **N7** | Idioma por fragmento | `fo:language`, `fo:country` em `style:text-properties` | Resolveria a lacuna **L14** do NDF (documentos multilingues) no sítio certo: o idioma de um trecho é propriedade do texto, não do documento. Decisão conjunta NDF+NCRTF |
| **N8** | Metadados semânticos no conteúdo | ODF 1.2+ *In Content Metadata (RDFa)*, `text:meta`, `xhtml:about`/`xhtml:property` | Permitiria marcar "este parágrafo é o Artigo 5.º, n.º 2" e tornar o articulado processável por máquina. **Mas** pode pertencer ao `documento` do NDF, não ao NCRTF — é uma decisão de fronteira, não uma adição. Relaciona-se com o vocabulário de papéis de 7.1: o papel diz o que um bloco **é**; o metadado semântico dá-lhe **identidade** referenciável |

## 6. Avaliação do NDT

### Prioridade 1

| Ref | Lacuna | Vocabulário ODF | Impacto |
|---|---|---|---|
| **T1** | Páginas pares/ímpares e margens espelhadas | `style:page-usage` — `all` (predefinido), `left`, `right`, `mirrored` | O NDT não distingue página par de ímpar. Qualquer documento oficial impresso frente e verso precisa de margens espelhadas |
| **T2** | Viúvas, órfãs e manter junto | `fo:orphans`, `fo:widows`, `fo:keep-with-next`, `fo:keep-together` em `style:paragraph-properties` | O NDT **não tem nada** nesta matéria. É a diferença entre um documento publicável e um com um título sozinho no fundo da página |
| **T3** | Área de notas de rodapé | configuração de notas na page-layout e separador de notas | Consequência direta de N1: sem declaração de área, o renderizador não sabe reservar espaço no fundo da página |

### Prioridade 2

| Ref | Lacuna | Vocabulário ODF | Impacto |
|---|---|---|---|
| **T4** | Estilos nomeados com herança | `style:style` com `style:parent-style-name`, referenciados por `text:style-name` | Maior diferença estrutural face ao ODF. Permitiria ao NCRTF ser puramente semântico — declarar "isto é uma citação legal" sem dizer como se vê |
| **T5** | Formato da numeração de página | `style:num-format` na página mestra | Romanos no preâmbulo, árabes no corpo. O NDT tem `{n}`/`{total}` sem formato |
| **T6** | Texto em múltiplas colunas | `style:columns` | **Reabre uma exclusão**: o roadmap NDT excluiu-o por "raro em AP; sem pedido documentado". O Diário da República publica a duas colunas — o pedido documentado que faltava existe agora |
| **T7** | Secção corrente no cabeçalho | `text:chapter` | Cabeçalho que acompanha o capítulo ou artigo corrente |

### Prioridade 3

| Ref | Questão | Vocabulário ODF |
|---|---|---|
| **T8** | Regiões nomeadas com visibilidade condicional | `text:section` com `text:display`/`text:condition`. O NDT tem `incluir_se` por elemento; falta granularidade de região |

## 7. Pontos de articulação NDT ↔ NCRTF

São as decisões de fronteira. Cada uma tem de ser resolvida **antes** de
redigir, porque determina em que especificação entra o quê.

| Ref | Questão | Recomendação |
|---|---|---|
| **A1** | Numeração de listas: formato no conteúdo ou no estilo? | **No NDT.** É o modelo ODF — as *list styles* vivem em `styles.xml`. O NCRTF declara nível e continuidade; o NDT declara se o nível 3 se apresenta como `a)` ou `i)`. Coerente com P2 do critério |
| **A2** | Notas de rodapé: onde acaba o conteúdo e começa o layout? | **Conteúdo no NCRTF** (texto da nota, âncora); **área, separador e numeração no NDT**. A nota é conteúdo; a sua colocação na página é layout |
| **A3** | Estilos nomeados (T4): o NCRTF passa a referenciar estilos? | **Sim, mas por papel semântico e não por estilo visual.** A análise completa está na cláusula 7.1 |
| **A4** | Idioma (N7): documento ou fragmento? | Ambos, com papéis distintos: `metadados.idioma` no NDF é o idioma principal declarado; o NCRTF marcaria exceções por fragmento. Resolve L14 sem alterar a semântica atual |

### 7.1 A dependência de estilo entre NCRTF e NDT

A objeção a T4 é que o NCRTF passaria a depender do NDT. A análise mostra que a
objeção assenta numa premissa falsa e que, bem formulada, a dependência não é
nova nem vai na direção que se receia.

**A dependência já existe, na pior forma possível.** O NCRTF v2.0.0 transporta
propriedades de apresentação dentro do conteúdo: `font_family` (em `paragraph`,
`heading`, `blockquote` e `text`), `alignment`, `indent` e `width_percent`. A
§1.2 assume-o expressamente — *"controlo de alinhamento, indentação e família
tipográfica por bloco ou por nó inline"* — em tensão com a §1.3, que atribui a
tipografia ao NDT. O NDT, por seu lado, já define em §5.8 a tabela de resolução
`LiberationSerif` ↔ `Times`. Os dois formatos não se tocam apenas por caminhos
de dados: tocam-se por decisões tipográficas.

**Porque é que a forma atual é a pior.** O NCRTF vive dentro do `payload_bytes`
canonicalizado e assinado, e aí uma decisão de apresentação torna-se
**imutável e replicada**: cada documento produzido transporta a sua própria
cópia da escolha tipográfica, e não existe sítio central onde a alterar — nem
sequer para os documentos futuros, já que cada produtor teria de repetir a
decisão e mantê-la coerente. No NDT, a mesma decisão é declarada uma vez e vale
para todos os documentos que venham a ser produzidos com aquele template.

O par NDF+NDT existente é fixo e assim deve permanecer: o `ndt_version_ref` está
dentro do payload assinado e o renderizador confirma a correspondência exata
(SPEC NDT §7). A separação não serve para re-renderizar o passado — serve para
não repetir a decisão em cada documento e para a poder mudar, num só sítio, para
o futuro. Ver [`CRITERIO-DE-CAMADAS.md`](CRITERIO-DE-CAMADAS.md) §3.1.

**A formulação correta inverte a direção.** O NCRTF não deve referenciar um
*estilo* do NDT — isso seria acoplamento a uma apresentação concreta. Deve
declarar o **papel semântico** do bloco: `citacao-legal`, `formula-promulgacao`,
`nota-editorial`. O NDT declara como cada papel se apresenta.

| | Quem declara | Quem depende de quem |
|---|---|---|
| Modelo ODF (`text:style-name`) | conteúdo aponta para estilo concreto | conteúdo → estilo |
| Modelo proposto (papel semântico) | conteúdo declara o que a coisa **é** | NDT → vocabulário de papéis |

Na formulação por papel, o NCRTF não precisa de saber nada sobre o NDT: é o NDT
que tem de conhecer o vocabulário de papéis. Essa dependência **já existe e é
natural** — o NDT renderiza NCRTF e já mapeia as suas famílias tipográficas.
Não se cria dependência nova; substitui-se uma dependência má por uma boa.

A referência aqui não é o ODF, mas o par HTML/CSS: `class` declara o papel, a
folha de estilo declara a apresentação. No ODF, `text:style-name` aponta para um
estilo concreto do mesmo pacote — acoplamento a uma apresentação determinada. O
NCRTF deve declarar o papel e deixar a apresentação ao template, porque o mesmo
papel é estilizado por templates diferentes ao longo das sucessivas `versao_ndt`
de um tipo documental, ainda que cada documento fique ligado à sua.

**Degradação graciosa.** Um papel desconhecido cai no estilo por defeito do tipo
de nó, tal como uma `class` desconhecida em HTML. Um NCRTF continua legível sem
NDT nenhum. O acoplamento é fraco por construção.

**Risco real: fragmentação do vocabulário.** Um espaço de papéis aberto leva a
que cada entidade invente os seus e o vocabulário deixe de significar algo. A
mitigação já existe no projeto e deve ser reutilizada: vocabulário base fechado
mais extensão qualificada `ext.<entidade>.<papel>` — o padrão de `relacoes[].tipo`
(ADR-008) e de `tipo_documento_ref` (ADR-014).

**Consequência para os campos atuais.** Se o modelo de papéis avançar,
`font_family`, `alignment` e `indent` ficam do lado errado da fronteira. Removê-los
é MAJOR e não se propõe agora. Propõe-se decidir, na versão que introduzir os
papéis, que o papel semântico tem precedência e que aqueles campos passam a
mecanismo legado — deixando a remoção para uma eventual v3.0. `width_percent`
em `image` é caso distinto e legítimo: dimensiona um objeto que só existe no
conteúdo.

### 7.2 Limite do sistema de estilos do NDT

Decidida a direção (7.1), falta o limite. É a decisão de desenho mais fácil de
perder e a mais cara de corrigir depois.

**Estilos nomeados e planos, com um nível de herança no máximo.** Suficiente
para a alteração transversal — mudar o estilo `citacao-legal` e todos os blocos
com esse papel acompanham; insuficiente para se tornar uma linguagem de folhas
de estilo.

Excluídos por decisão: cascata com resolução por especificidade, herança
múltipla, estilos automáticos gerados por instância (o `style:style` automático
do ODF), e seletores. O ODF tem centenas de elementos porque persegue a
expressividade universal de uma aplicação de escritório; o valor do NDT está em
ser pequeno e auditável por uma pessoa. Trocar uma coisa pela outra é mau
negócio.

**Dois níveis, não um.** O ODF separa estilo de parágrafo (`style:style`) de
estilo de página (`style:page-layout` + `style:master-page`). O NDT já tem o
nível de página, em `paginas_def`; falta-lhe o nível de parágrafo. As
propriedades de paginação fina — `fo:orphans`, `fo:widows`, `fo:keep-with-next`
(T2) — pertencem ao nível de parágrafo; páginas espelhadas (T1), área de notas
(T3) e colunas (T6) pertencem ao nível de página.

**O que os estilos não resolvem.** No perfil de impresso, a geometria *é* o
documento: uma caixa de dígitos a 60 mm da margem não é um estilo, é uma
exigência do formulário oficial. Nenhum sistema de estilos exprime isso bem, e é
por isso que o NDT mantém `paginas_def` com coordenadas absolutas além de
`estilos`, com os dois modelos mutuamente exclusivos na mesma página
(`NDT-PROD-008`). Os estilos dão versatilidade ao perfil de texto corrido; não
substituem o layout absoluto.

## 8. O que não incorporar, e porquê

Registado explicitamente para que a decisão não tenha de ser retomada:

| Elemento ODF | Razão da exclusão |
|---|---|
| `text:tracked-changes` | Colide com a imutabilidade do NDF. A sucessão documental é por `relacoes[]` (ADR-011), entre documentos finalizados |
| `office:annotation` | Comentários são estado de trabalho; não pertencem a um documento finalizado |
| `settings.xml` | Estado da aplicação. O próprio ODF o isola por ser não normativo para o conteúdo |
| `text:author-name`, `text:date` e campos afins | No NORMORDIS a autoria e a data vêm do NDF, assinadas. Importá-los criaria, dentro do conteúdo, dados não assinados que podem contradizer o envelope |
| `text:table-of-content`, `text:alphabetical-index` | Derivam dos `heading`; são geração do renderizador, não conteúdo a canonicalizar |
| `table:formula`, `office:scripts` | O NDT removeu deliberadamente o motor de expressões (CHANGELOG 2.0.0). Cálculo é da aplicação de domínio |
| Vocabulário `draw:` completo | O NDT limita as primitivas por decisão expressa (SPEC §5.3, nota normativa) |

## 9. Plano faseado

Todas as alterações propostas são **aditivas** — MINOR na política de extensão
do NCRTF (§11.1) e no versionamento do NDT (§2). Nenhum leitor existente quebra.

**Fase A — texto normativo (NCRTF v2.1 + NDT v2.1, coordenadas)**
N1+T3 (notas de rodapé), N2 (referências cruzadas), N3+A1 (listas por nível).
Fecha os pontos 1–3 da cláusula 3. É o caminho crítico para o cenário de
referência.

**Fase B — qualidade editorial e impressão**
T1 (páginas espelhadas), T2 (viúvas e órfãs), T5 (formato de numeração), N4, N5,
N6. Fecha o ponto 4.

**Fase C — decisões de fronteira**
T4+A3 (estilos nomeados), T6 (colunas — exige reabrir a exclusão do roadmap),
N7+A4 (idioma), N8 (metadados semânticos), T8.

**Precedência:** A1, A2 e A4 são pré-requisitos de redação da Fase A. A3 é
pré-requisito da Fase C e condiciona T4.

## 10. Riscos e questões em aberto

1. **Canonicalização.** Cada nó novo exige regra explícita nas restrições R1–R6
   do NCRTF (§8.2). As notas de rodapé introduzem conteúdo fora do fluxo
   principal: a canonicalização JCS não muda, mas a regra de fusão de nós `text`
   contíguos tem de ser reformulada para o corpo da nota.
2. **Integridade das referências.** Uma referência cruzada é um ponteiro
   intra-documento — ao contrário de `relacoes[]`, não precisa de `payload_hash`,
   mas precisa de garantia de resolução. Implica requisitos novos de produtor e
   de leitor NCRTF: toda a referência resolve para uma marca existente.
3. **Acoplamento.** T4/A3 **não** introduz a primeira dependência de estilo entre
   NCRTF e NDT: essa já existe, através de `font_family`, `alignment` e `indent`
   no NCRTF e da tabela de resolução tipográfica do NDT §5.8. O risco a gerir não
   é criar acoplamento, é a fragmentação do vocabulário de papéis — ver 7.1.
4. **Custo de conformidade.** Cada nó novo gera casos na suite NCRTF; cada campo
   NDT gera um `NDT-PROD-*`. A Fase A deve fazer crescer a suite proporcional-
   mente, ou repete-se o problema que este trabalho acabou de corrigir.
5. **Verificação normativa pendente.** Os nomes de elementos e atributos aqui
   usados foram confirmados por fonte para `style:page-usage`, `text:note`,
   `text:list-level-style-number`, `fo:keep-*`/`fo:orphans`/`fo:widows` e para a
   existência de *In Content Metadata (RDFa)* em ODF 1.2. Os valores de
   `text:reference-format` **não** foram confirmados. Antes de qualquer redação
   normativa, confirmar cláusula a cláusula contra OASIS ODF 1.3 Parte 3 /
   ISO/IEC 26300.
6. **Propriedade intelectual.** Inspirar-se no vocabulário conceptual do ODF não
   levanta problema; reproduzir texto normativo levanta. A relação com o ODF
   deve ficar registada em `docs/normalization/IPR-DECLARATIONS.md` e nas
   referências normativas antes da publicação.

## 11. Fontes consultadas

- [OASIS ODF 1.3 — Parte 3: OpenDocument Schema](https://docs.oasis-open.org/office/OpenDocument/v1.3/OpenDocument-v1.3-part3-schema.html)
- [OASIS ODF 1.3 — Parte 2: Packages](https://docs.oasis-open.org/office/OpenDocument/v1.3/OpenDocument-v1.3-part2-packages.html)
- [OASIS ODF 1.2 — Parte 1 (metadados e RDFa)](https://docs.oasis-open.org/office/v1.2/OpenDocument-v1.2-part1.pdf)
- [Library of Congress — OpenDocument Format (ODF) Family, OASIS e ISO/IEC 26300](https://www.loc.gov/preservation/digital/formats/fdd/fdd000247.shtml)
- [ODF Toolkit — `TextListLevelStyleNumberElement`](https://odftoolkit.org/api/odfdom/org/odftoolkit/odfdom/dom/element/text/TextListLevelStyleNumberElement.html)
- [ODF Toolkit — `StyleParagraphPropertiesElement`](https://odftoolkit.org/api/odfdom/org/odftoolkit/odfdom/dom/element/style/StyleParagraphPropertiesElement.html)
