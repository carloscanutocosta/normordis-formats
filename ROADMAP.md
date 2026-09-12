# NORMORDIS Roadmap

Estado em: 2026-08-11

---

## Estado actual

| Artefacto | Estado | Versão |
|---|---|---|
| NDF — NORMORDIS Document Format | Draft — Revisão pública | 1.0.0 |
| NDT — NORMORDIS Document Template | Draft — Revisão pública | 2.0.0 |
| NCRTF — NORMORDIS Canonical Rich Text Format | Draft — Revisão pública | 2.0.0 |
| JSON Schema NDF-core | Draft | 1.0.0 |
| Registo de tipos de documento | Draft (4 tipos canónicos) | 1.0.0 |
| Suite de conformidade NDF | Draft + CI verde | 1.0.0 |
| Suite conformidade NDT (válidos + inválidos) | Draft executável + CI verde | 2.0.0 |
| Suite conformidade NCRTF | Draft executável + CI verde | 2.0.0 |
| Cadeia de custódia | Schema + vetores draft | 1.0.0 |
| Portal de verificação | Contrato OpenAPI draft | 1.0.0 |
| CI/GitHub Actions | Operacional (3 jobs) | — |

**Roadmap operacional curto:**
[`docs/roadmap/NGI-MVP-2026.md`](docs/roadmap/NGI-MVP-2026.md) — **parcialmente
superado** pelas decisões de sequenciamento de 2026-08-11 abaixo. A etapa XML
saiu do caminho crítico e os marcos M2–M5 deixaram de ter datas.

---

## Decisões de sequenciamento (2026-08-11)

Origem: avaliação de prontidão para debate público e candidatura NGI, em
[`docs/reports/READINESS-ASSESSMENT.md`](docs/reports/READINESS-ASSESSMENT.md),
que mantém os achados abertos com ID estável (`R*`) e é o documento vivo onde
este trabalho se afina.

Constatação de fundo: **a especificação está sobredesenvolvida face à
demonstração**. O que falta não é âmbito normativo — é evidência executável e
validação independente. As decisões abaixo reordenam o trabalho em função
disso.

| # | Decisão | Efeito no roadmap |
|---|---|---|
| D1 | Debate público deixa de ter janela temporal e passa a ter **condição de evidência**: abre quando `normordis-pdf` estiver funcional. `normordis-odf` é evidência de segunda implementação, posterior, e **não bloqueia** a abertura | PR-001 adiado; datas substituídas por condição — ver `R1` |
| D2 | **Adapters XML despriorizados.** Reproduziriam apenas o payload de dados, e o NDF não substitui os dados estruturados dos sistemas aplicacionais. Coerente com o princípio de âmbito de `LACUNAS.md`. **Reforçado em 2026-08-11**: o NDF é formato de *documento*, não de *dados* — um adapter XML↔NDF conflacia camadas e não deve ser reposto. A interoperabilidade a explorar é ao nível do **pacote documental** (depósito OAIS/METS/PREMIS), não dos dados | `normordis-xml-adapters` sai do caminho crítico e não regressa; ver `R13` e secção 5.2 do relatório |
| D3 | **Versão inglesa necessária** | Novo item de Fase 6 (gaps editoriais) — ver `R3` |
| D4 | **Fixtures CAdES reais entram no roadmap**, deixando de ser apenas gate externo pendente | Trabalho atribuível sobre `CADES-GATE-PLAN.md` — ver `R2` |
| D5 | **NDF-core congelado em âmbito.** O formato prevê já o que foi idealizado: guarda de documentos, metadados de segurança, auditoria, relações entre documentos, intervenientes | Cessa o alargamento normativo do NDF-core; esforço desloca-se para NDT, NCRTF, `normordis-pdf` e `normordis-odf` |
| D6 | **Procura de necessidade institucional em linha paralela**, sem depender de marcos de engenharia | Gate externo 7 passa a trabalho ativo — ver `R5` |
| D7 | **Três eixos de posicionamento**: soberania documental, eficiência e capacidade, implementabilidade livre por terceiros | Exige corpus comparativo de medição antes de qualquer afirmação quantitativa — ver `R6` |
| D8 | **Resposta à avaliação externa de 2026-09-11 entra no caminho crítico, à frente do fecho do laboratório CAdES.** A falha NDF↔NDT (`R16`) e as omissões silenciosas do validador (`R17`, `R18`) tornam qualquer assinatura CAdES real, por si só, insuficiente para provar a cadeia de confiança | Nova **Fase 1E**. A Fase 1D (D4) passa a depender da conclusão do bloco P0 da Fase 1E para ser lida como prova completa da cadeia; os passos técnicos de laboratório em si não ficam bloqueados, só a sua interpretação |

### Alcance de D5

Congelar o âmbito **não** congela o texto. Continuam admissíveis: correções de
defeito, clarificações resultantes de revisão externa, e o trabalho editorial
de normalização já previsto na Fase 6 (linguagem normativa, termos e
definições, referências normativas, anexos). Os itens de NDF v1.1.0, v1.2.0 e
v2.0.0 mais abaixo mantêm-se — são evolução planeada, não lacunas do âmbito
atual.

**Risco registado:** D1 e D5 combinadas congelam o âmbito *antes* de qualquer
contacto externo. Se a revisão pública revelar lacunas de âmbito — e não apenas
defeitos —, o congelamento reabre. Isso deve ser lido como resultado esperado
do processo de revisão, não como falha de planeamento.

**Reabertura de D5 (2026-08-13).** O risco acima concretizou-se, por revisão
interna e não externa. D5 registava que «o formato prevê já o que foi
idealizado: guarda de documentos, metadados de segurança, auditoria, relações
entre documentos, intervenientes». Faltava uma categoria inteira: **documentos
gerados por sistemas determinísticos**, sem autor humano material —
liquidações de impostos, notificações, certidões automáticas —, que é
provavelmente a mais numerosa da Administração Pública moderna. O NDF não
sabia registar que sistema os produziu (`proveniencia_sistema`, ADR-013) nem
quem responde juridicamente por eles (`imputacao`, ADR-012), sendo esta última
uma menção legalmente obrigatória e condição do exercício dos meios de defesa.

Isto é lacuna de âmbito, não defeito de texto, pelo que **excede o alcance
admitido por D5** e é registado como tal. O congelamento mantém-se quanto ao
resto: esta reabertura é pontual, fundamentada nos três ADR, e não constitui
autorização genérica para alargar o NDF-core. `ndf_version` mantém-se em
`1.0.0` (ADR-007).

**Decisão de âmbito sobre SPEC §2.8 (2026-08-20).** A cláusula §2.8 exclui hoje,
pela negativa, os anexos binários opacos: declara que a especificação «cobre
apenas documentos gerados internamente sem anexos binários opacos». Admitir que
um schema de tipo documental declare componentes binários **por hash** — e só
por hash, nunca por bytes embutidos no core — remove essa exclusão.

Registado como **decisão de âmbito**, e não como clarificação editorial, por
conservadorismo: altera o que o formato admite. Mas é a categoria mais fraca
das três — não acrescenta nenhuma primitiva ao NDF-core, ao contrário da
reabertura de 2026-08-13.

Na verdade, o teste da secção seguinte mostra que §2.8 está em contradição
interna com ele próprio. Aplicado à declaração de componentes binários:
(1) é informação documental — que binário constitui este documento pertence ao
documento, não ao procedimento; (2) **cabe em `documento`, via schema do tipo**
— e o teste manda parar aí, porque esse é o lugar. É exatamente o que se faz
(`documento-capturado@1.0.0`, ver
[`docs/roadmap/PLANO-CAPTURA-NDFPKG.md`](docs/roadmap/PLANO-CAPTURA-NDFPKG.md)).
§2.8, tal como está, proíbe o schema de tipo de fazer aquilo que o passo 2 do
teste lhe atribui.

O NDF-core não é alterado: nenhum campo novo, nenhuma primitiva nova,
`ndf_version` mantém-se em `1.0.0` (ADR-007). O congelamento mantém-se quanto
ao resto, e esta decisão não constitui autorização genérica para alargar o
core.

**Segunda reabertura pontual de D5 (2026-08-20) — origem não apurável.** Ao
contrário da decisão sobre §2.8 acima, esta **altera o schema do NDF-core**:
acrescenta `metadados.origem_nao_identificavel` e um quarto ramo ao `anyOf` do
invariante de origem (§2.2.1).

O caso não existia antes da captura documental. Enquanto todo o NDF nascia no
sistema produtor, a origem era sempre conhecida e os três modos bastavam. Com a
captura, um documento pode entrar em custódia sem origem apurável — um
digitalizado de 1987 sem menção de autor, uma denúncia anónima, um ficheiro de
sistema de terceiro sem identificação. §2.2.1 obrigava, nesses casos, a rejeitar
o documento ou a fabricar-lhe um autor, o que a própria cláusula proíbe.

