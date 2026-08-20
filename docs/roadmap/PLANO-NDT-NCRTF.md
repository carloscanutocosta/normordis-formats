# Plano de ação — NDT e NCRTF

**Estado:** plano de execução. Não normativo.
**Data:** 2026-08-17
**Âmbito:** NDT 2.x e NCRTF 2.x. O NDF-core não é tocado — permanece congelado
pela D5 ([`ROADMAP.md`](../../ROADMAP.md)).

**Fundamentação:** [`docs/design/CRITERIO-DE-CAMADAS.md`](../design/CRITERIO-DE-CAMADAS.md)
(onde cada coisa vive e porquê) e
[`docs/design/ODF-ALIGNMENT-STUDY.md`](../design/ODF-ALIGNMENT-STUDY.md)
(o que falta e que vocabulário serve de referência).

---

## 1. Ponto de partida

**Estabilizado** (rondas de 2026-08-17):

- NDT com 19 requisitos de produtor e 11 de renderizador, todos com identificador;
- as nove regras estruturais que existiam só em prosa passaram a ter imposição
  em schema ou validador, com caso negativo cada;
- cada `versao_ndt` é uma unidade autónoma — sem requisitos de compatibilidade
  entre versões de um template;
- guardrails de coerência SPEC↔schema↔exemplos ativos para NDT e NCRTF.

**Por implementar** — e é o objeto deste plano:

| Lacuna | Consequência |
|---|---|
| NCRTF sem notas, remissões e numeração por nível | um diploma legal não cabe no formato |
| NDT sem estilos de parágrafo e sem controlo de paginação fina | texto corrido não sai publicável |
| Nenhum renderizador conforme | `NDT-RENDER-*` sem evidência; nenhuma alegação de interoperabilidade se sustenta |

## 2. Princípios de execução

Herdados das rondas anteriores e não renegociáveis durante este plano:

1. **Teste de admissão** — caso de uso documentado, ou não entra (ADR-015).
2. **Camada determinada pelo critério**, não pela conveniência de implementação:
   o conteúdo declara o que a coisa **é**, o template declara como se **vê**.
3. **Desenho correto antes de compatível** — enquanto durar a janela da
   cláusula 2.2. Uma alteração incompatível custa hoje o mesmo que uma aditiva.
4. **Verificabilidade** — requisito sem imposição é intenção. Foi o que esta
   ronda teve de corrigir; não se repete.
5. **IDs retirados não se reutilizam.** `NDT-PROD-020` e `NDT-PROD-021` foram
   removidos: a numeração de novos requisitos NDT começa em **`NDT-PROD-022`**.

### 2.2 Janela de desenho livre

**Premissa, verificada em 2026-08-17:** os três formatos estão em *"Draft —
revisão pública por abrir"*; o único renderizador de layout posicionado é um
stub que devolve erro (`ROADMAP.md`, R15); não existe implementação de terceiros
nem documento produzido em ambiente real. **Nada externo depende do desenho
atual.**

Enquanto isto se mantiver, a retrocompatibilidade não é um constrangimento: uma
correção incompatível custa o mesmo que uma adição. É preferível corrigir agora
o que está errado do que carregá-lo como legado.

**A janela fecha** quando ocorrer o primeiro de: abertura da revisão pública, ou
existência de uma implementação de terceiros. A partir daí volta a valer a
disciplina de aditividade e o versionamento SemVer do formato. **As decisões
abaixo devem ser tomadas antes disso** — depois, o custo muda de natureza.

| # | Oportunidade | Justificação | Estado |
|---|---|---|---|
| **O1** | Remover `font_family`, `alignment` e `indent` do NCRTF | Apresentação dentro do payload assinado, do lado errado da fronteira ([estudo ODF §7.1](../design/ODF-ALIGNMENT-STUDY.md)). Estava previsto ficar como legado até uma eventual v3.0; sem implementações, remove-se já | a decidir em 0.2 |
| **O2** | Promover os papéis semânticos (ex-C1) da Fase C para a Fase A | Faz par com O1: retira-se apresentação, dá-se semântica. Isolados, nenhum dos dois é coerente | a decidir em 0.2 |
| **O3** | Remover `descontinuado` do schema NDT | Com templates autónomos (§8.2) e sem retrocompatibilidade a preservar, não serve nenhum caso concreto | a decidir em 0.2 |
| **O4** | Reavaliar as `marks` de apresentação (`bold`, `italic`, `underline`) face a alternativas semânticas (`emphasis`, `strong`) | Coerente com O1, mas de alcance muito maior e com custo de usabilidade em editores. Decidir com consciência, não por arrasto | **em aberto** |
| **O5** | Renumerar ou reorganizar famílias de requisitos | Só possível agora. Contrapeso: a numeração atual já está em quatro commits e nos índices gerados | recomendação: **não** |
| **O6** | Absorver as alterações em `2.0.0` em vez de publicar `2.1.0` | Nada publicado depende de `2.0.0`; o bump sinalizaria uma compatibilidade que ninguém precisa | a decidir em A4 |

