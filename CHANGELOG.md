# Histórico de alterações

As alterações relevantes às especificações NORMORDIS são registadas aqui. Cada
formato mantém também o seu histórico em `specs/<formato>/CHANGELOG.md`.

## [Não publicado]

### Conjunto de transferência — schemas, exemplo e vetores (2026-08-23)

Executados os passos 2 a 4 da sequência do desenho. Nada disto é requisito de
conformidade NDF nem entra na SPEC: é camada exterior ao documento, como o Perfil
de Ciclo de Vida (ADR-010), e um produtor conforme pode nunca a usar.

- **`specs/ndf/schemas/transferencia.schema.json`** — declaração de composição de
  um `.ndfxfer`. Unidades identificadas por `ndf_id` **e** `payload_hash`;
  `referencias_externas[]` declara as relações cujo alvo não está no conjunto,
  e é **recomputável pelo recetor**, logo verificável nos dois sentidos
  (D-XFER-1);
- **`specs/ndf/schemas/evidencia-custodia.schema.json`** — extrato atestado da
  cadeia, com política de extração declarada e `finalizado` obrigatório na
  política (D-XFER-2). Não é uma cadeia com menos eventos: seria mutilá-la, o que
  `CUST-REQ-004` proíbe;
- **`specs/registry/schemas/aceitacao-custodia.schema.json`** — tipo documental
  novo, produzido pela entidade **recetora**. Fecha L-T3. Aceitação parcial por
  unidade, com fundamento obrigatório na recusa;
- **`specs/ndf/examples/ndfxfer-example/`** — duas unidades, uma com extrato
  integral e outra com extrato parcial. As unidades são geradas por
  `tools/build_ndfxfer_example.py` e não versionadas: são cópias de pacotes já
  sob revisão;
- **`tools/check_transferencia.py`** e **`tools/check_transferencia_vectors.py`**
  — validador e **11 vetores negativos**, no CI. Sem eles, «o conjunto está
  completo» seria alegação e não propriedade;
- **precisado ao implementar:** `inventario[]` **não** cobre as unidades. O
  digest de um `.ndfpkg` é da materialização, não da unidade documental — o mesmo
  documento rezipado tem outro digest e continua a ser a mesma unidade. As
  unidades são cobertas por `payload_hash`, que as prende ao conteúdo assinado;
- **alterado:** o ofício de `ndfpkg-example` passa a declarar `responde_a` o
  ofício n.º 45/2026, que o seu próprio assunto já afirmava. Sem uma relação para
  fora do conjunto, `referencias_externas[]` ficava por exercitar.

**Não executado, deliberadamente:** o passo 5, verificação cláusula a cláusula
contra OAIS/PREMIS/METS. Compete ao gate externo 3 — revisão arquivística — e
`READINESS.md` é expresso em que revisão interna não fecha esses gates.


### Fronteiras da transferência decididas (2026-08-23)

As três fronteiras que o desenho do conjunto de transferência deixara em aberto
estão decididas. Duas não custaram nada ao formato: o conjunto declara
**referências pendentes** — recomputáveis pelo recetor, logo verificáveis — e
não estrutura intelectual; a evidência de custódia declara uma **política de
extração** uniforme em vez de uma seleção caso a caso, que era o vetor de abuso.

A terceira acrescenta `event_type: "recebido"` ao schema de custódia — perfil
opcional, não o NDF-core — e obrigou a escrever o que estava implícito: **as
cadeias de custódia são por custodiante, não globais.** Ver
[`specs/ndf/CHANGELOG.md`](specs/ndf/CHANGELOG.md).


### Anexos, e o desenho do conjunto de transferência (2026-08-23)

**Um documento nativo pode ter anexos — e agora transporta-os.** Verificou-se
que não podia: `oficio` e `informacao-tecnica` declaravam anexos num vocabulário
próprio que o fecho de pacote `NDF-PKG-009` não reconhecia, pelo que um ofício
que transportasse o anexo era rejeitado e um que o omitisse era aceite.
`componentes[]` passa a ser o mecanismo único de binários, disponível a qualquer
tipo; ver [`ADR-025`](docs/architecture/ADR-025-componentes-mecanismo-unico.md) e
SPEC §2.8.1.3, que fixa também o teste que separa um anexo sem identidade própria
de um documento autónomo ligado por relação.

**Conjunto de transferência.**
[`NDF-CONJUNTO-DE-TRANSFERENCIA.md`](docs/design/NDF-CONJUNTO-DE-TRANSFERENCIA.md)
desenha L-T1 a L-T3 dentro da fronteira de `ADR-024`: o conjunto declarado e
selado, a evidência de custódia como extrato atestado — nunca como cadeia
mutilada, pela regra que L-T4 já fixara — e a aceitação como NDF produzido pelo
recetor. Nada exige ao NDF-core; três pontos de decisão ficam explicitamente em
aberto.

**Mapeamento OAIS consolidado.**
[`OAIS-MAPPING.md`](docs/interoperability/OAIS-MAPPING.md) reúne numa vista única
o modelo de informação (o que o NDF adota), o modelo funcional (o que fica fora),
a correspondência SIP/AIP/DIP, as fórmulas defensáveis em texto público e a lista
do que continua por verificar cláusula a cláusula.


### Fronteira formato ↔ direito material, e fronteira formato ↔ arquivo (2026-08-23)

Duas rondas com o mesmo critério: o que o formato representa e o que decide.

**Fronteira face ao direito material.** Correções em `specs/ndf/` onde o
princípio de ADR-022 era ultrapassado — sobretudo em descrições de schema e
exemplos, que são o que os implementadores copiam. `base_legal_conservacao` deixa
de codificar o artigo 6.º do RGPD e passa a par `{regime, base}`; §2.15.4 mantém
todas as regras mas deixa de as fundamentar em conclusões jurídicas; §2.10.1
deixa de dar exemplos de tipos de ato; e o exemplo de captura deixa de declarar o
submissor como autor. Detalhe em [`specs/ndf/CHANGELOG.md`](specs/ndf/CHANGELOG.md)
e na adenda a `ADR-017`.