O teste da secção seguinte foi percorrido e dá seis respostas coerentes, com o
passo 3 a resolver a colocação: entra em `metadados`, o bloco dos campos
descritivos transversais, e **não** como primitiva de topo. Fundamentação
completa em [ADR-023](docs/architecture/ADR-023-origem-nao-apuravel.md) e no
Bloco F de
[`docs/roadmap/PLANO-CAPTURA-NDFPKG.md`](docs/roadmap/PLANO-CAPTURA-NDFPKG.md).

Adição opcional que não invalida nenhum documento existente; `ndf_version`
mantém-se em `1.0.0` (ADR-007). Como as reaberturas anteriores, é pontual e
fundamentada, e não constitui autorização genérica para alargar o core.

### Teste de admissão de novas primitivas no NDF-core (2026-08-15)

D5 declara o congelamento de âmbito mas não definia **o que o quebra**. A
reabertura de 2026-08-13 foi decidida caso a caso, por juízo, sem critério
escrito — e correu bem, mas não é método. Este teste fixa o critério.

**Âmbito.** Aplica-se **apenas ao NDF-core**. NDT e NCRTF não estão sob D5:
pelo contrário, D5 desloca explicitamente o esforço para eles. Trabalho de
afinação em NDT e NCRTF não carece deste teste e não constitui reabertura de
nada.

#### O teste

Perante a proposta de uma nova primitiva no NDF-core, percorrer por ordem. A
primeira resposta afirmativa encerra a questão — a proposta **não** entra no
core:

1. **É informação documental?** Se for estado de procedimento, regra de
   workflow, prazo processual, entrega, notificação, ou facto posterior à
   finalização, é do sistema de gestão. Ver o princípio de âmbito de
   [`LACUNAS.md`](LACUNAS.md).
2. **Cabe em `documento`, via schema do tipo documental?** Se for específico de
   uma tipologia, o lugar é o schema do tipo, não o core (SPEC §2.9.1).
3. **Cabe num bloco transversal existente?** `metadados`, `avaliacao`,
   `relacoes`, `participantes`, `proveniencia_sistema`, `proveniencia_ia`,
   `imputacao`. Estes blocos foram desenhados para absorver casos novos sem
   crescer o topo do core.
4. **É variação jurisdicional de algo que já existe?** Então é matéria de
   perfil (SPEC §3.2.3), não de core. Ver [`docs/profiles/`](docs/profiles/README.md).
5. **Pode viver fora do NDF, referenciada por hash?** É o padrão já usado para
   evidência de IA, regras de sistema e artefactos externos. Referência mais
   hash preserva a verificabilidade sem inchar o documento.
6. **Pode simplesmente não existir?** Se nenhum caso real a exige, não entra.

Só depois de as seis respostas serem negativas se considera alterar o core. E
mesmo aí aplica-se a regra do [ADR-015](docs/architecture/ADR-015-generalizacao-avaliacao-arquivistica.md):
não abstrair por antecipação — só se generaliza um eixo quando for possível
**nomear três sistemas reais que divergem nesse eixo**.

As duas regras são complementares e respondem a perguntas diferentes: este
teste decide se uma primitiva **entra**; a regra do ADR-015 decide se uma
primitiva existente **se generaliza**.

#### O que NÃO é alteração de formato

Confusões frequentes, que não acionam este teste nem reabrem D5:

| Trabalho | Porquê não é alteração de formato |
|---|---|
| acrescentar ou corrigir documentação | o texto não é o contrato; o schema e os vetores são |
| acrescentar casos de conformidade | aumenta a cobertura do contrato existente |
| acrescentar um tipo documental | é `tipo_documento_ref` mais schema próprio; o core não muda |
| acrescentar um perfil de avaliação | é acréscimo ao registo (SPEC §3.2.3) |
| acrescentar ou afinar um NDT | fora de D5, e fora do NDF-core |
| corrigir defeito, ambiguidade ou incoerência editorial | admitido expressamente pelo alcance de D5 |

#### Validação retrospetiva

Aplicado ao caso que reabriu D5 em 2026-08-13, o teste dá a resposta certa.
`proveniencia_sistema` e `imputacao`: (1) é informação documental — quem
produziu e quem responde juridicamente pertencem ao documento, não ao
procedimento; (2) não é específico de uma tipologia — atravessa liquidações,
notificações e certidões; (3) não cabia em nenhum bloco existente —
`participantes` é índice de pessoas singulares e `entidade_produtora` é a
pessoa coletiva, nenhum exprime imputação jurídica nem cadeia de sistemas;
(4) não é variação jurisdicional; (5) não pode viver fora, por ser menção
legalmente obrigatória do próprio ato; (6) havia casos reais e numerosos.

Seis negativas: a primitiva entra. Foi o que se fez, e o teste confirma-o —
o que dá alguma confiança de que não é apenas uma racionalização das decisões
já tomadas.

#### Consequência prática

A partir daqui, a pergunta de trabalho deixa de ser *"o que falta ao NDF?"* e
passa a ser *"o que é que uma implementação real não consegue fazer com o NDF
tal como está?"*. A primeira pergunta produz âmbito; a segunda produz
evidência — e é evidência o que falta, não âmbito.

### Sequência de trabalho resultante

**Caminho crítico até à abertura do debate**

1. ~~corrigir o estado comunicado de PR-001 e do `README.md`~~ — ✅ concluído
   em 2026-08-11: PR-001 passa a `adiado` com condição de abertura em vez de
   datas; estado editorial corrigido para «Draft — revisão pública por abrir»
   (nível 1) nas seis SPECs e no `README.md` (`R1`);
2. `normordis-pdf` até ao caso Modelo 3 fim-a-fim, reproduzível por terceiros
   a partir do README (`R8`) — **reestimado em 2026-08-11**: o renderizador de
   layout posicionado NDT 2.0.0 é hoje um stub que devolve erro, e a ligação
   `Campo.referencia` → `NDF-core.documento` não está implementada (`R15`).
   A colisão de nomes com o NDF-core (`R14`) foi **resolvida em 2026-08-11**
   por renomeação para `RenderArchive` no crate, que passa a v4.0.0. O crate
   fica organizado em camadas — motor autónomo PDF/UA na base, conformidade
   NDF/NDT por cima, atrás de *feature* Cargo. Detalhe nas secções 5.1 e 5.3
   do relatório;
3. par mínimo de fixtures CAdES — uma positiva com certificado de teste próprio
   e uma `payload-tampered` (`R2`);
4. versão inglesa, começando por `README.en.md` e abstract/âmbito das três
   SPECs (`R3`).

**Linhas paralelas**

5. procura de necessidade institucional (`R5`);
6. corpus comparativo de eficiência e capacidade — NDF+NDT contra PDF/A e ODT,
   a 1 e a N documentos, com unidade de comparação declarada (`R6`).

**Posterior**

7. `normordis-odf`, com perfil mínimo definido à partida (`R9`);
8. portal de verificação mínimo (`R7`);
9. decisão sobre o enquadramento da tese face à ausência de demonstração de
   ingestão (`R13`).

---

## Fase 1 — Especificações tecnicamente completas

Objetivo: especificação autocontido e implementável por terceiros sem acesso ao core-documental NORMORDIS.

### NDF

- [x] Campos de topo (`ndf_id`, `payload_hash_alg`, `nivel_assinatura`, `ndt_version_ref`)
- [x] Schema normativo de `metadados` (§2.7) — `entidade_produtora`, RGPD, `classificacao_seguranca`
- [x] Estados de arquivo (`estado`) — mecanismo de transição e log de auditoria (§2.4.1)
- [x] `nivel_assinatura` — enum `nenhuma` / `avancada` / `qualificada` (§2.10)
- [x] `validation_code` — derivação SHA-256 + BASE32, 100 bits (§4.6)
- [x] Pipeline de finalização condicional (§5.2)
- [x] `tipo_classificacao_ref` — formato `<instrumento>/<codigo>` (§3.2.1)
- [x] Requisitos TSA (§4.2.1)
- [x] `versao_anterior` / `hash_anterior` — localização no envelope (§6.2)
- [x] Integridade de arquivo para `nivel_assinatura: "nenhuma"` (§2.10.4)
- [x] JSON Schema legível por máquina (`ndf-core.schema.json`, `envelope.schema.json`)
- [x] Registo de tipos (`oficio`, `informacao-tecnica`, `despacho`, `modelo3-irs`)
- [x] Suite de conformidade (válidos + inválidos) — `conformance/ndf/`
- [x] Exemplo `.ndfpkg` autocontido e verificável por hash
- [x] Exemplo render-ready NDF Modelo 3 IRS — `specs/ndf/examples/modelo3-irs-2025.json`
- [x] Conformance test runner NDF + NDT + NCRTF + verificação de pacote (`tools/validate.py`)
- [x] CI/GitHub Actions — pipeline verde em cada push
- [x] `proveniencia_sistema` — documentos gerados por sistemas determinísticos (§2.14, ADR-013)
- [x] `imputacao` — responsabilidade jurídica e título, com autenticação por entrada (§2.15, ADR-012)
- [x] Invariante de origem — todo o NDF declara origem humana, de sistema ou de IA (§2.2.1)
- [x] `participantes` como índice exclusivamente de pessoas singulares, com `qualificacao` (§2.12)
- [x] Tipos documentais por namespace de entidade `ext.<entidade>.*`, com schema no pacote (§2.9.5, ADR-014)
- [x] Exemplo de pacote de liquidação automática — `specs/ndf/examples/liquidacao-irs-automatica/`

