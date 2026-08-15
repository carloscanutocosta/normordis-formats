# Perfil `de-barch` — Alemanha federal

**Estado:** documentado. Schema não publicado.
**Autoridade:** Bundesarchiv.
**Fontes verificadas em:** 2026-08-15.

---

## 1. Base jurídica primária

| Instrumento | Conteúdo relevante |
|---|---|
| **Bundesarchivgesetz (BArchG), §5** | Os organismos públicos federais **DEVEM oferecer** (`anbieten`) ao Bundesarchiv todos os documentos de que já não necessitem para as suas funções e cuja conservação não seja imposta por outra disposição legal. Como regra supletiva, o mais tardar **30 anos** após a criação. Para a determinação do `bleibender Wert` — o valor arquivístico permanente — os colaboradores do Bundesarchiv têm de obter acesso aos documentos oferecidos. Documentos sem valor permanente podem ser dispensados de oferta ou entrega. |
| **VV-ReVuS** e regulação setorial equivalente | Prazos de conservação concretos são fixados por normas administrativas e legais próprias — por exemplo dez anos para determinadas peças contabilísticas — com remissão para a `Registraturrichtlinie`. |

**Nome do perfil.** `de-barch` e não `de-bund`: o que se perfila é o regime sob
competência do **Bundesarchiv**, não o regime federal alemão em geral. Os Länder
têm leis arquivísticas próprias e arquivos próprios; se vierem a ser perfilados,
serão perfis distintos.

## 2. Modelo arquivístico

```
prazo legal/administrativo de conservação
            ↓
       Anbietung  (a entidade oferece)
            ↓
       Bewertung  (o Bundesarchiv aprecia)
            ↓
   ┌────────┴────────┐
Übernahme        Vernichtung
(valor permanente)  (sem valor permanente)
```

O ponto determinante para o NDF: **a decisão de destino final não pertence ao
produtor do documento**. No momento da finalização, o organismo federal conhece
o prazo — que resulta de norma — mas não conhece nem pode antecipar o destino.

## 3. Mapeamento NDF

| NDF | Alemanha federal |
|---|---|
| `perfil` | `de-barch` |
| `classificacao_ref` | categoria do Aktenplan aplicável |
| `instrumento_ref` | norma, regulamento ou regra de retenção que fixa o prazo |
| `prazo_conservacao` | Aufbewahrungsfrist |
| `forma_contagem` | fixada na norma; `fim_ano_civil` cobre o padrão `Ablauf des Kalenderjahres` sem acréscimos |
| `destino_final` | **`a_determinar`** no caso corrente |
| `autoridade_avaliacao` | `Bundesarchiv` |

Instância típica:

```json
{
  "avaliacao": {
    "perfil": "de-barch",
    "classificacao_ref": "aktenplan-2021/63-40-02",
    "prazo_conservacao": {
      "valor": 10,
      "unidade": "anos",
      "forma_contagem": "fim_ano_civil"
    },
    "destino_final": "a_determinar",
    "autoridade_avaliacao": "Bundesarchiv",
    "instrumento_ref": "vv-revus-2001"
  }
}
```

## 4. O que um schema `de-barch` poderia impor

Pouco, e deliberadamente:

- fixar `perfil` em `de-barch`;
- exigir `instrumento_ref` não vazio;
- possivelmente exigir `autoridade_avaliacao` sempre que `destino_final` seja
  `a_determinar` — mas isso já é regra do NDF-core, pelo que não acrescenta nada.

**Não existe uma retention schedule federal universal** comparável à Lista
Consolidada portuguesa. Os prazos vêm de legislação e regulamentação dispersas
por domínio. Um schema que impusesse uma sintaxe única de `classificacao_ref`
estaria a inventar uma centralização que o regime alemão não tem.

## 5. Limitações

- Cobre apenas o nível federal. Os Länder ficam de fora e exigiriam perfis
  próprios.
- Os Aktenpläne são específicos de cada organismo. Não há evidência de um
  esquema de codificação transversal que possa ser imposto por schema.
- O prazo de 30 anos do §5 é supletivo, não o prazo corrente: os prazos
  efetivos vêm das normas setoriais. Um perfil não deve tratar 30 anos como
  valor por omissão.

## 6. Relevância para o desenho do NDF

Este perfil é a justificação empírica de `destino_final: "a_determinar"`
(SPEC.md §3.4.1, ADR-015). Antes dessa primitiva, um organismo federal alemão só
produzia um NDF-core válido declarando um destino final que não tinha
competência para decidir — isto é, produzindo uma afirmação falsa dentro de um
documento assinado e imutável.

O caso alemão é, por isso, o argumento mais forte de que a generalização de
`avaliacao` não foi internacionalização cosmética: corrigiu uma hipótese
ontológica errada — a de que quem produz o documento sabe sempre qual será o
seu destino arquivístico.

## 7. Fontes

- [Bundesarchivgesetz, §5 — Gesetze im Internet](https://www.gesetze-im-internet.de/barchg_2017/__5.html)
- [VV-ReVuS — Verwaltungsvorschriften im Internet](https://www.verwaltungsvorschriften-im-internet.de/bsvwvbund_14032001_IIE3H300600011001001DOKCOO7005100211689780.htm)
- [Bundesarchiv — Aussonderung von Schriftgut aus der E-Akte Bund (V2.3, 2026-01-28)](https://www.bundesarchiv.de/assets/bundesarchiv/de/Downloads/Erklaerungen/2026-01-28_Aussonderung_Schriftgut_aus_EAB_V2.3.pdf)
