# Plano de ação — captura documental e `.ndfpkg`

**Estado:** plano de execução. Não normativo.
**Data:** 2026-08-20
**Âmbito:** tipo documental de captura, composição do `.ndfpkg`, requisitos de
pacote e de leitor. **O NDF-core não é alterado** — a capacidade entra por
`tipo_documento_ref` mais schema próprio, que o [`ROADMAP.md`](../../ROADMAP.md)
classifica expressamente como não sendo alteração de formato. A única excepção
é o alargamento de SPEC §2.8, tratado no Bloco 0.

**Fundamentação:** [`docs/design/NDFPKG-CAPTURA-E-INGESTAO.md`](../design/NDFPKG-CAPTURA-E-INGESTAO.md)
— porquê de cada decisão. Este plano não repete argumentos; executa-os.

**Fora deste repositório:** pipeline de ingestão, `BlobRepository`, storage,
filas, cliente. Ver `HANDOFF-KERNEL-CORE-INGEST.md`, destinado a
`normordis-kernel`.

---

## 1. Ponto de partida

**O que existe:** NDF-core estável com envelope genérico e `documento` opaco
tipado por schema (SPEC §2.9.1); `.ndfpkg` autocontido com inventário fechado e
verificação de hash por ficheiro; nove vetores negativos de pacote; suite verde.

**O que falta, e é o objeto deste plano:**

| Lacuna | Consequência |
|---|---|
| Não existe tipo documental para documento não nascido no editor estruturado | O fluxo real dos serviços (`Word → PDF`) não tem representação NDF |
| Um binário não pode ser vinculado aos bytes assinados | A preservação de um documento capturado fica sem fundamento criptográfico |
| `ndt_version_ref` é obrigatório e um capturado não tem template | O tipo não pode existir sem resolver isto |
| Assinatura externa preservada em bytes, não em verificabilidade | «Preservação» que caduca com os certificados |
| Cadeia de custódia não acompanha o pacote | Transferência entre entidades incompleta (§11.2 do desenho, L-T2) |

## 2. Princípios de execução

Não renegociáveis durante o plano:

1. **Dever do formato é capacidade de representação**, não imposição de
   qualidade. Se algo relevante não tem onde ser guardado, é lacuna do formato;
   se tem lugar e vem mal preenchido, é do produtor (`CAP-03`).
2. **Fidelidade ao emitido.** O sistema não corrige, não normaliza, não completa
   e não reescreve (`CAP-04`).
3. **Teste de admissão** — caso de uso documentado, ou não entra (ADR-015).
4. **Verificabilidade** — requisito sem imposição é intenção.
5. **O que se decide dentro do artefacto pode ser conformidade; o que exige o
   mundo é do produtor** (§7.4 do desenho).

### 2.1 Definition of Done

Nenhuma tarefa está concluída sem os nove passos:

1. decisão registada na cláusula 3 com identificador `CAP-*`;
2. cláusula na SPEC, com modal BCP 14 em maiúsculas;
3. schema atualizado;
4. requisito com identificador novo;
5. vetor válido **e** vetor inválido com `_expected_match` que prove a regra;
6. índices regenerados (`REQUIREMENTS.md`, `NORMATIVE-STATEMENTS.md`, `conformance/INDEX.md`);
7. `check_spec_coherence.py` verde;
8. entrada no CHANGELOG;
9. suite completa verde.

Tarefas puramente doutrinárias (ADR, decisão de governação) cumprem 1, 8 e 9.

---

## 3. Registo de decisões

Consolidação do brainstorming de 2026-08-20. Coluna «Onde» remete para a
secção do documento de desenho.

### 3.1 Enquadramento e âmbito

| ID | Decisão | Onde |
|---|---|---|
| `CAP-01` | **Um só formato.** O NDF cobre documento nativo e capturado; não há formato separado para importados | §3 |
| `CAP-02` | `documento-capturado@1.0.0` é **tipo documental**, exercício de SPEC §2.9.1 — não alteração do core | §3 |
| `CAP-03` | **Dever do formato = capacidade de representação**; correção do que se representa = do produtor | §7.4 |
| `CAP-04` | **Fidelidade ao emitido**: não corrigir, não normalizar, não completar, não reescrever | §7.4 |
| `CAP-05` | O alargamento de SPEC §2.8 é **decisão de âmbito**, registada como tal — não clarificação editorial | §9 |