Sobre **O5**: manter a numeração custa pouco e a disciplina de não reutilizar
identificadores tem valor mesmo sem consumidores externos — é o que torna os
CHANGELOGs legíveis. Recomenda-se manter, e manter também `NDT-PROD-020/021`
como retirados.

### 2.1 Definition of Done

Nenhuma tarefa está concluída sem os oito passos:

1. cláusula na SPEC, com modal BCP 14 em maiúsculas;
2. schema atualizado;
3. requisito com identificador novo;
4. vetor válido **e** vetor inválido com `_expected_match` que prove a regra;
5. índices regenerados (`REQUIREMENTS.md`, `NORMATIVE-STATEMENTS.md`, `conformance/INDEX.md`);
6. `check_spec_coherence.py` verde — apanha exemplos da SPEC que a alteração invalide;
7. entrada no CHANGELOG do formato;
8. suite completa verde.

## 3. Bloco 0 — decisões que desbloqueiam (pré-requisito de tudo)

Sem estas decisões registadas, a Fase A não arranca: determinam em que
especificação entra o quê.

| # | Tarefa | Produz | Esforço |
|---|---|---|---|
| **0.1** | Verter o critério de camadas para decisão arquitetural | `ADR-018-criterio-de-colocacao-por-camada.md` + cláusula em `ARCHITECTURE.md` | P |
| **0.2** | Fixar a fronteira de estilo: papel semântico no NCRTF, apresentação no NDT; estilos nomeados e planos, um nível de herança. **Decide O1, O2 e O3** da cláusula 2.2 | `ADR-019-fronteira-de-estilo.md` | M |
| **0.3** | Confirmar o vocabulário ODF cláusula a cláusula contra ODF 1.3 Parte 3 / ISO 26300 — em especial `text:reference-format`, não confirmado | nota de verificação em `ODF-ALIGNMENT-STUDY.md` §10.5 | P |
| **0.4** | Registar a relação com o ODF em propriedade intelectual e referências normativas | `IPR-DECLARATIONS.md`, `NORMATIVE-REFERENCES.md` | P |

**0.2 condiciona o desenho de toda a Fase A**: mesmo que os estilos nomeados só
cheguem na Fase C, a Fase A não deve introduzir mecanismos que os impeçam.

## 4. Fase A — texto normativo

**Objetivo:** um diploma legal cabe no formato. Fecha os pontos 1 a 3 da
cláusula 3 do estudo ODF.
**Entrega:** NCRTF v2.1 e NDT v2.1, publicados em conjunto.

### A1 — Notas de rodapé e de fim

Referência ODF: `text:note` (`text:note-class`, `text:note-citation`, `text:note-body`).

| | |
|---|---|
| **NCRTF** | novo nó **inline** `note`, com corpo de nós bloco. Decisão de desenho a tomar: corpo aninhado no ponto de ocorrência (modelo ODF) *ou* âncora inline com corpo em coleção à parte. Recomendação: modelo ODF — mantém o texto da nota junto do sítio onde ocorre, ao custo de recursão bloco-dentro-de-inline |
| **Canonicalização** | R2 (fusão de nós `text` contíguos) **não atravessa** fronteira de nota. Regra nova explícita em §8.2 do NCRTF |
| **NDT** | área de notas na `pagina_def`: altura máxima, separador, formato de numeração. Cumpre T3 do estudo |
| **Requisitos** | `NCRTF-PROD-008` (nota com corpo não vazio), `NCRTF-READ-006` (rejeitar nota sem corpo), `NDT-PROD-022` (área de notas declarada quando o template admite `corpo`) |
| **Vetores** | `ncrtf/valid/nota-rodape.json`, `ncrtf/invalid/nota-sem-corpo.json`, `ndt/valid/area-notas.json` |
| **Esforço** | **G** — é a tarefa com maior impacto em canonicalização |

### A2 — Referências cruzadas internas

Referência ODF: `text:reference-mark`, `text:reference-ref`.

**Desenho fixado em [`NCRTF-IDENTIFICADORES-E-REFERENCIAS.md`](../design/NCRTF-IDENTIFICADORES-E-REFERENCIAS.md)**
(2026-08-18), posterior a este plano: é essa a fonte do vocabulário e das
regras abaixo, incluindo a decisão de que o `id` é conteúdo assinado.