**Fronteira face ao sistema de gestão documental.** Novo
[`ADR-024`](docs/architecture/ADR-024-fronteira-oais-modelo-de-informacao.md):
de OAIS, o NDF adota o **modelo de informação** e deixa fora o **modelo
funcional** e as responsabilidades organizacionais. Fixa o critério antes de
começar o desenho do conjunto de transferência (L-T1 a L-T3), que obriga a ir
buscar material a OAIS e que sem critério degeneraria em replicar OAIS num
repositório de formatos. Inclui as formulações defensáveis para texto público —
o que não se afirma sobre conformidade OAIS e eIDAS, e a distinção entre perfil
de preservação (B-LTA) e natureza jurídica da assinatura.

**Ferramenta nova:** `tools/reseal_example_package.py`, para recalcular
`payload_hash`, `validation_code` e inventário dos pacotes de exemplo sem
trabalho manual de digests.


### Correções à ronda de neutralização jurisdicional (2026-08-15)

Revisão externa da mesma ronda, no próprio dia. Três correções, uma delas a um
defeito introduzido nessa ronda.

- corrigido: `classificacao_seguranca` mantinha a regra "quando omitido, assumir
  `uso_interno`", que deixou de ser exprimível ao passar de escalar a objeto —
  não é possível inferir um **regime** a partir do silêncio, e um nível sem
  regime não tem significado determinado. A regra é retirada: a ausência passa a
  significar **não declarada** (nova §2.7.4.2). Um custodiante que aplique um
  nível conservador por omissão exerce política própria, legítima por §1.5, que
  não é leitura do NDF nem declaração do produtor;
- corrigido: a migração em bloco atribuíra `perfil: "pt"` a **todos** os casos,
  incluindo `avaliacao-perfil-generico`, o documento alemão — que passava assim
  a declarar o regime de segurança português. O campo foi removido desse caso,
  que passa a exercer também a regra de ausência;
- corrigido: `idioma` era descrito como "BCP 47" quando o padrão implementa o
  subconjunto `língua[-escrita][-região]`. RFC 5646 admite ainda extlang,
  variants, extensions, private-use e grandfathered tags. O texto passa a
  declarar o subconjunto explicitamente, em vez de alegar conformidade com a
  gramática completa. O padrão **não** foi alargado: BCP 47 integral por
  expressão regular seria pior do que um subconjunto declarado;
- precisado: §2.7.4.1 afirmava que um leitor pode ordenar documentos por
  sensibilidade sem conhecer o regime. Passa a delimitar o alcance — ordena os
  **níveis abstratos declarados**, o que suporta triagem operacional e **não**
  constitui comparação objetiva entre regimes soberanos nem equivalência entre
  `RESTREINT UE` e o nível português homónimo;
- atualizado: §1.5, que descrevia o campo na forma escalar anterior;
- adicionado: caso `invalid/idioma-locale-posix.json` — `pt_PT` em vez de
  `pt-PT`. O subconjunto BCP 47 não tinha qualquer cobertura negativa, e os
  valores existentes (`pt`) eram válidos também sob o padrão antigo, pelo que a
  alteração estava sem prova.

### Últimos vestígios de vocabulário nacional no NDF-core (2026-08-15)

Revisão externa observou que ADR-015 generalizou `avaliacao` mas deixou dois
campos de `metadados` a codificar Portugal diretamente no core. Corrigido em
[ADR-017](docs/architecture/ADR-017-identificadores-e-classificacao-por-perfil.md),
com o mesmo critério e antes de existirem utilizadores externos.

- alterado: `entidade_produtora.nif` e `.codigo_dglab` → `identificadores`,
  array de `{sistema, valor}` com `sistema` como identificador opaco
  qualificado (`pt-nif`, `pt-dglab`, `fr-siren`, `nl-kvk`, `eu-vat`, `eu-pic`).
  O core deixa de conhecer a sintaxe de qualquer identificador nacional — a
  validação do valor é do esquema, não do formato;
- alterado: `classificacao_seguranca` de string para `{perfil, nivel}`.
  `perfil` nomeia o regime (`pt`, `eu`, `nato`); `nivel` mantém o enum de seis
  valores, agora definido como **escala ordinal neutra**. Rejeitou-se a forma
  `"pt:reservado"`: delegaria ao perfil a própria noção de nível e impediria
  ordenar dois documentos por sensibilidade sem conhecer os dois regimes — o
  mesmo erro que ADR-015 recusou ao não delegar `avaliacao` inteira;
- registado: a correspondência entre `nivel` e a etiqueta legal do regime é
  declarada pelo produtor e **não é verificada** pela especificação. Arbitrar
  equivalências entre regimes de segurança de Estados soberanos está fora da
  competência do formato (§2.7.4.1);
- alterado: `idioma` de `^[a-z]{2}$` (ISO 639-1) para etiqueta **BCP 47**
  (`língua[-escrita][-região]`), o que passa a distinguir `pt-PT` de `pt-BR` e
  admite `zh-Hant`. Relaxamento de padrão: valores existentes continuam
  válidos;
- corrigido: contradição normativa sobre SHA-256. §2.5 declarava `sha256` como
  único valor válido em **v1.x** e, quatro linhas abaixo, anunciava suporte a
  múltiplos algoritmos na **1.2.0** — que é v1.x. O texto normativo passa a
  fixar 1.0.0 e a remeter compromissos de versão para o roadmap informativo;
- adicionado: justificação escrita de `estado` (§2.4). Um `enum` de um só valor
  parece redundante, mas num documento imutável e assinado declarar um facto
  não equivale a omiti-lo — mesmo raciocínio já aceite para
  `proveniencia_ia.utilizada: false` (ADR-005) e `contem_dados_pessoais: false`
  (ADR-016). Considerada e **rejeitada** a remoção do campo, que seria
  incoerente com dois ADRs;
