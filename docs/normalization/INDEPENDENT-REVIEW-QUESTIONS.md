# Perguntas para revisão independente delimitada (Fase 1E, P2.1)

**Estado:** sem contribuidor externo identificado. Este documento prepara
perguntas concretas para quando houver — não é, por si só, uma revisão
jurídica, criptográfica ou arquivística, e não fecha nenhum gate.

## Objetivo

A matriz de [ROADMAP.md, P2.1](../../ROADMAP.md#p21--revisão-independente-delimitada)
lista quatro temas por um título curto («O perfil e as conclusões do
verificador estão juridicamente bem delimitados?»). Um título curto não é
uma pergunta a que um revisor externo consiga responder de forma acionável —
convida a um parecer genérico sobre o projeto inteiro. Este documento
desdobra cada tema em perguntas concretas, com a referência exata do NDF a
que se aplicam, para que a resposta possa ser sim/não/depende-de-X e ligada
a um requisito.

Opera três gates externos de [READINESS.md](READINESS.md): 2 (revisão
criptográfica), 3 (revisão arquivística) e 4 (revisão jurídica). Contribui
também, indiretamente, para `R4`/`R5` do
[READINESS-ASSESSMENT.md](../reports/READINESS-ASSESSMENT.md) §5.6 — falta de
implementação independente e de necessidade institucional documentada —, na
medida em que um revisor externo que responda a estas perguntas é, ele
próprio, uma forma de escrutínio fora da auto-revisão do mantenedor.

**Não bloqueia P0/P1**, que avançam em paralelo (ver ROADMAP.md). Não tem
data — depende de um contribuidor real se apresentar, tal como o resto desta
secção.

## Como contribuir

Não existe ainda processo dedicado. Até existir, a via é a geral de
[`CONTRIBUTING.md`](../../CONTRIBUTING.md): abrir uma issue identificando a
pergunta (ou subconjunto) a que se responde, a qualificação de quem responde
e, quando aplicável, a fonte (parecer, norma, jurisprudência) em que se apoia
a resposta. Uma resposta sem fundamentação rastreável vale tanto quanto a sua
ausência.

## eIDAS (ação interna associada: P0.4)

Contexto: `nivel_assinatura` é um valor **declarado pelo produtor**
(SPEC.md §2.10); `tools/validate.py` não faz verificação criptográfica de
CAdES nem de cadeia de confiança (SPEC.md §9.4.2,
[NDF-INFORMATIVE-GUIDANCE.md](NDF-INFORMATIVE-GUIDANCE.md#garantias-e-limitações-informativo)).

1. A separação entre "o produtor declara `nivel_assinatura: qualificada`" e
   "nenhuma ferramenta deste repositório verifica que a assinatura
   subjacente é, de facto, uma assinatura eIDAS qualificada válida" está
   explicada de forma que evita a leitura de que o NDF, por si só, comprova
   uma assinatura qualificada nos termos do art. 3.º, ponto 12, do eIDAS?
   Se não, que texto falta e onde?
2. O mecanismo de re-selagem periódica previsto para a v1.1.0 (roadmap,
   `NDF-INFORMATIVE-GUIDANCE.md`) — re-timestamping sem alterar
   `payload_bytes` — é suficiente para o requisito de preservação a longo
   prazo do art. 34.º do eIDAS e do ETSI EN 319 122 (CAdES B-LTA), ou falta
   um procedimento que o NDF ainda não descreve?
3. O laboratório CAdES sem cartões previsto em P1.1 (identidades fictícias,
   certificados de laboratório) produz prova técnica suficiente da
   arquitetura de assinatura, ou qualquer afirmação pública de conformidade
   eIDAS exige adicionalmente um certificado qualificado real emitido por um
   PSC, que o projeto não tem (ver `CADES-GATE-PLAN.md`)?

## RGPD (ação interna associada: P0.4)

Contexto: o NDF é imutável após finalização (SPEC.md §2.1); alteração de
conteúdo exige um novo NDF ligado por `relacoes[{tipo:"substitui"}]`
(SPEC.md §2.11.2); eliminação associa-se a `avaliacao.destino_final` no
termo do PCA (SPEC.md §3.4); `metadados.protecao_dados.responsavel_tratamento`
identifica o responsável pelo tratamento (SPEC.md §1.4).

1. Um novo NDF que substitui o anterior via `relacoes[{tipo:"substitui"}]`
   é juridicamente equivalente a uma retificação do registo original nos
   termos do art. 16.º do RGPD, ou a imutabilidade de fundo exige que o
   responsável pelo tratamento comunique a retificação por um ato adicional
   que o NDF não captura?
2. `destino_final: eliminacao` aplicado no termo do PCA cumpre, por si só, o
   direito ao apagamento do art. 17.º, ou depende de um processo
   institucional de eliminação efetiva fora do NDF — que o formato não pode
   certificar nem o validador de referência verifica?
3. `metadados.protecao_dados.responsavel_tratamento` (um campo de texto,
   SPEC.md §1.4) identifica o responsável pelo tratamento nos termos do
   art. 4.º, ponto 7, de forma suficiente para efeitos de prestação de
   contas do art. 5.º, n.º 2, ou são necessários campos adicionais (ex.:
   subcontratante, base legal explícita por categoria de dados, em vez de
   só `protecao_dados.base_legal_conservacao`)?

## CRA (ação interna associada: P0.4)

Contexto: `CRA_REPORTING.md` assume por precaução que o ecossistema pode vir
a ser "produto com elementos digitais" nos termos do Regulamento (UE)
2024/2847, condicionado a haver "disponibilização no mercado" no decurso de
atividade comercial (art. 3.º, ponto 22).

1. O critério de "atividade comercial" do `CRA_REPORTING.md` (considerandos
   15, 18, 19) está corretamente aplicado à distribuição atual deste
   repositório e de `normordis-pdf`, ou há um cenário de financiamento
   (ex.: subvenção NGI/NLnet, prevista na Fase 1E e em
   [`candidatura-ngi-nlnet`](../../ROADMAP.md)) que o reclassifica?
2. Se o NORMORDIS entrar em âmbito do CRA, quem assume as obrigações de
   fabricante — o mantenedor da especificação, um core-documental
   institucional que a implemente, ou a entidade que efetivamente assina e
   distribui um NDT/schema de extensão de terceiro? A especificação, por si
   só, não é "produto com elementos digitais"; onde é que essa fronteira
   fica clara para quem for construir sobre o NDF?

## Arquivística (sem ação interna associada — pergunta direta)

Contexto: conjunto de transferência (`.ndfxfer`,
[`docs/design/NDF-CONJUNTO-DE-TRANSFERENCIA.md`](../design/NDF-CONJUNTO-DE-TRANSFERENCIA.md)),
explicitamente "não constitui alegação de conformidade com OAIS, METS ou
PREMIS"; extrato de cadeia de custódia (`evidencia/*.evidencia.json`,
exemplificado em `ndfxfer-example`); perfil `pt-dglab`
(`avaliacao.classificacao_ref`/`instrumento_ref`, SPEC.md §3.2) — marcado
como experimental do projeto, sem aprovação DGLAB (P0.1).

1. O conjunto de transferência e o extrato de cadeia de custódia contêm a
   informação mínima que a ISO 15489-1:2016 §5.3 e o MoReq2017 (R6) exigem
   para um arquivo definitivo aceitar uma unidade documental sem acesso ao
   sistema de origem? Que campo falta, se algum?
2. A sintaxe `classificacao_ref`/`instrumento_ref` do perfil `pt-dglab`
   (`<instrumento>/<código>`, SPEC.md §3.2.1–§3.2.2) é suficiente para um
   arquivista classificar e aplicar um PCA real sem interpretação ad-hoc, ou
   faltam categorias do MEG que este perfil experimental não capture?
3. `omitidos.contagem` e a distinção entre extrato parcial e íntegro
   (`ndfxfer-example`, caso "Requerimento": 4 de 6 eventos transferidos,
   2 retidos com fundamento) correspondem ao que a prática arquivística
   portuguesa reconhece como evidência válida de uma cadeia de custódia
   truncada, ou falta uma forma de atestação que este desenho não prevê?
4. Que informação pertence estruturalmente ao sistema custodiante de origem
   e **não deve** ser exigida numa transferência — para que o conjunto de
   transferência não acabe, por excesso de zelo, a pedir dados que o
   destinatário não tem direito de receber ou não tem onde guardar?

## Ligação a outros gates

Contributo externo em criptografia (revisão do ADR-026 e do laboratório
CAdES de P1.1), arquivística (as perguntas acima) e jurídico (as três
primeiras secções) fecha, respetivamente, os gates externos 2, 3 e 4 de
READINESS.md. O gate 6 (implementação independente) e o gate 7 (necessidade
institucional documentada) não são respondidos por este documento — ver
`R4`/`R5` em READINESS-ASSESSMENT.md.
