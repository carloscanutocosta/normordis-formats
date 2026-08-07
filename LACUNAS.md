# Lacunas e pontos a melhorar — NDF

**Estado:** análise crítica, não normativa. Não implica que qualquer ponto
aqui listado deva ser resolvido no NDF-core — muitos são explicitamente
**fora de âmbito**, conforme a nota de âmbito abaixo. Este documento distingue
os dois casos.

**Origem:** revisão adversarial pedida pelo responsável do projeto após a
consolidação registada em `docs/reports/NDF-STABILIZATION-REPORT.md`
(commits `3160496`, `70e6ca8`).

---

## Princípio de âmbito (determinante para ler o resto deste documento)

> O NDF pretende ser um formato eficiente para guardar documentos,
> reconstituíveis (em conjunto com o NDT) — não substitui os workflows
> específicos de cada procedimento. O `documento` no NDF-core contém os
> dados especificamente necessários à reconstrução do documento, sem
> pretender substituir a existência desses dados nas bases de dados das
> respetivas áreas de negócio.

Isto estabelece um teste claro para qualquer lacuna identificada:

- **Dentro de âmbito**: algo necessário para reconstituir, verificar a
  integridade, ou interpretar corretamente o *conteúdo imutável* de um
  documento já finalizado — mesmo que isso inclua contexto sobre a sua
  produção (autoria, relação com outros documentos, proveniência de IA).
- **Fora de âmbito**: estado de um procedimento, regras de workflow, quem
  *deve* agir a seguir, prazos processuais, entrega/notificação, ou
  qualquer facto que ocorra depois da finalização do documento e que pertença
  à gestão do procedimento, não ao documento em si. Isso é responsabilidade
  do sistema de gestão documental/processual (GED/GCA), que pode referenciar
  o NDF por `ndf_id`/`payload_hash`, mas não precisa de o NDF o modelar.

Vários pontos da análise original foram reformulados ou retirados por
aplicação deste teste.

---

## Lacunas que se mantêm (dentro de âmbito do NDF)

### L1 — Legitimidade das relações não é validada, só a integridade

`relacoes[]` prova que o `payload_hash` do alvo é real — não prova que o
alvo reconhece, consente, ou tem conhecimento da relação. Um documento pode
declarar `"decide_sobre"` ou `"anula"` outro documento real, assinado por
uma entidade legítima, sem que isso implique competência ou autoridade para
o fazer. Isto é uma propriedade que o **NDF deve documentar explicitamente
como limitação**, não tentar resolver com validação adicional — decidir
*quem tem autoridade* para estabelecer que tipo de relação é, precisamente,
uma questão de workflow/competência processual, fora de âmbito. O que falta
não é mais lógica no formato; é uma frase normativa clara dizendo isto.

**Recomendação**: acrescentar a SPEC.md §2.11 uma nota normativa —
*"uma relação DEVE ser interpretada como uma afirmação unilateral e
assinada da entidade produtora do documento de origem; não implica
reconhecimento, consentimento, nem validação de competência por parte da
entidade produtora do documento alvo. A validação de autoridade para
estabelecer uma relação é responsabilidade do sistema de gestão processual,
fora do âmbito desta especificação."*

### L3 — Ciclos no grafo de relações não são tratados

O vocabulário fechado não impede ciclos (A `substitui` B, B `substitui` A).
Isto é puramente estrutural/format-level — dentro de âmbito.

**Recomendação**: nota de implementação para verificadores/renderizadores
que percorram o grafo (deteção de ciclos obrigatória), já que o schema por
si só não pode impor acircularidade num grafo distribuído entre documentos
independentes.

### L4 — Vocabulário de `relacoes[]` sem via de extensão institucional

Ao contrário de `tipo_documento_ref` (registo extensível por entidade),
`relacoes[].tipo` só se estende por nova versão minor da especificação
base. Isto é uma inconsistência de arquitetura do formato, não uma questão
de workflow — dentro de âmbito.

**Recomendação**: equacionar, numa versão futura, um mecanismo de extensão
qualificada (namespace) para tipos de relação específicos de domínio,
espelhando o modelo já usado para tipos de documento.

### L5 — `despacho.sobre[]` vs `relacoes[]`: coerência só recomendada, nunca imposta

Nenhuma validação impede que os dois campos divirjam quando ambos
presentes. É uma questão de integridade interna do documento — dentro de
âmbito.