### NDT

NDT v2.0.0 está tecnicamente especificado e permanece em revisão pública. Ver
[specs/ndt/SPEC.md](specs/ndt/SPEC.md) e
[specs/ndt/CHANGELOG.md](specs/ndt/CHANGELOG.md).

- [x] Axioma layout-puro (sem expressões, sem validação, sem lógica de negócio)
- [x] `paginas_def[]` + `sequencia[]` — modelo multi-página com definições distintas
- [x] Primitivas gráficas: linha, rectangulo, grelha_digitos, imagem, texto_fixo, codigo_barras, poligono, elipse, svg, tabela_visual, assinatura
- [x] `campos[]` — valores NDF escalares posicionados em coordenadas absolutas
- [x] `blocos[]` — tabela (com `min_linhas_visivel`), corpo (NCRTF), cabecalho, rodape
- [x] `fluxo` — layout relativo para documentos administrativos, com `linha_lateral` e `quebra_pagina`
- [x] `estilos` — fonte principal de estilo para renderizadores ODF/HTML
- [x] Modelo de assinatura híbrida CAdES + PAdES (`modo: "hibrido"`)
- [x] Acessibilidade PDF/UA-2 (`alt`, `rotulo_acessivel`, AcroForm `/TU`)
- [x] `incluir_se` em `campos[]`, `blocos[]`, `fluxo.elementos` e `sequencia[]`
- [x] JSON Schema Draft 2020-12 (`specs/ndt/schemas/ndt.schema.json`)
- [x] Exemplos render-ready validados (`specs/ndt/examples/`) — ofício, Modelo 3 Rosto, Anexo A, Anexo G
- [x] Suite de conformidade NDT (`conformance/ndt/valid/` + `conformance/ndt/invalid/`)

---

## Fase 1B — Robustez normativa e de segurança (`LACUNAS.md`)

Origem: revisão adversarial pós-estabilização (2026-08-07), registada em
[`LACUNAS.md`](LACUNAS.md), já recalibrada pelo princípio de âmbito do NDF —
*"formato eficiente para guardar documentos reconstituíveis, não substituto
de workflows específicos de procedimento"*. A maioria dos itens desta fase é
**normativa (texto), não estrutural (schema)** — precisamente porque, após
recalibração, a maior parte do que faltava era dizer com clareza o que o
NDF *não* garante, não acrescentar mais schema.

### Lista de alterações

| # | Origem | Alteração | Tipo | Esforço | Estado |
|---|---|---|---|---|---|
| A1 | L1 | Nota normativa em §2.11.5: relação é afirmação unilateral e assinada, não implica reconhecimento/consentimento do alvo | Texto (SPEC.md) | Baixo | ✅ Feito |
| A3 | L3 | Nota de implementação em §2.11.5: deteção de ciclos é responsabilidade do verificador/renderizador de grafo, o schema não impõe acircularidade entre documentos independentes | Texto (SPEC.md) | Baixo | ✅ Feito |
| A4 | L7 | Nota normativa em §4.4.1: correspondência `papel`↔exigência legal de quem assina é responsabilidade da entidade produtora, não garantida pelo formato (mesmo padrão de §2.10.2) | Texto (SPEC.md) | Baixo | ✅ Feito |
| A5 | L9 | Nota normativa em §2.12.3: `participante_ref` é referência externa não resolvida pelo NDF, por desenho — paralelo explícito a `tipo_classificacao_ref` | Texto (SPEC.md) | Baixo | ✅ Feito |
| A6 | L10 | Nota em §2.12.4: `validador`/`aprovador` descrevem estado de workflow, não conteúdo intrínseco — uso desencorajado fora de sistemas que já os tratem como tal; **não removido do enum** (seria alteração incompatível sem necessidade demonstrada) | Texto (SPEC.md) | Baixo | ✅ Feito |
| A7 | L5 | Verificação semântica: `despacho.sobre[]` e `NDF-core.relacoes` com conjuntos divergentes de `ndf_id` produz aviso (não erro) | Código (`tools/validate.py`, `check_ndf_advisories`) | Médio | ✅ Feito |
| A8 | L8 | Estendido `delegacao_ref` (mesmo padrão de `despacho.decisor`) a `parecer.autor` e `informacao-tecnica.autor` | Schema aditivo (`specs/registry/schemas/`), editado em `1.0.0` — mesma lógica do ADR-007, sem consumidores externos a proteger | Médio | ✅ Feito |
| A9 | L4 | Mecanismo de extensão qualificada `relacoes[].tipo` = `ext.<entidade>.<tipo>`, além do enum fechado (`oneOf`, aditivo) | Schema (`ndf-core.schema.json`) + SPEC.md §2.11.7 + ADR-008 | Alto | ✅ Feito |
| A10 | L6 | Analisado e decidido **não alterar** o formato de `ndf_id` — identificador opaco por desenho; entidade produtora já resolvida por `metadados.entidade_produtora` | ADR-009 + clarificação normativa em SPEC.md §2.3 | Alto | ✅ Feito (fechado por decisão, não por schema) |

**A2 retirado.** A mitigação de fuga de metadados por `relacoes[]` em
documentos classificados é resolvida ao nível do core-documental (pacote
NDF protegido como artefacto opaco — cifra em repouso e em trânsito,
controlo de acesso do sistema custodiante), não por nenhum mecanismo do
NDF. Ver `LACUNAS.md` L2 e
`docs/normalization/NDF-INFORMATIVE-GUIDANCE.md`.

### Roadmap de implementação

**A1, A3–A8 — concluídos.** Todos os itens de baixo/médio esforço da lista
de alterações estão implementados, verificados (`tools/validate.py`
56/56, `check_package_vectors.py` 8/8, `audit_normative.py` e
`build_requirements_index.py` regenerados) e prontos a rever. §1.5
("Confidencialidade e controlo de acesso") também ficou concluída no
mesmo lote, embora não fizesse parte da lista original A1–A10 — emergiu
da mesma revisão adversarial. Fecha, com isto, a secção de Segurança e
Privacidade que tinha ficado por escrever na ronda de estabilização
anterior (mission §13, nunca cumprida até agora).

**A9, A10 — concluídos (2026-08-08).** A9 implementado como alteração
aditiva ao schema (todos os 11 valores base continuam válidos), com
mecanismo de extensão qualificada documentado em SPEC.md §2.11.7 e ADR-008.
A10 fechado por decisão registada em ADR-009: `ndf_id` mantém-se opaco,
sem alteração de schema — a necessidade original (identificar a entidade
produtora) já estava resolvida por `metadados.entidade_produtora`. Com
isto, `LACUNAS.md` fica com os dez pontos totalmente resolvidos: sete
implementados por texto/código, um fechado por decisão de não-alteração
(A10), dois retirados por estarem fora de âmbito (L2, L11).

Verificado: `tools/validate.py` 58/58 (56 + 2 novos casos de conformidade
para A9), `check_package_vectors.py` 8/8, `audit_normative.py` e
`build_requirements_index.py` regenerados sem erros.

**Separação NDF/Perfil de Ciclo de Vida NORMORDIS — concluída
(2026-08-08).** Revisão externa ao commit `40ef47a` identificou acoplagem
indevida entre conformidade de formato e requisitos operacionais de
custódia (`NDF-PROD-010`, §5.2 passo 8, `ARCHITECTURE.md` §2.1/§3).
Resolvido com ADR-010: nova família `CUST-REQ-*` (3 IDs, SPEC.md §9.5),
`NDF-PROD-010` reclassificado para persistência atómica (mesma ID,
conteúdo diferente), e clarificação de que `nivel_assinatura` é uma
declaração do produtor (não uma decisão jurídica do NDF) e que
`validation_code` é intrínseco ao formato, independente de qualquer
serviço específico. `tools/build_requirements_index.py` e
`audit_normative.py` passam a reconhecer `CUST-REQ-*` (54 IDs, antes 51).

---

## Fase 1C — Revisão adversarial pré-RC (concluída, 2026-08-08)

Revisão dirigida a **contradições, redundâncias e requisitos impossíveis de
implementar**, em vez de novas funcionalidades. Relatório completo, com os
16 achados e a resolução de cada um, em
[`docs/reports/NDF-PRE-RC-REVIEW.md`](docs/reports/NDF-PRE-RC-REVIEW.md).

