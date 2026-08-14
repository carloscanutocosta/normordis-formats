# ADR-015: Generalização do bloco `avaliacao` por perfil arquivístico

**Estado**: Aceite
**Data**: 2026-08-14
**Decisores**: carloscanutocosta

---

## Contexto

O bloco `avaliacao` (§3) é obrigatório em todos os NDF-core e exige quatro
campos cujo vocabulário é o do MEG/DGLAB: `tipo_classificacao_ref`,
`prazo_conservacao_administrativa` (PCA), `destino_final` (DF) e
`instrumento_avaliacao_versao_ref`. O enum de `destino_final` tem exatamente os
três valores do modelo português.

Uma entidade fora de Portugal só produz um NDF válido declarando valores num
vocabulário que não é o seu. O problema estava registado — risco **R11** em
`docs/reports/READINESS-ASSESSMENT.md` e item de v2.0.0 em `ROADMAP.md` — em
ambos os casos como "aberto, sem ação", por se aceitar que uma 1.0.0 focada na
Administração Pública portuguesa podia conviver com o acoplamento.

Duas coisas alteraram essa avaliação. Primeiro, o objetivo mais próximo passou a
ser uma candidatura NGI/OSOR, onde o âmbito é europeu e o acoplamento deixa de
ser aceitável. Segundo, a generalização é alteração incompatível: o NDF está em
nível 1 — Draft, sem revisão pública aberta e sem utilizadores externos, logo o
custo de a fazer é hoje o mais baixo que alguma vez será. Adiá-la para v2.0.0
significava publicar uma 1.0.0 sabidamente obsoleta.

Antes de decidir foi verificado se o modelo português é sequer representativo. O
levantamento sobre PT, FR, NL, DE e UK/CoE/Comissão Europeia está em
`docs/design/NDF-AVALIACAO-GENERALIZATION.md` §2. Conclusão: o invariante
`gatilho + prazo + ação de destino + instrumento que a autoriza` está presente em
todos os cinco, e PT e FR são praticamente isomórficos — incluindo o terceiro
valor de destino (amostragem / *tri*), que é a parte menos óbvia. O modelo
português é uma instância nacional de um padrão europeu comum, não uma
idiossincrasia. Isso reduz a generalização a três divergências, todas aditivas.

## Decisão

1. **`avaliacao` passa a declarar um `perfil`** (obrigatório) que identifica o
   sistema arquivístico aplicável. Enum aberto, padrão
   `^([a-z]{2}-[a-z0-9-]+|generic)$`. Cada perfil registado tem schema próprio em
   `specs/registry/profiles/<perfil>.schema.json`.

2. **Renomear os campos cujo nome é um termo legal português**:
   `tipo_classificacao_ref` → `classificacao_ref`;
   `instrumento_avaliacao_versao_ref` → `instrumento_ref`;
   `prazo_conservacao_administrativa` → `prazo_conservacao` (o "administrativa" é
   o **A** de PCA). `destino_final` e `forma_contagem` mantêm-se: traduzem-se
   diretamente para os equivalentes das outras jurisdições.

3. **Acrescentar `destino_final: "a_determinar"`**, com `autoridade_avaliacao`
   obrigatório quando usado. Cobre os sistemas em que a decisão de destino não
   compete ao produtor do documento.

4. **As regras portuguesas passam a ser condicionais ao perfil**, não gerais. O
   formato `<instrumento>/<...>` e a correspondência de prefixo entre
   `classificacao_ref` e `instrumento_ref` (§3.2.2) aplicam-se sob
   `perfil: "pt-dglab"` e apenas aí.

5. **A estrutura mantém-se no core.** `prazo_conservacao` e `destino_final`
   continuam campos concretos do NDF-core, com enums fechados. O perfil restringe
   vocabulário, não substitui estrutura.

6. **O schema do perfil viaja no `.ndfpkg`**, em `schemas/` — mesmo mecanismo e
   mesma justificação de ADR-014 para os schemas de tipo documental.

7. Perfis criados nesta ronda: `pt-dglab` e `generic`. `fr-siaf`, `nl-na`,
   `de-bund` e `eu-crl` ficam como candidatos documentados, a confirmar contra
   fonte primária.

8. As alterações são absorvidas em **1.0.0**, não numa 2.0.0.

## Alternativas consideradas

### Manter `avaliacao` como está e adiar para v2.0.0

**Prós**: nenhum trabalho agora; é a decisão que já estava tomada; a 1.0.0
serviria a Administração Pública portuguesa sem qualquer falha funcional.

**Contras**: publica-se uma 1.0.0 com um defeito conhecido e documentado em dois
sítios do próprio repositório — o que um avaliador externo encontra antes de
qualquer outra coisa. E a correção seria incompatível, obrigando a uma 2.0.0
precoce ou a arrastar o defeito. O argumento que sustentava o adiamento era o
custo de migração; esse argumento é mais fraco agora do que voltará a ser, porque
não há utilizadores. Rejeitado.

### Delegar o bloco `avaliacao` inteiro ao schema do perfil

