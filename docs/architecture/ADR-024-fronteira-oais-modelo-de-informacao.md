# ADR-024: OAIS entra pelo modelo de informação, nunca pelo modelo funcional

**Estado**: Aceite
**Data**: 2026-08-23
**Decisores**: carloscanutocosta

---

## Contexto

[`INTEROPERABILITY-LAYERS.md`](../interoperability/INTEROPERABILITY-LAYERS.md)
(2026-08-11) fixou que a interoperabilidade que interessa demonstrar é ao nível
do **pacote documental**, com o depósito conforme OAIS como primeiro caso.
[`PREMIS-METS-MAPPING.md`](../interoperability/PREMIS-METS-MAPPING.md)
(2026-08-20) começou a executá-lo, derivando o enum `papel` de vocabulário
estabelecido em vez de o inventar.

Nenhum dos dois responde à pergunta que vem a seguir, e que é de fronteira:
**quanto de OAIS entra no NDF?**

A pergunta não é académica. OAIS é um modelo de referência para um **arquivo**,
e as suas lacunas registadas em
[`NDFPKG-CAPTURA-E-INGESTAO.md`](../design/NDFPKG-CAPTURA-E-INGESTAO.md) §11.2
são, nos termos de [ADR-022](ADR-022-dever-do-formato.md), lacunas **do
formato**: L-T1 (não existe conjunto de transferência), L-T2 (a cadeia de
custódia não viaja no pacote) e L-T3 (transferir custódia é ato sem artefacto de
aceitação). Fechá-las obriga a ir buscar material a OAIS. Sem critério, «ir
buscar material a OAIS» degenera em replicar OAIS — e um repositório de formatos
que descreve funções de arquivo passou a especificar um sistema de gestão
documental sem o admitir.

O deslize é o mesmo que ADR-022 existe para impedir, agravado por o vocabulário
importado ser prestigiado: uma cláusula sobre *Preservation Planning* numa
especificação de formato parece rigor, e é excesso de âmbito.

## Decisão

**OAIS entra no NDF pelo modelo de informação. O modelo funcional e as
responsabilidades organizacionais ficam fora, e não são matéria deste
repositório.**

| Metade de OAIS | Estatuto no `normordis-formats` |
|---|---|
| **Modelo de informação** — Content Information, PDI (proveniência, referência, fixidez, contexto), Packaging Information, Descriptive Information | **Adotável.** Descreve artefactos, e artefactos são matéria de formato |
| **Modelo funcional** — Ingest, Archival Storage, Data Management, Access, Administration, Preservation Planning | **Fora de âmbito.** Descreve funções, responsabilidades e políticas de um arquivo, que nenhum formato executa |

### O teste

É a forma, para este domínio, do teste operacional de ADR-022:

> **É artefacto que viaja no pacote e que um verificador consegue examinar com o
> pacote em mãos? Pode ser NDF. É função, responsabilidade ou política de quem
> custodia? Não é NDF, em circunstância nenhuma.**

Aplicado às lacunas abertas, o teste decide as três no mesmo sentido — e é essa
a razão de ser desta decisão, que sem isso seria apenas uma reserva:

| Lacuna | Em OAIS | Veredicto |
|---|---|---|
| L-T1 — conjunto de transferência | o **SIP** | **É NDF.** O conjunto é um artefacto com composição declarada e verificável |
| L-T2 — evidência de custódia transferível | **Events** que viajam no AIP | **É NDF.** O que viaja é um artefacto; *que* eventos se transferem, e quais ficam em auditoria interna, é desenho de formato |
| L-T3 — aceitação pela entidade recetora | função *Ingest*, com confirmação ao produtor | **É NDF apenas o artefacto de aceitação.** O procedimento de receção, os critérios e quem decide são do arquivo |
| Preservation Planning, monitorização de obsolescência, política de migração | funções OAIS | **Não é NDF.** Nem sequer é este repositório |

L-T4 (divulgação parcial impossível por construção) confirma o critério pelo
lado oposto: é comportamento correto do formato, e resolve-se por documento novo
com relação tipada, nunca por mutilação do pacote.

### Duas regras de execução

**1. Não se importa nomenclatura, importa-se o modelo.** É o princípio já fixado
em [`CRITERIO-DE-CAMADAS.md`](../design/CRITERIO-DE-CAMADAS.md) §7 para o ODF e
já aplicado ao vocabulário PREMIS. Um artefacto NORMORDIS chama-se pelo seu nome
NORMORDIS e mapeia-se explicitamente para o conceito OAIS numa tabela. Um
conjunto de transferência chamado «SIP» seria lido como conformidade OAIS por
quem nunca chega às reservas.