- migrados 31 `entidade_produtora` e 35 `classificacao_seguranca` em casos de
  conformidade e exemplos; pacotes e cadeia informação→parecer→despacho
  reconstruídos com hashes e referências cruzadas recalculadas;
- registado em `LACUNAS.md`: **L13** (`base_legal_conservacao` — precisão RGPD,
  matéria para revisão jurídica externa) e **L14** (documentos multilingues —
  não resolvido por antecipação, por falta de caso real verificado).

### Verificação das ligações de dados NDT → schema do tipo (2026-08-15)

A pergunta que originou isto foi se o NDF estava estável para se avançar para
NDT sem regressões. Ao testar a junta NDF↔NDT antes de responder, descobriu-se
que **nada a verificava**: `tools/validate.py` conferia a sintaxe dos caminhos
do NDT contra `NDT_PATH_RE` e nunca a sua resolubilidade contra o schema do
tipo documental. Dois NDTs de exemplo tinham ligações impossíveis e ambos os
pacotes estavam verdes.

- adicionado: `check_ndt_bindings` em `tools/validate.py`, ligado a
  `validate_package_dir` — resolve cada `referencia` do NDT contra o schema
  declarado em `tipo_documento_ref`, e cada `colunas[].id` contra os itens do
  array referenciado. Resolve contra o **schema**, nunca contra a instância,
  para distinguir caminho impossível de campo opcional ausente;
- adicionado: vetor `PKG-NEG-009-ndt-referencia-pendurada`, que prova que a
  verificação morde;
- corrigido: `tools/check_package_vectors.py` reportava `8/8` a partir de um
  literal em vez de contar os casos — um vetor novo não aparecia na contagem;
- corrigido: NDT `oficio-generico@2.0.0` referenciava `destinatario.localidade`
  e `signatario_b.nome`/`.cargo`. `oficio.schema.json` tem
  `additionalProperties: false` e declara `destinatario` sem `localidade` e um
  único `signatario` — nenhum ofício conforme poderia ter esses campos, pelo
  que eram template morto. Removidos o campo e a coluna correspondente da
  `linha_lateral`. Se ofícios com dois signatários forem desejáveis, a
  alteração é em `oficio.schema.json` e a coluna regressa — agora com
  verificação a manter os dois artefactos coerentes;
- **em aberto**: o NDT `liquidacao-irs@2026.1` é, no conteúdo, um template de
  ofício — referencia `numero`, `assunto`, `data`, `destinatario.*`, `corpo`,
  `signatario.*`, enquanto o `documento` da liquidação tem `ano_fiscal`,
  `apuramento`, `data_liquidacao`, `meios_reacao`, `nif_sujeito_passivo`,
  `numero_liquidacao` e `prazo_pagamento`. **0 de 13 ligações resolvem.** O
  pacote fica a vermelho deliberadamente: é trabalho de desenho de NDT, não de
  correção mecânica, e o vermelho é o achado.

### Teste de admissão de novas primitivas no NDF-core (2026-08-15)

D5 (2026-08-11) congelou o âmbito do NDF-core mas não definia o que o quebra; a
reabertura de 2026-08-13, para `proveniencia_sistema` e `imputacao`, foi
decidida por juízo caso a caso, sem critério escrito.

- adicionado: teste de admissão em [`ROADMAP.md`](ROADMAP.md) — seis perguntas
  por ordem, em que a primeira resposta afirmativa exclui a primitiva do core,
  mais a tabela do que **não** é alteração de formato (documentação, casos de
  conformidade, tipos documentais, perfis, NDTs, correção de defeito);
- registado: o teste aplica-se **apenas ao NDF-core**. NDT e NCRTF não estão
  sob D5 — D5 desloca-lhes expressamente o esforço —, pelo que trabalho de
  afinação nesses formatos não o aciona;
- registado: articulação com a regra do ADR-015. Este teste decide se uma
  primitiva **entra**; a regra dos três sistemas divergentes decide se uma
  primitiva existente **se generaliza**;
- validado retrospetivamente contra a reabertura de 2026-08-13: o teste devolve
  a mesma decisão que foi tomada, o que reduz o risco de ser racionalização das
  escolhas já feitas.

### Namespace de perfis, terminologia dos artefactos e matriz jurisdicional (2026-08-15)

Ronda de consolidação após revisão externa, sem alteração de âmbito. Um item
com janela temporal — o identificador de perfil entra nos bytes assinados — e
dois editoriais.

- alterado: padrão de `avaliacao.perfil` de `^([a-z]{2}-[a-z0-9-]+|generic)$`
  para `^(generic|[a-z][a-z0-9]*(-[a-z0-9]+)+)$`. O padrão anterior codificava
  a hipótese de que um regime arquivístico é sempre nacional, que é falsa: a
  Comissão Europeia tem regime institucional próprio, e nada exclui perfis
  internacionais ou setoriais. `eu-ec` passava por acaso — `eu` tem duas letras
  — mas `int-un` ou `org-oecd` não passariam. O identificador passa a ser
  **opaco e qualificado**, com a semântica a vir do registo e não do padrão;
- alterado: candidatos `de-bund` → `de-barch` (o perfil é o regime sob
  competência do Bundesarchiv, não o regime federal em geral, que inclui os
  Länder) e `eu-crl` → `eu-ec` (os perfis nomeiam a autoridade, não o
  instrumento que ela publica);
- alterado: SPEC §1.2 deixa de anunciar "três partes" e apresentar duas. Passa a
  distinguir os três **artefactos** (NDF-core, Envelope, NDT) das duas
  **unidades** com nome próprio: *artefacto NDF assinado* (core + envelope,
  unidade mínima verificável) e *pacote NDF* (`.ndfpkg`, unidade mínima
  autossuficiente). A expressão "NDF completo" é abandonada por ser ambígua
  entre as duas;
