# Conjunto de transferência — desenho para L-T1, L-T2 e L-T3

**Estado:** desenho executado, informativo. Não acrescenta requisitos de
conformidade NDF e **não constitui alegação de conformidade** com OAIS, METS ou
PREMIS. As três fronteiras que abria — `D-XFER-1` a `D-XFER-3` — estão decididas
(§3.4, §4.4, §5.1), e os artefactos estão escritos e exercitados:

| Artefacto | Onde |
|---|---|
| `transferencia.schema.json` | `specs/ndf/schemas/` |
| `evidencia-custodia.schema.json` | `specs/ndf/schemas/` |
| `aceitacao-custodia@1.0.0` | `specs/registry/schemas/` |
| Exemplo de conjunto | `specs/ndf/examples/ndfxfer-example/` |
| Validador e 11 vetores negativos | `tools/check_transferencia*.py` |

O conjunto de transferência **não é requisito de conformidade NDF** e não entra
na SPEC: é camada exterior ao documento, tal como o Perfil de Ciclo de Vida
(ADR-010). Um produtor NDF conforme pode nunca o usar.

**Data:** 2026-08-23
**Origem:** lacunas L-T1 a L-T4 de
[`NDFPKG-CAPTURA-E-INGESTAO.md`](NDFPKG-CAPTURA-E-INGESTAO.md) §11.2; fronteira
fixada em [ADR-024](../architecture/ADR-024-fronteira-oais-modelo-de-informacao.md);
achado `R13`.

**Método:** o vocabulário conceptual vem de OAIS e PREMIS; os nomes são
NORMORDIS e o mapeamento é explícito (§8), pela razão dada em ADR-024 §2. As
linhas marcadas «por confirmar» exigem verificação contra o texto das normas
antes de qualquer uso normativo.

---

## 1. O problema, em uma frase

Um `.ndfpkg` é **um** documento. Entregar «o processo» a outra entidade é
entregar N pacotes, e **nada declara quais compõem o conjunto, nem permite ao
recetor saber se recebeu tudo**.

Três consequências, que são as lacunas registadas:

| | Falta |
|---|---|
| **L-T1** | o conjunto não existe como objeto — não há o que assinar, contar ou conferir |
| **L-T2** | a cadeia de custódia não faz parte do pacote, logo o que se transfere é o documento sem a sua história |
| **L-T3** | transferir custódia é um ato, e não há artefacto que prove que o recetor a aceitou |

L-T4 — divulgação parcial impossível sem quebrar a assinatura — **não é lacuna**:
é comportamento correto, e a regra que dele decorre governa o desenho de L-T2
(§4.2).

## 2. O que este desenho não faz

Fronteira de [ADR-024](../architecture/ADR-024-fronteira-oais-modelo-de-informacao.md),
aplicada caso a caso antes de desenhar seja o que for:

| | Estatuto |
|---|---|
| Declarar o conjunto, o seu conteúdo e o seu fecho | **artefacto** → cabe aqui |
| Declarar que eventos de custódia acompanham a unidade | **artefacto** → cabe aqui |
| Registar a aceitação pela entidade recetora | **artefacto** → cabe aqui |
| Decidir **se** aceita, com que critérios, e por que ordem processa | **função de arquivo** → não cabe aqui, nem neste repositório |
| Política de retenção do recetor, planeamento de preservação, migração | **função de arquivo** → não cabe |
| Transporte, autenticação de canal, cifra em trânsito | **infraestrutura** → não cabe |

O teste que separa as colunas é o de ADR-022: *um verificador decide isto tendo
apenas o que recebeu em mãos?*

## 3. L-T1 — o conjunto de transferência

### 3.1 Forma

Um contentor — proposta de extensão `.ndfxfer` — com esta composição:

```
processo-789-2026.ndfxfer (ZIP)
├── transferencia.json      — declaração do conjunto e do seu fecho
├── transferencia-envelope.json  — selo da entidade transmitente
├── evidencia/
│   └── <ndf_id>.evidencia.json  — evidência de custódia por unidade (§4)
└── unidades/
    └── <nome livre>.ndfpkg      — um pacote por unidade documental
```

