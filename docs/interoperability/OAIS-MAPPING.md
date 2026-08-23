# Mapeamento consolidado NDF ↔ OAIS

**Estado:** informativo. Não altera a especificação, não estabelece requisitos de
conformidade, e **não constitui alegação de conformidade** com OAIS, PREMIS,
METS ou eIDAS. A reserva de
[`INTEROPERABILITY-LAYERS.md`](INTEROPERABILITY-LAYERS.md) §6 aplica-se
integralmente.

**Data:** 2026-08-23
**Fronteira aplicável:** [ADR-024](../architecture/ADR-024-fronteira-oais-modelo-de-informacao.md)
**Método:** o mapeamento **não foi verificado cláusula a cláusula** contra o
texto das normas. É a consolidação de trabalho anterior — a posição por camadas,
o mapeamento PREMIS/METS do vocabulário de componentes e o desenho do conjunto
de transferência — numa vista única, para servir a conversa com competência
arquivística (gate externo 3) e não para a substituir.

---

## 1. Para que serve este documento

Responde a uma pergunta, e recusa outra.

**Responde:** *quando um arquivista pergunta «onde está a proveniência? e a
fixidez? e a Representation Information?», o que é que se lhe mostra?*

**Recusa:** *é o NDF conforme a OAIS?* — não é pergunta que um formato possa
responder. OAIS é modelo de referência para um **arquivo**, com funções,
políticas e responsabilidades organizacionais que nenhum formato executa.

## 2. Modelo de informação — a metade que o NDF adota

| OAIS | NDF | Onde |
|---|---|---|
| **Content Information** — Content Data Object | `documento` (nativo) ou `documento.componentes[]` (capturado ou anexos) | SPEC §2.2, §2.8.1 |
| **Content Information** — Representation Information | schema de `tipo_documento_ref`; NDT; NCRTF; recursos; `media_type` dos componentes | §2.9, `specs/ndt/`, `specs/ncrtf/` |
| **PDI** — Reference | `ndf_id`; `validation_code`; `numero_referencia` | §2.3, §4.6, §2.7.2 |
| **PDI** — Fixity | `payload_hash` + `payload_hash_alg`; `componentes[].sha256`; `manifest.inventario` | §2.5, §2.8.1, §8.2 |
| **PDI** — Provenance | `participantes`, `proveniencia_sistema`, `proveniencia_ia`, `proveniencia_submissao`, log de custódia | §2.12, §2.13, §2.14, §2.8.1, §2.4.2 |
| **PDI** — Context | `relacoes[]`, `entidade_produtora`, `processo_ref`, `classificacao_seguranca`, `avaliacao` | §2.11, §2.7, §3 |
| **PDI** — Access Rights | `classificacao_seguranca`, `protecao_dados` | §2.7.4, §1.4 |
| **Packaging Information** | `manifest.json`; estrutura do `.ndfpkg` | §8.1, §8.2 |
| **Descriptive Information** | `metadados` | §2.7 |

Duas notas onde a correspondência é mais interessante do que parece:

**Representation Information é o que o NDF faz melhor.** A separação entre dados
(`documento`), significado (schema do tipo) e apresentação (NDT) é precisamente a
decomposição que OAIS exige para que bytes continuem interpretáveis quando a
aplicação que os produziu já não existir — e os artefactos viajam dentro do
pacote (§8.1), não numa base de dados do produtor.

**Fixidez está dentro dos bytes assinados.** Os digests dos componentes vivem em
`documento`, coberto pela assinatura, e não apenas no manifesto
([ADR-021](../architecture/ADR-021-componentes-nos-bytes-assinados.md)). Em
vocabulário PREMIS, a fixidez não é asserção de embalagem: é parte do objeto
atestado.

## 3. Modelo funcional — a metade que fica fora

| Função OAIS | Estatuto | Onde vive |
|---|---|---|
| *Ingest* | fora | `core-ingest` e aplicação; só o **artefacto** de aceitação é NDF |
| *Archival Storage* | fora | custodiante; append-only/WORM é `CUST-REQ-002`, perfil **opcional** |
| *Data Management* | fora | aplicação |
| *Access* | fora | aplicação; o NDF classifica sensibilidade, **não controla acesso** (§1.5) |
| *Administration* | fora | entidade |
| *Preservation Planning* | fora | entidade; nem sequer é este repositório |