### 3.2 Vias de produção

| ID | Decisão | Onde |
|---|---|---|
| `CAP-06` | **Produção interna:** PDF/A exportado pelo próprio produtor. Não se capturam `.odt`/`.docx` nesta via | §2 |
| `CAP-07` | **Receção externa:** preservar byte a byte o que chegou, seja qual for o formato | §2.2 |
| `CAP-08` | Representação canónica **só quando necessária**; nunca substitui o original | §2.2 |
| `CAP-09` | **Nunca reescrever** binário assinado externamente | §6 |
| `CAP-10` | O **estado** da estratégia de reconstituição é sempre expressável — adequada, com deficiência, ou **ausente** | §7.3 |

### 3.3 Estrutura

| ID | Decisão | Onde |
|---|---|---|
| `CAP-11` | Componentes declarados em **`documento`** — nunca no manifesto, nunca no envelope. É a única colocação em que ficam assinados | §4 |
| `CAP-12` | **Nenhuma** referência de storage, URI, bucket ou nome de adapter no formato | §4 |
| `CAP-13` | **Um** tipo genérico, não uma família. `tipo_equivalente` opcional transporta a correspondência | §3.8, §3.9 |
| `CAP-14` | NDT `documento-capturado@1.0.0` = **auto de captura**; resolve `ndt_version_ref` sem tocar no core | §5 |
| `CAP-15` | Componente vs documento autónomo decide-se por **identidade documental/processual**, não por ter assinatura | §3 do handoff |
| `CAP-16` | Todos os componentes declarados **integram sempre** a materialização; sem omissão automática | §11.1 |
| `CAP-17` | `.ndfpkg` materializado é **sempre autocontido**; não implementar pacote fino/cheio nem flag de estado | §11.1 |

### 3.4 Assinatura e prova

| ID | Decisão | Onde |
|---|---|---|
| `CAP-18` | `nivel_assinatura` **nunca se herda** de um componente | §6 |
| `CAP-19` | PAdES **preservado** quando chega; produzido internamente é conveniência de distribuição, não a prova canónica | §6 |
| `CAP-20` | Ordem obrigatória: assinar o PDF → hash do PDF **já assinado** → ancorar no core → finalizar | §6 |
| `CAP-21` | Material de validação de assinatura externa **congelado na captura** (`evidencias/`) | §6.1 |

### 3.5 Fronteiras

| ID | Decisão | Onde |
|---|---|---|
| `CAP-22` | Texto extraído é **dado derivado**, fora do NDF-core e fora do pacote legal | §7.1 |
| `CAP-23` | Sugestão de IA vive no workflow; o recetáculo canónico pós-validação **já existe** (`proveniencia_ia`) | §7.2 |
| `CAP-24` | Divergência metadados/binário: o **binário** é autoritativo quanto ao conteúdo do ato; o **NDF** quanto a identidade, custódia e classificação | §3.9 |
| `CAP-25` | Um leitor conforme **NÃO DEVE** renderizar um capturado aplicando o NDT a `documento` — tem de resolver o componente | §7.4 |

### 3.6 Ingestão e governação

| ID | Decisão | Onde | Executa |
|---|---|---|---|
| `CAP-26` | Validação de formato é **política de ingestão recomendada**, não requisito de conformidade NDF | §2.4 | kernel |
| `CAP-27` | Receção externa: **sempre aceite** com deficiência registada; nunca fundamento de recusa da submissão | §2.4 | kernel |
| `CAP-28` | Produção interna: controlo de qualidade **a montante da emissão**, não recusa do formato | §2.4 | kernel |
| `CAP-29` | Governação pelo **registo de tipos versionado**: declara via predefinida e admissibilidade de captura; transição tipo a tipo | §8 | formats |
| `CAP-30` | A proporção estruturado/capturado por tipo é o **instrumento de progresso** do editor | §8 | kernel |