`transferencia.json` declara:

```json
{
  "ndfxfer_version": "1.0.0",
  "transferencia_id": "b7c19e04-2a55-4f83-9d61-0e7a4c8f2135",
  "criada_em": "2026-08-23T10:14:00Z",
  "transmitente": { "designacao": "…", "identificadores": [ … ] },
  "destinatario": { "designacao": "…", "identificadores": [ … ] },
  "fundamento": "Transferência para arquivo definitivo ao abrigo de …",
  "unidades": [
    {
      "ndf_id": "a1b2c3d4-e5f6-4789-abcd-ef0123456789",
      "payload_hash": "sha256:…",
      "validation_code": "NDF-…",
      "ficheiro": "unidades/oficio-123.ndfpkg"
    }
  ],
  "inventario": [ { "ficheiro": "…", "hash_sha256": "sha256:…" } ]
}
```

### 3.2 As quatro propriedades que o fecho tem de dar

**Composição declarada.** `unidades[]` enumera o conjunto. Um recetor que conte
as entradas e encontre os ficheiros sabe que recebeu o que foi enviado — o que
hoje não é possível afirmar de N pacotes soltos.

**Ligação à versão exata.** Cada unidade é identificada por `ndf_id` **e**
`payload_hash`, como já fazem as relações documentais (§2.11.3). Substituir um
pacote por outra versão do mesmo documento quebra a declaração.

**Fecho nos dois sentidos.** É a regra de `NDF-PKG-009` elevada ao conjunto:
cada unidade declarada tem de estar presente, e cada `.ndfpkg` presente em
`unidades/` tem de estar declarado. Um pacote a mais é tão grave como um a
menos — foi acrescentado por alguém e nada o cobre.

**Selo do transmitente.** `transferencia-envelope.json` cobre os bytes
canonicalizados de `transferencia.json`, pelo mesmo mecanismo do envelope de um
NDF (§4): sem ele, a declaração de composição é uma afirmação de ninguém.

> **Precisado ao implementar (2026-08-23).** O esboço de §3.1 sugeria que
> `inventario[]` cobrisse tudo, unidades incluídas. Não deve, e a razão é a mesma
> que leva §8.1 a resolver componentes por digest e nunca por caminho: o digest
> do ficheiro `.ndfpkg` é da **materialização**, não da unidade documental. O
> mesmo documento rezipado noutra máquina tem outro digest e continua a ser a
> mesma unidade. `inventario[]` cobre por isso apenas os ficheiros próprios do
> contentor — declaração, selo e evidência —, e as unidades são cobertas por
> `unidades[].payload_hash`, que as prende ao conteúdo assinado.

### 3.3 O que o conjunto NÃO faz aos documentos

**Não os altera.** Cada `.ndfpkg` viaja tal como foi selado; o conjunto é camada
exterior. É condição de o desenho ser possível: os NDF são imutáveis e
assinados, e um conjunto que exigisse reescrevê-los seria um conjunto que
destrói o que transporta.

**Não os relaciona.** As relações documentais já vivem em `relacoes[]` dentro de
cada NDF-core assinado (§2.11), e é lá que devem continuar: são afirmações do
produtor, não do transmitente. `transferencia.json` declara **composição**, não
estrutura intelectual. Um conjunto não é um processo.

### 3.4 D-XFER-1 — referências pendentes sim, estrutura não

**Decidido (2026-08-23).** `transferencia.json` declara `referencias_externas[]`
— as relações das unidades cujo alvo **não** está no conjunto — e **não** declara
a estrutura intelectual do processo.

O critério não é a utilidade, é a verificabilidade. `relacoes[].alvo` exige
`ndf_id` **e** `payload_hash` (§2.11), pelo que a lista de referências que saem
do conjunto é **inteiramente recomputável pelo recetor** a partir das unidades
que recebeu. Uma declaração que o recetor pode recalcular e conferir é um resumo
verificável; uma que só o transmitente conhece seria segunda fonte de verdade.

