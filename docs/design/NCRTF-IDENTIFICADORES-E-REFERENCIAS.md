# Critério de identificadores e referências internas (NCRTF)

**Estado:** documento de desenho, não normativo. Fixa a direção antes de N2
(referências cruzadas) e A1/A2/A4 avançarem para redação de SPEC, conforme
`ODF-ALIGNMENT-STUDY.md` §9 (Fase A).

**Origem:** pedido do responsável do projeto (2026-08-18), no seguimento da
revisão crítica de `CRITERIO-DE-CAMADAS.md` e `ODF-ALIGNMENT-STUDY.md`, que
identificou os identificadores internos e as referências cruzadas como a
decisão de fronteira mais afiada e ainda por resolver. Âmbito confirmado do
conjunto de formatos: documentos administrativos em geral e documentos
legais/normativos (ex.: diplomas publicados no Diário da República) — ver
`specs/ndt/SPEC.md` §Âmbito.

---

## 1. Porque isto não é um atributo auxiliar

Uma remissão interna ("nos termos do artigo 5.º") só é mais processável do
que texto morto em PDF se resolver para algo. Isso implica um identificador
de bloco (`id`) e um mecanismo de referência (`xref`) — e ambos, ao contrário
do que parecem, têm de responder a um conjunto duro de perguntas antes de
entrarem em qualquer schema:

unicidade, escopo, normalização, sensibilidade a maiúsculas, caracteres
permitidos, estabilidade entre versões, referências quebradas, referências
circulares, alvo de bloco vs. alvo inline, alvo eliminado numa sucessão
documental — e, sobretudo, **se o identificador é conteúdo assinado**.

Este documento aplica o critério de `CRITERIO-DE-CAMADAS.md` a cada uma.

## 2. A pergunta decisiva: o `id` é conteúdo assinado?

Teste de colocação (`CRITERIO-DE-CAMADAS.md` §3): *quando isto mudar, é
preciso reassinar o documento?*

Renumerar `artigo-5` para `artigo-6` muda o que uma remissão existente nesse
mesmo documento resolve. Se o `id` não fosse conteúdo assinado, seria
possível alterar silenciosamente o alvo de uma remissão já publicada sem
tocar na assinatura — exatamente o cenário que a imutabilidade do NDF existe
para impedir.

**Resposta: sim. `id` e `xref.alvo` vivem dentro do `payload_bytes`
assinado, como nós/atributos NCRTF normais.** Não há caminho alternativo que
não reabra o problema que ADR-003 e ADR-011 já fecharam para o documento como
um todo.

Isto tem uma consequência que resolve por si a maior parte da ansiedade em
torno de "estabilidade entre versões": **não existe edição de `id` num
documento finalizado.** Por ADR-011, sucessão é sempre um novo NDF autónomo,
nunca uma alteração interna. Se o diploma B substitui o diploma A e
renumera o que era "artigo 5" para "artigo 6", isso está no NCRTF de B — um
documento novo, assinado de novo. O NCRTF de A permanece, para sempre, com
`artigo-5` exatamente como foi publicado. Não há renumeração silenciosa
possível — o mecanismo que a impede já existe e é o mesmo que impede
qualquer outra edição.

## 3. Modelo proposto

### 3.1 `id` em nós bloco

Campo opcional `id` em nós bloco elegíveis como alvo de remissão:
`heading`, `paragraph`, `list_item`, `table`, `blockquote`.

```json
{ "type": "heading", "level": 2, "id": "artigo-5", "content": [...] }
```

| Regra | Valor |
|---|---|
| Sintaxe | `^[a-z][a-z0-9-]{0,63}$` — minúsculas ASCII, dígitos, hífen. Sem espaços, sem maiúsculas, sem Unicode fora de ASCII. |
| Unicidade | Por documento (todo o `NDF-core.documento`), não por subárvore. |
| Escopo | Local ao documento. Não endereça outro NDF — isso é uma relação distinta (§6). |
| Normalização | Nenhuma — o produtor escreve o `id` já na forma canónica; não há *case-folding* nem normalização Unicode a aplicar em leitura, precisamente para eliminar a pergunta de "que normalização". |

A sintaxe restrita (ASCII, minúsculas, sem espaços) não é estética: elimina
de raiz as perguntas de sensibilidade a maiúsculas e normalização Unicode,
que são a fonte mais comum de referências que resolvem num produtor e falham
noutro. Um `id` fora deste padrão é documento inválido — não um aviso.

### 3.2 `xref` como referência inline

Nó inline novo (candidato §7):

```json
{ "type": "xref", "target": "artigo-5", "content": [{ "type": "text", "text": "artigo 5.º" }] }
```

**Decisão central: o texto visível da remissão é escrito explicitamente pelo
produtor, dentro de `content`, tal como um `link`.** O NCRTF não gera rótulos
a partir de numeração resolvida em tempo de leitura.

Isto elimina o problema mais espinhoso à partida: se gerasse o rótulo
("artigo N.º") a partir da posição do alvo, uma remissão mudaria de
aparência sempre que a estrutura fosse percorrida por um renderizador
diferente, ou precisaria de numeração computada e assinada à parte. Ao
tratar `xref` como um `link` com alvo interno em vez de alvo externo, o
NCRTF mantém-se um formato de conteúdo estático: o que está escrito é o que
foi publicado, tal como qualquer outro texto do ato.

O preço aceite: se um artigo for de facto renumerado, o produtor tem de
escrever o novo texto da remissão — mas isso só acontece num documento novo
(§2), nunca por edição, logo não é um preço pago pela leitura, só pela
produção do sucessor.