### 3.7 Custódia

| ID | Decisão | Onde |
|---|---|---|
| `CAP-31` | A eliminação destrói **também os componentes** e regista o facto | §7.6 |

---

## 4. Bloco 0 — decisões que desbloqueiam

Sem estas, a Fase A não arranca.

| # | Tarefa | Produz | Estado |
|---|---|---|---|
| **0.1** | Alargamento de SPEC §2.8 registado como decisão de âmbito (`CAP-05`) | `ROADMAP.md`, secção «Alcance de D5» | ✅ 2026-08-20 |
| **0.2** | Perfil PDF/A alvo fixado (`CAP-06`) | desenho §2.4.1 | ✅ 2026-08-20 |
| **0.3** | Instrumento de governação no registo de tipos (`CAP-29`) | `specs/registry/SPEC.md` §3.2 | ✅ 2026-08-20 |
| **0.4** | Colocação normativa da regra de divergência (`CAP-24`) | decidida: §2.8 alargada, tarefa C1 | ✅ 2026-08-20 |
| **0.5** | **Dono e periodicidade da métrica estruturado/capturado** (`CAP-30`, Q7) | decisão do responsável | 🔎 **a verificar** |

**0.1 condiciona C1 — desbloqueado. 0.3 condiciona B2 — desbloqueado.**

`0.5` não bloqueia a Fase A nem a Fase B: o mecanismo existe (registo §3.2.3,
roquete), falta nomear quem o observa. Bloqueia a operação, não a
implementação — mas fica em aberto, não fechado por omissão.

## 5. Fase A — fundamentação normativa

Sem schema nem código. Fixa o desenho antes de o implementar.

| # | Tarefa | Produz | Decisões | Estado |
|---|---|---|---|---|
| **A1** | ADR — um só formato, duas realidades | [`ADR-020-um-formato-duas-realidades.md`](../architecture/ADR-020-um-formato-duas-realidades.md) | `CAP-01` `CAP-02` `CAP-13` | ✅ 2026-08-20 |
| **A2** | ADR — componentes nos bytes assinados | [`ADR-021-componentes-nos-bytes-assinados.md`](../architecture/ADR-021-componentes-nos-bytes-assinados.md) | `CAP-11` `CAP-12` | ✅ 2026-08-20 |
| **A3** | ADR — dever do formato e responsabilidade do produtor | [`ADR-022-dever-do-formato.md`](../architecture/ADR-022-dever-do-formato.md) + `ARCHITECTURE.md` §1.1 | `CAP-03` `CAP-04` | ✅ 2026-08-20 |
| **A4** | Cláusula — assinaturas contidas em componentes | SPEC NDF §4.5.1 | `CAP-18` `CAP-19` `CAP-20` `CAP-09` | ✅ 2026-08-20 |
| **A5** | Mapeamento PREMIS/METS ↔ papéis de componente | [`PREMIS-METS-MAPPING.md`](../interoperability/PREMIS-METS-MAPPING.md) | `CAP-15` | ✅ 2026-08-20 |

**Numeração de ADR:** `ADR-018` e `ADR-019` estão reservados pelo
[`PLANO-NDT-NCRTF.md`](PLANO-NDT-NCRTF.md) (Bloco 0). Esta ronda arranca em
`ADR-020`.

**Saída de A5 que entra em B1** — enum `papel` derivado, não inventado:

| `papel` | Uso |
|---|---|
| `original` | bytes tal como emitidos ou recebidos; sempre preservados |
| `representacao_congelada` | derivada de um `original` para fidelidade visual; nunca o substitui |
| `anexo` | componente de apoio sem identidade documental própria |
| `evidencia` | material de validação de assinatura contida, congelado na captura |

Consequência que dispensa caso especial: **a via de produção interna tem um só
componente**, com `papel: "original"` — nada foi congelado a partir de outra
coisa. O colapso entre original e representação canónica (`CAP-08`) deixa de ser
regra separada e passa a ser ausência de um valor.

