# Perfil `pt-dglab` — Portugal

**Estado:** **registado**. [Schema publicado](../../specs/registry/profiles/pt-dglab.schema.json).
**Autoridade:** Direção-Geral do Livro, dos Arquivos e das Bibliotecas (DGLAB).
**Fontes verificadas em:** 2026-08-15.

---

## 1. Base

O perfil formaliza o modelo já usado pelo projeto antes da generalização do
bloco `avaliacao` (ADR-015): MEG e instrumentos da DGLAB — Lista Consolidada,
Tabelas de Seleção, Portarias de Gestão de Documentos.

A Lista Consolidada integra as decisões de avaliação dos processos de negócio da
Administração Pública numa perspetiva **suprainstitucional**. É esta
centralização que distingue Portugal dos restantes regimes analisados e que
torna possível impor sintaxe por schema — ver §4.

## 2. Modelo arquivístico

```
instrumento (LC / TS / Portaria)
   │
   └── classe ou série
          ├── PCA + forma de contagem
          └── Destino Final
                 ├── conservação permanente
                 ├── eliminação
                 └── conservação parcial por amostragem
```

Prazo e destino são conhecidos no momento da finalização, resolvidos a partir do
instrumento. O produtor não precisa de diferir a decisão — mas `a_determinar`
continua disponível se o instrumento não cobrir o caso.

## 3. Mapeamento NDF

| NDF | Portugal |
|---|---|
| `perfil` | `pt-dglab` |
| `classificacao_ref` | `<instrumento>/<codigo_classe>` — ex.: `lc/450.10.001` |
| `instrumento_ref` | `<instrumento>/<versao>` — ex.: `lc/lista-consolidada-dglab-2023-v3` |
| `prazo_conservacao` | PCA |
| `forma_contagem` | forma de contagem do instrumento |
| `destino_final` | conservação permanente / eliminação / conservação parcial por amostragem |

Prefixos canónicos de instrumento: `lc` (Lista Consolidada), `ts` (Tabela de
Seleção institucional), `portaria` (Portaria de Gestão de Documentos), `pgd`
(Plano de Gestão de Documentos).

## 4. O que o schema impõe

Ao contrário dos restantes perfis, aqui há sintaxe evidenciada e o schema
impõe-na:

| Regra | Onde |
|---|---|
| `classificacao_ref` no formato `^[a-z][a-z0-9-]*/[^/]+$` | schema do perfil |
| `instrumento_ref` no formato `^[a-z][a-z0-9-]*/[^/\s]+$` | schema do perfil |
| prefixo de `classificacao_ref` = instrumento de `instrumento_ref` | verificação semântica, `tools/validate.py` (SPEC.md §3.2.2) |

A última regra não é exprimível em JSON Schema — relaciona dois campos por
igualdade de prefixo — e por isso vive no validador, condicionada ao perfil.

Casos de conformidade que a exercem: `invalid-classificacao-ref` (sintaxe) e
`mismatched-instrument` (correspondência de instrumento).

## 5. Limitações

- Entidades com instrumentos próprios homologados pela DGLAB usam prefixos
  próprios; o schema aceita qualquer prefixo em minúsculas, sem validar que o
  instrumento existe. Verificar a existência do instrumento é responsabilidade
  do sistema produtor, não do formato.
- `metadados.entidade_produtora.codigo_dglab` continua no NDF-core como campo
  opcional específico de Portugal. Está sinalizado em [`LACUNAS.md`](../../LACUNAS.md)
  como candidato a generalização por lista de identificadores, sem ação prevista
  para 1.0 por ser opcional e não bloquear nenhuma jurisdição.

## 6. Fontes

- MEG — Modelo de Enquadramento para a Gestão de documentos, DGLAB
- Lista Consolidada para a Classificação e Avaliação da Informação Arquivística, DGLAB
- Portaria n.º 1253-A/2009 e demais Portarias de Gestão de Documentos aplicáveis