Daqui decorre uma propriedade de conformidade, na forma de `NDF-PKG-009`:

> O `referencias_externas[]` declarado **DEVE** coincidir com o que a
> recomputação sobre `unidades[]` produz — nem a mais, que inventaria uma
> pendência, nem a menos, que esconderia que o conjunto não fecha.

Isto responde à pergunta que L-T1 existe para responder — *este conjunto está
fechado?* — sem se tornar um `structMap`: declara-se a **fronteira**, nunca a
árvore. A árvore continua em `relacoes[]`, dentro dos bytes assinados de cada
unidade, como afirmação do produtor e não do transmitente.

## 4. L-T2 — evidência de custódia transferível

### 4.1 Porque não basta acrescentar o log ao pacote

Duas razões, e a segunda é a que decide o desenho.

**Primeira:** o log de custódia vive no Perfil de Ciclo de Vida (§9.5), que é
**opcional** e não é requisito de conformidade NDF (ADR-010). O pacote não pode
exigir o que a conformidade não exige.

**Segunda:** o log integral divulga informação operacional interna — quem
acedeu, quando, a partir de que sistema. Transferir a custódia de um documento
não é transferir o histórico de acessos do serviço que o custodiava.

### 4.2 A regra de L-T4, aplicada ao log

L-T4 fixou que divulgação parcial se resolve por **documento novo**, nunca por
mutilação do original. A mesma regra resolve isto, e não por analogia: uma
cadeia de custódia é encadeada por hash, e retirar-lhe eventos é exatamente o
que `conformance/custody/omissao-recomposta.json` demonstra ser detetável e
inconforme — `CUST-REQ-004` já o proíbe.

Logo, o que se transfere **não é a cadeia com menos eventos**. É uma
**declaração atestada** sobre a cadeia, que é objeto novo e assinado:

```json
{
  "ndf_id": "a1b2c3d4-…",
  "cadeia": {
    "eventos_total": 9,
    "ultimo_event_hash": "sha256:…"
  },
  "eventos": [ { "sequence": 0, "event_type": "capturado",  "event_hash": "sha256:…", … } ],
  "omitidos": {
    "contagem": 4,
    "fundamento": "Eventos de consulta interna, não transferidos por conterem identificação de trabalhadores do serviço."
  }
}
```

### 4.3 O que o recetor consegue verificar — e o que não

| Consegue | Não consegue |
|---|---|
| Recalcular o `event_hash` de cada evento transferido a partir do seu próprio conteúdo | Reconstruir os eventos omitidos — **é o objetivo** |
| Confirmar que `eventos` + `omitidos.contagem` = `eventos_total` | Verificar o encadeamento entre eventos não contíguos |
| Ver `ultimo_event_hash`, que fixa o estado da cadeia no momento da extração | Provar que `eventos_total` é verdadeiro sem confiar no selo |

A última linha é a limitação honesta deste desenho e **deve ser afirmada, não
escondida**: a integridade do extrato assenta no selo do transmitente, não numa
propriedade criptográfica do encadeamento. Isso é adequado — o transmitente é
quem detém a cadeia e quem responde pela declaração — mas não é a mesma coisa
que verificar uma cadeia completa, e um leitor não deve tratá-las como
equivalentes.

### 4.4 D-XFER-2 — política declarada, não lista por omissão

**Decidido (2026-08-23).** Não há lista de tipos transferíveis por omissão. Duas
regras substituem-na.

A lista tinha um defeito que só se vê depois de a escrever: legitima a **seleção
caso a caso**. Se o formato enumera os tipos transferíveis, nada impede que num
documento incómodo se transfira menos, com um fundamento plausível escrito para
esse documento.