- adicionado: os termos ao Anexo A da SPEC e a `TERMINOLOGY.md`;
- adicionado: [`docs/profiles/`](docs/profiles/README.md) — matriz de
  compatibilidade jurisdicional e documentos de mapeamento para PT, FR, DE
  federal, NL e Comissão Europeia, cada um com base jurídica **primária
  verificada**, mapeamento NDF, o que um schema poderia impor, e limitações.
  Nenhum schema de perfil novo foi publicado: mapear um regime não é o mesmo que
  ter evidência de sintaxe que possa ser imposta, e só Portugal a tem. `eu-ec`
  fica **experimental** por não ter sido possível obter o SEC(2019)900 integral;
- registado: o R212-13 francês estrutura a avaliação em duas durações mais o
  destino, onde o NDF tem um único `prazo_conservacao`. Analisado como sem perda
  semântica para o efeito do NDF — o prazo relevante é o termo da conservação
  intermédia —, mas é o teste mais exigente que o modelo enfrentou e fica
  documentado como tal.

### Generalização da avaliação arquivística e separação custódia ↔ RGPD (2026-08-14)

Duas alterações **incompatíveis**, absorvidas em `1.0.0` por a especificação
estar em nível 1 — Draft, sem revisão pública aberta e sem utilizadores
externos (ADR-007). Fecham o risco R11 e retiram do ROADMAP v2.0.0 o item de
generalização de `avaliacao`. Detalhe em ADR-015, ADR-016 e
`docs/design/NDF-AVALIACAO-GENERALIZATION.md`.

O bloco `avaliacao` obrigava qualquer produtor a exprimir a decisão de
avaliação no vocabulário do MEG/DGLAB — PCA, Destino Final, Lista Consolidada —
o que tornava o NDF, na prática, um formato da Administração Pública
portuguesa. O levantamento comparativo sobre PT, FR, NL, DE e UK/CoE/Comissão
Europeia mostrou que o modelo português é uma instância de um padrão europeu
comum (`gatilho + prazo + ação de destino + instrumento`), e não uma
idiossincrasia: PT e FR são praticamente isomórficos, incluindo o valor de
amostragem. A generalização é, por isso, de vocabulário — a estrutura mantém-se
no core.

- adicionado: `avaliacao.perfil` (obrigatório) — perfil de avaliação
  arquivística aplicável, enum aberto com padrão
  `^([a-z]{2}-[a-z0-9-]+|generic)$`. As regras de sintaxe de cada jurisdição
  passam a viver no schema do perfil, em `specs/registry/profiles/`, que
  **DEVE viajar dentro do `.ndfpkg`** (NDF-PKG-008), pelo mesmo mecanismo dos
  schemas de tipo documental (ADR-014);
- adicionado: perfis `pt-dglab` — que preserva integralmente as regras
  portuguesas atuais, incluindo a correspondência de instrumento entre
  `classificacao_ref` e `instrumento_ref` — e `generic`, sem restrições
  jurisdicionais;
- adicionado: `destino_final: "a_determinar"`, com `autoridade_avaliacao`
  obrigatório quando usado e proibido nos restantes casos. Cobre os sistemas em
  que a decisão de destino não compete ao produtor mas à autoridade
  arquivística — `Anbietung`/`Bewertung` na Alemanha, `voorlopig te bewaren` e
  `nader te bepalen` nos Países Baixos, `review` no Reino Unido e nas
  instituições europeias. Antes desta alteração, um produtor nesses sistemas
  não conseguia produzir um NDF-core honesto;
- alterado: `tipo_classificacao_ref` → `classificacao_ref`;
  `instrumento_avaliacao_versao_ref` → `instrumento_ref`;
  `prazo_conservacao_administrativa` → `prazo_conservacao`. Renomeados apenas
  os campos cujo nome é um termo legal português; `destino_final` e
  `forma_contagem` mantêm-se, por traduzirem diretamente para os equivalentes
  das outras jurisdições;
- adicionado: `metadados.entidade_responsavel` (obrigatório sempre) —
  responsável pela **custódia do registo**. É o conceito que a SPEC já
  descrevia, mas alojado no campo errado;
- alterado: `categorias_dados_pessoais`, `base_legal_conservacao` e
  `responsavel_tratamento` saem do topo de `metadados` e passam ao bloco
  `metadados.protecao_dados`, **obrigatório se e só se**
  `contem_dados_pessoais: true` e **proibido** caso contrário. Antes, o formato
  exigia declarar um responsável pelo tratamento RGPD mesmo em documentos que
  afirmavam não conter dados pessoais, e a incoerência inversa não era
  detetável (ADR-016);
- adicionado: casos de conformidade `avaliacao-perfil-generico` (documento
  não-PT com `a_determinar`), `avaliacao-sem-perfil`,
  `avaliacao-a-determinar-sem-autoridade` e
  `protecao-dados-sem-dados-pessoais`;
- corrigido: `mismatched-instrument` e `invalid-tipo-classificacao-ref`
  (renomeado para `invalid-classificacao-ref`) eram **testes vácuos** — ambos
  omitiam a declaração de origem (§2.2.1) e o primeiro tinha ainda um `ndf_id`
  não conforme, pelo que eram rejeitados por erro de schema antes de a
  violação que pretendiam cobrir chegar a ser avaliada. Defeito pré-existente,
  detetado ao migrá-los, e ponto de partida para a entrada seguinte.

### Casos negativos verificados pelo motivo da rejeição (2026-08-14)

O runner comparava apenas aceite/rejeitado, pelo que um caso negativo rejeitado
por um defeito acidental era indistinguível de um caso que exercesse a regra
documentada — e continuaria a passar mesmo que essa regra fosse removida da
especificação. Detetado ao migrar dois casos de `avaliacao`; a instrumentação
mostrou que o problema era mais extenso.