Resultado: todos resolvidos. A decisão de fundo foi a **ADR-011** —
`versao_anterior`/`hash_anterior` removidos do envelope, ficando
`relacoes[{tipo:"substitui"}]` como única representação normativa de
sucessão documental, coberta pela assinatura.

**Lição registada para o processo, não só para o formato:** uma suite de
conformidade verde não demonstra coerência da especificação. Os 58 casos
passavam enquanto três blocos JSON da própria SPEC eram inválidos contra os
schemas que a SPEC torna obrigatórios. A validação passa a ter três camadas
distintas:

```text
correção dos schemas
        ↓
corpus de conformidade
        ↓
coerência SPEC ↔ schemas ↔ exemplos   ← acrescentada nesta fase
```

Guardrails introduzidos, ligados à CI:

| Ferramenta | O que impede |
|---|---|
| `tools/check_spec_coherence.py` | blocos JSON da SPEC inválidos; campos de schema não documentados; referências `§X.Y` quebradas; deriva entre enums duplicados; reaparecimento de propriedades removidas por ADR |
| `tools/build_conformance_index.py` | índice de conformidade desatualizado face aos ficheiros reais |

---

## Fase 1D — Evidência de assinatura CAdES (D4, `R2`)

O gate CAdES deixa de ser apenas "gate externo pendente" e passa a trabalho
atribuível. Estado atual: `tools/check_cades_gate.py` reporta **12/12 fixtures
em `skeleton`** — 5 positivas (`advanced-real`, `qualified-real`,
`institutional-seal-real`, `expired-certificate-historical`, `offline-tsa-real`)
e 7 negativas. A alegação de valor probatório de longo prazo, que é o argumento
mais forte do formato, não tem hoje qualquer suporte executável.

Plano operativo em
[`docs/normalization/CADES-GATE-PLAN.md`](docs/normalization/CADES-GATE-PLAN.md);
verificador já existente em [`tools/check_cades_gate.py`](tools/check_cades_gate.py).

| Passo | Entregável | Nota |
|---|---|---|
| 1 | Par mínimo: uma fixture positiva com certificado de teste próprio e a negativa `payload-tampered` | Converte o gate de "pendente" em "iniciado com evidência" — suficiente para responder em debate |
| 2 | Restantes negativas (`signature-tampered`, `timestamp-missing`, `timestamp-altered`, `chain-untrusted`, `payload-hash-mismatch`, `revocation-before-signing`) | Não dependem de certificado qualificado |
| 3 | Positivas com material real (`qualified-real`, `institutional-seal-real`, `offline-tsa-real`) | Dependem de certificado/TSA reais ou parceria — **permanecem gate externo** |

O passo 1 é caminho crítico até à abertura do debate; os passos 2 e 3 não são.

---

## Fase 1E — Integridade da cadeia de confiança e resposta à revisão adversarial de 2026-09-11

Origem: revisão adversarial assistida por IA, com testes locais reproduzidos,
ao commit `a9d72f8`, com achados registados em
[`docs/reports/READINESS-ASSESSMENT.md`](docs/reports/READINESS-ASSESSMENT.md)
§5.6 (`R16`–`R22`). **Não é revisão externa independente** — não houve
revisor humano especializado em criptografia, direito ou arquivística a
validar estes achados; ver a nota de método em READINESS-ASSESSMENT.md §5.6,
que inclui erros de remissão jurídica da própria primeira ronda de correção
(CRA e eIDAS), corrigidos só depois de verificação contra o texto legal.
Ainda assim, é a primeira resposta estruturada a achados que não nasceram de
auto-revisão do mantenedor (ver D8) — os achados técnicos falsificáveis
(`R16`–`R19`) foram reproduzidos localmente, pelo que o critério de conclusão
desses itens é mais estrito: tem de sobreviver a nova tentativa de
falsificação, não apenas passar a suite existente. Os achados jurídicos
(`R20`–`R22`) têm as citações corrigidas, mas continuam a precisar de
revisão profissional externa antes de fechar qualquer gate — ver P2.1.

**Objetivo único**: tornar demonstrável, por terceiros, o percurso
NDF → assinatura → pacote → validação → representação, sem depender de
leitura confiante da documentação. Cartão de Cidadão e cartão profissional
ECCE ficam fora de qualquer teste, em todos os passos abaixo — ver P1.1.

### Sequência de trabalho

| Prioridade | Entrega | Resultado esperado | Achados cobertos |
|---|---|---|---|
| P0.1 | Clarificar garantias e limitações na documentação | O leitor distingue especificado / implementado / demonstrado | `R18`, `R19`, `R21`, `R22` |
| P0.2 | Autenticar NDT e dependências de interpretação | Substituição de NDT sem alterar os bytes do NDF-core passa a ser detetada | `R16` |
| P0.3 | Eliminar validação silenciosa e separar resultados por camada | `rfc8785` obrigatório; validador reporta por camada; *placeholders* só aceites em testes explicitamente marcados como tal | `R17`, `R18` |
| P0.4 | Correções jurídicas pontuais | CRA, RGPD e assinatura qualificada corrigidos no texto | `R20`, `R21`, `R22` |
| P0.5 | Correções editoriais pontuais | regex/exemplo de `pt-dglab` coerentes; contagens desatualizadas corrigidas | `R19` |
| P1.1 | Laboratório CAdES sem cartões (estende a Fase 1D / D4) | Assinaturas e provas temporais reais, identidades fictícias, três resultados separados (técnico / laboratório / eIDAS) | `R2`, `R22` |
| P1.2 | Caso documental completo reproduzível | Um percurso ponta-a-ponta, verificável por terceiro | `R8`, `R15` |
| P2.1 | Revisão independente delimitada | Perguntas jurídicas/arquivísticas concretas, com resposta acionável | `R4`, `R5` |

O bloco P0 é o caminho crítico desta fase — nenhum item de P1 conta como
prova fechada de cadeia de confiança enquanto P0.2 e P0.3 não estiverem
concluídos (D8).

### P0.1 — Documentação: garantia / mecanismo / evidência / limitação — ✅ concluído (2026-09-12)

- [x] Tabela «garantia / mecanismo / evidência / limitação» em
      [`docs/normalization/NDF-INFORMATIVE-GUIDANCE.md`](docs/normalization/NDF-INFORMATIVE-GUIDANCE.md)
      (secção nova «Garantias e limitações»), cobrindo imutabilidade,
      `nivel_assinatura`, autonomia do pacote, reprodução fiel e
      conformidade — com a distinção especificado / implementado /
      demonstrado explicitada antes da tabela
- [x] A mesma secção explicita, como regra geral, a distinção entre valor
      **declarado pelo produtor** (ex.: `nivel_assinatura`) e **conclusão
      apurada pelo verificador** (SPEC.md §9.4.2); a linha `nivel_assinatura`
      da tabela aplica essa distinção em concreto. Correção ponto a ponto de
      cada menção normativa na SPEC.md fica para P0.4, que trata as
      correções jurídicas pontuais
- [x] Exemplos com assinaturas/certificados/timestamps fictícios já
      identificados explicitamente onde existe material desse tipo:
      `ndfpkg-example/README.md`, `informacao-parecer-despacho/README.md`,
      `liquidacao-irs-automatica/README.md` (nota própria); `ndfxfer-example`
      remete para os dois primeiros, de quem as unidades são cópia.
      `captura-requerimento` não tem assinaturas (`assinaturas: []`), não
      precisa de nota
- [x] `pt-dglab` marcado como perfil experimental do projeto, sem aprovação
      institucional, na `description` do próprio schema
      ([`specs/registry/profiles/pt-dglab.schema.json`](specs/registry/profiles/pt-dglab.schema.json))
      e em [`specs/registry/README.md`](specs/registry/README.md). Alteração
      ao schema propagada às 3 cópias embutidas estáticas
      (`ndfpkg-example`, `captura-requerimento`, `liquidacao-irs-automatica`)
      e ao hash declarado em `dependencias_interpretacao` de cada
      `ndf-core.json` (P0.2, ADR-026); pacotes reselados com
      `tools/reseal_example_package.py`, `ndfxfer-example` regenerado com
      `tools/build_ndfxfer_example.py`

**Critério de conclusão**: cumprido — cada garantia pública aponta para um
requisito e uma evidência; onde falta evidência, isso fica dito junto da
afirmação. Verificado: `tools/validate.py` 103/103, `--package` PASS nos 3
pacotes base + 2 unidades de `ndfxfer-example` (camada
`assinatura_confianca` continua, corretamente, `indeterminada`/
`não_executada` — P0.1 não muda o que é verificado, só a documentação),
`check_spec_coherence` PASS (6 schemas verificados nas cópias),
`check_package_vectors` 22/22, `check_profile_patterns` PASS,
`check_transferencia` e `check_transferencia_vectors` 11/11, `audit_normative`
109 IDs / 325 declarações.