| | |
|---|---|
| **NCRTF** | campo `id` opcional em nós bloco elegíveis como alvo (`heading`, `paragraph`, `list_item`, `table`, `blockquote`) e novo nó inline `xref` com `target`. Preferido a dois nós de marca — menos vocabulário novo e cobre o caso de uso, que é remeter para um artigo ou número. O texto visível da remissão é escrito pelo produtor em `content`, como num `link`; o NCRTF não gera rótulos a partir de numeração resolvida em leitura (§3.2 do desenho) |
| **Regra** | toda a `xref.target` resolve para um `id` declarado **no mesmo documento** (R7), e cada `id` é único no documento (R8). Sintaxe `^[a-z][a-z0-9-]{0,63}$`, sem normalização em leitura (§3.1). Ponteiro intra-documento: não leva hash, ao contrário de `relacoes[]`. Referências circulares são legítimas e não são erro (§3.4) |
| **Ferramenta** | verificação nova em `tools/validate.py`, no verificador semântico NCRTF |
| **Requisitos** | `NCRTF-PROD-009` (sintaxe e unicidade de `id`, R8), `NCRTF-PROD-010` (`xref.target` resolve, R7), `NCRTF-READ-007` (rejeitar violação de R7 ou R8) |
| **Vetores** | `valid/remissao-interna.json`, `invalid/remissao-pendurada.json`, `invalid/id-duplicado.json` |
| **Esforço** | **M** |

### A3 — Listas com numeração por nível

Referência ODF: `text:list-level-style-number` (`style:num-format`, `text:start-value`, `text:display-levels`).

| | |
|---|---|
| **Decisão A1 do estudo** | o **formato** de numeração vai para o NDT; o NCRTF declara estrutura e continuidade |
| **NCRTF** | `start` em `list` (valor inicial, já candidato em §11.3). Nada mais — o aninhamento já existe |
| **NDT** | `estilos.listas[]`: formato por nível (`1`, `a`, `A`, `i`, `I`), prefixo, sufixo, níveis apresentados |
| **Requisitos** | `NCRTF-PROD-011` (`start` inteiro positivo), `NDT-PROD-023` (níveis declarados sem lacunas), `NDT-RENDER-012` (aplicar formato por nível; nível sem estilo declarado usa o formato herdado) |
| **Vetores** | `ncrtf/valid/lista-start.json`, `ndt/valid/estilos-listas.json`, `ndt/invalid/nivel-lista-em-falta.json` |
| **Esforço** | **M** |

### A4 — Fecho da fase

Decidir **O6**: absorver as alterações em `2.0.0`, que continua em draft e de
que nada depende, ou publicar `2.1.0` em ambos os formatos. Se for bump, o
`ndt_version` do schema deixa de poder ser `const: "2.0.0"` — `const` na versão
exata ou `enum` das versões suportadas.

Atualizar `RENDERER-CONFORMANCE.md`, `READINESS.md` e `TRACEABILITY.md`.
Esforço: **M**.

## 5. Fase B — composição publicável

**Objetivo:** o texto corrido sai com qualidade de publicação oficial.
**Entrega:** NDT v2.2 (e NCRTF v2.2 para B4/B5).

| # | Tarefa | Referência ODF | Requisitos previstos | Esforço |
|---|---|---|---|---|
| **B1** | Páginas pares/ímpares e margens espelhadas | `style:page-usage` (`all`\|`left`\|`right`\|`mirrored`) | `NDT-PROD-024`, `NDT-RENDER-013` | M |
| **B2** | Viúvas, órfãs, manter-junto | `fo:orphans`, `fo:widows`, `fo:keep-with-next`, `fo:keep-together` | `NDT-RENDER-014` (é regra de renderização, não de estrutura) | M |
| **B3** | Formato da numeração de página | `style:num-format` na página mestra | `NDT-RENDER-015` | P |
| **B4** | Células combinadas em tabela | `table:number-columns-spanned`, `table:number-rows-spanned` | `NCRTF-PROD-012`, `NCRTF-READ-008` | M |
| **B5** | Formatação dentro de células | conteúdo de `table:table-cell` | `NCRTF-PROD-013`; estende R1–R6 ao conteúdo das células | G |
| **B6** | `code_block`, `horizontal_rule` | — (já candidatos em NCRTF §11.3) | `NCRTF-READ-009` | P |

**B2 é regra de renderizador, não de estrutura** — entra como `NDT-RENDER-*` e
só ganha evidência com o corpus golden (P2). É o primeiro requisito deste plano
cuja verificação depende da trilha paralela.

## 6. Fase C — condicionada a caso de uso