- adicionado: campo `_expected_match` em todos os 46 casos de
  `conformance/{ndf,ncrtf,ndt}/invalid/` — expressão regular que **DEVE**
  corresponder a pelo menos um dos erros reportados. `tools/validate.py` trata
  como falha a ausência do campo e a ausência de correspondência, mesmo quando
  o caso é corretamente rejeitado;
- adicionado: SPEC.md §9.4.1, que fixa a regra e delimita o que é exigível a
  uma implementação alternativa — rejeitar os casos é obrigatório, reproduzir
  as mensagens do runner de referência não é;
- corrigido: 17 casos NDF sem declaração de origem, 7 com `ndf_id` malformado
  e 2 com `documento` incompleto face ao schema do tipo — todos rejeitados por
  motivo alheio ao que documentavam;
- corrigido: 3 dos 5 casos negativos NDT (`duplicate-page-id`,
  `non-positive-dimension`, `unknown-page-ref`) omitiam
  `sequencia[].repeticao`, pelo que falhavam no schema sem nunca chegar à
  verificação semântica que existiam para cobrir;
- melhorado: `fmt_schema_error` passa a produzir mensagem legível para as
  proibições condicionais `if/then/else` — antes despejavam o objeto validado
  inteiro, o que as tornava inúteis como evidência.

### Proveniência de sistema produtor e imputação jurídica (2026-08-13)

Motivada por uma categoria não coberta: documentos gerados por sistemas
determinísticos, sem autor humano material — liquidações de impostos,
notificações, certidões automáticas. O NDF não sabia registar que sistema os
produziu, nem quem responde juridicamente por eles, sendo esta última uma
menção obrigatória (CPA art. 151.º/1/a; CPPT art. 36.º/2) e condição do
exercício dos meios de defesa (CPPT art. 66.º/2). `ndf_version` mantido em
`1.0.0` — ver ADR-007. Detalhe em ADR-012, ADR-013 e ADR-014.

- adicionado: campo de topo `proveniencia_sistema` (array) — sistema ou cadeia
  de sistemas determinísticos que produziu o conteúdo, com `sistema`
  (nome/identificador/versão), `componente`, `gerado_em` e referências
  externas opcionais de regra, *build* e configuração; **ordem cronológica
  normativa**, por JCS preservar a ordem dos arrays e esta entrar no
  `payload_hash` (ADR-013);
- adicionado: campo de topo `imputacao` (array) — quem responde juridicamente
  pelo documento e a que título, num vocabulário que cobre o regime do ato
  administrativo (`competencia_propria`, `delegacao`, `subdelegacao`) e o
  regime declarativo (`declaracao_propria`, `aceitacao_expressa`,
  `efeito_legal`), com condicionais por título; mais do que uma entrada
  significa co-titularidade — ato conjunto ou declaração conjunta — nunca
  cadeia de delegação (ADR-012);
- adicionado: bloco opcional `imputacao[].autenticacao` (`meio`,
  `nivel_garantia` em terminologia eIDAS) — regista o facto que fundamenta a
  imputação numa submissão por canal autenticado ou por atendimento
  presencial. Por entrada e não por documento, porque a lei exige autenticação
  de ambos os sujeitos passivos numa declaração em tributação conjunta;
- adicionado: **invariante de origem** (§2.2.1) — todo o NDF DEVE declarar
  pelo menos uma origem identificável do conteúdo (humana, de sistema ou de
  IA). Expresso por `anyOf` no JSON Schema, portanto aplicado por qualquer
  validador Draft 2020-12 sem código adicional;
- alterado: `participantes` passa a índice **exclusivamente de pessoas
  singulares** — removido o campo `tipo` e os papéis `sistema_tecnico`
  (um sistema não participa, produz), `entidade_produtora` (redundante),
  `validador` e `aprovador` (estado de workflow — encerra `LACUNAS.md` L10);
  acrescentados o papel `responsavel_tecnico` e o bloco `qualificacao`
  (`{ tipo, identificador }`), para quem responde tecnicamente em nome próprio
  com qualidade profissional que é condição de validade do documento
  (contabilista certificado, ROC, advogado, autor de termo de
  responsabilidade);
- alterado: `metadados.tipo_documento_ref` aceita a extensão qualificada
  `ext.<entidade>.<tipo>@<versao>`, com o schema do tipo a viajar no `.ndfpkg`
  em `schemas/` — mantém o registo canónico reservado a formas documentais
  transversais, sem perder validação estrutural (ADR-014);
- corrigido: a resolução do schema do tipo passa a preferir o pacote ao
  registo, tornando o `.ndfpkg` genuinamente autovalidável; e um
  `tipo_documento_ref` não resolúvel passa a ser **erro** — antes era saltado
  em silêncio, deixando `documento` sem validação nenhuma;
- adicionado: fronteira normativa entre `proveniencia_sistema` e
  `proveniencia_ia` — qualquer componente não determinístico pertence a
  `proveniencia_ia`, sem exceção, para que a escolha de campo não permita
  contornar o `revisao_humana.estado` obrigatório;
- adicionado: 12 requisitos normativos (`NDF-PROD-015` a `019`,
  `NDF-READ-014` a `020`, `NDF-PKG-007`);
- adicionado: 4 casos de conformidade válidos e 9 inválidos; exemplo de pacote
  `specs/ndf/examples/liquidacao-irs-automatica/`;
- adicionado: ADR-012, ADR-013 e ADR-014; notas de superveniência em ADR-005 e
  ADR-006;
- adicionado: `LACUNAS.md` L12 — duplicação entre `referencia_externa` e
  `evidencia_ref`, deixada deliberada e agendada para v1.1.0.

### Estabilização NDF — relações, assinaturas, participantes e proveniência de IA

Preparação de PR-001 (ver `docs/normalization/REVIEW-LOG.md`). `ndf_version`
mantido em `1.0.0` — ver ADR-007. Detalhe completo em
`docs/design/NDF-STABILIZATION-PROPOSAL.md` e
`docs/reports/NDF-STABILIZATION-REPORT.md`.

