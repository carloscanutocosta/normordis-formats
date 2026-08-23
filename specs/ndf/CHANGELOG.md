# Histórico NDF

## Não publicado

### Documentos multilingues (2026-08-23)

- **acrescentado: `metadados.idiomas_autenticos`** e SPEC §2.7.7. Fecha `L14`.
  `idioma` declarava uma língua «principal», o que é verdadeiro para a
  generalidade dos documentos e falso para aqueles cujas versões têm **igual
  força jurídica** — legislação da União, tratados, atos de Estados
  plurilingues. Nesses, eleger uma principal afirma uma hierarquia que o regime
  não estabelece: mesma família de falsidade forçada que levou a
  `origem_nao_identificavel` (ADR-023) e a §2.8.1.1;
- o bloco é **opcional** e `idioma` mantém-se obrigatório, pelo que nenhum
  documento existente é invalidado (ADR-007). Quando presente, **DEVE** conter o
  valor de `idioma` — regra cruzada verificada em `tools/validate.py`, por o JSON
  Schema não conseguir exigir que um array contenha o valor de outro campo;
- uma tradução **não** igualmente autêntica continua a ser outro documento,
  ligado por `relacoes[]`. Declará-la aqui afirmaria uma autenticidade que o
  produtor não tem — o mesmo teste de identidade que separa um anexo de um
  documento autónomo (§2.8.1.3);
- vetores `idiomas-igualmente-autenticos.json` e
  `idiomas-autenticos-sem-principal.json`.


### Fronteiras da transferência decididas (2026-08-23)

`D-XFER-1` a `D-XFER-3` de
[`NDF-CONJUNTO-DE-TRANSFERENCIA.md`](../../docs/design/NDF-CONJUNTO-DE-TRANSFERENCIA.md)
passam de pontos em aberto a decisões. Só a terceira toca artefacto existente, e
recai sobre o Perfil de Ciclo de Vida, que é opcional (ADR-010) — o NDF-core não
é alterado.

- **acrescentado: `event_type: "recebido"`** em `custody-event.schema.json` e na
  §2.4.2. Um documento que entra em custódia vindo de outra entidade não foi
  capturado nem finalizado por quem o recebe: já existe, com identidade,
  assinatura e história. Registá-lo como `capturado` seria uma declaração falsa
  da mesma família da que §2.8.1.1 acabou de proibir ao separar submeter de
  produzir;
- **acrescentado: as cadeias de custódia são por custodiante, não globais**
  (§2.4.2). Era o modelo de facto — `check_custody.py` sempre validou uma cadeia
  isolada — e estava por dizer. A cadeia do recetor abre em `sequence` 0 com
  `previous_event_hash` `null` e **não** continua a do transmitente, que ele não
  detém e não poderia encadear sem falsificar. O que liga custodiantes é
  documental, nunca criptográfico; um leitor com uma cadeia tem a história
  **desse** custodiante, e não deve apresentá-la como a história do documento;
- **acrescentado:** `conformance/custody/cadeia-do-recetor.json`, no CI, e o
  `details` recomendado para `recebido` (`transferencia_ref`, `transmitente`,
  referência à aceitação).

Decidido sem alteração a nenhum artefacto: **D-XFER-1** — o conjunto declara
`referencias_externas[]`, recomputável pelo recetor a partir das unidades, e não
estrutura intelectual; **D-XFER-2** — a evidência de custódia declara uma
política de extração aplicada uniformemente, em vez de uma seleção documento a
documento, com `finalizado` obrigatório quando existe.


### Anexos de documento nativo (2026-08-23)

- **corrigido: um documento nativo não conseguia transportar os seus anexos num
  pacote conforme.** `oficio` e `informacao-tecnica` declaravam `anexos[]` — um
  segundo vocabulário para binários, com `hash_sha256` em vez de `sha256`, sem
  `media_type`, sem `tamanho` e sem `id` — que `NDF-PKG-009` não reconhecia. O
  efeito verificado: um ofício que **transportasse** o anexo em `anexos/` era
  **rejeitado**, e um que o **omitisse** era **aceite**. O formato empurrava para
  o pacote incompleto, e contradizia a §8.1, que já afirmava não haver
  «categoria de componente documental omissível»;