**Dívida assumida:** A4 introduz prosa normativa em §4.5.1 sem requisito
enumerado. Os identificadores correspondentes entram em C4/C5 e os vetores em
D2 — é a organização própria da SPEC, que separa prosa normativa (corpo) de
requisitos enumerados (§9), não uma omissão.

## 6. Fase B — tipo documental e template

| # | Tarefa | Produz | Decisões | Estado |
|---|---|---|---|---|
| **B1** | Schema do tipo capturado | [`documento-capturado.schema.json`](../../specs/registry/schemas/documento-capturado.schema.json) | `CAP-10` `CAP-11` `CAP-13` `CAP-21` `CAP-24` | ✅ 2026-08-20 |
| **B2** | Entrada no registo + valores recomendados de governação | `specs/registry/SPEC.md` §3, §3.2.4 | `CAP-29` | ✅ 2026-08-20 |
| **B3** | NDT do auto de captura | [`documento-capturado.ndt.json`](../../specs/ndt/examples/documento-capturado.ndt.json) | `CAP-14` | ✅ 2026-08-20 |
| **B4** | Extensão qualificada `ext.<entidade>.instrui` | SPEC NDF §2.11.7 | — | ✅ 2026-08-20 |

**Seis regras condicionais impostas por B1**, cada uma com caso negativo
verificado: `representacao_congelada` sem `derivado_de`; `reconstituicao`
não-adequada sem `fundamento`; `validacao_formato` com resultado apurado sem
validador nem instante; `canal: "outro"` sem detalhe; `componentes` vazio;
`papel` fora do enum.

**Decisão de desenho tomada em B1 — resolução por hash, nunca por caminho.**
Um componente não declara o seu lugar no pacote. `nome_original` é descritivo e
um leitor não o DEVE usar para resolver o componente; a correspondência com
`manifest.inventario` faz-se pelo digest. Declarar o caminho poria a disposição
física do pacote dentro dos bytes assinados, e o mesmo documento materializado
de outra forma teria assinatura diferente.

### 6.1 Achados sobre o NDT 2.0.0

A construção do auto de captura expôs duas limitações reais do NDT — o género
de evidência que o [`ROADMAP.md`](../../ROADMAP.md) procura («o que é que uma
implementação real não consegue fazer»). Nenhuma bloqueou B3; ambas foram
contornadas e ficam registadas para o
[`PLANO-NDT-NCRTF.md`](PLANO-NDT-NCRTF.md):

| # | Limitação | Contorno usado |
|---|---|---|
| **N-C1** | `FormatoDisplay` não tem valor para data e hora — só `data`. Um auto de captura precisa do **instante** de entrada, não do dia | `formato: "texto"`, que rende o ISO 8601 completo. Preciso, mas não localizável |
| **N-C2** | `incluir_se` não suporta negação. Não é exprimível «mostrar este texto quando o bloco estiver ausente» | Elemento removido. A ausência de proveniência de submissão deixa de ser explicada no auto |

N-C1 tem impacto para além da captura: qualquer documento que precise de
carimbo temporal legível tem hoje o mesmo problema.

## 7. Fase C — especificação e pacote

| # | Tarefa | Produz | Decisões | Estado |
|---|---|---|---|---|
| **C1** | §2.8 alargada — componentes por hash; proibição recai sobre bytes embutidos | SPEC §2.8.1 | `CAP-05` `CAP-12` | ✅ 2026-08-20 |
| **C2** | Composição do pacote com os quatro diretórios de papel | SPEC §8.1 | `CAP-16` `CAP-21` | ✅ 2026-08-20 |
| **C3** | Coerência `componentes[].sha256` ↔ `manifest.inventario` | `NDF-PKG-009` | `CAP-11` | ✅ 2026-08-20 |
| **C4** | Requisitos de leitor | `NDF-READ-021/022/023` | `CAP-25` `CAP-18` | ✅ 2026-08-20 |
| **C5** | Requisitos de produtor | `NDF-PROD-020/021/022` | `CAP-04` `CAP-09` `CAP-12` | ✅ 2026-08-20 |
| **C6** | Regra de divergência, absorvida por C1 conforme 0.4 | SPEC §2.8.2 | `CAP-24` | ✅ 2026-08-20 |