- adicionado: bloco opcional `relacoes` ao NDF-core — relações verificáveis
  entre documentos (`ndf_id` + `payload_hash` do alvo), vocabulário fechado
  de 11 tipos, mapeamento informativo a PROV-O (ADR-002);
- adicionado: tipo de documento `parecer@1.0.0` ao registo, distinto de
  `informacao-tecnica` (ADR-003);
- adicionado: `payload_hash` opcional a `despacho.sobre[]`, para coerência
  com `relacoes[]` quando ambos presentes;
- alterado: material de assinatura (`timestamps`, `validation_material`)
  passa de campo global do envelope para campo de cada entrada de
  `assinaturas[]` — unidade de prova autocontida; acrescentados
  `assinatura_id` (obrigatório), `papel` e `ordem` opcionais (ADR-004);
- adicionado: bloco opcional `participantes` ao NDF-core, distinto de
  `assinaturas[].signatario` (ADR-006);
- adicionado: bloco opcional `proveniencia_ia` ao NDF-core — evidência
  proporcional de utilização de sistemas de IA, com estado de revisão
  humana obrigatório por intervenção (ADR-005);
- alterado: padrão de hash em `payload_hash`, `hash_anterior`,
  `event_hash`, `previous_event_hash`, `hash_sha256` (manifest e anexos do
  registo) generalizado de `^sha256:[0-9a-f]{64}$` para
  `^[a-z][a-z0-9-]*:[0-9a-f]+$` — agnóstico de algoritmo, sem quebra de
  compatibilidade (aceita estritamente mais do que antes);
- adicionado: `docs/normalization/AI-PROVENANCE-GUIDANCE.md`;
- adicionado: `specs/ndf/examples/informacao-parecer-despacho/` — três NDF
  autónomos (informação, parecer, despacho) ligados por `relacoes[]`, com
  hashes reais recalculáveis;
- adicionado: 6 novos casos de conformidade NDF (1 válido, 5 inválidos) e um
  novo vetor negativo de pacote (`PKG-NEG-008-assinatura-sem-id`);
- adicionado: ADR-002 a ADR-007.

### Revisão adversarial pós-estabilização — `LACUNAS.md`

Ver `LACUNAS.md` para a análise completa e `docs/reports/CURRENT-STATE-ASSESSMENT.md`
para o histórico de decisões.

- adicionado: SPEC.md §1.5 "Confidencialidade e controlo de acesso" — limite
  normativo explícito: o NDF não define nem garante cifra, controlo de
  acesso ou gestão de credenciação; `classificacao_seguranca` é sinal
  descritivo, a proteção é responsabilidade do sistema de custódia;
- adicionado: `docs/normalization/NDF-INFORMATIVE-GUIDANCE.md` — secção
  "Confidencialidade e controlo de acesso", incluindo pontos a considerar
  na implementação do core-documental (não normativo);
- decisão registada: mitigação de fuga de metadados por `relacoes[]` em
  documentos classificados fica fora de âmbito do NDF — resolvida por
  proteção do artefacto ao nível do core-documental, não por mecanismo do
  formato (`LACUNAS.md` L2);
- adicionado: SPEC.md §2.11.5 "Segurança e privacidade do grafo de
  relações" — relação é afirmação unilateral, não implica reconhecimento
  do alvo (A1/L1); deteção de ciclos é responsabilidade do verificador,
  não do schema (A3/L3);
- adicionado: nota em SPEC.md §4.4.1 — correspondência `papel`↔exigência
  legal de quem assina não é garantida pelo formato (A4/L7);
- adicionado: SPEC.md §2.12.3 — `participante_ref` é referência externa
  não resolvida pelo NDF, por desenho (A5/L9);
- adicionado: SPEC.md §2.12.4 — `validador`/`aprovador` descrevem estado
  de workflow; uso desencorajado fora de sistemas que já os tratem como
  tal, mantidos no enum sem alteração incompatível (A6/L10);
- adicionado: `tools/validate.py` `check_ndf_advisories` — aviso (não
  erro) quando `documento.sobre[]` e `NDF-core.relacoes` divergem (A7/L5);
- adicionado: `delegacao_ref` opcional em `parecer.autor` e
  `informacao-tecnica.autor`, mesmo padrão de `despacho.decisor` (A8/L8).

### Extensibilidade e fecho de `LACUNAS.md` (A9, A10)

- adicionado: extensão qualificada `ext.<entidade>.<tipo>` para
  `relacoes[].tipo`, além do vocabulário base fechado — alteração aditiva
  (`oneOf` no schema), sem quebra de compatibilidade; SPEC.md §2.11.7;
  ADR-008 (A9/L4);
- adicionado: 2 novos casos de conformidade NDF (1 válido com extensão
  qualificada, 1 inválido com extensão malformada) — suite passa a 58/58;
- decidido, e registado em ADR-009: `ndf_id` mantém-se UUID v4 opaco, sem
  espaço de nomes por entidade produtora — a necessidade já estava
  resolvida por `metadados.entidade_produtora`; alterar o identificador
  acoplaria-o a uma identidade organizacional mutável, para um ganho sem
  benefício real (A10/L6). Clarificação normativa acrescentada a SPEC.md
  §2.3, sem alteração de schema;
- `LACUNAS.md` fecha com os dez pontos resolvidos: sete implementados,
  um fechado por decisão de não-alteração, dois fora de âmbito.

### Separação entre conformidade NDF e Perfil de Ciclo de Vida NORMORDIS (ADR-010)

Revisão externa ao estado do repositório identificou que `SPEC.md`
misturava requisitos de formato com requisitos operacionais de gestão de
ciclo de vida documental, criando uma barreira de adoção desnecessária
para sistemas com o seu próprio modelo de custódia.

