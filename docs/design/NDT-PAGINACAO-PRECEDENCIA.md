# Critério de resolução de paginação (NDT)

**Estado:** documento de desenho, não normativo. Fixa a direção antes de T2/T3
avançarem para redação de SPEC, conforme `ODF-ALIGNMENT-STUDY.md` §9 (Fase B).

**Origem:** pedido do responsável do projeto (2026-08-18), no seguimento da
revisão crítica que identificou a paginação como a maior dificuldade técnica
futura do NDT: T2 (`ODF-ALIGNMENT-STUDY.md`) regista que "o NDT não tem nada
nesta matéria", mas nomear as propriedades (`orphans`, `widows`,
`keep-with-next`, `keep-together`) não basta — sem uma ordem de resolução de
conflitos entre elas, dois renderizadores conformes podem produzir páginas
diferentes e ambos alegar conformidade. Âmbito confirmado: documentos
administrativos e legais/normativos, onde a qualidade de paginação (sem
títulos isolados, com áreas de notas de rodapé reservadas) é requisito de
publicação, não só de estética — ver `specs/ndt/SPEC.md` §Âmbito.

---

## 1. Porque uma lista de propriedades não é suficiente

Propriedades de paginação entram frequentemente em conflito entre si e com o
espaço físico disponível. Exemplo de trabalho (retomado em §7):

```
heading:    keep_with_next = true
paragraph:  keep_together = true, orphans = 3, widows = 3
footnote:   45 mm de altura
página:     restam 30 mm no fim
```

Não há forma de satisfazer tudo. **Uma especificação que declare
propriedades sem declarar a ordem em que cedem não é uma especificação de
paginação — é uma lista de intenções.** O teste de conformidade de NDT §9.1
("o mesmo NDT + NDF produz uma representação semanticamente equivalente")
falha silenciosamente aqui: dois renderizadores podem ambos alegar que
respeitam `keep_with_next`, `orphans` e `widows`, e ainda assim produzirem
páginas visivelmente diferentes, porque cada um resolveu o conflito à sua
maneira.

Este documento propõe o algoritmo — não só o vocabulário.

## 2. Camada e nível

Aplicando a hierarquia de `CRITERIO-DE-CAMADAS.md` §4: paginação é
apresentação (é *como se vê*, não *o que é*), logo **NDT**. Mas falta-lhe um
nível: o NDT tem hoje estilo de página (`paginas_def`, §5.2 SPEC) mas não
estilo de parágrafo. `ODF-ALIGNMENT-STUDY.md` §7.2 já identificou esta falta
ao mapear o ODF (`style:style` de parágrafo vs. `style:page-layout` de
página). As propriedades desta secção pertencem ao **nível de parágrafo**,
tal como aí proposto — não ao nível de página nem ao NCRTF: são qualidade de
composição, não conteúdo (caso já resolvido em `CRITERIO-DE-CAMADAS.md` §9,
"viúvas, órfãs, manter-junto → NDT").

## 3. Vocabulário

Inspirado em XSL-FO / ODF (`fo:orphans`, `fo:widows`, `fo:keep-with-next`,
`fo:keep-together`), declarado por `role` ou por tipo de nó, no novo nível de
parágrafo dos `estilos` do NDT:

| Propriedade | Tipo | Significado |
|---|---|---|
| `keep_together` | `bool` \| `"auto"` | O bloco não deve ser dividido entre páginas, se couber inteiro nalguma página. |
| `keep_with_next` | `bool` | O bloco não deve ficar separado do bloco seguinte por uma quebra de página. |
| `orphans` | inteiro ≥ 1 | Mínimo de linhas de um parágrafo que **DEVEM** ficar no fundo de uma página, se o parágrafo for dividido. |
| `widows` | inteiro ≥ 1 | Mínimo de linhas de um parágrafo que **DEVEM** ficar no topo da página seguinte, se o parágrafo for dividido. |

Estas quatro propriedades **não** resolvem sozinhas o problema — são o
vocabulário de entrada do algoritmo de §4, não o algoritmo.

## 4. Algoritmo de resolução — ordem de precedência normativa

A composição de uma página, ao encontrar o próximo bloco a colocar, aplica
esta ordem. Cada passo só é avaliado se o anterior não determinar já a
decisão.

1. **Preservar conteúdo.** Nenhum bloco de conteúdo é omitido ou truncado
   silenciosamente. Não é uma regra que cede — é o invariante sob o qual
   todas as outras operam.
2. **Nunca ultrapassar a área de página definida.** A geometria de
   `paginas_def`/`layout` é um limite físico, não uma preferência.
3. **`keep_together`**, se o bloco cabe inteiro nalguma página (a atual ou a
   seguinte). Se o bloco for maior do que a área útil de qualquer página —
   `keep_together` é **impossível de satisfazer por construção** — degrada
   para o passo 5 (quebra o bloco, aplicando `widows`/`orphans` ao que
   resulta) e o renderizador **DEVE** poder sinalizar esta degradação, sem
   que isso constitua erro de conformidade: a alternativa seria perder
   conteúdo, o que o passo 1 proíbe.
4. **`keep_with_next`**, se o bloco e o seguinte cabem juntos no espaço
   restante da página atual. Se não cabem, o par move-se inteiro para a
   página seguinte — nunca se separa à força por overflow. Se o par for
   maior do que a área útil de qualquer página, degrada para o passo 5 pela
   mesma razão do passo 3.