**Sete identificadores novos** — o inventário normativo passa de 93 para 100 IDs
e de 274 para 285 declarações. `NDF-PKG-009` foi usado por estar livre: não
existia nem fora retirado, e deixar lacuna na numeração seria ruído.

**`manifest.schema.json` não foi alterado**, como ADR-021 previa. O inventário
já cobre a integridade física de qualquer ficheiro do pacote; o que faltava era
a ligação à declaração assinada, e essa é `NDF-PKG-009`.

**Dívida de A4 saldada:** os identificadores prometidos existem. Faltam os
vetores que os provam — `NDF-PKG-009` tem imposição em D2/D3, e
`NDF-PROD-020/022` e `NDF-READ-021/022/023` são regras de comportamento cuja
evidência depende de produtor e leitor conformes, como já sucede com a maioria
dos `NDF-READ-*`.

**C3 é a única junta verificável genuinamente nova.** O inventário do manifesto
já cobre a integridade física de qualquer ficheiro do pacote
([`tools/validate.py`](../../tools/validate.py)); o que falta é ligar essa
integridade à declaração assinada.

## 8. Fase D — exemplos e conformidade

| # | Tarefa | Produz | Esforço |
|---|---|---|---|
| **D1** | Exemplo completo de captura, com PDF/A mínimo reproduzível | `specs/ndf/examples/captura-requerimento/` | G |
| **D2** | Vetores negativos: componente declarado ausente do pacote; hash divergente entre `documento` e inventário; ficheiro em `original/` não declarado como componente; original reescrito; capturado sem estado de reconstituição | `conformance/package/` | M |
| **D3** | `validate.py` valida componentes e a junta C3 | `tools/validate.py` | M |
| **D4** | Regenerar índices e fechar a fase | `REQUIREMENTS.md`, `TRACEABILITY.md`, `NORMATIVE-STATEMENTS.md`, `conformance/INDEX.md` | P |

## 9. Fase E — custódia

| # | Tarefa | Produz | Decisões | Esforço |
|---|---|---|---|---|
| **E1** | Evento de captura no log de custódia | `custody-event.schema.json` | — | P |
| **E2** | Eliminação abrange componentes; `CUST-REQ-003` estendido | schema + SPEC §9.5 | `CAP-31` | M |
| **E3** | Separar **evidência transferível** (finalização, selagens, verificações, transferências) de **auditoria interna** (acessos) | nota de desenho + schema | — | M |

**E3 deixou de ser opcional.** Pelo critério `CAP-03`, a cadeia de custódia é
informação relevante e necessária que hoje **não pode** acompanhar uma
transferência — logo é lacuna do formato, não da operação (desenho §11.2, L-T2).

## 10. Trilha paralela

| # | Tarefa | Porquê | Esforço |
|---|---|---|---|
| **P1** | Doutrina de projeto sobre **o que o NORMORDIS diz quando algo passa** — nunca «válido» sem dizer o que foi verificado | Três manifestações do mesmo risco: `validation_code`, rótulo igual para duas realidades, formulário a verde (desenho §7.4.3) | M |
| **P2** | Documento de desenho do **conjunto de transferência** (L-T1 a L-T4) | Fecha `R13`, abre a conversa com a DGLAB (`R5`). Trabalho de mapeamento, não de invenção | G |
| **P3** | Mover `HANDOFF-KERNEL-CORE-INGEST.md` para `normordis-kernel` | Impede que arquitetura de aplicação contamine a especificação | P |

## 11. Sequência

```
Bloco 0 ──► Fase A ──► Fase B ──► Fase C ──► Fase D
   │          │           │
   │          └── A5 ─────┘  (informa o enum de papéis em B1)
   │
   ├── 0.1 ──────────────────────► C1
   └── 0.3 ─────────► B2

Fase E ─── depende de B1; E3 alimenta P2

P1, P3 ─── independentes, arrancam já
P2  ─────── depois de E3
```

**Ordem interna da Fase C:** C1 → C2 → C3 → C4/C5/C6. Da mais estrutural para a
mais declarativa, para que os vetores da Fase D sejam escritos uma só vez.

