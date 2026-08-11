# Roadmap NGI MVP 2026

> **⚠️ Parcialmente superado (2026-08-11).** As decisões de sequenciamento
> registadas em [`../../ROADMAP.md`](../../ROADMAP.md) e fundamentadas em
> [`../reports/READINESS-ASSESSMENT.md`](../reports/READINESS-ASSESSMENT.md)
> alteram este plano em três pontos:
>
> - **D1** — a abertura do debate/revisão pública deixa de ter data e passa a
>   ter condição de evidência: `normordis-pdf` funcional. Os prazos dos marcos
>   M2–M5 abaixo **deixam de vigorar**.
> - **D2** — a etapa XML (M3, `normordis-xml-adapters`) **sai do caminho
>   crítico**. O fluxo de demonstração passa de
>   `XML → NDF → NDT → PDF` para `NDF → NDT → PDF`, com ODF depois. A tese de
>   interoperabilidade das secções 2 e 11 precisa de ser reenquadrada — ver
>   achado `R13`.
> - **D5** — o âmbito do NDF-core está congelado; o esforço desloca-se para
>   NDT, NCRTF, `normordis-pdf` e `normordis-odf`.
>
> O que se mantém válido: a tese de financiamento (secção 2), o caso
> transversal Modelo 3 IRS (secção 4), as decisões de arquitetura (secção 5),
> a matriz de riscos (secção 9) e o orçamento indicativo (secção 10). O que
> caducou: as datas dos marcos e a centralidade do XML.

**Estado:** orientação de trabalho, parcialmente superada — ver aviso acima  
**Data:** 2026-06-27 (aviso de superação: 2026-08-11)  
**Horizonte original:** demonstração operacional até 2026-09-30; candidatura/apresentação em outubro de 2026  

Este documento fixa a memória de orientação para preparar uma candidatura NGI
ou equivalente sem dispersar a arquitetura NORMORDIS. O objetivo é transformar
o trabalho já feito em evidência demonstrável: especificações abertas,
fixtures, adapters, validação e uma demonstração documental fim-a-fim.

## 1. Objetivo

Entregar um MVP open source que demonstre interoperabilidade documental
verificável com formatos públicos/institucionais:

```text
Modelo 3 IRS sintética
  -> XML de interoperabilidade
  -> adapter XML
  -> NDF-core canónico validado
  -> envelope/hash/evento de transformação
  -> NDT
  -> renderização PDF via normordis-pdf
```

O MVP deve provar que NDF, NDT e NCRTF podem servir como núcleo aberto para
documentos institucionais preserváveis, auditáveis e interoperáveis, mantendo
separadas as responsabilidades de dados, template, texto rico, prova e
adapters.

## 2. Tese para financiamento

NORMORDIS permite interoperabilidade documental de interesse público sem
prender cidadãos, instituições ou fornecedores a um formato proprietário. O
documento torna-se:

- verificável por bytes canónicos, hash e código de validação;
- preservável por envelope, custódia e prova append-only;
- renderizável por templates NDT independentes dos dados;
- interoperável por adapters externos para XML, PDF e, futuramente, ODF;
- implementável por terceiros com schemas, fixtures e suites de conformidade.

O pedido de financiamento deve focar um pacote pequeno e verificável, não o
ecossistema inteiro. Um intervalo plausível para uma primeira candidatura é
**5 000 EUR a 25 000 EUR**, ajustado ao programa concreto e ao trabalho
elegível.

## 3. Repositórios envolvidos

| Repositório | Papel no MVP |
|---|---|
| `normordis-spec` | Fonte normativa: NDF, NDT, NCRTF, schemas, registry, conformance, Modelo 3 sintética |
| `normordis-pdf` | Renderização NDF+NDT para PDF/PDF-A e validação visual do template |
| `normordis-xml-adapters` | Adapter externo XML <-> NDF para interoperabilidade com formatos públicos |
| `normordis-tools` | Ferramentas CLI de validação, canonicalização, empacotamento e inspeção, se separadas do spec |

`normordis-spec` continua a ser o núcleo. Os adapters podem revelar lacunas,
mas não redefinem NDF, NDT, NCRTF, canonicalização, envelope, custódia ou
assinaturas.