Isto é, `avaliacao` como objeto aberto contendo apenas `perfil` e o que o perfil
definir.

**Prós**: generalidade máxima; qualquer jurisdição modelável sem alterar a
especificação; nenhuma decisão sobre que campos são universais.

**Contras**: falha o teste que dá sentido à generalização — *um leitor que nunca
ouviu falar do perfil declarado consegue, só com o NDF-core, saber se o documento
é eliminável e a partir de quando?* Com delegação total, não. Perde-se a gestão
de retenção transversal a jurisdições, que é precisamente o que se pretende
ganhar. Perde-se também a validação no core e a força da suite de conformidade,
e cada perfil torna-se mais um artefacto que tem de sobreviver 30 anos dentro do
pacote. Num formato canonicalizado e assinado há ainda um custo específico: cada
grau de liberdade acrescentado cria formas alternativas de exprimir o mesmo
facto, logo `payload_hash` distintos para o mesmo documento. Rejeitado.

### Traduzir as chaves do bloco para inglês

**Prós**: alinharia o vocabulário com o público-alvo internacional.

**Contras**: o NDF-core é integralmente português — `metadados`, `documento`,
`relacoes`, `participantes`, `imputacao`. Traduzir um bloco produziria um formato
bilingue sem critério. A questão da língua é real e é a mesma do risco R3
(ausência de conteúdo em inglês), mas tem de ser decidida para o conjunto.
Rejeitado neste âmbito, sem prejuízo de decisão futura.

### Acrescentar apenas `a_determinar`, sem perfis

**Prós**: alteração mínima; resolve o caso alemão, que é o único bloqueante
absoluto.

**Contras**: deixa intactos os nomes de campo em terminologia legal portuguesa e
a obrigação de exprimir a classificação no formato de instrumento da DGLAB. Uma
entidade neerlandesa passaria a conseguir produzir um NDF válido, mas continuaria
a preencher campos chamados "prazo de conservação administrativa" com referências
no formato da Lista Consolidada. Resolve a validade e não resolve o acoplamento.
Rejeitado.

## Justificação da decisão

O ponto determinante é o resultado do levantamento comparativo: como o modelo
português é uma instância de um padrão comum, a generalização é
**destilada de instâncias reais que divergem**, e não especulativa. Abstrações
assim acomodam com boa probabilidade o sistema seguinte, porque o invariante foi
observado e não inventado. Foi por esse critério que a abstração parou onde
parou — só se generaliza um eixo quando é possível nomear três sistemas reais que
divergem nesse eixo. Para `avaliacao` é possível (PT e FR convergem, NL diverge,
DE diverge); para outros blocos do core, não.

O ponto 4 é o que torna a decisão segura para o utilizador atual: as regras
portuguesas não são enfraquecidas, mudam de âmbito de aplicação. Um NDF com
`perfil: "pt-dglab"` é validado exatamente com o mesmo rigor de hoje.

O ponto 5 é o que a torna segura para o utilizador futuro: um sistema de arquivo
consegue processar retenção sobre um corpo documental multi-jurisdicional sem
resolver perfil nenhum, porque prazo e destino continuam a ser campos concretos
do core.

O ponto 6 é o que a torna verificável a longo prazo, pela mesma razão que ADR-014
invocou: dentro de um `.ndfpkg`, um verificador independente valida o bloco contra
o schema de perfil que veio no pacote, sem acesso a registo nenhum.

## Consequências

**Positivas**: fecha R11; o NDF deixa de ser interpretável como formato da
Administração Pública portuguesa sem deixar de a servir integralmente; passa a ser
exprimível o caso — comum na Europa central e do norte — em que a apreciação
arquivística não compete ao produtor; a suite de conformidade passa a conter
evidência executável de um caso não-PT.

**Negativas / mitigações**: mais um artefacto obrigatório no `.ndfpkg` (o schema
de perfil), mitigado por ser o mecanismo já existente de ADR-014; `perfil` é
enum aberto, logo um perfil desconhecido não é interpretável semanticamente —
mesmo compromisso já aceite em ADR-008 e ADR-014, e mitigado por o schema viajar
no pacote. Perfis para jurisdições não portuguesas exigem confirmação contra
fonte primária antes de serem publicados, e isso é trabalho que este ADR não
resolve.

**Compatibilidade**: **incompatível**. Todo o NDF-core produzido contra o draft
anterior é inválido. Absorvido em 1.0.0 antes de qualquer publicação, ao abrigo
de ADR-007 e do estado nível 1 — Draft. Não existe corpo documental produzido a
migrar.

## Referências

- `docs/design/NDF-AVALIACAO-GENERALIZATION.md` — desenho completo e levantamento comparativo
- SPEC.md §3, §8.3, §9.3
- ADR-014-tipos-documentais-namespace-entidade.md — mecanismo de schema no pacote
- ADR-010-separacao-conformidade-perfil-ciclo-vida.md — precedente de desacoplamento
- ADR-007-versionamento-estabilizacao.md
- `docs/reports/READINESS-ASSESSMENT.md` — R11