**Nota lateral, não relacionada com P0.1**: `liquidacao-irs-automatica`
falha hoje em `validate.py --package` por divergência entre o NDT e o
schema do tipo (`signatario`, `signatario_b`, `corpo`, `destinatario`,
`numero` não declarados por `ext.at.liquidacao-irs@2026.1`). Confirmado por
`git stash` que a falha já existia antes desta ronda — não é regressão
introduzida aqui. Fica registado como defeito a abrir separadamente, fora
do âmbito de P0.1/P2.1.

### P0.2 — Ligação criptográfica NDF↔NDT (`R16`, `R23`, `R24`, `R25`) — ✅ concluído (2026-09-11)

Três rondas, cada uma resposta a revisão adversarial à ronda anterior,
verificada de forma independente antes de corrigir. A primeira (commit
`3985001`) fechou o ataque ao NDT mas deixou duas dependências sem a mesma
proteção e uma promessa da SPEC por cumprir. A segunda fechou essas duas
(`R23`, `R24`) e retirou a promessa. A terceira (`R25`) fechou uma
ambiguidade na própria correção de `R23`: a resolução do recurso por
`recursos/<hash>.*` só verificava o primeiro candidato por ordem
alfabética — dois ficheiros com o mesmo hash declarado, um legítimo e um
adulterado, e só o primeiro por ordem alfabética era escrutinado.

- [x] Registado em **[ADR-026](docs/architecture/ADR-026-dependencias-interpretacao-autenticadas.md)**:
      campo `dependencias_interpretacao` inline no NDF-core (não manifesto
      à parte — precedente de ADR-021), com hash coberto pela assinatura,
      separado do inventário físico do `.ndfpkg`. Terceira reabertura
      pontual de D5
- [x] Bytes brutos (não JCS) do ficheiro materializado — mesma convenção
      de `manifest.inventario` e `documento.componentes[].sha256`.
      `hash_sha256` apertado para `^sha256:[0-9a-f]{64}$` (aceitava
      qualquer algoritmo/comprimento na primeira ronda)
- [x] Cadeia de referências: `"ndt"` (sempre), `"schema_tipo"` (**sempre**,
      canónico ou extensão qualificada — revisto na segunda ronda; a
      condição inicial só cobria extensão qualificada e deixava
      `schemas/oficio.schema.json` substituível, `R24`), `"schema_perfil"`
      (avaliação, sempre obrigatório em `schemas/`). Resolução por
      **caminho fixo** (`ndt/<ref>.ndt.json`, `schemas/<tipo ou
      perfil>.schema.json`) — a promessa de resolução por `ref`/hash da
      primeira ronda foi retirada, não implementada (decisão registada em
      ADR-026 §"Correções"). Recursos do NDT (fontes, imagens), vinculados
      por hash dentro do próprio NDT (`recursos[].hash_sha256`), passam a
      ter a verificação física que faltava (`R23`) — resolvidos por nome =
      hash (§8.1), não pelo `id` declarado
- [x] `specs/ndf/schemas/ndf-core.schema.json` (+ 3 cópias embutidas),
      `specs/ndf/SPEC.md` §1.2/§2.2/§2.6.2/§8.1/§8.3/§9.1–9.3,
      `specs/ndt/SPEC.md` §1.1, `tools/validate.py` (produtor semântico +
      leitor de pacote, `NDF-PROD-024/025`, `NDF-PKG-007/010/011`,
      `NDF-READ-025/026`), 26 fixtures de `conformance/ndf/`, os 3 pacotes
      de exemplo base (+ `ndfxfer-example`, derivado) e os dois recursos
      renomeados para a convenção nome = hash que já deviam seguir
- [x] Documentos antigos: sem instâncias externas a migrar (nível 1 —
      Draft), não há distinção retroativa a preservar
- [x] Vetores de teste em `tools/check_package_vectors.py`:

  | Caso | Resultado exigido | Estado |
  |---|---|---|
  | Alterar texto fixo do NDT, recalcular só o inventário físico (o ataque original) | rejeitar | ✅ `PKG-NEG-017` |
  | Trocar o schema do **perfil** mantendo o identificador | rejeitar | ✅ `PKG-NEG-018` |
  | Omitir uma dependência do manifesto | rejeitar | ✅ `PKG-NEG-019` |
  | Trocar o schema de um tipo **canónico** (não extensão) mantendo o identificador | rejeitar | ✅ `PKG-NEG-020` |
  | Substituir uma fonte ou imagem referenciada pelo NDT | rejeitar | ✅ `PKG-NEG-021` |
  | Dois ficheiros candidatos ao mesmo recurso (um legítimo, um adulterado) | rejeitar | ✅ `PKG-NEG-022` |
  | Reorganizar os caminhos do pacote, mesmos componentes | — | retirado; resolução é por caminho fixo, não é mais uma promessa a testar |

**Critério de conclusão**: cumprido, incluindo as lacunas e a divergência de
contrato encontradas em três rondas de revisão adversarial sucessivas —
cada uma à correção da anterior. Verificado: `tools/validate.py` 103/103,
`check_spec_coherence` PASS, `check_package_vectors` 22/22,
`check_profile_patterns` PASS, `audit_normative` 109 IDs / 317 declarações.

### P0.3 — Validador honesto sobre o que verificou (`R17`, `R18`) — ✅ concluído (2026-09-12)

- [x] `rfc8785` passa a dependência obrigatória em `tools/validate.py` —
      falha dura no arranque (`sys.exit(1)`, mesma mensagem de todas as
      outras ferramentas do projeto), não `PASS` silencioso na sua
      ausência. Vetor `tools/check_jcs_required.py` (subprocesso isolado,
      simula a ausência)
- [x] Relatório com resultado por camada — `validate_package_report()`
      devolve `estrutura`, `canonicalizacao`, `integridade_componentes`,
      `dependencias_interpretacao`, `assinatura_confianca`,
      `representacao`, cada uma `aprovada` / `reprovada` / `indeterminada`
      (só `assinatura_confianca` — nunca "aprovada", por este verificador
      não fazer validação criptográfica de CAdES nem de cadeia de
      confiança) / `não_executada` (sempre em `representacao`; em
      `assinatura_confianca` quando `nivel_assinatura: "nenhuma"` sem selo)
- [x] `tools/validate.py --package <dir> --json` — relatório completo em
      JSON, com `versao_verificador`, `perfil_avaliacao`,
      `instante_verificacao` e `politica_confianca` (declarada
      explicitamente como "nenhuma", não omissão)
- [x] Aprovação global já estava condicionada às verificações exigidas
      pelo perfil (P0.2, `dependencias_interpretacao.schema_perfil`
      sempre obrigatória quando `avaliacao.perfil` declarado)
- [x] Placeholders: `_contains_placeholder()` deteta o marcador
      `PLACEHOLDER` já usado pelos pacotes de exemplo em material
      criptográfico, e a camada `assinatura_confianca` sinaliza-o
      explicitamente no estado, nunca aceite em silêncio
- [x] SPEC.md §9.4.2 (novo) — recomendação para qualquer verificador, não
      só a ferramenta de referência
- [x] Vetor `tools/check_layered_report.py` — três estados de
      `assinatura_confianca` exercitados contra pacotes reais do
      repositório (placeholder presente, placeholder removido,
      `nivel_assinatura: "nenhuma"` sem selo)
- [ ] Testar os exemplos incluídos nos próprios schemas — já coberto por
      `tools/check_profile_patterns.py` (Fase 1E, P0.5)
- [ ] Casos adversariais de ZIP (nomes duplicados, caminhos inseguros,
      ligações simbólicas): **fora de âmbito nesta ronda** —
      `tools/validate.py --package` opera sobre um diretório já
      descomprimido, não existe hoje nenhum caminho de código que abra um
      `.ndfpkg` real (ficheiro ZIP); adversários de ZIP exigiriam primeiro
      construir esse caminho. Fica registado como trabalho futuro, não
      como lacuna de R18

**Critério de conclusão**: cumprido — um pacote estruturalmente válido mas
sem assinatura criptograficamente verificada nunca aparece como
"aprovado" na camada de assinatura/confiança; o `PASS` global passa a
dizer explicitamente que camadas cobre.

**Segunda ronda (2026-09-12) — revisão adversarial à própria correção.**
Três problemas no relatório, todos reproduzidos antes de corrigir:

- `--package --json` misturava mensagens de leitura humana com o JSON no
  mesmo `stdout` — `json.loads(stdout)` falhava. Corrigido: mensagens
  humanas passam a `stderr` quando `json_mode=True`; `stdout` fica só com
  o relatório.
- `ndf-core.json` que não fosse objeto JSON (ex.: `[]`) derrubava o
  processo com `AttributeError` dentro de `check_ndf_semantic` — o
  verificador nunca chegava a devolver relatório nenhum. Corrigido: um
  corte explícito antes da verificação semântica, que devolve estrutura
  reprovada e as restantes camadas `não_executada`.