Ver ADR-024 para o critério e para as alternativas recusadas.

## 4. Pacotes — a correspondência que mais se presta a erro

| OAIS | NORMORDIS | Estatuto da correspondência |
|---|---|---|
| **SIP** | conjunto de transferência (`.ndfxfer`) | **Em desenho** — [`../design/NDF-CONJUNTO-DE-TRANSFERENCIA.md`](../design/NDF-CONJUNTO-DE-TRANSFERENCIA.md) |
| **AIP** | `.ndfpkg` **pode constituir a base de** um AIP | Nunca «é um AIP»: o AIP existe dentro de um arquivo, com as suas responsabilidades |
| **DIP** | representação gerada de NDF + NDT (PDF/A, HTML) | O DIP é produzido para um pedido concreto; o NDF é a fonte, não o DIP |

**Um `.ndfpkg` é um documento; um SIP é um conjunto.** Confundi-los é o erro que
a lacuna L-T1 nomeia: hoje enviar «o processo» é enviar N pacotes soltos, sem
nada que declare a composição.

## 5. Fórmulas defensáveis, e as que não são

Repetido de ADR-024 §Decisão por ser o uso mais provável deste documento.

| Não afirmar | Afirmar |
|---|---|
| «NDF é OAIS compliant» | «o modelo de informação do NDF mapeia para o de OAIS — ver §2» |
| «`.ndfpkg` é um AIP» | «um `.ndfpkg` pode constituir a base de um AIP numa implementação arquivística» |
| «NDF é eIDAS compliant» | «o NDF transporta assinaturas e provas conformes a normas ETSI aplicáveis ao eIDAS» |
| «CAdES-B-LTA garante validade jurídica» | «B-LTA é perfil de preservação da verificabilidade; a natureza jurídica da assinatura é eixo independente» |
| «o NDF garante a preservação» | «o NDF transporta o que permite verificar integridade, origem e interpretabilidade; preservar é atividade de quem custodia» |

## 6. Onde o mapeamento está incompleto

Registado por honestidade de método, e é a lista que uma revisão arquivística
deve atacar primeiro:

1. **Verificação cláusula a cláusula** contra ISO 14721 / CCSDS 650.0-M, PREMIS
   e METS — nenhuma linha deste documento a teve. Confirmar também a edição
   vigente de cada norma antes de a citar.
2. **Avaliação arquivística não tem equivalente PREMIS** (`PREMIS-METS-MAPPING.md`
   §2). PCA e destino final são matéria de instrumento nacional; se um perfil
   METS de referência a modela, é isso que se deve adotar.
3. **Granularidade de Representation** quando coexistem original e representação
   congelada — `PREMIS-METS-MAPPING.md` §6.3.
4. **SIP com uma só unidade** — se o conjunto de transferência degenera num
   pacote, ou se continua a ser conjunto de cardinalidade um.
5. **`fileGrp/@USE`** não tem vocabulário controlado em METS; qualquer alegação
   concreta exige fixar um perfil.
6. **A evidência de custódia transferível não é uma cadeia**, é um extrato
   atestado — ver [`../design/NDF-CONJUNTO-DE-TRANSFERENCIA.md`](../design/NDF-CONJUNTO-DE-TRANSFERENCIA.md) §4.3.
   Confirmar se PREMIS admite essa figura ou se a modela de outro modo.

## 7. Referências

- [ADR-024](../architecture/ADR-024-fronteira-oais-modelo-de-informacao.md) — fronteira modelo de informação / modelo funcional
- [`INTEROPERABILITY-LAYERS.md`](INTEROPERABILITY-LAYERS.md) — camadas, `R13`, não-objetivos
- [`PREMIS-METS-MAPPING.md`](PREMIS-METS-MAPPING.md) — vocabulário de componentes, trabalho de confirmação
- [`../design/NDF-CONJUNTO-DE-TRANSFERENCIA.md`](../design/NDF-CONJUNTO-DE-TRANSFERENCIA.md) — L-T1 a L-T3
- OAIS (ISO 14721 / CCSDS 650.0-M), PREMIS Data Dictionary, METS — **edições e cláusulas não verificadas**