- **alterado: `anexos[]` é retirado dos dois tipos e substituído por
  `componentes[]`**, que passa a ser afirmado em §2.8.1 como mecanismo **único** de
  componentes binários, disponível a qualquer schema de tipo. **Incompatível**,
  absorvida em 1.0.0 antes de publicação; sem instâncias a migrar, por o campo
  nunca ter sido exercitado por NDT, exemplo ou vetor. Ver ADR-025;
- **acrescentado: §2.8.1.3 — anexos de um documento nativo**, com o teste de
  identidade documental que separa `componentes[] papel:"anexo"` de NDF autónomo
  ligado por `relacoes[{tipo:"anexa"}]`, e a nota de âmbito de ADR-022: o formato
  garante que os anexos declarados existem, estão íntegros e viajam — não que
  sejam os certos nem que estejam completos;
- **acrescentado:** o exemplo `ndfpkg-example` passa a transportar um anexo real,
  e os vetores `PKG-NEG-015` (anexo declarado e ausente) e `PKG-NEG-016`
  (ficheiro em `anexos/` não declarado) exercitam o fecho nos dois sentidos na
  via nativa;
- **acrescentado:** guarda **C7** em `tools/check_spec_coherence.py` — a definição
  de `componentes` é duplicada entre schemas de tipo por estes serem autocontidos
  por desenho, e C7 rejeita tanto `items` divergente como o reaparecimento de
  vocabulário paralelo. Foi a ausência desta guarda que deixou a incoerência
  nascer.


### Ronda de fronteira formato ↔ direito material (2026-08-23)

Revisão externa observou que o princípio de ADR-022 — o formato representa, o
produtor decide — estava correto no corpo da especificação mas era ultrapassado
em pontos concretos, sobretudo em descrições de schema e em exemplos. Correções
de fronteira semântica; nenhuma altera a arquitetura.

- **alterado: `metadados.protecao_dados.base_legal_conservacao` passa de escalar
  a par `{regime, base}`**, com `fundamento_ref` opcional (nova §1.4.1). O enum
  fechado anterior codificava o artigo 6.º do RGPD dentro do NDF-core — e
  listava quatro dos seis fundamentos, pelo que documentos assentes nos
  restantes não eram exprimíveis. Mesma operação e mesmo fundamento de
  `classificacao_seguranca` em 2026-08-15; ver adenda a ADR-017. **Incompatível**,
  absorvida em 1.0.0 antes de publicação;
- **corrigido: descrição de `nivel_assinatura` no schema** dizia «minimum
  electronic signature level *required by the legal nature of the act*»,
  contradizendo §2.10, que já a descrevia como determinação do produtor. Passa a
  declaração do produtor, alinhada com §2.10.2;
- **alterado: §2.10.1 deixa de dar exemplos de tipos de ato.** A coluna associava
  ofícios a `avancada` e contratos públicos a `qualificada`; marcada como
  ilustrativa ou não, seria copiada como classificação jurídica, que §2.10.2
  atribui expressamente à entidade produtora. A omissão passa a ser explicada;
- **corrigido: §2.15.4 fundamentava regras de formato em conclusões jurídicas** —
  «o acesso autenticado desempenha a função que a assinatura manuscrita
  desempenhava», «a identificação ao balcão e a autenticação digital produzem o
  mesmo efeito jurídico», «a imputação é idêntica nos três casos». As **regras
  mantêm-se todas** — não há mecanismo de gradação, e um leitor NÃO DEVE derivar
  imputação mais fraca de `nivel_garantia` mais baixo —, mas passam a ser
  fundamentadas no âmbito do formato e na semântica dos campos. As mesmas
  afirmações foram retiradas das descrições de `autenticacao.meio` e
  `autenticacao.nivel_garantia` no schema;
- **acrescentado: §2.8.1.1 — submeter não é produzir.** Um produtor NÃO DEVE
  declarar o submissor como `autor`, `coautor` ou `decisor` apenas por ele ter
  submetido o documento; não havendo fundamento para a autoria, aplica-se o
  quarto modo de §2.2.1 (ADR-023), que coexiste com `proveniencia_submissao`. O
  eixo da responsabilidade jurídica é `imputacao` (§2.15);
- **acrescentado: §2.8.1.2 — função do NDT num documento capturado.**
  `ndt_version_ref` designa aí a representação da **captura**, não um template
  capaz de reconstruir o componente. Um leitor NÃO DEVE apresentar a saída do NDT
  como sendo o documento recebido;