**2. Nenhuma alegação de conformidade.** Mantém-se sem alteração o §6 de
`INTEROPERABILITY-LAYERS.md`. Em particular, e para uso em texto público:

| Não afirmar | Formulação defensável |
|---|---|
| «NDF é OAIS compliant» | «o modelo de informação do NDF mapeia para o de OAIS; ver tabela» |
| «`.ndfpkg` é um AIP OAIS» | «um `.ndfpkg` pode constituir a base de um AIP dentro de uma implementação arquivística» |
| «NDF é eIDAS compliant» | «o NDF transporta assinaturas e provas conformes a normas ETSI aplicáveis ao eIDAS» |
| «CAdES-B-LTA garante validade jurídica» | «B-LTA é um perfil de preservação da verificabilidade; a natureza jurídica da assinatura é outro eixo» |

A última linha merece destaque por ser erro frequente: **perfil de preservação
(B-B → B-T → B-LT → B-LTA) e natureza jurídica (simples, avançada, qualificada)
são eixos independentes.** Um B-LTA transporta uma ou outra consoante o
certificado e as condições da sua emissão, e nunca qualifica nada por si.

## Alternativas consideradas

### Replicar o modelo funcional na especificação

Daria a um leitor arquivista a sensação de completude e é o que uma leitura
apressada de OAIS sugere fazer. Falha em dois pontos: o NDF passaria a descrever
obrigações que não consegue verificar nem impor — exatamente a fronteira de
ADR-022 —, e descreveria o comportamento de um sistema que vive noutro
repositório, ficando desatualizado sem que ninguém desse por isso.

### Não usar OAIS de todo, e desenhar do zero

É o estado anterior quanto a L-T1–L-T3. Foi recusado já em
`PREMIS-METS-MAPPING.md` §1 com o argumento que se mantém: inventar o que está
resolvido há duas décadas é a escolha mais rápida e a pior, e afasta o formato
da língua em que um arquivista formula a pergunta.

### Adotar OAIS integralmente noutro repositório e não decidir aqui

Adiar não resolve: as três lacunas são de formato, e o desenho do conjunto de
transferência começa agora. Sem critério escrito, cada cláusula parecerá
razoável isoladamente — que é o mecanismo de deslize descrito em ADR-022.

## Consequências

**Positivas**: o desenho do conjunto de transferência passa a ter fronteira
antes de começar, e pode ser escrito em vocabulário OAIS/PREMIS desde a primeira
linha sem risco de importar funções de arquivo. A divisão de trabalho entre
`normordis-formats` e o sistema produtor fica escrita, e não pressuposta: as
funções OAIS que o NORMORDIS venha a exercer pertencem ao `core-ingest` e à
aplicação, que as documentam nos seus próprios repositórios.

**Negativas / mitigações**: a fronteira é mais difícil de traçar em casos
concretos do que em abstrato — a *evidência transferível* de L-T2, por exemplo,
é artefacto (viaja) mas o critério de o que nela entra tem componente de
política. A mitigação é o teste ser aplicado ao artefacto, nunca à decisão:
o formato fixa **que** o conjunto de eventos transferíveis é declarado e
verificável; **quais** eventos uma entidade transfere é política dessa entidade.

Uma implementação NORMORDIS não se torna, por usar NDF, um arquivo conforme
OAIS, um prestador qualificado de serviços de confiança, nem um serviço
qualificado de arquivo eletrónico. Continua a poder integrar-se com qualquer
deles.

## Referências

- [`docs/interoperability/INTEROPERABILITY-LAYERS.md`](../interoperability/INTEROPERABILITY-LAYERS.md) §3, §6 — `R13`
- [`docs/interoperability/PREMIS-METS-MAPPING.md`](../interoperability/PREMIS-METS-MAPPING.md) §5, §6
- [`docs/design/NDFPKG-CAPTURA-E-INGESTAO.md`](../design/NDFPKG-CAPTURA-E-INGESTAO.md) §11.2 — L-T1 a L-T4
- [ADR-022](ADR-022-dever-do-formato.md) — dever do formato e teste operacional
- [ADR-020](ADR-020-um-formato-duas-realidades.md), [ADR-021](ADR-021-componentes-nos-bytes-assinados.md)
- OAIS (ISO 14721 / CCSDS 650.0-M), PREMIS Data Dictionary, METS — **edições e cláusulas não verificadas**; ver `PREMIS-METS-MAPPING.md` §6
