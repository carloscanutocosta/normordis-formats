# Camadas de interoperabilidade do NDF

**Estado:** informativo. Não altera a especificação nem acrescenta requisitos.
**Data:** 2026-08-11
**Origem:** achado `R13` e secção 5.2 de
[`../reports/READINESS-ASSESSMENT.md`](../reports/READINESS-ASSESSMENT.md);
decisão de sequenciamento D2 em [`../../ROADMAP.md`](../../ROADMAP.md).

Este documento existe para responder, de forma estável, à pergunta «e a
interoperabilidade?» — e para evitar que ela seja respondida com o adapter
errado.

---

## 1. A distinção que organiza tudo o resto

> **O NDF é um formato de documento, não um formato de dados.**

Um formato de **dados** transporta o dado de negócio entre sistemas: quem
declarou o quê, que valores, que campos. Vive nas bases de dados das áreas
funcionais e é aí que é a fonte de verdade.

Um formato de **documento** transporta o artefacto já produzido e finalizado:
o conteúdo tal como foi fixado, os metadados descritivos e de segurança, a
avaliação arquivística, as relações com outros documentos, os intervenientes,
e a prova de integridade e autenticidade que os cobre.

O NDF ocupa a segunda camada. Isto é coerente com o princípio de âmbito já
fixado em [`../../LACUNAS.md`](../../LACUNAS.md): o `documento` no NDF-core
contém os dados necessários à reconstituição do documento, *sem pretender
substituir a existência desses dados nas bases de dados das respetivas áreas
de negócio*.

---

## 2. Consequência: XML de dados não é a interoperabilidade relevante

Os contratos XML institucionais mais visíveis — SAF-T PT, perfis de faturação
eletrónica, formatos de submissão fiscal — são contratos de **intercâmbio de
dados**. Um adapter entre esses formatos e o NDF conflacia as duas camadas:

| Direção | O que faria | Porque não acrescenta |
|---|---|---|
| XML → NDF | construir um documento a partir de dados | é o que a aplicação produtora já faz, a partir dos seus próprios dados; o adapter acrescenta um desvio, não uma capacidade |
| NDF → XML | extrair de volta os dados | descarta exatamente o que faz do NDF um documento — assinatura, custódia, avaliação — e devolve dados que o sistema de origem já detinha |

Isto **não** significa que sistemas que falam XML não possam trabalhar com
documentos NDF. Significa que a ponte natural não é uma conversão de formato:
é a referência. Um sistema aplicacional guarda o seu dado como sempre guardou,
e referencia o documento produzido por `ndf_id` e `payload_hash` — como já
previsto em SPEC §2.3 e §2.11.

A serialização do NDF-core permanece JSON canónico (JCS/RFC 8785). A
justificação arquitetural está em
[`../architecture/ADR-001-json-not-xml.md`](../architecture/ADR-001-json-not-xml.md),
e SPEC §1.3 já estabelece que integrações cujo contrato externo exija XML, UBL
ou outro formato usam adaptadores explícitos, sem que isso torne o XML uma
serialização normativa alternativa do NDF-core.

---

## 3. Onde a interoperabilidade é relevante: a camada de pacote

Existem contratos — muitos deles em XML — que operam ao nível do **documento e
do pacote**, e não dos dados. Esses partilham camada com o NDF, e é aí que a
questão da interoperabilidade se coloca com sentido.

| Contrato | Camada | Questão a que responde |
|---|---|---|
| OAIS (ISO 14721) — pacotes SIP/AIP/DIP | pacote de submissão e arquivo | Como é que um documento entra num arquivo definitivo e lá permanece? |
| METS + PREMIS | estrutura do pacote e metadados de preservação e fixidez | Como se descrevem a estrutura, a proveniência e as verificações de integridade ao longo do tempo? |
| ETSI ASiC | contentor assinado | Como se compara o `.ndfpkg` com um contentor assinado normalizado em contexto eIDAS? |
| EAD | descrição arquivística | Como é que o documento se liga ao catálogo e ao quadro de classificação do arquivo? |

A especificação já assumiu compromissos neste terreno: SPEC §1.1 declara o
apoio à gestão arquivística e refere ISO 15489-1, MoReq2017 e o MEG/DGLAB, e o
§3 integra a avaliação (PCA e destino final) dentro dos bytes assinados. Um
formato que se declara adequado ao arquivo definitivo tem de conseguir
explicar como chega lá.

**A pergunta de interoperabilidade que interessa é, portanto:**

> Como é que um `.ndfpkg` é depositado num arquivo conforme OAIS, e o que é que
> o depósito preserva, transforma ou descarta?

Esta pergunta está por responder. É a que um arquivista competente colocará —
corresponde ao gate externo 3 de
[`../normalization/READINESS.md`](../normalization/READINESS.md) — e é também
uma boa porta de entrada para a demonstração de necessidade institucional
(gate externo 7).

---

## 4. Pontos de contacto que já existem no formato

Nada do que precede exige alteração ao NDF. Os elementos necessários a um
mapeamento futuro já estão especificados:

| Necessidade típica de um pacote de submissão | Onde já existe no NDF |
|---|---|
| Identificador estável do objeto | `ndf_id` (SPEC §2.3) |
| Fixidez / *checksum* verificável | `payload_hash` e `payload_hash_alg` (SPEC §2.5); inventário do `.ndfpkg` (SPEC §8.2) |
| Proveniência e cadeia de eventos | log de custódia encadeado, Perfil de Ciclo de Vida (SPEC §2.4.2, §9.5) |
| Metadados descritivos | `metadados` (SPEC §2.7) |
| Retenção e destino final | `avaliacao` (SPEC §3) |
| Relações entre objetos | `relacoes[]` (SPEC §2.11) |
| Representação visual preservável | PDF/A gerado a partir de NDF + NDT |
| Autenticidade de longo prazo | envelope com CAdES-B-LTA e timestamps (SPEC §4) |

O trabalho futuro é de **mapeamento e demonstração**, não de acrescento ao
formato — o que é compatível com o congelamento de âmbito decidido em D5.

---

## 5. Posição resumida, para uso em debate

1. O NDF é formato de documento; os dados continuam a viver, e a ser fonte de
   verdade, nos sistemas aplicacionais.
2. Converter XML de dados em NDF, ou o inverso, não demonstra a proposta de
   valor do formato — e por isso não está no caminho crítico.
3. A ponte com sistemas que falam XML de dados faz-se por **referência**
   (`ndf_id`, `payload_hash`), não por conversão.
4. A interoperabilidade que interessa demonstrar é ao nível do **pacote
   documental**, com o depósito arquivístico conforme OAIS como primeiro caso.
5. Os elementos necessários a esse mapeamento já existem no NDF; falta o
   mapeamento e a evidência, não especificação nova.

### 5.1 Quanto de OAIS entra no NDF

A pergunta de §3 tem, desde 2026-08-23, uma fronteira decidida: o NDF adota o
**modelo de informação** de OAIS e deixa fora o **modelo funcional** e as
responsabilidades organizacionais. O critério, as consequências para as lacunas
de transferência L-T1 a L-T4 e as formulações defensáveis em texto público estão
em [ADR-024](../architecture/ADR-024-fronteira-oais-modelo-de-informacao.md).

---

## 6. Não-objetivos

Este documento não define um perfil de mapeamento, não estabelece requisitos de
conformidade, e não constitui alegação de compatibilidade com OAIS, METS,
PREMIS, ASiC ou EAD. Qualquer alegação nesse sentido exige mapeamento
documentado e validação por competência arquivística.