- `estado` misturava valor estável e explicação (ex.: `"indeterminada —
  material presente..."`), impedindo um consumidor automático de comparar
  por igualdade. Corrigido: `estado` passa a valor estável, `motivo` leva
  o texto livre (`None` quando não há nada a explicar).

Vetores novos em `tools/check_layered_report.py`: pureza de `stdout` em
`--json`, e `ndf-core.json` não-objeto sem exceção. SPEC.md §9.4.2
atualizada com as duas recomendações (estado sem texto embutido; não
misturar leitura humana com formato estruturado).

**Terceira ronda (2026-09-12) — a correção anterior ainda não cobria a
causa geral.** O corte de "documento não é objeto" não protegia contra um
campo *interno* com o tipo errado — `metadados: []`, `manifest.inventario:
null`, `envelope.assinaturas: [null]` — cada um reproduzido e cada um
derrubava o processo num ponto diferente (`check_ndf_semantic`, a
construção do inventário, a verificação de assinaturas), sem devolver
relatório nenhum. Generalizado: o corte deixa de verificar tipos campo a
campo e passa a verificar se a validação de schema encontrou **qualquer**
erro nos três documentos — nesse caso, para ali, sem tentar continuar.
Cobre estes três casos e qualquer outro da mesma classe, sem os enumerar.

Quatro casos de estrutura inválida agora em `tools/check_layered_report.py`
(documento não-objeto + os três campos internos). SPEC.md §9.4.2 explicita
o critério geral (qualquer erro de schema interrompe as camadas
dependentes).

Verificado: `tools/validate.py` 103/103, `check_package_vectors` 22/22,
`check_jcs_required` PASS, `check_layered_report` PASS,
`check_spec_coherence` PASS, `audit_normative` 109 IDs / 325 declarações.

### P0.4 — Correções jurídicas pontuais (`R20`, `R21`, `R22`)

- [x] `CRA_REPORTING.md`: corrigir a citação para art. 14.º, **n.º 8**;
      remover a formulação que liga o aviso a utilizadores à sequência
      "após notificação à autoridade" — o n.º 8 liga-o ao conhecimento do
      evento
- [x] `CRA_REPORTING.md`: rever a justificação inicial de sujeição ao
      CRA. **Duas rondas**: a primeira substituiu "vocação institucional"
      por uma citação errada (art. 2.º, n.º 4 — equipamento marítimo,
      Diretiva 2014/90/UE); corrigida para se apoiar no art. 2.º n.º 1 +
      art. 3.º ponto 22 ("disponibilização no mercado") + considerandos
      15/18/19, sem fixar um número de exceção isolado
- [x] Secção RGPD do NDF (`specs/ndf/SPEC.md` §1.4): substituído
      "resolvido" por "enquadrado", distinguindo mecanismos suportados
      pelo formato de decisões que cabem ao responsável pelo tratamento —
      sem tentar resolver a tensão dentro do NDF-core. `LACUNAS.md` L13
      continua aberto, sem data
- [x] Tabela de `nivel_assinatura` (`specs/ndf/SPEC.md` §2.10.1):
      acrescentada nota normativa de que `qualificada` exige também
      dispositivo qualificado de criação. **Duas rondas**: a primeira
      citou eIDAS art. 26.º (assinatura avançada, não o dispositivo);
      corrigida para Art.º 3.º ponto 12 (definição), Art.º 29.º + Anexo
      II (requisitos do dispositivo) e Art.º 32.º, n.º 1, alínea f)
      (confirmação na validação)

**Critério de conclusão**: as referências legais citam corretamente o texto
aplicável, e nenhuma afirmação de especificação promove uma declaração do
produtor a conclusão jurídica. **Cumprido para as citações**; a adequação
jurídica de fundo (se esta é a leitura correta para o caso concreto do
NORMORDIS) continua sem revisão profissional externa — ver P2.1 e a nota de
método em READINESS-ASSESSMENT.md §5.6.

### P0.5 — Correções editoriais pontuais (`R19`)

- [x] Corrigir a regex de `classificacao_ref`/`instrumento_ref` em
      `specs/registry/profiles/pt-dglab.schema.json` (e nas 5 cópias
      embutidas). **Duas rondas**: a primeira (`[^/]+` → `.+`) ficou
      permissiva demais — aceitava `"ts/"`, `"ts//"`, `"ts/at/"` e
      espaços; corrigida para regex por segmentos
      (`^[a-z][a-z0-9-]*/[A-Za-z0-9][A-Za-z0-9.-]*(?:/[A-Za-z0-9][A-Za-z0-9.-]*)*$`).
      Guardrail novo, `tools/check_profile_patterns.py`, testa
      `examples[]` contra `pattern` e fixa os casos negativos que já
      escaparam duas vezes
- [x] Corrigir contagem de vetores negativos de pacote em
      `docs/normalization/READINESS.md` (8 → 16)
- [x] Reexecutar `tools/check_spec_coherence.py` e a suite completa depois
      das correções — verde de forma repetida nas rondas de 2026-09-12
      (`evidencia_acao`, §2.12.8, e correções subsequentes)

### P1.1 — Laboratório CAdES sem cartões (estende a Fase 1D / D4)

Não substitui a Fase 1D — acrescenta-lhe a decisão operacional de manter o
Cartão de Cidadão e o cartão ECCE fora de qualquer teste.

- [ ] `NORMORDIS TEST CA` fictícia (OpenSSL): CA raiz + certificados de
      assinatura, identidades inequivocamente fictícias (`Pessoa Fictícia
      001 — TEST ONLY`)
- [ ] Confiança configurada apenas no verificador de laboratório — nunca
      instalada como raiz confiável no sistema operativo
- [ ] Sequência incremental, alinhada com
      [`docs/normalization/CADES-GATE-PLAN.md`](docs/normalization/CADES-GATE-PLAN.md):
      assinatura destacada sobre bytes JCS → validação sob confiança de
      laboratório → timestamp de assinatura → material de validação →
      timestamp de arquivo e renovação → casos negativos e validação
      histórica
- [ ] Ferramentas: DSS (Comissão Europeia) para criação/extensão/validação
      CAdES a partir de certificados `.p12`; SoftHSM numa fase posterior
      para exercitar PKCS#11
- [ ] Acrescentar a `CADES-GATE-PLAN.md` o caso em falta: evidência de
      validade histórica insuficiente → resultado **indeterminado**, sem
      aprovação silenciosa (não consta hoje dos 5 positivos/7 negativos)
- [ ] Documentar explicitamente os **três resultados separados**:
      conformidade técnica CAdES / validação sob confiança de laboratório /
      qualificação eIDAS demonstrada externamente — nunca apresentar o
      segundo como o terceiro
- [ ] Chaves operacionais de CI separadas dos artefactos públicos; fixtures
      com chaves de teste deliberadamente incluídas marcadas como públicas
      e sem confiança fora dos testes

**Critério de conclusão**: outra pessoa executa os testes e obtém os
resultados previstos, incluindo os casos em que o resultado correto é
"indeterminado" — sem que o Cartão de Cidadão ou o cartão ECCE entrem em
nenhum passo.

### P1.2 — Caso documental completo reproduzível

- [ ] Primeiro caso: ofício sintético de várias páginas, com tabela,
      imagem, assinatura e anexo. Segundo caso: um documento capturado
- [ ] Produzir: NDF + dependências autenticadas (P0.2), pacote portátil,
      assinatura de laboratório (P1.1), PDF gerado, relatório de
      validação, instruções de reprodução, resultados esperados de
      conteúdo e apresentação
- [ ] Verificar: conteúdo (nada perdido), paginação (sem cortes/
      sobreposições/duplicações), recursos (fontes/imagens correspondem
      aos bytes declarados), PDF/A (perfil efetivamente pretendido),
      acessibilidade (automática + revisão humana), portabilidade
      (reprodução em ambiente limpo)
- [ ] Ferramentas: `normordis-pdf`, veraPDF, comparação de texto/estrutura/
      imagens
- [ ] Preencher os resultados *golden* em falta em
      `specs/ndt/RENDERER-CONFORMANCE.md` (número e caixas de páginas,
      *bounding boxes* com tolerância declarada, identidade de fontes e
      recursos incorporados) — fecha também a lacuna de
      `check_ndt_semantic_corpus.py`, que hoje verifica estrutura mas não
      renderiza nem compara conteúdo produzido
- [ ] Não usar igualdade binária entre PDFs como critério geral — só
      quando o ambiente completo estiver fixado; exigir a equivalência que
      o perfil efetivamente promete

**Critério de conclusão**: um terceiro reproduz o percurso sem explicações
informais do mantenedor, e qualquer diferença fica identificada.

### P2.1 — Revisão independente delimitada

