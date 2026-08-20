# Mapeamento PREMIS / METS — componentes e preservação

**Estado:** estudo de desenho, informativo. Não normativo, e **não constitui
alegação de conformidade** com PREMIS, METS ou OAIS — mesma reserva já feita em
[`INTEROPERABILITY-LAYERS.md`](INTEROPERABILITY-LAYERS.md).

**Data:** 2026-08-20
**Objetivo:** derivar o vocabulário de `papel` dos componentes de um documento
capturado a partir de vocabulário já estabelecido, em vez de o inventar — e
identificar os pontos de contacto para o gate externo 3 (avaliação por
arquivista competente) e para `R13` (depósito conforme OAIS).

**Método:** as linhas marcadas «por confirmar» exigem verificação cláusula a
cláusula contra o texto das normas antes de qualquer uso normativo. Segue o
mesmo procedimento já adotado para o vocabulário ODF em
[`ODF-ALIGNMENT-STUDY.md`](../design/ODF-ALIGNMENT-STUDY.md).

---

## 1. Porque este mapeamento existe

O documento capturado (ADR-020) declara componentes binários com um campo
`papel` (ADR-021). Um enum inventado por conveniência local seria a escolha
mais rápida e a pior: PREMIS e METS resolveram esta distinção há duas décadas,
são o que um arquivista competente conhece, e são o vocabulário em que a
pergunta de `R13` está formulada.

O que se importa é o **modelo conceptual**, nunca a serialização — princípio já
fixado em [`CRITERIO-DE-CAMADAS.md`](../design/CRITERIO-DE-CAMADAS.md) §7 para o
ODF, e aplicável aqui pela mesma razão.

## 2. Correspondência de entidades

| NORMORDIS | PREMIS | Nota |
|---|---|---|
| Documento (o ato) | Intellectual Entity | O NDF descreve-o; o `ndf_id` identifica-o |
| Conjunto de componentes que exprime o documento | Representation | Um documento capturado tem tipicamente uma representação; pode ter duas (original + congelada) |
| Componente individual | File | `componentes[]`, um por ficheiro |
| `sha256` de cada componente | Fixity (`messageDigestAlgorithm`, `messageDigest`) | Correspondência direta |
| Evento de custódia | Event | `custody-event.schema.json`, com `event_type` |
| `participantes`, `entidade_produtora`, `proveniencia_sistema` | Agent | Três tipos de agente já distinguidos no NDF |
| `avaliacao` (PCA/DF) | *sem equivalente direto* | PREMIS não modela avaliação arquivística; é matéria de instrumento nacional |

O NDF cobre num só objeto o que PREMIS distribui por Object, Event e Agent. Não
é divergência: é granularidade de serialização, e o mapeamento é possível nos
dois sentidos.

## 3. O enum `papel` — proposta derivada

| `papel` | Significado | PREMIS | METS `fileGrp/@USE` (convenção) |
|---|---|---|---|
| `original` | Os bytes tal como foram emitidos ou recebidos. Sempre preservados, nunca reescritos | File original da representação | `original` |
| `representacao_congelada` | Derivada de um `original` para garantir fidelidade visual futura. **Nunca o substitui** | File com relação de derivação (`hasSource`) | `reference` ou `service` — por confirmar |
| `anexo` | Componente de apoio sem identidade documental própria (ADR-020) | File da mesma representação | `original` |
| `evidencia` | Material de validação de assinatura contida, congelado na captura (SPEC §4.5.1) | File; PREMIS trata assinatura em `signatureInformation` — por confirmar se como Object ou como propriedade | sem convenção estabelecida |

**Nota sobre `USE` em METS:** o atributo não tem vocabulário controlado na
norma; os valores são convenção de perfil. Qualquer alegação de
interoperabilidade concreta exige fixar um perfil METS, não apenas usar os
valores habituais. **Por confirmar.**

### 3.1 Duas consequências de desenho

**A via de produção interna tem um só componente.** Um PDF/A exportado pelo
produtor é o documento tal como emitido: `papel: "original"`. Não existe
`representacao_congelada`, porque nada foi congelado *a partir de* outra coisa.
Isto resolve, sem caso especial, o colapso entre original e representação
canónica que o desenho preliminar tratava como regra separada.

**A relação original → congelada é derivação, não substituição.** PREMIS
modela-a como relação entre objetos, e é exatamente a semântica pretendida: os
dois coexistem, com funções diferentes, e o original nunca é descartado.

## 4. Fixidez e verificação periódica

PREMIS trata a verificação de fixidez como **Event** recorrente, não como
propriedade estática do objeto. O NDF tem hoje `event_type: "verificado"` no log
de custódia, o que serve.

Esta correspondência reforça uma decisão já tomada do lado da aplicação: a
verificação de integridade dos objetos deve correr periodicamente em segundo
plano, e não apenas no momento da exportação. Em vocabulário PREMIS, um objeto
sem eventos de fixidez ao longo do tempo tem **uma** verificação, não uma
história de verificações — e é a história que sustenta a alegação de
preservação.

## 5. O que este mapeamento não resolve

Confirma, por contraste, as lacunas já registadas para a transferência entre
entidades ([`../design/NDFPKG-CAPTURA-E-INGESTAO.md`](../design/NDFPKG-CAPTURA-E-INGESTAO.md) §11.2):

| Lacuna | Em vocabulário OAIS/METS |
|---|---|
| **L-T1** — não existe conjunto de transferência | É o **SIP**. Um `.ndfpkg` é um documento; um SIP é o conjunto e a sua descrição estrutural (`structMap`) |
| **L-T2** — a cadeia de custódia não acompanha o pacote | São os PREMIS **Events**, que num AIP viajam com o objeto. Hoje não viajam |
| **L-T3** — transferir custódia é um ato sem artefacto de aceitação | OAIS modela-o na função *Ingest*, com confirmação ao produtor |

Nenhuma destas exige inventar mecanismo: exige adotar o que já existe.

## 6. Trabalho de confirmação pendente

Antes de qualquer uso normativo destes valores:

1. Confirmar o tratamento de assinaturas em PREMIS — objeto próprio ou
   propriedade de objeto — e o seu efeito sobre `papel: "evidencia"`.
2. Confirmar os valores convencionais de `fileGrp/@USE` num perfil METS de
   referência, e decidir se o NORMORDIS adota um perfil existente ou declara o
   seu.
3. Confirmar a granularidade de Representation quando existem original e
   representação congelada: uma representação com dois ficheiros, ou duas
   representações relacionadas.
4. Verificar se algum instrumento da DGLAB já fixa perfil de submissão, o que
   tornaria as três questões anteriores decididas em vez de abertas.

O ponto 4 é o mais barato e o de maior efeito: é também a pergunta que abre a
conversa prevista em `R5`.

## 7. Referências

- [`INTEROPERABILITY-LAYERS.md`](INTEROPERABILITY-LAYERS.md) — posição por camadas, `R13`
- [`docs/design/NDFPKG-CAPTURA-E-INGESTAO.md`](../design/NDFPKG-CAPTURA-E-INGESTAO.md) §11
- ADR-020, ADR-021
- OAIS (ISO 14721), PREMIS Data Dictionary, METS — **não verificados cláusula a cláusula**; ver §6