- **corrigido: `proveniencia_submissao.autenticacao` e
  `imputacao[].autenticacao.meio` usavam vocabulários diferentes** para o mesmo
  conceito (`chave-movel-digital` vs `chave_movel_digital`). Unificados no
  separador usado pelo resto do NDF-core;
- **corrigido: exemplo `captura-requerimento`** declarava o submissor como
  `autor` e `tipo_equivalente: "oficio@1.0.0"` num requerimento. Passa a exercer
  os três blocos distintos — submissão, origem não apurável, imputação — e omite
  `tipo_equivalente`, que só se declara quando determinável;
- **corrigido: `conformance/custody/captura-chain.json`** declarava um
  `payload_hash` que não era o do pacote que o `ndf_id` identifica, com um
  `validation_code` derivado de outro. Sincronizado com o exemplo.
- **corrigido: schemas embebidos nos pacotes de exemplo estavam desatualizados.**
  Nove cópias em três pacotes (`ndf-core`, `ndt`, `custody-event`) declaravam o
  `$id` do schema publicado com conteúdo anterior — o `ndf-core` embebido é
  anterior a ADR-023 e rejeitava `origem_nao_identificavel`. Um pacote existe
  para ser verificável sem rede; uma cópia divergente entrega ao verificador
  outro contrato com o mesmo identificador. Sincronizadas, e acrescentada a
  guarda **C6** em `tools/check_spec_coherence.py` para que não voltem a
  divergir em silêncio.

### Acrescentado

- **§2.8.1 — componentes binários referenciados por hash.** A proibição de §2.8
  passa a recair sobre bytes embutidos, não sobre a referência a eles: um schema
  de tipo documental PODE declarar componentes por digest, mantendo os bytes fora
  do NDF-core. Decisão de âmbito registada em `ROADMAP.md` (2026-08-20); o
  NDF-core não é alterado e `ndf_version` mantém-se em `1.0.0`. Ver ADR-020 e
  ADR-021.
- **§2.8.2 — divergência entre declaração e componente.** O componente é
  autoritativo quanto ao conteúdo do ato; o NDF quanto a identidade, custódia e
  classificação. Nenhum corrige o outro.
- **§4.5.1 — assinaturas contidas em componentes.** `nivel_assinatura` não se
  deriva delas; os bytes assinados nunca se reescrevem; o material de validação
  congela-se na captura; a ordem assinar → hash do assinado → declarar →
  finalizar é normativa.
- **§8.1** — diretórios `original/`, `representacoes/`, `anexos/` e
  `evidencias/` na composição do `.ndfpkg`. A correspondência com a declaração
  faz-se pelo digest e nunca pelo caminho.
- **`NDF-PROD-020`, `NDF-PROD-021`, `NDF-PROD-022`** — não reescrever
  componentes; não declarar localização de armazenamento; não derivar
  `nivel_assinatura` de assinatura contida.
- **`NDF-READ-021`, `NDF-READ-022`, `NDF-READ-023`** — não apresentar a projeção
  do NDT de um capturado como sendo o documento; não apresentar assinatura de
  componente como assinatura do NDF; resolver componentes por digest.
- **`NDF-PKG-009`** — coerência entre `documento.componentes[].sha256` e
  `manifest.inventario`, **fechada nos dois sentidos**: nenhum componente
  declarado sem ficheiro, nenhum ficheiro em diretório de papel sem componente
  declarado. É a única junta verificável nova.
- Exemplo `specs/ndf/examples/captura-requerimento/` e vetores `PKG-NEG-010` a
  `PKG-NEG-014`.
- **`event_type: "capturado"`** no log de custódia — entrada dos componentes em
  custódia, anterior à finalização. `details` recomenda `componentes`, `canal` e
  `recebido_em`; a verificação periódica de fixidez usa `verificado` com
  `componentes_verificados` (§2.4.2).
- **§2.4.4 — evidência transferível e auditoria interna.** Classifica os eventos
  e fixa a propriedade que torna a transferência parcial honesta: a omissão é
  detetável por salto de `sequence` e ligação de hash que não fecha.
- **`CUST-REQ-004`** — transferir eventos íntegros; não renumerar nem recompor a
  cadeia para dissimular omissões.
- Vetores `conformance/custody/captura-chain.json` e `omissao-recomposta.json`.

