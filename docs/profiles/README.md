# Perfis de avaliação arquivística — matriz de compatibilidade jurisdicional

**Estado:** informativo. Não normativo.
**Última verificação das fontes:** 2026-08-15.

O NDF-core fixa a **estrutura** da decisão de avaliação arquivística; o perfil
declarado em `avaliacao.perfil` fixa o **vocabulário** da jurisdição aplicável
(SPEC.md §3.2.3, ADR-015).

Estes documentos existem para responder a uma pergunta que um schema não
responde: *o modelo do NDF consegue representar honestamente o regime de cada
jurisdição, sem obrigar nenhuma a fingir que funciona como Portugal?*

---

## O critério

Para qualquer jurisdição, tem de ser possível exprimir sem ambiguidade:

1. **quem decide** o destino final;
2. **com base em que instrumento**;
3. **qual o prazo** de conservação;
4. **a partir de que facto** o prazo se conta;
5. **qual o destino final** — incluindo o caso em que ainda não está decidido.

Se um regime real exigir um conceito que não cabe nestas primitivas **sem perda
semântica**, isso é argumento para alterar o NDF-core. Caber com folga é
argumento para não lhe tocar.

---

## Matriz

| Conceito NDF | PT | FR | DE federal | NL | Comissão Europeia |
|---|---|---|---|---|---|
| `perfil` | `pt-dglab` | `fr-siaf` | `de-barch` | `nl-na` | `eu-ec` |
| Autoridade | DGLAB | Service interministériel des Archives de France | Bundesarchiv | Nationaal Archief | Comissão Europeia |
| `classificacao_ref` | classe da LC / TS / Portaria | série ou catégorie da instrução aplicável | categoria do Aktenplan | categoria da `selectielijst` | categoria da retention list |
| `instrumento_ref` | Lista Consolidada, Tabela de Seleção, Portaria | instruction, circulaire de tri, tableau de gestion | norma ou regra de retenção aplicável | `selectielijst` aprovada | `SEC(2019)900` ou lista específica |
| `prazo_conservacao` | PCA | DUA | Aufbewahrungsfrist | bewaartermijn | retention period |
| `forma_contagem` | definida no instrumento | definida no instrumento | definida na norma | definida na lista | definida no instrumento |
| Destino conhecido pelo produtor | normalmente sim | normalmente sim | **frequentemente não** | normalmente sim | nem sempre |
| `a_determinar` | possível | possível | **essencial** | possível | possível |
| `autoridade_avaliacao` | DGLAB, quando aplicável | Archives de France | **Bundesarchiv** | Nationaal Archief | Comissão / Arquivos Históricos |
| Sintaxe nacional imposta no schema | **sim** — `<instrumento>/<código>` | não evidenciada | não evidenciada | não evidenciada | não obtida |

---

## Resultado

A matriz fecha sem gambiarras nos cinco regimes. Duas observações valem mais do
que o resultado global:

**O caso alemão não é uma variante — é o que justifica `a_determinar`.** O §5 do
Bundesarchivgesetz atribui ao Bundesarchiv, e não ao produtor, a determinação do
`bleibender Wert`. Sem `destino_final: "a_determinar"`, um organismo federal
alemão não conseguiria produzir um NDF-core honesto: teria de declarar um
destino que não lhe compete decidir. Esta primitiva não é uma acomodação
cosmética.

**O caso francês é o que mais se aproxima de uma perda semântica.** Ver
[`fr-siaf.md`](fr-siaf.md) §5: o artigo R212-13 do Code du patrimoine estrutura
a avaliação em **três** elementos — duração como arquivo corrente, duração de
conservação intermédia e destino definitivo — enquanto o NDF-core tem um único
`prazo_conservacao`. A conclusão é que não há perda para o efeito do NDF, mas é
o teste mais exigente que o modelo enfrentou até agora e está registado como
tal.

---

## Estados dos perfis

| Perfil | Estado | Schema publicado | Fundamentação |
|---|---|---|---|
| `pt-dglab` | **registado** | [sim](../../specs/registry/profiles/pt-dglab.schema.json) | instrumentos DGLAB em uso no projeto |
| `generic` | **registado** | [sim](../../specs/registry/profiles/generic.schema.json) | sem restrições jurisdicionais, por desenho |
| `fr-siaf` | documentado | não | [fr-siaf.md](fr-siaf.md) — fonte primária confirmada |
| `de-barch` | documentado | não | [de-barch.md](de-barch.md) — fonte primária confirmada |
| `nl-na` | documentado | não | [nl-na.md](nl-na.md) — fonte primária confirmada |
| `eu-ec` | experimental | não | [eu-ec.md](eu-ec.md) — instrumento integral não obtido |

**Documentado** significa: base jurídica primária verificada e mapeamento para
o NDF estabelecido, sem schema publicado. É deliberado. Um schema de perfil
impõe sintaxe, e impor sintaxe exige saber que ela existe — o que só se
confirmou para Portugal. Publicar quatro schemas permissivos apenas para "ter
perfis" acrescentaria artefactos sem acrescentar garantia, e criaria a impressão
falsa de que o regime foi codificado quando apenas foi mapeado.

Um perfil passa a **registado** quando exista: fonte primária para as regras que
o schema imponha; e, preferencialmente, um interlocutor na jurisdição que
confirme o mapeamento.

Entretanto, uma entidade dessas jurisdições produz NDF válido com
`perfil: "generic"`, que exige a estrutura sem impor vocabulário nacional.

---

## Aviso sobre as fontes

Cada documento de perfil cita legislação primária, verificada na data indicada
no cabeçalho. Nenhuma destas leituras foi confirmada por um profissional de
arquivo ou jurista da jurisdição respetiva. O gate externo 3 da
[`READINESS.md`](../normalization/READINESS.md) — revisão arquivística — abrange
explicitamente esta matéria.

Legislação muda. Antes de qualquer perfil transitar para **registado**, as
fontes DEVEM ser reverificadas.