- adicionado: `docs/architecture/ADR-010-separacao-conformidade-perfil-ciclo-vida.md`;
- adicionado: nova secção "Perfil de Ciclo de Vida NORMORDIS (opcional)"
  em SPEC.md §9.5, com requisitos próprios `CUST-REQ-001..003` — reclassifica
  o requisito de log de auditoria que estava indevidamente em `NDF-PROD-010`;
- alterado: `NDF-PROD-010` deixa de exigir log de custódia; passa a exigir
  persistência atómica de `payload_bytes` e envelope (mantém a mesma ID,
  conteúdo diferente — sem renumeração);
- alterado: SPEC.md §2.4 (nova nota de âmbito), §5.2 passo 8 (dividido em
  requisito de formato + requisito de perfil), §2.10, §4.6.1, §4.6.4 e
  glossário — linguagem sobre `nivel_assinatura` e `validation_code`
  ajustada para não sugerir que o NDF decide juridicamente o nível de
  assinatura exigido, nem que depende de um serviço específico;
- alterado: `docs/architecture/ARCHITECTURE.md` §2.1, §3 — "registo de
  custódia" deixa de ser apresentado como parte constitutiva do NDF;
  passa a Perfil de Ciclo de Vida NORMORDIS opcional;
- alterado: `tools/build_requirements_index.py`, `tools/audit_normative.py`
  — reconhecem a família `CUST-REQ-*` (54 IDs únicos, antes 51);
- atualizado: `docs/normalization/TRACEABILITY.md` — família `CUST-REQ-*`
  com evidência real, já não placeholder.

### Correções de seguimento pós-revisão

- alterado: SPEC.md §2.12.1 e §2.12.3 — `participantes` deixa de ser descrito
  como servindo "auditoria", termo que após a ADR-010 podia ser lido como
  *audit trail* operacional (Perfil de Ciclo de Vida). Passa a "consulta,
  proveniência e interoperabilidade documental";
- alterado: `.github/workflows/validate.yml` — `actions/checkout`,
  `actions/setup-python` e `actions/setup-node` atualizadas para v7, e o
  runtime Node dos verificadores JS de 20 para 24. Resolve os avisos de
  depreciação de Node.js 20 emitidos pelo GitHub Actions.

### Revisão adversarial pré-RC — 16 achados resolvidos (`NDF-PRE-RC-REVIEW.md`)

Revisão dirigida a contradições, redundâncias e requisitos impossíveis de
implementar, em vez de novas funcionalidades. Relatório completo em
`docs/reports/NDF-PRE-RC-REVIEW.md`.

**Alteração arquitetural (ADR-011):**

- removido: `versao_anterior` e `hash_anterior` do envelope. A sucessão
  documental passa a ser representada exclusivamente por
  `relacoes[{tipo: "substitui"}]` no NDF-core assinado — um facto, um sítio,
  coberto pela assinatura. Resolve em cascata a contradição do manifesto
  (F3), a hierarquia normativa invertida (F6) e a ausência total de
  cobertura de teste do mecanismo removido (F8);
- alterado: SPEC.md §6 reescrita — sucessão é uma relação entre documentos
  autónomos e imutáveis (`A continua a existir; B substitui A`), não
  versionamento interno.

**Contradições SPEC↔schema corrigidas:**

- corrigido: SPEC.md §2.4.2 — o exemplo e a tabela do log de custódia
  descreviam um modelo de dados que falhava 9 validações contra o
  `custody-event.schema.json` que a própria cláusula torna obrigatório
  (só `ndf_id` coincidia). Alinhados ao schema, com a semântica antiga
  (`motivo`, `instrumento_legal`) mapeada para `details` (F1);
- corrigido: SPEC.md §8.2 — o exemplo do `manifest.json` omitia três campos
  obrigatórios (`estado`, `nivel_assinatura`, `validation_code`) (F2);
- corrigido: SPEC.md §2.10.3 — a tabela ainda tratava `timestamps` e
  `validation_material` como campos de topo do envelope, contra a ADR-004
  (F4); mesma correção em §6.2 (F5) e na referência de §4.1, que apontava
  para §4.4.2 em vez de §4.4.1 (F12).

**Simplificações e clarificações:**

- alterado: o tombstone de eliminação (§2.4.3) deixa de ser um artefacto
  normativo próprio sem schema; passa a **evento terminal** no log de
  custódia (`event_type: "eliminado"`, evidência em `details`), reutilizando
  a estrutura já existente (F7);
- adicionado: SPEC.md §2.12.3 — as três noções de autoria
  (`documento.autor`, `participantes[].papel`, `assinaturas[].papel`) são
  declaradas semanticamente distintas, com regra de coerência, sem impor
  uma hierarquia de precedência artificial (F10);
- documentados: campos de schema que existiam sem prosa normativa —
  `assinado_em`, subcampos de `timestamps`, `validation_material` e
  `revogacao`, e `finalidade_detalhe` (F11).

**Guardrails de CI (novo — impede a reincidência do padrão):**

- adicionado: `tools/check_spec_coherence.py` — valida os blocos JSON
  normativos da SPEC contra os schemas, verifica que todo o campo de schema
  está documentado, que as referências `§X.Y` resolvem, que enums
  deliberadamente duplicados não derivam (F16), e que propriedades removidas
  por ADR não reaparecem;
- adicionado: `tools/build_conformance_index.py` — gera `conformance/INDEX.md`
  a partir dos ficheiros reais. O README de conformidade documentava 14 de
  28 casos por ser mantido à mão (F15); o índice passa a ser gerado e
  verificado em CI;
- alterado: `.github/workflows/validate.yml` — ambas as ferramentas ligadas
  ao pipeline.

### Resíduos de fronteira NDF/Perfil de Ciclo de Vida (revisão de consistência)

Revisão externa ao ADR-010 encontrou três resíduos onde a separação
formato/perfil não tinha sido aplicada até ao fim:

- corrigido: SPEC.md §2.10.4 — a linha de `conservacao_permanente` dizia
  "custódia append-only/WORM e auditoria continuam obrigatórias", em
  tensão direta com §9.5 (perfil opcional). Reescrita para tornar a
  dependência do perfil explícita;
- corrigido: SPEC.md §4.4.2 — separado o requisito de formato/pacote
  (preservar byte a byte a assinatura original, timestamps e material de
  validação) do requisito específico do Perfil de Ciclo de Vida NORMORDIS
  (registar renovação criptográfica como evento append-only no log de
  custódia);
- suavizado: SPEC.md §3.2.1 e §3.5 — "`tipo_classificacao_ref` é resolvido
  automaticamente... nunca introduzido manualmente" e equivalente para
  `prazo_conservacao_administrativa`/`destino_final` eram regras de
  implementação do sistema produtor apresentadas como requisito do
  formato; passam a **RECOMENDA-SE**, mantendo como requisito apenas que o
  valor final seja válido, coerente e imutável;
- registada em `ROADMAP.md` (v2.0.0): nota sobre generalização futura do
  bloco `avaliacao` — hoje semanticamente acoplado ao modelo arquivístico
  português (PCA/DF/DGLAB), relevante para adoção por outras
  administrações europeias. Sem ação prevista para 1.0, apenas registo da
  questão. **Superado em 2026-08-14**: a generalização foi antecipada para
  1.0.0 — ver a entrada no topo deste ficheiro e ADR-015.

### Harmonização editorial e de normalização

- estado comum `Draft — Revisão pública` para NDF, NDT e NCRTF;
- política editorial, língua normativa e estrutura documental comum;
- regras de consenso, votação, recurso, conflitos de interesse e IPR;
- referências normativas controladas e migração de RFC 4122 para RFC 9562;
- alegações jurídicas reformuladas como objetivos técnicos condicionados;
- terminologia e ortografia portuguesa harmonizadas;
- referências NDF/NDT harmonizadas em `versao_ndt`, `documento.corpo` e no
  âmbito explícito de `pdf_hash`;
- matriz de rastreabilidade expandida com prefixos estáveis de requisitos.
- auditoria automática de 45 IDs e inventário de declarações subordinadas;
- sete vetores negativos de pacote `.ndfpkg`;
- corpus semântico NDT com nove casos estáveis;
- dossier de revisão pública autocontido e verificado por hashes;
- gates editoriais e normativos integrados na CI.

### Correção do estado editorial e adiamento de PR-001 (2026-08-11)

Origem: avaliação de prontidão para debate público e candidatura NGI, em
`docs/reports/READINESS-ASSESSMENT.md` (achado `R1`, decisão D1). O estado
declarado descrevia uma revisão pública que nunca chegou a ser aberta.

- alterado: estado editorial de `Draft — Revisão pública` (nível 2 de
  `NORMALIZATION.md`) para `Draft — revisão pública por abrir` (nível 1) em
  `specs/ndf/SPEC.md`, `specs/ndt/SPEC.md`, `specs/ncrtf/SPEC.md`,
  `specs/registry/SPEC.md`, `specs/portal/SPEC.md` e
  `specs/ndt/RENDERER-CONFORMANCE.md`;
- alterado: PR-001 passa a estado `adiado` em
  `docs/normalization/REVIEW-LOG.md`; a janela proposta 2026-07-01 → 2026-08-15
  é dada por caduca sem comentários recebidos e sem commit fixado; o critério
  de abertura passa de temporal a **condição de evidência** — `normordis-pdf`
  a produzir um documento a partir de NDF + NDT, reproduzível por terceiros;
- alterado: secção "Estado" do `README.md` declara explicitamente que nenhum
  período de revisão está aberto e que nenhum dos oito gates externos de
  `READINESS.md` está cumprido;
- alterado: `tools/check_publication_profile.py` valida contra um conjunto
  `ALLOWED_STATES` em vez de exigir literalmente `Draft — Revisão pública` —
  a ferramenta tornava obrigatório por CI o estado incorreto; mantém-se como
  gate real, falhando se nenhum estado admissível for declarado;
- adicionado: `docs/reports/READINESS-ASSESSMENT.md` — documento vivo com as
  decisões de sequenciamento D1–D7, comparação NDF vs. abordagem tradicional
  (12 vantagens, 10 desafios) e achados `R1`–`R13` de estado rastreável;
- adicionado: secção de decisões de sequenciamento e Fase 1D (evidência de
  assinatura CAdES) em `ROADMAP.md`;
- alterado: `docs/roadmap/NGI-MVP-2026.md` marcado como parcialmente superado,
  distinguindo o que caducou (datas dos marcos, centralidade do XML) do que se
  mantém válido.

## [2026-06-20] — NDT v2.0.0 e harmonização NDF/NCRTF

### NDT

- formato declarativo de layout sem motor de regras de negócio;
- `versao_ndt` substitui `versao_impresso`;
- layout de fluxo, campo de assinatura e estilos globais;
- mapeamento NCRTF ↔ NDT;
- suporte estrutural a PDF/UA-2 e PDF/A-3;
- exemplos e suite de conformidade NDT.

### NDF / NCRTF

- harmonização do mapeamento tipográfico;
- revisão de consistência entre schemas e exemplos.

## [2026-06-18] — NCRTF v2.0.0 e NDF v1.0.0

### NCRTF

- listas unificadas, tabelas simplificadas e `font_family` explícito;
- nós `link`, `hard_break` e `blockquote`;
- novas marcas e regras de canonicalização.

### NDF

- estrutura NDF-core, envelope, avaliação arquivística, finalização,
  proveniência e versionamento.

### Repositório

- suites de conformidade NDF e NCRTF;
- schemas JSON para NDF, NDT, NCRTF, envelope, manifesto e registo;
- validador de referência;
- ADR sobre a escolha de JSON.