**Regra 1 — a extração declara uma política, não uma seleção.** A entidade
declara que tipos de evento extrai, como política identificada, e aplica-a a toda
a transferência; o identificador da política viaja no extrato. A auditoria passa
a incidir sobre a política e não sobre cada extrato — um documento cujo extrato
divirja da política declarada é detetável por comparação com os restantes. A
escolha seletiva deixa de ser invisível.

**Regra 2 — `finalizado` é obrigatório quando existe na cadeia.** Não é matéria
de política: sem ele, o extrato não estabelece quando o documento se tornou
imutável, e deixa de ser evidência de custódia para passar a ser uma lista de
acontecimentos. É o mesmo raciocínio de `fundamento` obrigatório em
`origem_nao_identificavel` (ADR-023) — o formato não escolhe o valor, exige que
o campo signifique alguma coisa.

Ambas se mantêm dentro de ADR-024: o formato fixa que a seleção é **declarada,
uniforme e verificável**; *quais* tipos uma entidade transfere continua a ser
política dessa entidade.

## 5. L-T3 — a aceitação

Transferir custódia é um ato bilateral. `event_type: "transferido"` já existe no
schema de custódia e regista o lado do transmitente; falta o do recetor. Sem
ele, «enviado de forma segura» é propriedade do transporte, não da custódia — e
não há momento identificável em que a responsabilidade muda de mãos.

**A aceitação é ela própria um ato documental, e deve ser um NDF.** Não é
conveniência: um recibo de custódia tem autor, data, entidade responsável,
imputação jurídica e valor probatório, que é a definição de documento neste
projeto. Sendo NDF, ganha sem trabalho novo identidade, assinatura, avaliação
arquivística, custódia própria e relações tipadas.

```
NDF de aceitação (produzido pelo recetor)
   │
   ├── documento.transferencia_ref → transferencia_id + selo
   ├── documento.resultado[] → por unidade: aceite | recusada + fundamento
   └── relacoes[] → uma por unidade aceite, ligando ndf_id + payload_hash
```

O recetor devolve-o ao transmitente, que passa a deter prova de que a custódia
foi assumida, ligada às versões exatas transferidas.

**Aceitação parcial é o caso normal, não a exceção.** Um recetor pode aceitar
oito unidades e recusar duas por não satisfazerem os seus requisitos de
depósito. O artefacto exprime-o por unidade; **os critérios de recusa são do
recetor** e não desta especificação.

### 5.1 D-XFER-3 — `event_type: "recebido"`

**Decidido e executado (2026-08-23).** O schema de custódia ganha
`event_type: "recebido"`, e a SPEC §2.4.2 documenta-o.

O argumento é de coerência interna. As entradas disponíveis eram `capturado` e
`finalizado`, e nenhuma é verdadeira do lado do recetor: não capturou — o
documento já existia, com identidade, assinatura e história — nem finalizou.
Registar `capturado` seria uma declaração falsa **da mesma família** da que
§2.8.1.1 acabou de proibir ao separar submeter de produzir. Não é possível fixar
a regra num sítio e violá-la no outro.

O custo é baixo e convém dizê-lo: o schema de custódia pertence ao **Perfil de
Ciclo de Vida, opcional** e não requisito de conformidade NDF (ADR-010). Não é
alteração ao NDF-core.

**O esclarecimento que o campo obrigou a escrever vale mais do que o campo.** As
cadeias de custódia são **por custodiante, não globais**: a do recetor abre em
`sequence` 0 com `previous_event_hash` `null` e não continua a do transmitente —
não pode, por o recetor não deter os eventos anteriores nem os poder encadear
sem os falsificar. O que liga as duas cadeias é documental (a evidência de §4 e
o documento de aceitação), nunca criptográfico. Era o modelo de facto e estava
por dizer; agora está em §2.4.2, com o vetor
`conformance/custody/cadeia-do-recetor.json`.

## 6. O que isto exige do formato, e o que não exige

**Não exige nada ao NDF-core.** Nenhuma das três lacunas se resolve dentro do
documento: o conjunto é exterior, a evidência é derivada e a aceitação é um
documento novo. É consistente com o congelamento de âmbito D5.

