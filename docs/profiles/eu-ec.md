# Perfil `eu-ec` — Comissão Europeia

**Estado:** **experimental**. Schema não publicado. Instrumento integral não obtido.
**Autoridade:** Comissão Europeia.
**Fontes verificadas em:** 2026-08-15.

---

## 1. Base jurídica primária

| Instrumento | Conteúdo relevante |
|---|---|
| **Decisão (UE) 2021/2121 da Comissão**, de 6 de julho de 2020, relativa à gestão dos documentos de arquivo e aos arquivos, art. **15.º/1** | *"The retention period for the various categories of files and, in certain cases, records, shall be set for the whole Commission by way of regulatory instruments, such as the common retention list"* — os períodos de conservação são fixados para toda a Comissão por instrumentos regulamentares, designadamente a lista comum de conservação. |
| Mesma decisão, art. **15.º/2** | *"Directorates-general and equivalent departments shall regularly conduct an appraisal of records and files managed by them to assess whether they shall be transferred to the Commission's historical archives referred to in Article 16, or eliminated"* — as DG apreciam regularmente os documentos para decidir entre transferência para os Arquivos Históricos e eliminação. Mantém-se um conjunto de metadados como comprovativo das transferências e eliminações. |
| **SEC(2019)900** — *Common Commission-Level Retention List* | Identificada na legislação da UE como instrumento regulamentar que fixa os períodos de conservação dos tipos de processos da Comissão. |

**Nome do perfil.** `eu-ec` e não `eu-crl`: os restantes perfis nomeiam a
**autoridade** com competência sobre o regime, não o instrumento que ela
publica. Instrumentos mudam de edição e de nome; a autoridade é o que se mantém
estável ao longo da vida do documento. Pela mesma razão, não se usa `eu-generic`:
o regime é institucional e a fonte que se conseguiu confirmar é da Comissão, não
das instituições europeias em geral. O Parlamento, o Conselho e as agências têm
regimes próprios e exigiriam perfis distintos.

## 2. Modelo arquivístico

```
common retention list (SEC(2019)900) ou lista específica
            ↓
     retention period por categoria de processo
            ↓
     appraisal pela DG competente
            ↓
   ┌────────┴────────┐
transfer to          elimination
historical archives
```

Estruturalmente próximo do modelo alemão em dois pontos: a apreciação é um ato
posterior e distinto da fixação do prazo, e o destino resulta dessa apreciação.
Difere por a apreciação competir à própria DG produtora e não a uma autoridade
arquivística externa.

## 3. Mapeamento NDF

| NDF | Comissão Europeia |
|---|---|
| `perfil` | `eu-ec` |
| `classificacao_ref` | categoria de processo da retention list |
| `instrumento_ref` | `SEC(2019)900` ou lista específica aplicável |
| `prazo_conservacao` | retention period |
| `forma_contagem` | facto desencadeador fixado no instrumento |
| `destino_final` | `conservacao_permanente` ← transferência para os Arquivos Históricos; `eliminacao` ← eliminação; `a_determinar` quando a apreciação do art. 15.º/2 esteja pendente |
| `autoridade_avaliacao` | a DG competente, quando `a_determinar` |

## 4. Porque é que este perfil é **experimental** e não documentado

Os restantes perfis assentam em texto legal integralmente acessível. Aqui não:

**Não foi possível localizar uma versão pública, integral e oficialmente
publicada do SEC(2019)900.** Existem múltiplas páginas oficiais da Comissão que
o citam, e a legislação da UE que confirma a sua existência e função, mas não o
seu conteúdo normativo.

Consequência prática: é possível estabelecer a **estrutura** do perfil a partir
da Decisão 2021/2121, que está confirmada textualmente, mas **não** as
categorias, os códigos ou a sintaxe de `classificacao_ref`, que vivem no
instrumento que não se obteve. Um schema que os inventasse seria pior do que a
ausência de schema, porque daria aparência de fundamentação a conteúdo
fabricado.

## 5. O que falta para sair de experimental

1. Obter o SEC(2019)900 integral, ou a versão vigente que o substitua, por via
   oficial — eventualmente por pedido de acesso a documentos.
2. Confirmar se a codificação de categorias de processo tem forma estável
   passível de ser expressa em schema.
3. Confirmar o âmbito: se o regime cobre apenas a Comissão ou se outras
   instituições o aplicam por remissão.

Até lá, uma entidade da Comissão que queira produzir NDF usa
`perfil: "generic"`, que exige a estrutura e não impõe vocabulário.

## 6. Fontes

- [Decisão (UE) 2021/2121 da Comissão — EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32021D2121)
- [Decisão (UE) 2022/121 — EUR-Lex (identifica o SEC(2019)900)](https://eur-lex.europa.eu/eli/dec/2022/121/oj/eng)
- [Comissão Europeia — política de gestão documental e arquivo](https://commission.europa.eu/about/service-standards-and-principles/transparency/access-documents/information-and-document-management/archival-policy/document-management-and-archival-policy_en)