| Tema | Ação interna | Pergunta para revisão externa |
|---|---|---|
| eIDAS | P0.4 | O perfil e as conclusões do verificador estão juridicamente bem delimitados? |
| RGPD | P0.4 | Como representar retificação, eliminação e conservação sem substituir o responsável pelo tratamento? |
| CRA | P0.4 | Que componentes e intervenientes estão efetivamente abrangidos? |
| Arquivística | — | Que informação é necessária numa transferência e que informação pertence ao sistema custodiante? |

Cada linha desdobrada em perguntas concretas, com referência SPEC exata, em
[`docs/normalization/INDEPENDENT-REVIEW-QUESTIONS.md`](docs/normalization/INDEPENDENT-REVIEW-QUESTIONS.md)
(2026-09-12) — um título de uma linha não é, por si só, uma pergunta a que
um revisor externo consiga responder de forma acionável.

Contributo externo em criptografia (revisão do ADR-026 e do laboratório
CAdES), direito (matriz acima) e arquivística (transferência OAIS/METS/
PREMIS) — não bloqueia P0/P1, que avançam em paralelo. Sem contribuidor
externo identificado; não há, por isso, prazo nem issue aberta.

### Issues a abrir no GitHub

1. Autenticar NDT e dependências de interpretação (P0.2, ADR-026, `R16`)
2. Impedir validação parcial silenciosa (P0.3, `R17`, `R18`)
3. Separar resultados estruturais, criptográficos e de confiança (P0.3, `R18`)
4. Corrigir afirmações e referências jurídicas (P0.4, `R20`, `R21`, `R22`)
5. Criar corpus CAdES com PKI de laboratório (P1.1, `R2`)
6. Publicar um percurso documental reproduzível por terceiros (P1.2)

Cada issue: problema, âmbito, ficheiros afetados, evidência esperada,
critério de conclusão — conforme os blocos acima.

### Calendário indicativo

Ajustável — sequência de dependências, não compromisso de prazo:

| Período | Foco | Condição para avançar |
|---|---|---|
| Semana 1 | P0.1, P0.3, P0.4, P0.5 | Limitações explícitas na documentação; validador falha cedo e por camada |
| Semana 2 | P0.2 | Ataque de substituição de NDT deixa de passar |
| Semana 3 | P1.1 | Assinatura de laboratório real, verificada, com identidades fictícias |
| Semana 4 | P1.2 | Caso documental completo, reproduzível por terceiro |

P2.1 e o fecho pleno da Fase 1D (fixtures com material real —
`qualified-real`, `institutional-seal-real`, `offline-tsa-real`) não têm
data — dependem de evidência externa (parceria, certificado real), tal como
já registado em D4/Fase 1D.

---

## Fase 2 — Ferramentas de referência (`normordis-tools`)

Ferramentas CLI independentes que demonstram que a especificação é implementável e reduzem o custo de adoção para terceiros. Repositório: `normordis-tools` (separado desta especificação).

**Nota sobre linguagem de implementação (em aberto).** `ARCHITECTURE.md` §1
já fixa o princípio: ferramentas em qualquer linguagem são implementações de
referência substituíveis, nunca requisitos normativos — o contrato é o JSON
Schema, os algoritmos publicados (JCS/RFC 8785, SHA-256) e os vetores de
conformidade, já hoje verificados em paralelo por uma segunda implementação
em Node.js (`tools/check-jcs-vectors.mjs`, `tools/check-custody.mjs`, job
`conformance-js` do CI). Rust encaixaria da mesma forma — e é candidato
natural precisamente onde a exatidão de bytes importa mais (JCS, cadeia de
hash de custódia): tipagem forte, sem GC a interferir com serialização, e
crates maduras para JSON canónico e SHA-256. Sem decisão tomada; registado
aqui para quando `normordis-tools` (T1/T2) for iniciado.

### T1 — `normordis-validate`

**Prioridade: crítica.** A ferramenta mais importante para adoção.

Valida um NDF-core JSON contra:
1. JSON Schema (`ndf-core.schema.json`)
2. Regras semânticas que o schema não captura (ex.: condicionais RGPD, integridade de arquivo por `destino_final`)
3. Formato de `tipo_classificacao_ref`
4. Resolubilidade de `tipo_documento_ref` (se registry disponível)

```
normordis-validate ndf-core.json
normordis-validate --strict ndf-core.json     # inclui recomendados como obrigatórios
normordis-validate --suite conformance/ndf/   # corre toda a suite de conformidade
```

**Dependências**: JSON Schema Draft 2020-12; sem dependências de rede.

### T2 — `normordis-canonicalize`

**Prioridade: alta.** Elimina a principal causa de erros de assinatura.

Toma um NDF-core JSON e produz os bytes canónicos JCS (RFC 8785), o `payload_hash`, e o `validation_code`.

```
normordis-canonicalize ndf-core.json                  # escreve payload_bytes para stdout
normordis-canonicalize --hash ndf-core.json            # imprime payload_hash (hex)
normordis-canonicalize --validation-code ndf-core.json # imprime validation_code
normordis-canonicalize --all ndf-core.json             # imprime os três
```

**Dependências**: implementação JCS (RFC 8785); sem dependências de rede.

### T3 — `normordis-pack` / `normordis-inspect`

**Prioridade: média.** Torna o `.ndfpkg` concreto e utilizável.

`normordis-pack`: cria um `.ndfpkg` a partir dos constituintes.
`normordis-inspect`: lê e valida a integridade de um `.ndfpkg` existente.

```
normordis-pack --core ndf-core.json --envelope envelope.json \
               --ndt oficio-generico@2.0.0.ndt.json -o documento.ndfpkg

normordis-inspect documento.ndfpkg
normordis-inspect --verify documento.ndfpkg   # verifica hashes do inventário
```

**Dependências**: T1, T2; suporte a ZIP.

### T4 — `normordis-verify`

**Prioridade: média.** Verificação end-to-end da cadeia de autenticidade.

Toma um `.ndfpkg` e verifica:
1. `sha256(ndf-core.json) == payload_hash` do manifesto
2. Validade das assinaturas CAdES-B-LTA (quando presentes)
3. Validade dos timestamps RFC 3161
4. `validation_code` correcto

```
normordis-verify documento.ndfpkg
normordis-verify --offline documento.ndfpkg   # sem acesso a OCSP/CRL online
normordis-verify --at "2030-01-01" documento.ndfpkg  # verifica como se fosse nessa data
```

**Dependências**: T3; biblioteca CAdES; TSA trust store.

---

## Fase 3 — Verificação pública e especificação v1.1.0

### Portal `validar.normordis.pt`

Interface pública de verificação de `validation_code`. Um cidadão, auditor, ou sistema automatizado insere o código impresso num documento e obtém confirmação de autenticidade.

- Lookup de `validation_code` em base de dados de NDFs publicados
- Recalcula e compara `payload_hash` antes de responder
- Valida assinatura ou selo CAdES quando existente e distingue claramente
  documento assinado, selado e apenas sob custódia
- Devolve: entidade produtora, data, tipo, estado actual, resultado de
  integridade, resultado de autenticidade e nível de assinatura
- Para `nivel_assinatura: "nenhuma"`, a autenticidade institucional resulta da
  custódia do registo pelo portal; não é apresentada como assinatura pessoal
- API REST documentada (OpenAPI) para integração com outros sistemas
- Verificação offline descrita na página (não requer o portal)

**Dependências**: T4; infraestrutura NORMORDIS.

### NDF v1.1.0

| Item | Motivação |
|---|---|
| Agility de algoritmo criptográfico — mecanismo de re-selagem | CAdES-B-LTA mitiga mas não elimina o risco de SHA-256 comprometido a 20+ anos |
| Categorias especiais de dados (RGPD Art.º 9.º) | Dados de saúde, biométricos — schema mais granular em `metadados` |
| Registo remoto `registry.normordis.pt` | Resolução de `tipo_documento_ref` sem acesso ao `.ndfpkg` |
| Suporte a QSCD (eIDAS 2.0 / European Digital Identity Wallet) | Regulamento (UE) 2024/1183 em transposição |
| Extensão qualificada do vocabulário de `relacoes[].tipo` (A9, `LACUNAS.md` L4) | Vocabulário fechado hoje sem via de extensão institucional, inconsistente com o registo de tipos de documento |
| Eliminar a duplicação entre `referencia_externa` e `evidencia_ref` (`LACUNAS.md` L12) | Estruturas idênticas definidas em dois sítios desde a ronda de 2026-08-13; a fusão exige rever o bloco de proveniência de IA de propósito, não como efeito colateral |

---

## Fase 4 — Renderização

### T5 — `normordis-pdf`

**Prioridade: alta para adoção institucional.** A prova mais tangível de que o formato funciona.

Renderizador NDF + NDT → PDF/A-3 (ISO 19005-3). O PDF/A-3 é escolhido para que o NDF-core possa ser embebido como ficheiro anexo ao PDF, tornando o PDF autocontido (PDF + NDF-core no mesmo ficheiro).

