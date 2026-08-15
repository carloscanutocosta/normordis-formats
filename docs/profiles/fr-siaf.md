# Perfil `fr-siaf` — França

**Estado:** documentado. Schema não publicado.
**Autoridade:** Service interministériel des Archives de France (SIAF).
**Fontes verificadas em:** 2026-08-15.

---

## 1. Base jurídica primária

| Instrumento | Conteúdo relevante |
|---|---|
| Code du patrimoine, art. **L212-2** | Terminada a utilização corrente, os arquivos públicos são objeto de seleção para separar o que se conserva do que, sem utilidade administrativa nem interesse histórico ou científico, deve ser eliminado. A lista e as condições de eliminação são fixadas por acordo entre a entidade e a administração dos arquivos. |
| Code du patrimoine, art. **R212-13** | Fixa, por acordo entre a entidade e o SIAF, **três** elementos: (1) a duração de utilização como arquivo corrente; (2) a duração de conservação como arquivo intermédio; (3) o **sort définitif** — eliminação imediata ou diferida, total ou parcial, com ou sem seleção; transferência como arquivo definitivo para um depósito de arquivos; ou conservação pela própria entidade. |
| Circular de **2 de novembro de 2001** | Os serviços seguem as instruções da administração dos arquivos que fixam as *durées d'utilité administrative* (DUA) e o destino final; na ausência delas, as regras são construídas conjuntamente com a administração dos arquivos. |

Existem instruções SIAF individualizadas por domínio, com código próprio — por
exemplo `DPACI/RES/2008/008`, classificada como *circulaire de tri*, que fixa
DUA para documentos contabilísticos.

## 2. Modelo arquivístico

```
utilisation courante  →  conservation intermédiaire  →  sort définitif
                                                          ├── élimination
                                                          ├── versement
                                                          └── conservation
```

A decisão é bilateral: fixada por acordo entre a entidade produtora e o SIAF,
tipicamente materializado num *tableau de gestion* ou numa instrução setorial.

## 3. Mapeamento NDF

| NDF | França |
|---|---|
| `perfil` | `fr-siaf` |
| `classificacao_ref` | série ou catégorie da instrução/tableau aplicável |
| `instrumento_ref` | instruction, circulaire de tri ou tableau de gestion, com referência e data |
| `prazo_conservacao` | DUA |
| `forma_contagem` | facto desencadeador fixado no instrumento |
| `destino_final` | `eliminacao` ← *élimination*; `conservacao_permanente` ← *versement* ou *conservation par le service*; `conservacao_parcial_por_amostragem` ← *tri* |
| `autoridade_avaliacao` | apenas se o instrumento remeter a decisão para o SIAF (`destino_final: "a_determinar"`) |

**Nota sobre `versement` e `conservation`.** O NDF funde as duas num único
`conservacao_permanente`. A distinção francesa é sobre *quem custodia* após o
prazo, não sobre *o que sucede ao documento* — e a custódia está fora do âmbito
do NDF-core (ADR-010). Se um caso real exigir distingui-las, o lugar é o perfil,
não o core.

## 4. O que um schema `fr-siaf` poderia impor

**Hoje, quase nada.** Não foi encontrada evidência de uma sintaxe nacional única
para referências de classificação, comparável a `lc/450.10.001` em Portugal: as
instruções SIAF usam codificações próprias por domínio. Um regex francês seria
invenção, não codificação.

Um schema `fr-siaf` deveria, no estado atual do conhecimento, limitar-se a:

- fixar `perfil` em `fr-siaf`;
- exigir `instrumento_ref` não vazio, com recomendação de incluir a referência
  formal da instrução (`DPACI/RES/2008/008`) e não apenas o seu nome corrente.

Restrições adicionais exigem levantamento das codificações efetivamente em uso
nos *tableaux de gestion*, que não foi feito.

## 5. Limitação — o teste mais exigente que o modelo enfrentou

O R212-13 estrutura a avaliação em **três** elementos, dos quais dois são
durações: `durée d'utilité courante` e `durée de conservation intermédiaire`. O
NDF-core tem um único `prazo_conservacao`.

Avaliação: **não há perda semântica para o efeito do NDF.** O que o NDF-core
existe para registar é o momento a partir do qual o documento fica elegível para
a aplicação do destino final, e esse momento é o termo da conservação
intermédia. A separação courante/intermédiaire distingue duas fases de *gestão*
do documento — nível de acesso, local de depósito, responsabilidade operacional
— e não dois momentos de decisão arquivística. Cai do lado operacional da
fronteira que a ADR-010 já traçou.

Isto **é**, ainda assim, o caso mais próximo de uma perda semântica encontrado
nos cinco regimes analisados, e é registado como tal. Se surgir evidência de que
uma entidade francesa precisa de exprimir as duas durações dentro do NDF-core —
por exemplo por o sort définitif ser condicionado à primeira e não à segunda —
essa evidência é argumento legítimo para reabrir o desenho de `prazo_conservacao`.
Até lá, aplica-se a regra do ADR-015: não abstrair por antecipação.

## 6. Fontes

- [Code du patrimoine, art. L212-2 — Légifrance](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019202835)
- [Code du patrimoine, art. R212-13 — Légifrance](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000042982395/2024-05-12)
- [Code du patrimoine, Paragraphe 2 : Collecte et conservation des archives publiques (R212-10 a R212-18-2) — Légifrance](https://www.legifrance.gouv.fr/codes/id/LEGISCTA000024240346)
- [Circulaire du 2 novembre 2001 relative à la gestion des archives dans les services et établissements publics de l'État — Légifrance](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000774334)
- [DPACI/RES/2008/008 — FranceArchives](https://francearchives.gouv.fr/fr/circulaire/DPACI_RES_2008_008)