**Recomendação**: adicionar verificação semântica em `tools/validate.py`
(fora do JSON Schema, que não pode comparar dois campos de proveniências
distintas facilmente) que sinalize divergência como aviso, se não erro.

### L6 — `ndf_id` sem espaço de nomes por entidade produtora

UUIDs v4 puros não distinguem visualmente a entidade produtora, e nada
impede — ainda que improvável — colisão deliberada por um sistema produtor
comprometido. É uma questão de desenho do identificador do próprio formato —
dentro de âmbito.

**Recomendação**: equacionar prefixo estruturado (código DGLAB/NIF da
entidade) em versão futura, sem quebrar compatibilidade do `ndf_id` atual.

---

## Lacunas reformuladas pelo esclarecimento de âmbito

### L7 (era "papel na assinatura não tem imposição face a nivel_assinatura")

**Análise original**: nada impede que um documento `qualificada` seja
assinado só por um `papel: "testemunha"`, sem ninguém com papel de decisor
assinar.

**Revisão**: decidir *quem deve assinar em que papel* para um ato ser
válido é uma regra de competência/delegação específica de cada procedimento
e entidade (CPA, estatutos, normas internas de delegação) — exatamente o
tipo de regra que o NDF **não deve** codificar, pela mesma razão que
`nivel_assinatura` já delega essa responsabilidade à entidade produtora
(SPEC.md §2.10.2: *"a classificação correta de um ato [...] é
responsabilidade da entidade produtora"*). Impor uma correspondência
`papel`↔`nivel_assinatura` no schema seria o NDF a assumir uma regra de
negócio processual — precisamente o que a nota de âmbito exclui.

**Recomendação revista**: nenhuma alteração ao schema. Acrescentar, no
máximo, uma frase explícita em SPEC.md §4.4.1 confirmando que a
correspondência entre `papel` e a exigência legal de quem deve assinar é
responsabilidade da entidade produtora, não uma garantia do formato — o
mesmo padrão de not-my-job já usado para `nivel_assinatura`.

### L8 (era "delegação de competências só existe no tipo despacho")

**Análise original**: só `despacho.decisor.delegacao_ref` existe; falta um
mecanismo geral no NDF-core.

**Revisão**: a referência à delegação (`delegacao_ref`) é dado de
**reconstrução do documento** — precisa de aparecer no PDF renderizado como
"por delegação de X" — logo está dentro de âmbito. Mas não precisa de ser
um bloco estrutural do NDF-core: é conteúdo específico do tipo de
documento, tal como já acontece em `despacho`. Elevá-lo a bloco genérico do
core seria tratar como preocupação transversal algo que só faz sentido no
`documento` de tipos que envolvem decisão.

**Recomendação revista**: não criar bloco novo no NDF-core. Estender o
padrão já existente em `despacho.schema.json` (`decisor.delegacao_ref`) aos
demais tipos do registo onde for relevante (`parecer`, `informacao-tecnica`)
como trabalho de registo, não de especificação base.

### L9 (era "`participante_ref` é opaco e não interoperável")

**Análise original**: falta de contrato de resolução para `participante_ref`
esvazia o valor de auditoria de `participantes`.

**Revisão**: à luz da nota de âmbito, isto pode não ser um defeito — pode
ser o desenho correto. `avaliacao.tipo_classificacao_ref` também é uma
referência opaca a um instrumento externo (a Lista Consolidada), sem
resolução embutida no NDF; o NDF não duplica o conteúdo desse instrumento,
só referencia-o. `participante_ref` pode seguir o mesmo princípio: uma
referência leve a um registo de identidade que **vive na base de dados do
sistema produtor**, não no NDF. Tentar embutir um esquema de identidade
verificável no NDF seria duplicar dados que já existem — exatamente o que a
nota de âmbito diz para evitar.

**Recomendação revista**: não adicionar infraestrutura de identidade ao
NDF. Documentar explicitamente em SPEC.md §2.12 que `participante_ref` é
uma referência externa não resolvida pelo NDF, por desenho — paralelo
explícito a `tipo_classificacao_ref`.

### L10 (era "`participantes[]` com papéis de workflow: `validador`, `aprovador`")

**Análise original**: nenhuma, este ponto emerge só agora, por autocrítica
ao reler a lista à luz da nota de âmbito.

**Revisão**: alguns dos valores do enum `papel` em `participantes[]`
(`validador`, `aprovador`) descrevem **estado de um fluxo de aprovação**,
não um facto intrínseco ao conteúdo do documento — isso é tipicamente
gerido e já existe na tabela de workflow do GED/GCA. `autor` e
`revisor_humano` (este último também usado em `proveniencia_ia`) são
diferentes: dizem respeito a *quem produziu o conteúdo exato que está
canonicalizado*, o que é dado de reconstrução legítimo. `decisor` e
`representante` ficam num meio-termo — descrevem quem agiu no documento
já finalizado, o que ainda é reconstrutivo (aparece no ato), mas
aproxima-se de estado processual.

**Recomendação revista**: manter `participantes[]`, mas rever se
`validador`/`aprovador` devem continuar no enum do NDF-core ou se pertencem
apenas ao sistema de workflow — sem urgência, não é um erro que quebre
nada, mas vale a pena decidir conscientemente em vez de ter ficado por
omissão do desenho original.

---

## Lacunas retiradas (fora de âmbito do NDF, por decisão)

### L2 (era "fuga de metadados através do grafo, mesmo com conteúdo sigiloso")

**Análise original**: uma relação revela que o documento alvo existe e foi
objeto de ação, mesmo que o conteúdo esteja classificado — classificado
como consideração de segurança dentro de âmbito do NDF, a documentar como
limitação e a equacionar (ex.: relações "opacas" para documentos
classificados).

**Retirada.** A proteção de documentos classificados — incluindo o grafo de
relações que eles contêm — é resolvida ao nível do core-documental: o
`.ndfpkg`/pacote NDF é protegido como artefacto opaco (cifra em repouso e em
trânsito, controlo de acesso do sistema custodiante), não através de
nenhum mecanismo definido pelo NDF. Se o sistema nunca entrega os bytes a
quem não está autorizado, `relacoes[]` nunca chega a ser lido por quem não
deve — não porque o NDF os escondeu, mas porque o acesso ao artefacto
inteiro já foi controlado antes disso.

A razão de fundo para esta decisão, e não só o resultado, está registada em
[`docs/normalization/NDF-INFORMATIVE-GUIDANCE.md`](docs/normalization/NDF-INFORMATIVE-GUIDANCE.md)
— resumidamente: confidencialidade/controlo de acesso é estado vivo de
sistema (quem está credenciado muda ao longo do tempo), ao contrário de uma
assinatura, que precisa de ser verificável por qualquer terceiro para
sempre sem depender de infraestrutura viva. Isso torna-o um problema de
sistema (core-documental), não de formato — pela mesma lógica já aplicada a
L7, L8 e L11.

### L11 (era "nenhuma noção de notificação/comprovativo de entrega")

**Análise original**: classificada como "a lacuna funcional mais importante"
— falta de qualquer mecanismo para registar notificação de um ato.

**Retirada.** Notificação, entrega, e prazos de impugnação são factos
processuais que ocorrem *depois* da finalização do documento e pertencem
inteiramente ao workflow do procedimento — exatamente o que a nota de
âmbito exclui do NDF. Modelar isto no NDF-core duplicaria dados que já
vivem, e devem continuar a viver, no sistema de gestão processual. Se for
necessário ligar um evento de notificação a um NDF, o mecanismo já existe
fora do NDF-core: um evento de custódia (`custody-event.schema.json`, campo
`details`, já livre) referenciando o `ndf_id` — sem exigir alteração ao
NDF-core nem ao envelope.

Este era o ponto de maior desvio de âmbito da análise original — retiro-o
por inteiro, não só reformulo.

---

## Priorização revista

**Dentro de âmbito, a considerar em próxima ronda**: L1 (nota normativa,
sem novo código), L5 (validação de coerência sobre/relacoes),
L9 (documentar `participante_ref` como referência externa não resolvida).

**Dentro de âmbito, sem urgência**: L3, L4, L6, L10.

**Fora de âmbito do NDF, por desenho**: L2 (pertence ao core-documental —
cifra em repouso/trânsito e controlo de acesso ao artefacto), L7, L8 (fica
ao nível do registo, não da especificação base), L11 (pertence ao sistema
de custódia/workflow, não ao NDF).

Note-se que a maioria das ações que sobrevivem são **normativas/documentais**
(clarificar o que o formato não garante), não schema novo — o que é
coerente com a própria nota de âmbito: o NDF já tem os blocos certos: o que
faltava, em grande parte, era dizer com mais clareza o que esses blocos
*não* fazem.