Nenhuma destas tarefas tem hoje caso de uso documentado que satisfaça o teste de
admissão. Ficam registadas, não agendadas.

| # | Tarefa | Condição de entrada |
|---|---|---|
| ~~**C1**~~ | ~~Estilos nomeados por papel semântico~~ | **Promovida a candidata da Fase A** pela cláusula 2.2 (O2): se `font_family`/`alignment`/`indent` saírem do NCRTF (O1), os papéis deixam de ser opcionais — sem eles o NCRTF perde a única forma de distinguir blocos do mesmo tipo. Decisão em 0.2 |
| **C2** | Texto em múltiplas colunas (T6) | o caso do Diário da República confirmado como requisito, não como observação |
| **C3** | Idioma por fragmento (N7 + A4 do estudo) | decisão conjunta com o NDF sobre a lacuna L14 |
| **C4** | Metadados semânticos no conteúdo (N8) | estudo próprio: pode pertencer ao `documento` do NDF |
| **C5** | Regiões nomeadas com visibilidade condicional (T8) | insuficiência demonstrada do `incluir_se` por elemento |

**C1 é a decisão estrutural mais importante do conjunto.** Se entrar, entra
antes de B4/B5 — não depois.

## 7. Trilha paralela — dívida técnica e gates

Independente das fases; pode correr a qualquer momento.

| # | Tarefa | Porquê | Esforço |
|---|---|---|---|
| **P1** | Generalizar a resolução de ramos `oneOf` a NDF e NCRTF | Hoje só o NDT reporta a causa concreta em uniões discriminadas. Sem isto, os vetores negativos de NCRTF da Fase A herdam o problema de mensagens genéricas | P |
| **P2** | Corpus golden e segundo renderizador | **Único gate por fechar** do `RENDERER-CONFORMANCE.md`. Nenhum `NDT-RENDER-*` tem evidência executável; sem duas implementações independentes, nenhuma alegação de interoperabilidade se sustenta | G |
| **P3** | Exemplo render-ready de diploma legal | Prova de que a Fase A cumpriu o objetivo. Deve entrar como exemplo em `specs/ndt/examples/` e caso no corpus semântico | M |

**P1 antes de A2**, para que os vetores de referência pendurada provem a regra
em vez de falharem genericamente.

## 8. Sequência

```
Bloco 0  ──► Fase A ──► Fase B
  │           │
  │           └──► P3 (exemplo de diploma, valida a Fase A)
  │
  └──► P1 (antes de A2)

P2 ─── independente, mas bloqueia qualquer alegação de conformidade
       de renderizador, incluindo B2

Fase C ─── só com caso de uso; C1, se entrar, antes de B4/B5
```

**Ordem interna da Fase A:** A3 → A2 → A1 → A4. Da menos para a mais invasiva em
canonicalização, para que os problemas de R1–R6 apareçam com o menor número de
alterações em curso.

## 9. Riscos

| Risco | Mitigação |
|---|---|
| A canonicalização das notas (A1) obriga a rever R1–R6 e invalida vetores NCRTF existentes | Fazer A1 por último na fase; correr a suite NCRTF completa a cada passo |
| A Fase A cresce por arrasto — "já agora" acrescenta-se X | Teste de admissão aplicado tarefa a tarefa, não à fase |
| C1 é adiada e a Fase A introduz mecanismos que a impedem | 0.2 fixa a fronteira **antes** de A1–A3, mesmo que os papéis não sejam implementados nessa fase |
| **A janela de desenho livre (2.2) fecha antes de as correções serem feitas**, e O1–O3 passam a exigir alteração MAJOR com legado | Tratar 0.2 como prioridade sobre tudo o resto, incluindo a Fase A. É a única tarefa cujo custo aumenta com o tempo |
| Bump de versão coordenado (A4) dessincroniza NCRTF e NDT | Publicar as duas versões no mesmo commit, com vetores cruzados |
| P2 nunca fecha e os `NDT-RENDER-*` ficam indefinidamente sem evidência | Declarar explicitamente na `READINESS.md` que a conformidade de renderizador está por demonstrar — já é o caso; manter enquanto for verdade |

## 10. O que este plano não faz

- **Não toca no NDF-core** — congelado pela D5. C3 e C4, se avançarem, exigem
  decisão prévia sobre esse congelamento.
- **Não implementa renderizadores.** `normordis-pdf` e `normordis-odf` são Fase 4
  do roadmap principal e vivem noutro repositório; este plano prepara-lhes o
  contrato e o corpus.
- **Não abre a revisão pública.** O estado editorial das SPECs mantém-se
  "Draft — revisão pública por abrir".