```
normordis-pdf --core ndf-core.json --ndt oficio-generico@2.0.0.ndt.json -o documento.pdf
normordis-pdf --pkg documento.ndfpkg -o documento.pdf
normordis-pdf --embed-ndf --core ndf-core.json --ndt *.ndt.json -o documento.pdf  # PDF/A-3 com NDF embebido
```

**Ponto de partida**: os exemplos render-ready em `specs/ndf/examples/` e os NDTs em `specs/ndt/examples/` são o input de referência para validar o renderizador.

**Dependências**: T3; motor de layout (Pango/cairo ou equivalente); engine NDT.

---

## Fase 5 — Arquivo de longo prazo e extensibilidade

### T6 — `normordis-migrate`

**Prioridade: necessária quando SHA-256 se aproximar de fim de vida.** Prevista para ser necessária por volta de 2035–2040.

Re-selagem periódica: aplica novo timestamp de arquivo (com SHA-3 ou algoritmo posterior) sobre o envelope existente, sem alterar `payload_bytes`.

```
normordis-migrate --pkg documento.ndfpkg --tsa https://tsa.example.pt -o documento-migrado.ndfpkg
normordis-migrate --batch *.ndfpkg --out-dir migrado/
```

**Dependências**: T4; TSA com algoritmos de próxima geração.

### NDF v1.2.0

| Item | Motivação |
|---|---|
| Suporte multi-hash (`sha256` + `sha3-256` em paralelo) | Preparação para transição de algoritmo sem ruptura |
| Perfil de alta confidencialidade | Integração com DL n.º 11/2023 para documentos `secreto` / `muito_secreto` |

### NDF v2.0.0

| Item | Motivação |
|---|---|
| Extensões de namespace (`ext.<entidade>`) | Permite que AT, SS, Municípios estendam o NDF-core com campos próprios sem alterar esta especificação base |
| Espaço de nomes por entidade produtora em `ndf_id` (A10, `LACUNAS.md` L6) | Resolvido em conjunto com extensões de namespace, acima — evita duas rondas de alteração incompatível separadas |
| Revisão de `tipo_documento_ref` para URI formal | Alinhamento com Linked Data / European Interoperability Framework |

#### Generalização arquivística europeia — RESOLVIDO em 1.0.0 (2026-08-14)

Identificado em revisão externa (2026-08-08) e reidentificado em 2026-08-14: o
bloco `avaliacao` estava semanticamente acoplado ao modelo arquivístico
português (PCA, DF, Lista Consolidada, DGLAB, PGD, Tabela de Seleção).

Antecipado de v2.0.0 para **1.0.0** por decisão de 2026-08-14, com dois
fundamentos: o objetivo mais próximo passou a ser uma candidatura NGI/OSOR, de
âmbito europeu; e a alteração é incompatível, pelo que o seu custo é hoje o
mais baixo que alguma vez será — a especificação está em nível 1 — Draft, sem
revisão pública aberta e sem utilizadores externos.

A direção então esboçada — conceito abstrato + perfil PT/DGLAB — confirmou-se,
depois de verificado que o modelo português é uma instância de um padrão
europeu comum e não uma idiossincrasia. Resultado: `avaliacao.perfil` com
schemas em `specs/registry/profiles/`, renomeação dos campos cujo nome era um
termo legal português, e o valor `destino_final: "a_determinar"` para os
sistemas em que a decisão não compete ao produtor. Ver ADR-015 e
`docs/design/NDF-AVALIACAO-GENERALIZATION.md`.

Fica em aberto, sem prazo: publicar schemas de perfil para outras jurisdições
(`fr-siaf`, `de-barch`, `nl-na`, `eu-ec`). O mapeamento jurídico já está feito e
verificado contra fonte primária em [`docs/profiles/`](docs/profiles/README.md);
o que falta é evidência de que exista sintaxe nacional passível de ser imposta
por schema — que só se confirmou para Portugal — e, de preferência, confirmação
por interlocutor de cada jurisdição. É acréscimo ao registo, não alteração
incompatível do NDF-core.

### NCRTF v2.0.0 ✅

NORMORDIS Canonical Rich Text Format — conteúdo de texto estruturado para campos `corpo` e equivalentes. Independente de editores (Lexical, ProseMirror, etc.); canonicalizável via JCS/RFC 8785; armazenado diretamente como valor JSON no NDF-core (por exemplo, `documento.corpo`). Suporta parágrafos, títulos, listas, tabelas, imagens por referência, citações e marcas inline. NDTs referenciam conteúdo NCRTF por caminhos relativos a `NDF-core.documento`.

---

## Fase 6 — Normalização técnica

**Objetivo expresso do projeto**: NDF, NDT e NCRTF tornarem-se standards técnicos sérios — NP (Norma Portuguesa), EN (Norma Europeia), ou ISO/IEC — adoptáveis por terceiros sem dependência da implementação NORMORDIS.

### Caminho de normalização

```
NP — via IPQ/Comissão Técnica competente
EN — via CEN/Comité Técnico competente
ISO — via membro nacional e ISO/TC competente (provavelmente TC 46/SC 11 e/ou TC 171)

Estas vias não formam uma sequência obrigatória. O projeto pode começar em
Portugal, seguir em paralelo com CEN ou ser proposto diretamente ao comité ISO
competente, desde que demonstre necessidade de mercado e obtenha apoio dos
membros.
```

### Estado da maturidade arquitectural (2026-06-22)

O conjunto NDF + NDT + NCRTF tem hoje a profundidade técnica necessária:

| Critério | Estado |
|---|---|
| Separação de âmbitos | ✅ Definida; revisão cruzada contínua |
| Referências a standards reais (ISO 14289-2, ISO 19005-3, ETSI EN 319 122, ISO/IEC 26300) | ✅ Completo |
| Cláusulas de conformidade com comportamento observável | Parcial; falta inventário requisito a requisito |
| Schema legível por máquina (JSON Schema Draft 2020-12) | ✅ NDF-core + envelope + manifest + NDT + NCRTF + registry (4 tipos) |
| Exemplos concretos validados contra schema | ✅ NDT + NDF, incluindo render-ready Modelo 3 IRS |
| Suite de conformidade executável com CI | ✅ 50/50 testes, pipeline verde em cada push |
| Termos e modelo de endereçamento canónico | Parcial; falta converter glossários para termos e definições controlados |

### Gaps editoriais para normalização

O trabalho restante é editorial, processual e de validação independente. Não
estão previstas alterações arquiteturais de fundo, mas a revisão pode revelar
correções técnicas.

| Gap | O que é necessário |
|---|---|
| **Linguagem normativa** | Aplicar a política editorial e eliminar formas normativas ambíguas nos três textos |
| **Secção "Termos e definições"** | Formato ISO 10241 (não glossário livre) — entradas com forma verbal, domínio, definição, nota |
| **Secção "Referências normativas"** | Secção própria com citações ISO formais (número, título, ano); separar de referências informativas |
| **Suite de conformidade executável** | Runner automatizado existente; expandir até cobrir cada requisito individualmente |
| **Implementações e adoção independente** | Produzir evidência de implementabilidade e necessidade de mercado; múltiplas implementações são desejáveis, mas não constituem requisito ISO universal |
| **Estrutura de anexos** | Distinguir Annex A normativo de Annex B informativo; mover exemplos para anexo informativo |
| **Versão inglesa** (D3, `R3`) | Não existe hoje um único ficheiro `.en.md`. Âmbito mínimo: `README.en.md` e abstract/âmbito das três SPECs; tradução integral depois, apoiada na base terminológica bilingue. Bloqueante para avaliação externa e para qualquer via CEN/ISO |

### Pré-requisitos antes de submeter a NP

1. **Congelamento editorial** — NDF, NDT e NCRTF com linguagem e estrutura uniformes
2. **Suite de conformidade executável** — runner existente ✅, a expandir até cobrir cada requisito normativo
3. **Implementação e pilotos independentes** — evidência recomendada de implementabilidade, interoperabilidade e necessidade real
4. **Base terminológica bilingue** — necessária para uma tradução controlada; não é apresentada como requisito ISO universal

### Estimativa de esforço editorial (passagem de especificação draft → NP)

| Tarefa | Estimativa |
|---|---|
| Reformatar linguagem RFC 2119 nos três specs | 2–3 sessões |
| Criar secção "Termos e definições" ISO | 1 sessão |
| Criar secção "Referências normativas" | 1 sessão |
| Reorganizar anexos (normativos vs. informativos) | 1 sessão |
| Suite de conformidade executável (requer T1) | depende de Fase 2 |

---

## Dependências entre ferramentas

```
T2 (canonicalize)
    └── T1 (validate)
            └── T3 (pack/inspect)
                    └── T4 (verify)
                            ├── Portal validar.normordis.pt
                            └── T6 (migrate)
T5 (pdf) ← T3

normordis-spec (esta repo) ← todas as ferramentas (implementam a especificação)
```