### 3.3 Referências quebradas

Regra de canonicalização/conformidade (candidatas a R7/R8, §8.2 NCRTF):

| Ref | Regra proposta |
|---|---|
| **R7** | Todo `xref.target` **DEVE** resolver para um `id` existente no mesmo documento. |
| **R8** | Um `id`, quando presente num nó bloco, **DEVE** ser único no documento. |

Um leitor conforme **DEVE** rejeitar um NCRTF com `xref.target` que não
resolva — o mesmo tratamento que NCRTF-READ-005 já dá a `image.ref` não
resolvido no `.ndfpkg`. Não existe remissão pendente em documento
finalizado: ou resolve, ou o documento é inválido.

### 3.4 Referências circulares

**Permitidas, e não são um erro.** Duas secções de um diploma que se citam
mutuamente são texto legal legítimo (ex.: dois artigos que se remetem um ao
outro para efeitos de aplicação conjunta). Isto contrasta deliberadamente com
`relacoes[]` (grafo entre documentos, onde L3 em `LACUNAS.md` regista ciclos
como questão em aberto): `xref` é um ponteiro de leitura dentro de uma árvore
já fechada, não uma aresta num grafo de proveniência ou sucessão. Um leitor
resolve cada `xref` independentemente; não há travessia que possa entrar em
laço infinito porque não há travessia — é *lookup* num índice de `id`s,
construído uma vez por leitura.

### 3.5 Alvo bloco vs. inline

Só nós bloco (§3.1) podem ser alvo. Só nós inline (`xref`) apontam. Não
existe âncora ao nível de um nó inline (ex.: remeter para uma palavra
específica dentro de um parágrafo). **Fica fora desta ronda** — candidato
futuro se surgir caso de uso documentado (regra do teste de admissão,
`CRITERIO-DE-CAMADAS.md` §8).

### 3.6 Alvo eliminado numa sucessão documental

Não aplicável ao NDF individual — é imutável, um `id` nunca desaparece do
documento que o define (§2). Quando a aplicação de domínio produz um
sucessor que deixa de ter um artigo equivalente, isso é uma decisão de
redação do sucessor, fora do âmbito do formato: o sucessor simplesmente não
declara esse `id`, e quaisquer remissões nesse sucessor que precisassem dele
são responsabilidade editorial de quem o redige — o produtor, não o
formato, garante R7 no documento que está a produzir.

## 4. Referências inter-documento — explicitamente fora deste mecanismo

Uma remissão de um diploma B para "o artigo 5.º do diploma A" **não** é um
`xref` interno. `xref`/`id` resolve dentro de um único NDF; uma referência
entre dois NDF distintos já tem mecanismo — `relacoes[]` (ADR-002, ADR-008),
com `alvo.ndf_id` + `alvo.payload_hash`. Se este caso de uso for confirmado
(remissão legislativa entre diplomas, comum em texto normativo — "revoga o
artigo 3.º do Decreto-Lei n.º X"), a extensão correta é um novo `tipo` em
`relacoes[]` (ex. `"remete-para"`, seguindo o padrão de extensão qualificada
de ADR-008), não uma variante de `xref`. Registado aqui para não se perder,
não proposto para decisão nesta ronda.

## 5. O que fica deliberadamente fora de âmbito nesta ronda

| Elemento | Razão |
|---|---|
| Âncoras inline (span-level) | Sem caso de uso documentado ainda — §3.5 |
| Referências inter-documento tipadas | Mecanismo distinto, já existe (`relacoes[]`) — §4 |
| Geração automática de rótulo/numeração a partir do `id` | Contradiria §3.2 — o NCRTF não computa texto, o produtor escreve-o |
| Resolução de `xref` através de composição (`composicao[]`, NDT §6) | Um documento composto a partir de vários NDF levanta a mesma pergunta de §4 num contexto diferente; decisão a acoplar a essa funcionalidade, não a esta |

## 6. Requisitos de conformidade candidatos

Não normativos nesta fase — para revisão quando N2 avançar para redação de
SPEC (Fase A, `ODF-ALIGNMENT-STUDY.md` §9).

Os identificadores abaixo são os reservados para A2 em
[`docs/roadmap/PLANO-NDT-NCRTF.md`](../roadmap/PLANO-NDT-NCRTF.md) §4. A SPEC
do NCRTF vai hoje até `NCRTF-PROD-007` e `NCRTF-READ-005`; `NCRTF-PROD-008` e
`NCRTF-READ-006` estão reservados para A1 (notas).

| Candidato | Enunciado |
|---|---|
| `NCRTF-PROD-009` | Um produtor **DEVE** garantir que todo `id` presente respeita a sintaxe de §3.1 e é único no documento (R8). |
| `NCRTF-PROD-010` | Um produtor **NÃO DEVE** incluir `xref` cujo `target` não resolva para um `id` existente no mesmo documento (R7). |
| `NCRTF-READ-007` | Um leitor **DEVE** rejeitar um NCRTF que viole R7 ou R8. |

## 7. Ligação ao plano faseado

Este documento é pré-requisito de redação de N2 (referências cruzadas) na
Fase A de `ODF-ALIGNMENT-STUDY.md` §9, ao lado de A1/A2/A4. §10 desse estudo
já registava "integridade das referências" como risco em aberto — este
documento é a resposta a esse risco, incluindo o ponto que ali faltava: a
confirmação de que o identificador é conteúdo assinado.