**Relação com o caminho crítico do repositório:** este plano **não compete** com
`R8`. A via capturada não precisa de renderizador — o PDF já existe. Pode
portanto correr em paralelo com `normordis-pdf`, e é provavelmente o caminho
mais rápido até um utilizador institucional real (`R5`, gate 7). Não substitui
`R8` para efeitos de abertura de PR-001, e não deve ser apresentada como se
substituísse.

## 12. Cobertura — nenhuma decisão sem destino

| Decisão | Implementada em | Decisão | Implementada em |
|---|---|---|---|
| `CAP-01` | A1 | `CAP-17` | doutrina; kernel executa |
| `CAP-02` | A1, B1 | `CAP-18` | A4 |
| `CAP-03` | A3 | `CAP-19` | A4 |
| `CAP-04` | A3, C5 | `CAP-20` | A4; kernel executa |
| `CAP-05` | 0.1, C1 | `CAP-21` | B1, C2 |
| `CAP-06` | 0.2; kernel executa | `CAP-22` | C1 (cláusula negativa) |
| `CAP-07` | C1, C5 | `CAP-23` | sem trabalho — recetáculo existe |
| `CAP-08` | B1 (estado), C2 | `CAP-24` | 0.4, C6 |
| `CAP-09` | C5 | `CAP-25` | C4 |
| `CAP-10` | B1 | `CAP-26` | kernel |
| `CAP-11` | A2, B1, C3 | `CAP-27` | kernel |
| `CAP-12` | A2 (cláusula negativa) | `CAP-28` | kernel |
| `CAP-13` | A1, B1 | `CAP-29` | 0.3, B2 |
| `CAP-14` | B3 | `CAP-30` | 0.3 (quem olha), kernel |
| `CAP-15` | A5, B1 | `CAP-31` | E2 |
| `CAP-16` | C2 | | |

Sete decisões (`CAP-06`, `CAP-17`, `CAP-20`, `CAP-26` a `CAP-28`, `CAP-30`)
executam-se no `normordis-kernel`; ficam aqui registadas para que a fronteira
seja explícita e não se percam por não terem dono neste repositório.

## 13. Riscos

| Risco | Mitigação |
|---|---|
| **Implementar o schema antes de fixar a doutrina** — B1 sem A1–A3 produz campos sem critério | Fase A é pré-requisito duro; não é documentação a posteriori |
| **A Fase B cresce por arrasto** — o tipo de captura acumula campos «já agora» | Teste de admissão tarefa a tarefa; `CAP-13` proíbe a família de tipos |
| **O regime de transição torna-se permanente por inércia** | `CAP-30` com dono nomeado em 0.3; sem dono, a métrica não é olhada |
| **Validação estrutural lida como correção substantiva** | P1, tratado como resposta única e não como três remendos |
| **0.1 tratado como clarificação editorial** | Registo explícito no `ROADMAP.md` como decisão de âmbito, com fundamentação |
| **E3 adiado** e a cadeia de custódia nunca viaja | Reclassificado como lacuna do formato por `CAP-03`; não é item opcional |
| **Dimensão da materialização** com scan extenso ou gravação | Q4 em aberto; assumir no perfil de custódia, não no formato |
| **A captura absorve o esforço** e o editor estruturado estagna | `CAP-30` mede-o; se a proporção não descer, o problema é de investimento, não de formato |

## 14. O que este plano não faz

- **Não altera o NDF-core.** A capacidade entra por tipo documental. A única
  excepção é o alargamento de §2.8, decidido em 0.1 com registo próprio.
- **Não implementa o core-ingest.** Pipeline, storage, filas e cliente vivem no
  `normordis-kernel` (P3).
- **Não define o conjunto de transferência.** É trabalho adjacente com documento
  próprio (P2), embora E3 o prepare.
- **Não decide política de arquivo** — normalização de imagens recebidas, perfis
  de preservação. Gate externo 3, com a DGLAB.
- **Não abre a revisão pública** nem altera o estado editorial das SPECs.
- **Não substitui `R8`.** A condição de abertura de PR-001 mantém-se inalterada.