**Exige três artefactos novos** — `transferencia.json`, a evidência de custódia,
e um tipo documental de aceitação — mais um contentor. Todos passam o teste de
ADR-024.

**Exigiu uma alteração ao schema de custódia** — `event_type: "recebido"`,
D-XFER-3, já executada. É a única alteração a artefacto existente que este
desenho produziu, e recai sobre o Perfil de Ciclo de Vida, que é opcional.

## 7. Sequência proposta

| # | Passo | Porquê primeiro |
|---|---|---|
| 1 | ~~Fechar D-XFER-1 a D-XFER-3~~ | ✅ 2026-08-23 — §3.4, §4.4, §5.1; `recebido` executado |
| 2 | ~~`transferencia.schema.json` + vetores~~ | ✅ 2026-08-23 — schema, exemplo, validador e 11 vetores negativos |
| 3 | ~~Tipo documental de aceitação~~ | ✅ 2026-08-23 — `aceitacao-custodia@1.0.0`, com vetor positivo e negativo |
| 4 | ~~Evidência de custódia~~ | ✅ 2026-08-23 — `evidencia-custodia.schema.json`, aplicando D-XFER-2 |
| 5 | Verificação cláusula a cláusula OAIS/PREMIS/METS | **Deliberadamente por fazer.** Compete a revisão arquivística (gate externo 3), e revisão interna não a fecha. Ver [`../interoperability/OAIS-MAPPING.md`](../interoperability/OAIS-MAPPING.md) §6 |

Os vetores negativos importam mais do que os positivos, pela razão habitual
neste projeto: **unidade em falta, unidade a mais, `payload_hash` divergente,
selo ausente, contagem de eventos que não fecha**. Sem eles, «o conjunto está
completo» é uma alegação, não uma propriedade.

## 8. Correspondência com OAIS e PREMIS

Conceptual e informativa; nomes NORMORDIS por decisão de ADR-024 §2.

| NORMORDIS | OAIS / PREMIS | Nota |
|---|---|---|
| Conjunto de transferência (`.ndfxfer`) | **SIP** | Objeto de submissão; o `.ndfpkg` individual não o é |
| `transferencia.json` → `unidades[]` | Packaging Information | Composição e fecho, não estrutura intelectual |
| Evidência de custódia | PREMIS **Events** que viajam com o objeto | Aqui como extrato atestado, não como cadeia — §4.2 |
| NDF de aceitação | confirmação da função *Ingest* ao produtor | O artefacto é NDF; a **função** é do arquivo e fica fora (ADR-024) |
| `relacoes[]` dentro de cada unidade | estrutura intelectual (`structMap` em METS) | Já existe no NDF; ver D-XFER-1 |

**Por confirmar** em todas as linhas: o mapeamento não foi verificado cláusula a
cláusula, e a granularidade de SIP quando o conjunto tem uma só unidade merece
verificação — ver [`../interoperability/PREMIS-METS-MAPPING.md`](../interoperability/PREMIS-METS-MAPPING.md) §6.

## 9. Referências

- [`NDFPKG-CAPTURA-E-INGESTAO.md`](NDFPKG-CAPTURA-E-INGESTAO.md) §11 — L-T1 a L-T4
- [ADR-024](../architecture/ADR-024-fronteira-oais-modelo-de-informacao.md) — fronteira; [ADR-022](../architecture/ADR-022-dever-do-formato.md) — teste operacional
- [ADR-010](../architecture/ADR-010-separacao-conformidade-perfil-ciclo-vida.md) — o Perfil de Ciclo de Vida é opcional
- SPEC.md §2.4.2 (cadeia de custódia), §2.11 (relações), §8 (pacote), §9.5 (`CUST-REQ-004`)
- `conformance/custody/omissao-recomposta.json` — porque não se transfere uma cadeia mutilada
- [`../interoperability/OAIS-MAPPING.md`](../interoperability/OAIS-MAPPING.md) — mapeamento consolidado