## 4. Caso transversal: Modelo 3 IRS

A Modelo 3 IRS deve continuar a ser o exemplo principal do MVP porque já está
representada no repositório e pressiona dados, layout e interoperabilidade ao
mesmo tempo.

Uso previsto:

| Camada | Função |
|---|---|
| XML | Interoperabilidade com contratos externos e validação estrutural |
| NDF-core | Dados normalizados, canónicos e auditáveis |
| Envelope | Hashes, código de validação, assinaturas/provas e eventos |
| NDT | Layout do rosto/anexos e regras de renderização |
| PDF | Saída humana, comparação visual e portabilidade |

O fixture deve ser sintético. Dados reais de contribuintes não devem ser usados
em documentação, testes, demos públicas ou candidaturas.

## 5. Decisões de arquitetura

1. O NDF-core permanece JSON canónico via JCS/RFC 8785.
2. XML é adapter de interoperabilidade, não serialização normativa alternativa
   do NDF-core.
3. PDF é saída/evidência/renderização, não modelo de dados.
4. ODF fica fora do MVP inicial; entra depois para testar edição, estilos e
   rich text.
5. Quando uma entrada externa tiver valor legal ou probatório, os bytes
   originais devem ser preservados como evidência e referenciados por hash.
6. Assinaturas originais em XML, PDF, CAdES, PAdES, XAdES ou XMLDSig não devem
   ser "convertidas"; devem ser preservadas e acompanhadas por prova
   append-only.
7. Qualquer lacuna descoberta nos adapters deve gerar proposta no
   `normordis-spec` com schema, fixture, vetor ou validação associada.

## 6. Escopo do MVP

### Dentro do escopo

- Modelo 3 IRS sintética com Rosto e Anexo A.
- Perfil XML inicial para Modelo 3, com mapeamento XML -> NDF.
- Exportação NDF -> XML limitada ao mesmo perfil, se couber no prazo.
- Validação NDF usando schemas e `tools/validate.py`.
- Hash do XML original preservado no fluxo de evidência.
- NDTs existentes para Modelo 3 usados como base de renderização.
- Renderização PDF demonstrável via `normordis-pdf`.
- README público, demo script e pacote de candidatura.

### Fora do escopo

- Certificação oficial AT.
- Submissão real ao Portal das Finanças.
- Cobertura integral de todos os anexos da Modelo 3.
- Suporte genérico a XML arbitrário.
- ODF.
- Fixtures com dados pessoais reais.
- CAdES-B-LTA real como requisito bloqueante do MVP; permanece gate externo,
  salvo se houver tempo/parceria para o resolver.

## 7. Milestones

### M0 - Congelamento do pacote de candidatura

**Prazo:** 2026-07-15

Entregáveis:

- escopo MVP aceite;
- lista de repositórios e responsabilidades;
- issue/milestone por repositório;
- versão curta da tese de financiamento;
- inventário do que já existe no `normordis-spec`;
- decisão sobre a variante Modelo 3 usada na demo.

Critério de pronto:

- qualquer pessoa consegue ler este roadmap e saber o que será entregue até
  setembro.

### M1 - Baseline NDF/NDT validável

**Prazo:** 2026-07-31

Entregáveis:

- `normordis-spec` com validação verde;
- Modelo 3 sintética validada contra o registry atual;
- NDT Modelo 3 Rosto + Anexo A verificados contra o schema NDT;
- lista de gaps que bloqueiam `normordis-pdf`;
- script de validação reproduzível documentado.

Critério de pronto:

- `tools/validate.py` passa localmente e o caso Modelo 3 permanece render-ready.

### M2 - Alinhamento `normordis-pdf`

**Prazo:** 2026-08-15

Entregáveis:

- renderização PDF mínima para Modelo 3 Rosto + Anexo A;
- relatório de limitações de renderização;
- comparação visual/manual documentada;
- decisão sobre PDF/A-3 e eventual embedding de NDF-core;
- erros de layout convertidos em issues NDT quando forem de especificação.

Critério de pronto:

- existe um PDF gerado a partir de NDF+NDT, suficientemente estável para demo
  técnica.

### M3 - Skeleton `normordis-xml-adapters`

**Prazo:** 2026-08-31

Entregáveis:

- repositório criado;
- estrutura `profiles/at/modelo3-irs/`;
- fixture XML sintético;
- mapeamento XML -> NDF documentado;
- preservação de hash do XML original;
- casos positivos e negativos mínimos;
- README com aviso explícito de não-certificação AT.

Critério de pronto:

- um comando ou script transforma o XML sintético em NDF-core validável.

### M4 - Demo fim-a-fim

**Prazo:** 2026-09-15

Entregáveis:

- fluxo XML -> NDF -> validação -> NDT -> PDF;
- hashes e artefactos guardados;
- demo script reproduzível;
- screenshots/PDF de saída;
- documentação de perdas e limites;
- lista de requisitos satisfeitos e gates externos.

Critério de pronto:

- uma pessoa externa consegue reproduzir a demo a partir do README.

### M5 - Pacote de candidatura

**Prazo:** 2026-09-30

Entregáveis:

- resumo executivo;
- problema, solução, inovação e impacto;
- plano de trabalho e orçamento;
- milestones financiáveis;
- matriz de riscos;
- links para repos, testes e demo;
- licença/open source statement;
- pedido de revisão por uma pessoa externa.

Critério de pronto:

- o projeto pode ser submetido ou apresentado sem precisar explicar a
  arquitetura do zero numa conversa síncrona.

## 8. Critérios de pronto do MVP

O MVP está operacional quando:

- há uma Modelo 3 sintética em XML e NDF;
- o NDF valida contra schema e regras semânticas atuais;
- existe hash verificável do XML original;
- existe evidência de transformação XML -> NDF;
- NDF+NDT gera PDF demonstrável;
- a demo é reproduzível localmente;
- os limites são declarados sem overclaim;
- a candidatura consegue apontar para artefactos públicos e testes.

## 9. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Escopo cresce para todos os anexos IRS | limitar a Rosto + Anexo A |
| Confusão entre interoperabilidade e certificação AT | usar sempre "fixture público/sintético", não "certificação" |
| `normordis-pdf` bloqueia em fidelidade visual | aceitar renderização demonstrável e declarar gaps |
| XML puxa o NDF para outro modelo | manter adapter fora do core e referenciar ADR-001 |
| Assinaturas reais atrasam o MVP | manter CAdES/XAdES/PAdES real como gate externo |
| Falta de tempo para ODF | deixar ODF como segunda candidatura ou milestone posterior |
| Candidatura exige impacto mais claro | focar digital commons, interoperabilidade, auditabilidade, privacidade e independência de fornecedor |

## 10. Orçamento indicativo

Um orçamento inicial deve ser pequeno, auditável e ligado aos entregáveis.

| Item | Justificação |
|---|---|
| Desenvolvimento | adapters XML, alinhamento PDF, validação e scripts |
| Documentação | specs, README, demo, material de candidatura |
| Testes/conformance | fixtures, casos negativos, CI e reprodução local |
| Infraestrutura | runners, domínio/site/demo mínima, armazenamento de artefactos |
| Revisão externa | revisão técnica, arquivística, jurídica ou acessibilidade quando possível |

O orçamento deve distinguir trabalho futuro financiável de custos já realizados.
Os custos passados podem ser apresentados como investimento próprio e evidência
de tração, mas só devem ser pedidos como reembolso se a chamada concreta o
permitir.

## 11. Mensagem curta

> NORMORDIS is an open, verifiable document interoperability layer for public
> interest records. It separates canonical data, templates, rich text,
> original evidence and adapters, enabling institutions and citizens to preserve
> and exchange documents without vendor lock-in.

## 12. Memória futura

Decisões a não perder:

- o objetivo até outubro é financiamento e demonstração operacional, não
  normalização completa;
- Modelo 3 IRS continua o fio narrativo principal;
- XML vem depois do alinhamento PDF porque testa interoperabilidade semântica;
- `normordis-xml-adapters` deve ser projeto irmão, não extensão do core;
- SAF-T PT e outros formatos XML públicos podem ser perfis futuros, mas a
  primeira demo deve ficar pequena;
- ODF é importante, mas deve esperar até XML/PDF provarem o ciclo base;
- qualquer alegação jurídica ou de conformidade oficial deve ser evitada até
  haver validação externa.