- **`metadados.origem_nao_identificavel`** com `fundamento` obrigatório —
  quarto modo do invariante de origem (§2.2.1, §2.7.6). Único caso desta ronda
  que **altera o schema do NDF-core**; decisão de âmbito registada em
  `ROADMAP.md`, fundamentação em ADR-023. Não coexiste com `participantes` de
  papel autoral nem com `proveniencia_sistema`; **pode** coexistir com
  `proveniencia_ia`, por a intervenção de IA ser assistência e não produção.
- **`NDF-PROD-023`** e **`NDF-READ-024`** — coerência do quarto modo, e não
  confundir origem não apurável com ausência de entidade produtora ou de
  responsável pela custódia.
- Vetores `conformance/ndf/valid/origem-nao-apuravel.json`,
  `invalid/origem-nao-apuravel-sem-fundamento.json` e
  `invalid/origem-nao-apuravel-com-autor.json`.

### Alterado

- **§2.12.2** — a definição de `autor` passa de «produziu materialmente o
  conteúdo canonicalizado» para «o conteúdo do documento: o conteúdo estruturado
  que é canonicalizado, ou o componente binário que o constitui». Precisão
  exposta pela captura; sem alteração de schema nem do invariante.
- **Mensagem do validador** para o invariante de origem, que enumerava três
  modos e agora enumera quatro.
- **`CUST-REQ-003` e §2.4.3** — a eliminação abrange **também os componentes
  binários**. Um documento cujo conteúdo resida em componentes não fica
  eliminado pela destruição do NDF-core: o conteúdo do ato continuaria a existir
  nos ficheiros preservados. Os digests dos componentes destruídos conservam-se
  em `details`, provando o que existiu sem que os bytes subsistam.

### Notas

`manifest.schema.json` não é alterado: o inventário do pacote já cobre a
integridade física de qualquer ficheiro, e a declaração documental vive em
`documento`. Os vetores negativos de `NDF-PKG-009` acompanham o exemplo de captura.


## [Não publicado] — avaliação arquivística por perfil e separação custódia ↔ RGPD

`ndf_version` mantido em `1.0.0` (ADR-007) — alterações **incompatíveis**
absorvidas antes de qualquer publicação. Ver `CHANGELOG.md` na raiz para o
detalhe completo.

- adicionado: `avaliacao.perfil`, com schemas de perfil em
  `specs/registry/profiles/` e obrigação de viajarem no `.ndfpkg`
  (NDF-PKG-008); perfis `pt-dglab` e `generic` (ADR-015);
- adicionado: `destino_final: "a_determinar"` com `autoridade_avaliacao`, para
  sistemas em que a decisão de destino não compete ao produtor;
- alterado: `tipo_classificacao_ref` → `classificacao_ref`;
  `instrumento_avaliacao_versao_ref` → `instrumento_ref`;
  `prazo_conservacao_administrativa` → `prazo_conservacao`;
- adicionado: `metadados.entidade_responsavel` (custódia do registo);
- alterado: campos RGPD agrupados em `metadados.protecao_dados`, obrigatório
  se e só se `contem_dados_pessoais: true` (ADR-016).

## [Não publicado] — proveniência de sistema e imputação jurídica

`ndf_version` mantido em `1.0.0` (ADR-007). Ver `CHANGELOG.md` na raiz para o
detalhe completo.

- adicionado: `proveniencia_sistema` (array) — sistema determinístico que
  produziu o conteúdo, com ordem cronológica normativa (ADR-013);
- adicionado: `imputacao` (array) — quem responde juridicamente e a que
  título, com bloco opcional `autenticacao` por entrada (ADR-012);
- adicionado: invariante de origem — todo o NDF declara origem humana, de
  sistema ou de IA (§2.2.1);
- alterado: `participantes` passa a índice exclusivamente de pessoas
  singulares; removidos `tipo`, `sistema_tecnico`, `entidade_produtora`,
  `validador` e `aprovador`; acrescentados `responsavel_tecnico` e
  `qualificacao`;
- adicionado: `tipo_documento_ref` aceita `ext.<entidade>.<tipo>@<versao>`,
  com o schema a viajar no pacote (ADR-014).

## [1.0.0] — Draft — Revisão pública

- Especificação inicial: estrutura NDF-core, envelope CAdES-B-LTA, avaliação
  arquivística, pipeline de finalização, proveniência e versionamento.