5. **`orphans`/`widows`**, aplicadas apenas ao ponto de quebra dentro de um
   parágrafo que já vai ser dividido (porque não coube em `keep_together`,
   ou não tem essa propriedade). Restringem *onde* a quebra pode cair —
   nunca decidem *se* há quebra.
6. **Área de notas de rodapé (T3) compete pelo mesmo espaço restante da
   página**, com prioridade sobre o corpo: se uma nota ancorada a um trecho
   já colocado na página não couber no espaço que resta, o renderizador
   **DEVE** recuar — mover para a página seguinte o trecho que ancora a
   nota (e a própria nota com ele) — nunca cortar o texto da nota. É a razão
   pela qual o passo 6 vem depois de 3–5: só se decide o que fica na página
   depois de saber quanto espaço as notas dessa página vão exigir, o que só
   se sabe depois de saber que conteúdo ficou nela — por isso a composição é
   iterativa: coloca-se conteúdo, calcula-se a área de notas necessária, e
   recua-se o que não couber.
7. **Fallback normativamente definido.** Esgotadas as regras 3–6 sem solução
   que as satisfaça todas, cede-se pela ordem inversa da lista: primeiro
   `widows`/`orphans` (perder uma linha órfã é o dano estético menor),
   depois `keep_with_next` (separar título do corpo é pior, mas não parte um
   bloco), só por fim `keep_together` (partir um bloco explicitamente
   marcado como indivisível — ex. uma tabela pequena a meio — é o pior
   resultado e só ocorre quando fisicamente inevitável).

A regra observável e testável, resumida: **preservar > geometria >
keep_together > keep_with_next > notas de rodapé > widows/orphans**, com
degradação em cascata inversa quando o espaço físico não permite satisfazer
tudo.

## 5. Caso de trabalho resolvido

Retomando o exemplo de §1: heading com `keep_with_next`, parágrafo com
`keep_together` + `orphans=3` + `widows=3`, nota de rodapé de 45 mm, 30 mm
restantes no fundo da página.

1. Passo 2: 30 mm não chegam para o parágrafo completo nem para a nota de
   45 mm — há overflow garantido nalgum ponto.
2. Passo 3 (`keep_together` do parágrafo): testa-se se o parágrafo cabe
   inteiro na página seguinte (não na atual, que só tem 30 mm). Cabe
   inteiro na próxima página → mover o parágrafo inteiro para lá.
3. Passo 4 (`keep_with_next` do heading): o heading já está colocado antes
   do parágrafo. Se o parágrafo desloca para a página seguinte, o heading
   **também** desloca — senão fica separado do que o segue, violando
   `keep_with_next`. Resultado: heading + parágrafo, ambos na página
   seguinte.
4. Passo 6 (nota de rodapé): a nota estava ancorada a um trecho que já não
   está nesta página (moveu com o parágrafo) — a nota move com ele. Os
   30 mm da página atual ficam livres para o bloco anterior continuar, ou
   para a página fechar mais cedo.
5. Passo 5 (`orphans`/`widows`): não chega a ser avaliado — o parágrafo não
   foi dividido, moveu-se inteiro. `orphans`/`widows` só entram quando o
   parágrafo *tem* de ser dividido porque nem a página atual nem a seguinte
   o comportam inteiro.

O resultado é determinístico e replicável por qualquer renderizador que
implemente a mesma ordem — que é precisamente o que falta hoje.

## 6. O que esta secção não resolve, deliberadamente

Quebra de página condicionada por valor de dados (`if total < 0`, `if
tipo == "subtotal"`) permanece excluída — é lógica de negócio, já fora de
âmbito por decisão anterior (mesma linha de raciocínio de T2 no roadmap
sobre agrupamento de tabelas). O algoritmo aqui descrito reage à geometria
do conteúdo já materializado pelo NDF, nunca ao seu valor semântico.

## 7. Requisitos de conformidade candidatos

Não normativos nesta fase — para revisão quando T2/T3 avançarem para
redação de SPEC (Fase B, `ODF-ALIGNMENT-STUDY.md` §9).

| Candidato | Enunciado |
|---|---|
| `NDT-RENDER-XXX` | Um renderizador de fluxo **DEVE** resolver conflitos entre `keep_together`, `keep_with_next`, `orphans`/`widows` e a área de notas de rodapé pela ordem de precedência de §4. |
| `NDT-RENDER-XXX` | Um renderizador **NÃO DEVE** truncar ou omitir conteúdo para satisfazer `keep_together` ou `keep_with_next` (passo 1 é invariante). |
| `NDT-RENDER-XXX` | Um renderizador **PODE** sinalizar (fora do documento produzido, ex. em log) os pontos onde `keep_together` degradou por o bloco exceder a área útil de página (passo 3). |

## 8. Ligação ao plano faseado

Este documento é pré-requisito de redação de T2/T3 na Fase B de
`ODF-ALIGNMENT-STUDY.md` §9. O nível de parágrafo em `estilos` (§2 deste
documento) é também pré-requisito de T4/A3 (estilos nomeados, Fase C), que já
previa dois níveis — página e parágrafo — em §7.2 desse estudo.
